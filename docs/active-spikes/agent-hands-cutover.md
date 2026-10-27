---
attention: live
---
# Agent Hands cutover
## Purpose and boundaries
Remove generic tooling that is fully covered by Agent Hands while keeping Open Austin's governance, meeting authorship, target selection, Airtable schema/data procedures and scheduled GitHub automation in this repository. This bounded work includes a privacy/security review of the outgoing Org history and selected changes, coherent commits and an explicitly authorized normal push. It does not authorize live organization writes, credential changes, history rewriting or changes to contributor-policy.md.

## Capability decisions
Agent Hands use-google-docs covers the local reader and unique-match replacement, including tab selection, embedded links, UTF-16 indices, preview/execute and revision guards. Retire the duplicate reader, OAuth module, wrapper and local implementation tests. README and the meeting skill retain Org's canonical-record and approval rules; credentials remain external and unchanged. The original eight behavior tests pass against both implementations; the replacement's independent offline guard/formatting suites also pass. These checks do not establish live account access.

Keep Airtable: no equivalent Agent Hands skill exists, and the schema and reconciliation rules are Org-specific. Keep the Slack Incoming Webhook/Block Kit helpers: Agent Hands sends as a user through its API and is not a transport/identity-equivalent replacement. The monthly role report posts directly in its workflow and does not call these helpers. The weekly-summary procedure remains retired, with its routing and rationale preserved.

## Safety and verification
The webhook helper previously sent by default despite the repository's dry-run-first rule. It now previews by default and requires explicit --execute. Offline tests exercise the transport boundary with a fake curl executable, including malformed/conflicting inputs and failed sends. No messages are posted during verification, and the scheduled workflow's implementation is unchanged.

Check current and outgoing Git content without reading ignored credentials or downloading private records. Report historical public references separately from new disclosures. Ignore private scratchpad work locally, verify the pinned workflow is publicly retrievable, and run a fresh recursive clone after publication. The reusable workflow branch and all unrelated repositories remain unchanged. Actual client discovery and authorized live Docs operations remain separate checks.

## Verified publication checkpoint
Implementation checkpoint `181d159` was normally pushed and anonymously cloned recursively on 2026-10-27. The clone retrieved workflow `4352866`, had clean parent/child trees, and passed the 14 offline webhook tests. GitHub reported no checks or Actions runs for that checkpoint. The bounded custom history/content scan found no known credential signatures or newly introduced flagged private references; no ignored credential contents or private service records were read. Client discovery and live Docs access remain untested and do not block this Git publication result.
