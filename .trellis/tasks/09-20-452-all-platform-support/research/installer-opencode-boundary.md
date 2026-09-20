# Research: Issue #452 installer and OpenCode boundary

- Query: Inspect the current installer implementation and the approved #452 plan for capability-inventory selection, OpenCode public projection, `--platform opencode`, `--all-platforms`, and focused tests.
- Scope: mixed (current workspace plus locked upstream evidence already recorded in the task research)
- Date: 2026-09-20

## Findings

### Current platform-selection sources

- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:30-41` defines `DEFAULT_PLATFORMS = ("codex", "cursor")`, `PLATFORM_OVERLAY_PREFIXES` for only `codex`, `cursor`, and `claude`, aliases that mapping as `ALL_PLATFORMS`, and enumerates only three finish overlay entry paths. This is the current single installer-side platform inventory; it does not distinguish upstream, Guru-supported, and default-dogfood sets.
- `.../apply_guru_team_trellis_preset.py:59` fixes skill projection order to `shared`, `codex`, `claude`, `cursor`; OpenCode is absent.
- `.../apply_guru_team_trellis_preset.py:775-781` validates manifest overlay `selected_platforms` against `ALL_PLATFORMS`, so adding OpenCode requires the same inventory change to manifest provenance validation.
- `.../apply_guru_team_trellis_preset.py:1524-1529` maps `--all-platforms` to `ALL_PLATFORMS`, explicit `--platform` to its values, and no argument to `DEFAULT_PLATFORMS`. The default Codex/Cursor behavior is therefore already isolated from `ALL_PLATFORMS` by control flow, but the naming and all-platform set are currently conflated.
- `.../apply_guru_team_trellis_preset.py:2790-2800` exposes `--platform` with `choices=ALL_PLATFORMS` and `--all-platforms` as a mutually exclusive flag. Once OpenCode is part of the Guru-supported installer inventory, this is the CLI acceptance point; unknown values remain argparse failures.

### Current OpenCode failure points

- `.../apply_guru_team_trellis_preset.py:2640-2657` requires the canonical overlay tree to equal exactly the three paths in `GURU_OVERLAY_ENTRY_PATHS`. The existing untracked `trellis/presets/guru-team/overlays/.opencode/commands/guru-finish-work.md` therefore makes the current installer fail closed before it can install overlays.
- `.../apply_guru_team_trellis_preset.py:1365-1384` builds platform skill destinations from `SKILL_DESTINATION_PLATFORM_ORDER` and `PLATFORM_OVERLAY_PREFIXES`; no `.opencode/skills` destination can be produced by the current code.
- `.../apply_guru_team_trellis_preset.py:1982-2000` repeats the same destination model for transaction source projections. Without OpenCode here, the managed preimage and staging inventory cannot account for `.opencode` files.
- `.../apply_guru_team_trellis_preset.py:1952-1955` only projects `GURU_OVERLAY_ENTRY_PATHS`, so an OpenCode command is absent from transaction planning even if its canonical source exists.
- `.../apply_guru_team_trellis_preset.py:1156-1243` already provides the reusable public projection rule: it reads `interface.json`, excludes package roots `runtime`, `tests`, and `errors`, excludes non-public scripts, removes private artifacts, and retains declared public schemas/examples/authoring paths. This is the correct existing rule to reuse for `.opencode/skills`; no package-private `tests/` should enter that projection.
- `.../apply_guru_team_trellis_preset.py:2561-2572` passes the selected platform set into package and overlay installation, but the selection is still backed by the old constants. `install_assets` then writes manifest state at `:2596-2619`, so selected-platform and installed-validation behavior must remain internally consistent.

### Tests and expected implementation coverage

- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py:1257-1378` verifies the no-argument/default projection and explicitly expects only Codex/Cursor. This is the compatibility test that must remain unchanged semantically.
- `.../test_apply_guru_team_trellis_preset.py:1465-1500` covers explicit Claude selection; an analogous explicit OpenCode test must assert shared plus `.opencode` skill/command projection and no unrelated platform roots.
- `.../test_apply_guru_team_trellis_preset.py:1505-1545` covers `selected_platforms(..., True)` and all-platform install, currently expecting `claude`, `codex`, `cursor` and three overlay entries. Those assertions need to follow the approved Guru-supported inventory, while no-argument assertions remain Codex/Cursor.
- `.../test_apply_guru_team_trellis_preset.py:2020-2050` tests mutual exclusion and currently treats `opencode` as unknown. Once accepted, the unknown case must use a genuinely unsupported string; the mutual exclusion test remains required.
- `.../test_apply_guru_team_trellis_preset.py:2390-2428` hardcodes eval adapter ids and installed adapter files to `shared`, `codex`, `claude`, `cursor`. This is not an installer-only OpenCode projection unless the approved implementation explicitly changes the adapter inventory; it is a likely out-of-slice coupling that must not be changed casually.
- `.../test_apply_guru_team_trellis_preset.py:2550-2632` verifies installed manifest selected platforms and reapply provenance. OpenCode selection and platform-set changes need equivalent manifest/reapply assertions if the existing transaction contract is preserved.
- `trellis/presets/guru-team/scripts/python/test_preset_transaction_installer.py:20-48` seeds and reapplies all currently known platforms, so adding OpenCode to the supported set requires transaction fixtures to include it if `--all-platforms` is meant to cover it.
- `.../test_preset_transaction_installer.py:100-184` exercises managed transaction inventory and source projections; it will catch missing `.opencode` staging paths once the fixture selects OpenCode.
- `.../test_preset_transaction_installer.py:250-330` proves package-private tests remain source-only for installed packages and stale reapply removal. The analogous public projection assertion should use the existing `skill_platform_public_files` rule and assert no `.opencode/**/tests/**` output.

### Official Trellis AI_TOOLS source

- The task-local upstream evidence at `.trellis/tasks/09-20-452-all-platform-support/research/official-trellis-platforms.md` records the locked source as `castbox/Trellis`, `upstream/main`, commit `43fffc170927c85d9f7fc106cc5a059e80d4530b`, CLI `0.6.17`, file `packages/cli/src/types/ai-tools.ts`.
- That registry is the likely official source for the upstream capability layer. It records 22 ids, including `opencode`, and for OpenCode records template dirs `common` and `opencode`, config dir `.opencode`, CLI flag `opencode`, `defaultChecked: false`, `agentCapable: true`, and `hasHooks: false`.
- The same task research records upstream native public roots `.opencode/skills/`, `.opencode/commands/`, `.opencode/agents/`, and `.opencode/plugins/`; the Guru installer slice only has evidence for skills/commands and must not infer support for the other roots without an approved consumer.

## Caveats / Not Found

- The current working tree contains an untracked `.opencode` overlay path (`trellis/presets/guru-team/overlays/.opencode/commands/guru-finish-work.md`) outside the three user-authorized implementation files. It was pre-existing at inspection time and was not modified, staged, removed, or tested.
- The approved PRD/design/implement documents describe broader registry, manifest, ownership, compatibility, throwaway, README, and spec changes, but the current user authorization narrows this slice to only three Python files. Those broader consumers remain unverified and cannot be repaired in this research-only role.
- Current tests still include package-private integration tests under the installed `.trellis/guru-team/skills/tests` domain by design; the OpenCode requirement concerns the public platform projection, which should use `skill_platform_public_files` and not the installed runtime inventory rule.
- No tests were run because this agent is constrained to read-only research and may write only under the task `research/` directory. No code, branch, worktree, task, or external state was changed.
