# #332 收敛原 public invoke 入口并修复 Release Gate wrapper 合同

## Goal

解除 `v0.6.15-guru.5` exact-candidate Release Gate 的 public wrapper 阻塞，并纠正
#330 / PR #341 的实现方向：Commit、Publication、Finalizer、Merge 必须继续使用各自
既有的 `scripts/invoke.sh` 公共入口和稳定 command id，在该入口内部收敛 Happy Path、
减少重复事实读取与无谓 recorder/checker/invoke 编排，而不是把原入口降级为 legacy 后
再新增第二套 public wrapper。

本任务的用户价值是同时恢复公共 API 连续性、package/platform 分发边界与 Release Gate
可信度，并真正实现 #330 的耗时目标，不用“适配新入口”掩盖错误的双入口架构。

## Background And Confirmed Facts

- Live authority 是仍为 Open 且无评论的 `castbox/guru-trellis#332`。固定发布映射仍为
  repo tag `v0.6.15-guru.5`、extension revision `0.6.15-guru.40`、Trellis CLI
  `0.6.15`，predecessor 为 `v0.6.15-guru.4`。
- 当前 task branch 为 `fix/332-release-matrix-public-wrapper-contract`，基线与 HEAD 均为
  `593872c4c086524303ed075039986fc4ac31d415`。旧 detached candidate checkout 保持 clean、
  immutable，本任务不修改或复用其 Release Gate evidence。
- #330 的产品意图已经由用户在当前对话澄清：保留并直接优化原公共入口；兼容性指旧入口
  和旧调用形态继续可用，不是保留旧实现再增加第二套正常入口。
- PR #341 为四阶段增加了新的 facade command/wrapper：
  `invoke-guru-create-task-commit-happy-path-v1` / `invoke-happy-path-v1.sh`、
  `review-task-publication` / `review-task-publication.sh`、
  `finalize-task-happy-path` / `finalize-task-happy-path.sh`、
  `complete-task-pr-merge` / `complete-task-pr-merge.sh`。其中后三者还替换了 Interface
  的 public invocation wrapper，造成原 `invoke.sh` 被标记为兼容或 legacy。
- `trellis/presets/guru-team/README.md:671-695` 把上述 package-local wrapper 列入
  `.trellis/guru-team/scripts/bash/**` 共享 companion asset 清单，但这些共享路径实际不存在。
  正确修复是删除虚假共享声明，不是在共享目录补建 Skill 私有脚本。
- Installer 与 installed projection runtime 已按
  `interface.json.public_contracts.invocation.wrapper` 选择唯一平台公共 wrapper；Interface 是
  已有公共合同权威。
- Compatibility matrix 与 throwaway verifier 的通用 projection 检查仍硬编码
  `scripts/invoke.sh`。这会掩盖 Interface drift，也会错误拒绝首个公共入口本来就叫
  `restore-archived-task.sh` 的 `guru-restore-archived-task`。
- `guru-restore-archived-task` 属于 #348 的独立新 Skill，其原始正常入口就是
  `restore-archived-task.sh`，不属于 #330 的入口退役问题；本任务不改名、不退役该入口，
  只用它证明通用消费者能够遵循 Interface 声明。
- `.trellis/spec/workflow/skill-package-contract.md:1450-1478` 已要求 eval runner 调用每个
  Interface 声明的 exact wrapper；每个 Skill 的 wrapper path 由自身 Interface 独立声明。
  当前 compatibility matrix、throwaway projection checks、preset README 和
  `trellis/skills/guru-team/runtime/validate.py` 与该规则不一致。
- 当前 active RDT/Architecture authority 为 `current-main-0.6.5-guru.44`，live public graph 为
  23 Skills / 97 external exits / 81 commands。删除 PR #341 新增的四个 facade command 后，
  successor graph 必须由 live registry/interface 重新派生为 23 / 97 / 77；不得原地改写 `.44`。
- 当前 Architecture design constitution 的 `minimum-necessary-complexity` 与
  `debt-one-way-convergence` 禁止无 consumer 的 wrapper、第二 authority 和无退出双写。
  因此本修复具有真实 Architecture/RDT impact，不能再沿用 #330 的
  `no_architecture_impact` 结论。

## Requirements

### R1. 保留四阶段原公共入口身份

- Commit、Publication、Finalizer、Merge 的 Interface public wrapper 必须分别保持为原有
  `scripts/invoke.sh`。
- 稳定公共 command id 必须保持为：
  `invoke-guru-create-task-commit`、`invoke-guru-review-task-publication`、
  `invoke-guru-finalize-task`、`invoke-task-pr-merge`。
- 不得要求 workflow、Agent、平台 projection 或业务仓库 caller 切换到 PR #341 新增的
  facade wrapper/command id。
- `SKILL.md` 与 package contract 必须把原 `invoke.sh` 描述为唯一正常入口，不再使用
  “legacy public invocation” 或“新 facade 替代旧入口”的模型。

### R2. 在原入口内部完成 Happy Path 收敛

- 保留 PR #341 已实现且经验证的 invocation-local snapshot、单事务、mapped recovery、
  stdout-loss recovery、terminal stop 和 operation budget 能力，但将其挂到原 command id。
- 正常参数形态只运行一次 Happy Path 必需的当前校验和事务，不先执行旧完整路径、再执行
  新路径，也不为了兼容而重复读取同一 Git/GitHub/Trellis facts。
- 旧 caller 所需的参数形态由同一 `invoke.sh` 的互斥参数分支承接；仅检测到旧参数时运行
  compatibility branch。兼容分支不得成为正常路径的前置检查或双写 authority。
- record、check、execute 低层命令继续作为 package-private 诊断、测试和有界恢复入口，
  但不进入平台 public projection，也不要求 Agent 在正常路径逐个调用。

### R3. 删除 PR #341 的第二公共入口层

- 从 canonical commands/interfaces/scripts、installed package、manifest、Shared/Codex/Claude/
  Cursor projection、workflow/Skill 文案和测试期望中删除四个新增 facade command/wrapper。
- 删除只服务这些第二入口且不再有直接 consumer 的 schema、example、fixture、runtime 分支或
  compatibility 标签；仍被原 `invoke.sh` Happy Path 使用的 runtime 能力必须迁入/保留，而不是
  机械回退到 PR #341 之前的慢路径。
- 不新增 `.trellis/guru-team/scripts/bash/finalize-task-happy-path.sh` 或其它共享转发脚本。
- #330 的 watcher、terminal stop、正确性、恢复与确认边界继续保留；本任务不是简单 revert。

### R4. Interface 驱动的通用分发与验证

- Installer、source/installed validator、compatibility matrix、throwaway verifier、generic eval
  adapter 与 projection tests 必须从当前 Interface 读取唯一 public wrapper path、runtime command、
  bytes 和 executable mode。
- 通用消费者不得用 `scripts/invoke.sh` 文件名猜测公共入口，也不得把其它 validator wrapper
  当成 public wrapper；platform projection 只能包含 Interface 声明的那一个 wrapper。
- `trellis/skills/guru-team/runtime/validate.py` 的 platform fallback 校验必须作用于声明的 public
  wrapper，而不是只在 wrapper 名为 `invoke.sh` 时生效。
- Qualification 专属 helper 若其被选 package 合同固定为 `invoke.sh`，可保留该 profile-local
  断言；不得把 profile-local 假设扩散回 generic eval/runtime。
- 以 `guru-restore-archived-task/scripts/restore-archived-task.sh` 作为非 `invoke.sh` 回归样本，
  证明 generic verifier 与 eval 不依赖固定文件名。

### R5. Package-private 与 shared asset 边界

- 每个 Skill 的 transaction/helper wrapper 继续位于对应 package 内；共享
  `.trellis/guru-team/scripts/bash/**` 只列出真实存在且跨 package 的兼容/dispatcher/owner wrapper。
- README、manifest、ownership inventory、installer output 与磁盘实际文件必须一致；不存在的共享
  path 不得通过文档、fixture 或测试伪装为 installed asset。
- 平台 projection 不得泄漏 record、check、execute、preview、helper wrappers、runtime、tests、errors
  或 private schemas。

### R6. 保持语义和副作用边界

- 不削弱 Commit、Publication、Finalizer、Merge 的 AI semantic judgment、freshness、expected-head、
  dirty/mismatch、Issue disposition、恢复和 fail-closed 行为。
- Commit、Finalizer publication、Merge 的当前动作确认继续独立，且授权不持久化、不复用。
- Finalizer mapped same-plan recovery 只能在 plan/scope/authority/side-effect set 未变化时自动承接；
  任何实质变化重新 preview/确认。
- Merge terminal exit 返回后当前 Skill operation 为零；watcher 只绑定当前 repo/PR/expected head。

### R7. RDT、Architecture 与 Release authority 修订

- 把 active `.44` 作为 immutable source authority；先创建本 task 独占的 RDT/Architecture correction
  contribution，禁止在 implementation slice 中原地改写 `.44` shared current。
- 由 serialized RDT/Architecture owner 绑定 expected `.44` 生成唯一 successor
  `current-main-0.6.5-guru.45`。`.45` 必须把 #330 的“双入口/facade”表述改为原入口原地优化，
  并把 compatibility branch 的触发条件限定为检测到旧参数。
- successor `DES-019` 必须声明：platform projection 发布 Interface 声明的唯一 public wrapper；
  不得声称所有 Skill 都固定发布 `scripts/invoke.sh`。
- 新 Architecture correction contribution 与 project check 选择 `dedicated_refactor_slice`，覆盖
  authority、single-writer、compatibility exit、before/after、projection、23 / 97 / 81 到
  23 / 97 / 77 的 graph 收敛、Release Gate freshness 和无第二 authority。既有
  `docs/architecture/contributions/332-release-v0615-guru5.md` 保留为 `.44` promotion history，
  不原地改写其已完成的 `.43 -> .44` 事实。
- 不新增 ADR，除非 implementation discovery 证明出现现有 constitution/change contract 无法承接的
  新长期决策。
- #332 Issue 正文必须在 task activation 前补充该 blocker、原入口纠正方向、successor `.45`、
  23 / 97 / 77 graph 与旧 candidate evidence 作废事实；GitHub 正文修改必须先展示 exact diff，
  再取得独立确认。

## Hard Acceptance Criteria

- [ ] AC1: 四阶段 Interface public wrapper 均为原 `scripts/invoke.sh`，四个稳定 public command id
  不变，workflow/platform caller 不使用 PR #341 新增 command/wrapper。
- [ ] AC2: 四个 PR #341 facade wrapper/command 从 canonical、installed、manifest 和平台 projection
  消失，且没有在共享 scripts 目录补建替代文件。
- [ ] AC3: 原 `invoke.sh` 正常调用保留 PR #341 的低调用次数事务能力；兼容分支只在旧参数出现时
  执行，正常路径不重复 legacy checks/live reads。
- [ ] AC4: Commit 最多一次 prepare 与一次确认后 `invoke.sh`；Publication 一次 `invoke.sh`；
  Finalizer 一次 preview 与一次确认后 `invoke.sh`；Merge 在必要 watcher 后一次确认后 `invoke.sh`。
- [ ] AC5: #330 operation budget 继续满足：正常 command invocation 相对旧基线下降至少 50%，重复
  完整事实读取下降至少 70%，terminal 后 operation 为 0。
- [ ] AC6: 旧 `invoke.sh` 调用形态在同一入口的 compatibility mode 中继续通过既有 fixtures，且不会
  创建第二 public wrapper、第二 authority 或正常路径双写。
- [ ] AC7: Generic installer/verifier/matrix/eval 按 Interface 解析 public wrapper；非 `invoke.sh` 的
  `guru-restore-archived-task` canonical/installed/platform projection、actual-load、bytes/mode/leak
  检查通过。
- [ ] AC8: `runtime/validate.py` 对任何 Interface-declared platform public wrapper 执行 managed launcher
  fallback 校验；qualification-only 固定路径与 generic 路径有明确测试隔离。
- [ ] AC9: Preset README 不再声明不存在的共享 facade assets；canonical、dogfood、installed、
  Shared/Codex/Claude/Cursor、manifest、ownership、reapply、drift 和 recursive sidecar 均一致。
- [ ] AC10: affected package、closeout integration、restore、installer、matrix、throwaway、eval/runtime、
  source/installed validator 回归全部通过，无 P0-P3 open finding。
- [ ] AC11: `.44` 保持 immutable source；task-owned correction contributions 通过独立 review 后由
  serialized owner 生成唯一 active `.45` RDT/Architecture authority，内容正确反映原入口原地优化、
  Interface wrapper authority 与 23 Skills / 97 exits / 77 commands，project check 无
  `fitness_regression`，promotion-created diff 完成 fresh Phase 2、commit 和完整 Branch Review。
- [ ] AC12: preparation PR 合并后只从 fresh `origin/main` 创建新的 detached clean exact candidate；
  旧 candidate 不改写、不作为新 gate 证据，完整 Release Gate 重新从零执行。

## Out Of Scope

- 不重新设计 #348 `guru-restore-archived-task` 的公共命名、typed exits 或恢复语义。
- 不强制所有 Skill 的 public wrapper 都命名为 `invoke.sh`；文件名由 Interface 声明，既有公共入口
  在各自兼容合同内保持稳定。
- 不删除必要 semantic gate、mutation-boundary freshness、post-mutation verification 或恢复能力。
- 不退回 PR #341 之前的多命令慢路径，也不以简单 revert 代替事务能力迁移。
- 不修改 Trellis upstream、全局 npm、`node_modules`、未授权业务仓库或旧 candidate checkout。
- Phase 1 不执行 implementation、Release Gate、commit、push、PR、merge、tag、GitHub Release、Issue
  closure 或 cleanup。
- 暂不创建新的 GitHub Issue；发现与 #332 发布 blocker 独立且无法在本 task 内安全验收的长期
  迁移责任时，才形成一个明确 owner/acceptance 的后续 Issue proposal。

## Open Questions

无。用户已明确原入口原地优化的产品决策；其余 wrapper、consumer、compatibility、RDT 与
Architecture 边界均可由 live Issue、Interface、代码、测试和 current authority 确定。
