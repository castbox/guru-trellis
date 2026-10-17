# Research: Targeted validation and real Codex behavior harness

- Query: Identify useful current tests and an actual platform path for Issue #599 AC5 without synthetic Tasks.
- Scope: mixed
- Date: 2026-10-17

## Findings

### Existing mechanical tests

- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py:682`: existing AGENTS tests cover missing file, preservation of external bytes including CRLF, repeated idempotent apply, and older bounded block replacement. Extend these with the writing locator and full-spec existence/reference.
- Same file, lines 995, 1012, 1035 and 1059: managed-spec unknown collision produces `.new`; known managed upgrade uses `.bak`; user edits survive reapply; identical older manifest gets current managed hash. Reuse the same path tuple mechanism for the new document, and prove the new file specifically participates.
- Same file, lines 771-841: existing language normalization and payload tests. Preserve exact legacy matcher constants; do not broaden normalization into prose translation.
- `test_guru_platform_inventory.py:96-151`: registry-bound native skill roots, current managed projection inventory, descriptor-driven overlays, and selected platform provenance.
- `test_verify_native_platform_load.py:61`: all-platform projection parity test.
- `test_upstream_ownership.py:86-185`: current descriptor claims, exact ownership, and no package-private test leakage.
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`: canonical/dogfood drift after preset apply. `.new`/`.bak` must be individually reviewed and resolved; do not delete evidence indiscriminately.
- `trellis/skills/guru-team/` package registry validators and workflow-marker checks remain relevant if skill references or mandatory workflow loading are changed. Scope tests to actual changes and preserve fixed contract-wording scope/exits.

`verify_native_platform_load.py:246-258` explicitly returns `actual_load=projection_parity` for every non-OpenCode platform, including Codex. Only OpenCode uses a native catalog server. This verifier does not establish text-generation behavior on Codex and cannot alone pass AC5.

### Actual platform options observed

Local executable `/opt/homebrew/bin/codex`; `codex --version` reports `codex-cli 0.162.1`. `codex features list` reports `multi_agent` and `hooks` stable and enabled. Local CLI help documents:

- `codex exec --cd <repo> --sandbox read-only --json --output-last-message <path> -` for actual model execution with stdout JSONL and a final output file.
- `codex exec resume <exact-session-id> --json <prompt>` for a precise resumed session. Capture the session UUID from the initial event; never use `--last` for task-specific evidence.
- `--ephemeral` prevents session persistence and is suitable for isolated one-shot cases, but cannot prove persisted session restoration. Omit it for the scenario that must resume.

No Codex run was executed in this research; flags were read from actual `--help`. Current availability of a CLI/feature does not prove model access or successful child spawn.

The existing `trellis/skills/guru-team/packages/guru-qualify-root-cause/tests/run_native_eval.py:26-55` is an example of real Codex authoring with read-only sandbox, prompt on stdin, captured stdout/stderr, explicit timeout, final response file and no access to host-only expected answers. Its `--ephemeral` semantic package evaluation is not itself the #599 harness. `trellis/skills/guru-team/adapters/eval/{native_adapter.py,codex.sh,codex.json}` are package-eval adapters, not a first-output/resume/child behavior suite.

### AC5 minimum meaningful experiment

Reuse the one representative complete throwaway required by AC6, or an existing matching fully installed environment. Do not create a meaningless Task. Use this Issue's existing exact Task and a separately no-Task session context, with the production binding mechanics only where necessary. An execution directory or inventory listing does not itself establish an exact Task binding.

For each scenario retain actual JSONL or platform trace and the produced text. An AI reviewer must inspect whether the complete installed specification read precedes the first substantive output; a claim “I read it” in the final message is insufficient.

1. No-Task main session: begin through installed entry/root instructions, give a normal writing task, observe any brief loading progress, full-body read and meaningful compliant output.
2. Bound-Task main session: deliberately use the real existing #599 Task identity through its documented binding/current-context path; repeat first meaningful output. Do not manufacture a Task merely for testing.
3. Restore the captured exact session: re-enter actual native resume, establish current rule loading availability, then produce output. Clarify whether the same context remains or a fresh read is required; do not label a second plain prompt “resume.”
4. Independent child: actually spawn the selected native child with exact scope/Task path and the installed rule locator; child must read the complete body through its own tools or verified full native injection. Do not provide the complete body in the parent prompt and call inheritance independent loading. Preserve role-isolated manifests.
5. Ordinary missing-rule install/environment case: a concise missing-path diagnostic only, then pause dependent text. Restore the spec through the supported install/reapply path or a dedicated fixture setup and continue the same normal request; successful reread continues without new approval. This is a legitimate missing dependency scenario, not an artifact-tamper defense test.

Keep prompts factual and avoid instructing the model to output an expected PASS, fabricate a read, or short-circuit the normal loader. Mechanical event ordering can verify reads/distribution; language/meaning preservation remains AI judgment. Cover actual output examples with conditions, negation, exception, execution order, requirement/recommendation strength, unverified limitations, exact public names and redacted excerpts.

### Evidence reporting

Report separately: source references and rule mapping; installed projection/reapply and user-byte preservation; actual Codex behavior. A code test is not runtime evidence, and the representative platform cannot prove other platforms' actual behavior. Full multi-platform release/upgrade matrices remain deferred to their dedicated owner.

## Caveats / Not Found

No existing dedicated clear-writing AC5 harness was found. Actual model access, hook trust, exact child tool availability and session binding must be verified by the implementation/coordinator in the installed environment. Do not expose credentials, inherited secret config or raw unrelated session records when capturing CLI logs. Do not change upstream hooks/agents to force the test to pass.
