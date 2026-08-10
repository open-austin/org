#!/usr/bin/env bash
# Wrapper for the Airtable read CLI. Loads AIRTABLE_TOKEN from the gitignored
# repo-root .env and runs airtable.py. Never echoes the token.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [ -f "$REPO_ROOT/.env" ]; then
  AIRTABLE_TOKEN="$(grep -E '^AIRTABLE_TOKEN=' "$REPO_ROOT/.env" | head -1 | cut -d= -f2- | tr -d '"'"'"'' )"
  export AIRTABLE_TOKEN
fi

exec python3 "$SCRIPT_DIR/airtable.py" "$@"
