# Task-Free Change Execution Contract

This semantic Skill owns checkout suitability, bounded editing, targeted checks,
and execution-time scope/risk evolution. Before writing, the AI reads repository,
branch/worktree, active-task scope, dirty/untracked, and target-overlap facts.
Default versus non-default branch identity is not a blocker. Branch protection
and other remote publication policy are outside this local execution decision.

The AI Review Gate must bind both sides of execution. `pre_write_review` records
why the selected checkout is suitable or why another route is required.
`completed` additionally requires `completion_evidence` containing the actual
edited paths, targeted checks with concise report summaries, a passed
`post_write_review`, and explicit unverified boundaries. Its public DTO exposes
only those edited paths, summarized check results, and unverified boundaries
needed by the workflow completion response; commands, review narrative, and
complete execution evidence remain private.

`reselect_mode` and `explicit_choice_required` are post-write routes. Each
requires `evolution_evidence` for a real partial edit: actual edited paths, the
new scope/risk fact, `stop_after_detection=true`, remaining target writes not
performed, and applicable targeted checks. Deterministic record/check/invoke
commands validate identity, bounded edited/remaining target membership, and
structure only; they never decide suitability, expansion
significance, scope, risk, edit completion, check adequacy, or route.

Same-scope active-task work returns `resume_active_task`; potential expansion
returns `scope_change`. Unrelated worktrees, dirty overlap, or insufficient
position evidence return `location_required`. Automatic task-free expansion
returns `reselect_mode`; explicit task-free expansion returns
`explicit_choice_required`. The two interaction exits self-reenter without
persisting the user's answer or authorization.

The public handoff is deliberately minimal. Review narrative, Git status,
target snapshots, check transcripts, and authorization remain private or
dialogue-local. Missing, stale, multiple, unknown, or unmapped results fail
closed.
