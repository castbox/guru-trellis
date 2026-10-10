# #250 current Intake API migration

Upgrade the complete Guru preset and controlled callers together. Stable Skill
IDs and external exit IDs remain. There is no dual reader, alias, fallback or
compatibility adapter. An in-flight old input is not a current success; re-enter
Sync/context/Clarify with fresh legal input. Pinned-old history is not runtime.

| Previous boundary | Current boundary |
| --- | --- |
| Clarify initial_change_request 2.0 / aggregate 2.0 | standard_intake 1.0, reviewed_plan_intake 1.0 / aggregate 3.0 |
| Clarify active/standalone input 1.0 | input 2.0 with exact task generation or standalone consumer |
| Clarify clear 2.0 / needs_context 1.0 | clear 3.0 / needs_context 2.0 |
| Clarify private owner schema 2.0 | schema 3.0, explicit minimal source_selection |
| Discovery pre_task 2.0 | pre_task 3.0 with initial Clarify profile |
| Fixed initial context return 3.0 | context_ready 4.0 and context_request input 1.0 |
| Stage0 context/clarity/wording/readiness relays 1.0 | successor 2.0 identities with source/profile relay |
| Readiness clarify output 1.0, ready 4.0; Wording pass 2.0 | clarify 2.0, ready 5.0; pass 3.0 |
| Fixed downstream profile_id | Interface 1.8 selector reads only producer handoff_profile |

Both qualification confirmation input contracts remain 1.0. Their actual
qualifier producers and original owners remain separate. Interface 1.8 adds
only a named structured skill_input selector for producer handoff_profile; it
is a deterministic projection, with no expression language or route judgment.

Source selection is retained only in adjacent call-local transitions through
clear → Wording → readiness → task intake → current Planning. Create Task's
created DTO is still TaskId/TaskRef/generation. Loss or source revision returns
to the original Clarify/context owner. No task.json source model or future
Author prerequisite is introduced.
