# Extension Installation Verification Contract

## Entry

`verification_required` is the workflow target bootstrap owned by this package
for active `guru-finalize-task`. Its five business seed fields are
`task_ref`, `plan_ref`, `repo_ref`, `branch_review_commit`, and
`verification_target`; `profile` and `mode` are fixed discriminators. Global
Finish-family routing automatically consumes this target through the active
finalizer loop; the verifier result is not exposed as a user continuation gate.

`standalone_verification` carries `repo_ref`, `remote`, `ref`, and
`caller_intent`. Its closed schema has separate task-bearing and session-only
branches. The caller does not select a command matrix, supply source facts, or
author adequacy. Workflow and standalone calls apply the same runtime, target
repository, extension source, ownership, redaction, and freshness preconditions.

Every task-bearing execute, record, and check entry rebuilds repository
identity from the exact direct active task. It uses current `task.json`, the
ignored runtime mapping, the current checkout, and live Git worktree facts.
It requires the public `task_ref` to equal the current active task, rejects
archived or completed task locators, and proves the live branch, task identity,
target repository, and workspace boundary all describe the same repository
worktree. A wrong task, stale
active-task pointer, wrong branch/repository, or wrong worktree fails before
execution, persistence, or route projection. Taskless standalone calls do not
manufacture a task identity.

## Semantic loop

The AI first reads the target, reviewed diff, public installation contracts,
current manifest, and ownership inventory. It decides whether the change affects
an installable extension surface. If required, it selects a closed capability
profile and maps every affected surface to at least one of:

- `marketplace_index`
- `new_repo_init`
- `existing_repo_preview_switch`
- `preset_initial_apply`
- `preset_reapply`
- `trellis_update_reapply`
- `managed_conflict_sidecars`
- `skill_contract_discovery`
- `platform_equality`
- `ownership_inventory`
- `readme_commands`
- `redaction`

The deterministic executor first resolves and clones the public target into an
isolated `target-checkout`, verifies its exact HEAD, and derives reviewed-content
identity only from that checkout and the current task root. Task-bearing calls
then require `.trellis/guru-team/extension.json` in the target checkout. A
taskless standalone call may use its explicit public repository locator only
when that manifest is absent; malformed manifest bytes never select fallback.

The executor canonicalizes the manifest source to credential-safe GitHub HTTPS,
requires task-bearing manifest provenance to report `tree_state=clean`, then
resolves its requested ref, selects the peeled commit for an annotated tag and
the direct commit for a branch or lightweight tag, and compares that commit to
`source.commit` before source checkout. A full 40-hex ref initializes the
isolated checkout, fetches exactly that OID, and requires
`FETCH_HEAD^{commit}`, manifest commit, and checkout HEAD to match. Preset apply
from a Git worktree records the apply-time commit as this immutable ref, so a
later target branch commit does not move the selected source. It checks out the selected object in a separate
`extension-source-checkout` and verifies `HEAD^{commit}`. Either checkout or
manifest/commit mismatch fails closed. The throwaway installer, canonical
workflow/runtime/schema/package bytes, ownership inventory, and source sidecar
facts come only from the extension source checkout. Removing an installer from
the target cannot change execution; a missing source installer blocks it.

The executor gives the throwaway installer an explicit temporary work root and
reads installed assets only from its resulting clean `project` target. It then
records installed workflow, preset, schema, shared Skill, and
Agents/Codex/Claude/Cursor package digests. Every expectation names its
canonical source, manifest/platform relation, expected digest, category, and
optional platform. Category counts, missing/duplicate/unexpected/mismatched
paths, relation errors, and the expected-set digest make completeness
reviewable. Missing, duplicate, relation-mismatched, or byte-mismatched assets
fail the execution before `verified`.

Each selected capability records stable references to the command facts that
executed it and to its corresponding installed asset digest paths. The
monolithic throwaway command can support several capabilities, but a single
last-command index is never copied across the profile as sufficient evidence.
The executor records only credentials-safe locators, sanitized argv, exit codes,
output digests and sizes, installed asset facts, ownership facts, and sidecar
facts. It never infers applicability or route.

After execution, the AI reviews applicability, capability coverage, remote
identity, installation and update/reapply results, ownership, sidecars,
platform equality, and redaction. Every finding has a stable ref, evidence,
route class, status, and closure evidence. Human confirmation occurs only when
a standalone caller intent and the AI applicability judgment require a product
choice; a workflow plan-bound required target cannot be skipped by override.

## Private evidence

Workflow and task-bearing standalone calls persist exactly one task-local
`marketplace-verification.json`. Session-only standalone calls keep the owner
result in the current invocation and do not create a repository cache, latest
pointer, index, task artifact, or task-work route.

The current-only private 3.0 evidence binds the public input, separate
`target_repository` and `extension_source` identities, the target local and
remote `guru-reviewed-content-1.0` identities, source selection and manifest
provenance, direct object, selected commit and source checkout HEAD,
AI applicability and reason, selected closed capability profile, sanitized
command facts, installed asset expectations/digests/category completeness,
per-capability command/asset references, ownership/sidecar facts, AI adequacy,
findings, actual exit, consumer, redaction scan, retry/supersession identity,
and opaque `verification_ref`. Machine and semantic digests are recorded
separately and then bound by the final evidence digest.
Command facts use only `target_checkout` or `extension_source_checkout` owner
labels. Asset expectations/digests, ownership, and the sidecar fact object each
carry `checkout_owner=extension_source_checkout`; the binding remains present
when the sidecar path set is empty.

The checker validates schema, task/session persistence, public-input identity,
`branch_review_commit`, target ref/HEAD and reviewed-content binding, installed
manifest provenance, source direct/peeled resolution and checkout HEAD, plan and
supersession freshness, redaction, route
shape, consumer mapping, and evidence digests. It does not decide
applicability, sufficiency, findings, or semantic pass.

Private `target_repository.resolved_head` and standalone public `resolved_head`
both denote the target checkout commit. The source direct tag object and peeled
commit remain private and never enter a public DTO. Freshness checks re-resolve
both target and source refs with the same full-OID or direct-versus-peeled rules and reread
task-bearing installed manifest provenance.

The source locator must be canonical `https://github.com/<owner>/<repo>.git`
without userinfo, query, fragment, or alternate host. Unsafe source content is
rejected before clone and artifact write; public errors and eval traces retain
only generic errors or digests and never the credential URL.

## Exits and re-entry

- `verified`: every selected capability has passed command and installed asset
  evidence, the deterministic expected asset set is complete with all category,
  manifest, canonical, platform, and digest relations matched, every adequacy
  dimension passed, all current-scope findings are closed, remote identity is
  current, and redaction passed.
- `not_required`: AI applicability evidence is complete and no execution
  profile or fabricated pass facts exist. A workflow input fixed to
  `verification_target=extension-installation` cannot silently use this exit.
  The reachable finalizer edge therefore selects the task-bearing standalone
  `repo_ref/resolved_head/verification_ref` output; the finalizer target authors
  only `profile/mode/task_ref` and validates the task-local private evidence.
- `return_to_task_work`: a task-bearing invocation has open code/docs/tests
  findings routed to `phase-2`.
- `blocked`: auth, network, remote availability, taskless installation failure,
  or another external dependency prevents completion.

The public wrapper reruns the checker, derives the actual exit from the checked
owner result, chooses that exit schema, and serializes only the matching branch.
`expected_exit` is eval-only and is compared after invocation.

An unresolved remote HEAD is recorded as `null` only for a blocked execution.
The checker accepts it only while the exact ref remains unresolved; a later
resolution makes the blocker stale and requires a complete re-entry. The
standalone blocked DTO does not publish a fabricated `resolved_head`.

Auth/network retry under the same plan/ref/HEAD reruns the complete Skill.
Target HEAD/content, installed manifest, source ref/commit, plan, or task
implementation drift makes prior evidence stale and requires publication
review, closeout preparation, push, and extension verification to run again.
Production real-wrapper eval and a
real remote-ref clean installation are independent acceptance surfaces.
