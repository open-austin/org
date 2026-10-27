#!/usr/bin/env bash
set -euo pipefail

# Preview an Incoming Webhook payload; send only with explicit --execute.
# The first argument names an environment variable, never the secret URL.
usage() {
  printf '%s\n' \
    'Usage: tools/notify/post.sh WEBHOOK_ENV_VAR [message] [--execute | --dry-run]' \
    '       tools/notify/post.sh WEBHOOK_ENV_VAR --payload FILE [--execute | --dry-run]' \
    '       cat message.txt | tools/notify/post.sh WEBHOOK_ENV_VAR [--execute]' \
    'Preview is the default and needs no webhook. Review the destination and payload before executing.'
}
fail() { printf 'Error: %s\n' "$1" >&2; exit 1; }

case "${1:-}" in -h|--help) usage; exit 0 ;; '') usage >&2; exit 1 ;; esac
WEBHOOK_VAR="$1"; shift
[[ "$WEBHOOK_VAR" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || fail 'Expected a webhook environment variable name, not a URL.'
MESSAGE=''
PAYLOAD_FILE=''
HAS_MESSAGE=false
EXECUTE=false
EXPLICIT_DRY_RUN=false
while [ "$#" -gt 0 ]; do
  case "$1" in
    --execute) EXECUTE=true; shift ;;
    --dry-run) EXPLICIT_DRY_RUN=true; shift ;;
    --payload)
      [ "$#" -ge 2 ] && [ -n "$2" ] || fail '--payload requires a JSON file.'
      [ -z "$PAYLOAD_FILE" ] || fail 'Specify only one payload file.'
      PAYLOAD_FILE="$2"; shift 2 ;;
    --)
      shift
      [ "$#" -eq 1 ] && [ "$HAS_MESSAGE" = false ] || fail 'Provide one quoted message.'
      MESSAGE="$1"; HAS_MESSAGE=true; shift ;;
    --*) fail 'Unknown option; use -- before a message beginning with --.' ;;
    *)
      [ "$HAS_MESSAGE" = false ] || fail 'Provide one quoted message.'
      MESSAGE="$1"; HAS_MESSAGE=true; shift ;;
  esac
done
[ "$EXECUTE" = false ] || [ "$EXPLICIT_DRY_RUN" = false ] || fail 'Choose --execute or --dry-run, not both.'
if [ -n "$PAYLOAD_FILE" ]; then
  [ "$HAS_MESSAGE" = false ] || fail 'Choose a message or --payload, not both.'
  [ -f "$PAYLOAD_FILE" ] || fail 'Payload file not found.'
  jq -e -s 'length == 1 and (.[0] | type == "object" and (.text | type == "string" and length > 0))' "$PAYLOAD_FILE" >/dev/null || fail 'Expected one JSON object with nonempty text fallback.'
  PAYLOAD="$(cat "$PAYLOAD_FILE")"
else
  if [ "$HAS_MESSAGE" = false ]; then MESSAGE="$(cat)"; fi
  [ -n "$MESSAGE" ] || fail 'No message provided.'
  PAYLOAD="$(jq -n --arg text "$MESSAGE" '{text: $text}')"
fi

if [ "$EXECUTE" = false ]; then
  printf '%s\n' "$PAYLOAD"
  printf 'Dry run: no Slack message posted (%s). Add --execute only after approval.\n' "$WEBHOOK_VAR" >&2
  exit 0
fi

WEBHOOK_URL="${!WEBHOOK_VAR:-}"
[ -n "$WEBHOOK_URL" ] || fail "Environment variable '$WEBHOOK_VAR' is not set."
# Never retry a send automatically: a failed response can follow a delivered message.
curl --silent --show-error --fail --connect-timeout 10 --max-time 30 \
  --request POST --url "$WEBHOOK_URL" \
  --header 'Content-type: application/json' --data-binary "$PAYLOAD"
printf '\nPosted Slack payload (%s). If delivery is uncertain, inspect before retrying.\n' "$WEBHOOK_VAR" >&2
