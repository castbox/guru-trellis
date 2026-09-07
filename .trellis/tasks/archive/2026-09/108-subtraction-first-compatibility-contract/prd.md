# Guru Team：建立减法优先、废弃代码退出与兼容例外显式确认合同

## 1. 目标与范围

本任务解决 [castbox/guru-trellis#108](https://github.com/castbox/guru-trellis/issues/108)。在不新增 Skill、phase、审批系统、审计平台或通用静态分析器的前提下，将以下合同接入现有 semantic owners：

- Planning：方案先判断直接修改、删除、原位替换或复用；显式列出当前范围内失效资产的退出方案。
- Implementation：实施提示必须承接退出方案；正常发现的废弃资产进入现有 qualification、scope 和 owner route。
- Phase 2：`guru-check-task` 对完整 worktree candidate 检查直接演进、废弃资产退出、兼容支持合同、删除型 diff 增长原因，并独立判断 `code_subtraction` 与 `docs_ssot_subtraction`。
- Branch Review：`guru-review-branch` 从完整 committed `origin/<base>...HEAD` diff 和 live authority 独立重算同一组检查，不读取 Phase 2 私有结果。
- Docs SSOT：RDT 与 Architecture 继续由各自 owner 管理；task artifact 只承载 delta/history，不成为 current authority。

不修改 upstream `trellis-*` agent/Skill，不扩张为全仓库清理，不实现业务仓库清理、通用调用图、净删除指标或完整 Release/upgrade 矩阵。

## 2. 功能需求

### R1 直接删改优先

对于删除、替换、合并和新增需求，规划必须基于真实入口、调用关系、配置 consumer、注册点、需求和设计，先说明为何直接删改/复用可行或不可行。默认方案不得新增第二执行路径、wrapper、adapter、fallback 或并行状态机。

### R2 受影响废弃资产退出

当前范围内因本次改变失去用途的独占入口、实现、分支、配置/schema、依赖、测试、文档和导航必须在同一任务退出；共享资产只有在确认仍有受支持 consumer 后才能保留。零文本引用不能单独证明废弃，注册、反射、依赖注入、外部调用和公共 API consumer 必须纳入判断。

### R3 兼容默认值与边界

非服务端对外 API 默认直接演进：同步可控 consumer，定义新合同并删除旧路径。内部 Skill DTO、checkpoint/artifact schema、脚本参数、CLI 别名、配置字段、内部函数/模块、安装副本和平台 wrapper 均不因 `public/stable` 命名获得豁免。已有明确且未扩大的服务端对外 API 稳定性合同继续履行。

### R4 兼容例外交互

Agent 认为需要新增、扩大或延长兼容时，必须在编码、兼容测试或自修复前向用户说明真实旧 consumer、证据、直接演进影响、精确兼容行为、范围、维护责任、退出条件、清理责任和验证方式，并在取得该具体例外的明确批准后实施。泛化的“继续”或计划确认不得授权隐藏兼容。拒绝或未批准时采用非兼容方案，无法实现则阻塞。

### R5 授权与历史边界

兼容批准只存在于当前对话，不写入 tracked/ignored artifact、schema、checkpoint、gate、handoff 或 public DTO。长期文档只记录最终支持合同、版本边界、退出条件和清理责任。合法历史、archived task、review evidence、ADR、release/changelog/migration 记录不构成当前运行兼容责任。

### R6 删除型增长复审

删除、替换、合并任务在 Phase 2 和 Branch Review 中按 production、测试、生成/受管资产、文档区分增删分布。新增明显多于删除，或出现第二执行路径、兼容包装、额外状态/持久化时，必须触发 AI 方案复审；必要测试、生成产物和新业务能力可增长，但必须说明职责与原因。不设置固定比例或行数 pass/fail 门槛。

### R7 双 subtraction 维度

`code_subtraction` 与 `docs_ssot_subtraction` 必须独立判断适用性、范围、结论和理由；code-only、docs-only、mixed 不互相推导。文档维度覆盖 requirement/product、design、test、operations/navigation，并处理旧行为、旧设计、旧测试和第二套现行权威的退出。RDT 与 Architecture 是 docs 维度内分别判断的 authority 子域。

### R8 生命周期与证据边界

Planning、Phase 2、Branch Review 分别执行语义判断；Phase 2 checkpoint 不作为 Branch Review 证据。脚本只提供或校验 Git/diff/path/schema/状态与其他客观事实，不决定废弃、兼容必要性、severity、pass 或 route。正常路径中的 stale/mismatch、实现缺陷和证据缺口必须 fail closed 或走既有 owner route；恶意伪造、攻击模型、并发压力和非常规加固不在本任务范围。

### R9 复杂度与长期解耦

任务执行不得仅为攻击防护、无限向后兼容、并行压力、形式幂等或非常规故障恢复引入无直接 consumer 的字段、状态、锁、重试、fallback、adapter 或持久化。`personaId` 类无 consumer 的任务字段属于禁止的冗余增长。方案必须同时检查长期职责解耦、既有 owner 和 Architecture 决策收敛；短期通过但污染共享合同或堆积 hack 路径的方案必须回到既有 qualification/Architecture owner。

### R10 非生成文件规模门禁

对未来变更，任何被 task 触及的非生成代码文件不得超过 3000 行；达到或超过阈值必须在当前 task 内完成 AI 审查认可的机械式切分或小幅解耦式重构。历史未触及的大文件不因此纳入本任务；生成文件和 canonical managed projection 不计入该源码阈值，但继续执行既有生成与 drift ownership。

## 3. 验收标准

- [ ] Planning 与实现提示明确先做直接删改/复用判断，并要求删除/替换任务提出旧资产退出方案。
- [ ] 代表性删除场景能识别初始 diff 外因本次改变失去用途的入口/helper/config/schema/dependency/test/docs，同时保留真实共享 consumer、注册式入口和合法局部重复。
- [ ] 非服务端兼容新增/扩大/延长在编码、测试或自修复前触发具体例外交互；未批准时不隐藏保留兼容路径。
- [ ] 已有服务端稳定性合同继续有效，内部 `public/stable` 命名、旧代码或旧测试不自动产生兼容豁免。
- [ ] 一次性必要迁移不被误删；用户数据和副作用确认边界保持不变；不持久化授权信息。
- [ ] 过度设计约束阻止无直接 consumer 的字段/状态/重试/锁/fallback/持久化，以及仅由攻击、并发、非常规故障或形式幂等理由驱动的增长；`personaId` 类错误不能复现。
- [ ] 方案同时证明长期解耦和 Architecture 决策收敛，不因当前 task 通过而接受 hack 式重复职责或共享合同污染。
- [ ] 3000 行规则对未来变更和本任务触及的非生成代码生效，达到阈值触发机械切分或小幅解耦；不扩张为全仓历史大文件重构。
- [ ] 删除型 diff 增长按资产类别触发 AI 复审，无固定净删除阈值；冗余兼容增长不能以一句“安全/兼容”放行。
- [ ] Phase 2 与 Branch Review 都独立检查 `code_subtraction`、`docs_ssot_subtraction`、废弃退出和兼容合同；未验证或 open finding 不能通过。
- [ ] RDT subtraction/promotion、Architecture baseline/change contract、canonical/dogfood/platform projection 继续使用既有 owner 和 single-writer 规则。
- [ ] 语义评估覆盖直接删除、替换收敛、隐藏兼容、批准前后、既有 API 合同、正常废弃识别、具有直接 consumer 与退出条件的必要增长、无直接 consumer 的冗余增长及 code/docs/mixed 三类。
- [ ] 定向 package/runtime/eval/test 覆盖实际结果完整性、consumer/退休、失败传播和 typed routes；不增加仅服务于恶意伪造或攻击场景的负例。
- [ ] canonical、受影响 installed/dogfood/平台投影与 equality/drift 检查通过；overlay 修改执行 apply 和 drift 检查并处理 `.new/.bak`。
- [ ] 一个代表性 clean throwaway 验证新合同安装、加载和代表性执行；完整多平台、workflow switch、Trellis update/upgrade 与 Release 矩阵明确留给专门任务。

## 4. 文档状态

本仓库 durable docs 状态为 `complete_docs`。唯一 Docs SSOT Plan 位于 [design.md](./design.md) 的“Docs SSOT Plan”章节；本 task 采用 `ssot_first`。`prd.md` 只记录需求与影响，`implement.md` 记录执行 checkpoint，不把 task artifact 当作 current authority。

## 5. 非目标与依赖

依赖并复用 #132、#263、#264/#283、#265 既有 owner/合同；#305 Evolution 仍是独立 target 设计，不改写为 current runtime。本任务不新增路由、不恢复早期排队条件、不修改 upstream Trellis 或全局安装包，不执行 commit、push、PR、merge、release 或业务仓清理。
