# #283 架构单向收敛与设计宪法消费合同

## 目标与用户价值

在 #264 的 Architecture Baseline 原子闭环之上，让业务仓库的 Architecture Baseline 文档 SSOT 真正成为 Guru Team 全任务生命周期的架构决策权威：Planning 读取并引用，Implementation discovery 在范围变化时重新判断，Phase 2 检查满足性，Branch Review 独立复核，task 只形成隔离 contribution/必要 ADR，reviewed promotion 再回补 shared current authority，后续 task 读取新的 current identity。公共 schema、typed route 与项目检查协议只服务这个自我迭代闭环；设计宪法、项目架构基线和 Guru Team 的所有权保持单一，不把业务规则或原则正文复制进公共 Skill。

## Live authority 与已确认事实

- 唯一需求权威是 live Issue #283：`https://github.com/castbox/guru-trellis/issues/283`。fresh re-entry 重读状态为 `OPEN`、1 条权威澄清评论、`updated_at=2026-08-20T14:23:09Z`；标题 SHA-256 为 `90a88ce5e71ff7c862c2826a8635ba074861cd6b13913e7cef910bd09b2f2c2f`，正文 SHA-256 为 `aa2c66224b762d0835cd6b8abe2cd8fddd154e0682cf8a9eea73a063e0824436`。正文已完整定义两个维度强约束、项目 Architecture change contract、最终 reviewed HEAD、串行 promotion/并行 stale 和 10 个代表性业务仓库场景；评论明确 schema/process 全消费者原子切换，不保留 legacy schema、dual-read 或兼容输入。
- 当前 task base、本地 `main`、`origin/main` 与 live remote `main` 均为 `2d34abfc9ea3ef488aedf529e022854050270db7`。#260 由 PR #284 合并，reviewed head 为 `2d5462faa6a0c5d5ead7938325617777324bb327`、merge commit 为 `11d150dece429f75e1c1609e1bf54fe039e6bb29`；#285 由 PR #289 合并，reviewed head 为 `86ff3062c2cee9b116094fd6f0615eb52f190b88`、merge commit 为 current main `2d34abfc9ea3ef488aedf529e022854050270db7`。
- #264 已注册 `guru-maintain-architecture-baseline` 的四个 semantic profile 和七个 typed exit，但 current 1.0 input/output 仍以宽泛且全部非必填的 `object` 为主，runtime 主要投影 `exit_id`，尚不能闭合设计宪法 identity、三类路径、before/after 差量、项目级架构检查或阶段消费合同。
- 项目 Architecture Baseline 当前 authority 为 `docs/architecture/README.md`，active version 为 `current-main-0.6.5-guru.37`。设计宪法正文目前没有独立 authority；#283 只定义 locator、identity、最小原则投影与消费合同，不在公共包中创建设计宪法正文。
- 官方 Trellis 约束已重新核对：workflow 行为由 Markdown workflow/skill 定义，spec marketplace 只承载可复用工程约定，不承载 active task 或项目私有运行状态。

## 范围内需求

### R283-00 Architecture Baseline SSOT 自我迭代闭环

业务仓库必须能够沿同一条正常流程持续使用并演进 Architecture Baseline：

1. Planning 从 current Architecture Baseline 与设计宪法 authority 读取架构决策、GAP、owner、适用原则和项目检查入口，形成当前 task 的 impact/change-path 结论。
2. Implementation discovery 发现 scope、risk、owner 或边界扩大时，返回 Architecture owner 重做影响判断，不能沿用旧计划。
3. Phase 2 对候选实现执行适用的项目检查和 before/after 满足性判断；只有新增或改变 architecture decision、原则权衡/例外、GAP 生命周期、owner/single-writer 或兼容退出条件时，才形成 ADR/contribution 记录。
4. Branch Review 在 committed full diff 上独立复核相同 authority、满足性和 contribution/ADR，不复用 Phase 2 结论代替独立判断。
5. 普通 task 不直接改 shared current；reviewed contribution/ADR 由 Architecture `promotion` 回补 current baseline、history、decision/GAP/owner 状态。
6. promotion 产生的新 current version/content identity 成为后续 task 的读取起点，使 Architecture Baseline 随多个 task 单向收敛、自我迭代。

纯 no-impact 或完全遵循 current decision 且不产生新决策的 task 不创建 contribution/ADR，也不增加人工文档负担。

### R283-00A 两个维度的不可绕过强约束

1. **Guru Team 方法论维度**：每个标准 task 都必须通过 mandatory workflow invocation 进入 Architecture owner。Planning 缺少 current impact/no-impact 结果不得批准；implementation discovery 扩大 scope/risk/owner/状态权威/持久化/SDK/外部或架构边界时旧结果立即 stale；Phase 2 与 Branch Review 分别完成候选与 committed full-diff 的独立语义判断；Publication/Finish 不得消费 missing、stale、conflict、incomplete 或 regression。
2. **业务 repository 项目语义维度**：项目 Architecture Baseline 与 Architecture change-contract authority 提供具体正确答案、required concern set、字段适用性和项目检查入口。适用字段缺失、为空、陈旧、无法证明 `not_applicable`，或与 requirement/design/code/diff/test/runtime/external evidence 不一致时失败关闭。
3. 两个维度只通过 task-local Architecture change contract 相交。公共 Guru Team 不复制项目正文，不硬编码 Afizzy 私有规则；项目也不能绕过 Guru Team mandatory stage/freshness/typed-route 合同。

### R283-01 设计宪法 authority 与最小投影

1. Architecture Baseline 必须声明 current 设计宪法的 authority locator，以及可验证的 version 或 content identity。
2. authority locator 只能指向独立横向基线或项目 Architecture Baseline；设计宪法正文与解释由该 authority 唯一拥有。
3. Guru Team 只消费五项稳定原则 identity 与简短名称：成熟实践与适用性、概念与语义完整性、职责内聚与变化隔离、最小必要复杂度、技术债务单向收敛。
4. 五项原则不是逐项评分表。只有出现适用冲突、权衡、例外或基线不足时，`impact_kind=architecture_impact` 的 task 才记录理由与证据；no-impact task 不新增文档负担。

### R283-02 三类互斥变更路径

`impact_kind=architecture_impact` 的 task 必须恰好属于以下一类：

1. `target_native`：新能力直接遵循 active target architecture，不清理无关历史债务，也不新增已禁止实现。
2. `legacy_boundary_convergence`：Feature/Bug 触及遗留边界时绑定 decision/GAP，在需求范围内局部收敛并明确兼容层、剩余债务和删除条件。
3. `dedicated_refactor_slice`：独立专项重构必须保持用户行为、API 和业务规则不变，并拆成可独立合并、验证、观测和回滚的小切片；需要改变上述行为合同的 task 不属于该路径。

`no_architecture_impact` 是三类路径之外的快速结果，不伪装成第四类架构变更路径。

### R283-03 Task architecture impact

`impact_kind=architecture_impact` 的 reviewed task-local Architecture change contract 必须同时绑定 Guru Team public contract identity 与项目 Architecture Baseline/change-contract identity，并完整包含：requirement/behavior authority、active baseline、设计宪法、领域/集成边界/decision/GAP、唯一 change path、required concern set、当前与目标 owner、single-writer、兼容层与退出条件、`parallel_scope.allowed`/`parallel_scope.forbidden`、计划关闭/保留/新增的偏移、旧实现删除条件、概要/详细设计责任、before plan、after candidate、项目检查、测试/运行/外部 evidence、contribution、必要 ADR、review、promotion 与 expected current baseline identity。普通 task 仍 mandatory 进入 owner，但只返回 task/stage/current baseline identity 与可审核 `no_architecture_impact` 理由。

### R283-04 单向收敛与项目级检查

1. Phase 2 和 Branch Review 比较 task 的 before/after：新增违规、已有违规恶化、GAP 关闭/保留/新增、owner 切换、双写权威、兼容层退出条件和已关闭 GAP 重现。
2. 新增或恶化同类偏移必须返回 `fitness_regression`，不能以 observation 或 future cleanup 放行。
3. 项目可声明自己的架构检查入口。通用结果合同必须包含 check identity/version、applicable scope、rule/decision/GAP identity、before/after、`pass|fail|unverified`、evidence locator、unavailable reason 与 freshness identity。
4. Guru Team 只统一调用、结构、freshness 和失败路由；AI 判断适用性与语义，公共脚本不实现语言/框架检查器或业务阈值。

### R283-05 阶段消费与稳定路由

- Planning 读取 current baseline/设计宪法并完成 impact 与 change path 判断。
- Implementation discovery 在 scope 或 risk 扩大时重新进入 impact 判断。
- Phase 2 执行适用项目检查并完成首次 before/after 语义判断。
- Branch Review 基于完整 committed diff 独立复核，不把自己当成首次检查执行者。
- Publication 只消费 fresh `baseline_current` 最小结果。
- Acceptance/Finish 只接受 reviewed contribution 已 promotion、明确 no-change，或通过 `sync_required` 返回 Architecture owner。
- `contract_incomplete` 返回 Planning/repair owner；`architecture_conflict` 返回 Planning owner；`fitness_regression` 返回 implementation/check owner；authority identity stale 返回 `sync_required`。所有出口保持唯一 consumer 和 fail-closed/re-entry。

### R283-06 Contribution、review、promotion 与并行隔离

`impact_kind=architecture_impact` 的普通 task 只形成 task-owned contribution；shared active baseline 或设计宪法 identity 只能经独立 review 后由唯一 Architecture owner 串行 `promotion` 更新。promotion 必须绑定 expected current baseline identity，重读 reviewed task commit、contribution/必要 ADR、项目检查和 live baseline；live baseline 已推进时返回 `sync_required`，禁止覆盖。promotion 产生新 current identity 后，所有仍绑定旧 identity 的并行 task 必须重新执行 impact、满足性与并行边界判断。两个并行 task 不直接修改同一 shared architecture current 文件，不竞争关闭同一 GAP、不建立冲突 owner、不产生两个 current authority。旧/新权威并存时只有一个写入 owner，并有明确退出条件；每个保留 GAP 均有 owner、原因、依赖和删除/关闭条件。

### R283-07 Public API 原子版本切换

保持 stable Skill id、四个 profile id 和七个 exit id，但不保留 #264 的旧 schema。新增闭合 2.0 input/output/private/consumer schema，并在同一变更中原子切换 canonical、dogfood、installed、全部声明平台和所有 consumer。旧 schema/示例/selector/兼容输入被删除；旧输入明确拒绝，不能被静默解释成 2.0 current evidence。

### R283-08 Canonical、安装投影与验证

canonical package、workflow、preset、installed dogfood、Shared/Codex/Claude/Cursor 声明平台投影和 public docs 必须一致。运行 package/contract/runtime/eval、schema/consumer、preset apply/reapply、drift/sidecar、代表性 clean installation 与 workflow smoke；本 Issue 不执行 #267 的完整多平台 exact-candidate Release Gate。

### R283-08A 固定代表性业务仓库场景

项目中立 fixture 必须覆盖且只能按 live Acceptance 解释以下 10 类场景：

1. `no-impact`：纯文案/等价资源低成本通过，不创建 contribution/ADR。
2. `target-native`：新能力使用目标边界、稳定端口和唯一 owner；新增旧边界业务权威被阻断。
3. `legacy-boundary convergence`：Feature/Bug 绑定 decision/GAP、需求内收敛、剩余债务、兼容、删除条件和禁止并行范围。
4. `dedicated refactor slice`：行为不变的小切片定义单一主写、scope identity、兼容上限、迁移、清理、观测、回滚和旧实现删除条件。
5. `scope expansion`：实现额外触及清理、持久化、SDK 生命周期或 mutation owner 时旧 Planning 结果 stale 并重新判断。
6. `fitness regression`：第二状态/价格/规则权威、扩大旧 owner、无退出双写或 closed GAP 重现时返回 `fitness_regression`。
7. `parallel stale`：task A promotion 后，仍绑定旧 baseline 的 task B 返回 `sync_required`。
8. `unpromoted contribution`：实现/测试通过但所需 contribution/ADR/promotion 未完成时阻断 Publication/Finish。
9. `next-task consumption`：promotion 后的新 task 只读取新的 baseline identity、GAP 与 owner 状态。
10. `missing external evidence`：后端、SDK、生产或商店 evidence 不可访问时保持 `evidence_gap|unverified`，不虚构关闭或排期。

### R283-09 Scope 与依赖边界

本任务只关闭 #283，只使用一个 Trellis task、一个专用 branch/worktree 和一个 PR。不得实现业务仓库重构，不吸收 #247/#249/#250/#261/#248/#252 或 #108 的减法审计，不启动 #267，不创建或修改其他 Issue，不发布 tag 或 Release。

## Acceptance Criteria

- AC-01：设计宪法正文/解释只由 authority locator 指向的独立横向基线或项目 Architecture Baseline 拥有；Guru Team 只持有 identity 与最小原则投影。
- AC-02：Planning、Phase 2、Branch Review 都读取 current 设计宪法，并对冲突、权衡、例外与不足产生稳定 semantic route。
- AC-03：五原则不成为机械 checklist；no-impact task 没有新增 contribution 或人工文档要求。
- AC-04：设计宪法和 active baseline 只有 reviewed promotion 才能改变，且 version/content identity 可验证。
- AC-05：`target_native`、`legacy_boundary_convergence`、`dedicated_refactor_slice` 稳定、互斥、可复用。
- AC-06：`impact_kind=architecture_impact` 的 task 绑定 baseline、decision、GAP 与 owner；AC-07：无关 task 以最小 current/no-impact 结果退出。
- AC-08：Phase 2 证明未新增或恶化同类偏移；AC-09：Branch Review 独立复核相同 before/after 差量而非首次执行检查。
- AC-10：新增/恶化偏移稳定返回 `fitness_regression`；AC-11：项目级检查使用通用协议且公共包没有业务规则。
- AC-12：新旧权威并存只有一个写入 owner 和明确退出条件；AC-13：保留 GAP 具备 owner、原因、依赖和删除/关闭条件。
- AC-14：task contribution 与 active baseline 分离且只有 promotion 可更新 shared authority；AC-15：并行 task 不竞争 shared architecture current 文件。
- AC-16：#108 可消费架构状态与退出信息，但 #283 不实现其代码/Docs 减法审计。
- AC-17：Planning、Phase 2、Branch Review、Publication、Acceptance/Finish 的 Architecture typed routes 全部闭合。
- AC-18：public schema 使用新的显式 2.0 identity，并原子切换全部 producer/consumer/projection；旧 schema 不保留，旧输入明确拒绝，#264 语义不被静默混用。
- AC-19：canonical、dogfood、installed 和声明平台投影一致。
- AC-20：package/contract/runtime/eval 与一个代表性 clean installation 验证通过；完整 release matrix 明确留给 #267。
- AC-21：reviewed promotion 产生的新 Architecture Baseline version/content identity、ADR/decision、GAP 与 owner 状态能被下一 task 的 Planning 作为 current authority 读取；无新架构决策的 no-impact/current-conforming task 不创建 ADR。
- AC-22：每个标准 task mandatory 进入 Architecture owner；Planning 没有 current architecture result 时不得批准。
- AC-23：架构相关 task 同时绑定 Guru public contract 与项目 Architecture Baseline/change-contract identity；任一维度缺失时失败关闭。
- AC-24：required concern set 的适用字段缺失、为空、陈旧、无法证明 `not_applicable` 或与 requirement/design/code/evidence 不一致时失败关闭。
- AC-25：Publication 不消费 missing、stale、`architecture_conflict`、`contract_incomplete` 或 `fitness_regression`。
- AC-26：改变长期架构事实的最终 reviewed HEAD 同时包含实现、evidence、reviewed contribution、必要 ADR、promotion 增量，以及 promotion 后重新通过的 Phase 2 与独立 Branch Review。
- AC-27：不修改 shared Architecture Baseline 的 task 提供 current、可审核的 no-change 证明。
- AC-28：promotion 绑定 expected current identity 并由唯一 Architecture owner 串行执行；live baseline 已推进时稳定返回 `sync_required`。
- AC-29：promotion 后的新 identity 被下一 task Planning 消费；绑定旧 identity 的并行 task 重新执行 impact、满足性和并行边界判断。
- AC-30：两个并行 task 不竞争关闭同一 GAP、不建立冲突 owner、不产生两个 current authority。
- AC-31：package/runtime/eval 与代表性 installed verification 覆盖固定 10 场景，fixture 保持项目中立。
- AC-32：外部 evidence 不可访问时保持 `evidence_gap|unverified`，不得虚构通过、GAP 关闭或排期。
- AC-33：最终 evidence chain 从 requirement/behavior authority 连续到新 shared current identity，任一环缺失、陈旧或矛盾均不能由后续阶段补写解释为通过。

## Docs SSOT Plan

- `strategy`: `delta_first`。
- `RDT profile`: `guru-maintain-requirements-design-test-ssot:task_impact_sync`。实施阶段先创建 `docs/requirements-design-test-contributions/283-architecture-convergence-governance/`，记录 requirements/design/test/traceability；独立 review 后再由 `promotion` 决定 current authority 更新。
- `Architecture profile`: `guru-maintain-architecture-baseline:task_impact_sync`，change path 为 `target_native`。创建隔离 Architecture contribution，绑定 current `.37`、ARCH-FND/GOV 与 #283 影响；不得在 review 前直接改 shared current。
- `durable update`: reviewed promotion 后，current Requirements/Design/Test 与 Architecture Baseline 记录 2.0 架构治理合同、设计宪法 locator/identity、单向收敛和 project-check integration；`.trellis/spec` 只保留 locator/读取/消费规则。
- `task history only`: live Issue payload、完整搜索过程、命令日志、owner-private checkpoint、逐文件 digest、授权信息和临时安装路径不进入 durable docs。
- `release boundary`: #283 只通过 reviewed promotion 演进 current-main authority；stable tag、Release、exact-candidate 全平台矩阵和 immutable smoke 仍由 #267 独占。

## 关键决策

- 交付主线是 Architecture Baseline SSOT 在完整 task 生命周期中的读取、满足性检查、必要 ADR/contribution、reviewed promotion 和后续 task 再消费；schema 2.0 是该闭环的支撑机制，不是独立目标。
- 不新增 Skill 或 exit；扩展现有 Architecture owner，保持 21 Skills/89 exits 公共图基数。
- 2.0 current contract 使用闭合 schema，并与全部 producer/consumer/projection 一次性切换；不保留 1.0 schema、legacy inventory、dual-read 或 migration adapter。
- 仅 `impact_kind=architecture_impact` 的 task 形成结构化 contribution；no-impact 结果不创建额外 artifact。
- Publication/Acceptance/Finish 通过 workflow Architecture router 消费 current 结果，不修改 #261 与 #248 下游 owner 的业务语义。
- 本 Issue 的代表性安装只证明 current-version 安装态，不替代 #267 的 Release Gate。

## 明确非目标

- 不修改业务 repository 产品代码、领域规则、CI、生产配置或业务 Architecture Baseline 正文。
- 不把 Afizzy 或任何单一业务项目的规则、阈值、检查器放入公共包。
- 不实现全仓库静态分析/调用图平台，不自动批准架构例外、重构或 baseline 升级。
- 不引入锁、压力竞态、TOCTOU、攻击模型或与 acceptance 无关的历史重构。

## 阻塞问题

无。最新 live Issue 正文（`updated_at=2026-08-20T14:23:09Z`、body SHA-256 `aa2c66224b762d0835cd6b8abe2cd8fddd154e0682cf8a9eea73a063e0824436`）及 2026-08-20T13:32:08Z 的权威澄清评论、现有 #264 package、current Architecture/RDT authority、#260/PR #284、#285/PR #289 与 repaired normal merge path 已共同确定当前需求、范围、迁移和验证决策。
