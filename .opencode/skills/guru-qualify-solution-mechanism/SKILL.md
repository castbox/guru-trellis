---
name: guru-qualify-solution-mechanism
description: Qualify whether a proposed implementation mechanism can carry the required business authority without delegating it to OS, kernel, process, or descriptor primitives.
---

# Qualify Solution Mechanisms

Read `references/contract.md` completely before judging the candidate set. The
Skill is a semantic owner: read current requirement, planning, architecture,
dependency/caller graph, diff, tests, and repository contract yourself. Then
review the complete candidate set and invoke `scripts/invoke.sh --invocation -`
with one call-local JSON envelope on stdin.

Do not use keyword, import, command-name, path, or static scanner output as the
qualification decision. Such output can be evidence for AI inspection, but it
never replaces semantic review.

OS locks (`flock`, `fcntl`, lock files, inode ownership), `/proc`, PID/PGID/SID
or process trees, liveness scans, FD identity/inheritance, signals, `kill`,
process-group control, and equivalent kernel/process/descriptor wrappers are
never business authority. Ordinary files and directories remain valid for
state, artifacts, logs, caches, configuration, and durable records when their
existence, inode, FD, or open state is not used as authority, fencing, leader
election, or a concurrency protocol.

Return exactly one declared typed exit. The runtime only checks closed shape,
identity, freshness, enum aggregation, and consumer binding; it must not decide
whether a mechanism is good or bad and must not write qualification state.
