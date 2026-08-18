# Architecture Baseline Contract

The package is semantic and owns architecture authority, state transitions,
conflict classification, revision and route selection. It has four exclusive
profiles: `bootstrap_foundation`, `task_impact_sync`, `promotion`, and `repair`.

`docs/architecture/` is the business repository authority. FOUNDATION selects a
versioned horizontal stack baseline; CURRENT is evidence-proven implementation;
TARGET is accepted future state; GAP is an explicit delta; PLAN is approved
intent; ADR is historical decision context; EVIDENCE supports, but never
replaces, semantic judgment. Draft or inferred content cannot become active
authority without review, applicability, migration and verification evidence.

The deterministic invocation validates input schema, profile/continuation
identity and the owner-authored minimal projection. It does not decide
sufficiency, conflict, status, severity, acceptance or route intent.
