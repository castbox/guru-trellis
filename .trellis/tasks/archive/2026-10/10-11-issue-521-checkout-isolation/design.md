# Guru #521：隔离执行设计候选

## 当前对象与责任
设计对象是 canonical guru-select-workflow-mode、guru-execute-task-free-change、trellis/workflows/guru-team/workflow.md 的 caller/re-entry，以及 runtime/task_lifecycle 中正式 Task checkout acquisition。安装投影由 preset apply 拥有，upstream start/continue、continuation extractor 与 hooks 保持 upstream-owned。

以下是实施前的历史行为记录，不是本候选合同：selector 明文限定 current checkout 且不创建 worktree/branch；执行 Skill 允许 default branch 编辑；正式 Task adoption 可采用 primary non-base checkout。上游 continue 在无绑定时返回 no_current_task 并结束其自身步骤；它没有 Task-free 身份。Task resolution 要求 clean checkout，本候选不得借隔离需求放宽全部生命周期校验。

## 单一路径
1. 当前 caller 先读取真实 binding。有效正式 Task 回原 Task owner；stale/conflict 停止。无 binding 才按 fresh 当前请求和范围进入 selector/task-free，不从别的聊天 inventory 自动选择 Task。
2. Selector 只判断 mode，不负责资源创建或把非默认分支当 Task 信号。移除 current-checkout 限定，保留最小现有 DTO 和 selection origin。
3. task-free execution owner 在原 pre-write suitability 判断内读取 Git registration、common-dir、primary/linked topology、branch/HEAD 与完整 dirty 差额。适合位置须是本仓 linked worktree、非 base 工作分支、无 unresolved conflict，且范围/候选归属和真实 binding 合法。
4. 无合适位置由此 owner 返回现有 location_required；同一 owner 明确复用或展示创建计划，按当前对话实际授权执行认证 git worktree add 的精确动作，进入目标目录后重读事实再写。此路径不使用 TaskLifecycleKey、Task checkout acquisition DTO、Task ledger 或正式 Task wrappers。既有中立 Git facts 可复用；不新增 acquisition Skill、task-free registry、checkout mapping 或临时 adapter。
5. 所有文件工具使用隔离绝对路径；命令/tool root 与输出也指向隔离目录。task-free continuation 的范围与位置只由 host 当前对话和真实差额承接，新聊天靠明确请求及 live facts 恢复；上下文不足回 location_required 或 bounded blocked，不创建缓存来猜身份。
6. Guru workflow caller 定义 upstream continue 返回 no_current_task 后的唯一 consumer：该结果只证明无正式 Task，caller fresh 核对当前范围、实际位置和绑定后进入合法 task-free owner。上游 Skill 的 stop 仅结束上游步骤，caller 不改上游字节、不把返回解释为 Task 创建前置。真实 native 调用若不能把返回交给 caller，停止该依赖验收并列出最小 upstream 变更；不通过 patch 接管入口弥补。

## 正式 Task 与部分修改
Task creation/adoption 的正常位置改为 linked non-base checkout。正式新 Task 的 primary 拒绝放在 runtime/task_lifecycle/composition.py:prepare_creation_inputs 与 guru-create-task 的 create-only 合同；共享 adopt_invocation_checkout、recover_checkout_acquisition、checkout resolution 和旧 Task result recovery 不增加全局 primary 禁令或放宽 clean 校验，base Sync、Cleanup 保留 checkout 职责不变。旧 primary Task 仅由原生命周期 owner 依据 live Task/binding/control state 逐例迁移，未迁移对象不宣称新默认已生效。

task-free 的自动与显式扩张继续走原 reselect_mode/explicit_choice_required。owner 先停止剩余写入，读取并保留已产生修改；模式升级只进入原 Intake。clean 合适工作树可被正式 acquisition 精确复用。若当前隔离位置已有部分修改而 Task acquisition 的 clean 前置不满足，不放宽全局 clean 校验：先审查归属和完整差额，再由原 Intake/acquisition owner 选择新的 clean linked worktree；真实承接动作须另展示来源、目标、精确差额与影响，取得适用授权后才操作。未取得授权或差额不足时保留原候选并停止依赖动作，不造空 Task 绕过。不得自动 stash/丢弃、退回 primary、静默 bind 或重复搬运；已完成的精确承接由 live source/target 差额和 host continuation 判断，不增加迁移账本。

## 直接演进与替代
直接修改现有 owner 合同和受支持的 caller；旧 current-checkout 语义在新安装中退出，不保留双模式 fallback。保留现有 typed exits，只有直接 consumer 不能消费必要事实时才提出最小 schema 变更并回 Planning 重新审核。
拒绝 shell alias、post-checkout 自动恢复、空 Task、持久化位置映射与新 wrapper：这些不满足 first-write 隔离，或重复既有责任。同步主 checkout 不属于本任务安装/交付副作用。

## Docs SSOT Plan
只在独立 task contribution docs/requirements-design-test-contributions/521-checkout-isolation/{manifest.yaml,requirements.md,design.md,test.md,traceability.md} 承接 R521/T521 增量；当前 RDT .84 和 Architecture .83 保持 single writer，promotion 前重读 expected current。阶段内不直接竞争 shared current README/spec 索引。
Architecture 独立 owner 决定真实 impact/change path、贡献与必要 ADR；不能由本设计自称 no-impact。task-owned Architecture contribution 为 docs/architecture/contributions/521-checkout-isolation.md；内嵌 ADR-521-CANDIDATE 只为 proposed decision，长期登记仍归 promotion owner。不复制 constitution 正文。晋升产生的 diff 必须重新 Phase2/commit/独立完整 Branch Review。
canonical workflow/Skills、workflow/preset README 和现有 spec 在其最近责任位置解释新合同，preset apply 同步 dogfood/发现入口。业务 #120 只消费实际可采用版本及本仓安装结果，不把源测试当安装生效。

## 证据边界
客观测试验证 topology、Task creation 拒绝 primary、binding 事实、schema/consumer、projection parity 和 upstream 字节。真实 Agent 验证 start、普通/新聊天续接、显式 continue caller，以及两种 expansion 的原 owner 回程和 partial preservation。完整 Release matrix、正式 tag/Release 和业务升级不由本候选静态 pass 宣称通过。

## 无 Issue 标准接管的最小输入兼容修订

R521-07/T521-06 的真实标准接管链在 Sync、Discovery、Clarify、Wording 后停止：原 Review 的 standalone_request 输入只允许 standalone，而实际标准链的 workflow transition 又必须被保留。这是当前验收直接依赖的 consumer 输入兼容前置；仅改调用 mode、改写 producer DTO 或换用 Issue 会转移原失败。

直接演进 guru-review-change-request 的既有 standalone_request public input：mode 同时接受 workflow 与 standalone，source profile 仍表示无 Issue 请求，mode 仍表示执行方式。保持现有 schema id、target identity、source/owner/profile matching、producer transition mode equality、typed exits、router 与 Task clean acquisition；不新增字段、owner、wrapper、state 或 side effect。proposed_draft 已接受两模式，无须额外修改。

在原 package 最近合同处解释两种语义相互独立；现有 package test 和 production producer-chain fixture 覆盖 workflow/no_issue 到原 ready，保留 standalone 路径与普通 mode mismatch 拒绝。按 preset 同步 source/installed/platform schema 投影，再在原 native GitHub-backed 会话同输入接续，验证 ready 后由原 Task owner 展示 clean linked 位置与独立 Task/精确承接计划。此前失败和 partial 候选继续保留；Task/资源创建和承接不由模式升级执行。
