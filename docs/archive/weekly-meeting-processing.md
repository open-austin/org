---
tags:
  - open-austin
  - spike
  - meetings
  - google-docs
  - github
---
# Spike: Weekly Meeting Processing
## Status
- Active as of 2026-07-29.

## Purpose
Create a reusable Open Austin workflow for reconciling the weekly organizing meeting with the shared recurring Google Doc and GitHub, usable by any contributor from a clone of this repo.

## Boundary
The canonical shared Doc is [General Organizing - meeting notes](https://docs.google.com/document/d/REDACTED-DOC-ID/edit), a human-authored recurring record. The public workflow receives chatbot-produced beat-by-beat notes and analysis, not the transcript. That handoff can reveal missing actions, stale states, or absent issue links, but it is not a second set of minutes to paste into the document.

The public workflow owns:

- preserving the established per-meeting structure and local style in `General Organizing - meeting notes`;
- reconciling meeting actions against fresh GitHub state;
- interlinking the shared record and existing issues when useful;
- drafting bounded shared-Doc corrections or issue links;
- producing an exact approval slate;
- applying approved Google Docs and GitHub writes through dry-run-first public tooling.

The workflow does not own private personal-tooling context integration, private Trello work, or a redundant local meeting note.

## Tool Ownership
The org repo owns the reusable Open Austin write mechanics. GitHub issue creation lives here, in `tools/issues/create.sh`, as the primary implementation of public issue writes.

Google Docs writes also belong here because they modify a shared Open Austin artifact. Authentication remains local and uncommitted. The public repo documents the required environment variables and provides its own OAuth path for other contributors; the wrapper can reuse existing local credential and Open Austin token files (via `OA_LOCAL_SECRETS_DIR`) when present, instead of copying secrets.

## Google Docs Safety Model
The first write surface is intentionally narrow: read a document and replace one exact, uniquely occurring text span. The tool is dry-run by default, re-fetches the live document before execution, uses `requiredRevisionId`, and refuses ambiguous matches. This supports small action corrections and issue cross-links without authorizing broad note regeneration.

## Open Questions
- Which Google account should be treated as the normal Open Austin editing identity for each contributor?
- `General Organizing - meeting notes` currently uses tab `t.0`; the July 27 test targeted that tab explicitly. Keep the tab ID configurable because the shared document may evolve.
- After one real meeting test, is exact-match replacement sufficient, or is a second bounded insertion primitive justified?
- Should issue update/comment helpers be added after real use, or does reviewed direct `gh` remain clearer?
