---
name: guru-bind-task-session
description: Bind one current session to a TaskLifecycleDTO, rebind after loss, switch, reactivate, and resume with lifecycle freshness.
---

# Guru Bind Task Session

`judgment_mode=semantic`. Read the explicit TaskId and generation (including
generation 0), current session, and the official Fixed Fork TaskId resolver.
Review the requested profile and target lifecycle before invoking the recorder.
The shared C4 branch/ownership readers and C3 checkout validator must agree on
one live execution checkout for every selected lifecycle. Ordinary dirty work
does not disqualify a session resume; identity or artifact conflicts do.
Select that current checkout before calling the Fixed Fork TaskId resolver:
an old branch may legitimately retain the same task artifact after rebind,
but it is not another current checkout. Scope official resolution to the
selected registered checkout and compare its TaskRef/artifact to the C3 result.
Only the current session pointer is mutable here; branch association, checkout,
resource ownership, task artifact locator, and lifecycle transitions have
separate owners. A missing context key yields `explicit_task_mode` with the
TaskLifecycleDTO and no session write.

- `resume_current_task` requires the existing session pointer to resolve to
  the exact current lifecycle; it performs no write.
- `rebind_missing_session` restores a missing pointer for the selected lifecycle.
- `switch_task` validates both the bound source and the selected target before
  replacing only this session's pointer. A -> B -> A is supported.
- `reactivate_rebind` accepts a pointer for the same TaskId at an older
  generation or a missing pointer in a new session; the target generation must
  fresh-resolve.
- `manual_recovery` repairs only a missing/stale schema-2 pointer for the
  explicitly selected task, never task/workspace mappings.

All five success exits carry `TaskLifecycleDTO + resume_target` to their retained
workflow routers. `explicit_task_mode` carries TaskLifecycleDTO to
`guru-current-phase-router`; `binding_blocked` carries ReasonDTO to
`task-session-binding-blocked`. Each consumer derives TaskRef afresh if needed.
Unknown, stale, ambiguous or mismatched official identity stops without writing.
