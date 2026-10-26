# D3：README 正式归档恢复说明实施计划

## 1. 输入与引用

范围使用 [Task PRD](../../prd.md) 的 AC2/R3/R4，本批行为与验收使用 [D3 PRD](./prd.md)，唯一来源处置使用 [design第3节](./design.md#3-来源设计处置唯一)。B 为 `fad4f082231e5058c6f4d5f7ce5fc8c55e424937`，PR target 为 main；D1/D2 是历史已交付事实。

实施前读取 README 完整旧段、原 Reactivate Skill、canonical workflow 正常归档段和 MIGRATION-669，保留其关联条件。独立 candidate_assessment 已提供 no_architecture_impact；它不代替后续 Wording/final_plan/Approval。两轮独立 Review 与生命周期顺序只由 design 第9节集中定义。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、原 owner 与文件 | 可审核行为与完成观察 |
| --- | --- | --- |
| I1 | Planning 激活后；实施 owner；顶层 README 的原段 | 最小修正两句：补 Task2/指定正式 schema1，保留后继优先和原 operation recovery；原链接、人员/manual/unfinished/Finalizer 分流完整。 |
| I2 | I1 内容完整；原 Check/Review owners | 按第3节验证，并严格执行 design 第9节的当前双 Review 恢复路线；不写共享定义或空贡献。 |
| I3 | 两轮完整 Review 与正式质量结果实际成立；原交付和终态 owners | 原 Refs-only PR、expected-head merge 及整体准备收尾；后续精确新候选交原 Stage 2。 |

没有新增临时功能限制或待解除机制；不为本批制造迁移、禁用开关或后继清理责任。实施中保留他人改动，只处理 README、本 D3 规划及原 owner 正常生命周期写入。

## 3. 验证入口、输入与预期观察

| ID | 实际入口/输入 | 预期观察与证据范围 |
| --- | --- | --- |
| V1 | AI 完整对照 README 修改前后段落、原 Skill/workflow 及 design 第3节 | 满足 D3-AC1/2，包括合法后继继续、无后继才增代及全部旧状态限制；不以关键词计数代替语义判断。 |
| V2 | 检查本段 Markdown 链接目标为原 Reactivate Skill 且实际存在；`git diff --check`；`git diff --name-status B..H` 及当前 staged/unstaged/untracked 全范围 | 满足 D3-AC3；仅本段文案及正常 Task/D3 资料差额，无 code/runtime/Fork/API/schema/workflow/preset/其它 README 修改。 |
| V3 | `./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`；`./.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json`；source 入口分别用 `--platform-root .agents/skills`、`.codex/skills`、`.claude/skills`、`.cursor/skills`；四根私有 release Skill 的 SKILL/contract 字节比较 | 相关 source/installed/platform/docs 合同一致；先由原 Check 判定输入适用性，再执行或采纳未受影响的真实工程事实并说明来源。失败/缺项保留实际结果，不泛化为安装/原生/Release 通过。 |
| V4 | design 第9节所列当前原 candidate/final Check、两次完整独立 Review、readiness/Delivery 与收尾结果 | 每个结果覆盖各自完整候选；旧门禁、Draft 或 candidate_checked 不冒充正式 full_review/最终 Check。 |

不新增测试文件或字面镜像测试，不重复 heavy 安装矩阵。源码、安装、实际 Agent、业务与生产证据分层；本批只证明本次语义/静态边界。新的 Stage 2 候选仍执行原 release contract 的完整定向门禁。

## 4. 停止条件与适用回退点

文案丢失必要条件回原实施/Author；机制或 owner/接口扩张回原 Architecture/candidate assessment；真实 scope 变化回 Clarify。链接、diff 或相关机械验证失败时停止依赖门禁，修复后由原 owner 重判适用范围。普通等义措辞交原 Wording，不新增需求确认。

TaskCommit/Publish/Review/maintenance 的输出丢失恢复各自同一原操作；不造新身份、空提交或 pass。候选变化回受影响 Check/Review；原失败观察保留。没有业务数据、部署或迁移，因此不新增生产回滚协议；不覆盖并行文件或历史记录。

## 5. Delivery Policy（唯一）

Policy 为 full：D3 完整覆盖当前 AC2 中这次 README family 说明差额，没有计划延期项。完成条件为 D3-AC1–4 满足，design 第9节两轮完整独立 Review 与正式质量链实际成立，并由原 owners 完成交付。

这不是整个 Task 已完成的声明；整体 Completion 仍核跨代真实交付和必要证据。Stage 2 为 #656 的独立发布责任，#656 仍为 reference_only，不由本批 PR 关闭。

## 6. Docs SSOT Plan（唯一）

strategy 选择 `no_docs_update_needed`，其含义是本批无 RDT/Architecture 规范定义差额；README 本身正是当前需要修正的派生公开说明，由实施 owner 修改，不将此策略解释为不改 README。

命中 authority 与具体章节见 PRD 第7节：RDT-REQ-COMPLETION、RDT-DES-COMPLETION、RDT-TST-COMPLETION 已定义正式 family、后继优先及证据层次；ARCH-DOM-032/060、ARCH-INT-063 已定义原 owner/公共 operation/matching capability。原 RDT writer 和 Architecture owner 在 candidate_checked 后的原 final_integration 各自核真实无差额，直接 consumers 为原 Check、完整 Review 和后续 Delivery/Completion。无差额不创建 contribution、ADR、共享 promotion 或结果追记提交；发现真实差额即回原 writer/独立 gates，在最终 Phase 2 前收敛。历史正文保持原观察，不追写本次最终 pass、HEAD 或 Release 状态。
