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


def paragraph(text):
    return {"paragraph": {"elements": [{"textRun": {"content": text}}]}}


class DocumentTextTests(unittest.TestCase):
    def setUp(self):
        self.document = {
            "tabs": [
                {
                    "tabProperties": {"tabId": "tab-a", "title": "July 27"},
                    "documentTab": {"body": {"content": [paragraph("Action one\n"), paragraph("Action two\n")]}},
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


if __name__ == "__main__":
    unittest.main()
