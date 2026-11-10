# D1：实施与验证计划

## 1. 输入与引用

实际输入为 [整体 PRD](../../prd.md)、[本片 PRD](prd.md) 和 [设计](design.md)。规范性来源设计处置只在 design 第3节维护。实施前加载原 Clarify/Author 完整合同、现有 Creation/阶段接续、workflow-contract 的 Interaction Budget 与 Candidate Applicability、quality-guidelines 的 Test And Validation Value 与 Validation Scope Ownership。

原安装 owner 是完整源 `guru-upgrade-tools`，其 Skill/contract 拥有 preview/prepare/写入/恢复。公共 package/平台/受管副本职责见 `.trellis/spec/workflow/skill-package-contract.md` 与 preset ownership/installer 规范。固定 B 与 main target 见 design 第1节；这是首片，不读取不存在的前序交付结果。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、owner 与文件 | 具体动作与完成观察 |
| --- | --- | --- |
| I1 Clarify 方法 | 当前计划激活；实施 owner 修改 canonical Clarify `references/contract.md` | 在当前 Delivery scope revision 中加入 design §4/§6 的新增差额判断，保留整体范围发布和原交互边界；当前源读后能分辨 S1/S2/S3 |
| I2 Author 承接 | I1；同一实施 owner 修改 canonical Author `references/authoring.md` | 修改唯一 Policy 段和 implementing scope-revision 的解释，明确独立后置、必要当前片刷新、剩余责任和旧片失效；保留原 rework/stop/Candidate 合同 |
| I3 现有合同与 package 检查 | I1–I2；原实施/Check owner | 执行 V1/V2；不新增自动分类器、schema 或自证测试；发现真实差额回受影响原 owner |
| I4 受管投影同步 | I3，完整源和原 tools plan 已准备；`guru-upgrade-tools` | 在此 worktree 按精确源/写集和原写入边界同步 installed 与现有平台投影，核 Task/session/peers 保持及 sidecar；不手工复制 |
| I5 最终检查与交付准备 | I4；原实施、Architecture、Check、Commit、Branch Review、Delivery Review/Publish | 覆盖完整候选及必要未改 consumer，执行 V3/V4；原 final integration 无知识差额不造文件；实际 commit/PR 各保原边界，发布后停止等待协调器 |

不修改 workflow 内部流程、脚本、schema、配置或测试行为。若实际证据表明这些对象出现本片必需差额，先回原 Author/Architecture，不在实施中静默扩大。

## 3. 验证入口、输入与预期观察

V1：原审核 owner 对实际两处合同逐项检查 PRD S1/S2/S3、R1–R3 和 design §3；同时读未改的 Creation、Approval、Delivery Review 和 workflow 接续。预期明确区分三条正常路线，保留原 owner 和完整范围，无固定新增问答。

V2：从仓库根运行现有两包 contract tests，使用受管解释器和 canonical PYTHONPATH；分别选择 `trellis/skills/guru-team/packages/guru-clarify-requirements/tests`、`guru-author-task-plan/tests` 的 `test_contract.py`。运行：

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=trellis/skills/guru-team .trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/packages/guru-clarify-requirements/tests -p test_contract.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=trellis/skills/guru-team .trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/packages/guru-author-task-plan/tests -p test_contract.py
bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
```

预期原 schema/consumer 合同和完整 package inventory 有效。它们只证明确定性合同层，不替代 V1。没有新增 runtime 行为，故不新增重复长期回归或混合 Git 场景。

V3：原 tools owner 完成精确同步后运行 installed package validator 和 `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .`，核受影响 package 的 `.trellis/guru-team/skills/packages`、共享 `.agents/skills`、Claude、Cursor 与既有 manifest 声明一致；Codex 使用共享根。按实际同步差额处理 `.new/.bak`、mode 和本聊天 session/current，确认 peer/common 状态保持。无新增 clean throwaway 或多平台矩阵。

V4：官方 `task.py validate <TaskRef>`、实际 Delivery manifests 和 `git diff --check`；验证本次 curated context 足够、文件真实存在、内容仅在选定范围。按仓库必需的 source syntax/入口一致性检查补命中项；无 Python 修改不据此扩张新运行场景。

V1–V4 尚未执行完毕。确定性、installed、真实 Agent 和远端结果分别报告；证据充分后停止无新信息重跑。

## 4. 停止条件与适用回退点

来源/范围或真实交付时序变化回 Clarify；机制/owner 变化回 Author 和 Architecture；同步未完事务、源不匹配、权限或 sidecar 冲突回 `guru-upgrade-tools`。恢复原 operation，不换 checkpoint 或手写 pass。局部失败只阻塞依赖部分，不转成 #734/#765 工作。

本地文字修订保留原当前文件和并行改动；不通过 reset/revert 清理其它执行者。此片无数据库或部署副作用，不新增数据回滚协议。commit、push/PR、merge 各自保原操作边界；本节点不执行 merge。发现测试失败先界定是否到达命中行为，按真实缺口补证，不以重复绿色或数量代替覆盖。

## 5. Delivery Policy（唯一）

策略：full。本片当前范围完整覆盖整体 R1–R3 与 AC1–AC3，交付物是两处原 owner 合同及实际受管分发。独立交付条件是三场景语义和职责一致、必要 package/投影/drift 检查完成，以及原最终 Check/独立审核/readiness 覆盖实际内容。

计划内没有留给后继的 #778 实现责任；未执行验证仍是当前片义务，不能当作已完成。Task Completion 还须核全量要求和真实交付事实。本片 full 只表示当前选定覆盖，不能把未来所有 Task 新要求自动纳入此片；新增差额仍回原 Clarify 判断。没有人为新增临时产品限制。

## 6. Docs SSOT Plan（唯一）

策略：no_docs_update_needed，限定于共享 RDT/Architecture 正文。当前 RDT 的 `task-delivery-lifecycle.md` 已定义 Task 整体责任与 Delivery 独立切片、原 Clarify/Author/阶段/Creation 分工、固定内容范围与 Policy；`requirement-decisions.md` 已定义真实选择与具体委托。此次只在原 step-local SSOT 细化已有归属方法，没有新的公共状态、API、owner、持久化或生命周期能力，故不复制规则到共享 current、README、全局索引或额外 contribution。

实际 durable 差额由原 Clarify/Author canonical references 拥有，installed 和平台 Agent 是直接 consumer；原 tools owner 完成投影。原 RDT/Architecture 在后续阶段核这项 no-change 判断，若实际实现导致当前知识义务变化，回原 writer 准备真实隔离贡献，经 candidate Check/final integration 后才能写共享 current。当前候选 Architecture 已判断 no_architecture_impact，因此无空 contribution/ADR，最终阶段仍亲自核实际差额。

上述策略不免除源码合同、规划正文、必要上下文与投影维护，也不把 planned checks 或 source parity 写成真实 Agent/业务效果。
