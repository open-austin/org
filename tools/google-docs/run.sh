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

# Optional convenience: point OA_LOCAL_SECRETS_DIR (in your gitignored .env) at a
# local directory holding google-credentials.json / google-open-austin-token.json,
# and the wrapper will pick them up without setting the explicit paths below.
local_secrets_dir="${OA_LOCAL_SECRETS_DIR:-}"
if [[ -n "$local_secrets_dir" ]]; then
    if [[ -z "${GOOGLE_CLIENT_CREDENTIALS_PATH:-}" && -f "$local_secrets_dir/google-credentials.json" ]]; then
        GOOGLE_CLIENT_CREDENTIALS_PATH="$local_secrets_dir/google-credentials.json"
    fi
    if [[ -z "${GOOGLE_TOKEN_PATH:-}" && -f "$local_secrets_dir/google-open-austin-token.json" ]]; then
        GOOGLE_TOKEN_PATH="$local_secrets_dir/google-open-austin-token.json"
    fi
fi

: "${GOOGLE_CLIENT_CREDENTIALS_PATH:?Set GOOGLE_CLIENT_CREDENTIALS_PATH in .env or the environment}"
: "${GOOGLE_TOKEN_PATH:?Set GOOGLE_TOKEN_PATH in .env or the environment}"
export GOOGLE_CLIENT_CREDENTIALS_PATH GOOGLE_TOKEN_PATH

if [[ "${1:-}" == "auth" ]]; then
    shift
    exec python3 "$SCRIPT_DIR/google_oauth.py" "$GOOGLE_CLIENT_CREDENTIALS_PATH" "$GOOGLE_TOKEN_PATH" "$@"
fi

exec python3 "$SCRIPT_DIR/docs.py" "$@"
