---
name: guru-finish-task
description: Persist Completion and Closure into one reviewed task archive and terminal bookkeeping result.
---

# Guru Finish Task

Finish consumes only current Closure `closed` or `no_mutation`. It owns the
active-to-archive projection and terminal metadata. A bookkeeping merge is not
a business Delivery and never creates a Delivery result or closes an Issue.

The normal transaction has three independently confirmed mutations: local
archive projection, bookkeeping commit/push/PR publication, and expected-head
merge. The executor recovers only that exact transaction and returns `success`
only after the remote target baseline contains the final archive and no active
copy. The reviewed payload forbids Issue-closing keywords and Delivery trailers.
