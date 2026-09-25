# #454 D443 Bind Session Architecture Contribution

- Identity: `architecture-contribution-454-task-lifecycle-d443-v1`.
- State: contribution candidate; current predecessor `.64/active`; proposed successor `.65` is not promoted.
- Source: live #454, generation 5 task, #456 `443-*` migration boundary and reviewed Phase C substrate.
- Change path: `target_native`; `ADR-015` remains framework/identity owner; no new ADR.

The existing deferred Bind package still uses workspace mappings and a path-bearing task locator. The target
major replaces that package's session semantics with TaskId/generation, live Phase C checkout and branch facts,
and the official Fixed Fork schema-2 session adapter. Bind owns route judgment and pointer validation/write;
it does not create a second session store or assume task, branch or resource ownership. Manual recovery restores
only the official pointer, not retired mappings. The five historical success exit IDs remain; explicit task mode
adds one exit, and blocked projects ReasonDTO.

This candidate narrows `ARCH-GAP-011` only at D443. Production workflow, registry selection, active manifest and
installed/platform projection remain on the old graph until E434 atomically publishes the complete D443/D436
package set and retires predecessor edges. Code tests, independent full-range review, serialized Architecture/RDT
promotion and fresh post-promotion gates must be reported separately; none is asserted here.
