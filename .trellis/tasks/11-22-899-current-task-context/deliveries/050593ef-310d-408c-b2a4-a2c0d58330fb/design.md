# D1 标准续接只读上下文设计

## 1. 设计目标、需求与基线

D1 承接本批 PRD 的 AC1、AC2。开发基线 B 和规划时 HEAD 都是 `f06eddb6ccf97ddd2d1a41c117692f5957cb2dc7`。独立集成目标为 `castbox/guru-trellis:main`。阶段权威为 `guru-trellis-architecture`、`guru-trellis-design-constitution-v1` 和 `guru-trellis-architecture-change-contract-v1`。独立 Architecture 候选评估选择 `target_native`，决策引用为 ADR-035 和 ADR-STEP-CONTEXT-LOADING。

## 2. 当前系统、边界与目标差额

标准续接先核对当前会话，再解析 Task 与 checkout，最后读取当前 Delivery。上游 `delivery.py current --json` 读取官方选择。Guru 的 Ensure 另外验证 C4 分支绑定、C5 资源归属和唯一登记 checkout。新入口在同一进程组合已有读取，不修改 Fixed Fork 安装文件。

## 3. 来源设计处置

#899 的约束是复用既有查询、保持只读及保留原恢复职责。#736 提供来源范围。两者均未指定 CLI 字段或缓存实现。ADR-035 规定的原写入与续接边界继续适用，标准路径改用下述公开读取。

## 4. 模块与职责

| 位置 | 责任 |
| --- | --- |
| `trellis/workflows/guru-team/scripts/bash/read-continuation-context.sh` | 新增公共只读 launcher，沿现有 managed Python 调用模式分发。 |
| `trellis/skills/guru-team/runtime/` | 组合 Task/session、C4/C5 checkout 及官方 Delivery 读取。仅为共用读取提取所需最小函数，保留现有 wrapper、schema 和错误语义。 |
| `trellis/workflows/guru-team/workflow.md` | 在唯一续接段采用一次读取，按 Markdown 原规则判断当前义务与后继 owner。 |
| `trellis/presets/guru-team/` | 分发对应 runtime、wrapper 和公开使用说明。同一匹配源同步 dogfood 与命中的平台入口。 |

## 5. 接口与数据

公共命令为 `bash .trellis/guru-team/scripts/bash/read-continuation-context.sh --root . [--input -]`。省略 `--input` 时读取本次官方会话的当前选择。提供 `--input -` 时从 stdin 读取以下闭合对象。版本与模式必填。

| 字段 | 约束 |
| --- | --- |
| `schema_version` | 固定为 `1.0`。 |
| `intent` | `continue_session` 读取当前会话。 `inspect_task` 使用原只读显式入口。 |
| `task` | 可选的 `{task_id,lifecycle_generation,task_ref}`。`inspect_task` 必须提供三个字段。 `continue_session` 提供时只断言所续接的同一对象，并可定位缺失绑定的恢复。 |
| `delivery_id` | 可选，须有 `task`。续接模式下只断言现有选择。显式读取模式只在原显式查询允许时读取精确对象。未给定 ID 时不从清单选择。 |
| `previous` | 可选，限 `continue_session`。调用方直接传回同会话上次成功查询的完整结果。解析器只采用匹配当前依赖的部分。 |

最小的会话查询是 `bash .trellis/guru-team/scripts/bash/read-continuation-context.sh --root .`。显式读取示例用 `--input -` 传入 `{"schema_version":"1.0","intent":"inspect_task","task":{"task_id":"example","lifecycle_generation":0,"task_ref":".trellis/tasks/11-22-example"}}`。有适用上下文时，入口执行原合法对象约束。另一有效选择、stale 或不支持版本返回原诊断。显式读取返回的事实带 `mode=explicit`，会话结果为 `mode=session`。

每个结果都含 `schema_version`、`kind`、`mode`。下表的附加字段按 kind 固定。Task 信息为 `{task_id,lifecycle_generation,task_ref,checkout_path}`。Delivery 信息为 `{delivery_id,phase,planning_root}`，依附返回的 TaskKey。

| kind | 额外字段 | 直接消费者 |
| --- | --- | --- |
| `current`、`terminal_delivery` | `task`、`delivery` | 原精确 Delivery 读取及 Workflow 分流，终态交原终态入口。 |
| `no_current_delivery` | `task` | 原整体 Task 义务路由。显式查询未请求交付对象时仅返回已验证的 Task 定位。 |
| `no_current_task` | 无 | 原 No-Task 入口。 |
| `binding_required` | 原请求的 `task_id`、`lifecycle_generation`、`task_ref`，以及 `diagnostic` | 原 Bind 的 missing-session profile。 |
| `error` | `diagnostic` | 原诊断/契约 owner。 |

`diagnostic` 包含原 `code`、`field_path`、`remediation` 及定位该回程所需的 `owner`。原读取若只有 code/message，保留原 message 并由 Workflow 的既有路由映射消费。身份或代际归 Identity，绑定缺失或失配归 Bind，C4/C5 与登记不匹配归 Ensure/Branch，Delivery 选择与 profile 归原选择或维护入口。已识别的旧记录保留现有 `maintenance_required` 行为。调用参数错误沿公开 CLI 错误返回。

会话的三类成功定位结果额外携带一个 `reuse` 对象。它只用于下一次相同会话调用，包含 `origin` 与对应存在的 `task`、`checkout`、`delivery` 依赖标识。入口依据当前仓库 common-dir、官方 context 和依赖表重新核对，绝不采用单个标识推定整次成功。origin 失配时读取本次事实。局部依赖失配时重建该项和受其影响的后续项。输入和输出都不公开原 session key，不写恢复凭据。例：第二次把首个成功结果作为 `previous`，再次发送 `intent=continue_session` 和版本 1.0。

## 6. 顺序与刷新

先定位本次会话与当前绑定，再核对 TaskId/generation、C4/C5 关系和 Git 登记，再读取官方 Delivery 投影。每一调用共享实际读取到的身份和定位。可复用结果仅在同一会话和同一仓库内有效。入口重读独立的依赖事实，用已匹配部分承接仍有效的投影。Task 或 checkout 关系变动刷新依赖它的结果。仅 Delivery 变化不使已验证的 Task 位置自动失效。按以下依赖核对前次结果。使用原读取对象和本次调用内的共享快照，避免为计算一个全局 token 再执行全链。失去前次结果时直接读取。前次结果没有写入授权或阶段资格。

| 可复用事实 | 每次调用读取或核对的当前依赖 | 变化后的处理 |
| --- | --- | --- |
| Task 身份与 TaskRef | 仓库 common-dir、官方当前 context 对应绑定、TaskId/generation、当前 Task 记录和来源身份 | Task 或来源变化时刷新身份及其下游，普通 stale 转原 Identity 或 Bind。 |
| checkout 位置 | 同一 TaskKey、C4 绑定、C5 归属和 Git 已注册路径、分支及当前实际 checkout 对应关系 | 只采用仍匹配的定位，实际登记不符交原 Ensure/Branch owner。 |
| 当前 Delivery 定位 | 当前 schema-3 绑定的 DeliveryKey、相同 Task generation、选中记录的 phase、planning_root 和 profile，以及匹配 workflow 声明 | 变化时重投影 Delivery，保留有效 Task 和 checkout。终态交原终态或发布恢复入口。 |

Workflow 在已绑定标准续接调用此入口一次。相邻原 typed exit 继续经原 discovery 映射。无当前 Task 进入原 No-Task entry。已绑定且无当前 Delivery 交现有 Task 义务。当前 Delivery 将精确 TaskRef、DeliveryKey 与 checkout 交原 phase owner。原恢复可能写入时由原入口以相同对象执行。核对失败保留原 code、field 和解除条件。

### 阶段分流前的原权威读取

取得 current 或 terminal_delivery 时，Workflow 在分流前使用返回的 TaskRef、已验证 checkout 和 DeliveryKey 读回该精确 Delivery 的官方 public record 及 gate applicability。选择目标由本次解析给出，后续精确读取不再解析会话、分支或 checkout。读取发生在同一流程步骤，确认所读 record 仍属于返回的 generation、key 和 profile。读取错误或关系变化回原 owner。此处复用原公共 Delivery 读取接口与适用性计算，新增上下文结果只负责定位，不携带门禁结果。

如果选定 Delivery 有 Publication PR，使用它的精确 repo、PR 编号和适用 head 通过原 repo-bound GitHub 查询读回真实状态，然后再使用阶段表。真实 MERGED 先进入原 Merge recovery。原显式选择已合并 PR 但缺少 Publication 时，沿原 adopt 入口。只有实际 delivered 进入 Completion。没有 Publication PR 时继续原分流。按原 public gate applicability 和原 producer 结果消费各阶段事实。只有当前适用的 approved 进入 Activation，缺失或过期的结果回原 producer。正在 checking、reviewing 或 publishing 时继续原阶段对当前 Check、full_review 和 readiness 的要求。


## 7. 恢复与兼容

原会话恢复、显式读取、Delivery 终态和维护各用原 owner。部署通过匹配 workflow 与 preset 成套更新，旧版本继续使用原完整入口。已有资源和可恢复事务用原合同续接。新入口无状态写入和数据迁移。实施中如证实需要改变上游 API 或支持范围，先回 Architecture 或 Clarify 处理该差额。

## 8. 验证

先运行同一公开入口的正常续接旅程。使用真实注册 checkout、Task 和会话绑定。覆盖当前、无 Delivery 和终态结果，并验证一次调用、重复复用和受影响事实刷新。比对 Task 文件、会话记录及 Git 资源前后状态。补验无 Task、已知 Task 缺少绑定、合法显式只读及实际 stale 或旧合同诊断。采用仍适用的原恢复证据。定向运行 source/installed 行为、平台投影、reapply 和 drift 验证。

## 9. Canonical 与未决点

需要更新续接 RDT 和 Workflow Context 对应正文，保留同一权威和实际受影响引用。隔离 Architecture 贡献位于本 Delivery 的 `research/architecture-proposed.md`，负责说明 Workflow Context 和 ADR-035 的承接差额。沿原 final_integration 由 Architecture owner 写入实际当前定义并读回。既有 ADR 已记录唯一续接和 owner 划分，本轮延伸现有决定。实现须证明复用能通过真实读取依赖保持结果适用性。旧记录样本和平台投影范围按当前支持合同核实。
