# Issue #105 Round 27 问题闭环审查报告

## Findings

### [P1] 最新修复提交不满足强制 commit message 合同

- reviewed HEAD：`1643a8c3424801fc9c302719dc45fd3ce2717148`
- 实际 subject：`fix(finish-work): 统一大小写仓库的 PR URL 合同`
- 固定合同要求 `{type}({scope}): #{primary_issue} 中文描述`：`.trellis/spec/workflow/workflow-contract.md:165`。
- 当前 validator 明确返回 `kind=invalid`，错误为 subject 缺少 `#105`：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:7811`。
- Phase 2 artifact 的 `commit messages 16/16` 只覆盖提交前旧历史；当前分支已有 17 个提交，不能证明最新提交合规。

影响：Branch Review Gate 明确要求审查当前完整提交历史，当前 HEAD 无法通过 `check-commit-messages`，不得记录 gate pass。

建议：仅改写该提交 subject 为 `fix(finish-work): #105 统一大小写仓库的 PR URL 合同`，保持 tree 不变；随后重新执行 post-commit message check，并由本 finding owner 做 closure。

## Round 26 Finding

Round 26 mixed-case repo P2：`closed`

- 新增唯一 `parse_canonical_pull_request_url()`。
- 仅接受 HTTPS GitHub owner/repo/pull/positive-number。
- repo identity 使用 casefold，输出保留合法 remote casing。
- final projection、incomplete recovery、exact recovery 均复用同一 parser。
- 错误 transport/repo/percent encoding/path/query/fragment/zero/leading-zero/5000 位数字均统一抛出 `WorkflowError`。
- `microsoft/PowerToys` final、fresh recovery 与 installed closeout 均通过。

Phase 2 的超长纯数字裸 `ValueError`：`closed`。

## 验证证据

- focused parser：`3/3`
- manual matrix：`1 valid + 15 invalid`
- canonical full：`426/426`
- preset：`36/36`
- public-sample throwaway initial #105 / update #106：通过 mixed-case URL、ready、clean、fresh binding、三方 HEAD
- compile、diff check、overlay drift、canonical/dogfood equality：通过
- Phase 2 的 14 个 dirty paths 与最新提交文件集合一致

未修改 resolver、symlink、schema、平台入口、CI/CD、容器、K8s、Helm、migration 或 Makefile。Docs SSOT 对 mixed-case/parser 行为已同步；安全与部署检查无新增问题。

## 结论

- reviewed_head：`1643a8c3424801fc9c302719dc45fd3ce2717148`
- reuse_decision：`reuse-for-closure`
- P0：`0`
- P1：`1`
- P2：`0`
- P3：`0`
- findings_count：`1`
- 结论：`FAIL，Round 27 closure 被 commit message contract 阻塞`

残余风险：current-branch remote marketplace 与真实 GitHub E2E 未验证；`v0.6.5-guru.3` 不存在。
