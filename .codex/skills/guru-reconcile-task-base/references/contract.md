# `guru-reconcile-task-base` Contract

## Entry And Pair Guard

The semantic Skill has six caller-owned input profiles: `post_plan`,
`post_check`, `post_commit`, `post_branch_review`, `post_publication`, and
`finalizer_base_mismatch`. Each carries one exact active-task identity,
`(task_head, old_base_head, new_base_head)`, selected base ref, and a closed
`resume_target`. Profiles carrying an existing branch or publication judgment
also carry its minimum caller-owned commit identity. There is no optional
continuity bag.

Before semantic invocation, `guard-task-base-pair` performs one live resolution
of the selected base ref. It returns only `unchanged`, `current_pair`,
`new_pair`, or `blocked`. It checks identity and ancestry, but never judges
authority, task-content impact, integration impact, relevant paths, validation
sufficiency, findings, or route. `unchanged` creates no checkpoint. A matching
owner-private result is consumable once and is then deleted by this package's
public wrapper.

## Semantic Owner

Before searching Docs, code, tests, history, consumers, or prior decisions,
read `.trellis/spec/workflow/semantic-retrieval.md`. That file is the sole
concept-family and evidence-coverage contract. Do not copy its vocabulary or
persist search terms/transcripts here.

The AI reviews three independent dimensions:

1. authority impact from live Issue, accepted requirements, Docs SSOT and scope;
2. task-content impact on approved planning, task code, tests and documentation;
3. integration impact for the exact candidate pair, conflicts and affected
   validations.

Base identity or path overlap alone is not a finding, stale result, pass, or
block. Insufficient applicable evidence fails closed. A semantic conclusion is
recorded only after the AI has bound the pair, reviewed scope, key delta,
validation adequacy, findings, remaining boundaries, and exactly one exit.

## Candidate And Script Boundary

`execute-base-candidate` creates a detached temporary worktree, merges the task
HEAD into the new base without committing or updating a persistent ref, runs
only closed argv-array validation commands, records objective return codes and
candidate tree identity, and removes the worktree. It never selects commands,
interprets failures, resolves conflicts, or chooses a route. Arbitrary shell
strings are rejected.

The recorder and checker validate the AI-authored result and live Git facts.
They do not generate semantic retrieval terms or infer impact/route. The
ignored `base-reconciliation.json` checkpoint contains only the exact pair,
selected exit, minimal consumer fields, and local digest. It is deleted after a
successful same-owner public invocation; stale state is removed before a fresh
review rather than chained.

## Exits

- `reconciled`: the workflow router receives task/current-base identity and the
  original `resume_target`.
- `review_continuity_required`: Branch Review receives the exact old/new pair,
  prior branch-review identity, candidate tree token, semantically relevant
  paths, and original route for bounded continuity.
- `implementation_required`: implementation receives exact finding refs and
  resumes the affected downstream graph.
- `planning_stale`: Planning receives exact reason refs.
- `scope_confirmation_required`: Requirements Clarification receives exact
  proposal refs; any user confirmation remains dialogue-local.
- `blocked`: stop with zero public payload.

Unknown, multiple, stale, consumer-mismatched, or structurally invalid results
fail closed.

## Compatibility

This additive 1.0 package replaces no published Skill id. Legacy active-task
base anchors may form one initial pair; absent anchors require a complete
bounded reconciliation. The package never reads another Skill's private
checkpoint, restores the retired shared compatibility dispatcher, rewrites
tracked task artifacts, or creates a persistent branch/ref/commit.
