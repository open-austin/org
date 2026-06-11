#!/usr/bin/env bash
set -euo pipefail

# Run all sync tools to regenerate snapshot/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Syncing Open Austin org state to snapshot/" >&2
echo >&2

python3 "$SCRIPT_DIR/issues.py"
python3 "$SCRIPT_DIR/labels.py"
python3 "$SCRIPT_DIR/boards.py"

echo >&2
echo "==> Sync complete" >&2
echo "    snapshot/issues.md" >&2
echo "    snapshot/labels.md" >&2
echo "    snapshot/board-org-kanban.md" >&2
echo "    snapshot/board-open-roles.md" >&2
