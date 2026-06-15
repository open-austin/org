#!/usr/bin/env bash
set -euo pipefail

# Post a message to a Slack channel via Incoming Webhook.
# Usage:
#   tools/notify/post.sh <webhook_env_var> <message>
#   cat message.txt | tools/notify/post.sh <webhook_env_var>
#   tools/notify/post.sh <webhook_env_var> --payload payload.json
#   tools/notify/post.sh <webhook_env_var> --payload payload.json --dry-run
#
# Example:
#   tools/notify/post.sh SLACK_WEBHOOK_ENGAGEMENT "Weekly summary text here"
#   echo "Hello" | tools/notify/post.sh SLACK_WEBHOOK_ENGAGEMENT
#   tools/notify/post.sh SLACK_WEBHOOK_ORG --payload snapshot/weekly-summary.blocks.json
#
# The webhook URL is read from the environment variable name you pass.
# Load your .env first: source .env

WEBHOOK_VAR="${1:-}"
MESSAGE="${2:-}"
PAYLOAD_FILE=""
DRY_RUN=false

if [ -z "$WEBHOOK_VAR" ]; then
  echo "Usage: tools/notify/post.sh <WEBHOOK_ENV_VAR> [message]" >&2
  echo "       tools/notify/post.sh <WEBHOOK_ENV_VAR> --payload <payload.json>" >&2
  echo "       Add --dry-run to print the payload without posting." >&2
  echo "  Or pipe message via stdin." >&2
  exit 1
fi

if [ "$MESSAGE" = "--dry-run" ]; then
  DRY_RUN=true
  MESSAGE="${3:-}"
fi

if [ "$MESSAGE" = "--payload" ]; then
  PAYLOAD_FILE="${3:-}"
  if [ -z "$PAYLOAD_FILE" ]; then
    echo "Error: --payload requires a JSON payload file." >&2
    exit 1
  fi
  if [ ! -f "$PAYLOAD_FILE" ]; then
    echo "Error: payload file not found: $PAYLOAD_FILE" >&2
    exit 1
  fi
  if [ "${4:-}" = "--dry-run" ]; then
    DRY_RUN=true
  fi
fi

if [ -n "$PAYLOAD_FILE" ]; then
  jq -e 'type == "object" and (.text | type == "string")' "$PAYLOAD_FILE" >/dev/null

  if [ "$DRY_RUN" = true ]; then
    cat "$PAYLOAD_FILE"
    echo "✓ Dry run: Slack payload rendered but not posted ($WEBHOOK_VAR)" >&2
    exit 0
  fi

  # Resolve the webhook URL from the env var name
  WEBHOOK_URL="${!WEBHOOK_VAR:-}"
  if [ -z "$WEBHOOK_URL" ]; then
    echo "Error: environment variable '$WEBHOOK_VAR' is not set." >&2
    echo "Did you source your .env file?" >&2
    exit 1
  fi

  curl -s -X POST "$WEBHOOK_URL" \
    -H 'Content-type: application/json' \
    --data-binary "@$PAYLOAD_FILE" \
    --fail

  echo "" >&2
  echo "✓ Posted Slack payload ($WEBHOOK_VAR)" >&2
  exit 0
fi

# Read message from arg or stdin
if [ -z "$MESSAGE" ]; then
  MESSAGE=$(cat)
fi

if [ -z "$MESSAGE" ]; then
  echo "Error: no message provided." >&2
  exit 1
fi

# Escape for JSON
ESCAPED=$(echo "$MESSAGE" | jq -Rs .)
PAYLOAD="{\"text\": $ESCAPED}"

if [ "$DRY_RUN" = true ]; then
  echo "$PAYLOAD" | jq .
  echo "✓ Dry run: Slack text payload rendered but not posted ($WEBHOOK_VAR)" >&2
  exit 0
fi

# Resolve the webhook URL from the env var name
WEBHOOK_URL="${!WEBHOOK_VAR:-}"
if [ -z "$WEBHOOK_URL" ]; then
  echo "Error: environment variable '$WEBHOOK_VAR' is not set." >&2
  echo "Did you source your .env file?" >&2
  exit 1
fi

curl -s -X POST "$WEBHOOK_URL" \
  -H 'Content-type: application/json' \
  --data "$PAYLOAD" \
  --fail

echo "" >&2
echo "✓ Posted to Slack ($WEBHOOK_VAR)" >&2
