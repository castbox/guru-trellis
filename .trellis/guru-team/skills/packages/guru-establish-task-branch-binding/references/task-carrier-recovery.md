# Same-identity Task carrier recovery

This is the original Branch owner's bounded recovery profile. Markdown owns
intent, source sufficiency, the exact target/write set, semantic review and
route. Git, native task tools and the existing Identity/Branch/Ensure/Bind
writers execute their own facts. This procedure does not create another owner,
Task, generation, Delivery, gate or recovery ledger.

## Entry and stop conditions

Use this contract when a supported schema-2 active Task is missing from the
receiving checkout, or its original files have been restored but an unbound
HEAD tree does not contain it. There must be a retrievable fixed Git commit
that identifies the original TaskId/generation, source/scope, Delivery and
complete planning carrier. Read the original record and plans, including real
Publication/Delivery/full_review/readiness gaps. A history gap is not a failed
file restore and must not be replaced with an invented success.

Stop at the original Identity/source or migration owner if the carrier cannot
be obtained, identity/source is ambiguous, the schema is unsupported or the
records conflict. Stop at Branch for a different existing association or
resource incarnation. Missing/multiple registered checkouts retain the original
acquisition route. Do not create substitute identities, copy another common
directory's controls or hand-edit Task/session/ledger JSON to make a step pass.

## 1. Fix the carrier and review the local action

1. Resolve the chosen source to a full commit and inspect its exact Task
   directory, metadata, Delivery planning roots, full plans and necessary
   history. The source need not already be in the default branch.
2. Compare that carrier with the intended original TaskId/generation and
   current repository. Identify existing valid C4/C5 and current-session facts.
3. Select the target baseline, current branch/registered checkout and exact
   file write set. Read local tracked/untracked changes in those paths. Display
   the concrete file restore, any base change and missing association/pointer
   writes under their original dialogue boundaries. Do not overwrite unrelated
   work. An already reviewed same-target action continues automatically;
   changed target, payload or write scope returns to that original boundary.

Authorization stays in the current dialogue. No request, confirmation, timestamp,
authorization field or authorization history enters an input, Task, runtime
checkpoint or public DTO.

## 2. Restore files and the selected baseline

Use native Git for only the reviewed original paths. The following is a
parameterized example; replace its source and path with the current reviewed
facts before running it:

```bash
TASK_CARRIER_COMMIT='<fixed-full-commit>'
TASK_RESTORE_REF='.trellis/tasks/08-15-example-recovery'
git restore --source "$TASK_CARRIER_COMMIT" --worktree -- "$TASK_RESTORE_REF"
```

The example restores one reviewed Task directory. If the reviewed write set
has several paths, pass each exact path as another quoted argument after `--`.

When the selected baseline differs from the restored value, use the native
writer in the target checkout:

```bash
TASK_RECOVERY_REF='.trellis/tasks/08-15-example-recovery'
TASK_RECOVERY_BASE='dev'
python3 .trellis/scripts/task.py set-base-branch "$TASK_RECOVERY_REF" "$TASK_RECOVERY_BASE"
```

Reread the actual files and diff. Require the same TaskId/generation/Delivery,
full plans and historical gaps, plus only the reviewed base change. Git
restoration is a file result; set-base-branch is a baseline-field result.
Neither establishes C4/C5, selects a Delivery or records a stage pass.

## 3. Resolve workspace identity

Call the original Identity owner in the registered target checkout. This
deidentified example shows the complete input shape; replace every identity
with the reviewed carrier's actual value:

```bash
.trellis/guru-team/skills/packages/guru-establish-task-identity/scripts/invoke.sh \
  --root . --input - <<'JSON'
{"profile":"delivery_active_task","mode":"workflow","task_id":"example-recovery","task_ref":".trellis/tasks/08-15-example-recovery","lifecycle_generation":0}
JSON
```

Only the actual `identity_established` result continues. Identity reads the
restored workspace Task. Normal unbound Branch candidates instead validate the
Task in the candidate HEAD Git tree. Therefore an untracked restored directory
can pass Identity and still fail normal candidate qualification. Repeating
discovery does not restore the carrier. Do not introduce a commit requirement
to work around this difference.

## 4. Establish or reuse the original C4/C5 relationship

If both C4/C5 are already valid for the original lifecycle and selected branch,
reuse them and continue to Ensure. If normal HEAD candidates meet the original
contract, use `delivery_active_task` establishment. For the reviewed restored
workspace case, this owner performs its semantic Gate, then explicitly invokes
`delivery_restored_checkout`:

```bash
.trellis/guru-team/skills/packages/guru-establish-task-branch-binding/scripts/invoke.sh \
  --root . --input - <<'JSON'
{"profile":"delivery_restored_checkout","mode":"workflow","task_id":"example-recovery","task_ref":".trellis/tasks/08-15-example-recovery","lifecycle_generation":0,"branch_name":"dev","expected_head":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
JSON
```

The SHA is an example, not an expected result. Replace it with the actual
reviewed target HEAD. `--root` is that current registered checkout; the input
does not carry a persistent machine path, source commit, write list, judgment
or authorization.

The executor validates schema-2 active workspace identity, current registration,
actual branch/HEAD and the selected values. Both primary and linked checkouts
are supported. It does not inherit Creation's non-primary/non-base restriction.
Existing C4/C5 must agree on TaskId/generation, branch and revision. Another
Task's branch association, an unresolved resource incarnation or a conflicting
existing control stops; recovery never replaces it.

Only missing controls are established with the original transaction and
readback. When both are absent, the original initial revision is 0; when one
exists, its matching revision supplies the missing control. Matching controls
and existing ownership remain unchanged. New branch ownership is caller_owned;
new primary-worktree ownership is not_applicable, and new linked-worktree
ownership is caller_owned. No Task/Delivery file, session, gate or extra store
is written by this profile.

`binding_established` carries the original TaskKey to the original Ensure
consumer. Identity failures retain `invalid_task_state`; control/registration/
HEAD contradictions retain `blocked`. Normal discovery/recorder commands still
use `delivery_active_task/action=establish`; their enumeration and sorting do
not change. Do not read an intermediate receipt as a formal typed exit.

## 5. Ensure the checkout, then bind the receiving chat

Reinvoke the original Ensure owner after establishment:

```bash
.trellis/guru-team/skills/packages/guru-ensure-task-checkout/scripts/invoke.sh \
  --root . --input - <<'JSON'
{"profile":"delivery_active_task","mode":"workflow","task_id":"example-recovery","lifecycle_generation":0}
JSON
```

Require actual `checkout_resolved` for one current registered checkout. Then
the Bind owner reads this receiving chat's own current session and chooses its
original resume/rebind/switch/manual-recovery profile. A missing pointer uses
`delivery_rebind_missing_session`; a valid matching pointer uses
`delivery_resume_current_task`. A different or stale pointer follows its own
original preconditions and is not silently overwritten. A missing context key
uses the original explicit-task path with no session write.

Read [the Bind input/carrier contract](../../guru-bind-task-session/references/json-inputs.md),
complete its current semantic review and form its actual input/owner result.
For a missing pointer the public input has profile/mode, original TaskId,
generation and the caller's real continuation_id. Use the original invocation;
one parameter may be stdin, or both may be regular UTF-8 JSON files:

```bash
.trellis/guru-team/skills/packages/guru-bind-task-session/scripts/invoke.sh \
  --root . --input ./bind-input.json --owner-result ./bind-owner-result.json
```

These files contain the current Bind owner's actual reviewed objects, not
sample pass assertions or user authorization. Remove private temporary inputs
after their direct consumer completes. The result changes only the receiving
session pointer; it does not select a Delivery or supply a business gate.

## 6. Read the real continuation and report each result

From the resolved checkout, read the original public facts and workflow-owned
continuation:

```bash
python3 .trellis/scripts/task.py current --json
python3 .trellis/scripts/delivery.py current --json
python3 .trellis/scripts/get_context.py --mode continuation
```

Consume the actual key, phase, scope/root and missing obligations. A valid
same-Task selection remains selected. `no_current_delivery` goes to the real
continuation owner for its current obligation; it does not allocate an empty
Delivery. Files restored, baseline changed, branch associated and session bound
are separate results. None establishes Publication, Delivery, full_review,
readiness, Task Completion or Issue closure. Preserve the original historical
gaps and the verification layer actually observed.

## Lost output and ordinary failure

If establishment stdout is lost, first use the original read-only
`scripts/discover-candidates.sh` with `delivery_active_task/action=establish`.
Only `result.status=already_established` supplies the real `binding_ref`.
Copy its actual binding revision, retain the reviewed branch and unchanged
HEAD, and call the existing read-only result recovery:

```bash
.trellis/guru-team/skills/packages/guru-establish-task-branch-binding/scripts/recover-result.sh \
  --root . --input - <<'JSON'
{"profile":"delivery_active_task","mode":"workflow","action":"recover","task_id":"example-recovery","task_ref":".trellis/tasks/08-15-example-recovery","lifecycle_generation":0,"recovery":{"expected_revision":0,"expected_branch_name":"dev","expected_head":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}}
JSON
```

Use the actual revision and HEAD, not these example values. Recovery rereads
the exact existing result; it does not establish another association. An output
loss is not proof that mutation failed. Ordinary stale/identity/resource errors
return to their original owner and preserve the scene. The existing transaction
owns normal rollback; this profile adds no locks, crash protocol or retry ledger.

## Adoption and proof boundary

The new profile requires the complete matching Branch package/shared runtime,
schemas/Interface/examples and managed projections described by canonical
`trellis/presets/guru-team/MIGRATION-773.md`. Existing checkouts adopt through
the original `guru-upgrade-tools` owner with Task/session preservation; do not
hand-copy managed scripts or bypass ordinary install inventory checks.

New examples and schema acceptance are invocation guidance. The changed action
needs one deidentified representative carrier recovery that exercises the new
association and same-identity Bind, preserving historical gaps. Component,
installed, native Agent, remote and business effects remain distinct claims.
This contract does not require replaying a real historical chat, reoperating
the original business incident or a full multi-platform Release matrix.
