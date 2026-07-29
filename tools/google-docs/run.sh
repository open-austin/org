#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    exec python3 "$SCRIPT_DIR/docs.py" --help
fi

if [[ -f "$ROOT/.env" ]]; then
    set -a
    # shellcheck disable=SC1091
    source "$ROOT/.env"
    set +a
fi

lifeos_secrets_dir="${LIFEOS_TOOLS_SECRETS_DIR:-$HOME/configs/lifeos-tools/secrets}"
if [[ -z "${GOOGLE_CLIENT_CREDENTIALS_PATH:-}" && -f "$lifeos_secrets_dir/google-credentials.json" ]]; then
    GOOGLE_CLIENT_CREDENTIALS_PATH="$lifeos_secrets_dir/google-credentials.json"
fi
if [[ -z "${GOOGLE_TOKEN_PATH:-}" && -f "$lifeos_secrets_dir/google-open-austin-token.json" ]]; then
    GOOGLE_TOKEN_PATH="$lifeos_secrets_dir/google-open-austin-token.json"
fi

: "${GOOGLE_CLIENT_CREDENTIALS_PATH:?Set GOOGLE_CLIENT_CREDENTIALS_PATH in .env or the environment}"
: "${GOOGLE_TOKEN_PATH:?Set GOOGLE_TOKEN_PATH in .env or the environment}"
export GOOGLE_CLIENT_CREDENTIALS_PATH GOOGLE_TOKEN_PATH

if [[ "${1:-}" == "auth" ]]; then
    shift
    exec python3 "$SCRIPT_DIR/google_oauth.py" "$GOOGLE_CLIENT_CREDENTIALS_PATH" "$GOOGLE_TOKEN_PATH" "$@"
fi

exec python3 "$SCRIPT_DIR/docs.py" "$@"
