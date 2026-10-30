# JSON inputs and complete Bind invocations

`--input` and `--owner-result` each accept one JSON object as inline text, a
regular UTF-8 JSON file, or `-` for stdin. Existing regular files take priority
over inline text. A symlink to a regular file retains its existing support.
Directories, devices, FIFOs and shell process substitution such as `<(...)`
are unsupported. Use a regular file or the single stdin channel instead.

Only one parameter may be `-`. Two stdin selections fail before either read
with `conflicting_arguments`, `field_path=arguments.--owner-result`, and exit 2.
The remediation names both parameters and gives a supported alternative.

## Prepare the original two inputs

First complete the original Identity and Ensure steps for the current TaskId
and lifecycle generation. Read the actual current session. Select one of the
five original Bind profiles only when its preconditions hold. The Bind owner
then reviews the lifecycle and route and authors the original semantic result.
Do not manufacture a passed gate to try a carrier example.

For `delivery_resume_current_task`, `bind-input.json` contains the original
`profile`, `mode`, actual `task_id`, `lifecycle_generation` (including zero), and
`continuation_id`. The existing session must resolve to that exact lifecycle.
`bind-owner-result.json` contains the matching original fields, `route=resume`,
the reviewed `resume_target`, and the owner's actual `ai_review_gate` result.
Both files must satisfy the selected package schemas. The other profiles keep
their own preconditions and required fields, including source lifecycle fields
for a switch. This document adds no profile or envelope.

Save those already reviewed objects as `./bind-input.json` and
`./bind-owner-result.json` in the selected checkout. The paths below are regular
files containing that session's real identities; `example` is not a TaskId to
reuse. Run from the selected checkout with the complete matching preset and
managed runtime installed.

## Two regular files

```bash
.trellis/guru-team/skills/packages/guru-bind-task-session/scripts/invoke.sh \
  --root . \
  --input ./bind-input.json \
  --owner-result ./bind-owner-result.json
```

## One stdin and one inline object

The command substitution below supplies the already reviewed owner object as
one quoted argument. It does not use a file descriptor or process substitution.

```bash
cat ./bind-input.json | \
  .trellis/guru-team/skills/packages/guru-bind-task-session/scripts/invoke.sh \
    --root . \
    --input - \
    --owner-result "$(cat ./bind-owner-result.json)"
```

A successful resume returns the original `session_resumed` typed exit. A missing
context key retains the original `explicit_task_mode`; other identity, schema
or semantic failures retain their original handling. Neither carrier example
selects a Delivery or proves that business work has completed. After the call,
follow the exit's original consumer and retain any existing same-Task Delivery
selection. Keep temporary owner inputs private and remove them after their
consumer completes; never include authorization or secrets in these inputs.

## Read failures and recovery

All rows except the double-stdin conflict retain `invalid_json`, the original
parameter field (`input` or `owner_result`), and exit 2. Remediation describes
the actual failure without echoing JSON, local paths or OS exception details.

| Observation | Correction |
| --- | --- |
| An explicit absolute, `./` or `../` file path does not exist | Supply an existing regular UTF-8 JSON file, inline object or one stdin. |
| File/stdin cannot be read, or text cannot be decoded as UTF-8 | Repair the readable UTF-8 source. |
| Nonregular carrier, including zsh process substitution | Use a regular file, inline object or one stdin. |
| Empty or whitespace-only content | Supply one JSON object. |
| Syntax error in already-read file/stdin content | Correct the JSON syntax. |
| Parsed array, scalar or null | Supply an object at the top level. |
| Mixed argument is neither a readable file nor valid inline JSON | Use an explicit path, valid inline JSON or one stdin. A slash or suffix alone does not establish a file path. |

File probing must not reject valid long inline JSON. An ambiguous argument is
not reported as a confirmed missing file or as malformed already-read content.
After reading succeeds, original schema and lifecycle checks still apply.
