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
