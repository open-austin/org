"""Offline send-boundary tests. A fake curl prevents every network request."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('post.sh')


class NotifyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.log = self.root / 'curl.json'
        fake = self.root / 'curl'
        fake.write_text('#!/usr/bin/env python3\nimport json, os, pathlib, sys\npathlib.Path(os.environ["CURL_LOG"]).write_text(json.dumps(sys.argv[1:]))\nsys.exit(int(os.environ.get("CURL_EXIT", "0")))\n')
        fake.chmod(0o755)
        # Do not inherit service credentials from the invoking environment.
        self.env = {'PATH': str(self.root) + os.pathsep + os.environ['PATH'], 'CURL_LOG': str(self.log)}
        self.payload = self.root / 'payload.json'
        self.payload.write_text(json.dumps({'text': 'Synthetic fallback', 'blocks': [{'type': 'divider'}]}))

    def run_tool(self, *args, stdin=''):
        return subprocess.run(['bash', str(SCRIPT), *args], input=stdin, text=True, capture_output=True, env=self.env, timeout=5)

    def assert_no_send(self, result, success=True):
        self.assertEqual(result.returncode == 0, success, result.stderr)
        self.assertFalse(self.log.exists())

    def test_default_text_preview_without_credentials(self):
        r = self.run_tool('ORG_NOTIFY_TEST_WEBHOOK', 'A "quote"\nand a line')
        self.assert_no_send(r)
        self.assertEqual(json.loads(r.stdout)['text'], 'A "quote"\nand a line')

    def test_default_payload_preview_preserves_blocks(self):
        r = self.run_tool('ORG_NOTIFY_TEST_WEBHOOK', '--payload', str(self.payload))
        self.assert_no_send(r)
        self.assertEqual(json.loads(r.stdout), json.loads(self.payload.read_text()))

    def test_stdin_preview(self):
        r = self.run_tool('ORG_NOTIFY_TEST_WEBHOOK', stdin='From stdin')
        self.assert_no_send(r)
        self.assertEqual(json.loads(r.stdout)['text'], 'From stdin')

    def test_explicit_dry_run(self):
        self.assert_no_send(self.run_tool('ORG_NOTIFY_TEST_WEBHOOK', '--dry-run', 'Preview'))

    def test_execute_text_uses_exact_payload(self):
        self.env['ORG_NOTIFY_TEST_WEBHOOK'] = 'https://example.invalid/synthetic-webhook'
        r = self.run_tool('ORG_NOTIFY_TEST_WEBHOOK', 'Approved text', '--execute')
        self.assertEqual(r.returncode, 0, r.stderr)
        args = json.loads(self.log.read_text())
        self.assertEqual(args[args.index('--url') + 1], self.env['ORG_NOTIFY_TEST_WEBHOOK'])
        self.assertEqual(json.loads(args[args.index('--data-binary') + 1]), {'text': 'Approved text'})
        self.assertNotIn(self.env['ORG_NOTIFY_TEST_WEBHOOK'], r.stdout + r.stderr)

    def test_execute_payload_preserves_blocks(self):
        self.env['ORG_NOTIFY_TEST_WEBHOOK'] = 'https://example.invalid/synthetic-webhook'
        r = self.run_tool('ORG_NOTIFY_TEST_WEBHOOK', '--execute', '--payload', str(self.payload))
        self.assertEqual(r.returncode, 0, r.stderr)
        args = json.loads(self.log.read_text())
        self.assertEqual(json.loads(args[args.index('--data-binary') + 1]), json.loads(self.payload.read_text()))

    def test_execute_requires_webhook(self):
        self.assert_no_send(self.run_tool('ORG_NOTIFY_TEST_WEBHOOK', 'Text', '--execute'), False)

    def test_conflicting_flags_refuse_send(self):
        self.env['ORG_NOTIFY_TEST_WEBHOOK'] = 'https://example.invalid/synthetic-webhook'
        self.assert_no_send(self.run_tool('ORG_NOTIFY_TEST_WEBHOOK', 'Text', '--execute', '--dry-run'), False)

    def test_invalid_destination_name_refused(self):
        self.assert_no_send(self.run_tool('https://example.invalid', 'Text', '--execute'), False)

    def test_bad_payloads_refused(self):
        for value in ['not-json', '{}', '{"text":""}', '{"text":"one"}\n{"text":"two"}']:
            self.payload.write_text(value)
            self.assert_no_send(self.run_tool('ORG_NOTIFY_TEST_WEBHOOK', '--payload', str(self.payload), '--execute'), False)

    def test_message_and_payload_refused(self):
        self.assert_no_send(self.run_tool('ORG_NOTIFY_TEST_WEBHOOK', 'Text', '--payload', str(self.payload)), False)

    def test_missing_message_refused(self):
        self.assert_no_send(self.run_tool('ORG_NOTIFY_TEST_WEBHOOK'), False)

    def test_transport_error_not_reported_as_success(self):
        self.env.update(ORG_NOTIFY_TEST_WEBHOOK='https://example.invalid/synthetic-webhook', CURL_EXIT='22')
        r = self.run_tool('ORG_NOTIFY_TEST_WEBHOOK', 'Text', '--execute')
        self.assertEqual(r.returncode, 22)
        self.assertTrue(self.log.exists())
        self.assertNotIn('Posted Slack', r.stderr)

    def test_help_needs_no_credentials(self):
        self.assert_no_send(self.run_tool('--help'))


if __name__ == '__main__':
    unittest.main()
