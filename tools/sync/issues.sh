#!/usr/bin/env bash
set -euo pipefail

# Sync all open issues from open-austin/org to snapshot/issues.md
# Grouped by team label, sorted by staleness

REPO="open-austin/org"
OUT_DIR="snapshot"
OUT_FILE="$OUT_DIR/issues.md"

# Ensure output dir exists
mkdir -p "$OUT_DIR"

# Fetch all open issues as JSON
echo "Fetching issues from $REPO..." >&2
ISSUES_JSON=$(gh issue list --repo "$REPO" --state open --limit 500 --json number,title,assignees,labels,updatedAt,body)

# Generate markdown header
cat > "$OUT_FILE" <<HEADER
# Open Issues — open-austin/org

**Generated:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

This snapshot groups issues by team label for triage purposes. Issues without team labels appear under "Unlabeled."

---

HEADER

# Parse JSON and render markdown
echo "$ISSUES_JSON" | jq '
  # Team labels in priority order
  ["finance", "fundraising", "communications", "engagement", "education", "infrastructure", "product team", "community", "board"] as $team_labels |
  
  # For each issue, find its first team label
  map(
    (
      .labels | map(.name) | . as $label_names |
      ($team_labels[] | select(. as $tl | $label_names | index($tl))) // "unlabeled"
    ) as $group_label |
    . + {group_label: $group_label}
  )
' | jq -r '
  # Group by label
  group_by(.group_label) |
  
  .[] |
  
  # Render group header
  "## " + (.[0].group_label | ascii_upcase) + "\n",
  
  # Render each issue in group
  (.[] |
    # Calculate staleness
    (now - (.updatedAt | fromdateiso8601)) / 86400 | floor as $days_stale |
    
    # Format assignees
    (if .assignees | length > 0 then
      " | **Assigned:** " + (.assignees | map(.login) | join(", "))
    else
      ""
    end) as $assignee_text |
    
    # Body preview
    ((.body // "") | gsub("\n"; " ") | .[0:200]) as $body_preview |
    (if $body_preview | length >= 200 then $body_preview + "..." else $body_preview end) as $body_text |
    
    # Output
    "\n### [#\(.number)] \(.title)\n\n" +
    "**Updated:** \($days_stale)d ago\($assignee_text)\n\n" +
    (if $body_text | length > 0 then $body_text + "\n\n" else "" end) +
    "---\n"
  )
' >> "$OUT_FILE"

echo "✓ Issues synced to $OUT_FILE" >&2
