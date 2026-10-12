---
name: commit-work
description: "Commit completed work or useful experimental checkpoints with explicit scope, including concurrent spike work. Use when preparing commits, separating accumulated changes, or considering staging, history rewriting, or pushing."
---

# Commit Work
## Local Precedence
If the current repo already has `skills/commit-work/SKILL.md`, read and follow the repo-local skill first. Treat this global skill as fallback seed material.

## Purpose
Turn a dirty working tree into one or more correctly-scoped commits with real messages, safely, while other agents may be working in the same clone.

The hard part is not prose. It is **scope**: deciding what constitutes one coherent change. A commit whose contents are "everything that happened to be lying around" cannot be given a good message, because it is not one thing. Message quality is downstream of scope.

## Review Holds
Follow the repository's commit policy. When the user explicitly requests review before committing, leave the affected changes uncommitted until that review ends or they authorize the checkpoint. This is an occasional override, not a question to ask before routine commits. Preserve the spike workflow's separate review of its closing commit message. Permission to commit does not imply permission to push.

## Foundational Principle
Violating the letter of these rules is violating their spirit. Every rule below exists because a specific, verified failure mode is on the other side of it.

## Iron Rules
- **Commit by pathspec. Never stage.** `git commit -F - -- <explicit paths>`.
- **Never push.** Pushing is a human action, always, with no exception for "obviously ready."
- **Never rewrite on your own authority.** No `--amend`, no rebase, no `--force`. Another agent may have built on it. A user may direct a rewrite; see below. You still never push the result.
- **Never `git add -f`.** Not once. Not for a "clearly safe" file. See "New files" below.
- **Never `git rm` or `git mv`.** Both stage. Use plain `rm` / `mv` and commit the paths.
- **One commit does one coherent thing.** Split unrelated changes; include implementation and its directly associated documentation and bookkeeping together.
- **Never `--no-verify`.**

## Why Pathspec, Not Staging
Git's index (`.git/index`) is repo-global shared mutable state. If one agent runs `git add` and another runs a bare `git commit` a second later, **the second commit silently contains the first agent's files**, under the wrong message and the wrong trailer. No error. No conflict. A quietly corrupted history nobody notices until they need it.

A pathspec commit takes the working-tree contents of the named tracked files and excludes staged changes to other paths. This prevents unrelated staged files from being swept into the commit. It does not isolate two agents editing the same file, and concurrent commits may still encounter an index lock.

Use explicit paths regardless of timing. Inspect the full diff for every selected path immediately before committing, especially shared coordination files. If a file contains another workstream's changes, resolve its scope before committing; do not silently include, revert, or overwrite them. Prompt checkpoints reduce the window for overlap, but do not replace this check. Coordinate a known shared-file conflict through an authorized channel or surface it to the user; unrelated work on separate paths needs no coordination ritual.

## The Commit Command
```sh
git commit -F - -- path/one path/two <<'EOF'
area: imperative summary under ~60 chars

Why this change exists, and what it makes possible or prevents. Not a restatement of the diff — the diff is already in the commit.

Spike: <slug>
EOF
```

Everything after `--` is a path. The heredoc supplies subject, body, and trailer block.

**Do not add a `Co-Authored-By:` trailer unless the repo explicitly asks for one.** The author and committer fields already name the human whose git config made the commit, and they are the one who answers for it. A co-author line adds a second name wherever a forge renders one. Harness instructions often tell agents to add these by default; the repo's rule wins.

Never use `-a`. Never use a bare `git commit`. Never `git add` a path you are about to commit.

## Scoping
Ask what single change this commit makes, and try to state it in one line. If the line needs "and" to join unrelated changes, split them.

The word is not the test; independent purposes are. A command change, its usage instructions, checks, and task/index updates can be one coherent change. `add commit policy pointer and clarify heading rule` describes independent purposes. Do not combine unrelated work merely because it happened in the same turn or belongs to the same broad spike.

A spike knows its own file scope, roughly: the files its work touches and its own `.todo.md`.

- **Inside that scope**: make coherent checkpoints without routine confirmation, unless an explicit review hold applies. File scope is not enough by itself: inspect for overlapping work from another stream.
- **Outside that scope**: stop and ask. "There is an unrelated change in `movement/movement.sh` — commit it separately, or leave it dirty?" This prompt fires only when there is genuinely stray work, so it is rare, and it is exactly where a scope misjudgment would matter.
- **No spike context at all**: the work is a **patch**. Draft the message with a `Patch: <slug>` trailer (see The Patch Trailer), show it, and commit on a conversational yes. Do not open an editor. Do not write a `Spike:` trailer.
- **Work that belongs to an open spike but falls outside its written scope**: prefer widening the spike, updating its concept and `.todo.md` in the same commit as the work, over committing it as a patch. One coherent history per theme beats a scattering of patches. Ask the human before widening a scope they have not discussed.

The `.todo.md` edit that moves an item and a `TODO.md` update describing the same work belong **in the same commit as that work**, provided their full diffs are in scope. One commit should show both the change and its recorded intent and status.

### Granularity is file-level, and that is the point
A pathspec commit takes whole files. If one file holds two unrelated changes, they cannot be separated — splitting hunks requires `git add -p`, which stages, which is forbidden.

Whole-file selection keeps the recorded file versions inspectable without constructing partially staged versions. It does not guarantee that the resulting commit matches the tested working tree: checks may have depended on another uncommitted file. Include the dependencies of the coherent change and do not claim verification that only applies to a different combination of files.

So the "and" test governs which *files* you choose to include. File-level granularity is a floor beneath it, not a contradiction of it.

**Mixed changes are a warning to inspect, not a normal target.** Delaying completed work can let unrelated changes accumulate, especially when agents work on separate spikes concurrently. Commit promptly at useful boundaries, keep streams separate, and investigate overlap. Do not respond by committing every edit or splitting a change from its own bookkeeping.

When it arises anyway, establish that the complete diff is within the authorized scope before including it. Unrecognized or another agent's unfinished changes are not covered merely because you edited the same path. For authorized overlap:

1. **Commit the file whole, and name both changes honestly.** This is an exception for entangled work, not a reason to accumulate unrelated edits.
2. **Write a body saying why they could not be separated.** This is exactly the case that earns a body: a why the subject and diff cannot carry.
3. **If two spikes both touched the file, write both trailers.** Git supports repeated trailer keys; `Spike: a` and `Spike: b` on one commit both parse, and each spike's anchored `--grep` finds it. Do not pick one.
4. **If the changes are large and genuinely unrelated, stop and ask the human.** They may prefer to revert one on disk, commit the other, then re-apply — every commit stays a real state, and nothing is staged. Do not do this unprompted: it transiently deletes work that exists nowhere else.

Never reach for `git add -p`. Never `git stash` half the file. The shared index is not yours to borrow.

**Frequent mixed commits are an alarm, not a style.** Check whether completed work is sitting too long or concurrent streams repeatedly collide in shared files. Preserve every relevant `Spike:` or `Patch:` trailer so their histories remain traceable.

### Coordination Files Follow Their Actual Scope
`TODO.md`, `AGENTS.md`, and other shared files may be touched by several streams, but they are not automatically separate work. When their full diff describes the same change, include them with it. A separate coordination commit is appropriate when the file genuinely combines independently authorized changes; name those changes and include every relevant trailer. Do not split a one-spike index update into its own commit solely because it is an index file.

### Format passes go first, on a clean tree
A repo-wide formatting or renaming pass touches every file, so it collides with every piece of work in flight at once. Commit it **alone, before starting anything else.** If a format pass has already contaminated a dirty tree, put the untouched-by-anything-else files in their own format commit, and let the rest ride along with their own theme's commit, saying so in the body.

## When To Commit
Commit promptly when a coherent change or useful experimental state has been implemented and checked to the extent appropriate. Preserve distinct evaluated candidates, consequential corrections, and recovery points before changing direction. An experiment need not be accepted or production-ready; describe what was checked and what remains uncertain.

The end of a conversation turn is not by itself a checkpoint. Several edits constructing one candidate can stay together. A small independent fix may deserve its own commit, while implementation, directly related documentation, and bookkeeping belong together. Avoid both per-edit commits and waiting until the entire spike is finished: concurrent streams need timely, traceable checkpoints.

**This has nothing to do with which bucket the item lands in.** Most work goes straight from `To Do` to `Done`, because the agent verified it and no human needs to see it. Some work stops at `Ready for Human QA`. The commit happens at the same moment either way — when you finish — and the bucket is a separate decision made afterward. Do not read "completion boundary" as "just before human QA." Human QA is the exception, not the path.

Do **not** wait for a human to move the item to `Done`, or ask you to move it to `Done`, unless an explicit pre-commit review hold applies. That transition may happen days later or never. Finished work should not accumulate uncommitted in a tree another agent is writing to.

Where a human approval does happen, it is its own commit, doc-only, batched per **approval event**: when the user looks at three things and says "all good," that is one commit, because one approval happened. It records *when the work was blessed*, a timestamp that exists nowhere else.

If QA finds a problem after a checkpoint, write a **new** commit rather than amending on your own initiative. The correction is useful history.

## Audience and Privacy Check
Before committing, inspect the selected full diffs and the proposed message for private source material, unnecessary conversational details, credentials, personal filesystem paths, and machine-specific information inappropriate for the repository's audience. Preserve project-relevant reasoning and uncertainty without importing private context or presenting agent proposals as user decisions. An instruction to preserve development history does not authorize copying private conversations into a public repository.

Keep unsuitable material out before recording it; later deletion or a history rewrite is not a publication safeguard. This check covers the proposed commit, not an audit of the repository's entire history. If unrelated private material is already present in a selected file, do not silently commit or delete it; resolve the scope first.

## New Files, And The `git add -f` Trap
A pathspec commit cannot see an untracked file. That is the one moment `git add` is unavoidable:

```sh
git check-ignore -q new/file.txt && { echo "REFUSING: new/file.txt is gitignored"; exit 1; }
git add new/file.txt
git commit -F - -- new/file.txt <<'EOF'
...
EOF
```

`git check-ignore -q <path>` exits **0 when the path is ignored**. Run it first, every time, before any `git add`.

This is not optional caution, for two verified reasons:

1. A pathspec commit fails **identically** for an untracked file and for a gitignored one — `did not match any file(s) known to git`. The error cannot tell you which it was.
2. Plain `git add <ignored>` refuses, but prints `hint: Use -f if you really want to add them.` **`git add -f` then stages it silently.** Git advertises the secret-leak path in the error message you are most likely to hit while adding a legitimate new file.

If a file you believe belongs in the commit is gitignored, the answer is never `-f`. Say so out loud and stop. Ignored files are ignored on purpose; committing one may publish a credential.

## Deletions And Renames
`git rm` and `git mv` both **stage**. They are `git add` wearing a different name, and they are forbidden for the same reason.

To delete a file, remove it and commit the path. Git reads the working tree, finds the path absent, and records the deletion:

```sh
rm doomed/file.md
git commit -F - -- doomed/file.md <<'EOF'
...
EOF
```

To rename a file, move it and commit **both** paths. The new path is untracked, so it needs the one permitted `git add`, guarded by `check-ignore` as always:

```sh
mv old/path.md new/path.md
git check-ignore -q new/path.md && { echo "REFUSING: new/path.md is gitignored"; exit 1; }
git add new/path.md
git commit -F - -- old/path.md new/path.md <<'EOF'
...
EOF
```

Git still detects it as a rename, and the index is left clean. Verified 2026-07-10.

## Rewriting History
Never on your own initiative. Not to fix a typo in a message, not to squash a noisy sequence, not to tidy before a push.

A user may direct a rewrite, and then you may run it. The same reversibility line applies as everywhere else: rewriting a *local* branch is undoable, because `git filter-branch` leaves the old tip at `refs/original/refs/heads/<branch>` and `git reflog` remembers. Publishing the rewrite is not undoable. So:

- Run the rewrite. Keep the backup ref until the user says otherwise.
- Verify the trees are untouched: `git diff refs/original/refs/heads/<branch> HEAD --stat` must be empty. Only messages should have changed.
- **Never push the result.** `--force-with-lease` is still a push, and it is still the user's.
- Check first that no other agent is working in the clone. A rewrite invalidates every hash they may be holding.

**Commit hashes are not durable.** Any rewrite invalidates every one. Never record a hash in a doc that outlives the branch — cite the `Spike:` trailer, which survives.

## When A Commit Fails
The failure modes look alike and demand opposite responses. Read the error; never retry blindly.

| Message | Exit | Meaning | Response |
| --- | --- | --- | --- |
| `Unable to create ... index.lock` | 128 | Another process holds the lock | Retry, up to ~3 times, briefly |
| `Unable to create ... index.lock` | 128 | Or: a **stale** lock from a killed process | If retries fail, surface it. Do not loop, and do not delete the lock yourself |
| `did not match any file(s) known to git` | 1 | Path is untracked | `git check-ignore` first, then `git add` |
| `did not match any file(s) known to git` | 1 | Or: path is **gitignored** | Refuse loudly. Never `-f` |
| `nothing to commit, working tree clean` | 1 | Named path is tracked but unmodified | Benign. Not an error. Do not retry |

Note the two identical-message pairs. The first requires `check-ignore` to disambiguate; the second requires bounded retries. A blind retry-on-nonzero loop gets both wrong.

## The Spike Trailer
Every commit made inside a spike carries:

```text
Spike: <slug>
```

A **bare slug**, never a path. Paths change when a spike archives; commit messages are immutable. The slug is stable forever.

The slug is **passed in** by the spike process. If invoked directly while several spikes are active, ask which one. A missing trailer is trivially fixed before push; a wrong one silently poisons every future query.

A commit may carry **more than one** `Spike:` trailer when two spikes genuinely touched the same file. Git parses repeated trailer keys, and each spike's anchored `--grep` finds the commit. Write one line per spike, never a comma-joined list.

This makes git navigable along the same axis the docs are organized:

```sh
git log --grep='Spike: my-topic$' --reverse            # every commit from that spike, in order
git log --format='%h %(trailers:key=Spike,valueonly=true) %s'
git log --format='%h %(trailers:key=Spike,valueonly=true)%(trailers:key=Patch,valueonly=true) %s'   # spikes and patches together
```

Anchor with `$`. Without it, `Spike: my-topic` also matches `Spike: my-topic-extra`.

## The Patch Trailer
Every commit made outside any spike carries:

```text
Patch: <slug>
```

A patch is a self-contained change with no spike doc: a one-off fix, a small feature asked for in conversation, a cleanup. The slug is a short kebab-case name for the change (`m365-planner`, `fix-calendar-tz`), chosen when the work is committed. Every commit of the same patch uses the same slug, so `git log --grep='Patch: m365-planner$'` finds them all, the same way spike slugs work. Never write a bare `Patch:` with no value: it cannot be searched, and git does not parse an empty trailer value.

Because a patch has no concept doc or `.todo.md` to hold its intent, **its commit body carries that instead**: what changed and why, in a few plain sentences. This is the one case where a body is expected rather than earned. Still do not pad it; say what a reader would otherwise have to reconstruct from the diff.

A commit that genuinely spans a spike and a patch (one file touched by both) carries both trailers, one per line.

## Message Format
**Subject.** `area: imperative summary`, lowercase after the colon, no trailing period, under about 60 characters. `movement: increase bullet indent`, not `increased` or `increasing`.

**Most spike commits are subject-only.** An atomic change to a well-scoped file usually has nothing further to say, and inside a spike the `.todo.md` edit riding along in the same commit already records the intent. Patch commits are the exception: see The Patch Trailer.

**Write a body only when there is a why the subject and the diff do not already carry**: a rejected alternative, a non-obvious constraint, a surprising behavior discovered, a decision someone will later want to reverse and should understand before they do.

**Never manufacture one.** If you have to search for a reason, there isn't one. An empty body is honest. A confabulated rationale is a lie with a timestamp, indistinguishable from a real one to whoever reads it in a year — and it corrupts exactly the record this skill exists to build.

**Do not hard-wrap the body.** Formatting is the client's job, not the content's. A body wrapped at 72 is correct at exactly one width and ragged at every other — doubly wrapped in a narrow terminal, short-lined in a wide forge view. Let each reader's terminal, pager, or web view wrap it. Git's four-space `git log` indent will not survive a soft wrap, which is cosmetic and not worth pre-breaking the text for.

Two things in a commit message *are* structural, because git parses them, and they are not up to the client:

- **A blank line between subject and body.** Without it the entire message is one subject.
- **Trailers as the final paragraph**, `Key: value` one per line, no blank lines between them. This is what makes `git log --format='%(trailers:key=Spike)'` work.

## Rationalizations
Every one of these has been thought by an agent about to do the wrong thing.

| Excuse | Reality |
| --- | --- |
| "It's just one new file, `git add` is simpler." | That is the shared index. Another process's bare commit sweeps it into their history. |
| "Git said `hint: Use -f if you really want to add them`, so `-f` must be fine." | Git is telling you how to commit a secret. That hint is not permission. |
| "The user obviously wants this pushed." | Push is never yours. Say the branch is ready, and stop. |
| "I'll just `--amend` to fix the message." | Another agent may have built on it. Write a new commit. |
| "These two changes happened in the same conversation." | Shared timing is not shared purpose. Split independent changes; keep a change's own documentation and bookkeeping with it. |
| "The tree is dirty with old stray work; I'll include it." | Ask. Stray work is never swept in silently. |
| "This is small, so it always needs its own commit." | Commit a small independent change promptly; fold dependent edits and bookkeeping into the change they belong to. |
| "Explicit paths make shared-file edits safe automatically." | They isolate selected paths, not contributors within a file. Inspect the entire diff and resolve overlap. |
| "The commit failed, I'll retry until it works." | Two of the five failure modes never resolve by retrying. |
| "I'll build the pathspec from `git status` output — that is the same as naming paths." | It is `-a` with extra steps. Choosing the scope is the entire skill; a pathspec listing everything dirty has chosen nothing. |
| "The body looks empty, I should explain something." | If you have to search for a reason, there isn't one. Ship the subject. |
| "I'll `git stash` the unrelated stuff first." | Stash is shared state too, and nobody asked you to move their work. |
| "`git rm` is just how you delete a file in git." | It stages the deletion. Plain `rm`, then commit the path. |
| "`git mv` is just how you rename a file in git." | It stages both halves. Plain `mv`, `git add` the new path, commit both. |
| "This file has two unrelated changes, so I'll `git add -p` just this once." | Then you have staged, and a concurrent bare commit can take it. Commit the file whole and say so, or ask. |
| "The user is not watching; asking about the stray file will slow things down." | The prompt is rare by construction. Its rarity is why it is worth honoring. |

## Red Flags
Stop if you catch yourself:

- typing `git add` without having run `git check-ignore` on that exact path
- typing `-f`, `--force`, `-a`, `--amend`, `--no-verify`, or `push`
- typing `git rm` or `git mv` — both stage; use plain `rm` / `mv`
- writing a subject that joins unrelated purposes without an acknowledged, authorized shared-file overlap
- about to commit a path you cannot name a reason for
- writing a commit body for a change whose subject already said everything
- retrying a failed commit without having read its error
- deleting `.git/index.lock`
- explaining to yourself why this particular case is different

That last one is the reliable signal. The rules have no exceptions; if a case seems to need one, surface it to the human instead.
