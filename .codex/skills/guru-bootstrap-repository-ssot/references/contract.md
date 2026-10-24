# Bootstrap repository SSOT Contract

The package is semantic and owns Bootstrap orchestration, cross-SSOT alignment,
activation, revision and route selection. It has three public profiles:
`new_repository`, `existing_repository`, and `repair`.

The forward behavior invokes upstream `trellis-spec-bootstrap`,
`guru-maintain-requirements-design-test-ssot:bootstrap_foundation`, and
`guru-maintain-architecture-baseline:bootstrap_foundation`. Only minimal,
schema-validated typed outputs cross those package boundaries.

`docs/architecture/` is the business repository authority. FOUNDATION selects a
versioned horizontal stack baseline; CURRENT is evidence-proven implementation;
TARGET is accepted future state; GAP is an explicit delta; PLAN is approved
intent; ADR is historical decision context; EVIDENCE supports, but never
replaces, semantic judgment. Draft or inferred content cannot become active
authority without review, applicability, migration and verification evidence.

The deterministic invocation validates input schema, profile/continuation
identity and the owner-authored minimal projection. It does not decide
sufficiency, conflict, status, severity, acceptance or route intent. The only
external exits are `completed`, `baseline_incomplete`, `repair_required`, and
`blocked`, each with one direct consumer.

## Same-owner repair continuation

On `repair_required`, the declared rename maps only `exit_id` to `source_exit`.
The original caller authors `profile=repair`, retains its original `mode` and
`continuation_id`, and preserves any applicable `repo_locator`, `baseline`,
`scope`, and `contribution` from its current invocation. These values remain
call-local. They are not recovered from a producer-private result or added to
the output DTO. The same owner performs the actual repair and returns its real
exit; the projection itself grants no maintenance success.
