# Official Trellis Docs Check

## Sources

- https://docs.trytrellis.app/advanced/custom-workflow
- https://docs.trytrellis.app/advanced/custom-spec-template-marketplace

## Findings

- Official custom workflow docs state that `.trellis/workflow.md` controls Trellis phase definitions, skill routing, per-turn breadcrumbs, and task command catalog. The docs also state workflow edits do not require Python, hook code, or re-releasing Trellis.
- Official spec template marketplace docs state spec templates are for reusable engineering conventions, testing rules, release rules, review checklists, and examples; they must not be used as a remote task store or project-private runtime state.

## Impact For Issue #70

- Branch Review raw report retention belongs in the Guru Team marketplace workflow, platform overlays, and companion recorder/validator scripts.
- No active task state or per-task raw review reports should be placed in a reusable spec template marketplace.
- Scripts may record and validate objective digest/path facts; AI review judgment remains in Markdown workflow / skill / prompt process.
