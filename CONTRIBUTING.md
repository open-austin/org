# Contributing to Open Austin Org Tooling
This doc covers the practical mechanics of contributing to this repo. For Open Austin's policies on licensing, attribution, and open-source requirements, see [`contributor-policy.md`](contributor-policy.md).

## What This Repo Is
This repo contains operational tooling and documentation for managing the Open Austin GitHub org — issue triage, project board automation, backlog snapshots, and agent-facing CLI/MCP tools.

## Getting Started
### Prerequisites
- [GitHub CLI (`gh`)](https://cli.github.com/) — `brew install gh`
- A GitHub PAT with `repo` and `project` scopes, authorized for the `open-austin` org
- If the org enforces SAML SSO: authorize your token at GitHub → Settings → Tokens → Configure SSO

### Setup
```sh
git clone --recurse-submodules https://github.com/open-austin/org.git
cd org
# For an existing checkout:
git submodule update --init --recursive

# Use your existing gh login, or authenticate your own account if needed.
gh auth status
# gh auth login
```

Copy `.env.example` to an ignored `.env` only if one does not already exist. Keep real tokens and target IDs private. `gh` can use its existing credential store or an explicitly exported `GH_TOKEN`; neither cloning nor this setup requires replacing credentials. Org access and any SSO authorization must be verified for the actual operation. For Google Docs, follow [Shared Google Docs](README.md#shared-google-docs) to use Agent Hands with an existing account alias. No service authorization or shared-state write follows from installing the tooling.

## How Work Is Organized
This repo uses a spike-based workflow. See [`project-workflows/run-project-spike/SKILL.md`](project-workflows/run-project-spike/SKILL.md) for the full process.

- **`TODO.md`** — active work and backlog
- **`docs/`** — policies, active spikes (`docs/active-spikes/`), scratch, archive
- **`project-workflows/`** — pinned reusable workflow skills
- **`skills/`** — organization-specific procedures, with retired procedures clearly marked
- **`tools/`** — retained Airtable operations and Slack webhook/Block Kit helpers; generic Docs tooling lives in Agent Hands
- **`AGENTS.md`** — rules for AI agents working in this repo

## Opening Issues and PRs
- Open an issue before starting significant work so others know what's in flight.
- Keep PRs focused. One spike or feature per PR.
- Reference the relevant spike doc or policy in your PR description if applicable.
- Do not commit `.env` or any file containing real credentials. See `.env.example` for what's needed.

## Write Safety
This tooling touches shared org state. Before contributing write tools or running write commands:

- Read the write-safety rules in `AGENTS.md`.
- All write tools must support `--dry-run`.
- No bulk operations without a reviewed change plan.
- When in doubt, open an issue or ask in `#oa-admin` on Slack before running anything that touches real issues, comments, or board state.
