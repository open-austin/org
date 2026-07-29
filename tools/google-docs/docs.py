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


def walk_tabs(tabs):
    for tab in tabs or []:
        properties = tab.get("tabProperties", {})
        document_tab = tab.get("documentTab", {})
        body = document_tab.get("body", {})
        yield {
            "id": properties.get("tabId", ""),
            "title": properties.get("title", "Untitled tab"),
            "text": structural_text(body.get("content", [])),
        }
        yield from walk_tabs(tab.get("childTabs", []))


def document_tabs(document):
    tabs = list(walk_tabs(document.get("tabs", [])))
    if tabs:
        return tabs
    return [{"id": "", "title": "Document", "text": structural_text(document.get("body", {}).get("content", []))}]


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
    return 0


def count_matches(document, tab_ids, old_text):
    return sum(tab["text"].count(old_text) for tab in selected_tabs(document, tab_ids))


def print_replacement_plan(document, document_id, tab_ids, old_text, new_text):
    print("Google Docs exact replacement plan:")
    print(f"Document: {document.get('title', 'Untitled document')} ({document_id})")
    print(f"Revision read: {document.get('revisionId', '<missing>')}")
    print(f"Tabs: {', '.join(tab_ids) if tab_ids else '<all tabs>'}")
    print("--- current exact text ---")
    print(old_text)
    print("--- proposed replacement ---")
    print(new_text)
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
    print_replacement_plan(document, document_id, args.tab_id, old_text, new_text)
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
    replace_request = {
        "replaceText": new_text,
        "containsText": {"text": old_text, "matchCase": True, "searchByRegex": False},
    }
    if args.tab_id:
        replace_request["tabsCriteria"] = {"tabIds": args.tab_id}
    payload = {
        "requests": [{"replaceAllText": replace_request}],
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
