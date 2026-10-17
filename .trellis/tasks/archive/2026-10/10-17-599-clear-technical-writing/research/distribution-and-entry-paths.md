# Research: Issue 599 distribution and load paths

- Query: Locate canonical managed-spec distribution, all platform entries, Agent loading and language constraints for Issue #599.
- Scope: internal
- Date: 2026-10-17

## Findings

### Canonical body and installation

No clear-writing rule exists in the inspected baseline. The existing canonical directory is `trellis/presets/guru-team/spec/workflow/`, not `managed-spec/`. Recommended new body: `trellis/presets/guru-team/spec/workflow/clear-technical-writing.md`; install to `.trellis/spec/workflow/clear-technical-writing.md` by extending the explicit `MANAGED_SPEC_PATHS` tuple in `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:148`. This is a recommendation, not an already installed path.

`copy_managed_spec()` at `apply_guru_team_trellis_preset.py:1700` installs absent files, accepts identical bytes, upgrades previous-known managed bytes, and preserves unknown edits with `.new`. Installation collects conflicts and sidecars at lines 2562-2615. The matching extension manifest and managed assets are derived from this tuple; use the existing manifest generation, not a parallel registration mechanism.

The preset owns one bounded root AGENTS block (`AGENTS_AI_FIRST_BLOCK`, line 351). `ensure_agents_ai_first_principles()` at line 1521 preserves every byte outside stable markers, replaces a well-formed older block, and is idempotent. `.trellis/spec/preset/installer.md:125` explicitly excludes root `AGENTS.md` from whole-file ownership. This is an existing supported additive distribution point for a short loading instruction. Do not whole-file replace AGENTS or add upstream-agent ownership.

### Entry inventory

`platform_projection_contract.py:55` is the exact 22-platform descriptor inventory. Each path below has a canonical counterpart under `trellis/presets/guru-team/overlays/`; active public Guru skill packages additionally project from `trellis/skills/guru-team/packages/<id>/` to `.agents/skills/<id>/` and selected platform skill roots. Do not infer platform support from dogfood's selected three platforms.

| Platform id | Skill root | Guru entry installed path | Kind |
| --- | --- | --- | --- |
| claude-code | .claude/skills | .claude/commands/guru/finish-work.md | markdown_command |
| cursor | .cursor/skills | .cursor/commands/guru-finish-work.md | markdown_command |
| opencode | .opencode/skills | .opencode/commands/guru-finish-work.md | markdown_command |
| codex | .codex/skills | .codex/prompts/guru-finish-work.md | markdown_prompt |
| kilo | .kilocode/skills | .kilocode/workflows/guru-finish-work.md | markdown_workflow |
| kiro | .kiro/skills | .kiro/skills/guru-finish-work/SKILL.md | skill_command |
| gemini | .agents/skills | .gemini/commands/guru/finish-work.toml | toml_command |
| antigravity | .agent/skills | .agent/workflows/guru-finish-work.md | markdown_workflow |
| devin | .devin/skills | .devin/workflows/guru-finish-work.md | markdown_workflow |
| qoder | .qoder/skills | .qoder/commands/guru-finish-work.md | markdown_command |
| codebuddy | .codebuddy/skills | .codebuddy/commands/guru/finish-work.md | markdown_command |
| copilot | .github/skills | .github/prompts/guru-finish-work.prompt.md | markdown_prompt |
| droid | .factory/skills | .factory/commands/guru/finish-work.md | markdown_command |
| dsh | .agents/skills | .dsh/skills/guru-finish-work/SKILL.md | skill_command |
| pi | .agents/skills | .pi/prompts/guru-finish-work.md | markdown_prompt |
| reasonix | .reasonix/skills | .reasonix/skills/guru-finish-work/SKILL.md | skill_command |
| zcode | .zcode/skills | .zcode/commands/guru/finish-work.md | markdown_command |
| trae | .trae/skills | .trae/commands/guru-finish-work.md | markdown_command |
| omp | .omp/skills | .omp/commands/guru-finish-work.md | markdown_command |
| grok | .grok/skills | .grok/commands/guru-finish-work.md | markdown_command |
| kimi | .agents/skills | .kimi-code/skills/guru-finish-work/SKILL.md | skill_command |
| snow | .snow/skills | .snow/commands/guru-finish-work.json | json_prompt |

Direct consumers are the Agent reading root instructions/workflow, the main-session finish entry, and the currently loaded semantic skill owner. References must all resolve to the installed body. Add short locators, not copied writing rules. Public docs should point to the canonical body rather than reproduce it.

### Native main-session and child loading

`trellis/workflows/guru-team/workflow.md` is canonical; `.trellis/workflow.md` is the runtime dogfood copy. The workflow continuation begins around line 734 and includes no-Task, current Task, compressed/new-chat recovery and manual Git/GitHub routes. Native hooks are upstream-owned.

Important: `.codex/hooks/session-start.py:482-495` injects a compact Phase Index, not arbitrary text placed at the workflow top. Put a mandatory locator where the existing injected Phase Index/state paths can carry it, plus a root AGENTS short locator and standalone Guru skills/entries where necessary. A top-only workflow paragraph does not prove first output loading.

`.codex/hooks/inject-workflow-state.py:221` reads only current `[workflow-state:STATUS]` blocks. All relevant status blocks need to reach the same common loader, or the injected common Phase Index must establish that obligation.

`.codex/agents/trellis-research.toml:16-31`, `trellis-implement.toml:29-33`, and `trellis-check.toml:49-53` declare native `SubagentStart` injection when available; the fallback reads the exact dispatched Task path and role-specific manifest. Research does not read implement/check JSONL. An independent child must not infer inherited complete rule text. Main owner should pass the installed rule locator and explicit instruction to read the complete file, or include it in the appropriate role's existing manifest for native hook injection, with fallback reading the same locator. Do not modify native hooks/trellis-* agents for this Issue.

`.trellis/agents/{implement,check}.md` are separate upstream-owned channel-runtime agents; changing platform agent prompts would not change channel behavior. Generic independent children also need the explicit load instruction in the dispatch contract.

### Existing language policy and conflicts

`.trellis/spec/docs/public-docs.md:5-20` is current language policy: target business docs default Chinese; extension README/source comments/script help/marketplace metadata can remain English or bilingual. Preserve this division.

`apply_guru_team_trellis_preset.py:339-346` contains two exact known upstream English-only documentation statements and the replacement Chinese default. `normalize_business_doc_language_guidance()` at line 1882 is bounded normalization, not translation. `.trellis/spec/preset/installer.md:441-459` forbids broad rewrite and describes its JSON report. These old English strings are matcher constants, not active instructions to rewrite. Existing tests require them literally.

`guru-review-task-delivery/SKILL.md:36` requires Chinese PR title/body; `guru-create-task-commit/references/contract.md:122` requires Chinese Conventional Commit content; `guru-activate-delivery/references/contract.md:7` reads three Chinese planning docs. These are compatible with #599 and must stay.

No verified current policy requires all writing to be English, forbids all passive voice, or makes a raw sentence-length threshold a gate. Historical `README.pre-434.md` and archives are not current authority. Do not rewrite them solely for expression.

## Related Specs

- `.trellis/spec/preset/{installer,upstream-ownership,overlay-guidelines}.md`: additive ownership, managed hash/reapply and platform boundaries.
- `.trellis/spec/workflow/{workflow-contract,quality-guidelines,skill-package-contract}.md`: semantic ownership, tests and package/DTO boundaries.
- `.trellis/spec/docs/public-docs.md`: Chinese/English policy.
- Official Trellis docs read live: https://docs.trytrellis.app/advanced/custom-workflow.md and https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md. Workflow Markdown defines behavior; existing installations do not update merely because source changed.

## Caveats / Not Found

This research is baseline discovery, not installed-behavior proof. No product file or lifecycle state was changed. All 22 entries are enumerated; only actual selected-platform behavior can be claimed after runtime verification. Root AGENTS automatic loading is platform-dependent: each supported platform needs an explicit workflow/entry loading route, and projection parity must not be labeled actual execution. No historical-wide prose rewrite is warranted.
