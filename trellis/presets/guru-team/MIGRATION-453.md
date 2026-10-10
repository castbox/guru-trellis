# #453 Intermediate CLI Stdout Migration

The current command metadata schema is `guru-team-skill-commands-1.1` at
`trellis/skills/guru-team/schemas/skill-commands-1.1.schema.json`. The previous
1.0 schema retains its published bytes as a historical identity. Public Skill
input/exit DTOs, exit consumers, internal helpers and owner checkpoints retain
their existing contracts.

Current intermediate wrappers return a closed receipt with
`schema_version=1.0`, `formal_exit=false`, and `result` containing the previous
stdout object. The canonical behavior definition is
[Intermediate Command Stdout](./spec/workflow/companion-scripts.md#intermediate-command-stdout-10).
Read `result` before using `artifact_path`, an owner object, a checker receipt,
or an atomic execution/recovery result. Do not rerun an executed action merely
because its transport changed. Formal invoke output is consumed unchanged.

Update controlled CLI integrations, eval authoring and subprocess tests in the
same delivery. Trace receipts preserve actual outer stdout; they never label a
projected intermediate object as a public invoke result. Runtime accepts only
current metadata; no old-format fallback or permanent compatibility reader is
installed.

For a complete installation already accepted by current preset apply, use the
matching source checkout and run `scripts/bash/apply.sh --repo <target>`, then
the installed package validator. Preserve target edits through normal managed
provenance and resolve each `.new`/`.bak` before using the target. Runtime,
shared schemas, all packages and selected discovery projections form one unit.
An older installation rejected by current apply goes through the existing
`guru-upgrade-installation` source-owned contract; this document does not weaken
that owner's preconditions or reinterpret in-flight legacy work.

Validate current wrappers after reapply/update, including record/check/result
projection and formal positive/non-pass routing. One representative clean
sample and a complete predecessor-installation reapply establish this Issue's
bounded install evidence. List untested versions/platforms/update paths
explicitly; this task does not establish a full Release matrix or business
production upgrade. Real native Agent checker-only and record+check cases are
required independently of package/schema tests.
