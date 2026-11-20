# Direct independent Issue review

Use this method in `guru-clarify-requirements:standalone_issue_requirements`
and `guru-review-change-request:standalone_issue_readiness`. Complete the
review asked for before the single checked invocation. If the user explicitly
asks to write back or start work, follow the applicable original operation
and its prerequisites.

## Read the current Issue first

Read the installed clear writing and review sufficiency specifications, then
the complete [Issue content specification](issue-content.md). Apply the
selected owner's requirements or readiness review criteria. For GitHub access,
follow the repository-bound CLI contract in
`.trellis/spec/workflow/workflow-contract.md#github-platform-io`.

Read the selected Issue's title, body, state and discussion. Keep the exact
JSON snapshot in call-local memory for the final check. For example, this
read targets Issue 17 in the example repository.

```bash
gh issue view 17 --repo example/project --json number,url,state,title,body,updatedAt,comments
```

Read the comments and any linked discussions that actually affect goals,
scope, prerequisites or acceptance. If the Issue and discussion answer the
review questions, proceed directly to the semantic gate. For a material gap,
name the evidence needed and read the closest source that can resolve it.
Before semantic retrieval, apply `.trellis/spec/workflow/semantic-retrieval.md`.
Use a fixed Git source and the existing original review or discovery entry when
its evidence is necessary, for example when related implementation has to be
compared across repositories or when the impact of conflicting sources cannot
be bounded. Keep its actual result and continue the independent review. The
direct final invocation requires only the reviewed Issue and the report.
Report an unresolved dependency or finding when the available evidence is
enough to describe it accurately. If the target cannot be identified or read,
use `blocked` and explain which prerequisite could not be verified.

## Re-review

Read current Issue content and effective discussion. Compare them with the
actual basis of the earlier conclusion. Check the current version of any
specific outside evidence that could change that conclusion. Carry forward
applicable coverage and findings from the current conversation. A comment
that leaves the source authority unchanged does not require repeating an
unaffected assessment. Recheck the parts affected by a substantive edit or
new evidence. If the earlier basis is unavailable, collect the minimum
evidence required for the current conclusion. If the impact cannot be bounded,
review the full affected scope. The current report identifies which prior
coverage still applies and which part needed new evidence.

## Invoke once after the semantic gate

In the completed review, provide the scope actually covered, the conclusion,
findings and remaining open items. Use the example as a shape. Replace the
repository, issue number, entire `issue_snapshot` and report with current
observations and your judgment. The wrapper re-reads this exact Issue once.
It validates objective facts before projecting the report to the user
response. The read-only result carries no intake authorization.

```bash
bash .trellis/guru-team/skills/packages/guru-clarify-requirements/scripts/invoke.sh --invocation - --json <<'JSON'
{
  "schema_version": "1.0",
  "public_input": {
    "profile": "standalone_issue_requirements",
    "mode": "standalone",
    "issue": {"repo_ref": "example/project", "number": 17}
  },
  "owner_context": {
    "issue_snapshot": {
      "number": 17,
      "url": "https://github.com/example/project/issues/17",
      "state": "OPEN",
      "title": "Write CSV output to stdout",
      "body": "Emit the selected rows as CSV on stdout. Verify the example with the documented CLI invocation.",
      "updatedAt": "2026-11-01T08:12:00Z",
      "comments": []
    }
  },
  "owner_result": {
    "typed_exit": "issue_reviewed",
    "report": {
      "coverage": ["当前正文中的输出行为、边界和验收说明。"],
      "conclusion": "正文描述了目标输出，验收条件仍需明确。",
      "findings": ["请明确输出列及顺序，以便核对实际 CSV。"],
      "open_items": ["确认验收示例的预期列及顺序。"]
    }
  }
}
JSON
```

For readiness, use the same envelope with
`profile=standalone_issue_readiness` and the installed command
`bash .trellis/guru-team/skills/packages/guru-review-change-request/scripts/invoke.sh --invocation - --json`.
Fill the report with the readiness judgment. For a semantic `blocked` outcome,
supply `owner_context={}` and `owner_result={"typed_exit":"blocked"}` and explain
the concrete blocker in the reply. For `issue_reviewed`, show the returned
report to the user, including any negative conclusion.

If invocation fails, use its code, field and remediation to identify the
failed step. If the snapshot changed, reread the Issue and reassess the
affected parts before invoking the same profile. Fix a parameter error in
this invocation. Reuse still applicable evidence. If GitHub access fails,
restore it and reread the same Issue before continuing. Read-only execution
never posts comments or creates an Issue, Task or branch.
