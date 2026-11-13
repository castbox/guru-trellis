# #818 D1 实施与验证计划

## 1. 输入与引用

先读 Task 整体 [PRD](../../prd.md)、本批 [PRD](./prd.md)、[design](./design.md)第1–9节及第3节唯一来源设计处置。整体公共 accepted_scope 与 D1 scope_ref 保持；开发 B 为 `fd0ee32618433a92ae934e29afb5b72e7136b4f7`，没有前序 Delivery。

实施上下文实际加载：安装的 `clear-technical-writing.md`、`review-sufficiency.md`、共享 `planning-body.md`、本批三个模板；canonical `issue-content.md`、四原 owner 和必要合同；质量规范的 Test And Validation Value、Validation Scope Ownership；原 tools 和 RDT maintenance 合同及 shared current-knowledge。来源角色和外仓方法边界按整体 PRD 第1节，不把引用列表当作已经读取。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、原 owner 与写集 | 完成观察 |
| --- | --- | --- |
| I1 旧入口观察 | 规划接受/Activation 后，由实施 owner 通过现有原生 Agent 和原 Issue 写作/审核入口执行 design V1/V2 的旧安装输入。复用现有示例，保持侧效应为空。 | 得到首轮真实输出及覆盖边界，不能把旧版未失败误写成已复现代码缺陷。 |
| I2 原正文收敛 | 原内容写作职责修改 `trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md` 的原完整段落；按 design 第4节统一必要性、派生义务、规则组织和验收。 | 旧的分散/过强表述已退出；来源保留、真实保护和适配未丢失。没有新 ledger、DTO 或脚本判断。 |
| I3 消费者与共同引用 | 同步四原 `SKILL.md` 和三个原合同的薄引用；共同 `trellis/presets/guru-team/spec/workflow/review-sufficiency.md` 只定位 Issue 原规范。沿原 owner 判断实际必要差额，未受影响文字保留。 | 四入口各在原职责调用同一完整正文；没有第二完整规则或新流程节点。 |
| I4 新输出与定向分发 | 复用 V1/V2 输入观察新行为；执行 V3。只补真实分发缺口，不新增文本关键词断言来证明语义。 | 分别得到实际 Agent 输出和分发层结果；保留原始失败、修订及未验证项。 |
| I5 受管采用 | 原 `guru-upgrade-tools` 从完整候选 source 对本正式 checkout 做 preview → AI 逐路径审查 → prepare → invoke/readback，并按原 owner 同操作 reapply。写集限其 reviewed managed projections、manifest 和必要自身 runtime。 | Task/session、配置、用户内容和 peer 保持；明确 `.new`/`.bak` 处置，完成 V4。普通 apply 和手工覆盖不作 fallback。 |
| I6 RDT 差额与整合 | 原 RDT owner 在 `docs/requirements-design-test-contributions/818-issue-minimal-sufficiency/` 准备必要完整 proposed targets 和追踪；按 design 第9节维护本能力当前 R/D/T 正文。 | 以真实 V1–V4 证据写 Test，当前能力与历史边界清楚，完整定义有直接消费者。 |
| I7 提交前门禁 | 按原 Phase 2 完成工程自检与知识 final_integration/readback。此后才展示精确 stage/commit 计划，处理该独立副作用边界。 | 全部真实 after 纳入后续候选；提交后一次独立完整 Review 判断质量与知识整合。未满足提交前门禁不进入提交。 |

每个写批次先通过本 Task 的 fresh checkout boundary。只写本 Task、其本批规划和获准实现范围，不动其它 Task、primary 或 peer。实现中出现新增范围/机制时回最早受影响原 owner；不靠增加切片掩盖未完成责任。

## 3. 验证入口、输入与预期观察

- **V1/V2：**通过原 `guru-clarify-requirements`、`guru-review-contract-wording`、`guru-review-change-request` 及 Create Issue 创建前语义门禁执行 design 第8节的等价请求。被测原生 Agent 只取得实际请求、来源和原入口合同，不注入本 Task 的预期 Findings。实施 owner 比较完整输出，核原始目标、必要保护、真实入口和派生义务。只读审核及 draft 保持无外部写入；未执行的正式外部操作如实列出。
- **V3：**从实际锁定 Fork CLI 包中解析并验证 `GURU_UPSTREAM_DELIVERY_SCRIPTS`，确认 `common/delivery_schema.py` 及其所属 package/version，再执行：

  ```bash
  python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_issue_content_distribution.py
  python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_review_sufficiency_distribution.py
  ```

  第二条只在共同规范确有本批差额时执行。使用 fixture 已有原 writer 和 reapply，核受影响所有声明投影/链接、保留用户文件和 sidecar。fixture 模拟的 managed Python 环境只服务分发观察，不宣称完整 CLI 安装或 native 行为。
- **V4：**原 tools owner 先读取 `trellis/presets/guru-team/source/trellis-source.json`，当前锁为 `castbox/Trellis@e3793251fad8bd261d0c370d408c7675b9f6a140 / 0.7.0-castbox.6`。核真实匹配 CLI/Core 根、maintenance API 和未完成同操作，再执行其完整工具合同。安装完成及同源 reapply 后执行：

  ```bash
  bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
  bash .trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json
  bash trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
  bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
  python3 .trellis/scripts/get_context.py --mode continuation
  git diff --check
  ```

  V4 证明范围限本 checkout、受影响 managed closure 和实际声明投影，不外推其它平台 Agent 行为、正式 source_locked、软件发布或业务仓采用。

按依赖顺序先旧入口、正文差额、新输出/分发，再实际受管采用和必要新安装入口复核。沿现有 Test 记录真正的输入、观察、首轮失败、采用方式和边界；保留不可重新推导的必要结果，不新建逐项证明账本。证据足以判断本项后停止额外测试；只有具体未决问题才追加有独立价值的实验。

## 4. 停止条件与适用回退点

源/范围、Task/generation/key、checkout 或用户内容发生真实冲突时，停止依赖写入并回对应原 owner。没有明确 source/API/状态差额时不增加迁移、兼容 reader 或恢复框架。规范不可读和普通 stale/mismatch 按原流程恢复，不制造新资格门禁。

tools preview 的未知改动逐路径判断，实际冲突和中断由原同操作 resume/rollback；不改 checkpoint、hash 或 peer 内容。匹配 CLI/Core 不可得、native/分发未到达声明路径或真实行为未满足时，记录具体缺口，停止相关通过声明；设施反复失败时改用能回答同一问题的原受支持观察方式，不能将设施错误当作需求效果。

本批没有数据迁移、部署或真实 GitHub 写入需求，因此没有新增此类回滚协议。候选本地修订仅由原写作 owner 在其路径回退，保留无关 dirty。commit、push、PR、merge、Closure 和 Finish 各到自己的精确副作用边界再处理。

## 5. Delivery Policy（唯一）

**full。**D1 覆盖 Task R1–R4、AC1/AC2，交付共享方法、四原消费者、真实 Agent 行为和受管采用证据。没有转给后继 Delivery 的独立工作或临时功能限制。只有 V1/V2 足以判断目标行为、V3/V4 足以判断实际采用且必要保护/兼容保持，才具备本切片交付依据；规划、文件存在或分发通过本身不满足该条件。

普通任务不承担完整多平台安装、升级或发布矩阵；这些不构成本 Task 隐藏剩余实现责任。未验证边界继续如实报告。原 Task Completion 仍核整体范围及真实证据；Delivery 合并不自动完成 Task 或关闭 #818。

## 6. Docs SSOT Plan（唯一）

**strategy=`delta_first`。**实施中由原 RDT maintenance owner 准备本 Task 隔离贡献与完整 proposed targets；命中既有 R153/BEH153/D153/CON153/T153，以及当前 review-sufficiency 能力的真实关系。按 design 第9节，在本能力 `docs/{requirements,design,test}/current/issue-content.md` 承接完整责任和追踪，保留原来源/别名及精确历史替代范围；已有 current 同能力则原位整合，不保留第二定义。完整规则只引用原 canonical Issue 正文，不复制到知识摘要。

直接 consumer 为当前 Issue 写作/审核 owner 及后续实施、独立 Review、Completion；Test 分别拥有实际 Agent、分发和安装结果。原 RDT owner 在 Planning 批准、实现与真实工程验证后，提交前 final_integration 重读真实目标、整合、写入并 readback；后续独立 committed Review 审真实 after。Planning 不写共享 current、全局 README/index/manifest，不递增无关版本，不修改其它 Task 贡献。

Architecture 当前为 no_architecture_impact，不制造 contribution/ADR 或共享架构改动。若真实方案引入架构差额，则回原 Architecture 重新判断，并刷新受影响规划，不以当前结果自证。
