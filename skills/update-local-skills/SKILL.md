---
name: update-local-skills
description: "Update existing repo-local skill copies from global seed skills while preserving local divergence. Use when the user asks to refresh, sync, compare, or update local skills from their global/source versions, especially after global skill taxonomy or workflow changes."
---

# Update Local Skills
## Local Precedence
If the current repo already has `skills/update-local-skills/SKILL.md`, read and follow the repo-local skill first. Treat the global skill as fallback seed material. Preserve this repo's Open Austin-specific write-safety and public-org boundaries.

## Purpose
Use this skill when a repo already has local `skills/` and the user wants to update one or more local copies from a global seed source.

Locate the seed library from the user's request, project configuration, or installed skill catalog. Do not assume a personal checkout location. Ask for the source only if the available context cannot resolve it.

Default local target:

```text
repo/skills/
```

This is different from first-time vendoring. Use `setup-local-skills` when copying skills into a repo that does not yet carry them.

## Core Rule
Never silently overwrite a local skill.

The value of this workflow is the comparison: what changed upstream, how the local copy diverged, and whether those differences should be preserved, merged, or replaced.

## Workflow
1. Identify the repo root and the local `skills/` directory.
2. Identify the requested skill names. If the user asked for "all," list local skills and matching seed skills.
3. Read each global seed `SKILL.md` and each local `SKILL.md` in full, then inspect changed or referenced supporting resources and metadata.
4. Compare:
   - upstream changes in the seed
   - local project-specific divergence
   - direct conflicts where both changed the same guidance
   - introduced dependencies, personal paths, private examples, or references unavailable in the target project
5. Report the comparison before editing unless the user explicitly requested a verbatim overwrite.
6. Apply upstream changes while preserving intentional local divergence.
7. If a conflict is substantive, ask the user rather than guessing.
8. Validate edited skills when practical. Check that required relative resources resolve and separately installed dependencies have an available or documented setup route; inspect supporting files as well as `SKILL.md`.
9. Report updated skills, explicit adaptations, dependencies still unavailable, and any skills left untouched. Do not equate matching the seed with being usable after clone.

## What To Preserve
Project-local divergence may include:

- repository-relative paths
- project-specific authority order
- validation commands
- public/private boundaries
- local docs taxonomy
- domain vocabulary
- user taste or quality rules

Do not replace these with generic seed text unless the user explicitly asks to reset the local copy.

Personal absolute paths and assumed home-directory layouts are portability defects, not useful project specialization. Resolve them through supplied relative resources, documented configuration, or discovery without losing the underlying workflow. Preserve actual platform-required paths when justified. Repair reusable seed defects when authorized and disclose target-specific adaptations; do not silently introduce a dependency on the maintainer's private tools or global skills. Keep required dependencies distinct from optional integrations.

## Rename Handling
When a global skill has been renamed:

1. Check whether the local repo still has the old skill name.
2. Confirm the rename maps to the same workflow.
3. Move the local skill folder to the new name if the project should follow the rename.
4. Update references in local docs and `AGENTS.md`.
5. Preserve local content while adapting names and paths.

Do not leave both old and new local skill names active unless the user wants a transition period.

## No Metadata Merge System
Do not add version fields, hashes, merge markers, or source metadata to skill files. The repo's version control is the undo mechanism, and the human review is the merge mechanism.
