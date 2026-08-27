---
name: guru-verify-extension-installation
description: Verify a Guru Team source checkout through a clean standalone throwaway installation, semantic adequacy review, and two terminal exits.
---

# Guru Verify Extension Installation

Invoke only for explicit standalone verification from a clean
`castbox/guru-trellis` source checkout. Read `references/contract.md` before
use. This package is not a global workflow step and accepts no business task,
Publication, Finalizer, branch-review, or task-artifact identity.

Run source identity preflight before clone, install, temporary-directory
creation, or owner-result write. Then execute the clean throwaway installation
catalog, perform the AI adequacy review, record/check only ignored session
state, and return exactly one of `verified` or `blocked`. Any retired
task-bearing input fails closed and returns to current Publication/Finalizer
reprepare; it is never adapted into the standalone input.

If the throwaway compatibility matrix fails, consume only its cleanup-safe
structured terminal facts: `pre-matrix|matrix-cell|post-matrix`, applicable
cell id, stable command label, exit code, and a bounded credential-safe error
tail. Preserve them in execution facts before the temporary lifecycle exits.
Malformed terminal output is recorded explicitly as
`unparseable_failure_output`; aggregate stdout/stderr digests remain present but
never replace the structured failure facts. A failed command or a failed
inventory, ownership, sidecar, or capability postcheck likewise records one
deterministic `postcheck_failure`; `status=failed` never carries `failure=null`.
