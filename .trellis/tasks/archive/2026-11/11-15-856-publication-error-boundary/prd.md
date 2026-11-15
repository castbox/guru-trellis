# 修复 Publication 已知错误被误报为 internal_error 的公共异常边界整体需求

## 1. 来源与术语

| 标识 | 来源与定位 | 角色 | 本 Task 用途 |
| --- | --- | --- | --- |
| SRC-856 | https://github.com/castbox/guru-trellis/issues/856 ，问题与目标、最小解决方案、验收、相关工作与范围；正文更新时间 2026-11-15T13:00:08Z | Direct Source／要求 | 定义整体修复目标、正常调用场景、兼容边界和验收 |
| SRC-856-D | 同一 Issue 的“最小解决方案”三节 | 已约定设计约束 | 保留原异常构造、内部 typed recovery、单一接续点、现有公共合同和脱敏边界；实际方案由 Delivery design 承接 |
| SRC-856-R | https://github.com/castbox/guru-trellis/issues/856#issuecomment-6894689222 | 审核证据／建议 | 说明已完成的因果调查、只读复现及其适用边界；不代替本次实施验收 |
| SRC-CODE | `trellis/skills/guru-team/packages/guru-publish-task-delivery/runtime/owner.py`、`runtime/invoke.py`、`errors/catalog.json`；`trellis/skills/guru-team/runtime/command.py`、`runtime/io.py` | 当前实现证据 | 定位原 owner 异常、公开入口、共享序列化边界及退出码 |
| SRC-VALIDATION | `.trellis/spec/workflow/quality-guidelines.md` 的 Test And Validation Value、Validation Scope Ownership；`.trellis/spec/workflow/causal-completion-semantics.md` | 工程约束 | 选择有效的最小验证集，区分本轮代码／测试证据与历史业务发布效果 |

术语：

- Publish 指当前 `guru-publish-task-delivery` owner。
- `WorkflowError` 是该 owner 已分类的领域异常，现有 code 和必要 payload 仍供内部逻辑使用。
- `CommandError` 是共享公共命令错误合同，承载 code、field_path、remediation 和退出码。
- typed recovery 指原 owner 已声明并合法消费的恢复路线，包括 resume、stale 和 reprepare；它不等同于公开命令错误。

TaskId 为 `856-publication-error-boundary`，lifecycle generation 为 0。Task 的 Direct Source 为 #856，关系为 `exact_source`。创建或编写本 PRD不代表实现、交付或整体完成。

## 2. 背景与问题

当前 Publish owner 定义 `WorkflowError(RuntimeError)`。共享 command 边界仅捕获 `CommandError`。未被 owner 内部路线消费的已分类 WorkflowError 因此进入通用异常兜底，被改报为 `internal_error/runtime`，丢失原类别、定位、恢复提示和部分声明退出码。

Issue 已从原公开 invoke wrapper 只读复现两类正常调用错误：漏传 `readiness_result_id`，以及 PR body 误用 `Closes #435`。它们在 Task／Delivery 读取及发布写入之前被拒绝，但原类别被丢失。共享 JSON 读取器对不完整 JSON `{` 能正确返回 `invalid_json/input`，构成对照。

本 Task 的固定调查基线为 `origin/main@4f3d9069e0720ec94e39d1079154d2f7a7058935`。当前相关 Publish package 和共享 command 边界相对接受评论核实的 f76e76e 基线没有差额；异常类型断层仍存在。

历史 G10 首次发布失败只留下 generic internal_error，没有首次 traceback。旧 Draft 事务关联已合并 PR 的状态支持 `publication_stale` 解释，但不是已经直接观测到的唯一异常。本 Task 不依赖重放该历史发布来证明当前缺陷。Preview 的旧额外实验受本地 runtime 前置条件阻塞，不计为该入口已经通过或失败的完整验收。

## 3. 目标与非目标

### 3.1 整体目标

修复原 Publish owner 已分类领域异常与共享公共错误序列化之间的连接，使正常输入或状态错误通过其原公开命令返回有依据的类别、定位、安全恢复提示和声明退出码。

整体完成须覆盖实际直接入口、内部正常发布／恢复路线、真正未知异常的安全兜底及必要分发验证。不得以单一函数修复、内部异常属性断言或一次 wrapper 通过替代整体范围。

### 3.2 非目标

- 不实施 #850，不修改默认 Wording gate。
- 不修改业务仓库、业务 PR、Task／Delivery 生命周期、CI／merge policy 或发布许可。
- 不恢复 #794 已退役的提前 Draft 路线。
- 不把移动、删除或改写历史 checkpoint 当作公共修复或恢复方法。
- 不修改历史终态处理，除非另有当前受支持 consumer 的独立证据；该扩展不属于本 Task。
- 不新增公共 DTO、异常协议、通用日志框架、诊断服务或全局异常重构。
- 不新增恢复状态、审计 artifact 或长期失败账本。
- 不扩张到恶意伪造、攻击模型、锁、竞态压力、崩溃一致性、额外 fault injection 或跨 OS 加固。
- 不真实重放业务发布、旧 Draft、push、PR 创建、Ready 或 merge。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前置条件 | 触发动作 | 必须保留的行为与可观察结果 |
| --- | --- | --- | --- |
| S856-01 缺少必填字段 | 当前 Publish 调用方准备 delivery_review_ready 输入 | 从原生产 invoke wrapper 提交缺少 readiness_result_id 的对象 | 在任何 Task／Publication 或 Git／GitHub 副作用之前拒绝；返回 schema_mismatch、依据充分的定位、安全纠正提示和 exit 2 |
| S856-02 PR body 关闭关键词 | 当前 Publish 调用方提交其余字段完整的输入 | PR body 含 Closes #435 | 在副作用之前拒绝；返回 closing_keyword_forbidden、对应定位、安全提示和 exit 3 |
| S856-03 共享读取器错误 | 调用方传入不完整 JSON | 从原 wrapper 提交 `{` | 保留现有 invalid_json/input 与 exit 2，不被 package 异常接续改变 |
| S856-04 直接入口与内部路线 | 正式 invoke、Preview、record、check、execute 使用其合法当前输入／状态 | 某入口触发原 owner 已分类且尚未被内部路线消费的失败，或合法进入 typed recovery | 已分类失败由同一公共边界承接；原内部 resume／stale／reprepare 路线保持其原 consumer，不被提前截断 |
| S856-05 同事务恢复 | 原发布事务已有完成动作，或外部动作结果未知 | 调用原 owner 继续失败后的恢复 | 先回读并恢复同一事务，不自动重发已完成或结果未知的 push、建 PR、Ready 或 merge |
| S856-06 真正未知异常 | package 出现无法按已声明 owner code 分类的编程异常 | 公共命令处理该异常 | 保留安全 internal_error 和原维护路径，不输出原始异常或敏感内容，不伪装成已知业务失败 |

## 5. 行为要求

### R856-01 已分类失败接续

对应 S856-01、S856-02、S856-04。未被 owner 内部路线合法消费的已分类 WorkflowError，必须接入共享公共错误合同。已声明失败保留 package catalog 的类别、客观定位、安全恢复提示和退出码。

定位由有依据的原抛错点提供。证据不足时定位到原步骤，不从异常 message 猜测字段。

### R856-02 单一原边界与兼容

对应 S856-04。优先在原 WorkflowError 定义处兼容接入 CommandError。保留原构造调用、内部捕获和 code／必要 payload 的内部用途。

只有实际 consumer 证明继承关系存在兼容约束时，才选择 package 内单一适配点。不得在各 wrapper 复制映射，不创建第二套异常协议或公共 DTO。

必要但未声明的 owner code 只依据真实直接 consumer 补最小声明，或映射到合适的既有类别；不得按任意异常属性通用推断。

### R856-03 内部恢复与语义门禁保持

对应 S856-04、S856-05。原 owner 已合法消费的 resume_publication、stale／reprepare 等 typed exit 保持原职责、触发条件和 consumer。

错误接续不得改变原失败条件、发布资格、scope／readiness 判断或原语义审核结论。调用方依据客观失败回原 owner；脚本不决定是否放行。

### R856-04 不重复外部动作

对应 S856-05。已执行外部动作或结果未知时，沿原 owner 先回读、恢复同一事务。失败提示或自动接续不得导致重复 push、建 PR、Ready 或 merge。

无需为展示错误增加恢复状态、持久失败记录或诊断账本。

### R856-05 未知异常与脱敏

对应 S856-06。真正未知的编程异常继续失败为安全 internal_error，沿原 package 维护路径处理。

任何公开输出不得包含 traceback、原始异常 message、外部 stderr、命令参数、PR 正文、完整 payload、环境或凭据。最小诊断优先采用现有 code／field_path／remediation。内部必要 payload 的保留不代表可以公开序列化它。

### R856-06 catalog 与实际退出码一致

对应 S856-01 至 S856-06。核对本 package 的实际公共退出码与既有 catalog。缺字段为 schema_mismatch／exit 2；关闭关键词为 closing_keyword_forbidden／exit 3；共享 invalid_json 对照保留 exit 2。其余触及类别按本 package 有效声明验证，包括真正未知异常的安全兜底。

本要求不重设计所有 package 的错误系统。

### R856-07 必要分发与诚实证据

同步必要 canonical、dogfood 和受影响平台投影。验证本次 package／runtime 与原安装 owner 的定向 reapply／drift、受影响 sidecar 和 mode 条件。

只有实际改动需要证明干净安装时，最多运行一个代表性 throwaway。完整多平台安装／升级／Release 矩阵不属于本 Task。不得声称历史业务发布、旧 Draft 或生产效果已经由本轮重放验证。

## 6. 约束与依赖

- Markdown／AI 保留 scope、充分性、finding、readiness、revision 和 route 判断；脚本只执行、记录或校验确定性事实。
- 保留原构造及必要内部 consumer，实际继承或适配方案由所选 Delivery 设计展开；本 PRD 不新增实现接口。
- 正式 invoke、Preview、record、check、execute 的测试范围以真实直接调用关系决定，不要求每个错误与每个入口的全排列。
- 复用现有 transaction／remote recovery stateful fixture 的可观察动作，隔离真实 GitHub 写入；不得通过直接 assertRaises(WorkflowError) 或读取内部属性代替公共入口验收。
- #269／#361 的旧 Publication Review facade、#773 的 Branch LifecycleContractError 映射、#847 的 schema union 诊断属于相关边界，不扩大本 Task 的修复 owner。
- 本 Task 不新增配置、数据库、权限或发布接口；如实施调查发现确有必要的兼容变更，必须回原规划／范围 owner 处理，不静默扩大。
- 实施及分发采用仓库当前匹配版本的 canonical 与安装 owner；不得手工覆盖受管投影或绕过安装门禁。

## 7. 可观察验收与验证方式

| 验收 | 对应要求／场景 | 验证入口与输入 | 预期结果及证据边界 |
| --- | --- | --- | --- |
| AC856-01 | R856-01、06；S856-01 | 原生产 invoke wrapper，缺 readiness_result_id | schema_mismatch、依据充分的定位、安全纠正提示、exit 2；拒绝先于 Task／Publication 及 Git／GitHub 副作用 |
| AC856-02 | R856-01、06；S856-02 | 原生产 invoke wrapper，PR body含 Closes #435 | closing_keyword_forbidden、对应定位、安全提示、exit 3；拒绝先于副作用 |
| AC856-03 | R856-02、03；S856-03、04 | 按真实入口关系选取必要直接调用，并保留 invalid_json 对照 | 共享读取器行为保持；同一异常边界覆盖实际直接入口；内部 typed recovery 保持原出口和 consumer |
| AC856-04 | R856-03、04；S856-04、05 | 复用原 stateful fixture，观察正常发布与同事务恢复的适用路径 | 不绕过 gate，不重复完成动作；结果未知时先回读同一事务；不连接真实 GitHub 写入 |
| AC856-05 | R856-05、06；S856-06 | 定向公共边界测试与原输出检查 | 真正未知异常仍为安全 internal_error；实际退出码符合 catalog；公开输出不含禁止的敏感原始内容 |
| AC856-06 | R856-07 | package／runtime、canonical／dogfood／受影响平台、原安装 owner 的定向 reapply／drift 检查 | 必要分发一致，实际 sidecar／mode 结果明确；只声明实际验证层级，不宣称完整矩阵或历史业务发布效果 |

断言从 Direct Source 的输入、动作和可观察结果推导。实现与测试相互一致不能单独证明需求完成；修正输入后成功也不能代替失败诊断验收。

若某入口受 runtime、fixture 或环境前置条件阻塞，保留具体缺口，不把未到达目标行为的失败算作缺陷复现或验收通过。验证顺序、命令及所需补充覆盖由 Delivery 规划按最小可靠集合明确。

## 8. 实际未决项

当前整体需求没有需要用户决策的未决项。

后续 Delivery 设计须核对原异常全部实际 consumer、直接入口和安全字段来源，选择满足既定兼容约束的最小接续方案，并明确实际验证命令。这些是已明确范围内的技术工作，不构成新增产品问题。

当前尚未实施修复、执行修复后验收、完成分发验证或确认生产效果。Task 完成由原 Completion owner 对整体 accepted scope 判断。
