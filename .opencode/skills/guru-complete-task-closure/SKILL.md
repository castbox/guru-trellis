---
name: guru-complete-task-closure
description: Apply the exact source Issue disposition after Completion approval and return a recoverable closure result.
---

# Guru Complete Task Closure

This owner consumes only Completion `completed`. No-Issue, reference-only,
follow-up and parent dispositions return `no_mutation`. An exact source Issue
never uses `no_mutation`; after confirmation, its CLOSED/OPEN decision comes
from a live read of that exact repository and Issue rather than a supplied
snapshot. An OPEN Issue is closed and post-checked against the same identity.

`resume_closure` carries the exact `closure_ref` transaction identity. Recovery
must return that identity; changing the source Issue, disposition or action
fails closed. The identity distinguishes `closed` from `no_mutation`.
