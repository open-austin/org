---
tags:
  - open-austin
  - spike
  - todo
---
# Weekly Meeting Processing To-Do
## Now
- [x] Settle the public/private boundary and canonical-record posture.
- [x] Draft `skills/process-weekly-meeting/SKILL.md` with the approved reconciliation taxonomy and exact approval slate.
- [x] Move guarded issue creation into `tools/issues/create.sh`.
- [x] Add dry-run-first Google Docs read and exact-match replacement tooling.
- [x] Document clone-local Google authentication in `.env.example` while allowing contributors to reuse existing local credential/token files by path.
- [x] Update repo authority docs and tool documentation.
- [x] Validate the skill shape manually and run local tooling tests. The bundled validator could not run because PyYAML is not installed; no dependency was installed as a side effect.
- [x] Simplify the skill around its actual input and output: audit chatbot beat-by-beat notes and analysis against the explicitly named shared Doc, reconcile missed actions with live GitHub, and present exact changes for approval without expecting or adding a transcript link.
- [x] Fix the wrapper's local-credential fallback so paths discovered after `.env` loading are exported to the Python tool.
- [x] Vendor the global `commit-work` seed into `skills/commit-work/` so the repo-local spike workflow has its required commit workflow after clone.

## Human QA
- [x] Complete the July 27 real-meeting test without creating parallel minutes. After Aslan corrected the first slate, the approved writes assigned Adam Corvus's completed audit to Communications through #483, linked Infrastructure work to #484/#506/#510/#511, recorded the separate Product CoP and Haley follow-ups accurately, and created #515 to coordinate all three September CoP presentations with Aslan, Bishop, and Beto.
- [x] Review one dry-run shared-Doc replacement against the canonical Doc. On 2026-07-29 the tool read the live Doc, selected tab `t.0`, required a unique exact match, and printed a no-write replacement plan.
- [x] Execute the first approved shared-Doc write: correct Vanessa's capitalization and add the already approved action to document her ambassador onboarding steps as they happen. The tool re-fetched the live revision, replaced exactly one match, and a follow-up read verified the final text.
- [x] Verify the final July 27 action block after the approved replacements and refresh the GitHub snapshot after creating [#515](https://github.com/open-austin/org/issues/515).

## Commit Boundary
- [ ] Commit the verified workflow, tools, and vendored skill in atomic explicit-path commits. The pre-commit audit found no credential material; `.env`, OAuth token/credential JSON, `snapshot/`, and Python bytecode are ignored.

## Done
