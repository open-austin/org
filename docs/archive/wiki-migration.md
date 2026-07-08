# Wiki Migration

## Goal

Get the content out of the Open Austin GitHub wiki and into Google Drive where non-technical contributors can actually find, read, and edit it.

The wiki is effectively invisible. Most contributors don't know it exists, don't have a workflow for editing it, and are intimidated by the GitHub-as-documentation interface. Google Drive is where Open Austin already does its collaborative document work — meeting notes, policies, guides, shared knowledge. The wiki should follow.

---

## Non-Goals

- We are not deleting the wiki. It stays as-is until migration is confirmed complete.
- We are not migrating issue tracker content here — that's the backlog triage spike.
- We are not deciding the full long-term documentation architecture for the org. This spike is specifically about moving existing wiki content to a more accessible home.
- Google Drive agent tooling is a future consideration. Once this migration is done, giving agents Google Drive access would allow them to read org docs, meeting notes, etc. as context — but that's outside this spike.

---

## Why the Wiki Is the Wrong Home

- Editing requires a GitHub account and comfort with either the web editor or git
- It's not surfaced anywhere in the org's regular workflows (Slack, events, etc.)
- Search is poor compared to Google Drive
- Non-programmers (designers, PMs, community stakeholders) are unlikely to contribute to it
- The contributor policy and org ethos lean toward "accessible and open" — a GitHub wiki fails the accessibility bar for most of the org's contributors

---

## Technical Facts

The GitHub wiki is a real git repository, separate from the main repo:

```sh
git clone https://github.com/open-austin/org.wiki.git
```

This gives us a local checkout of all wiki pages as Markdown files. From there:
- We can read and render the full content
- We can produce a clean export for Google Drive
- We can identify what's worth migrating vs. what's stale/redundant

The wiki repo is separate from `open-austin/org` — changes to the wiki don't appear in the main repo's history.

---

## Approach

1. **Clone the wiki** — `git clone https://github.com/open-austin/org.wiki.git` into a local working directory (not committed to the org repo)
2. **Inventory the content** — list all pages, assess staleness, flag anything that's clearly outdated or redundant
3. **Export to Google Drive** — convert Markdown to Google Docs format (or paste as clean text); organize into a sensible folder structure
4. **Human review** — someone (you, or a future team chair) confirms the Google Drive structure looks right before the wiki is formally retired
5. **Point the wiki at Google Drive** — leave a short note in the wiki pointing to where the content now lives, so anyone who finds the wiki via old links isn't stranded
6. **Formally retire the wiki** — once migration is confirmed, it becomes read-only historical reference

---

## Open Questions

- Where in Google Drive should this land? Is there an existing "Open Austin Docs" folder structure, or does one need to be created?
- Who has the authority to archive or retire the wiki? Probably a Board resolution isn't needed, but the right person should sign off.
- Is any wiki content sensitive enough that it shouldn't be public? (Google Drive docs shared with "anyone with the link" vs. restricted to org members.)
- After migration: should new org documentation live in Google Drive, the GitHub repo, or both? Need a clear norm so content bifurcate again.
- **Board onboarding doc:** When reviewing the wiki for migration, check if there's existing board onboarding material. If not, creating one should be part of this work (closed #393 with note that onboarding should be handled here).
