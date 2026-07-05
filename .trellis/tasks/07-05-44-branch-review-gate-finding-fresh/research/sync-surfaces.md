# Research: Branch Review Gate finding/P3/fresh final reviewer sync surfaces

- Query: List all workflow, overlay, dogfood, spec, and docs files that need synchronization for Branch Review Gate finding/P3/fresh final reviewer semantics. Searched terms: `P3`, `P0/P1/P2`, `finding`, `observation`, `followup_candidate`, `Branch Review Gate`, `最终放行审查代理`, `问题闭环审查代理`, `review-branch`.
- Scope: mixed
- Date: 2026-07-05

## Findings

### Executive summary

The sync surface is broad. The canonical contract is `trellis/workflows/guru-team/workflow.md`; this repo dogfoods it in `.trellis/workflow.md`. The same Branch Review Gate wording is then repeated in canonical preset overlays under `trellis/presets/guru-team/overlays/` and dogfood installed copies under `.agents/`, `.codex/`, `.claude/`, `.cursor/`, and `.trellis/agents/`. Project specs and durable docs also describe the same evidence chain. If issue #44 changes only AI judgment wording, edit Markdown workflow/overlays/spec/docs. If it changes machine behavior for P3, observation/followup candidates, or final reviewer freshness, also update companion script config/code/tests.

Official Trellis docs support this split:

- `https://docs.trytrellis.app/advanced/custom-workflow.md`: `workflow.md` defines phase definitions, skill routing, per-turn reminders, and command catalog; workflow changes do not require Python/hook code by default.
- `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`: spec templates are for reusable engineering conventions/review checklists, not active tasks, platform prompt files, or project-private runtime state.

### Files found

#### Canonical workflow and dogfood workflow

| File | Description | Suggested change summary |
| --- | --- | --- |
| `trellis/workflows/guru-team/workflow.md` | Canonical marketplace workflow contract. | Primary edit point. Align Branch Review Gate finding taxonomy, P3 non-blocking behavior, `observation` / `followup_candidate` if required, and fresh `最终放行审查代理` role/reuse rules. |
| `.trellis/workflow.md` | Dogfood active workflow parsed by local Trellis context injection. | Keep byte/semantic sync with canonical workflow after canonical edit. |

Evidence:

- `trellis/workflows/guru-team/workflow.md:647` starts Phase 3.5 Branch Review Gate.
- `trellis/workflows/guru-team/workflow.md:651` defines post-commit Phase 2 audit and permits only task-local `agent-assignment.json` as post-commit review metadata.
- `trellis/workflows/guru-team/workflow.md:655` says independent reviewer/check Agent review is required and main-session self-review cannot pass.
- `trellis/workflows/guru-team/workflow.md:668` assigns first issue-finding review to `问题发现审查代理`.
- `trellis/workflows/guru-team/workflow.md:669` assigns fix verification to `问题闭环审查代理`.
- `trellis/workflows/guru-team/workflow.md:670` assigns pass/final release review to `最终放行审查代理`.
- `trellis/workflows/guru-team/workflow.md:672` requires `review_rounds[]` to record findings count, reuse policy, and reuse decision.
- `trellis/workflows/guru-team/workflow.md:691` defines findings as `P0`, `P1`, `P2`, `P3`.
- `trellis/workflows/guru-team/workflow.md:693` says `P0/P1/P2` block `finish-work`.
- `trellis/workflows/guru-team/workflow.md:694` says `P3` is recorded but non-blocking.
- `.trellis/workflow.md:647`, `.trellis/workflow.md:651`, `.trellis/workflow.md:668`, `.trellis/workflow.md:691`, `.trellis/workflow.md:693`, and `.trellis/workflow.md:694` mirror the same installed workflow semantics.

#### Canonical continue overlays

| File | Description | Suggested change summary |
| --- | --- | --- |
| `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md` | Shared skill-layer continue entry. | Sync concise Branch Review Gate instructions: P3 record/non-block, P0/P1/P2 block, role freshness/reuse policy, `review-branch` recorder boundary. |
| `trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md` | Codex skill continue entry. | Same as shared skill; keep Codex skill copy aligned. |
| `trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md` | Codex prompt command for continue. | Same wording, using `/trellis:finish-work` platform spelling. |
| `trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md` | Claude continue command. | Same wording, using `/trellis:continue` and `/trellis:finish-work`. Also currently lacks the detailed post-commit dirty-path sentence that Codex/Cursor have. |
| `trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md` | Cursor continue command. | Same wording, using `/trellis-continue` and `/trellis-finish-work`. |

Evidence:

- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md:21` says after commit the AI must obtain independent Agent review, record role/reuse decisions, write task-local `review.md`, and record Branch Review Gate.
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md:33` says P0/P1/P2 block finish-work and P3 can be recorded without blocking.
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md:35` lists `问题闭环审查代理` and `最终放行审查代理` as logical roles.
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md:27` uses the P0/P1/P2/P3 wording in Codex prompt form.
- `trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md:27` uses the same P0/P1/P2/P3 wording in Claude command form.
- `trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md:27` uses the same P0/P1/P2/P3 wording in Cursor command form.

#### Dogfood installed continue overlays

| File | Description | Suggested change summary |
| --- | --- | --- |
| `.agents/skills/trellis-continue/SKILL.md` | Dogfood shared skill continue entry. | Sync from canonical overlay after edit. |
| `.codex/skills/trellis-continue/SKILL.md` | Dogfood Codex skill continue entry. | Sync from canonical overlay after edit. |
| `.codex/prompts/trellis-continue.md` | Dogfood Codex prompt continue entry. | Sync from canonical overlay after edit. |
| `.claude/commands/trellis/continue.md` | Dogfood Claude continue command. | Sync from canonical overlay after edit. |
| `.cursor/commands/trellis-continue.md` | Dogfood Cursor continue command. | Sync from canonical overlay after edit. |

Evidence:

- `.agents/skills/trellis-continue/SKILL.md:21`, `.codex/skills/trellis-continue/SKILL.md:21`, `.codex/prompts/trellis-continue.md:15`, `.claude/commands/trellis/continue.md:15`, and `.cursor/commands/trellis-continue.md:15` all describe the after-commit independent review and Branch Review Gate step.
- `.agents/skills/trellis-continue/SKILL.md:33`, `.codex/skills/trellis-continue/SKILL.md:33`, `.codex/prompts/trellis-continue.md:27`, `.claude/commands/trellis/continue.md:27`, and `.cursor/commands/trellis-continue.md:27` all contain finding/P3 gate wording.
- `.agents/skills/trellis-continue/SKILL.md:35`, `.codex/skills/trellis-continue/SKILL.md:35`, `.codex/prompts/trellis-continue.md:29`, `.claude/commands/trellis/continue.md:29`, and `.cursor/commands/trellis-continue.md:29` all contain Chinese logical roles.

#### Finish-work overlays

| File | Description | Suggested change summary |
| --- | --- | --- |
| `trellis/presets/guru-team/overlays/.agents/skills/trellis-finish-work/SKILL.md` | Shared finish entry. | If issue #44 changes what counts as a valid final gate, mention that finish requires a passed gate with fresh final reviewer evidence and accepted P3/followup semantics. |
| `trellis/presets/guru-team/overlays/.codex/skills/trellis-finish-work/SKILL.md` | Codex finish skill. | Same as shared finish skill. |
| `trellis/presets/guru-team/overlays/.codex/prompts/trellis-finish-work.md` | Codex finish prompt. | Same, platform prompt copy. |
| `trellis/presets/guru-team/overlays/.claude/commands/trellis/finish-work.md` | Claude finish command. | Same, Claude command wording. |
| `trellis/presets/guru-team/overlays/.cursor/commands/trellis-finish-work.md` | Cursor finish command. | Same, Cursor command wording. |
| `.agents/skills/trellis-finish-work/SKILL.md` | Dogfood shared finish entry. | Sync from canonical overlay after edit. |
| `.codex/skills/trellis-finish-work/SKILL.md` | Dogfood Codex finish skill. | Sync from canonical overlay after edit. |
| `.codex/prompts/trellis-finish-work.md` | Dogfood Codex finish prompt. | Sync from canonical overlay after edit. |
| `.claude/commands/trellis/finish-work.md` | Dogfood Claude finish command. | Sync from canonical overlay after edit. |
| `.cursor/commands/trellis-finish-work.md` | Dogfood Cursor finish command. | Sync from canonical overlay after edit. |

Evidence:

- `trellis/presets/guru-team/overlays/.agents/skills/trellis-finish-work/SKILL.md:30` says finish helper verifies the passed Branch Review Gate and that the gate must record task-local `review.md` digest and optional `agent-assignment.json` evidence.
- `.agents/skills/trellis-finish-work/SKILL.md:30`, `.codex/skills/trellis-finish-work/SKILL.md:30`, `.codex/prompts/trellis-finish-work.md:24`, `.claude/commands/trellis/finish-work.md:24`, and `.cursor/commands/trellis-finish-work.md:24` mirror that finish boundary.

#### Check-agent overlays

| File | Description | Suggested change summary |
| --- | --- | --- |
| `trellis/presets/guru-team/overlays/.trellis/agents/check.md` | Channel-runtime check agent definition. | If final reviewer or P3 semantics affect check/review reporting, update report instructions to distinguish blocking findings, P3 observations, and follow-up candidates. |
| `trellis/presets/guru-team/overlays/.claude/agents/trellis-check.md` | Claude check sub-agent. | Same reporting taxonomy; keep Chinese logical role wording. |
| `trellis/presets/guru-team/overlays/.cursor/agents/trellis-check.md` | Cursor check sub-agent. | Same reporting taxonomy; keep Chinese logical role wording. |
| `trellis/presets/guru-team/overlays/.codex/agents/trellis-check.toml` | Codex check custom agent. | Add explicit P0/P1/P2/P3 / observation / followup_candidate reporting guidance if Codex review output should use it. |
| `.trellis/agents/check.md` | Dogfood channel-runtime check agent. | Sync from canonical overlay. |
| `.claude/agents/trellis-check.md` | Dogfood Claude check agent. | Sync from canonical overlay. |
| `.cursor/agents/trellis-check.md` | Dogfood Cursor check agent. | Sync from canonical overlay. |
| `.codex/agents/trellis-check.toml` | Dogfood Codex check agent. | Sync from canonical overlay. |

Evidence:

- `trellis/presets/guru-team/overlays/.trellis/agents/check.md:13` lists UI-facing roles including `问题闭环审查代理` and `最终放行审查代理`.
- `trellis/presets/guru-team/overlays/.trellis/agents/check.md:32` asks for concrete findings.
- `trellis/presets/guru-team/overlays/.claude/agents/trellis-check.md:10` lists UI-facing roles including `问题闭环审查代理` and `最终放行审查代理`.
- `trellis/presets/guru-team/overlays/.cursor/agents/trellis-check.md:10` has the same role list.
- `trellis/presets/guru-team/overlays/.codex/agents/trellis-check.toml:52` says to prefer concrete findings over speculative warnings.
- Dogfood copies mirror these at `.trellis/agents/check.md:13`, `.claude/agents/trellis-check.md:10`, `.cursor/agents/trellis-check.md:10`, and `.codex/agents/trellis-check.toml:52`.

#### Specs

| File | Description | Suggested change summary |
| --- | --- | --- |
| `.trellis/spec/workflow/workflow-contract.md` | Main workflow behavior spec. | Sync the authoritative Branch Review Gate contract: P3 vs P0/P1/P2, final reviewer freshness/reuse, `review.md`, `review-gate.json`, and `agent-assignment.json`. |
| `.trellis/spec/workflow/data-contracts.md` | Artifact schema/data contract spec. | Add or adjust fields if `observation` / `followup_candidate` become first-class artifact semantics. Sync `findings`, `review_rounds[]`, and agent assignment contract. |
| `.trellis/spec/workflow/companion-scripts.md` | Companion script boundary spec. | Sync recorder/validator responsibilities if `review-branch` accepts or validates new finding categories/final reviewer freshness. |
| `.trellis/spec/workflow/quality-guidelines.md` | Verification/review quality spec. | Sync review focus checklist and search commands with new terms. |
| `.trellis/spec/preset/overlay-guidelines.md` | Overlay sync rules. | Add the new Branch Review Gate wording requirements to continue/finish/check overlays so future platform copies stay aligned. |
| `.trellis/spec/docs/public-docs.md` | Public docs SSOT rules. | Use as docs update checklist if README/workflow README/preset README wording changes. |
| `.trellis/spec/workflow/index.md` | Workflow spec index. | Usually no semantic edit needed, but include if pre-development checklist or reference set changes. |

Evidence:

- `.trellis/spec/workflow/workflow-contract.md:84` defines Branch Review Gate as post-commit independent Agent review over complete branch diff.
- `.trellis/spec/workflow/workflow-contract.md:86` says no P0/P1/P2 findings before passing.
- `.trellis/spec/workflow/workflow-contract.md:114` says `review-branch.sh` verifies Phase 2 check evidence before writing `review-gate.json`.
- `.trellis/spec/workflow/workflow-contract.md:120` through `.trellis/spec/workflow/workflow-contract.md:123` describe post-commit `agent-assignment.json` update and digest.
- `.trellis/spec/workflow/workflow-contract.md:143` through `.trellis/spec/workflow/workflow-contract.md:160` list passing gate requirements and no P0/P1/P2 findings.
- `.trellis/spec/workflow/data-contracts.md:123` records findings/resolution status in Phase 2 check.
- `.trellis/spec/workflow/data-contracts.md:125` says P0/P1/P2 findings block commit until resolved.
- `.trellis/spec/workflow/data-contracts.md:147` through `.trellis/spec/workflow/data-contracts.md:159` define review rounds and logical roles including `问题闭环审查代理` and `最终放行审查代理`.
- `.trellis/spec/workflow/data-contracts.md:167` through `.trellis/spec/workflow/data-contracts.md:171` state why final reviewer assignment can update after commit and must be digested by `review-branch.sh`.
- `.trellis/spec/workflow/companion-scripts.md:120` through `.trellis/spec/workflow/companion-scripts.md:124` require `review-branch.sh --pass` to fail on unresolved P0/P1/P2 and require independent-agent evidence.
- `.trellis/spec/workflow/companion-scripts.md:138` through `.trellis/spec/workflow/companion-scripts.md:143` describe `--agent-assignment` digest behavior.
- `.trellis/spec/workflow/quality-guidelines.md:61` through `.trellis/spec/workflow/quality-guidelines.md:64` require independent Agent review before Branch Review Gate.
- `.trellis/spec/preset/overlay-guidelines.md:41` through `.trellis/spec/preset/overlay-guidelines.md:46` define required continue-overlay Branch Review Gate content.
- `.trellis/spec/preset/overlay-guidelines.md:85` through `.trellis/spec/preset/overlay-guidelines.md:88` provides overlay search commands that should include new terms if introduced.
- `.trellis/spec/docs/public-docs.md` says behavior changes must update `README.md`, `trellis/workflows/guru-team/README.md`, and `trellis/presets/guru-team/README.md`.

#### Docs

| File | Description | Suggested change summary |
| --- | --- | --- |
| `README.md` | Top-level install/daily operation docs. | Sync user-facing explanation for independent review, P3/finding behavior, and final reviewer freshness if changed. |
| `trellis/workflows/guru-team/README.md` | Marketplace workflow behavior docs. | Sync detailed workflow behavior and helper usage examples. |
| `trellis/presets/guru-team/README.md` | Preset installer and installed file docs. | Sync installed overlay behavior and dogfood drift expectations. |
| `docs/requirements/README.md` | Requirements navigation matrix. | Add/update requirement row if issue #44 adds new P3/fresh-reviewer requirement category. |
| `docs/requirements/requirement-main.md` | Durable requirement SSOT. | Main docs source for issue lineage and gate contracts; add issue #44 semantics here. |

Evidence:

- `README.md:302` through `README.md:307` explains that `review-branch.sh` records prior AI/human review, task-local `review.md` must come from independent Agent review, and no P0/P1/P2 finding is required.
- `docs/requirements/README.md:31` identifies Planning/check/Branch Review Gate evidence chain as P0 requirement category.
- `docs/requirements/README.md:58` maps AI review prompt and Branch Review Gate to issues/PRs.
- `docs/requirements/requirement-main.md:78` starts the Branch Review Gate evidence-chain requirement section.
- `docs/requirements/requirement-main.md:95` through `docs/requirements/requirement-main.md:101` define Phase 2 check findings, AI review prompt, `review-branch.sh`, independent review source, assignment ledger, and post-commit audit.
- `trellis/workflows/guru-team/README.md:194` through `trellis/workflows/guru-team/README.md:205` explain independent Agent review, no P0/P1/P2 findings, `review-branch.sh` recorder boundary, and Phase 2 evidence validation.
- `trellis/workflows/guru-team/README.md:221` through `trellis/workflows/guru-team/README.md:224` says PR body Review Gate section must include findings state.
- `trellis/presets/guru-team/README.md:231` through `trellis/presets/guru-team/README.md:238` explains post-commit audit and passing gate requirements.

#### Config and enforcement surfaces to inspect if semantics become machine-enforced

These are not Markdown workflow/docs surfaces, but they are the places that currently enforce P0/P1/P2/P3 and role/reuse data.

| File | Description | Suggested change summary |
| --- | --- | --- |
| `trellis/workflows/guru-team/config-template.yml` | Canonical Guru Team config defaults. | If P3 or new categories become configurable, update `review_gate.block_priorities` or add new keys. |
| `.trellis/guru-team/config-template.yml` | Dogfood installed config template. | Sync from canonical config template. |
| `.trellis/guru-team/config.yml` | Dogfood active config. | Sync only if active dogfood behavior should change. |
| `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` | Canonical companion script implementation. | Update only if issue #44 changes objective validation: priority enum, blocking rules, review-round/freshness validation, artifact payload schema, or CLI args. |
| `.trellis/guru-team/scripts/python/guru_team_trellis.py` | Dogfood installed companion script. | Sync from canonical script through preset apply, not hand-edit as sole source. |
| `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` | Canonical unit tests for companion behavior. | Add/adjust tests for P3 non-blocking, observation/followup candidate payloads, and fresh final reviewer validation if machine-enforced. |
| `trellis/workflows/guru-team/scripts/bash/review-branch.sh` | Thin canonical wrapper for `review-branch`. | Usually no edit unless command name/path changes. |
| `.trellis/guru-team/scripts/bash/review-branch.sh` | Dogfood installed wrapper. | Sync through preset apply if canonical wrapper changes. |
| `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` | Preset installer asset list / dogfood sync source. | Update only if new overlay/script/config files are added or managed file list changes. |
| `trellis/guru-team-extension.json` and `.trellis/guru-team/extension.json` | Extension manifests listing installed commands/assets. | Update only if command/assets list or descriptions change; current match is command inventory only. |
| `trellis/index.json` | Marketplace workflow index entry. | Usually no edit unless public description/tags need to mention new gate semantics. |

Evidence:

- `trellis/workflows/guru-team/config-template.yml:62` through `trellis/workflows/guru-team/config-template.yml:70` define `review_gate.artifact_path`, `block_priorities: P0/P1/P2`, `require_head_match`, and deployment evidence.
- `.trellis/guru-team/config.yml:51` through `.trellis/guru-team/config.yml:59` mirrors active dogfood review gate config.
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:56` defines `VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}`.
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:57` defines `BLOCKING_PRIORITIES = {"P0", "P1", "P2"}`.
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:84` through `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:87` include `问题闭环审查代理` and `最终放行审查代理`.
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:89` defines allowed reuse decisions.
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:1509` through `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:1542` parse and validate findings.
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:1695` through `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:1724` append review rounds with findings count and reuse fields.
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:2015` through `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:2027` compute blocking/unresolved findings.
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:3015` through `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:3109` enforce Branch Review Gate recorder preconditions.
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:765` through `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:783` test unresolved blocking finding behavior.
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:1739` through `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:1748` test final reviewer review round fields.
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:2151` through `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:2166` test problem-finding review round reuse/finding count.
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:51` through `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:54` list managed review scripts.
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:259` through `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:261` says Codex defaults to sub-agent mode so independent Branch Review Gate can be satisfied by default.

### Recommended sync order

1. Update `trellis/workflows/guru-team/workflow.md` first; this is the canonical workflow source.
2. Mirror to `.trellis/workflow.md` for dogfood active workflow.
3. Update canonical overlays under `trellis/presets/guru-team/overlays/`:
   continue entries first, finish entries second, check-agent entries if output taxonomy changes.
4. Apply preset to dogfood copies rather than treating dogfood as the only source:
   `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
5. Run dogfood drift check:
   `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
6. Update specs:
   `.trellis/spec/workflow/workflow-contract.md`,
   `.trellis/spec/workflow/data-contracts.md`,
   `.trellis/spec/workflow/companion-scripts.md`,
   `.trellis/spec/workflow/quality-guidelines.md`,
   `.trellis/spec/preset/overlay-guidelines.md`.
7. Update durable docs:
   `docs/requirements/requirement-main.md`,
   `docs/requirements/README.md`,
   `README.md`,
   `trellis/workflows/guru-team/README.md`,
   `trellis/presets/guru-team/README.md`.
8. Only if machine-enforced behavior changes, update `guru_team_trellis.py`, config templates, installed dogfood script, and tests.

### Suggested semantic decisions before implementation

- Define whether `P3` remains a normal `finding` with non-blocking priority, or becomes a separate `observation`.
- Define whether `followup_candidate` is a new structured finding kind, a finding status, or only review-report prose.
- Define what "fresh final reviewer" means:
  - same technical agent as `问题发现审查代理` is never allowed for `最终放行审查代理`;
  - same technical agent may be reused only with explicit `reuse_policy` / `reuse_decision`;
  - or freshness means a new review round at current HEAD, independent of whether the same agent id is reused.
- Define whether the above must be AI-judged only in Markdown, or machine-validated by `review-branch.sh`.

## Caveats / Not Found

- `python3 ./.trellis/scripts/task.py current --source` reported no active task, but the user supplied the exact task path and requested this research file. The research directory was therefore created at `.trellis/tasks/07-05-44-branch-review-gate-finding-fresh/research/`.
- No live non-archived matches were found for `observation` or `followup_candidate` in workflow, overlay, dogfood, spec, docs, or companion script surfaces. If issue #44 requires those terms, this is new contract work rather than simple wording synchronization.
- Archived task artifacts contain many historical matches for P0/P1/P2/P3 and Branch Review Gate, but they are evidence history and should not be treated as sync targets.
- This was a read-only/source-code research pass. No workflow, overlay, spec, docs, script, config, or test files were modified.
