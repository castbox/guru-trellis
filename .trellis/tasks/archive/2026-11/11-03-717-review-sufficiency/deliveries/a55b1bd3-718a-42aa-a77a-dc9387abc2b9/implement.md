# D1：实施、验证与交付安排

## 1. 输入与引用

已读取整体 `prd.md`、本批 `prd.md`、`design.md`；来源设计处置只由 design 第3节拥有。B 为 `404c841e9ca917b4680831aa0becd2e26d72fa0c`，没有前序 Delivery。实际 candidate_assessment 已由独立 Architecture owner 返回 `architecture_impact / target_native`；最终规划仍须经 Wording → final_plan → Approval → Activation。

必要规范是 installed Author `references/planning-body.md` 与三份 Delivery 模板、`.trellis/spec/workflow/{clear-technical-writing,workflow-contract,quality-guidelines,skill-package-contract,subtraction-first-compatibility,semantic-retrieval}.md`，preset 的 installer/upstream-ownership/overlay-guidelines，以及实际共同方法、十二消费者和现有 eval/分发测试。实施者先完整加载命中正文与关联条件，不能只读本列表。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、责任与文件 | 完成观察 |
| --- | --- | --- |
| I1 | Activation 后，原实施协调方核 checkout boundary；Trellis implement worker 读取实际三份规划与 JSONL。验收侧在现有 eval adapter/test 位置确定正常案例、具体问题与合法控制，期望只保留验收侧 | 案例/输入/预期先于任何实际旧新运行固定；未把期待 findings 注入 Agent |
| I2 | eval worker 从固定 B 取得完整旧 provider，复用原 native collector/原生产入口，执行首次 baseline；同时实施 worker 在 canonical spec/packages 准备共同规范与迁移 | 首次旧观察保留；没有因新方法改写旧结果。可并行，因为旧 provider 固定且隔离 |
| I3 | 实施 worker 拥有 `trellis/presets/guru-team/spec/workflow/review-sufficiency.md`、命中 workflow/quality/index 引用、十二 package 的 SKILL/references、薄 review-method、必要 README 和定向分发测试 | 按 design 第4节逐条迁出共同正文；原专题和阶段特例保留，公共 I/O/出口不变，无无效 wrapper/台账 |
| I4 | 原 RDT owner 准备 `docs/requirements-design-test-contributions/717-review-sufficiency/` 的完整 proposed 单元与关系；Author 准备真实 Architecture 贡献/必要 ADR。原 Architecture/RDT 审查这些隔离拟写内容 | 正文完整且可供 candidate Check，shared current 此时未变；共同规则正文不复制进项目知识 |
| I5 | 原 tools owner 使用完整本地候选源，仅同步本 checkout 的 Guru managed projections，保留 Task/session；执行命中分发/原 package 测试和 installed 验证 | 新 spec、package、声明平台实际可读，drift/sidecar 结果明确；无业务项目升级 |
| I6 | eval worker 在相同案例/模型配置/工具/权限/入口条件执行新侧；同一后继案例用真实 thread resume。验收方独立读首次报告与完整轨迹逐例评估 | V3 的遗漏、误报、早停、同类入口、未修复结束、缺口及后继承接都有实际判断；首次失败和限制保留 |
| I7 | 实施协调方汇总全部 tracked/untracked 候选并 begin_check；独立 Architecture phase2 → 原 candidate Check → 原 RDT/Architecture final_integration/读回 → 实际 candidate 重绑 begin_check → final Architecture/Check | 候选结果不冒充最终 passed；晋升后全部真实文件进入最终质量范围 |
| I8 | 主会话经原 TaskCommit、独立完整 B..H Branch Review、Delivery Review、Publish/Merge，再整体 Completion/Closure/Finish；精确资源由原 Cleanup 处理 | 每阶段有真实正式结果和 live GitHub 回读，PR 为 Refs-only，整体 Issue 由 Closure 决定 |

每次 source/test/task-artifact 写入前运行 `.trellis/guru-team/scripts/bash/check-task-checkout-boundary.sh --json --task .trellis/tasks/11-03-717-review-sufficiency`。并行 worker 拥有明确文件范围，保留他人改动。发现规划外候选只返回 ref、observed_behavior、locators、minimal_reproduction_hint，由原协调方准入后才实施。

## 3. 验证入口、输入与预期观察

- **V1 / AC1–AC2**：按 design 第4节迁移表核固定 B→候选和十二消费者，完整读取旧/新段落与必要未改依赖。扩展原 package contract/runtime 和受管投影测试，证明实际读取与旧依赖退出；不只断言关键词。必要命中测试由真实 diff 选取，不无因扩大为全仓历史套件。
- **V2 / AC5**：沿原 installer projection test fixture安装/reapply 新 spec 和命中 packages，实际读 installed/selected platform bytes，保留用户文件、无未解决 `.new/.bak`。最多一个代表 clean；不执行完整平台/Release 矩阵。
- **V3 / AC3–AC4**：在现有 `trellis/skills/guru-team/adapters/eval/` 或原 package tests 中扩展有界 native 行为采集，使用完整 old/new provider 和原公开 owner 入口。执行前的 case 集合见 design 第8节，具体 host-only expectations 只用于验收。`codex-cli 0.162.1` 已可用，multi_agent 已启用；保持实际默认模型配置，不覆盖模型来制造可比性。检查启动、完整结束、原入口/工具轨迹、实际 findings/结论及首次失败。原始结果保留于 repo 外 `/tmp` 下该次 eval 目录，验收摘要进入现有本批验证位置；不把 transcript 复制为运行时 ledger。
- **V4 / AC2、AC5**：`guru-upgrade-tools` 的 preview/prepare/invoke 在明确 checkout、source HEAD 和 local_candidate 下同步，实际 installed discovery/validation、`trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`、命中 reapply/平台投影核验。local_candidate 不证明 formal Fork source lock 或远程安装发布矩阵。
- **V5 / 全部 AC**：执行原质量规范的内存 Python syntax 检查及额外改动 eval Python、`python3 -m json.tool trellis/index.json`、必要 `bash -n`、`python3 .trellis/scripts/task.py validate <TaskRef>`、实际 installed discovery 和 `git diff --check`；然后按 I7/I8 取得原完整 Check/Review/Completion。机械结果不能代替真实模型行为或语义充分性。

报告分别说明 canonical/dogfood/installed、真实 Agent、机械检查和未验证完整安装/Release 边界。实际证据不足时保留具体未完成义务，不将其改称已完成或默认为外部依赖。

## 4. 停止条件与适用回退点

来源或整体 scope 真实变化回 Clarify；机制/职责变化回 Author/Architecture。新的规划外机制或测试先经过原 normal/solution/root qualification。真实执行问题由原 owner 调查，保留首次结果；外部必要证据缺失只阻塞依赖它的结论。保持合法阶段特例，不能通过缩小案例、预填判断、删除失败样本或注入纠偏使评测通过。

安装保留未知本地修改，sidecar 按原 owner 逐个解决；源/计划变化重新审查实际写集。没有数据库或业务部署回滚。源代码修订保持同一 Delivery，回最早受影响原 owner；不制造空提交或新切片绕过质量链。

## 5. Delivery Policy（唯一）

**full**。本批承担整体 AC1–AC5，包括共同源、全部固定消费者、旧定义迁出、真实旧新行为与分发验证，没有延后给未来 Delivery 的本项实施责任。独立可交付条件是这五项实际成立、公共边界保持、所有当前 finding 及原 Check/Review/readiness 条件满足。

不要求完整多平台 installer/Release Gate 或外部专业 Skill 已修改；这些是明确非目标。真实评测完成与 canonical 安装证据不可缺省。Delivery merge 不等于整体 Task 完成，由原 Completion 重新核整个 accepted scope 和真实结果。

## 6. Docs SSOT Plan（唯一）

**strategy=delta_first**。RDT state 为现有完整 authority。原 `guru-maintain-requirements-design-test-ssot` 是三层正文和必要导航的 writer，直接 consumers 为当前实施、Check/Review/Completion 及日常读取。依据根 Issue 和共同规范，准备本项 requirement/design/test 完整结果单元及必要关系，正文定位唯一共同源，不再复制审核规则。贡献根为 `docs/requirements-design-test-contributions/717-review-sufficiency/`；已有 knowledge-maintenance 单元的实际关系差额按原 owner 纳入，未变主题不复制。

Architecture 原 owner 拥有 `docs/architecture/contributions/717-review-sufficiency.md`、必要 ADR 与实际 current 边界的晋升。其完整 proposed targets 在当前实现候选中独立受审，候选 Check 后才 final_integration 写入，随后读回与重新绑定实际候选，完成 final Check、commit 和独立完整 Review。共享 README/index 仅在真实新 locator/关系需要时更新，不追加全仓版本或本 Issue 审核台账。

Canonical 共同 spec、Skill 和 README 是本次实现源码，依原受管分发同步；项目 `.trellis/spec` 为安装投影。Planning 不直接修改共享 current 或手工覆盖投影。历史 archives、旧测试失败、ADR 旧观察和不可变版本保持原样。验证案例输入和预期属于 eval 资产，实际执行证据在既有 eval 结果位置，最终摘要如实记未验证边界。
