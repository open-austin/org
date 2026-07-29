#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
if [[ -f "$ROOT/.env" ]]; then
    set -a
    # shellcheck disable=SC1091
    source "$ROOT/.env"
    set +a
fi

repo="${GITHUB_REPO:-${GITHUB_ORG:-open-austin}/org}"
title=""
body=""
body_file=""
execute=0
sync_after=1
assign_me=0
labels=()
assignees=()

fail() {
    printf 'ERROR: %s\n' "$*" >&2
    exit 1
}

usage() {
    cat <<'EOF'
Usage: tools/issues/create.sh --title TITLE [options]

Options:
  --body TEXT
  --body-file FILE
  --label LABEL             Repeatable
  --assignee LOGIN          Repeatable
  --assign-me
  --repo OWNER/REPO
  --execute                 Create the approved issue
  --dry-run                 Print the plan only (default)
  --no-sync                 Skip tools/sync/run.sh after creation
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --title) [[ $# -ge 2 ]] || fail "--title requires TEXT"; title="$2"; shift 2 ;;
        --body) [[ $# -ge 2 ]] || fail "--body requires TEXT"; body="$2"; shift 2 ;;
        --body-file) [[ $# -ge 2 ]] || fail "--body-file requires FILE"; body_file="$2"; shift 2 ;;
        --label) [[ $# -ge 2 ]] || fail "--label requires LABEL"; labels+=("$2"); shift 2 ;;
        --assignee|--assign) [[ $# -ge 2 ]] || fail "$1 requires LOGIN"; assignees+=("$2"); shift 2 ;;
        --assign-me) assign_me=1; shift ;;
        --repo) [[ $# -ge 2 ]] || fail "--repo requires OWNER/REPO"; repo="$2"; shift 2 ;;
        --execute) execute=1; shift ;;
        --dry-run) execute=0; shift ;;
        --no-sync) sync_after=0; shift ;;
        -h|--help) usage; exit 0 ;;
        *) fail "Unknown option: $1" ;;
    esac
done

[[ -n "$title" ]] || fail "--title is required"
[[ -z "$body_file" || -z "$body" ]] || fail "Use either --body or --body-file, not both"
[[ -z "$body_file" || -f "$body_file" ]] || fail "Body file does not exist: $body_file"

if [[ $assign_me -eq 1 ]]; then
    if [[ $execute -eq 1 ]]; then
        command -v gh >/dev/null || fail "gh is required"
        assignees+=("$(gh api user --jq .login)")
    else
        assignees+=("@me")
    fi
fi

printf 'GitHub issue create plan:\n'
printf 'Repo: %s\n' "$repo"
printf 'Title: %s\n' "$title"
if [[ -n "$body_file" ]]; then
    printf 'Body file: %s\n' "$body_file"
    printf '%s\n' '--- body preview ---'
    sed -n '1,240p' "$body_file"
    printf '%s\n' '--- end body preview ---'
elif [[ -n "$body" ]]; then
    printf 'Body:\n%s\n' "$body"
else
    printf 'Body: <empty>\n'
fi
if [[ ${#labels[@]} -gt 0 ]]; then printf 'Labels: %s\n' "${labels[*]}"; else printf 'Labels: <none>\n'; fi
if [[ ${#assignees[@]} -gt 0 ]]; then printf 'Assignees: %s\n' "${assignees[*]}"; else printf 'Assignees: <none>\n'; fi

if [[ $execute -ne 1 ]]; then
    printf 'DRY RUN: no GitHub issue was created. Re-run with --execute after approval.\n'
    exit 0
fi

command -v gh >/dev/null || fail "gh is required"
gh repo view "$repo" --json nameWithOwner --jq .nameWithOwner >/dev/null

cmd=(gh issue create --repo "$repo" --title "$title")
if [[ -n "$body_file" ]]; then cmd+=(--body-file "$body_file"); else cmd+=(--body "$body"); fi
for label in "${labels[@]}"; do cmd+=(--label "$label"); done
for assignee in "${assignees[@]}"; do cmd+=(--assignee "$assignee"); done

created_url="$("${cmd[@]}")"
printf 'Created issue: %s\n' "$created_url"

if [[ $sync_after -eq 1 ]]; then
    "$ROOT/tools/sync/run.sh"
fi
