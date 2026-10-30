# 发现阶段 fitness 出口：D1 实施与验证计划

## 1. 输入与引用

读取根 PRD 的整体范围及 V5 责任、当前 slice PRD 和 design 全文，尤其 design 第3节唯一来源设计处置。当前独立 candidate_assessment 仅供方案写作，Wording-current final_plan 和 Approval 后才 Activation。必要规范和 canonical authority 按 design 第9节实际加载；这是首批，无历史 Delivery 可代替当前证据。

## 2. 有依赖顺序的步骤与文件责任

S1：实施 Agent 先读取 approved 三文档、official context 和规范。每次写入前执行 check-task-checkout-boundary。tests/test_contract.py 复用有效安装 fixture，先编写原失败组合、经正式 wrapper 重现 stdout schema_mismatch，保留首次结果。

S2：仅在 design 第4节指定三个 schema 的相应非 Planning Delivery stage 枚举增补 implementation_discovery。核对 interface 当前聚合和 consumer 引用，保留 id、required、字段、既有阶段及 return_route。不得改 runtime 来规避错误。

S3：执行 T1/T2/T3，检查同一 stdout 的身份/root/refs/route 保持和既有合法路径。通过后使用现有 apply --repo . 同步 dogfood/declared platform，并 reapply/drift/sidecar。canonical 是唯一源，不手改安装副本形成长期 patch。

S4：主会话协调独立 Architecture phase2 和原 Check 候选检查。candidate_checked 合法回 implementation；no-change final integration 不写共享文档，再绑定实际 candidate，最终 Architecture/Check 通过后 exact commit 和完整 committed Review。所有实际差额在同一源码 PR，以 Refs #690 保留 V5 整体验收。

## 3. 验证入口、输入与预期观察

T1/T2 对应 V1/V2，新增 package contract case 经 scripts/invoke.sh --invocation -，原失败边界前后对照和两种 route；同一 stdout 通过 design 第8节列出的实际/聚合/consumer schemas，字段相等。

T3 对应 V3，用受管 Python 执行 Architecture tests/test_contract.py 的完整 unittest suite；现有 Planning/phase2/final_integration/普通 stale 检查必须保持。若命令有环境错误，保留原结果并定位必要环境，不记通过。

T4 对应 V4，运行 .trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json 及 --mode installed --json；执行 trellis/presets/guru-team/scripts/bash/apply.sh --repo .，重入同命令验证 reapply，再执行 check-dogfood-overlay-drift.sh。运行 quality-guidelines 的 Python 内存 compile、JSON/shell 定向检查、task validate 和 git diff --check。检查受影响 package 的实际 bytes/mode、declared-platform 投影和零未处置 sidecar。完整多平台 Release、官方 upgrade/update 和业务现场不由这些定向结果证明。

## 4. 停止条件与适用回退点

身份/checkout 不一致停止原写入；合法输入在原失败边界之前失败时先修 fixture 普通遗漏，不能绕过 validator。当前问题或机制超出计划时返回候选事实，由原资格/Architecture/Author 处理。源码回归失败不发布；无关历史问题证明不相关后停止扩查，不擅修。

本批无业务数据迁移、部署或生产写入，因此没有对应回滚协议。源码可由 reviewed commit 回退；受管副本按 canonical apply 恢复，保留无关并行内容。Git/GitHub 副作用由原 owner 执行。

## 5. Delivery Policy（唯一）

policy=partial。本批独立切片为 V1–V4 的源码合同修复、回归与分发。完成条件是原合法发现阶段真实 wrapper 和公开 consumer 承接、两种回程及受影响既有路径保持、安装投影一致，再经标准质量与合并。上述条件不依赖 V5 已完成。

剩余责任为 V5：正式来源可安装后，由原业务 Architecture owner 沿业务仓自己的授权/发布流程采用，fresh 审核同条件并确认实际出口交还实施。Task Completion 仍检查这一整体要求；本批不宣称业务现场解除、reconcile 或部署成功，不关闭仍缺整体验收的来源。

## 6. Docs SSOT Plan（唯一）

strategy=no_docs_update_needed。本次补齐当前 package 已承诺阶段在 output/current consumer 的遗漏，精确 API 由 canonical package 单写；没有新增 requirement、owner、Architecture 决策、知识单元定义或导航关系。docs/requirements|design|test/current/knowledge-maintenance.md 和 Architecture distribution/change-contract 保持原适用含义。

原 RDT owner 在 candidate/final integration 判断真实 no-change；Architecture 独立评估当前候选。没有必要 delta 或 shared promotion target，不制造空 contribution/ADR。测试实际结果保留在当前执行证据与最终 PR，Task 三文档作为接受规划；后继 Completion 用公共 Delivery/Git/PR 事实和业务 V5 证据，不复制第二完成账本。
