#!/usr/bin/env python3
"""Read Google Docs and perform one exact, revision-guarded replacement."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

import google_oauth


DOCS_API = "https://docs.googleapis.com/v1/documents"


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def required_env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"{name} is required; set it in .env or the current environment")
    return os.path.expanduser(value)


def api_json(method, url, access_token, body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Google Docs API returned HTTP {exc.code}: {detail}") from exc


def get_document(document_id, access_token):
    url = f"{DOCS_API}/{urllib.parse.quote(document_id)}?includeTabsContent=true"
    return api_json("GET", url, access_token)


def structural_text(elements):
    chunks = []
    for element in elements or []:
        paragraph = element.get("paragraph")
        if paragraph:
            for paragraph_element in paragraph.get("elements", []):
                text_run = paragraph_element.get("textRun")
                if text_run:
                    chunks.append(text_run.get("content", ""))
        table = element.get("table")
        if table:
            for row in table.get("tableRows", []):
                for cell in row.get("tableCells", []):
                    chunks.append(structural_text(cell.get("content", [])))
        toc = element.get("tableOfContents")
        if toc:
            chunks.append(structural_text(toc.get("content", [])))
    return "".join(chunks)


def utf16_length(value):
    return len(value.encode("utf-16-le")) // 2


def structural_text_with_spans(elements):
    chunks = []
    spans = []
    for element in elements or []:
        paragraph = element.get("paragraph")
        if paragraph:
            for paragraph_element in paragraph.get("elements", []):
                text_run = paragraph_element.get("textRun")
                if not text_run:
                    continue
                content = text_run.get("content", "")
                index = paragraph_element.get("startIndex")
                if index is None:
                    raise ValueError("Google Docs text run is missing startIndex")
                chunks.append(content)
                for character in content:
                    next_index = index + utf16_length(character)
                    spans.append((index, next_index))
                    index = next_index
        table = element.get("table")
        if table:
            for row in table.get("tableRows", []):
                for cell in row.get("tableCells", []):
                    text, cell_spans = structural_text_with_spans(cell.get("content", []))
                    chunks.append(text)
                    spans.extend(cell_spans)
        toc = element.get("tableOfContents")
        if toc:
            text, toc_spans = structural_text_with_spans(toc.get("content", []))
            chunks.append(text)
            spans.extend(toc_spans)
    return "".join(chunks), spans


def structural_links(elements):
    links = []
    for element in elements or []:
        paragraph = element.get("paragraph")
        if paragraph:
            for paragraph_element in paragraph.get("elements", []):
                text_run = paragraph_element.get("textRun")
                link = (text_run or {}).get("textStyle", {}).get("link", {})
                if text_run and link.get("url"):
                    links.append({"text": text_run.get("content", ""), "url": link["url"]})
        table = element.get("table")
        if table:
            for row in table.get("tableRows", []):
                for cell in row.get("tableCells", []):
                    links.extend(structural_links(cell.get("content", [])))
        toc = element.get("tableOfContents")
        if toc:
            links.extend(structural_links(toc.get("content", [])))
    return links


def walk_tabs(tabs):
    for tab in tabs or []:
        properties = tab.get("tabProperties", {})
        document_tab = tab.get("documentTab", {})
        body = document_tab.get("body", {})
        text, spans = structural_text_with_spans(body.get("content", []))
        yield {
            "id": properties.get("tabId", ""),
            "title": properties.get("title", "Untitled tab"),
            "text": text,
            "spans": spans,
            "links": structural_links(body.get("content", [])),
        }
        yield from walk_tabs(tab.get("childTabs", []))


def document_tabs(document):
    tabs = list(walk_tabs(document.get("tabs", [])))
    if tabs:
        return tabs
    text, spans = structural_text_with_spans(document.get("body", {}).get("content", []))
    body = document.get("body", {})
    return [{"id": "", "title": "Document", "text": text, "spans": spans, "links": structural_links(body.get("content", []))}]


def selected_tabs(document, tab_ids):
    tabs = document_tabs(document)
    if not tab_ids:
        return tabs
    wanted = set(tab_ids)
    selected = [tab for tab in tabs if tab["id"] in wanted]
    missing = wanted - {tab["id"] for tab in selected}
    if missing:
        raise ValueError(f"Unknown tab ID(s): {', '.join(sorted(missing))}")
    return selected


def text_argument(value, path, label):
    if value is not None:
        return value
    if path is not None:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    raise ValueError(f"{label} text is required")


def document_id_from(args):
    document_id = (args.document_id or os.environ.get("OPEN_AUSTIN_WEEKLY_NOTES_DOC_ID", "")).strip()
    if not document_id:
        raise ValueError("Provide --document-id or set OPEN_AUSTIN_WEEKLY_NOTES_DOC_ID")
    return document_id


def access_token():
    credentials_path = required_env("GOOGLE_CLIENT_CREDENTIALS_PATH")
    token_path = required_env("GOOGLE_TOKEN_PATH")
    return google_oauth.get_access_token(credentials_path, token_path)


def command_read(args):
    document_id = document_id_from(args)
    document = get_document(document_id, access_token())
    print(f"# {document.get('title', 'Untitled document')}")
    print(f"Document ID: {document_id}")
    print(f"Revision ID: {document.get('revisionId', '<missing>')}")
    for tab in selected_tabs(document, args.tab_id):
        print(f"\n## {tab['title']} [{tab['id'] or 'first-tab'}]\n")
        print(tab["text"], end="" if tab["text"].endswith("\n") else "\n")
        if args.show_links:
            print("\nEmbedded links:")
            for link in tab["links"]:
                print(f"- {link['text']} -> {link['url']}")
    return 0


def count_matches(document, tab_ids, old_text):
    return sum(tab["text"].count(old_text) for tab in selected_tabs(document, tab_ids))


def exact_text_range(document, tab_ids, value):
    matches = []
    for tab in selected_tabs(document, tab_ids):
        position = tab["text"].find(value)
        while position >= 0:
            matches.append((tab, position))
            position = tab["text"].find(value, position + 1)
    if len(matches) != 1:
        raise ValueError(f"Exact text must occur once in the selected scope; found {len(matches)}")
    tab, position = matches[0]
    end_position = position + len(value)
    if not value or end_position > len(tab["spans"]):
        raise ValueError("Unable to resolve the exact text to Google Docs indices")
    return {
        "tab_id": tab["id"],
        "start_index": tab["spans"][position][0],
        "end_index": tab["spans"][end_position - 1][1],
    }


def parse_link_specs(specs, new_text):
    links = []
    occupied = []
    for spec in specs or []:
        label, separator, url = spec.partition("=")
        label = label.strip()
        url = url.strip()
        if not separator or not label or not url:
            raise ValueError("Each --link must use the form 'visible text=https://example.com'")
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"Link URL must be HTTP(S): {url}")
        if new_text.count(label) != 1:
            raise ValueError(f"Link text must occur once in the replacement text: {label!r}")
        start = new_text.index(label)
        end = start + len(label)
        if any(start < other_end and other_start < end for other_start, other_end in occupied):
            raise ValueError(f"Link text overlaps another link: {label!r}")
        occupied.append((start, end))
        links.append({"label": label, "url": url, "start": start, "end": end})
    return links


def link_style_requests(old_range, new_text, links):
    requests = []
    for link in links:
        start_index = old_range["start_index"] + utf16_length(new_text[: link["start"]])
        end_index = old_range["start_index"] + utf16_length(new_text[: link["end"]])
        range_value = {"startIndex": start_index, "endIndex": end_index}
        if old_range["tab_id"]:
            range_value["tabId"] = old_range["tab_id"]
        requests.append(
            {
                "updateTextStyle": {
                    "range": range_value,
                    "textStyle": {"link": {"url": link["url"]}},
                    "fields": "link",
                }
            }
        )
    return requests


def print_replacement_plan(document, document_id, tab_ids, old_text, new_text, links):
    print("Google Docs exact replacement plan:")
    print(f"Document: {document.get('title', 'Untitled document')} ({document_id})")
    print(f"Revision read: {document.get('revisionId', '<missing>')}")
    print(f"Tabs: {', '.join(tab_ids) if tab_ids else '<all tabs>'}")
    print("--- current exact text ---")
    print(old_text)
    print("--- proposed replacement ---")
    print(new_text)
    if links:
        print("--- embedded links ---")
        for link in links:
            print(f"{link['label']} -> {link['url']}")
    print("--- end plan ---")


def command_replace_once(args):
    document_id = document_id_from(args)
    old_text = text_argument(args.old, args.old_file, "Old")
    new_text = text_argument(args.new, args.new_file, "New")
    if not old_text:
        raise ValueError("Old text must not be empty")
    token = access_token()
    document = get_document(document_id, token)
    matches = count_matches(document, args.tab_id, old_text)
    if matches != 1:
        raise ValueError(f"Exact old text must occur once in the selected scope; found {matches}")
    links = parse_link_specs(args.link, new_text)
    old_range = exact_text_range(document, args.tab_id, old_text)
    print_replacement_plan(document, document_id, args.tab_id, old_text, new_text, links)
    if not args.execute:
        print("DRY RUN: no Google Doc was changed. Re-run with --execute after approval.")
        return 0

    live_document = get_document(document_id, token)
    live_matches = count_matches(live_document, args.tab_id, old_text)
    if live_matches != 1:
        raise ValueError(f"Document changed before execution; exact old text now occurs {live_matches} times")
    revision_id = live_document.get("revisionId")
    if not revision_id:
        raise ValueError("Google Docs response did not include a revisionId")
    live_old_range = exact_text_range(live_document, args.tab_id, old_text)
    if live_old_range != old_range:
        raise ValueError("Document changed before execution; exact text moved to a different range")
    replace_request = {
        "replaceText": new_text,
        "containsText": {"text": old_text, "matchCase": True, "searchByRegex": False},
    }
    if args.tab_id:
        replace_request["tabsCriteria"] = {"tabIds": args.tab_id}
    requests = [{"replaceAllText": replace_request}]
    requests.extend(link_style_requests(live_old_range, new_text, links))
    payload = {
        "requests": requests,
        "writeControl": {"requiredRevisionId": revision_id},
    }
    url = f"{DOCS_API}/{urllib.parse.quote(document_id)}:batchUpdate"
    result = api_json("POST", url, token, payload)
    responses = result.get("replies") or result.get("responses") or []
    changed = 0
    for response in responses:
        changed += response.get("replaceAllText", {}).get("occurrencesChanged", 0)
    if changed != 1:
        raise RuntimeError(f"Google reported {changed} replacements; expected exactly 1")
    print(f"Updated document at revision {result.get('writeControl', {}).get('requiredRevisionId', revision_id)}; replacements: {changed}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    read_parser = subparsers.add_parser("read", help="Render document text")
    read_parser.add_argument("--document-id")
    read_parser.add_argument("--tab-id", action="append", default=[])
    read_parser.add_argument("--show-links", action="store_true")
    read_parser.set_defaults(func=command_read)

    replace_parser = subparsers.add_parser("replace-once", help="Replace one exact text occurrence; dry-run by default")
    replace_parser.add_argument("--document-id")
    old_group = replace_parser.add_mutually_exclusive_group(required=True)
    old_group.add_argument("--old")
    old_group.add_argument("--old-file")
    new_group = replace_parser.add_mutually_exclusive_group(required=True)
    new_group.add_argument("--new")
    new_group.add_argument("--new-file")
    replace_parser.add_argument("--tab-id", action="append", default=[])
    replace_parser.add_argument(
        "--link",
        action="append",
        default=[],
        metavar="TEXT=URL",
        help="Embed a link on uniquely occurring visible text in the replacement; repeatable",
    )
    replace_parser.add_argument("--execute", action="store_true")
    replace_parser.set_defaults(func=command_replace_once)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
