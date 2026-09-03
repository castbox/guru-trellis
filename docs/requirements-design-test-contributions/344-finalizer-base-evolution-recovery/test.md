# #344 Test contribution

- `T344-01`: a real Git fixture covers a predecessor Publication followed by
  multiple base commits and a legal non-fast-forward base merge, then asserts
  existing-PR strict-ancestor recovery.
- `T344-02`: the fallback test asserts the current Publication is the only
  push target, PR creation remains zero, and the delegated recovery retains
  predecessor remote/PR identity and current Publication HEAD.
- `T344-03`: a business commit after the legal merge, plus existing scope/PR,
  multiple/fork, metadata and conflicting-transaction tests, remains
  fail-closed.
- `T344-04`: the existing #342 direct-child provenance-tail and #338
  equal-HEAD tests remain passing, together with canonical/installed package,
  preset reapply, ownership, drift, task-boundary and syntax checks.
- `T344-05`: the full release-wide throwaway matrix, tag/Release, deployment
  and production proof are outside this ordinary Issue's validation scope.
