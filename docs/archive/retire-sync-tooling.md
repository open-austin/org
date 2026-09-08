# Retire The Sync Tooling
## Why
`tools/sync/` pulls issues, labels, and board state into gitignored `snapshot/` markdown. It was built to feed one person's private knowledge vault, and in practice it has had exactly one user. Nobody else has adopted it, and it only makes sense to someone running a comparable personal system.

Keeping it here costs the maintainer dual maintenance and — the sharper cost — it fragments the workflow. Processing an Open Austin weekly meeting currently means running part of a private skill, then switching repos for a second pass with a skill that lives here. That is not a workflow anyone was going to adopt, and it exists only because the tooling was split across two homes.

The generic replacement lives in the maintainer's private tooling and talks to the GitHub API directly, so it needs nothing from this repo.

## What Changes
- `tools/sync/` is removed.
- `skills/weekly-org-summary/SKILL.md` is rewritten to describe the **process** rather than invoke removed tools. The routing table, review discipline, Slack formatting rules, and archive step all stay — that is the part with real org value, and it is more useful to a non-CLI contributor as prose than it ever was as a script wrapper.
- `README.md` and `AGENTS.md` drop their sync references.

## What Explicitly Stays
Investigated and confirmed still load-bearing:

- **`tools/notify/`** — Slack posting and Block Kit rendering. Generic, works from any input file, unrelated to sync.
- **`tools/issues/create.sh`** — issue creation. Nothing to do with sync.
- **`tools/google-docs/`** — bounded shared-Doc reads and replacements.
- **`tools/airtable/`** — separate active spike.
- **The thirteen GitHub Actions workflows** in `.github/workflows/`. These are the org's real shared automation: board routing, issue/board status sync, scheduled archiving, role pipeline reporting, stale-role warnings. They run for everyone without anyone touching a CLI, they do not use `tools/sync/`, and removing sync does not touch them.
- **The GitHub PAT setup in `CONTRIBUTING.md`.** Originally slated for removal on the assumption it existed for the sync tooling. It does not — `tools/issues/create.sh` and `tools/airtable/` both need `gh` auth, and so does anyone running `gh` by hand.
- **The Write Safety section of `CONTRIBUTING.md`.** Same correction. It governs `tools/issues/create.sh` and `tools/google-docs/`, which are the repo's actual write paths. `tools/sync/` was read-only and was never what those rules were protecting against.

## Non-Goals
- Not removing anything a contributor could use.
- Not changing board automation.
- Not leaving the weekly summary undocumented. The knowledge stays; only the scripts leave.

## The Snapshot Contract Changes
`snapshot/` stays gitignored and stays the working directory for weekly-summary drafts, since `tools/notify/` reads from it. What changes is that nothing in this repo regenerates it from GitHub any more. A contributor picking this up has two options: read the live board and issues in the GitHub UI, or write their own sync. That gap is deliberate and is named in the skill.
