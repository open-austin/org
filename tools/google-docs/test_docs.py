#!/usr/bin/env python3

import importlib.util
import pathlib
import sys
import unittest


MODULE_PATH = pathlib.Path(__file__).with_name("docs.py")
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("open_austin_google_docs", MODULE_PATH)
DOCS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DOCS)


def paragraph(text, start_index=1):
    return {
        "paragraph": {
            "elements": [
                {
                    "startIndex": start_index,
                    "endIndex": start_index + DOCS.utf16_length(text),
                    "textRun": {"content": text},
                }
            ]
        }
    }


class DocumentTextTests(unittest.TestCase):
    def setUp(self):
        self.document = {
            "tabs": [
                {
                    "tabProperties": {"tabId": "tab-a", "title": "July 27"},
                    "documentTab": {"body": {"content": [paragraph("Action one\n", 1), paragraph("Action two\n", 12)]}},
                    "childTabs": [],
                },
                {
                    "tabProperties": {"tabId": "tab-b", "title": "July 20"},
                    "documentTab": {"body": {"content": [paragraph("Older action\n")]}},
                    "childTabs": [],
                },
            ]
        }

    def test_extracts_each_tab(self):
        tabs = DOCS.document_tabs(self.document)
        self.assertEqual([tab["id"] for tab in tabs], ["tab-a", "tab-b"])
        self.assertEqual(tabs[0]["text"], "Action one\nAction two\n")

    def test_counts_matches_in_selected_tab(self):
        self.assertEqual(DOCS.count_matches(self.document, ["tab-a"], "Action"), 2)
        self.assertEqual(DOCS.count_matches(self.document, ["tab-b"], "Older action"), 1)

    def test_rejects_unknown_tab(self):
        with self.assertRaises(ValueError):
            DOCS.selected_tabs(self.document, ["missing"])

    def test_resolves_exact_text_to_document_range(self):
        result = DOCS.exact_text_range(self.document, ["tab-a"], "Action two")
        self.assertEqual(result, {"tab_id": "tab-a", "start_index": 12, "end_index": 22})

    def test_parses_links_and_builds_style_requests(self):
        new_text = "Review Casa #481 and Food #475"
        links = DOCS.parse_link_specs(
            ["Casa #481=https://github.com/open-austin/org/issues/481", "Food #475=https://github.com/open-austin/org/issues/475"],
            new_text,
        )
        requests = DOCS.link_style_requests(
            {"tab_id": "tab-a", "start_index": 40, "end_index": 50},
            new_text,
            links,
        )
        self.assertEqual(requests[0]["updateTextStyle"]["range"], {"startIndex": 47, "endIndex": 56, "tabId": "tab-a"})
        self.assertEqual(requests[1]["updateTextStyle"]["textStyle"]["link"]["url"], "https://github.com/open-austin/org/issues/475")

    def test_rejects_non_unique_or_overlapping_link_text(self):
        with self.assertRaises(ValueError):
            DOCS.parse_link_specs(["Issue=https://example.com"], "Issue and Issue")
        with self.assertRaises(ValueError):
            DOCS.parse_link_specs(["Casa #481=https://example.com", "#481=https://example.org"], "Casa #481")

    def test_utf16_length_counts_astral_characters(self):
        self.assertEqual(DOCS.utf16_length("A😀B"), 4)

    def test_extracts_embedded_links(self):
        elements = [
            {
                "paragraph": {
                    "elements": [
                        {
                            "startIndex": 1,
                            "endIndex": 10,
                            "textRun": {
                                "content": "Casa #481",
                                "textStyle": {"link": {"url": "https://github.com/open-austin/org/issues/481"}},
                            },
                        }
                    ]
                }
            }
        ]
        self.assertEqual(
            DOCS.structural_links(elements),
            [{"text": "Casa #481", "url": "https://github.com/open-austin/org/issues/481"}],
        )


if __name__ == "__main__":
    unittest.main()
