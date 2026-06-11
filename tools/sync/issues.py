#!/usr/bin/env python3
"""
Sync all open issues from open-austin/org to snapshot/issues/*.md
Each issue gets its own file with full comment thread.
snapshot/issues.md is an index grouped by team label.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Config
REPO = "open-austin/org"
OUT_DIR = Path("snapshot")
ISSUES_DIR = OUT_DIR / "issues"
INDEX_FILE = OUT_DIR / "issues.md"

# Team labels in priority order
TEAM_LABELS = [
    "finance",
    "fundraising",
    "communications",
    "engagement",
    "education",
    "infrastructure",
    "product team",
    "community",
    "board"
]

def fetch_issues():
    """Fetch all open issues from GitHub."""
    print(f"Fetching issues from {REPO}...", file=sys.stderr)
    result = subprocess.run(
        [
            "gh", "issue", "list",
            "--repo", REPO,
            "--state", "open",
            "--limit", "500",
            "--json", "number,title,assignees,labels,updatedAt,createdAt,body,author"
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)

def fetch_comments(issue_number):
    """Fetch all comments for an issue."""
    result = subprocess.run(
        [
            "gh", "api",
            f"/repos/{REPO}/issues/{issue_number}/comments",
            "--jq", "."
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)

def get_group_label(issue):
    """Get the first matching team label for an issue, or 'unlabeled'."""
    label_names = {label["name"] for label in issue["labels"]}
    for team_label in TEAM_LABELS:
        if team_label in label_names:
            return team_label
    return "unlabeled"

def days_stale(updated_at):
    """Calculate days since last update."""
    if not updated_at:
        return None
    updated = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    return (now - updated).days

def render_issue_file(issue, comments):
    """Render a full issue with comments to its own markdown file."""
    stale = days_stale(issue["updatedAt"])
    created = days_stale(issue["createdAt"])

    # Metadata
    lines = [
        f"# #{issue['number']} — {issue['title']}\n",
        f"**Status:** Open\n",
        f"**Created:** {created}d ago by @{issue['author']['login']}\n",
        f"**Updated:** {stale}d ago\n",
    ]

    # Assignees
    if issue["assignees"]:
        lines.append(f"**Assigned:** {', '.join('@' + a['login'] for a in issue['assignees'])}\n")

    # Labels
    if issue["labels"]:
        label_names = ", ".join(f"`{l['name']}`" for l in issue["labels"])
        lines.append(f"**Labels:** {label_names}\n")

    lines.append("\n---\n\n")

    # Body
    body = issue.get("body") or "(No description provided)"
    lines.append(f"## Description\n\n{body}\n\n")

    # Comments
    if comments:
        lines.append(f"---\n\n## Comments ({len(comments)})\n\n")
        for comment in comments:
            comment_date = datetime.fromisoformat(comment["created_at"].replace("Z", "+00:00"))
            formatted_date = comment_date.strftime("%Y-%m-%d %H:%M UTC")
            author = comment["user"]["login"]

            lines.append(f"### @{author} — {formatted_date}\n\n")
            lines.append(f"{comment['body']}\n\n")
            lines.append("---\n\n")

    return "".join(lines)

def render_index_entry(issue):
    """Render a single line for the index file."""
    stale = days_stale(issue["updatedAt"])

    # Assignees
    if issue["assignees"]:
        assignee_text = f" | **Assigned:** {', '.join(a['login'] for a in issue['assignees'])}"
    else:
        assignee_text = ""

    # Preview (first 100 chars of body)
    body = (issue.get("body") or "").replace("\n", " ").strip()
    if len(body) > 100:
        body = body[:100] + "..."

    link = f"issues/{issue['number']}.md"

    return f"### [#{issue['number']} {issue['title']}]({link})\n\n**Updated:** {stale}d ago{assignee_text}\n\n{body}\n\n---\n\n"

def main():
    # Ensure output dirs exist
    OUT_DIR.mkdir(exist_ok=True)
    ISSUES_DIR.mkdir(exist_ok=True)

    # Fetch issues
    issues = fetch_issues()

    print(f"Fetching comments for {len(issues)} issues...", file=sys.stderr)

    # Group by label for index
    groups = {}
    for issue in issues:
        group = get_group_label(issue)
        groups.setdefault(group, []).append(issue)

        # Fetch comments and write individual issue file
        print(f"  #{issue['number']}...", file=sys.stderr)
        comments = fetch_comments(issue['number'])

        issue_file = ISSUES_DIR / f"{issue['number']}.md"
        with issue_file.open("w") as f:
            f.write(render_issue_file(issue, comments))

    # Write index file
    with INDEX_FILE.open("w") as f:
        f.write(f"# Open Issues — {REPO}\n\n")
        f.write(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
        f.write(f"**Count:** {len(issues)} open issues\n\n")
        f.write("This index groups issues by team label. Click through to see full issue with comments.\n\n")
        f.write("---\n\n")

        # Render each group
        for label in TEAM_LABELS + ["unlabeled"]:
            if label not in groups:
                continue

            f.write(f"## {label.upper()}\n\n")
            for issue in groups[label]:
                f.write(render_index_entry(issue))

    print(f"✓ {len(issues)} issues synced to {ISSUES_DIR}/", file=sys.stderr)
    print(f"✓ Index written to {INDEX_FILE}", file=sys.stderr)

if __name__ == "__main__":
    main()
