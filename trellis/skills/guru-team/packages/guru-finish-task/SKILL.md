---
name: guru-finish-task
description: Persist Completion and Closure into one reviewed task archive and terminal bookkeeping result.
---

# Guru Finish Task

Finish accepts only the current Closure ResultRefDTO, resolves TaskRef from the
stable TaskId, and reads the exact terminal action set through the shared
read-only Closure result API. Before
terminal mutation it rereads every required-closed Issue; drift returns
`closure_refresh_required` for Closure's semantic re-entry. A bookkeeping
merge is not a business Delivery and never closes an Issue.

The normal transaction has three independently confirmed mutations: local
archive projection, bookkeeping commit/push/PR publication, and expected-head
merge. The executor recovers only that exact transaction and returns `success`
only after the remote target baseline contains the final archive and no active
copy. The reviewed payload forbids Issue-closing keywords and Delivery trailers.
Only after remote target verification does Finish seal the current generation
and exact result in the common-dir resource ledger against the bookkeeping PR
head (the cleanup refs' actual HEAD), then retire its branch binding. The
target merge commit separately proves that the archive is persisted. `success` hands its
ResourceSealRefDTO to Cleanup; missing terminal ownership returns
`manual_cleanup_required`. Finish never deletes a resource. This canonical
manual route records the minimal terminal identity in Git common-dir so it
survives removal of the original checkout;
Reactivate requires its matching completed manual Cleanup receipt before using
the archived generation. The Finish bookkeeping commit and target merge commit
remain distinct identities.
This canonical
package major is not active until the separate graph activation.
If the shared Closure result reader is unavailable, Finish stops before
terminal mutation instead of accepting an unbound caller action list.
