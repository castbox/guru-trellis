---
name: guru-complete-task-closure
description: Apply the exact source Issue disposition after Completion approval and return a recoverable closure result.
---

# Guru Complete Task Closure

This owner consumes only Completion `completed`. No-Issue, reference-only,
follow-up and parent dispositions return `no_mutation`. An exact source Issue
may return `closed` only after the current conversation has confirmed the
displayed repository, Issue, action and reason.
