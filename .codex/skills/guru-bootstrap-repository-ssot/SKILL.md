---
name: guru-bootstrap-repository-ssot
description: Bootstrap and repair the repository Requirements/Design/Test and Architecture Baseline SSOTs with a minimal .trellis/spec projection.
---

# Guru Bootstrap Repository SSOT

`judgment_mode=semantic`. This Skill owns Bootstrap orchestration, cross-SSOT
alignment, activation, revision, and route selection. It supports exactly three
public profiles: `new_repository`, `existing_repository`, and `repair`.

The forward path is: preflight; call upstream `trellis-spec-bootstrap`,
`guru-maintain-requirements-design-test-ssot:bootstrap_foundation`, and
`guru-maintain-architecture-baseline:bootstrap_foundation`; review cross-SSOT
alignment; project only the minimal overview into `.trellis/spec/`; then run the
deterministic validator. The child Skills own their internal authority
decisions. This Skill consumes only their minimal schema-validated locator,
version, status, scope, and freshness fields.

Use `new_repository` when no repository SSOT exists, `existing_repository` when
facts or partial authorities must be reconciled, and `repair` for an incomplete,
stale, conflicting, or failed projection. The AI decides sufficiency, conflict,
activation, revision, and route. The runtime only validates the selected public
input, owner identity, and typed projection; it never decides semantic status.

Public exits are exactly `completed`, `baseline_incomplete`, `repair_required`,
and `blocked`. Each exit has one declared consumer and one output schema.

Shared tracked document/spec writes require the normal current workflow
confirmation. Installation, upgrade, update, workflow switching, and preset
reapply may report Bootstrap state but never invoke it or archive the upstream
bootstrap task. This Skill does not own task creation, delivery, PR publication,
merge, or cleanup.
