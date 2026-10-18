# D1 发布准备实施与验证计划

## 1. 输入与引用

整体 Task 根 prd.md R1–R6/AC1–AC6；本批 prd.md DR1–DR5/DAC1–DAC5；本批 design 第3节为唯一来源设计处置。已读 Issue #626 与 release contract Two-Stage Lifecycle、RDT 三层 knowledge-maintenance 完整单元、Architecture FOUNDATION/current/change-contract、当前 manifest/source lock 和 maintenance package。首次 D1，输入为 B=33f18a768c9c8d901f34b899934ac40c3d97cc5b；没有前序已交付结果。

## 2. 有依赖顺序的步骤与文件责任

- I1（Activation 后）：实施 Agent 只负责 canonical extension .5、maintenance target/const/consumer/示例/现有测试，以及三公开 README和public-docs。逐文件读取后改动，固定 Fork lock不变；不编辑生成投影或知识 authority。
- I2（原知识 owner）：Architecture 建立 .7.0-guru.102/predecessor .101 的 identity 后继；RDT 读取公开 Architecture locator/version/status 后，建立三层 .7.0-guru.111/predecessor .110，切换必要导航。保留旧版本页、current完整定义、历史Git关系与未迁移入口；执行窄 direct sync判断与正式输出。
- I3（I1/I2 完成）：主会话串行执行 canonical apply 同步 Claude/Codex/Cursor，审查受管变更和sidecar，运行 source/installed/平台、ownership与drift。维护 runtime/schema tests和V5定向tests完成。
- I4：fresh独立 Phase2 Architecture评估最终完整候选与知识写入；原 Check检查全部accepted scope，TaskCommit创建精确提交，再做fresh committed Architecture与完整 Branch Review。
- I5：原 Delivery Review/Publish/Merge 创建中文 Refs-only PR；整体 Completion与reference_only Closure后正常 Finish archive/bookkeeping，资源清理仅处理本任务明确拥有对象。原release caller继续Stage2。

每项产物都是实际源码/文档或原owner最小结果；不生成动态发布清单、tracked gate状态或授权记录。

## 3. 验证入口、输入与预期观察

- V1：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-upgrade-installation/tests`，再对 guru-upgrade-tools/tests 执行同入口；以实际 target .5 验证原维护行为和output契约（DAC1）。
- V2：全文审核三个 README/public-docs，核对 .4 live tag peeled commit 855f236850714edc4b78169218c09568c823f336、source lock和成功CI 39043542548；观察 .4稳定/.5准备/历史边界（DAC2）。
- V3：原知识owner语义审查新版本/导航/关系与历史diff；校验新页面的Markdown本地引用和三层一致性，观察 .111/.102、前驱可读及不变完整单元（DAC3）。
- V4：source/installed `check-skill-packages.sh --root . --mode ... --json`，source再逐个指定 `.agents/skills`、`.codex/skills`、`.claude/skills`、`.cursor/skills`；`check-upstream-ownership.sh --repo . --json`；`apply.sh --repo . --platform claude --platform codex --platform cursor`；`check-dogfood-overlay-drift.sh --repo .`，观察完整受管一致（DAC4）。
- V5：preset scripts/python 的 `test_issue_content_distribution.py`、`test_planning_body_distribution.py`、`test_bytecode_hygiene.py` 现有 unittest；`git diff --check` 与递归 bytecode/.new/.bak检查，观察无本批引入回归或残留（DAC4）。
- V6：原Check/TaskCommit/full Review/Delivery/Completion/Finish入口绑定最终bytes和实际Git/GitHub事实；观察准备任务完整交付归档，#626仍OPEN（DAC5）。

上述均为预期，实施后记录实际结果。Stage2的精确SHA安装、前驱existing升级、真实scanner、tag smoke和Release外部结果不由本批测试替代；完整累计矩阵、真实业务和生产保持未验证。

## 4. 停止条件与适用回退点

版本轴/Knowledge source不一致回原writer；真实source/范围/机制变化回Clarify/Author/Architecture；测试失败先定位受影响行为，不移除合法输入制造绿色。未知本地修改保留，通过原installer处理sidecar。执行分支上的未提交更改可在原owner确认后按精确路径恢复；历史tag/归档不可改写。本批没有DB/部署迁移，不构造生产回滚机制。普通输出丢失用原owner同操作恢复，不重复远端副作用。

## 5. Delivery Policy（唯一）

策略为 full。D1完整覆盖准备Task R1–R6/AC1–AC6，不延期准备义务。独立交付条件为版本/维护/公开文档/内部知识一致、投影与定向检查完成、完整Check和Review无开放finding。Delivery合并仍需原Task Completion/Closure/Finish；Stage2由#626及原release caller负责，不属于本Task accepted scope，不以准备合并证明Release已完成。

## 6. Docs SSOT Plan（唯一）

strategy=ssot_first。公开版本单写于canonical manifest/三README与public-docs；原Architecture maintenance writer负责current identity .102与关系，原RDT maintenance writer负责三层 .111和navigation，直接consumer为新知识读者、Check/Review及release caller。当前完整知识行为不变，历史版本页和#331 trace保留。适用authority为阶段原.101/.110；先由原owner窄direct sync并核对实际写入，再最终Phase2/Check/committed Review。无架构行为变化不新增contribution/ADR；若出现真实promotion，按design第3节返回原assessment和晋升流程。
