# D1 实施与验证计划

## 1. 输入与引用

先读 [本批 PRD](prd.md)、[整体 PRD](../../prd.md) 和 [design 第3节](design.md#3-来源设计处置唯一)。实际来源为完整 Issue #766；source design 处置只由 design 第3节维护。

实施及 Check 读取安装的 planning-body、三份 Delivery 模板、clear-technical-writing、companion-scripts、quality-guidelines 的测试价值/范围/内存语法检查，以及 workflow 的 Candidate Applicability And Coverage。基线为 main@8d97fe540，无前序输入。

## 2. 有依赖顺序的步骤与文件责任

1. P1：实施 Agent 读取当前源和引用使用，核实原错误树与固定出口声明；先补真实 Author schema 回归到 `trellis/skills/guru-team/runtime/tests/test_public_contract_diagnostics.py`。观察 production validate_json 的拒绝及定位，确认用例触达原缺口。
2. P2：同 Agent 修改 `trellis/skills/guru-team/runtime/schema.py` 的共享诊断选择，复用原字段解释与实际引用上下文。只处理本方案，不改 schema/入口接线或新增推断框架。
3. P3：运行 V1/V2 及受影响基础检查。新增或扩大机制先回原 qualification/Architecture，不能通过测试扩张范围。
4. P4：由完整源 guru-upgrade-tools 同步该工作树的受管 runtime/manifest，保留 Task/session 与 peer；检查 source/installed、drift、sidecar。原 owner 处理冲突，无手工拷贝或 hash 修补。
5. P5：完整 candidate 绑定后进入原 Architecture phase2、Check、精确 commit、独立完整 B..H Review、Delivery Review 和实际 PR 交付。整体 Completion/Closure/Finish 保持原职责。

每次写入前执行 `check-task-checkout-boundary.sh --json --task .trellis/tasks/11-09-766-union-exit-diagnostic`。只写本批文件，不覆盖并行改动。

## 3. 验证入口、输入与预期观察

- V1/V2：用本 checkout 的 `.trellis/guru-team/runtime/resolve-python.sh`（参数按其现有入口）运行 `python -m unittest` 的共享 `test_public_contract_diagnostics.py`。真实 scope 输出加 mode 失败位置准确、删 mode 成功；原歧义/缺失/不回显回归通过。若改动触及分支选择之外的共享 runtime helper，运行该 helper 的既有回归；其余 package eval 不进入本批验证。
- V3：原 `check-skill-packages.sh --json --mode source`、`--mode installed`、`check-dogfood-overlay-drift.sh`，核实际安装无 unresolved sidecar。tools owner 自身的 postvalidation 及 Task/session 保留证据不得被源码通过替代。
- V4：执行 quality-guidelines 的内存 compile 全 Guru Python recipe，`bash -n` workflow/preset Bash、`python3 -m json.tool trellis/index.json`、`task.py validate` 和 `git diff --check`。

V1 是直接生产模块层回归；未改 Author 接线时不构造业务生命周期。未验证外部升级、clean install、完整声明平台矩阵、native 链及生产效果。测试结果在执行后记录，不预填 pass。

## 4. 停止条件与适用回退点

身份或 checkout 边界失败时停止写入，交原 Identity/Ensure/Bind owner。需求或 scope 变化回 Clarify；实现机制超出候选回原 qualification/Architecture。必要测试失败时调查并修复本范围，无法归因时保留真实缺口，不改断言制造通过。

受管写入失败回原 tools transaction 恢复，不重复 prepare 或覆盖备份。无业务数据迁移，故无需数据回滚；Git/GitHub 副作用按各原 owner 的计划执行。证据覆盖全部 AC 且受影响检查通过后停止追加可选验证；设施反复失败时重新评估复现层级，缺口不能当通过。

## 5. Delivery Policy（唯一）

采用 full：D1 完整覆盖 R1–R5/AC1–AC3，没有功能延期或后继切片。独立可交付条件是共享修复、真实生产 schema 回归、原诊断回归及受影响投影均具备证据，并完成原交付审核与 PR 合并。原 Task Completion owner 继续负责全部 accepted scope 和实际 Delivery 事实；Delivery 合并不替代 Completion。

## 6. Docs SSOT Plan（唯一）

strategy=`no_docs_update_needed`。本次细化既有 schema 校验失败的字段选择，保持所有 public schemas、错误 envelope、成功 DTO、workflow 及 owner 合同。精确 schema/字段语义已有 canonical schema.py/public schemas 和生产回归直接拥有；不创建 Issue 专属第二 current 定义。

已读取 RDT current 的 local-fix-intake requirements/design/test 单元，其诊断范围是 Discovery 私有绑定比较，与本次共享 union 选择不同，不能借此扩写。Architecture candidate 已判无影响，无 contribution/ADR。原 RDT owner 在 Phase2 核该 no-change 决策，直接 consumer 为 Check/Branch Review；若实现引入真实持久合同变化，回 Author/RDT 制作隔离候选，经原 candidate Check/final_integration 后晋升。现有规范、指南和导航没有因本次解除而失效的临时限制。
