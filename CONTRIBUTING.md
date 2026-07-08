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
# 1. Clone the repo
git clone https://github.com/open-austin/org.git
cd org

# 2. Copy and fill in your environment
cp .env.example .env
# Edit .env and set GH_TOKEN to your PAT

# 3. Authenticate the gh CLI
export GH_TOKEN=$(grep GH_TOKEN .env | cut -d= -f2)
gh auth status   # should show open-austin org access
```

## How Work Is Organized
This repo uses a spike-based workflow. See [`skills/run-project-spike/SKILL.md`](skills/run-project-spike/SKILL.md) for the full process.

- **`TODO.md`** — active work and backlog
- **`docs/`** — decision records, active spikes (`docs/active-spikes/`), scratch, archive
- **`skills/`** — repo-local agent workflows (spike process, misc triage, weekly org summary)
- **`tools/`** — CLI and MCP tooling (to be created)
- **`AGENTS.md`** — rules for AI agents working in this repo

## Opening Issues and PRs
- Open an issue before starting significant work so others know what's in flight.
- Keep PRs focused. One spike or feature per PR.
- Reference the relevant spike doc or decision record in your PR description if applicable.
- Do not commit `.env` or any file containing real credentials. See `.env.example` for what's needed.

## Write Safety
This tooling touches shared org state. Before contributing write tools or running write commands:

- Read the write-safety rules in `AGENTS.md`.
- All write tools must support `--dry-run`.
- No bulk operations without a reviewed change plan.
- When in doubt, open an issue or ask in `#oa-admin` on Slack before running anything that touches real issues, comments, or board state.
