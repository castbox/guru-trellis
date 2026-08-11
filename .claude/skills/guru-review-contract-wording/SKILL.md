---
name: guru-review-contract-wording
description: Review controlled contract wording through fixed change-request, planning-artifact, or explicit-path scope, semantic revision and classification, deterministic evidence, and typed exits.
---

# Guru Review Contract Wording

Use this Skill after requirements clarification, before planning approval, or
for an explicit standalone Markdown review. Load
[references/contract.md](references/contract.md) before acting.

Choose exactly one fixed profile. Build its complete scope, call the
deterministic scanner, prefer a permitted rewrite over retaining weak
wording, classify every retained hit with a non-empty reason, rebuild and
rescan after any mutation, then complete the AI Review Gate and any required
real-choice or side-effect interaction before calling the recorder and checker
wrappers. Any authorization stays only in the current dialogue; the owner
result contains no authorization state or process.

Return exactly one declared typed exit. `content_changed` requires complete
re-entry by the profile consumer; it is not a partial pass. Fail closed when
scope can be narrowed, evidence is stale or incomplete, a hit is unclassified
or a contract violation, mutation preconditions are missing, product semantics
would change without confirmation, or the compatible Guru Team runtime is not
installed. Results are stdout-only owner-private evidence. A mapped
`content_changed` re-entry rebuilds the complete current scope and discards the
prior result; it never creates a task-local replacement chain. This package is
not self-contained or portable.

After the semantic gate and owner recorder/checker complete, invoke
`scripts/invoke.sh --invocation -` with the closed call-local public input,
`clarity_current` transition, and checked owner result on stdin.
The minimal DTO preserves the fixed profile for the workflow router; the
runtime reruns the existing checker, derives the route from its checked result,
and never reclassifies wording or reads private evidence on behalf of a
consumer.
