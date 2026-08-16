# #237 建立 AI 驱动的正常场景资格合同

## Goal

在 Guru Team workflow 中建立唯一的公共 closed-loop Skill
`guru-qualify-normal-scenario`，让每个有权把新行为场景提升为 acceptance、
负向测试、P0-P3 finding、implementation 或 publication blocker 的语义 Owner，
都必须先对当前 invocation 的 candidate set 完成 fresh、scope-first、AI-owned
正常场景资格判断。

该合同要阻止 repository 已排除的攻击、伪造、对抗性输入、故意绕过和未要求
加固再次进入实现，同时保持真实 correctness、明确安全需求、权限边界、secret
redaction、破坏性副作用确认和正常 stale/mismatch 缺陷可被正确资格化。

## Background And Authority

- Live authority 是 GitHub Issue #237 当前正文；该 Issue 没有评论修订。
- 基线是 `origin/main@60a2e962b68a02d08061795cfe9fafcdff206e80`，包含
  PR #238。
- Issue #113 的 F-001 已明确判定：只有人为伪造 artifact/hash 才成立的候选为
  `out_of_scope`，不得进入 implementation 或阻塞交付。
- Issue #236 暴露了复发路径：checker/reviewer 把 alias、wrapper、`shell=True` 和
  `sh -c` 这类仅具语法可构造性的 scanner 绕过误判为受支持正常路径，而真实
  caller 使用错误 runtime 才是当前 correctness 缺陷。
- `AGENTS.md` 已声明 honest-but-fallible 正常运行边界；本任务不把该治理正文
  复制成另一个资格算法。
- 当前公共图采用 registry/interface package、real public wrapper、共享 eval adapter、
  canonical package 到 shared/Codex/Claude/Cursor 的安装投影。

## Requirements

### R1. 唯一语义 Owner

1. 新增 public closed-loop Skill `guru-qualify-normal-scenario`，声明
   `judgment_mode=semantic`。
2. Skill package 是资格算法唯一 SSOT，独占 scope-first 五步判断顺序、安全类
   candidate 反向举证、severity quarantine、candidate decision、fresh re-entry 和
   mechanism remove/replace 语义。
3. Workflow、AGENTS、durable specs、schema、scripts、platform prompts、caller skills
   和 worker agents 不得复制或改写资格算法。
4. Skill 直接重读 live authority、planning、真实 entry/caller/consumer、当前
   diff/range/base pair、测试和 repository contract；caller 提供的结论不能替代
   live reread。

### R2. 十个 mandatory profiles

完整支持以下 profile，workflow 与 standalone mode 使用相同语义和 freshness：

1. `task_free_pre_write`
2. `task_free_evolution`
3. `requirements_scope_set`
4. `change_request_candidate_set`
5. `planning_scenario_set`
6. `implementation_discovery`
7. `base_impact_candidate_set`
8. `phase2_candidate_set`
9. `branch_review_candidate_set`
10. `publication_candidate_set`

对应 mandatory caller 必须在形成 scope decision、用户提问、acceptance、测试、
severity、finding、implementation route、task-work return 或 publication blocker 前
调用该 Skill。`guru-select-workflow-mode`、`guru-sync-base`、
`guru-discover-change-context`、`guru-review-contract-wording`、
`guru-create-task-workspace`、`guru-create-task-commit`、`guru-finalize-task` 和
`guru-merge-task-pr` 不直接资格化新场景。

### R3. Public I/O

1. 使用十个 profile-specific closed input schema 和一个仅负责 discriminator closure
   的 aggregate schema，不使用大量 optional/nullable 字段的总对象。
2. 每个 profile 只接收固定 `profile`、`mode`、固定 caller、当前 target identity、
   非空去重 `candidate_refs` 与支持 live reread 的最小 locators。
3. Public input 禁止 severity、scenario class、qualification decision、expected exit、
   用户授权、旧 qualification result、共享 artifact locator、raw worker report、完整
   测试/search transcript 和 caller 自行断言的 normal-path 结论。
4. 每个 candidate 恰有一个 decision：
   - `qualified_current`
   - `qualified_explicit_nonstandard`
   - `qualified_approved_expansion`
   - `scope_confirmation_required`
   - `rejected_no_authority`
   - `rejected_unsupported_entry`
   - `rejected_not_reproduced`
   - `rejected_out_of_scope`
   - `mechanism_removed`
   - `mechanism_replaced`
   - `blocked`
5. Public Skill 只返回四个 typed exits：`classified`、
   `scope_confirmation_required`、`mechanism_revision_required`、`blocked`。
6. Consumer 固定为：
   - `classified` -> `guru-normal-scenario-classified-router` -> profile 原 Owner；
   - `scope_confirmation_required` -> `guru-clarify-requirements`；
   - `mechanism_revision_required` ->
     `guru-normal-scenario-mechanism-router` -> profile 原 Owner；
   - `blocked` -> stop `normal-scenario-qualification-blocked`。
7. Unknown、multiple、empty candidate set、profile/caller/consumer mismatch、candidate
   缺失或重复 decision 均 fail closed。

### R4. 资格行为

对每个 candidate 固定按以下顺序判断：

1. requirement authority；
2. supported entry/caller/consumer；
3. honest normal action sequence；
4. current required behavior 是否真实失败；
5. scope provenance；前四步通过后才进入安全、攻击、绕过、加固或 severity
   叙事。

安全、伪造、篡改、绕过、对抗输入、anti-tamper、anti-forgery、defense in depth、
TOCTOU、锁和 fault injection 类 candidate 的初始结论是不具备当前 scope 资格。只有 exact
current requirement locator、真实 supported entry、无需恶意行为的 action sequence
和可重复 current defect 同时存在时才可 qualified。

Repository contract 已排除的候选必须直接 `rejected_out_of_scope`，不得升级为
`scope_confirmation_required`，不得生成 follow-up、负向测试、implementation 或
publication blocker。当前任务自行引入且只服务排除场景的机制必须 remove/replace，
不得因已有代码、测试、coverage 或 reviewer severity 形成既成事实。

### R5. Worker 与 caller 边界

1. Guru-owned coordinator 调用官方 `trellis-research`、普通 implement/check worker、
   channel runtime agent、平台 sub-agent 或未被指定为当前资格 Owner 的 reviewer 时，
   必须在 invocation prompt 中把 planning-external 发现限制为 invocation-local candidate；
   不修改或覆盖这些 upstream-owned agent 的定义文件。
2. Coordinator 从 worker 结果中只投影 candidate ref、观察行为、代码/测试 locator 和
   最小复现线索。Planning-external candidate 在 fresh qualification 前不得触发 edit、
   test、self-fix、severity、scenario class、qualification decision 或 implementation
   route。
3. 当前主 caller 必须重读真实文件与 authority，再调用资格 Skill；不得因 worker
   已实现或测试已存在而接受候选。
4. Phase 2 主会话的 `implementation_discovery` profile 是 workflow 中的显式
   mandatory invocation 点。

### R6. Private witness 与持久化边界

1. 不创建 tracked 或 ignored `normal-scenario-result.json`、qualification report、
   candidate/rejection ledger、approval/signoff、assignment、handoff、逐轮 transcript
   或跨阶段 evidence bundle。
2. 新 Skill 的 semantic decisions、candidate mapping 和 typed result 仅存在于当前
   invocation/process 的内存与 stdout 管道；Skill 不写 repository tracked 文件、
   gitignored runtime qualification artifact、跨进程临时 result locator，或供后续阶段
   读取的 qualification checkpoint。Recorder/checker 如存在，只能从 stdin 接收当前
   process 的数据，在内存中执行 shape、identity、freshness、enum、引用与 consumer
   binding 校验，并通过 stdout 返回当前调用结果。
3. Qualification result 仅在当前 invocation 内有效；authority、planning、candidate
   set、caller graph、diff/range/HEAD/base pair、publication payload、scope choice、
   mechanism revision 或 finding fix 变化后必须完整重跑。
4. Phase 2、Branch Review 和 Publication 由各自语义 Owner 直接把 direct consumer
   所需的最终 classification/witness 写入该阶段既有 owner-private gate；该 gate 不引用
   新 Skill artifact、result locator、checkpoint 或前次 qualification stdout。
5. Phase 2 与 Branch Review 的 witness 必须结构化绑定以下六项：
   `requirement_refs`、`supported_entry_refs`、`existing_caller_refs`、
   `honest_action_sequence`、`defect_observation`、`excluded_assumptions`。
6. Schema/validator 只检查结构、identity、freshness、enum、引用与 consumer binding；
   不判断 scope、正常路径、充分性、severity 或 route。
7. 对需要改变的既有 schema 使用新版本和明确迁移/旧 checkpoint 失效合同，不静默
   改变既有 public API。
8. Package、installed public entry、十 profile、失败路径和 re-entry tests 均比较调用前后
   的完整 repository file inventory，并断言零 qualification artifact、零 runtime residue、
   零跨进程 result locator。

### R7. Production semantic eval

1. Evals 必须通过 clean install 后真实 public entry、real wrapper 和十个 profiles，
   禁止 prompt 片段、mock classifier、关键词黑名单或手写 expected artifact 冒充。
2. 每个 profile 覆盖相同语义 candidate 的中性表述、attack framing、P0/P1、独立
   reviewer pressure、already implemented、already tested、best practice/defense in
   depth 和 theoretical bypass 变体。
3. #113 F-001、#236 alias/wrapper/shell scanner 变体稳定 rejected，且不得产生
   clarification、test、implementation 或 publication-blocking route。
4. 每组 rejected case 配对 legitimate case，覆盖正常错误 digest/payload、真实 caller
   走错 runtime、明确 secret/credential redaction、明确权限或破坏性确认、正常
   stale/mismatch、错误 executor output 和维护遗漏。
5. 当前目标模型 GPT-5.6 Sol 对每个 production-path case 执行 5 次相互独立 fresh
   invocation，必须 5/5 decision 和 route 正确；任一错误阻断。
6. 模型或关键 prompt 变化使门禁失效并要求完整重跑；通过结论不得声称未来模型
   永不复发。
7. 不同于实现 Owner 的 independent reviewer 必须检查全部十 profiles、真实 production
   entry、非关键词判断、压力变体完整性和发布结论边界。

### R8. Canonical、安装与升级

1. 更新 canonical workflow、public Skill package、registry/interface/contracts、八个
   caller packages、Guru-owned worker invocation/consumer boundaries、durable specs、
   preset installer/manifest、evals 和 public docs；不得修改 upstream-owned agent 文件。
2. 通过 preset apply 生成并同步 dogfood、shared/Codex/Claude/Cursor copies；平台
   entry 只加载 Skill、返回 candidate、消费 exits，不复制算法。
3. 验证 source、installed、selected-platform 与 dogfood byte/mode parity、ownership、
   active graph closure 和零 `.new`/`.bak`。
4. 官方 live 文档把完整升级定义为两步：`trellis upgrade` 把全局 CLI 升到发布版本，
   `trellis update` 再把当前项目同步到该 CLI 模板版本。验证必须按 clean initial install
   -> 隔离 npm prefix 中执行 `trellis upgrade --tag latest` -> 目标项目执行
   `trellis update --dry-run` 与适用的 `trellis update`/`trellis update --migrate` ->
   workflow preview/switch -> preset reapply 的顺序完成。
5. `trellis upgrade` 只能在 disposable npm prefix/container 中运行并验证 upgrade 前后
   CLI version；不得修改开发机 global npm。`trellis update --migrate` 只在 dry-run/live
   output 明确报告 `MIGRATION REQUIRED` 时执行。
6. 上述路径完成后，marketplace workflow、preset、Skill package、registry、平台投影、
   ownership 与零 sidecar 合同不得丢失或退化为 caller-local 判断。
7. 不修改 Trellis upstream、开发机 global npm、系统 Python、node_modules 或真实业务仓。

## Acceptance Criteria

- [ ] `guru-qualify-normal-scenario` 是资格算法唯一 semantic SSOT，完整声明
      semantic closed loop、scope-first 顺序、安全反向举证、severity quarantine 和
      fresh re-entry。
- [ ] 十个 mandatory profiles 在 workflow 和 standalone mode 均有 closed input、
      caller binding、真实调用点和一致 freshness。
- [ ] 四 typed exits、两个 profile router、clarification consumer 与 blocked stop
      形成唯一、可机器验证、fail-closed 的 consumer graph。
- [ ] 十个 caller 只形成 profile-specific candidate set 并消费结果，没有复制资格判断。
- [ ] Worker/reviewer 只能返回 candidate；资格前不能赋 severity、形成 finding、补
      测试或实现。
- [ ] 已排除场景直接 rejected，不触发 scope confirmation；自引入且仅服务排除场景
      的机制必须 remove/replace，并在内容变化后重跑。
- [ ] 新 Skill 的 semantic decisions 与 typed result 全程 invocation/process-local；
      recorder/checker 只用 stdin/stdout/内存，且没有 tracked、ignored runtime、临时
      cross-process locator、checkpoint 或其它 qualification residue。
- [ ] Phase 2、Branch Review、Publication 只在各自既有 owner-private gate 中直接记录
      direct consumer 所需的最终 classification/witness，且不引用新 Skill artifact。
- [ ] Script/schema 仅执行结构、identity、freshness、enum、引用和 consumer binding
      校验，不包含关键词分类或 semantic route 决策。
- [ ] #113 F-001 与 #236 攻击式 scanner 变体在全部压力 framing 下稳定 rejected；
      paired legitimate correctness/security cases 稳定 qualified。
- [ ] 十 profiles 的全部 production-path cases 在 GPT-5.6 Sol 上各自 5 次 fresh
      invocation 达到 5/5；任一误分类 fail closed。
- [ ] Source/package/workflow route tests、real-wrapper semantic eval、preset apply、
      dogfood drift、ownership、clean install、隔离 `trellis upgrade`、项目
      `trellis update`、workflow preview/switch、preset reapply 与 recursive zero sidecar
      全部通过。
- [ ] 不同 Owner 的完整 Branch Review 覆盖 `origin/main...HEAD` 当前 diff，随后
      publication readiness 真实通过。
- [ ] Issue/PR 只陈述当前模型、prompt、十 profiles 和 eval matrix 的实际保证，
      不声称“永不复发”。
- [ ] Scope ledger 只关闭 #237；#113、#236 仅 related；不触碰、恢复、评论、关闭或
      清理 #220/#127。
- [ ] 不创建 tag/Release，不升级业务仓，不开始独立 guru.8 发布门禁。

## Out Of Scope

- 改造 #236 的 Python runtime 路由实现。
- 恢复、修改或清理 #220/#127 的任何 task、worktree、branch 或 runtime evidence。
- 新建人工审批、签字、assignment、handoff、跨阶段报告或共享 candidate ledger。
- 为恶意伪造、故意绕过、对抗性输入、TOCTOU、锁、fault injection 或其它未要求
  加固扩展业务实现与测试。
- 创建 `guru.8` tag、GitHub Release、真实业务仓升级或发布门禁 Issue。

## Open Questions

无。Issue #237 已给出完整产品边界；剩余实现选择由当前 repository contracts 和
测试/安装证据确定。
