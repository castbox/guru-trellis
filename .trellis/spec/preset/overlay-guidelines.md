# Overlay Guidelines

## Canonical Relationship

Overlay files are small platform entrypoints. They should point the AI back to
`.trellis/workflow.md` and the Guru Team companion scripts instead of
duplicating the full workflow.

Reference overlay groups:

- `.agents/skills/trellis-start/SKILL.md`
- `.agents/skills/trellis-continue/SKILL.md`
- `.agents/skills/trellis-finish-work/SKILL.md`
- `.trellis/agents/implement.md`
- `.trellis/agents/check.md`
- `.codex/agents/trellis-implement.toml`
- `.codex/agents/trellis-check.toml`
- `.codex/agents/trellis-research.toml`
- `.cursor/agents/trellis-implement.md`
- `.cursor/agents/trellis-check.md`
- `.cursor/agents/trellis-research.md`
- `.codex/prompts/trellis-start.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.claude/commands/trellis/continue.md`
- `.cursor/commands/trellis-finish-work.md`

## Required Content

All Guru Team overlays should include the marker:

```markdown
<!-- guru-team-overlay: v1 -->
```

Continue entries must:

- run `python3 ./.trellis/scripts/get_context.py`
- run `python3 ./.trellis/scripts/get_context.py --mode phase`
- route by task status
- apply the business-project Chinese documentation default from `.trellis/workflow.md` across `.trellis/spec/**`, `.trellis/tasks/**`, `docs/**`, `00-bootstrap-guidelines` docs SSOT, and human-readable workflow artifact fields
- state that default `sub-agent` mode requires the main session to dispatch
  `trellis-implement` / channel `implement`, then `trellis-check` / channel
  `check`, and later a Branch Review review sub-agent; the main session cannot
  replace those boundaries with its own implementation, check, self-review, or
  script validation output
- write task-local `review.md`, run Branch Review Gate with
  `--review-source independent-agent` and
  `--review-report <task-local review.md>`, then stop before finish-work
- state that any finding priority blocks Branch Review Gate, while
  `observation` and `followup_candidate` are separate non-blocking records
- state that a review agent with findings may only perform closure review and
  must do that same-agent closure review before the passing gate can use a fresh
  `最终放行审查代理`
- state that independent review sub-agents review docs/code/diff evidence as AI
  reviewers and must not run Guru Team recorder/validator extension scripts
  such as `review-branch.sh`, `check-review-gate.sh`, or `record-*`; the main
  session runs those scripts only after review
- state that passing Branch Review Gate requires task-local
  `--agent-assignment`
- state that `wait_agent`, `trellis channel wait`, or equivalent timeout is only
  a wait-window result, not failure or partial-completion evidence; unfinished
  termination must be recorded in `agent-assignment.json.status_events[]` and
  must have same-agent resume or replacement plus later `completed` / `failed`
  before gate pass
- state that main-session self-review cannot pass Branch Review Gate; if
  independent Agent review is unavailable, continue must stop with the gate
  pending
- state that `trellis-continue` must not stage/commit review metadata, push,
  create a PR, call `publish-pr`, or invoke `finish-work`
- avoid adding a separate user-facing publish step

Finish entries must:

- call `.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work`
- explain that the `--from-trellis-finish-work` marker belongs only in explicit
  finish entries and must not be copied into continue entries
- explain that finish-work archives the task, records journal metadata, and
  publishes a non-draft PR
- explain that finish-work may commit Trellis metadata-only changes after the
  reviewed HEAD, but rejects non-metadata changes
- explain that the gate must already contain task-local `review.md`
  `review_report` digest evidence
- state that only `close_issues` may use close keywords

Start entries must:

- identify themselves as fallback/explicit orientation
- support natural-language issue-backed intake when no active task exists
- ask for consent before creating GitHub issues, worktrees, branches, or Trellis
  tasks unless explicitly requested
- treat `handoff.json` as intake provenance only

Sub-agent overlay entries must:

- keep technical dispatch `name` values stable;
- use Chinese UI-facing descriptions and headings;
- for Codex custom agents, keep `nickname_candidates` ASCII so Codex loads the
  agent file, and put the Chinese display role in `description`;
- keep recursion guards and task-context loading preludes intact;
- require implement agents to output a completion handoff with files changed,
  requirement/design carryover, verification state, remaining risks, completion
  status, and focus areas for `trellis-check`;
- require check agents to distinguish Phase 2 check from Branch Review: Phase 2
  may self-fix small in-scope mechanical issues and must output evidence that
  can support `phase2-check.json`; Branch Review is review-only over the full
  committed diff and must report, not patch, missing implementation/check work;
- require unfinished handoff reporting when interrupted/replaced before
  completion, including current diff, remaining work, validation state, and gate
  blockers for same-agent resume or replacement;
- avoid turning agent files into workflow judgment rules.

## Cross-Platform Consistency

When changing one overlay, search all copies:

```bash
find trellis/presets/guru-team/overlays -type f | sort
rg "Branch Review Gate|finding|observation|followup-candidate|最终放行审查代理|finish-work|handoff.json|guru-team-overlay" trellis/presets/guru-team/overlays
```

After canonical overlay edits, re-apply the preset to this source repository and
run the dogfood drift check:

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

The drift check is read-only and only verifies file presence/content equality.
It does not decide whether an overlay change is semantically correct.

Keep platform-specific command names only where needed, such as
`/trellis:finish-work` for Claude and `/trellis-finish-work` for Cursor.

## Anti-Patterns

- Pasting the entire workflow into every overlay.
- Creating platform-only semantics that do not exist in
  `trellis/workflows/guru-team/workflow.md`.
- Omitting the overlay marker, which makes installer conflict detection weaker.
- Mentioning publish as a separate user-facing step.
