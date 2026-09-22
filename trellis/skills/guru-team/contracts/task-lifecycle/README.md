# Task lifecycle contract primitives

`task-lifecycle-dtos.schema.json` is the canonical Draft 2020-12 catalog for
the shared lifecycle DTO family. Consumers reference one named definition,
for example `#/$defs/TaskArtifactDTO`; they do not accept the catalog's broad
top-level union as a public package output.

The catalog keeps stable task identity, mutable task locator, lifecycle
generation, source relation and operation-scoped result identity separate.
It intentionally contains no checkout path, workspace path, session identity,
authorization state, generic evidence bundle or durable Git HEAD authority.

This directory is substrate only. It does not register a Skill, select a
workflow edge or activate a production package.
