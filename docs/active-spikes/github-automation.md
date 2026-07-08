# GitHub Automation

## Goal

Reduce the manual work of keeping boards and issue state in sync, and prevent the "No Status drift" problem where issues accumulate on the Org Kanban without being deliberately placed there.

The current problem: Open roles were landing on the Org Kanban as "No Status" because GitHub adds new issues to all boards with no routing logic. This required manual triage to sort out.

---

## Non-Goals

- Not replacing human judgment on issue disposition
- Not automating governance decisions
- Not building anything that fires unsolicited notifications to contributors

---

## Automation Ideas

### 1. Open Role Routing

**Trigger:** Issue gets `open role` label added
**Action:** Add to Open Roles board (if not already there); remove from Org Kanban (if present)

**Why:** Open roles have their own board. They shouldn't pollute the Org Kanban with "No Status" noise.

**Implementation:** GitHub Actions `on: issues` → `labeled` event, GraphQL mutation to add/remove board items.

---

### 2. New Issue → Org Kanban "To Do"

**Trigger:** Issue opened (without `open role` label)
**Action:** Add to Org Kanban under "To Do" status

**Why:** Currently new issues land with "No Status" or don't land on the board at all. "To Do" is the right default — it surfaces new work to the right triage view without requiring manual board management.

**Note:** Need to handle the race condition where `open role` is added shortly after issue creation (labeling event should override the initial routing).

---

### 3. Filled → Auto-Close

**Trigger:** Open Roles board item moved to "Filled" status
**Action:** Close the linked issue with a comment ("Role filled — closing issue.")

**Why:** Roles get filled but issues stay open because closing is a separate manual step. Keeping them open creates noise.

**Implementation:** GitHub Actions `on: projects_v2_item` → `edited` event, check if status changed to "Filled", close the linked issue.

**Note:** "Filled" column needs to exist on the Open Roles board first.

---

### 4. Done → Archive After 6 Months

**Trigger:** Scheduled (weekly or monthly cron)
**Action:** Find Org Kanban items in "Done" with `updatedAt` > 6 months ago, archive them off the board

**Why:** The Org Kanban had 47 Done items cluttering the board. Automated archiving keeps the Done column from becoming a graveyard.

**What archiving does:** Removes the item from the active board view. The underlying issue is unaffected. Archived items are visible in the project's Archive tab.

**Implementation:** `gh api graphql` to query items, then `archiveProjectV2Item` mutation for each qualifying item. Needs care around rate limits with large boards.

---

### 5. Issue Closed → Move to Done

**Trigger:** Issue closed
**Action:** If the issue is on Org Kanban and not already in "Done", move it there

**Why:** Right now there's no feedback loop — closing an issue doesn't update board state. This creates "open items" on the board that are actually resolved.

---

### 6. Team Views

Rather than creating a separate board per team (which fragments the org's work into silos), team-specific views are better handled via **Org Kanban saved filters** by label. For example, a Communications Chair would use a filter on the Org Kanban for `label:communications`.

This is preferable to separate boards because:
- All work stays in one place for cross-team visibility
- No duplicate board management
- Chair gets a filtered view of their work without a separate repo

Note: Liani created a separate Engagement Team board in its own repo. Worth discussing whether that work should migrate back into `open-austin/org` for consistency. Keeping it in a separate repo creates a split in where engagement work lives.

---

### 7. Slack Integration

All Slack notifications use plain **Incoming Webhooks** — a curl POST to a webhook URL. No Slack SDK, no app plugins beyond the initial webhook creation.

Setup per channel:
1. Go to `api.slack.com/apps` → create or select an app → Incoming Webhooks
2. Add webhook for the target channel
3. Copy the URL into `.env` as `SLACK_WEBHOOK_<CHANNEL>` and into GitHub Actions secrets

Current webhooks:
- `SLACK_WEBHOOK_ENGAGEMENT` — `#t-engagement` channel (role pipeline reports, stale role warnings)
- `SLACK_WEBHOOK_ORG` — `#oa-org` channel (weekly org summary, manually posted)

| Board | Number | Project ID |
|---|---|---|
| Org Kanban | 9 | `PVT_kwDOAA7NZM4AqQF8` |
| Open Roles | 6 | `PVT_kwDOAA7NZM4AmdbW` |

### Org Kanban Status Field

**Field ID:** `PVTSSF_lADOAA7NZM4AqQF8zghh1hc`

| Option | ID |
|---|---|
| To Do | `f75ad846` |
| Blocked | `b22db561` |
| In Progress | `47fc9ee4` |
| Done | `98236657` |

### Open Roles Status Field

**Field ID:** `PVTSSF_lADOAA7NZM4AmdbWzgeWrcw`

| Option | ID |
|---|---|
| Open | `f75ad846` |
| In Progress | `561a5d37` |
| Filled | `47fc9ee4` |

### Existing Workflows

`.github/workflows/open-role-add.yaml` — Already exists. Triggers on `issues: labeled`, adds issues with `open role` label to the Open Roles board (project #6). Uses `actions/add-to-project@v0.5.0` and `ACTIONS_TOKEN` secret.

**Gap:** This adds to Open Roles but does not remove from Org Kanban. New `open role` issues still land on the Org Kanban as "No Status."

### Secrets

`ACTIONS_TOKEN` — already configured on the repo. Needed for GraphQL mutations (board operations require a token with `project` scope, which `GITHUB_TOKEN` doesn't cover for org-level projects).

---

## Open Questions

- For Done→Archive: `updatedAt` on the project item is the best proxy for "time in Done" since Projects v2 doesn't expose when a status changed. 6-month threshold seems right but can be tuned.
- New issue → "To Do" routing: treat as opt-out (all non-`open role` issues go to Org Kanban). PRs should be excluded.
- `actions/add-to-project@v0.5.0` in the existing workflow is outdated — replace with direct GraphQL in the new unified workflow.
- Rate limits: the Done→Archive scheduled job needs to handle boards with many items gracefully.

---

## Implementation Order

1. Open role routing (highest impact — fixes the root cause of board noise)
2. New issue → "To Do" (establishes good hygiene going forward)
3. Issue closed → Done (closes the feedback loop)
4. Filled → auto-close (nice-to-have for Open Roles lifecycle)
5. Done → auto-archive (scheduled cleanup, lower urgency now that board is cleaned)
