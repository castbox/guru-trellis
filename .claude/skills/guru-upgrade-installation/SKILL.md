---
name: guru-upgrade-installation
description: Upgrade a supported legacy installation from the complete target source with explicit reviewed projections, ordinary partial-write recovery and bounded rollback.
---

Load this standalone semantic Skill from the complete target canonical source
checkout before asking an old installation to validate current runtime state.
Read [the owned contract](references/contract.md) and the selected public input
and per-exit schemas in `interface.json`. Use `scripts/preview.sh` only for
read-only owner facts; `scripts/invoke.sh` is the sole normal public entry.

The source checkout's managed interpreter and complete package graph are
required. A discovery copy is not a self-contained migration tool. `--root`
identifies the target checkout; the wrapper still loads the target source's
runtime. Do not route initial migration through the old target's dispatcher.

Follow the exact semantic profile: forward behavior, AI Review Gate,
conditional current-dialogue confirmation, executor/validator, one typed exit.
Unknown versions, stale decisions, missing provenance and unmapped exits stop.
Scripts do not decide scope, semantic sufficiency, task disposition or approval.
