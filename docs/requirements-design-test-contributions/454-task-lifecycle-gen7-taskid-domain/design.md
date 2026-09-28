# #454 Generation 7 TaskId Domain Design Contribution

Status: isolated candidate against `.67/active`; not promoted.

- `D454-G7-01`: Pin the merged official Fork commit
  `09994d21a462813c4d1a280cce7fe1bf803af019` as the implementation
  candidate. The official task writer validates explicit and slug-derived IDs. Guru
  `identity.py` and the shared DTO schema use the exact same TaskId pattern.
- `D454-G7-02`: Derive handoff receipt refs in one runtime owner. Preserve
  the prior ref for Git-valid IDs; otherwise use
  `guru-task-lifecycle-id/<sha256(TaskId UTF-8)>`. Keep the generated ref
  separate from the immutable TaskId and validate retained-control ownership
  against the resulting Git-valid namespace.
- `D454-G7-03`: Project the source to installed and declared platform
  copies through the preset mechanism. Remove no session or task binding
  flexibility: a session focus can switch or rebind by TaskId without
  treating Git HEAD, Issue, checkout, developer or assignee as task identity.
