# Requirements Design Test SSOT Contract

This semantic package owns one atomic repository authority across Requirements,
Design, and Test. The default versioned roots are `docs/requirements/`,
`docs/design/`, and `docs/test/`; the default isolated task contribution is
`docs/requirements-design-test-contributions/<task-ref>/` with `manifest.yaml`,
`requirements.md`, `design.md`, `test.md`, and `traceability.md`.

Every active requirement or behavior links to an owning design responsibility
or contract and at least one test strategy, scenario, or case. References carry
identity and location, not duplicated prose. Subtraction and structural changes
preserve predecessor/successor and version history. Two parallel tasks use
different contribution locators and do not mutate the same shared current file.

The package inherits the public Architecture Baseline identity as
locator/version/status. It does not read Architecture private state or copy
Architecture content. Repository authority remains separate from Trellis
task-local `prd.md`, `design.md`, and `implement.md`.

The AI owns provenance, authority, completeness, traceability, conflict,
revision, sync, and route decisions. The deterministic runtime records only
call-local data and validates the explicit AI gate, declared mode/profile,
continuation identity, safe locator, direct version/freshness binding, unique
consumer, minimal output, and schema. Public
output never contains document bodies, scan history, review narrative, Git
facts, authorization, recorder state, or private digests.
