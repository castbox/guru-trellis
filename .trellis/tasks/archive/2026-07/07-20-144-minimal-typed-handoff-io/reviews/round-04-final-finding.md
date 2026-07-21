# #144 Branch Review Round 4 最终放行审查原始报告

## 审查元数据

- 审查身份：`/root/issue_144_final_release_review_2`
- 逻辑角色：`最终放行审查代理`
- 复用决策：`new-agent`
- 审查 HEAD：`b758893506e7298cd237d3284cfeda6edf4d4e8d`
- 基线：`origin/main@cbd0396a2ddb7dd0efa613be7b7d93790eb2e34d`
- 范围：`origin/main...HEAD`，共 96 个文件
- 问题计数：P0=0，P1=0，P2=2，P3=0，`findings_count=2`
- 审查方式：只读；未修改文件，未运行 recorder、review gate、finish、push 或 PR 命令。

## 问题

### [P2] Workflow/structured-stop consumer contract 未强制 consumer-owned locator

`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:16193` 对 `json_schema` contract 仅以 `skills_root` 为边界加载；`trellis/skills/guru-team/schemas/skill-interface-1.3.schema.json:75` 也没有按 `consumer.kind` 约束 owner root。

正常复现：把 `workflow_completed_input` 的 contract 改为 producer 自身的 `packages/guru-example-action/schemas/action-completed-output.schema.json` 并同步 schema id，`validate_skill_source()` 仍返回 `status=passed, errors=[]`。

这允许 workflow 或 structured-stop consumer 复用 producer-owned output schema，违反 consumer 独立拥有 input contract 的要求。修复应分别强制 `consumers/workflow/**`、`consumers/stop/**`；`zero_payload` stop 保持现有语义，并补 producer-package locator 负例。

### [P2] Draft 2020-12 schema 只按未闭合的自定义关键字子集执行

`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15132` 接受 Draft 2020-12 方言，但 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15252` 的 custom validator 忽略 `patternProperties` 等标准关键字；新的 output example 正在 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:16147` 通过该函数验证。

正常复现：给 producer output 和直接 workflow consumer schema 同时加入合法但与 example 冲突的 `patternProperties`。标准 `Draft202012Validator` 判定 example 无效，当前 source validator 仍通过。

修复应使用开箱环境可保证的完整 Draft 2020-12 validator，或定义并递归校验闭合的受支持关键字 grammar，拒绝所有未实现或类型错误的关键字，并同步合同文档。

## 问题生命周期

- Round 1：4 个 P2。
- Round 2：3 个关闭，`F-BR-P2-001` reopened，并新增 `F-BR-P2-005`。
- Round 3：Round 2 两项、Round 1 其余项及 fresh Phase 2 的三项 finding 全部关闭，targeted closure tests 7/7 通过。
- 本报告的两个 P2 均为 Round 4 新发现，前序 closure 结论本身不回退。

## 需求/设计/实现承接

`prd.md` R5/R6 要求 output example 通过独立 schema，并由 consumer 独立拥有 input contract。`design.md` 4.4 明确 workflow/stop consumer-owned roots；`implement.md` 也要求 producer 只保存 locator。两个 finding 均属于 #144 current scope。

## Docs SSOT 与范围

Durable docs 对预期 ownership 的定义正确；当前缺口是实现和负例未完整承接。#144 只关闭自身；live #145、#146 均为 OPEN follow-up，不得关闭，也不得承接本轮两个 current-scope finding。

九个 production Skills 仍为 1.2 + `legacy`，fixture 未进入 production registry、inventory 或 mandatory route。

## 验证证据

- Skill package：106/106；installer：39/39；ownership：6/6；targeted closure：7/7。
- Phase 2 与 Round 3 shared runtime：548 passed、13 skipped、0 failure/error。本轮异步重跑已结束，但终端尾部未捕获，因此不将其冒充新的完整结果。
- Source validation：9 个 active 均为 1.2 legacy，0 个 production minimal。
- Installed validation：384 managed files，0 sidecar/removal/conflict。
- Dogfood drift、43 frozen/active overlays、13 managed claims、`git diff --check` 均通过。
- `.new`/`.bak` 为 0；canonical/installed runtime 与 1.3 schema 字节一致。
- 绿色回归不能覆盖上述两个正常 authoring 反例。

## Upgrade/Update/开箱即用

Public-sample clean throwaway 以 exit 0 覆盖 init、preview/switch、update、preset reapply 和 post-update 检查。默认 exact-ref 以 exit 2 fail closed，仅因分支尚未 push；这是发布前待补证据，不是实现失败。

尽管安装链路通过，当前 validator 仍会在新安装仓库接受两个不合规 package，因此不能据此宣称 #144 已满足开箱即用验收。

## 观察项

除未推送 exact feature ref 外，无新增非阻塞观察项。该远端验证应在 reviewed branch push 后由 Remote Marketplace Verification Gate 完成。

## 后续候选

#145、#146 保持既有迁移职责。本轮两个 finding 不应降级为 follow-up issue。

## 部署与安全

完整 diff 不涉及 CI/CD、container、K8s/Kustomize、数据库 migration 或 Makefile。未发现 token、secret、private key、`.env`、数据库 URL、签名 URL或客户数据泄漏。

## 结论

Round 4 阻塞。不得记录 passing Branch Review Gate，也不得进入 `trellis-finish-work`。

应返回实现修复两个 P2，重新执行完整 Phase 2，创建 finding-fix commit，完成问题闭环审查，再派发一个从未参与前序 review round 的全新最终放行审查身份。
