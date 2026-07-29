#!/usr/bin/env python3
"""Small OAuth helper for the Open Austin Google Docs tools."""

import base64
import hashlib
import http.server
import json
import os
import secrets
import socket
import sys
import time
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime, timedelta, timezone


def load_credentials(path):
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if "installed" in data:
        data = data["installed"]
    elif "web" in data:
        data = data["web"]
    for key in ("client_id", "auth_uri", "token_uri"):
        if not data.get(key):
            raise ValueError(f"Missing {key} in Google credentials")
    return data


def load_token(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_token(path, token):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    temporary = f"{path}.tmp"
    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump(token, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(temporary, path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def utc_now():
    return datetime.now(timezone.utc)


def iso_at(seconds):
    return (utc_now() + timedelta(seconds=int(seconds))).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_expired(token):
    expires_at = token.get("expires_at")
    if not expires_at:
        return True
    try:
        expires = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
    except ValueError:
        return True
    return expires <= utc_now() + timedelta(minutes=5)


def post_form(url, fields):
    body = urllib.parse.urlencode(fields).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def client_fields(credentials):
    fields = {"client_id": credentials["client_id"]}
    if credentials.get("client_secret"):
        fields["client_secret"] = credentials["client_secret"]
    return fields


def refresh(credentials_path, token_path):
    credentials = load_credentials(credentials_path)
    token = load_token(token_path)
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise ValueError("No refresh_token found. Run tools/google-docs/run.sh auth first.")
    fields = client_fields(credentials)
    fields.update({"refresh_token": refresh_token, "grant_type": "refresh_token"})
    updated = post_form(credentials["token_uri"], fields)
    token.update(updated)
    token["refresh_token"] = refresh_token
    if "expires_in" in updated:
        token["expires_at"] = iso_at(updated["expires_in"])
    token["refreshed_at"] = utc_now().replace(microsecond=0).isoformat().replace("+00:00", "Z")
    write_token(token_path, token)
    return token


def get_access_token(credentials_path, token_path):
    token = load_token(token_path)
    if not token.get("access_token") or is_expired(token):
        token = refresh(credentials_path, token_path)
    return token["access_token"]


def find_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


class OAuthHandler(http.server.BaseHTTPRequestHandler):
    server_version = "OpenAustinGoogleOAuth/1.0"

    def log_message(self, fmt, *args):
        return

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        self.server.oauth_result = {
            "code": params.get("code", [""])[0],
            "state": params.get("state", [""])[0],
            "error": params.get("error", [""])[0],
        }
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Open Austin Google auth complete</h1><p>You can close this tab.</p></body></html>")


def authorize(credentials_path, token_path, scopes, no_browser=False):
    credentials = load_credentials(credentials_path)
    port = find_free_port()
    redirect_uri = f"http://127.0.0.1:{port}/"
    state = secrets.token_urlsafe(24)
    verifier = secrets.token_urlsafe(64)
    params = {
        "client_id": credentials["client_id"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "true",
        "state": state,
        "code_challenge": code_challenge(verifier),
        "code_challenge_method": "S256",
    }
    auth_url = f"{credentials['auth_uri']}?{urllib.parse.urlencode(params)}"
    server = http.server.HTTPServer(("127.0.0.1", port), OAuthHandler)
    server.timeout = 300
    server.oauth_result = None
    print("Opening Google authorization URL...", flush=True)
    if no_browser or not webbrowser.open(auth_url):
        print(auth_url, flush=True)
    deadline = time.time() + 300
    while time.time() < deadline and not server.oauth_result:
        server.handle_request()
    server.server_close()
    result = server.oauth_result
    if not result:
        raise TimeoutError("Timed out waiting for Google OAuth redirect")
    if result.get("error"):
        raise RuntimeError(f"Google OAuth returned error: {result['error']}")
    if result.get("state") != state:
        raise RuntimeError("OAuth state did not match")
    if not result.get("code"):
        raise RuntimeError("OAuth redirect did not include an authorization code")
    fields = client_fields(credentials)
    fields.update({"code": result["code"], "code_verifier": verifier, "grant_type": "authorization_code", "redirect_uri": redirect_uri})
    token = post_form(credentials["token_uri"], fields)
    existing = load_token(token_path)
    if "refresh_token" not in token and existing.get("refresh_token"):
        token["refresh_token"] = existing["refresh_token"]
    if "expires_in" in token:
        token["expires_at"] = iso_at(token["expires_in"])
    token["obtained_at"] = utc_now().replace(microsecond=0).isoformat().replace("+00:00", "Z")
    token["requested_scopes"] = scopes
    write_token(token_path, token)
    print(f"Wrote Google token: {token_path}")


def main(argv):
    if len(argv) < 3:
        print("Usage: google_oauth.py CREDENTIALS TOKEN [--no-browser]", file=sys.stderr)
        return 1
    unknown = [argument for argument in argv[3:] if argument != "--no-browser"]
    if unknown:
        print(f"Unknown option: {unknown[0]}", file=sys.stderr)
        return 1
    try:
        authorize(argv[1], argv[2], ["https://www.googleapis.com/auth/documents"], no_browser="--no-browser" in argv[3:])
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
