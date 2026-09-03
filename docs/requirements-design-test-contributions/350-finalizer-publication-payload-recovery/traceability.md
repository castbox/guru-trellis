# #350 Traceability

| Requirement | Design | Test |
| --- | --- | --- |
| Allow normal Publication title/body evolution only for exact base evolution plus one legal tail | Publication mismatch bypasses pure fallback and requires the composed tail-parent classifier | Base-plus-tail metadata assertions and pure-base mismatch regression |
| Preserve fail-closed identity and business-drift checks | No changes to task/repo/branch/scope/HEAD/provenance validators | Negative drift matrix |
| Preserve public compatibility and idempotent execution | No schema/exit/stage changes; existing bound transaction engine | Execution/retry cardinality tests |
