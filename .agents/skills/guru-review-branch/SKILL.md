---
name: guru-review-branch
description: Review a committed task branch or bounded base delta through independent semantic review and five typed exits.
---

# Guru Review Branch

Use this Skill after `guru-create-task-commit:committed` and before publication.
Read [references/contract.md](references/contract.md) completely before acting.

Before searching the range, Docs, tests, fixtures, consumers, or relevant
history, read `.trellis/spec/workflow/semantic-retrieval.md` and apply it in
candidate qualification. A negative finding or impact conclusion cannot rely
on a single-language zero result, and no query process enters the gate or DTO.

Validate all eight entry preconditions in workflow or standalone mode. Perform one
independent semantic review of the complete current range. Form only candidate
refs and live locators, then invoke `guru-qualify-normal-scenario` with
`branch_review_candidate_set` before assigning severity.
Scripts never decide scope, scenario class, qualification, severity,
review sufficiency, pass, or route.
Rejected candidates remain `rejected_candidate` without severity or
finding-only fields and cannot become scope confirmation, tests,
implementation, follow-up, or publication blockers. Mechanism revision returns
to task work for remove/replace and fresh qualification; blocked stops. The
review gate records only this owner's final classifications and direct-consumer
witness, never a qualification artifact.

Before this review can pass, consume a fresh
`guru-maintain-architecture-baseline:task_impact_sync(stage=branch_review)`
result. The Architecture owner independently recomputes project checks and
before/after satisfaction from the complete committed base-to-HEAD diff. This
Skill then rereads the current Architecture Baseline, design constitution, and
task-local change contract as part of its own complete-range semantic review.
Neither owner may reuse the Phase 2 Architecture result as Branch Review proof.
A stale identity, incomplete contract, authority conflict, fitness regression,
unreviewed contribution, or missing project check prevents `passed` and follows
the Architecture result's unique global route.

Every official independent-review worker invocation prompt authorizes
approved-plan work only. A planning-external observation must stop before any
edit, added test, self-fix, severity, classification, or route and return only
`candidate_ref`, `observed_behavior`, `locators`, and
`minimal_reproduction_hint`. This owner rereads the live range and authority
and completes fresh qualification before continuing the review or dispatching
another worker for that candidate. Upstream-owned `trellis-*` agent files stay
unchanged.

Current-scope qualified findings return `implementation_required`; fixes must
pass the applicable checks, a fresh task commit, and this Skill again. An
unconfirmed nonstandard proposal returns `scope_confirmation_required` and
cannot become a finding. After a fix commit, the finding owner or a real
unfinished-agent replacement performs closure as an internal transient
judgment. It retains `introduced_head`, binds the fixing `fix_head`, and
produces a later `closure_head` plus concrete closure evidence. The AI workflow
then automatically dispatches a distinct fresh reviewer over the complete
current `origin/<base>...HEAD` range.

Closure emits no public exit and writes no artifact. Only the distinct
`fresh_final_review` may reach the recorder and pass. After its AI Review Gate
exists, the recorder writes the compact `review-gate.json` to the exact
task-owned ignored-runtime checkpoint and returns only a minimal receipt; it
does not create assignment, liveness, rollup, or raw per-round reports. Only
after `check-review-gate` resolves and validates that exact checkpoint
may the public wrapper emit exactly one of `passed`,
`continuity_passed`, `implementation_required`,
`scope_confirmation_required`, or `blocked`.
`passed` targets the active `guru-review-task-publication` Skill through its
target-owned authoring seed. The workflow caller performs the publication
content authoring preparation required by the global Phase 3.6 order before
invoking that active owner.
This package is not self-contained or portable.

The public wrapper accepts only current public input, reruns the objective
checker internally, and never accepts caller-authored gate or checker output.
Successful `passed`, `continuity_passed`, and zero-payload stop `blocked`
projection retires the checkpoint. The two active re-entry routes retain the
one checkpoint for deterministic
same-owner re-entry; a repeated invocation returns the same DTO without writing
another checkpoint. Failed check or projection preserves the current regular
checkpoint. A retired, mismatched, stale, unsafe, or symlink-backed checkpoint
fails closed.

If Architecture promotion changes shared current files, that diff returns to a
fresh Phase 2 Architecture/check round, a new task commit, and this independent
complete-range Branch Review. Publication cannot consume the pre-promotion
review or a Phase 2 result in place of that fresh review.

Aggregate public input schema 3.0 dispatches two profiles: `branch_review`
schema 2.0 accepts only `initial_review` and `fresh_final_review`, while
`base_continuity` schema 1.0 accepts only `base_continuity`. The owner-private
gate is current-only schema 6.0 and records profile-specific identity plus
`review_commit`, `reviewed_content_algorithm`, and `reviewed_content_sha256`.
Aggregate input schema 2.0 and gate schema 5.0 or older remain legacy stale
inventory, not current runtime authority. Any non-6.0 gate fails closed through
the stable stale-identity path. Any other current input shape fails closed
through the normal invalid-input path. The commit is used for range and finding
ancestry; the reviewed-content identity alone owns content freshness.
