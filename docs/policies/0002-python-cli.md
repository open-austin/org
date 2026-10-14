# 0002 — Python CLI over Shell Scripts
## Current Approach
Use Python 3 for substantive CLI tools. Thin shell wrappers may provide familiar entry points. Current examples include `tools/airtable/` and `tools/google-docs/`; the retired `tools/sync/` scripts are historical examples, not missing dependencies.

## Rationale
1. **Native JSON handling:** Python's `json` module is more intuitive than multi-stage `jq` pipelines for complex transformations
2. **Better error messages:** Python exceptions are clearer than `jq: error (at <stdin>:490): Cannot index number with string "assignees"`
3. **Easier to extend:** Future write tools will need argument parsing, validation, dry-run logic — Python's standard library handles this cleanly
4. **Testability:** Python functions can be unit tested; shell pipelines are harder to test in isolation
5. **Readability:** The logic is explicit and procedural, not spread across multiple chained commands

**Tradeoff:** Python is slightly more verbose than shell one-liners, but the improved clarity and maintainability justify the cost.

## Operating Notes
Document Python and each tool's actual runtime dependencies in its setup instructions. Prefer standard-library argument parsing, validation, JSON handling, and dry-run logic where sufficient; inspect a tool's current implementation instead of inferring its dependencies from retired sync tooling.

## Links
- [Tooling history](../archive/github-tooling.md)
- [Sync retirement](../archive/retire-sync-tooling.md)
- `docs/policies/0001-tooling-foundations.md` — foundational architectural choices
