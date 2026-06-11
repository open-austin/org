# 0002 — Python CLI over Shell Scripts

**Date:** 2026-06-10
**Status:** Accepted

---

## Context

During implementation of the sync tools (issues, labels, boards), we needed to decide between shell scripts with `jq` processing vs. Python scripts with native JSON handling.

Initial implementation attempted shell + `jq`, but encountered complexity with:
- Complex grouping and nested data structures
- String interpolation within jq expressions
- Debugging multi-stage pipelines
- Handling edge cases in date parsing

---

## Decision

Use Python 3 for CLI tools, not shell scripts.

The sync tools are implemented as:
- `tools/sync/issues.py`
- `tools/sync/labels.py`
- `tools/sync/boards.py`
- `tools/sync/run.sh` (thin wrapper)

---

## Rationale

1. **Native JSON handling:** Python's `json` module is more intuitive than multi-stage `jq` pipelines for complex transformations
2. **Better error messages:** Python exceptions are clearer than `jq: error (at <stdin>:490): Cannot index number with string "assignees"`
3. **Easier to extend:** Future write tools will need argument parsing, validation, dry-run logic — Python's standard library handles this cleanly
4. **Testability:** Python functions can be unit tested; shell pipelines are harder to test in isolation
5. **Readability:** The logic is explicit and procedural, not spread across multiple chained commands

**Tradeoff:** Python is slightly more verbose than shell one-liners, but the improved clarity and maintainability justify the cost.

---

## Consequences

- Sync tools require Python 3 (present on macOS by default)
- No external dependencies beyond `gh` CLI (which provides the data)
- Write tools (Phase 2) will also be Python scripts
- `tools/sync/run.sh` remains shell to maintain the familiar entry point pattern from LifeOS tools

---

## Related

- `docs/github-tooling.md` — conceptual doc for tooling architecture
- `docs/github-tooling.todo.md` — tracks implementation progress
- `docs/decisions/0001-tooling-foundations.md` — foundational architectural choices
