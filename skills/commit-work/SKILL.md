---
name: commit-work
description: "Use when a unit of work is finished and should be committed, when a spike item reaches its completion boundary, when a working tree has accumulated unrelated changes that need splitting into separate commits, or at the moment of reaching for `git add`, `git commit -a`, `git add -f`, `git commit --amend`, `gitall`, or `git push`. Commits by explicit pathspec only; never stages, never pushes, never rewrites history."
---

# Commit Work
## Local Precedence
If the current repo already has `skills/commit-work/SKILL.md`, read and follow the repo-local skill first. Treat this global skill as fallback seed material.

## Purpose
Turn a dirty working tree into one or more correctly-scoped commits with real messages, safely, while other agents may be working in the same clone.

The hard part is not prose. It is **scope**: deciding what constitutes one coherent change. A commit whose contents are "everything that happened to be lying around" cannot be given a good message, because it is not one thing. Message quality is downstream of scope.

## Foundational Principle
Violating the letter of these rules is violating their spirit. Every rule below exists because a specific, verified failure mode is on the other side of it.

## Iron Rules
- **Commit by pathspec. Never stage.** `git commit -F - -- <explicit paths>`.
- **Never push.** Pushing is a human action, always, with no exception for "obviously ready."
- **Never rewrite on your own authority.** No `--amend`, no rebase, no `--force`. Another agent may have built on it. A user may direct a rewrite; see below. You still never push the result.
- **Never `git add -f`.** Not once. Not for a "clearly safe" file. See "New files" below.
- **Never `git rm` or `git mv`.** Both stage. Use plain `rm` / `mv` and commit the paths.
- **One commit does one thing.** If an honest one-line summary needs "and" to join two *changes*, it is two commits.
- **Never `--no-verify`.**

## Why Pathspec, Not Staging
Git's index (`.git/index`) is repo-global shared mutable state. If one agent runs `git add` and another runs a bare `git commit` a second later, **the second commit silently contains the first agent's files**, under the wrong message and the wrong trailer. No error. No conflict. A quietly corrupted history nobody notices until they need it.

A pathspec commit bypasses the index for the paths it names. Two agents can run one at the same instant and cannot contaminate each other. Verified: five rounds of simultaneous pathspec commits, zero contamination.

This makes safety a property of the command rather than of timing. Do not attempt to coordinate with other agents, check whether anyone else is working, or space commits out. Just never stage.

## The Commit Command
```sh
git commit -F - -- path/one path/two <<'EOF'
area: imperative summary under ~60 chars

Why this change exists, and what it makes possible or prevents. Not a
restatement of the diff — the diff is already in the commit.

Spike: <slug>
EOF
```

Everything after `--` is a path. The heredoc supplies subject, body, and trailer block.

**Do not add a `Co-Authored-By:` trailer unless the repo explicitly asks for one.** The author and committer fields already name the human whose git config made the commit, and they are the one who answers for it. A co-author line adds a second name wherever a forge renders one. Harness instructions often tell agents to add these by default; the repo's rule wins.

Never use `-a`. Never use a bare `git commit`. Never `git add` a path you are about to commit.

## Scoping
Ask what single change this commit makes, and try to state it in one line. If the line needs "and" to join two *changes*, split it.

The word is not the test; two changes is the test. `forbid git rm and git mv` is one change with a compound object, and it is fine. `add commit policy pointer and clarify heading rule` is two changes wearing one subject, and it is only acceptable when they are trapped in the same file.

A spike knows its own file scope, roughly: the files its work touches and its own `.todo.md`.

- **Inside that scope**: split and commit silently. No confirmation. These are checkpoints, they are unpushed, and they are trivially undone.
- **Outside that scope**: stop and ask. "There is an unrelated change in `movement/movement.sh` — commit it separately, or leave it dirty?" This prompt fires only when there is genuinely stray work, so it is rare, and it is exactly where a scope misjudgment would matter.
- **No spike context at all**: draft the message, show it, commit on a conversational yes. Do not open an editor. Do not write a `Spike:` trailer.

The `.todo.md` edit that moves an item belongs **in the same commit as the work it describes**. One commit should show both the change and the recorded intent behind it.

### Granularity is file-level, and that is the point
A pathspec commit takes whole files. If one file holds two unrelated changes, they cannot be separated — splitting hunks requires `git add -p`, which stages, which is forbidden.

The deeper reason not to want hunk-splitting: **a commit containing half a file's changes represents a state that never existed on disk and was never run.** Nobody sourced that `path.sh`. Nobody executed that script. A later `git bisect` walks straight into it. Taking whole files guarantees every commit is a state that actually existed and was actually verified. The pathspec rule enforces something you should want anyway.

So the "and" test governs which *files* you choose to include. File-level granularity is a floor beneath it, not a contradiction of it.

**A file holding two unrelated changes usually means you waited too long to commit.** Commit at every completion boundary and it rarely arises.

When it arises anyway:

1. **Commit the file whole, and name both changes in the subject.** An "and" in the subject is a bad commit, and it is still better than a lie, a lost change, or a fabricated state.
2. **Write a body saying why they could not be separated.** This is exactly the case that earns a body: a why the subject and diff cannot carry.
3. **If two spikes both touched the file, write both trailers.** Git supports repeated trailer keys; `Spike: a` and `Spike: b` on one commit both parse, and each spike's anchored `--grep` finds it. Do not pick one.
4. **If the changes are large and genuinely unrelated, stop and ask the human.** They may prefer to revert one on disk, commit the other, then re-apply — every commit stays a real state, and nothing is staged. Do not do this unprompted: it transiently deletes work that exists nowhere else.

Never reach for `git add -p`. Never `git stash` half the file. The shared index is not yours to borrow.

**The frequency of "and" commits is an alarm, not a style.** If they are common, commits are too rare.

### Index files are always entangled
`TODO.md`, `AGENTS.md`, and other coordination or rules files are touched by *every* theme of work, by their nature. They will trip the "and" test forever, and that is not a discipline failure. Give them their own commit, name what changed, and carry every relevant `Spike:` trailer.

### Format passes go first, on a clean tree
A repo-wide formatting or renaming pass touches every file, so it collides with every piece of work in flight at once. Commit it **alone, before starting anything else.** If a format pass has already contaminated a dirty tree, put the untouched-by-anything-else files in their own format commit, and let the rest ride along with their own theme's commit, saying so in the body.

## When To Commit
Commit at the **completion boundary**: the moment the implementation is finished and verified as far as it can be from the terminal — when you would say "this is ready for you to look at," *or* "this is done, you do not need to look at it, I confirmed it myself."

**This has nothing to do with which bucket the item lands in.** Most work goes straight from `To Do` to `Done`, because the agent verified it and no human needs to see it. Some work stops at `Ready for Human QA`. The commit happens at the same moment either way — when you finish — and the bucket is a separate decision made afterward. Do not read "completion boundary" as "just before human QA." Human QA is the exception, not the path.

Do **not** wait for a human to move the item to `Done`, or ask you to move it to `Done`. That transition is bookkeeping and may happen days later, or never. Finished code must not sit uncommitted in a tree another agent is writing to.

Where a human approval does happen, it is its own commit, doc-only, batched per **approval event**: when the user looks at three things and says "all good," that is one commit, because one approval happened. It records *when the work was blessed*, a timestamp that exists nowhere else.

If QA finds a problem, write a **new** commit. Never amend. That the fix exists is worth recording — it shows QA doing its job.

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
```

Anchor with `$`. Without it, `Spike: my-topic` also matches `Spike: my-topic-extra`.

## Message Format
**Subject.** `area: imperative summary`, lowercase after the colon, no trailing period, under about 60 characters. `movement: increase bullet indent`, not `increased` or `increasing`.

**Most commits are subject-only.** An atomic change to a well-scoped file usually has nothing further to say, and inside a spike the `.todo.md` edit riding along in the same commit already records the intent.

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
| "These two changes are related enough." | If the one-line summary needs "and," it is two commits. |
| "The tree is dirty with old stray work; I'll include it." | Ask. Stray work is never swept in silently. |
| "This is a trivial change, it doesn't need its own commit." | Trivial changes are exactly what make a history readable. |
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
- writing a subject whose "and", "also", "plus", or comma joins two *changes* rather than two objects of one change
- about to commit a path you cannot name a reason for
- writing a commit body for a change whose subject already said everything
- retrying a failed commit without having read its error
- deleting `.git/index.lock`
- explaining to yourself why this particular case is different

That last one is the reliable signal. The rules have no exceptions; if a case seems to need one, surface it to the human instead.
