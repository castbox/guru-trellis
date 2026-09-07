# 实施计划

## 0. 激活前与边界

- [x] 在计划展示前完成 planning wording review、Architecture planning impact 与 `guru-approve-task-plan`；未批准不运行 `task.py start`。
- [x] 激活后读取 live Issue #108、当前 main/base、RDT/Architecture current authority、`.trellis/spec/workflow/semantic-retrieval.md` 与本任务三份规划。
- [x] 每次写 source、test 或 task artifact 前通过现有 workspace-boundary 检查；只处理本任务范围文件，不覆盖用户并行改动。

## 1. Durable contract first

- [x] 根据 live owner 结果更新 Requirements/Design/Test/Architecture contribution 或 current-safe docs，明确 R1-R8、直接演进、废弃退出、兼容例外、历史边界和双 subtraction 维度。
- [x] 更新 workflow/preset/spec canonical 合同与 README 引用；workflow 只编排 stable Skill，入口不复制 owner checklist。
- [x] 为 planning/implementation/check/review caller 写入 approved-plan 约束和兼容例外交互要求；不修改 upstream `trellis-*` agent/Skill。
- [x] 在第一次 runtime/schema/test 编辑前复核 Docs SSOT merge checkpoint，确认本文第 6 节的 task delta 已有 durable 落点。

## 2. Planning 与机制评估

- [x] 让 `guru-approve-task-plan` 复用现有 requirement/design/caller/config/test/docs 读取，先形成 direct delete/modify/reuse 判断，再形成 compatibility candidate。
- [x] 让 `guru-qualify-solution-mechanism` 在 planning profile 中先排除未经批准的兼容 wrapper、fallback、dual-read、旧配置读取和第二执行路径。
- [x] 明确当前范围废弃资产退出计划及共享 consumer、注册式入口、外部 API、单测自证边界。
- [x] 兼容例外仅在当前对话说明完整具体选择并获批准后实施；不将批准写入任何 artifact、schema、gate、DTO 或脚本。

## 3. 实施承接

- [x] 更新实现/平台 worker prompt，使 worker 只执行 approved-plan work；发现规划外废弃资产、兼容需求或 owner/authority 扩张时停止并返回 invocation-local candidate。
- [x] 保持新增能力走已有 owner，删除/替换功能原位收敛；同一任务退出无真实 consumer 的生产实现、配置/schema/dependency/test/docs。
- [x] 将过度设计、长期解耦、`personaId` 类无 consumer 字段和 3000 行门禁纳入 durable contract；本 task 不批量重构历史未触及大文件。
- [x] 复核未发现 cross-owner dependency、真实 scope 变化或 architecture boundary 扩张；因此无需触发 qualification、clarification 或 Architecture re-entry。

## 4. Phase 2 与 Branch Review

- [x] 在 `guru-check-task` 中加入九维检查所需的 direct evolution、deprecated exit、compatibility support contract、deletion-growth review。
- [x] 独立形成 `code_subtraction` 与 `docs_ssot_subtraction` 结论；按 production/test/generated-managed/docs 分类解释增长，不设机械比例门槛。
- [ ] 在 `guru-review-branch` 中从完整 committed range 独立重算同一合同；不读取、恢复或复用 Phase 2 checkpoint（前一轮发现 preset 投影与 workflow SSOT 问题，已修复，待修复提交后重审）。
- [ ] 保持 RDT subtraction/promotion、Architecture before/after、GAP、ADR、single-writer 与 existing typed routes 归原 owner；适用失败或 blocking unverified 不得 aggregate pass。

## 5. 测试与评估

- [x] 添加/更新 contract/eval tests，覆盖 public input/output 不膨胀、typed route、失败传播、consumer/退休和 stale/mismatch 的既有处理；补充无 consumer 复杂度、解耦目标和 3000 行触发语义评估。
- [x] 添加 synthetic semantic eval：直接删除、替换收敛、隐藏兼容提议、批准前拒绝/改方案/批准后有界实现、已有服务端合同、正常废弃识别与合法保留、具有直接 consumer 与退出条件的必要增长、无直接 consumer 的冗余增长、code-only/docs-only/mixed。
- [x] 通过 contract/eval 检查验证仅测试调用的未接入实现不被视为生产能力；注册/反射/依赖注入/外部公共 API 不被零文本结果误删；合法历史与受管副本不被误报。
- [x] 未添加以攻击、伪造 artifact/hash/state、并发压力、TOCTOU 或非常规 crash consistency 为目的的机制或负例。

## 6. Canonical、安装与投影

- [x] 对 canonical package、preset、workflow、README、schema、commands、overlay 做 source checks。
- [x] 运行并核对 source/package、managed hash、接口/exit identity 与 equality/drift；新 workflow spec 已补入 preset managed inventory、throwaway inventory 和通用 drift checker。preset apply 因现有 installed provenance conflict 未能安全同步，受影响副作用已恢复，不能据此声称 installed projection 通过。
- [x] overlay 未变化；已运行 `check-dogfood-overlay-drift.sh` 并通过，无 `.new/.bak` 遗留。

## 7. 代表性环境验证

- [x] 运行受影响 package/runtime/eval suite、`task.py validate`、静态语法/JSON 校验与 `git diff --check`。
- [ ] 执行一个 clean throwaway：安装 workflow/preset，加载 planning/check/review 入口，运行一个代表性语义场景并验证新合同（当前因 installed provenance conflict 未完成）。
- [ ] 不把一个 throwaway 结果扩张为完整多平台、workflow switch、Trellis update/upgrade 或 Release Gate；未验证边界在最终说明中列出。

## 8. Phase 2 收敛

- [x] 运行 fresh `guru-check-task`，覆盖修复后的完整 task scope、live docs、RDT/Architecture 当前结果、过度设计/解耦/3000 行门禁和所有 applicable checks。
- [x] 对 Branch Review 发现的 current-scope findings 完成修复，并重新运行 Architecture owner、定向验证和 Phase 2；未发生 scope/authority/architecture 扩张。

## 9. Commit/Review 后续门禁

- [ ] 仅在 Phase 2 passed 后进入 `guru-create-task-commit`；只 stage 本任务授权文件，提交中文 Conventional Commit。
- [ ] 由独立 `guru-review-branch` 审查完整 `origin/<base>...HEAD`，确认 code/docs subtraction、废弃退出、兼容合同和 Docs SSOT 一致。
- [ ] Publication/Finish 不首次执行 subtraction 判断；PR readiness 只消费已审查结果和真实验证边界。

## 10. 明确未覆盖

- [ ] 不创建或修改 upstream Trellis 源码、全局 npm/node_modules、业务仓库、通用静态分析器或独立审批系统。
- [ ] 不执行 push、PR、merge、tag、Release、cleanup；这些必须由后续既有阶段和单独副作用确认承接。
