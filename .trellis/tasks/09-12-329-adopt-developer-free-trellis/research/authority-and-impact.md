# #329 Authority And Impact Evidence

## Live authority

- Issue: `https://github.com/castbox/guru-trellis/issues/329`, OPEN，updated at
  `2026-09-12T08:58:04Z`；close scope 仅 #329。
- Framework prerequisite: `castbox/Trellis#3` CLOSED on 2026-09-12；PR #4 merged at
  `3f078854d6c39ca2cf02ee08c1b83b167fa1cfaa`。
- Selected fixed candidate: `castbox/Trellis@a2003296b4c4ce46c50d72ead3b2ec9c317f69fc`；
  CLI package `0.6.17`，root package manager `pnpm@10.32.1`。
- General extension boundary: Trellis custom workflow and spec-template marketplace remain the supported
  extension surfaces; Guru behavior stays in Markdown workflow/Skill/preset overlays rather than upstream
  source or global installation patches.

## Upstream migration facts

The fixed candidate's `docs/identity-workspace-retirement.md` specifies:

- init `--user/-u` exits; bootstrap ownership uses explicit `--creator` / `--assignee`;
- task create requires explicit owner fields; existing task read/resume requires no new person input;
- `task list --mine/-m` migrates to `--assignee <name>`;
- identity initialization/read and session recording are retired without a replacement global store;
- default context removes developer/journal and exposes validated `currentTask`;
- historical identity/workspace/agent-trace data remains untouched and unconsumed;
- update migration must reconcile active customized runtime instead of silently leaving a mixed graph.

The old-to-new upstream diff touches about 400 files across generated templates, task/context helpers,
hooks, commands, update migration, tests and docs. It is therefore unsafe to hand-patch only current
dogfood scripts.

## Current Guru impact snapshot

Before implementation, active non-archive text references include both supported negative assertions and
stale normal-path dependencies. Approximate file counts from the 2026-09-12 worktree scan:

| Token | Active files | Main concentration |
| --- | ---: | --- |
| `.trellis/.developer` | 32 | preset verifier/tests, generated dogfood, task-workspace result contract, platform references |
| `.trellis/workspace` | 88 | installer/specs, workflow/docs, generated hooks/skills, root instructions |
| `TRELLIS_DEVELOPER` | 1 | generated `common/paths.py` |
| `init_developer` | 18 | generated runtime, preset fixtures/docs, platform references |
| `get_developer` | 22 | generated runtime plus create-task-workspace adapter/result |
| `add_session` | 28 | finish fixtures/overlays/docs and generated stock finish assets |
| `--mine` | 4 | generated stock task CLI and platform session hooks |

Zero matches are not the acceptance rule. Each occurrence must be classified as active consumer,
upstream retired stub, negative/preservation test, current migration documentation, or immutable history.

## Version-axis decision

Issue #378 established the repository pattern: a source-adoption task may advance the fixed Fork CLI while
leaving Guru extension/repository release publication to a later release task. Accordingly #329 advances
the framework/CLI/source axis to `0.6.17` / `a2003296...`; it does not create a new Guru tag or GitHub
Release. Public docs must not imply that the already released `v0.6.16-guru.1` contains the new source.

## Planning conclusion

- Scope is clear; no user-owned product decision remains.
- Direct evolution is required. There is no approved compatibility exception for old developer/workspace
  runtime behavior.
- Architecture impact is material because source binding, task identity resolution, distribution migration
  and lifecycle verification change. RDT and Architecture contributions are required before shared-current
  promotion.
