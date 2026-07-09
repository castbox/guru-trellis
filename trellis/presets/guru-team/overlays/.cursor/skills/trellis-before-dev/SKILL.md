---
name: trellis-before-dev
description: "Discovers and injects project-specific coding guidelines from .trellis/spec/ before implementation begins. Reads spec indexes, pre-development checklists, and shared thinking guides for the target package. Use when starting a new coding task, before writing any code, switching to a different package, or needing to refresh project conventions and standards."
---

<!-- guru-team-overlay: v1 -->

Read the relevant development guidelines before starting your task.

Execute these steps:

1. **Validate the planning start gate before editing**:
   ```bash
   .trellis/guru-team/scripts/bash/check-planning-approval.sh --json --task <task-path>
   ```
   Stop if the artifact is missing, old schema, lacks passed
   `ambiguity_review` evidence, does not use
   `user_confirmation.source=explicit-post-planning-review`, or no longer
   matches the current `prd.md`, `design.md`, and `implement.md` content
   digests. Current HEAD or dirty-path drift alone is not a planning approval
   failure.

2. **Read current task artifacts**:
   - `prd.md` for requirements and acceptance criteria
   - required `design.md` for technical design
   - required `implement.md` for execution order and validation plan

3. **Discover packages and their spec layers**:
   ```bash
   python3 ./.trellis/scripts/get_context.py --mode packages
   ```

4. **Identify which specs apply** to your task based on:
   - Which package you're modifying (e.g., `cli/`, `docs-site/`)
   - What type of work (backend, frontend, unit-test, docs, etc.)
   - Any spec/research paths referenced by the task artifacts

5. **Read the spec index** for each relevant module:
   ```bash
   cat .trellis/spec/<package>/<layer>/index.md
   ```
   Follow the **"Pre-Development Checklist"** section in the index.

6. **Read the specific guideline files** listed in the Pre-Development Checklist that are relevant to your task. The index is NOT the goal — it points you to the actual guideline files (e.g., `error-handling.md`, `conventions.md`, `mock-strategies.md`). Read those files to understand the coding standards and patterns.

7. **Always read shared guides**:
   ```bash
   cat .trellis/spec/guides/index.md
   ```

8. Understand the coding standards and patterns you need to follow, then proceed with your development plan.

This step is **mandatory** before writing any code.
