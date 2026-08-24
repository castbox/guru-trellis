# Guru Trellis Evolution 非功能需求

版本：`evolution-requirements-revision-2026-08-25`；状态：`requirements_draft`。

本文件是 Evolution Requirements 非功能约束的唯一主定义。功能范围与场景见
[`requirement-main.md`](./requirement-main.md)，验收 fixture 与执行成本证据规则见该文件第 5 章。

## 1. 执行效率、安静性与上下文治理

`requirement-main.md` 的 `EVO-REQ-044..050` 是执行连续性功能行为的唯一主定义；本节只拥有
质量门槛与计数口径，不重新定义允许的消息类别、handoff 内容、resume route 或状态转换。
以下约束以 `requirement-main.md` 第 5.2 节的 action/consumer 与 correctness trace 为依据。
流程耗时、rounds、bytes、compression 次数及相对 baseline 改善比例可用于诊断，不作为
Requirements、candidate 或 Release 的验收门槛；不得通过删减能力、隐藏失败或跳过 gate 获得
表面上的短路径。

- `EVO-NFR-001`：对 `EVO-REQ-044..050` 定义的正常行为，没有新 authority、finding、选择或
  副作用变化时，重复 semantic gate、重复阶段往返和同一 owner 可合并却拆开的重复动作计数均为
  0；不设置相对耗时或轮次阈值。
- `EVO-NFR-002`：同一 exact unchanged source 在相邻阶段的重复正文/累计输出/private evidence
  注入计数为 0；具体允许传递的最小信息由 `EVO-REQ-045..048` 主定义，本条不维护第二份字段集合。
- `EVO-NFR-003`：正常路径保留动作的 direct-consumer 或 correctness/freshness coverage 为 100%；
  无 consumer 的脚本、validator、recorder、文档重读和外部状态查询计数为 0。
- `EVO-NFR-004`：`EVO-FIX-FULL-NORMAL` 必须覆盖 request-to-cleanup 的完整正常生命周期，并为
  每项保留的 handoff、读取、脚本、gate、validation 和 transition 说明不可替代的责任；无法说明
  直接 consumer 或 correctness 价值的动作必须删除，不设置相对耗时或交互轮次门槛。
- `EVO-NFR-005`：正常 Planning 主动生成 continuation capsule 或非 durable 中间交接文件的计数为
  0；平台自动 context compression 只作为诊断信号，不作为 PASS/FAIL 条件。发生
  compression/resume 时仍须按 `EVO-NFR-009` 恢复 current 工作，具体恢复行为由
  `EVO-REQ-046..047` 主定义。
- `EVO-NFR-006`：对 `EVO-REQ-049` 定义的 clear/no-finding 路径，暴露内部读取、projection、
  recorder、validator 或 locator 搬运的用户可见消息计数为 0；允许展示的业务消息类别只由
  `EVO-REQ-049` 主定义。
- `EVO-NFR-007`：任一 public handoff/result 的字段都必须有唯一直接 consumer；无 consumer
  字段、可 live 重建事实、process metadata、授权和完整 evidence 不进入 public output。
- `EVO-NFR-008`：本条是执行连续性异常计数的唯一主定义。每个支持的 exact normal fixture/run
  中，invalid handle wait、decision-relevant truncation、duplicate cumulative stdout、
  unconsumed user intent 和 orphan artifact 均为 0；workflow 主动生成但没有直接恢复 consumer
  的 continuation capsule 计入 orphan artifact。术语对应的正向行为与 route 只引用
  `EVO-REQ-044..050`，不得在本文件另起一套功能合同。

## 2. 可靠性、恢复与可用性

- `EVO-NFR-009`：在 `EVO-FIX-ENTRY-ROUTING` 中，invocation-level exactly-one route 与 new-change
  二级 exactly-one mode 的分类覆盖率必须为 100%，unfinished/terminal lifecycle 误分类、
  distribution-contract-change 误入验证 route、in-flight event 重新顶层分流和歧义未收敛前副作用
  计数均为 0。在 `EVO-FIX-REQUEST-STOP` 中，合法 stop 的新增/修改/cleanup/发布副作用为 0，既有
  work 可发现性与不变性覆盖率为 100%，且终点必须可观察为
  `request_stopped -> workflow_completed`。在恰好一个 current work 可解析，或 stale identity 经 live
  facts 证明 semantically equivalent 且唯一的 resume/interruption fixture 中，最新用户意图、current
  phase、已发生副作用、未解决 finding 和唯一下一 route 的保留率必须为 100%。在 not-found、
  multiple、unresolved stale 或 material mismatch 的 blocked fixture 中，候选 identity、最后确认
  facts、已知副作用、未解决 finding、唯一所需输入和 `current_work_resolution` re-entry 的记录
  覆盖率必须为 100%；不得伪造单一 current phase、猜测 checkout/route，或只恢复压缩前的旧目标。
  `EVO-FIX-LATEST-INTENT` 中 generic override 按无副作用、可逆本地副作用、不可逆远端副作用的
  分类和 exact-owner attribution 覆盖率必须为 100%；远端分支必须覆盖旧 route 的三类收敛结果，
  并在结果 current 后对新的 `request_received` 完成五类顶层 exactly-one route 覆盖，绕过
  `entry_route_selected`、错误默认 new change 或错误进入二级 mode selection 的计数均为 0。
  owner-local additive、不可逆远端副作用前 material additive、不可逆远端副作用后 material additive
  的分类和 exact-owner attribution 覆盖率也必须为 100%；后者必须
  分别覆盖旧 route 正常形成既定 current terminal、失败后 forward recover 至 current terminal 与
  terminal block，且 `additive_change_pending` 可发现性、唯一 consumer 与新 `request_received` 的五类
  顶层 exactly-one route 覆盖率必须为 100%。intent 丢失、重排、重复或提前消费、错误 owner/re-entry、
  无 consumer pending、material additive 绕过 `entry_route_selected`、错误默认 new change、错误进入二级
  mode selection、绕过原远端 owner 以及修改 in-flight/published candidate 的计数均为 0。override/additive
  正向行为只由 `EVO-REQ-010,041,047` 主定义，本条不复制其功能路线。
- `EVO-NFR-010`：`EVO-REQ-039,053..054,056` 覆盖的 Delivery、distribution、clean install、
  existing migration 与 Release 外部 provider failure，以及 `EVO-REQ-032,060` 覆盖的 base
  movement/refresh failure，必须产生明确 current blocked/recovery 边界。provider 场景必须可解释
  current contract/capability、target/action 与 unknown-outcome classification；base 场景必须可解释
  selected base、exact upstream identity 与影响范围。两类结果都必须解释最后确认的 live state、
  已完成与待执行副作用、可重试/幂等/停止分类、当前尝试是否仍在 Design 声明的有界策略内，以及
  唯一恢复入口；不得把 `unverified`、`skipped` 或历史结果冒充 PASS。日志、指标或 public result
  的具体承载形式由 Design 决定。
- `EVO-NFR-011`：本条只拥有 `EVO-REQ-033` 并行隔离行为的质量门槛。对同一 exact base 上
  A=`github_pr`、B=`none` 的双 task fixture，两种 completion/merge order 中 task-local resource、
  provider、archive、Finish、cleanup、history 与 retained-ref 的交叉写入、错误归属、副作用重放和
  failure propagation 均为 0；B 的 GitHub I/O 为 0，两个 task 各自 recovery 后的 history/current
  result 与 cleanup 前后 retained-ref reachability 覆盖率均为 100%。shared authority 仍只经
  serialized promotion 前进。
- `EVO-NFR-018`：parent repository 的正常 mode selection、Intake、RDT/Architecture Planning、
  Implementation、validation、Finish 与 Cleanup 不得依赖无关 Git submodule 的初始化、可访问性、
  clean/branch 状态或命令成功；默认路径的 submodule I/O 与 validation 为 0。显式 submodule
  repository scope 必须隔离运行，不能扩大 parent task 的 authority、artifact 或验证集合。

## 3. 兼容、分发与可维护性

- `EVO-NFR-012`：Shared/Codex/Claude/Cursor 与 canonical/dogfood/installed 的 scenario、
  semantic result 和 re-entry/stop 必须一致。对 `EVO-REQ-053` 的每个 supported projection cell，
  capability-loss gate 只比较 `workflow`、`task_data`、`docs_authority`；独立的
  consistency/installation gate 比较 Skill API/interface/schema/command、distribution、
  managed/installed inventory、mode、template hash、sidecar、声明平台 parity 与 extension
  identity/version binding。两类 gate 的 drift 检出、分类、affected-surface 解释和 exact validation
  re-entry 覆盖率均必须为 100%；后一类 drift 仍阻断但不得计为 capability loss。top-level
  standalone mismatch 的 projection-owner attribution 与 `projection_validation_blocked` re-entry
  覆盖率必须为 100%；clean install、existing migration 或 Release pre-publish 内嵌 gate finding 的
  exact-caller return 覆盖率必须为 100%，错误取得 standalone projection ownership 或产生
  `projection_validation_blocked` 的计数为 0。错误 `projection_current`、未分类 projection failure
  和以其它 distribution route 掩盖 failure 的计数为 0。
- `EVO-NFR-013`：本条只拥有 `EVO-REQ-053` clean install、`EVO-REQ-054` existing migration 与
  `EVO-REQ-056` Release pre-publish caller-owned failure 的质量门槛，不重新定义 phase、cutover 或
  terminal categories。clean install 的每个
  supported cell 都必须能够查询并解释 current install status，且 100% 落入
  `new_contract_current` 或 `clean_install_blocked`；existing repository 经 official Trellis
  install/update/upgrade、preset reapply 或 workflow switch 的每个 supported migration cell，都必须
  能够查询并解释 current phase/cutover status，且 100% 落入 `pre_migration_current_preserved`、
  `new_contract_current` 或 `migration_blocked`。对迁移前可发现的 active/resumable work 与
  archived finish/history result，100% 必须在 cutover 前得到可解释的 preservation/migration 判定：
  能由新合同承接的，在 `new_contract_current` 后保持可恢复/可查询；不能承接的，只能在 cutover
  前保留 pre-migration current 并阻塞。Release pre-publish finding 的 Release-owner attribution、
  `release_pre_publish_blocked` 结果、新 candidate identity 与完整 gate rerun 覆盖率必须为 100%。三类
  caller 路径中的错误 projection terminal、历史静默丢失、legacy runtime consumer、可运行旧新混合
  graph、静默 authority 丢失、未分类 terminal、旧 candidate evidence 复用和发布后 legacy fallback
  均为 0；用户本地修改与 current Requirements/Design/Test/Architecture authority 按官方语义保留。
- `EVO-NFR-014`：正常路径的 semantic owner 数量、持久 artifact 数量和 public data volume
  必须由直接业务责任/consumer 证明；不得为了“合同完整”新增 wrapper、schema 或 checkpoint。
- `EVO-NFR-015`：同一事实在 Requirements/Design/Test/Architecture/workflow/Skill 中只有一个
  semantic owner；projection 只引用 identity/locator/version/status，不复制正文。

## 4. 安全与隐私

- `EVO-NFR-016`：prompt、log、artifact、Issue、PR、history 与测试证据不得泄露 secret、token、
  private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。
- `EVO-NFR-017`：Git/GitHub/Trellis 副作用只能发生在用户已确认的 exact target/scope 上；
  unrelated dirty/untracked files、worktree、branch、task 和远程资源必须保持不变。

## 5. 非功能范围豁免

| `waived_item` | `scope_refs` | `waiver_reason` | `risk_statement` |
| --- | --- | --- | --- |
| 服务端 QPS/并发吞吐 | 全局 | 本产品是本地/Agent 驱动的交互 workflow，无常驻服务端 API；本轮只治理 workflow 内无 consumer 动作、重复读取/注入和不必要交接，不设置替代性的吞吐或相对性能指标 | 不代表外部 GitHub/Trellis 服务性能；流程耗时与工具量可用于诊断，但不决定 PASS/FAIL |
| 恶意 actor、对抗输入、artifact 人为伪造、额外锁/TOCTOU | 全局 | 产品假设 honest-but-fallible 协作，按仓库 current 安全边界执行 | 普通 stale/mismatch、错误 recorder/validator 和 secret/副作用边界仍必须处理 |
| 旧 Guru workflow 合同兼容 | `REQ-UC-EVO-034..035` | 用户明确要求重构后只保留新合同 | existing repository 仍必须通过一次受支持迁移进入新合同；不能静默留在旧路径 |
