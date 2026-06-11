#!/usr/bin/env python3
"""
Sync Projects v2 board state from open-austin/org to snapshot/board-*.md
Currently syncs: Org Kanban, Open Roles
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Config
ORG = "open-austin"
OUT_DIR = Path("snapshot")

# Project numbers to sync
PROJECTS = {
    9: "org-kanban",     # Org Kanban
    6: "open-roles"      # Open Roles
}

def fetch_project_items(project_number):
    """Fetch all items from a project board using gh CLI."""
    print(f"Fetching project #{project_number} items...", file=sys.stderr)
    result = subprocess.run(
        [
            "gh", "project", "item-list", str(project_number),
            "--owner", ORG,
            "--format", "json",
            "--limit", "500"
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)

def days_stale(updated_at):
    """Calculate days since last update."""
    if not updated_at:
        return None
    # Handle various date formats
    for fmt in ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]:
        try:
            updated = datetime.strptime(updated_at, fmt).replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            return (now - updated).days
        except ValueError:
            continue
    return None

def render_board(project_number, slug):
    """Render a single board to markdown."""
    items = fetch_project_items(project_number)

    # Group by status
    groups = {}
    for item in items.get("items", []):
        status = item.get("status", "No Status")
        groups.setdefault(status, []).append(item)

    # Write output
    out_file = OUT_DIR / f"board-{slug}.md"
    with out_file.open("w") as f:
        f.write(f"# Project #{project_number} — {slug.replace('-', ' ').title()}\n\n")
        f.write(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
        f.write(f"**Total items:** {len(items.get('items', []))}\n\n")
        f.write("---\n\n")

        for status in sorted(groups.keys()):
            f.write(f"## {status}\n\n")
            f.write(f"**Count:** {len(groups[status])}\n\n")

            for item in groups[status]:
                # Extract title and type
                title = item.get("title", "(No title)")
                content_type = item.get("type", "unknown")

                # Assignees
                assignees = item.get("assignees", [])
                if assignees:
                    assignee_text = f" | **Assigned:** {', '.join(assignees)}"
                else:
                    assignee_text = ""

                # Updated date
                updated = item.get("updatedAt")
                stale = days_stale(updated)
                if stale is not None:
                    stale_text = f" | **Updated:** {stale}d ago"
                else:
                    stale_text = ""

                # Labels
                labels = item.get("labels", [])
                if labels:
                    label_text = f" | **Labels:** {', '.join(labels)}"
                else:
                    label_text = ""

                f.write(f"### {title}\n\n")
                f.write(f"**Type:** {content_type}{assignee_text}{stale_text}{label_text}\n\n")
                f.write("---\n\n")

    print(f"✓ Project #{project_number} synced to {out_file}", file=sys.stderr)

def main():
    # Ensure output dir exists
    OUT_DIR.mkdir(exist_ok=True)

    # Sync each project
    for project_number, slug in PROJECTS.items():
        render_board(project_number, slug)

if __name__ == "__main__":
    main()
