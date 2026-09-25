# #454 D443 Bind Session Architecture Contribution

- Identity: `architecture-contribution-454-task-lifecycle-d443-v1`.
- State: reviewed and promoted; immutable predecessor `.64` to current successor `.65`.
- Source: live #454, generation 5 task, #456 `443-*` migration boundary and reviewed Phase C substrate.
- Change path: `target_native`; `ADR-015` remains framework/identity owner; no new ADR.

The existing deferred Bind package still uses workspace mappings and a path-bearing task locator. The target
major replaces that package's session semantics with TaskId/generation, live Phase C checkout and branch facts,
and the official Fixed Fork schema-2 session adapter. Bind owns route judgment and pointer validation/write;
it does not create a second session store or assume task, branch or resource ownership. Manual recovery restores
only the official pointer, not retired mappings. The five historical success exit IDs remain; explicit task mode
adds one exit, and blocked projects ReasonDTO.

The C4 binding and C3 live validation first select the unique current checkout. Official TaskId resolution then
checks that checkout's artifact, not every retained old-branch copy: an old resource incarnation can still contain
the same TaskId/generation after rebind without becoming a second current task authority.

This candidate narrows `ARCH-GAP-011` only at D443. Production workflow, registry selection, active manifest and
installed/platform projection remain on the old graph until E434 atomically publishes the complete D443/D436
package set and retires predecessor edges. Code tests, independent full-range review, serialized Architecture/RDT
promotion and fresh post-promotion gates must be reported separately; none is asserted here.
