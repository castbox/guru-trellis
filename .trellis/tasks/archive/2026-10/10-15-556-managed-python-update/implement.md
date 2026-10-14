# #556 执行与验证

## Delivery Policy

policy=full：一个业务 Delivery 交付 PRD R556-01..07 的全部 accepted installer/runtime 行为、测试与使用文档。没有隐藏剩余业务 slice；whole-task Completion 负责整体 scope 与实际证据判断。完整 Python-minor、多平台/Release 矩阵、业务升级和源仓整体旧模型迁移均为非本次验收范围，不能写成 PASS。

## Docs SSOT Plan

strategy=delta_first。原 guru-maintain-requirements-design-test-ssot 拥有唯一 contribution：docs/requirements-design-test-contributions/556-managed-python-update/{manifest.yaml,requirements.md,design.md,test.md,traceability.md}。test.md 单写真实运行结果、first failure、fixture-only、skipped 和未验证边界；task 文档不复制结果链。Final Phase2 前由原 owner 完成 task_delta_reconciliation。首次独立完整 committed Branch Review 后，只有原 RDT owner 按 live expected authority 决定并执行必要 shared promotion，晋升差额重新进入 Phase2/commit/不同 reviewer 完整 review。Architecture no-impact 不制造 contribution/ADR/promotion。

## 实施顺序

1. 完成 Author → candidate Architecture → Author solution → Wording → final_plan Architecture → Approval，展示当前三份规划后等待本次计划接受，再由原 Activation 进入实施。工程 Task 使用完整旧 dogfood；canonical 产品新模型只在独立完整 matching install 验证，不拼接 DTO。
2. 先补聚焦行为回归：默认 PATH 与显式选择，真实未枚举3.15 identity admission；其它 minor 的选择测试明确为 fixture，不声称兼容性矩阵。相同有效 identity reuse、minor identity 变化、patch/path 不参与 identity。
3. 改原 bootstrap/manifest 和 apply 选择/诊断；按 design D556-03 在原 candidate 提交前运行公开 wrapper schema check，旧环境与 pointer 在依赖/检查失败时保持。复用现有 cache/repair，不建立新更新器。
4. 将 installer managed Python plumbing 作最小模块提取，调整其传递解释器与必要受控 managed caller。原 installer 其它事务/ownership 行为保持；新增 helper 注册原 inventory。测试证明普通 apply 与受控 explicit runner 均正确。
5. 更新 executable 使用/排障文档、canonical preset spec 与唯一 RDT trace。同步独立 complete current installed 样本的 managed runtime/package/平台投影；不修改业务仓、系统 Python 或旧源仓安装模型。
6. 运行下表验证；失败按 first failure 记录并修正本任务问题；缺真实依赖/CLI/API 环境时保持 SKIP/blocked，由 Check/Completion 判断 accepted scope 是否仍可完成，不自动豁免。
7. 原 RDT reconciliation、fresh independent Architecture phase2 与完整 semantic Check → exact Task Commit → fresh 不同 reviewer Architecture + 完整 origin/main...HEAD Branch Review。必要 promotion 后重走原 gates。
8. 原 PR readiness → Refs-only Publication → Delivery merge → whole-task Completion → Closure → Finish bookkeeping → 精确资源 Cleanup。各真实 Git/GitHub 副作用分别展示当时精确目标后承接当前对话确认；规划接受不授权 commit/push/merge/cleanup。

## 聚焦验证与判据

| 验证 | 必须观察的行为 | 证据层 |
| --- | --- | --- |
| Interpreter selection | 默认读取当前 PATH python3；--python 优先；不存在/不可执行/非3无回退，诊断可操作 | 执行选择入口 + isolated fixture；非真实 interpreter 明示 |
| Identity admission/cache | 实际3.15不再被allowlist拒绝；既有identity字段不变、same valid reused；minor变化，patch/path无需rebuild | 实际只读identity + 定向runtime tests；不外推minor兼容 |
| Dependency/public runtime失败 | 依赖安装失败和真实wrapper检查失败分别停止；已有pointer bytes及旧环境内容/mode保持，候选可清理 | 可控故障fixture调用真实公开路径；不冒充网络/生产事故 |
| Runtime capability | locked依赖probe、Draft202012关键行为及真实schema-bound public wrapper正/普通错误路径 | 真实managed interpreter/公开wrapper |
| One current clean/reapply | 具备当前API1/Task2/Plan2的固定matching CLI，PATH Python无jsonschema，完整canonical preset安装；显式reapply可复用并通过wrapper，bytes/modes、sidecar收敛 | 一个真实临时installed样本；fixture任务语义与正式发布分列 |
| Regressions | 原runtime/cache/repair/resolver与installer事务相关回归；必要受控managed caller路由定向检查 | 真实product tests；既有未触及矩阵不重跑 |
| Projection/drift | canonical source校验、完整installed投影/声明平台descriptor、定向reapply/modes和sidecar；source旧dogfood reapply/drift如实记录 | current样本PASS与旧载体拒绝不可混用 |
| Static/context | shell语法、相关Python编译、JSON、task context validate、whitespace及触及代码3000行审查 | 静态证据，不替代semantic Check |

实际结果、first failure、fixture与未验证边界只由[本次唯一Test](../../../docs/requirements-design-test-contributions/556-managed-python-update/test.md)拥有；本计划不复制执行结果。

## 精确范围与禁止项

改动集中在canonical runtime、preset apply及其最小helper/原inventory、相关测试/harness、必要受控调用方和使用/排障文档。source旧dogfood本任务载体必须完整保留；source reapply的migration-required边界不自动修复。不改系统Python/Homebrew，不自动删旧cache，不升级业务仓，不动backend #148、#149/PR #526或其资源，不开始#557，不发软件Release。
