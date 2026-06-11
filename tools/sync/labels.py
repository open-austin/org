#!/usr/bin/env python3
"""
Sync label taxonomy from open-austin/org to snapshot/labels.md
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Config
REPO = "open-austin/org"
OUT_DIR = Path("snapshot")
OUT_FILE = OUT_DIR / "labels.md"

def fetch_labels():
    """Fetch all labels from GitHub."""
    print(f"Fetching labels from {REPO}...", file=sys.stderr)
    result = subprocess.run(
        [
            "gh", "label", "list",
            "--repo", REPO,
            "--json", "name,description,color",
            "--limit", "500"
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)

def main():
    # Ensure output dir exists
    OUT_DIR.mkdir(exist_ok=True)

    # Fetch labels
    labels = fetch_labels()

    # Sort alphabetically
    labels.sort(key=lambda l: l["name"].lower())

    # Write output
    with OUT_FILE.open("w") as f:
        f.write(f"# Labels — {REPO}\n\n")
        f.write(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
        f.write(f"**Count:** {len(labels)} labels\n\n")
        f.write("---\n\n")

        for label in labels:
            color = label.get("color", "")
            desc = label.get("description", "")

            f.write(f"### `{label['name']}`\n\n")
            if color:
                f.write(f"**Color:** #{color}\n")
            if desc:
                f.write(f"**Description:** {desc}\n")
            f.write("\n---\n\n")

    print(f"✓ Labels synced to {OUT_FILE}", file=sys.stderr)

if __name__ == "__main__":
    main()
