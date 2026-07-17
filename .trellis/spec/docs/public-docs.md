# Public Documentation

## Audience and Language

Top-level user-facing docs in this repository are primarily Chinese because
the install/upgrade prompts are intended for Guru Team users. Keep command
names, config keys, file paths, GitHub keywords, and Trellis template ids in
English.

Lower-level script comments and Python docstrings may stay English when they
document implementation mechanics.

When public docs describe behavior inside target business repositories, state
the Guru Team default explicitly: `.trellis/spec/**`, `.trellis/tasks/**`,
`docs/**` durable docs, docs SSOT created or completed by
`00-bootstrap-guidelines`, and workflow artifact human-readable fields should be
Chinese. Literal commands, paths, config keys, GitHub keywords, marketplace ids,
and code symbols may remain English. `guru-trellis` itself is a public extension
repository, so public README/source comments/script help/marketplace metadata
may remain English or bilingual when that is clearer.

## Install and Upgrade Prompts

README install docs must provide both:

- a non-interactive command-line installation path for copy/paste or automated
  verification;
- an AI prompt path for users who want Codex, Cursor, or another AI tool to run
  the install, validation, commit, and publish workflow.

Default install commands must not enter the interactive spec template picker.
Use `trellis init -y ... --workflow guru-team --workflow-source ...`, or an
officially supported explicit `--template <name>` path when a specific template
is intended. If docs mention interactive template selection, describe it as an
opt-in user choice, not as the team default or automated validation path.

Prompts in `README.md` are meant to be copied into an AI coding session in a
target business repository. They should tell the AI to:

- confirm the current `@mindfoldhq/trellis` latest version live, while clearly
  distinguishing it from the pinned official Trellis target used by the current
  Guru Team stable release
- detect conflicting SDD or agent harness frameworks before installing
- use the `guru-team` marketplace workflow source
- apply the preset installer from this public repository
- detect `00-bootstrap-guidelines` after init and explain that spec bootstrap
  is a one-time repo-level task that needs explicit user confirmation before
  AI modifies `.trellis/spec/`
- explain that bootstrap-created `.trellis/spec/**` and docs SSOT content in
  target business repos should use Chinese human-readable prose by default
- keep only selected platform entry directories
- run minimal validation, including `check-env --json`; if `github_repo` cannot
  be inferred, the docs or prompt must tell the user to configure
  `.trellis/guru-team/config.yml` or a GitHub `origin` remote before treating
  GitHub issue intake / publish as ready
- check for secrets before commit
- do Git publishing preflight before pushing or opening a PR

Do not write prompts that assume direct push to protected branches.

Do not write prompts that silently complete spec bootstrap as an install or
upgrade side effect. Installation docs should tell the AI to report the
bootstrap task, explain the intended `.trellis/spec/` changes, and ask whether
to complete it now or leave it for a separate follow-up.

## SSOT Rules

Public docs must identify `trellis/skills/guru-team/` as the only canonical
workflow skill root and distinguish registry lifecycle (`reserved` versus
`active`), package/interface ownership, workflow marker ownership, generated
platform copies, and deterministic script limits. They must state that the
workflow marketplace installs only `.trellis/workflow.md`, while the preset is
the complete Guru Team extension configurator.

Skill ids, external exit ids, registry/interface/schema ids, stable script
commands, and lifecycle states are public APIs. Breaking changes require a new
id or an explicit migration. Upgrade instructions must require workflow and
preset reapply after `trellis update`, resolution of `.new`/`.bak`, and source,
installed, and drift validation before claiming success.

All three public README files must use the same Skill mode/runtime wording:
`workflow` means mandatory global workflow routing, while `standalone` means
direct platform discovery without that routing. Both modes require a complete,
compatible Guru Team preset and shared extension runtime; a Skill directory is
not a self-contained or portable package. The docs must name
`run-skill-command` as the shared dispatcher, describe fail-closed full-preset
install/upgrade remediation, and list its installed executable path.

Public docs that describe task work commits must name
`guru-create-task-commit` as the active closed-loop owner, retain
`guru-create-work-commit` only as a reserved tombstone, distinguish AI review
from deterministic candidate/executor checks, and document fresh-sequence
re-entry after finding fixes. Platform entry docs should reference the stable
skill and typed exits instead of repeating its step-local contract.

Public docs that describe Phase 0 must name `guru-sync-base` as the active
selected-base closed-loop owner, list stable exits `synced` / `skipped` /
`blocked`, and state that the package uses the deterministic schema 1.2 profile
without selected-base or post-execution AI review gates. They must state the
four-level order: explicit, scalar config, first existing ordered candidate
(default `dev`, `develop`, `main`, `master`), then remote default; prohibit
current-branch implicit fallback; require decision/local/remote HEAD equality;
and explain that resolution/result facts stay on stdout, the executor emits a
post-sync resolution digest, the validator passes only that digest forward,
and each `prepare-task` guard consumes the previous post-sync digest and returns
the next one before reads or mutation boundaries. They must not describe
evidence files, leases, release, or cleanup APIs. All three
README files must list the active id, result schema,
runtime commands, full-preset requirement, update/reapply steps, and
missing/drift/sidecar remediation without duplicating the complete Skill loop.

Public Phase 0 docs must also name active semantic
`guru-discover-change-context` as the only `guru-sync-base:synced` consumer.
They state the fixed current-state-before-history order, workflow/standalone
freshness parity, archived `finish-summary.json:index.*`-only reader,
`guru-context-history-score-1.0`, stable query/manifest/preview digests, invalid
isolation, 1-3 candidate deep-read, zero-candidate success with empty
selection/deep reads and consistent `mem_review=not_needed`, candidate-present
four-source mem insufficiency gate, stdout-only pre-task result, and exact
same-snapshot task-local persistence. Public docs distinguish pre-task/
standalone decision-branch binding from direct active task-mode
`task.json.branch` feature-worktree binding at the unchanged snapshot HEAD; all
sync provenance, selected base refs, repository identity, active task and
task-local dirty-scope checks remain mandatory. They list exits `context_ready` / `refresh_base` /
`blocked`, schema `guru-context-discovery-1.0`, all three runtime commands, and
the no-workspace/no-runtime/no-repo-cache boundary. Docs must not imply that
the Skill chooses duplicate reuse/new target or that a script performs its AI
Review Gate.
They also state that duplicate candidate facts are digest-bound to canonical
repo/number/identity/URL/open-state/update-time facts recomputed from the one
duplicate search result without a second search/re-read, and that `blocked` is
valid exactly when the AI Review Gate is blocked. Public examples must not
imply candidate fields or Gate/exit pairs are caller-trusted.
They also identify active semantic `guru-clarify-requirements` as the only
`context_ready` consumer. Public docs describe its initial/active-task/
standalone entry coverage, repository-answerable-before-user-question rule,
one-question loop, exact action/proposal confirmation, AI-owned GitHub mutation
boundary, stdout-only pre-task result, no dedicated clarification artifact,
schema `guru-requirements-clarification-1.0`, record/check runtime commands,
and exits `clear` / `needs_context` / `refresh_context` / `new_task` /
`blocked` with unique staged consumers. They must state that successful GitHub
mutation returns `refresh_context`, issue creation belongs to #112, and `clear`
uses the caller-aware `guru-requirements-clear-router`: initial/draft still
targets the staged #114 wording route, active-task resumes planning or the
exact interrupted phase, and standalone returns to its caller. Docs also state
that `answered` requires checked evidence, every question id participates in
the reducer lifecycle, and confirmed GitHub payload bytes equal mutation/live
content. For active tasks they must state that `clear`/`new_task` requires a
non-empty terminal proposal set and every five-class scope classification,
regardless of origin, requires exact user-decision evidence; every scope classification
has live GitHub authority and one exact structured
`issue-scope-ledger.json.scope_decisions[]` trail binding planning/review/re-entry
evidence; planning evidence must pass the complete shared schema 1.2 validator
rather than a hash/placeholder check; GitHub authority mutation returns
`refresh_context`; context time must not predate authority time, the task update
binds that digest without a second refresh, and mechanism dispositions require
no confirmation/trail/mutation before exact progression or a #112 side-effect-free new-task
draft. Docs also document source-specific task/GitHub/Git deep-read
locators, structured no-raw-payload persistence, and field-specific
validation. Workflow and stop route markers must
be described as validator-resolved target declarations, not new Skill packages.
Refresh documentation must state that record/check compare caller-authored
current stale codes, superseded query/snapshot digests, reason, and detection
time with live freshness, then require complete re-entry from only the current
payload and expected snapshot identity. It must also state that
task-local recorder/checker prove the exact target is not ignored by repository,
`.git/info/exclude`, or global Git exclude rules using `--no-index`, while
pre-task stdout mode does not run that target gate.

When workflow behavior changes, update the docs that users actually read:

- `README.md` for install/upgrade and daily operation
- `trellis/workflows/guru-team/README.md` for marketplace workflow behavior
- `trellis/presets/guru-team/README.md` for installer behavior and installed files

Do not let README instructions contradict the canonical workflow in
`trellis/workflows/guru-team/workflow.md`.

## Safety

Public docs must not include tokens, private repository URLs that reveal
secrets, signed URLs, `.env` contents, database URLs, or raw provider responses.

## Validation

For docs-only changes:

```bash
git diff --check
rg "publish-pr|review-branch|finish-work|trellis-start|trellis-continue" README.md trellis/workflows/guru-team/README.md trellis/presets/guru-team/README.md
```

When docs mention installed files, compare with the actual overlay and managed
asset lists:

```bash
find trellis/presets/guru-team/overlays -type f | sort
rg "MANAGED_ASSET_PATHS|Installed Files" trellis/presets/guru-team trellis/workflows/guru-team
```
