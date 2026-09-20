# Research: Issue #452 installer and OpenCode boundary

- Query: Inspect the pre-change installer implementation and the approved #452 plan for capability-inventory selection, OpenCode public projection, repeated `--platform`, and focused tests.
- Scope: mixed (current workspace plus locked upstream evidence already recorded in the task research)
- Date: 2026-09-20

> Current-authority note: 本文的实现快照早于 live Issue #452 superseding platform-contract amendment。凡提到三层集合、Guru-supported inventory、Codex/Cursor 默认值、全集安装选项或仅补 OpenCode 的结论均已 superseded；current 结论见 `official-trellis-platforms.md`、task planning 与 `.58` RDT authority。下列代码定位仍可作为 before-state evidence。

## Findings

### Current platform-selection sources

- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:30-41` defines `DEFAULT_PLATFORMS = ("codex", "cursor")`, `PLATFORM_OVERLAY_PREFIXES` for only `codex`, `cursor`, and `claude`, aliases that mapping as `ALL_PLATFORMS`, and enumerates only three finish overlay entry paths. This is the current single installer-side platform inventory; it does not distinguish upstream, Guru-supported, and default-dogfood sets.
- `.../apply_guru_team_trellis_preset.py:59` fixes skill projection order to `shared`, `codex`, `claude`, `cursor`; OpenCode is absent.
- `.../apply_guru_team_trellis_preset.py:775-781` validates manifest overlay `selected_platforms` against `ALL_PLATFORMS`, so adding OpenCode requires the same inventory change to manifest provenance validation.
- The pre-change selection resolver accepted both an explicit platform list and a boolean full-inventory branch. Current authority removes the boolean branch and keeps only repeated explicit values plus the three-platform default.
- The pre-change argparse surface used a mutually exclusive full-inventory flag. Current authority removes that option; unknown values and the removed option remain argparse failures.

### Current OpenCode failure points

- `.../apply_guru_team_trellis_preset.py:2640-2657` requires the canonical overlay tree to equal exactly the three paths in `GURU_OVERLAY_ENTRY_PATHS`. The existing untracked `trellis/presets/guru-team/overlays/.opencode/commands/guru-finish-work.md` therefore makes the current installer fail closed before it can install overlays.
- `.../apply_guru_team_trellis_preset.py:1365-1384` builds platform skill destinations from `SKILL_DESTINATION_PLATFORM_ORDER` and `PLATFORM_OVERLAY_PREFIXES`; no `.opencode/skills` destination can be produced by the current code.
- `.../apply_guru_team_trellis_preset.py:1982-2000` repeats the same destination model for transaction source projections. Without OpenCode here, the managed preimage and staging inventory cannot account for `.opencode` files.
- `.../apply_guru_team_trellis_preset.py:1952-1955` only projects `GURU_OVERLAY_ENTRY_PATHS`, so an OpenCode command is absent from transaction planning even if its canonical source exists.
- `.../apply_guru_team_trellis_preset.py:1156-1243` already provides the reusable public projection rule: it reads `interface.json`, excludes package roots `runtime`, `tests`, and `errors`, excludes non-public scripts, removes private artifacts, and retains declared public schemas/examples/authoring paths. This is the correct existing rule to reuse for `.opencode/skills`; no package-private `tests/` should enter that projection.
- `.../apply_guru_team_trellis_preset.py:2561-2572` passes the selected platform set into package and overlay installation, but the selection is still backed by the old constants. `install_assets` then writes manifest state at `:2596-2619`, so selected-platform and installed-validation behavior must remain internally consistent.

### Tests and expected implementation coverage

- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py:1257-1378` verifies the old no-argument/default projection and explicitly expects only Codex/Cursor. Current authority requires this expectation to change to `claude,codex,cursor`.
- `.../test_apply_guru_team_trellis_preset.py:1465-1500` covers explicit Claude selection; an analogous explicit OpenCode test must assert shared plus `.opencode` skill/command projection and no unrelated platform roots.
- The pre-change installer tests covered a boolean full-inventory selection. Current authority deletes those tests; no-argument assertions become `claude,codex,cursor` and explicit subset tests use repeated `--platform`.
- The pre-change parser tests treated `opencode` as unknown. Current authority uses a genuinely unsupported string for unknown coverage and adds removed-option rejection coverage.
- `.../test_apply_guru_team_trellis_preset.py:2390-2428` hardcodes eval adapter ids and installed adapter files to `shared`, `codex`, `claude`, `cursor`. This is not an installer-only OpenCode projection unless the approved implementation explicitly changes the adapter inventory; it is a likely out-of-slice coupling that must not be changed casually.
- `.../test_apply_guru_team_trellis_preset.py:2550-2632` verifies installed manifest selected platforms and reapply provenance. OpenCode selection and platform-set changes need equivalent manifest/reapply assertions if the existing transaction contract is preserved.
- Transaction fixtures that previously used a full-inventory shorthand must now pass the exact repeated platform selection needed by the scenario.
- `.../test_preset_transaction_installer.py:100-184` exercises managed transaction inventory and source projections; it will catch missing `.opencode` staging paths once the fixture selects OpenCode.
- `.../test_preset_transaction_installer.py:250-330` proves package-private tests remain source-only for installed packages and stale reapply removal. The analogous public projection assertion should use the existing `skill_platform_public_files` rule and assert no `.opencode/**/tests/**` output.

### Official Trellis AI_TOOLS source

- The task-local upstream evidence at `.trellis/tasks/09-20-452-all-platform-support/research/official-trellis-platforms.md` records the locked source as `castbox/Trellis`, `upstream/main`, commit `43fffc170927c85d9f7fc106cc5a059e80d4530b`, CLI `0.6.17`, file `packages/cli/src/types/ai-tools.ts`.
- That registry is the likely official source for the upstream capability layer. It records 22 ids, including `opencode`, and for OpenCode records template dirs `common` and `opencode`, config dir `.opencode`, CLI flag `opencode`, `defaultChecked: false`, `agentCapable: true`, and `hasHooks: false`.
- The same task research records upstream native public roots `.opencode/skills/`, `.opencode/commands/`, `.opencode/agents/`, and `.opencode/plugins/`; the Guru installer slice only has evidence for skills/commands and must not infer support for the other roots without an approved consumer.

## Caveats / Not Found

- The current working tree contains an untracked `.opencode` overlay path (`trellis/presets/guru-team/overlays/.opencode/commands/guru-finish-work.md`) outside the three user-authorized implementation files. It was pre-existing at inspection time and was not modified, staged, removed, or tested.
- The original read-only research slice was narrower than the later accepted task scope. Current planning owns the complete registry, manifest, ownership, compatibility, throwaway, README, spec and test consumer set; this research note does not narrow it.
- Current tests still include package-private integration tests under the installed `.trellis/guru-team/skills/tests` domain by design; the OpenCode requirement concerns the public platform projection, which should use `skill_platform_public_files` and not the installed runtime inventory rule.
- No tests were run because this agent is constrained to read-only research and may write only under the task `research/` directory. No code, branch, worktree, task, or external state was changed.
