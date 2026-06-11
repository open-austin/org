#!/usr/bin/env bash
set -euo pipefail

# Post a message to a Slack channel via Incoming Webhook.
# Usage:
#   tools/notify/post.sh <webhook_env_var> <message>
#   cat message.txt | tools/notify/post.sh <webhook_env_var>
#
# Example:
#   tools/notify/post.sh SLACK_WEBHOOK_ENGAGEMENT "Weekly summary text here"
#   echo "Hello" | tools/notify/post.sh SLACK_WEBHOOK_ENGAGEMENT
#
# The webhook URL is read from the environment variable name you pass.
# Load your .env first: source .env

WEBHOOK_VAR="${1:-}"
MESSAGE="${2:-}"

if [ -z "$WEBHOOK_VAR" ]; then
  echo "Usage: tools/notify/post.sh <WEBHOOK_ENV_VAR> [message]" >&2
  echo "  Or pipe message via stdin." >&2
  exit 1
fi

# Resolve the webhook URL from the env var name
WEBHOOK_URL="${!WEBHOOK_VAR:-}"
if [ -z "$WEBHOOK_URL" ]; then
  echo "Error: environment variable '$WEBHOOK_VAR' is not set." >&2
  echo "Did you source your .env file?" >&2
  exit 1
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

curl -s -X POST "$WEBHOOK_URL" \
  -H 'Content-type: application/json' \
  --data "{\"text\": $ESCAPED}" \
  --fail

echo "" >&2
echo "✓ Posted to Slack ($WEBHOOK_VAR)" >&2
