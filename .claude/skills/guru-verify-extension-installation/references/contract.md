# Extension Installation Verification Contract

## Entry

`verification_required` is the workflow target bootstrap owned by this package
until `guru-finalize-task` is implemented. Its five business seed fields are
`task_ref`, `plan_ref`, `repo_ref`, `reviewed_head`, and
`verification_target`; `profile` and `mode` are fixed discriminators. This
package does not publish or activate the future producer edge.

`standalone_verification` carries `repo_ref`, `remote`, `ref`, and
`caller_intent`. Its closed schema has separate task-bearing and session-only
branches. The caller does not select a command matrix, supply remote facts, or
author adequacy. Workflow and standalone calls apply the same runtime,
repository, remote/ref, ownership, redaction, and freshness preconditions.

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

The deterministic executor runs the selected closed profile against a frozen
remote HEAD. It records only credentials-safe locators, sanitized argv,
exit codes, output digests and sizes, asset digests, ownership facts, and
sidecar facts. It never infers applicability or route.

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

The private evidence binds the public input, safe repository/ref/HEAD identity,
AI applicability and reason, selected closed capability profile, sanitized
command facts, asset/ownership/sidecar facts, AI adequacy, findings, actual
exit, consumer, redaction scan, retry/supersession identity, and opaque
`verification_ref`. Machine and semantic digests are recorded separately and
then bound by the final evidence digest.

The checker validates schema, task/session persistence, public-input identity,
remote/ref/HEAD binding, plan and supersession freshness, redaction, route
shape, consumer mapping, and evidence digests. It does not decide
applicability, sufficiency, findings, or semantic pass.

## Exits and re-entry

- `verified`: every selected capability and adequacy dimension passed, all
  current-scope findings are closed, remote identity is current, and redaction
  passed.
- `not_required`: AI applicability evidence is complete and no execution
  profile or fabricated pass facts exist. A workflow input fixed to
  `verification_target=extension-installation` cannot silently use this exit.
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
Remote HEAD, plan, reviewed content, or task implementation drift makes prior
evidence stale and requires publication review, closeout preparation, push,
and extension verification to run again. Production real-wrapper eval and a
real remote-ref clean installation are independent acceptance surfaces.
