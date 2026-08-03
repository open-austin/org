---
name: process-weekly-meeting
description: "Reconcile an Open Austin weekly organizing meeting handoff with the canonical shared notes and current GitHub work. Use when checking the weekly notes for missed actions, updating action status or issue links, or proposing GitHub issue changes from the meeting."
---
# Process Weekly Meeting
## Scope
Use this skill only for Open Austin's recurring weekly organizing meeting. [General Organizing - meeting notes](https://docs.google.com/document/d/REDACTED-DOC-ID/edit) is the canonical meeting record. Preserve that document's existing per-meeting structure and local writing style; do not create parallel minutes or require anyone's private LifeOS system.

Other Open Austin meetings follow their normal meeting workflow, even when their notes also live in a shared Google Doc.

## What This Workflow Does
Use the chatbot's `Beat-by-beat notes` and `Light analysis` to audit the latest dated section of the shared Doc. The goal is to:

- catch concrete action items that the shared notes missed;
- correct action status when the available evidence is clear;
- connect actions to existing GitHub issues;
- propose updates to existing issues when the meeting materially changed the work; and
- propose new issues only for concrete org-visible work that has no current home.

Do not paste the chatbot handoff or a second summary into the shared Doc. Do not infer commitments, owners, or decisions merely to make the record look complete.

## Inputs
Gather:

- the meeting date;
- the chatbot-produced `Beat-by-beat notes` and `Light analysis`;
- the matching dated section of [General Organizing - meeting notes](https://docs.google.com/document/d/REDACTED-DOC-ID/edit); and
- current GitHub issue and project state from a fresh `tools/sync/run.sh` run.

Explicit corrections from an authorized participant outrank the chatbot handoff. Treat the handoff as compressed evidence, not as authoritative minutes.

## Workflow
1. Run `tools/sync/run.sh` to refresh GitHub state.
2. Read the meeting's current dated section in `General Organizing - meeting notes`, especially its existing action list.
3. Compare the shared section with the chatbot's beat-by-beat notes and analysis. Identify concrete actions, decisions, status changes, and dependencies that may have been missed or recorded incompletely.
4. Search current GitHub issues before proposing a new issue. For each credible action, classify it as `update existing`, `create candidate`, `already covered`, `completed`, or `not actionable`.
5. Apply the public/private filter. Keep private strategy, personal workload, sensitive context, and speculative judgments out of the shared Doc and GitHub.
6. Present an exact approval slate covering both shared-Doc and GitHub changes. Do not edit either system until the user approves each proposed change, unless the current request already contains exact approval for that change.
7. Re-fetch each approved target, run the narrow write tool in dry-run mode, and confirm the dry run still matches the approved text or issue change.
8. Execute only the approved changes. Re-read changed objects and refresh `snapshot/` afterward.

## Reconciliation Categories
- **Update existing:** an action or issue already owns the work and needs new context, a corrected status, or a cross-link.
- **Create candidate:** concrete org-visible work has no current GitHub home.
- **Already covered:** the shared notes and GitHub already represent the work accurately.
- **Completed:** evidence shows the work is finished; propose the smallest useful status update or issue closure.
- **Not actionable:** the material is discussion, aspiration, duplicate work, unclear ownership, or too uncertain to track.

The categories support review; they do not authorize writes or require every action to become an issue.

## Approval Slate
Separate proposed shared-Doc changes from proposed GitHub changes. For every write, show:

```text
ID: D1 or G1
Classification: Update existing | Create candidate | Completed
Target: Exact dated Doc section, existing issue number, or new open-austin/org issue
Current evidence: What the live Doc or GitHub currently says
Proposed exact change: Exact replacement text, issue title/body/labels/assignees, comment, link, or state change
Why: One sentence
Public or notification effect: Who can see it and whether anyone will be notified
```

List `Already covered` and `Not actionable` findings briefly after the actionable slate. Approval applies only to the exact displayed change. If live state has materially changed, stop and present a revised slate.

## Shared Google Doc Writes
Use `tools/google-docs/run.sh` for API reads and exact, uniquely matched replacements. `replace-once` is dry-run by default, re-fetches the live document, and uses its current revision ID. Add repeatable `--link "Visible text=https://…"` arguments when approved replacement text needs embedded links; each visible label must occur exactly once in the replacement.

Make only small in-place improvements such as adding a missing action, correcting an action's state, or linking an action to its GitHub issue. Preserve the surrounding dated section and its local format. Do not add a transcript link, chatbot analysis, or separate agent-written minutes.

If the needed insertion cannot be expressed safely with the current exact-replacement tool, stop and propose the smallest additional bounded tool operation rather than rewriting the whole meeting section.

## GitHub Writes
- Use `tools/issues/create.sh` for an approved new issue; it dry-runs by default.
- Inspect an existing issue immediately before proposing or executing an edit.
- Use the narrowest explicit `gh` command allowed by [../../AGENTS.md](../../AGENTS.md) for approved updates, comments, closures, or project-field changes.
- Interlink the shared action and issue when the link materially improves follow-through.
- Do not post a comment merely to repeat meeting prose. Comments notify people and should add operational value.

## Verification
Before reporting completion, confirm that:

- the shared section still follows its established format;
- no chatbot summary, analysis, or transcript link was inserted;
- every issue link points to the intended issue;
- every executed change matches its approved slate item; and
- `snapshot/` reflects final GitHub state.

Report unresolved ambiguity instead of filling it with assumptions.
