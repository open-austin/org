#!/usr/bin/env python3
"""
Render snapshot/weekly-summary.md as a Slack Incoming Webhook payload.

The weekly summary remains a readable plain-text artifact for review. This
script converts that simple Slack-flavored markdown into Block Kit rich_text
blocks so Slack renders real bullet lists instead of text-only hyphen lines.
"""

import argparse
import json
import re
import sys
from pathlib import Path


BULLET_RE = re.compile(r"^(?P<spaces> *)- (?P<text>.*)$")
LINK_RE = re.compile(r"<(?P<url>[^|>]+)\|(?P<label>[^>]+)>")


def is_emphasis_line(line):
    return line.startswith("*") and line.endswith("*") and len(line) > 2


def strip_emphasis(line):
    return line[1:-1]


def text_element(text, style=None):
    element = {"type": "text", "text": text}
    if style:
        element["style"] = style
    return element


def link_element(url, label):
    return {"type": "link", "url": url, "text": label}


def append_text(elements, text, style=None):
    if text:
        elements.append(text_element(text, style))


def parse_inline(text):
    """Parse the small subset of Slack mrkdwn used by weekly summaries."""
    elements = []
    position = 0

    while position < len(text):
        link_match = LINK_RE.match(text, position)
        if link_match:
            elements.append(link_element(link_match.group("url"), link_match.group("label")))
            position = link_match.end()
            continue

        if text[position] == "*":
            end = text.find("*", position + 1)
            if end > position + 1:
                append_text(elements, text[position + 1:end], {"bold": True})
                position = end + 1
                continue

        next_link = text.find("<", position + 1)
        next_bold = text.find("*", position + 1)
        candidates = [idx for idx in (next_link, next_bold) if idx != -1]
        next_special = min(candidates) if candidates else len(text)
        append_text(elements, text[position:next_special])
        position = next_special

    return elements or [text_element(" ")]


def rich_text_section(text):
    return {"type": "rich_text_section", "elements": parse_inline(text)}


def rich_text_block(elements):
    return {"type": "rich_text", "elements": elements}


def header_block(text):
    return {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": text[:150],
            "emoji": True,
        },
    }


def markdown_text_block(text):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text,
        },
    }


def parse_bullet(line):
    match = BULLET_RE.match(line)
    if not match:
        return None

    # The weekly-summary template uses two spaces per nesting level.
    return len(match.group("spaces")) // 2, match.group("text")


def list_elements(bullets):
    elements = []
    current_indent = None
    current_sections = []

    def flush():
        nonlocal current_indent, current_sections
        if not current_sections:
            return
        item = {
            "type": "rich_text_list",
            "style": "bullet",
            "elements": current_sections,
        }
        if current_indent:
            item["indent"] = current_indent
        elements.append(item)
        current_indent = None
        current_sections = []

    for indent, text in bullets:
        if current_indent is None:
            current_indent = indent
        elif indent != current_indent:
            flush()
            current_indent = indent

        current_sections.append(rich_text_section(text))

    flush()
    return elements


def render_payload(markdown):
    lines = [line.rstrip() for line in markdown.splitlines()]
    blocks = []
    index = 0

    while index < len(lines):
        line = lines[index]

        if not line:
            index += 1
            continue

        bullet = parse_bullet(line)
        if bullet:
            bullets = []
            while index < len(lines):
                parsed = parse_bullet(lines[index])
                if not parsed:
                    break
                bullets.append(parsed)
                index += 1
            blocks.append(rich_text_block(list_elements(bullets)))
            continue

        if is_emphasis_line(line):
            text = strip_emphasis(line)
            if not blocks:
                blocks.append(header_block(text))
            else:
                blocks.append(markdown_text_block(f"*{text}*"))
            index += 1
            continue

        paragraphs = []
        while index < len(lines):
            candidate = lines[index]
            if not candidate or parse_bullet(candidate) or is_emphasis_line(candidate):
                break
            paragraphs.append(candidate)
            index += 1

        blocks.append(rich_text_block([rich_text_section("\n".join(paragraphs))]))

    return {
        "text": plain_text_fallback(markdown),
        "blocks": blocks,
    }


def plain_text_fallback(markdown):
    lines = []
    for line in markdown.splitlines():
        if is_emphasis_line(line):
            lines.append(strip_emphasis(line))
        else:
            lines.append(line)
    return "\n".join(lines).strip()


def main():
    parser = argparse.ArgumentParser(
        description="Render a weekly summary markdown file as Slack Block Kit JSON."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="snapshot/weekly-summary.md",
        help="Weekly summary markdown file. Defaults to snapshot/weekly-summary.md.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write JSON payload to this file. Defaults to stdout.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    markdown = input_path.read_text()
    payload = render_payload(markdown)
    output = json.dumps(payload, indent=2) + "\n"

    if args.output:
        Path(args.output).write_text(output)
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
