# #305 Requirements 审核与修订映射

## Authority

- Change authority：[GitHub Issue #305](https://github.com/castbox/guru-trellis/issues/305)。
- Requirements planning snapshot / current branch HEAD：
  `f962b640f7f142bf657fc9e5ebf5da3cd79a1a6b`；这是本 task 的历史基线，不声称等于 fresh
  `origin/main`。每轮 gate 必须只读核对 live upstream drift，未经独立授权不 rebase/merge。
- Repository Requirements authority：`docs/requirements/evolution/README.md`、
  `requirement-main.md`、`requirement-non-functional.md`、
  `current-capability-inventory.md`。
- 本文件只记录本 task 的 review/revision delta 与执行映射，不复制或替代 repository
  Requirements SSOT。

## Current Phase Boundary

- 当前执行保持 repository Requirements 为 `requirements_draft`、current-to-target trace 为
  `requirements_trace_draft`，只修订并复审 Requirements；fresh 全稿门禁通过前不得恢复 ready 状态。
- Requirements 结果展示前不进入 Evolution Design，不创建或修改 target
  Design/Test/Architecture contribution。
- 不执行 runtime implementation、commit、push、PR、merge、tag、Release、Issue 链修改或
  Git submodule 操作。
- #304 是相关但隔离的 pre-refactor Release authority，不是本 Requirements gate 的前置或 owner。

## Review And Revision Delta

| Finding | Severity | Repository authority gap | Required closure | Status |
| --- | --- | --- | --- | --- |
| `REQ-REV-001` | P1 | README 把 #304 发布闭环写成 Design 前置，并把 `candidate_stale` 快照写成已冻结/验证 | 统一 #304 隔离、snapshot 状态与 Design eligibility | closed in Requirements revision |
| `REQ-REV-002` | P1 | Design 启动授权被列入 `requirements_ready_for_design` 文档门禁，形成先 ready 还是先授权的循环 | 分离文档资格与后续副作用授权 | closed in Requirements revision |
| `REQ-REV-003` | blocking P2 | `.40` Test capability 只给出汇总式“有 target fixture”结论，不能逐组复核 successor 差集 | 为全部 `TST/SCN/CASE` 建立 current capability、target requirement 与 fixture successor | closed in capability inventory revision |
| `REQ-REV-004` | blocking P2 | migration/provider 的正常失败、部分成功和 terminal state 不足以约束 Design | 补齐 live reread、无重复副作用、无 mixed graph 与 forward recovery 验收 | closed in Requirements/NFR/fixture revision |
| `REQ-REV-005` | P3 | “Requirements 阶段不创建资源”没有区分本次已授权审核资源与后续实施资源 | 收窄为不据 target authority 创建后续实施资源 | closed in Requirements revision |
| `REQ-REV-006` | blocking P2 | provider 恢复未要求绑定 current 外部合同，也未闭合可重试/幂等/有界停止语义 | 要求 action contract/capability binding、live reread、安全重复前提、有界尝试和 non-retryable/partial-success stop | closed in Requirements/NFR/fixture revision |
| `REQ-REV-007` | blocking P2 | migration 使用 cutover 前后分支，但 phase identity 与 cutover boundary 不可观察 | 要求 preflight/application/final-validation identity、唯一 cutover boundary 和逐阶段失败分类 | closed in Requirements/NFR/fixture revision |
| `REQ-REV-008` | P3 | API/CLI 不适用理由明确，但只笼统引用“需求标准” | 显式引用 `requirement-doc-standard` 第 5.1 节 | closed in Requirements revision |
| `REQ-REV-009` | blocking P2 | README 重复定义 #304 隔离、snapshot 状态与 Design 授权规则，和 `requirement-main.md` 形成可再次漂移的双主定义 | 将 README 收敛为 status/locator 导航，只链接第 0/10 章主定义 | closed in Requirements revision |
| `REQ-REV-010` | P3 | 第二章入口摘要未显式列入 `REQ-UC-EVO-033` 正常清晰请求 | 将该场景归入标准 change workflow 的摘要级入口范围 | closed in Requirements revision |
| `REQ-REV-011` | P1 | 第二章声明五类入口，但第六章只保留 standard/task-free；`github_pr`/`none`、Issue closure 与 specialist/release/resume route 不可达 | 重构第六章入口分流、delivery route selection/freshness、closure-current/not-applicable 与全部 terminal/re-entry | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-012` | P1 | post-publish smoke 被写成发布前置，Release 时序不可执行 | 分离 pre-publish gate、独立确认、immutable publication、tag-pinned post-publish verification 与发布后 forward recovery | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-013` | blocking P2 | task-free 资格是循环定义，且缺少 finding/recheck、位置/active-task recovery 与 blocked | 定义显式/自动选择边界、一次 choice、完整 check/revision/recovery/blocked/scope-expansion 产品结果 | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-014` | blocking P2 | Phase 2 后已有本地副作用时，latest-intent override 没有保留、suspend、清理或新 lifecycle 路线 | 按无副作用、可逆本地副作用、不可逆远端副作用定义 override/additive route 与 fixture | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-015` | blocking P2 | 执行连续性零计数与 migration terminal 在功能/NFR 两边重复主定义 | 功能正文拥有行为与状态，NFR 只拥有可测质量门槛并单向引用 | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-016` | blocking P2 | fresh review 发现 entry/change-mode、Release confirmation、Issue closure 与 specialist caller/terminal 使用未映射组合状态 | 收敛为两级 entry projection、`ready_for_release_confirmation`、两个 exact closure outcome 与 caller/standalone 互斥出口 | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-017` | blocking P2 | migration、resume 与可逆本地 work 只覆盖成功/保留，没有失败 terminal、唯一 consumer 或跨 lifecycle reconciliation/isolation | 补三类 migration terminal、partial publication、recovery not-found/multiple/stale，以及 suspended work 的同 scope reconciliation/异 scope isolation | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-018` | blocking P2 | 第 5.2 节重复定义功能行为，NFR-010 owner 引用不完整，workflow switch 只存在于 NFR | 将 5.2 收敛为 evidence 判读；修正 base/provider owner；由场景、功能需求和 fixture 承接 workflow switch | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-019` | blocking P2 | 状态图先产生 `workspace_ready`，再判定 suspended work 的 scope/归属/隔离，允许标准资源在 exact plan confirmation 前创建 | 将 scope resolution 与 `suspended_work_plan_confirmed` 前置到任何标准资源副作用；资源准备后再验证 reconciliation/isolation，未收敛不得 Planning | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-020` | blocking P2 | clean install 被错误纳入 existing migration terminal；final-validation failure 又被固定解释为 cutover 后 | 为无旧 current 的 clean install 建立独立 application/validation route 与 `clean_install_blocked`；existing migration 的 application/final-validation finding 均按 live cutover state 分流 | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-021` | blocking P2 | resume 将所有 stale/mismatch 无条件阻塞，与 equivalent identity freshness 合同及 NFR-009 的单一 current-phase 质量门槛冲突 | 区分 equivalent stale refresh/recovery 与 unresolved/material stale block；blocked 质量门槛改为 known candidates/facts、唯一所需输入和 resolution re-entry | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-022` | P3 | Evolution Design gate 的复审范围仍写 `REQ-REV-011..015`，漏列已进入 fresh review 的后续 finding | 将主文档与 task gate 范围始终统一为 current complete finding set；本轮为 `REQ-REV-011..024` | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-023` | blocking P2 | `REQ-UC-EVO-030` 的 completed archive history query 被压入 active-work recovery，唯一历史结果没有独立 success terminal | 区分 active resume/recovery 与 completed history query；新增 archived result current、query completed/blocked 和各自 resolution re-entry，已完成 task 不被重新激活 | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-024` | blocking P2 | projection validation 只有成功路径，drift/sidecar/`.new/.bak` 等 mismatch 没有 owner、blocked result 或 exact re-entry | 由 `EVO-REQ-053` 定义 `projection_validation_blocked`、candidate/surface/mismatch 解释与修复后的 exact validation re-entry，并同步状态图、fixture 与 NFR 质量门槛 | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-025` | blocking P2 | provider recovery 只显式覆盖 Delivery，没有约束 distribution、clean install、migration 与 Release 的外部动作 | 将 `EVO-REQ-039` 扩展为跨 route 外部 provider 合同，并由 `EVO-REQ-053..054,056`、fixture、NFR 与 return matrix 显式继承 | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-026` | blocking P2 | existing migration 只证明切换合同，没有证明迁移前 active/resumable task 与 archived finish/history result 在新合同下仍可恢复/查询 | 在 cutover 前盘点并判定 preservation；不可承接则保留 pre-migration current 并停止，成功后经新合同恢复/查询且无 legacy runtime consumer | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-027` | blocking P2 | 并行 fixture 未覆盖 A=`github_pr`、B=`none` 混合 route 的 provider/archive/Finish/cleanup failure、双完成顺序和 retained-ref/history 隔离 | 扩展 `EVO-REQ-033`、`EVO-NFR-011`、`EVO-FIX-PARALLEL` 与 return matrix，证明两种顺序、失败归属、各自 recovery/history 与 cleanup reachability | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-028` | P3 | 第二章重复定义 `change_request/change_mode_selected` 的可执行选择规则，与第 3/6 章形成双主定义 | 第二章仅保留入口层级摘要与第 3/6 章链接，删除强制选择与 route 约束 | closed in prior Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-029` | blocking P2 | 当前候选曾使用晚于 `2026-08-24` 的 authority 日期，并把未发生的 fresh review 写成 ready/pass | 将日期恢复为真实证据日期，撤销 ready/pass，保持 draft 直到 exact candidate fresh 全稿复审 | closed in Requirements revision; fresh full review pending |
| `REQ-REV-030` | blocking P2 | live `.40` authority 已把 capability-loss 收窄为 `workflow/task_data/docs_authority`，但 Evolution trace 仍把 Skill API、distribution 与 installed consistency 混入 capability loss | 同步 `EVO-REQ-053`、NFR、fixture 与 `CUR-CAP-017..018`：两类 gate 都阻断，consistency/installation drift 不构成 capability loss | closed in Requirements revision; fresh full review pending |
| `REQ-REV-031` | blocking P2 | 顶层入口只有类别名，没有完整互斥分类；terminal history 后的新修改、distribution 合同修改、in-flight event 与 stop 的边界仍可能走错 route，且 stop 没有完整 terminal | 在 `EVO-REQ-010`、状态图、return matrix 与 fixture 中定义 new change/resume/distribution/specialist/stop 的互斥规则、歧义处理、in-flight 边界及 `request_stopped -> workflow_completed` | closed in Requirements revision; fresh full review pending |
| `REQ-REV-032` | blocking P2 | projection mismatch 一律由 projection owner 终止，未区分 standalone validation 与 clean install/migration/Release 内嵌 gate，允许 child validator 抢占 caller ownership | standalone mismatch 保留 `projection_validation_blocked`；内嵌 gate 只返回最小 finding，由 clean-install、migration、Release caller 分别产生 route-local blocked/terminal，并同步 NFR、fixture、状态/return matrix 与 inventory | closed in Requirements revision; fresh full review pending |
| `REQ-REV-033` | blocking P2 | current capability inventory 以 worktree 相对路径描述 `.40` authority，未把全套 Requirements/Design/Test/Architecture locator 绑定 immutable source ref，未 reconciliation checkout 可能被误读为 current | 将 current authority 统一绑定 `source_ref=a4b68d42b25e3d2173fac2db353295043590cca5`，逐项列出 Requirements main/NFR/decisions、Design inventory/main/traceability、Test strategy/traceability 与 Architecture README 的 immutable path | closed in Requirements revision; fresh full review pending |
| `REQ-REV-034` | blocking P2 | additive intent 只有“并入未完成请求/返回最早 owner”的单一路线，未区分 owner-local 输入、改变 candidate/route/acceptance 的 material change，以及不可逆远端副作用开始后的 pending 新 invocation | 在 `REQ-UC-EVO-031`、`EVO-REQ-041,047`、状态回程、NFR、fixture 与 inventory 中定义三类 additive route；远端边界后的 material additive 必须形成不修改旧 candidate、可发现且有唯一 consumer 的 `additive_change_pending`，并在原 owner 收敛为既定正常 current terminal、失败后 forward-recovered terminal 或 terminal block 后，从新的 `request_received` 重新执行 entry selection | closed in Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-035` | blocking P2 | 不可逆远端副作用后的 generic override 在旧 route 收敛后被直接强制为 new change，绕过 `request_received -> entry_route_selected` 的五类互斥分类 | 在 `REQ-UC-EVO-031`、`EVO-REQ-047`、状态回程、NFR、fixture 与 inventory 中统一为：旧 route 收敛 current 后由唯一 request-entry consumer 生成新的 `request_received` 并重新执行五类 exactly-one entry selection，只有 new change 进入二级 mode selection，错误默认 new change 为 0 | closed in Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-036` | blocking P2 | 不可逆远端副作用后的 material additive 虽重新执行 `entry_route_selected`，但被预设为 new change；distribution/release、resume/history、specialist review 或 stop 等正常追加意图会被误送到 change lifecycle | 与 generic override 使用相同的顶层分类合同：旧 route 三类结果任一 current 后，pending intent 从新的 `request_received` 重新执行五类 exactly-one entry selection；只有 new change 进入二级 mode selection 与独立 change lifecycle，其他分类返回对应顶层 route，错误默认 new change 为 0 | closed in Requirements revision; current exact-candidate fresh review pending |
| `REQ-REV-037` | P3 | `requirement-main.md` 的 Design gate 仍停在 `REQ-REV-034`，且 `EVO-CAP-001/004` 未引用直接确认 generic override 修订的 `EVO-EVD-017` | 将 current finding/revision 范围同步到完整集合，并把 `EVO-EVD-017` 及本轮 material-additive 决定 `EVO-EVD-018` 加入两项核心能力 evidence refs | closed in Requirements revision; current exact-candidate fresh review pending |

## Acceptance Mapping

- `EVO-001..007`、`EVO-CAP-001..004`：由 repository Requirements 主定义及 Goal trace 审核。
- Finding 严重度只使用 `finding_severity=P1/P2/P3`；核心能力表中的 `P0/P1/P2` 只表示
  `capability_priority`，不引入或混用 `P0` finding。
- `REQ-UC-EVO-001..044`、`EVO-REQ-001..066`、`EVO-NFR-001..018`：执行编号完整性、
  入口分支、唯一主定义与 fixture 可达性差集检查。
- `.40` current capability：校验 live 21 active Skills / 89 external exits，并审核
  `CUR-CAP-001..020`、previous Skill coverage 与 Test capability successor closure；另外独立验证
  `workflow/task_data/docs_authority` capability-loss 与 Skill API/distribution/installed
  consistency，禁止把后一类 drift 归类为 capability loss。
- Final gate：fresh 全稿复审无 P1、无阻断性 P2、无高风险 open question，输出
  `requirements_ready_for_design` 后停止。

## Fresh Requirements Gate

- `REQ-REV-011..037` 的 current 正文修订已完成；`REQ-REV-029..037` 使 exact candidate 发生变化，
  之前候选的 fresh review 结论不得复用。
- 当前审核结果：尚未对修订后的 exact candidate 执行 fresh full-document semantic review、strict
  technical review 与确定性闭包；不得声明 `P1/P2/P3=0` 或高风险 open question 已清零。
- 当前 gate：`requirements_draft` / `requirements_trace_draft`。只有 fresh Requirements 全稿审核
  通过才可恢复 `requirements_ready_for_design`；本 task 随后仍在 Requirements 结果展示处停止，未经
  另一次独立明确确认不得进入 Design。
