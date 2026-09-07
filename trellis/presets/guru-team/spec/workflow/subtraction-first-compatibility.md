# Subtraction-First Compatibility Contract

This is the durable policy source for Issue #108. It extends existing semantic
owners; it does not create a Skill, phase, approval system, audit ledger, or
static call-graph analyzer.

## Default Mechanism

For delete, replace, merge, and add work, the owner first reviews the supported
entry, callers, registrations, configuration/schema consumers, tests, and
current documentation. The default mechanism is direct modification, deletion,
in-place replacement, reuse, or synchronized consumer migration. A second
execution path, wrapper, adapter, fallback, dual-read/write, legacy parser, or
parallel state machine requires a concrete reason; a `public` or `stable` name
alone is not a compatibility contract.

An affected deprecated asset that loses its only supported consumer in the accepted scope exits in
the same task, including its entry, implementation, branch, configuration,
schema, dependency, test, documentation, and navigation. Shared assets remain
only for verified supported consumers. Zero text matches are evidence to
investigate, not proof of retirement; registration, reflection, dependency
injection, external callers, public APIs, and test-only callers must be
considered. A test-only call does not establish production capability, while a
legitimate local duplicate is not removed mechanically.

## Compatibility Exception

Non-server external APIs use direct evolution by default: update controlled
consumers to the new contract and remove the old path. Internal DTOs,
checkpoint/artifact schemas, script arguments, CLI aliases, configuration
fields, internal modules, installed copies, and platform wrappers receive no
compatibility exemption from naming.

An existing, explicit, unexpanded server-side external API stability contract
continues to apply without another confirmation. It is not permission to add
versions, widen behavior, or extend the support period.

Before coding, adding compatibility tests, or self-fixing, any other proposed
compatibility must be presented in the current conversation with its real
legacy consumer and evidence, direct-evolution impact, exact behavior and
scope, maintenance owner, exit condition, cleanup responsibility, and
verification method. Only explicit approval of that concrete exception permits
implementation. A generic continuation or plan confirmation does not. If it
is not approved, use direct evolution or stop at the existing owner route.
One-time data/configuration migration is reviewed separately from long-term
runtime compatibility and retains its existing side-effect confirmation rules.

Approval is dialogue-local. Never persist authorization, approval status,
approval wording, approval hashes, or review transcripts in task artifacts,
checkpoints, gates, schemas, DTOs, or scripts. Durable docs record only the
resulting support contract, version boundary, exit condition, and cleanup owner.

## Complexity and Maintainability Boundary

Normal task execution must not add mechanisms merely for hostile-input defense,
unbounded backward compatibility, concurrency stress, TOCTOU handling, unusual
crash consistency, or formal idempotency when the accepted contract does not
require them. Existing normal stale, mismatch, failure propagation, secret
redaction, permission, and destructive-side-effect rules remain in force. The
AI must first ask whether a proposed field, state, retry, lock, fallback,
adapter, receipt, or persistence is required by a named direct consumer (or
named direct consumers when responsibility is shared); if not, it is
redundant growth and must be removed or redesigned.

The task's long-term maintainability objective has equal standing with its
immediate acceptance target. Before adding a fix, the owner checks whether it
duplicates an existing responsibility, leaks task-local state into a shared
contract, shifts an Architecture owner or decision, or makes later changes
depend on a hack-specific path. Such a candidate returns to the existing
qualification or Architecture owner instead of being accepted solely because
the current task would pass. The `personaId` task-field regression is a
representative warning: a field without a direct durable consumer must not be
introduced to carry incidental context.

For future changes, every non-generated code file touched by a task must remain
at or below 3000 lines. The 3000-line threshold triggers an
AI-reviewed mechanical split or small decoupling refactor before the task can
pass; the threshold is a mandatory review trigger, not a claim that every
historical large file is refactored by this Issue. Generated files and
canonical managed projections are excluded from this source-file threshold,
while their existing generation, ownership, and drift checks still apply.
Untouched historical large files remain outside this task's scope.

## Independent Review Dimensions

Phase 2 and Branch Review independently judge both dimensions when applicable:

- `code_subtraction`: production/runtime, scripts, schema, config, dependency,
  registrations, and test-entry retirement or retained responsibility.
- `docs_ssot_subtraction`: requirement/product, design, test,
  operations/navigation, RDT authority, and Architecture authority retirement,
  merge, historical marking, or intentional retention.

`code-only`, `docs-only`, and `mixed` are not inferred from one another. For a
delete/replace/merge task, net growth is an AI review signal, not a numeric
gate. Explain growth by production, test, generated/managed, and documentation
categories; necessary tests, generated assets, or new behavior may grow. Growth
caused by unsupported compatibility or redundant state requires deletion or
redesign, not a generic safety justification.

Historical tasks, archived evidence, ADRs, releases, changelogs, migrations,
contributions awaiting promotion, and canonical managed projections are not
current runtime compatibility consumers. RDT and Architecture retain their
existing ownership, subtraction, promotion, before/after, GAP, and single-writer
contracts.

## Owner Integration

- `guru-approve-task-plan` checks the direct-evolution choice, affected-asset
  exit plan, support contract, and any concrete compatibility candidate before
  approval.
- Implementation callers authorize approved-plan work only. A newly observed
  out-of-plan deprecated asset, compatibility need, or owner/authority change
  stops before editing and returns the existing invocation-local candidate
  route for qualification.
- `guru-check-task` checks the complete worktree, deletion-growth rationale,
  deprecated-asset exit, current compatibility contract, and both independent
  subtraction dimensions.
- `guru-review-branch` independently recomputes those checks over the complete
  committed `origin/<base>...HEAD` range and does not read Phase 2 evidence.

AI owns applicability, consumer sufficiency, compatibility necessity, growth
reason, findings, and routes. Scripts only capture or validate objective Git,
path, schema, status, and identity facts. Normal stale, mismatch, missing
evidence, and implementation defects follow existing fail-closed or owner
routes; hostile-input, deliberate forgery, concurrency stress, TOCTOU, and
unusual fault-injection hardening are outside this contract.
