# #410 Release v0.6.17-guru.1 Design contribution

- `D410-01`: advance only current release-facing version mapping and required
  canonical/dogfood projections; preserve historical facts.
- `D410-02`: keep repository tag, extension version, and CLI/source lock as
  separate identity axes.
- `D410-03`: route Architecture and RDT through serialized promotion; any
  promotion-created bytes invalidate earlier Phase 2, commit, and review.
- `D410-04`: after preparation merge, derive one exact candidate from fresh
  `origin/main` and prevent cross-SHA evidence reuse.
- `D410-05`: retain existing owner boundaries and use `Refs #410` for the
  Publication reference without implying Issue closure.
- `D410-06`: perform annotated tag, tag-pinned smoke, GitHub Release, and Issue
  closure as separate live actions with separate authority checks.
