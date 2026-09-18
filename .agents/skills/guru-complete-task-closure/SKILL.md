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
