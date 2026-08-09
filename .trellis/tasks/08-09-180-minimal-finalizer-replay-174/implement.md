# Implementation Plan

## 1. Durable SSOT First

- [ ] Update workflow specs for the 15-Skill/57-exit/33-target graph, `ready_for_merge`, merge route, minimal Finalizer transaction, verification reuse and automatic commit eligibility.
- [ ] Replace the current `Closeout Plan` data contract with versioned owner-private transaction and minimal verification-result contracts; retain explicit legacy compatibility text.
- [ ] Update companion-script boundaries, quality matrix, installer/overlay/public-doc contracts and graph-count assertions.

## 2. Public Graph And Package Contracts

- [ ] Add canonical `trellis/skills/guru-team/packages/guru-merge-task-pr/` with `SKILL.md`, complete contract, Interface 1.3, independent input/output schemas, examples, eval corpus, thin wrappers and tests.
- [ ] Add merge workflow/stop consumer schemas and current production activation data.
- [ ] Migrate `guru-finalize-task` current `published` exit/schema/projection to `ready_for_merge`, preserving legacy assets byte-for-byte and documenting rejection/re-entry behavior.
- [ ] Update registry, workflow invoke/exit markers, route maps and closure validators; keep every exit mapped to one consumer.

## 3. Deterministic Runtime

- [ ] Introduce minimal ignored Finalizer transaction schema and helpers; remove current plan creation, tracked move, archive retention and recovery dependence on `closeout-plan.json`.
- [ ] Refactor preview/execute/recovery to recompute live plan facts, persist only the minimal recovery input after confirmation, and delete terminal/superseded state.
- [ ] Refactor Verifier execution/record/check so completed capability facts survive stdout/result-capture failure, current immutable identity is executed once, and the durable result is minimal.
- [ ] Add repo-bound merge preview/record/check/execute commands using authenticated `gh` and expected head SHA; implement post-merge Issue state and timestamp validation without Issue close mutation.
- [ ] Update `guru-create-task-commit` candidate/check/execute flow to automatically run eligible ordinary commits and preserve exact staging/fail-closed behavior.

## 4. Canonical Distribution And Dogfood

- [ ] Update canonical workflow, schemas, extension manifest, preset asset inventory, ownership expectations and public READMEs.
- [ ] Update only the three Guru-owned Codex/Claude/Cursor finish entries if their thin routing text changes; do not modify official `trellis-*` entries.
- [ ] Run `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json` to synchronize dogfood packages/runtime/workflow assets.
- [ ] Resolve every generated `.new`/`.bak`, then run dogfood drift and installed/source package validation.

## 5. Automated Tests

- [ ] Extend package contract tests for current/legacy version selection, DTO minimality, projection uniqueness, wrapper thinness and three merge exits.
- [ ] Add runtime tests for Finalizer no-closeout-plan lifecycle, recovery, terminal cleanup, verification exactly-once/result-capture recovery and stale identity rerun.
- [ ] Add commit eligibility matrix tests for dedicated unpublished branches and every exclusion.
- [ ] Add merge tests for expected-head success, head drift, Draft, checks/reviews/mergeability blockers, close-keyword mismatch, early/manual close, GitHub closure mismatch and no local sync/Issue close calls.
- [ ] Update finish-family and installer integration tests plus current graph count assertions.

## 6. Controlled Replay And Installation Gates

- [ ] Build a sanitized #174 fixture beginning at the last reviewed content commit; never mutate #174/PR #176.
- [ ] Assert Open-Issue confirmation count 3, new-Issue count 4, commit confirmation 0, Branch Review count 1, immutable verification execution count 1 and terminal transaction artifact count 0.
- [ ] Run clean marketplace init and existing-project workflow preview/switch.
- [ ] Run preset initial apply/reapply, official `trellis update`/version upgrade/reapply, platform equality, ownership inventory, README command and recursive zero-sidecar checks.

## 7. Required Validation Commands

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 -m unittest discover -s trellis/workflows/guru-team/scripts/python -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team -p 'test_*.py'
python3 -m unittest trellis.presets.guru-team.scripts.python.test_apply_guru_team_trellis_preset
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-09-180-minimal-finalizer-replay-174
git diff --check
```

Exact test module invocations may be narrowed during development, but the final gate must include the full source/installed/throwaway/update-reapply surfaces above.

## 8. Risk And Rollback Points

- Public graph activation is atomic: registry, Interface schemas, workflow markers, consumers, production manifest and preset inventory must change together.
- `closeout-plan.json` removal is the highest recovery-risk area; retain legacy fixtures until current Finalizer recovery and #174 replay pass.
- `gh pr merge` tests must use controlled fakes/fixtures except the separately authorized live merge stage; no test may mutate #174/PR #176.
- Any unrelated dirty path, unknown platform edit or `.new`/`.bak` stops staging/activation. Do not overwrite or revert user changes.

## 9. Pre-Start Gate

- [ ] `prd.md`, `design.md` and `implement.md` pass planning wording review.
- [ ] `implement.jsonl` and `check.jsonl` contain only real spec/research inputs.
- [ ] `guru-approve-task-plan` returns `approved` and official task state becomes `in_progress`.
- [ ] No `implementation-handoff.md` is created.
