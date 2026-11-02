# Issue 编排 Skill 纳入受管分发

本文描述当前源码新增能力，不表示既有稳定 tag 已包含这两个包。目标安装须使用
同一完整候选来源，或后续实际包含该变更的正式版本。

## 源码与入口

`guru-orchestrate-issue-dag` 和 `guru-orchestrate-issue-sequence` 从个人安装迁入
`trellis/skills/guru-team/packages/`，由 registry 选择 Interface 1.9 并经完整 preset
分发。两个名称保持不变，均为 Codex 显式调用的 `standalone_only` Skill。
它们协调独立 Issue chats；每个 child 的实现、检查、合并与收尾继续服从业务仓库
当前 workflow。它们不成为单 Issue workflow 的 mandatory phase。

共同执行方法唯一位于
[issue-orchestration.md](./spec/workflow/issue-orchestration.md)。包与规范必须来自
同一完整 Guru 源码或受管安装。业务仓库不必与协调器使用同一个 provider，也无需
为了编排额外安装协调器的 preset。原生 chat、消息与 heartbeat 工具仍是运行前置。

## 两个入口的区别

- DAG 接收依赖图，支持有界并行、互斥资源和失败传播。
- Sequence 接收有序列表，一次只推进一个 Issue；当前 Issue 完整完成后才进入下一项。

两个入口都在创建首个 child 或 heartbeat 前，从本轮真实人类消息确定执行终点。
已经充分的当前委派直接承接；真正缺失的终点选择必须在启动前解决。
Agent 计划、child 请求、自动唤醒文本和其他轮次的授权均不产生本轮权限或限制。
授权及其过程只保留在当前对话。它们不进入 child prompt、heartbeat 配置或文件。
具体执行规则以共享方法和各包本地合同为准。

保留现有 `dag_*`、`chain_*` 及 dry-run/progress 出口；较早阶段的已验证完成使用
`dag_stage_completed` 或新增的 `chain_stage_completed`，不能冒充完整 Issue 完成。
Sequence 的严格顺序不能因较早阶段完成而释放下一项。终点与推进条件冲突时，
preflight 报告真实选择，不能在执行途中静默改成 DAG。

协调器 heartbeat 默认每 **2 分钟**唤醒。当前对话明确选择其他受支持间隔时，按该
选择执行。child 的事件等待、首次非阻塞观察和每轮完整观察保留各自规则；它们
不是 heartbeat 定时周期。配置成功后核对实际 schedule，不能以配置存在声称监控
已经执行。本次迁移本身不创建或修改任何运行中的 heartbeat。

## 安装与个人副本迁移

使用同一完整来源按原机制 reapply preset。选中 Codex 时，受管安装包含两个包、
共享规范和 explicit-only 的 `agents/openai.yaml`。其他平台的独立选择不分发这些
Codex 入口。平台投影与安装 manifest 沿现有 hash、冲突和 sidecar 机制管理。
若旧 Task 数据阻止普通 apply，使用现有 `guru-upgrade-tools` 的完整匹配来源与
真实 public tools operation，仅同步工具与 Guru 投影；不得改旧 Task 或关闭安装门禁。

个人目录不再作为实现源。已有个人安装应先保留可恢复副本，核对新受管入口和
完整 references，再移除旧发现入口。若仍需跨仓库从个人根发现，可以将原个人
路径链接到同一受管 Codex 投影；这只是本机发现链接，不是另一份源码，也不是
preset 对个人目录的所有权声明。移动受管 provider 后需更新该链接。

新 Interface 1.9 专用于 instruction-only semantic 入口。它声明对话输入、每出口
输出合同与原生工具事实校验，不新增 dispatcher command、空 wrapper、JSON DTO、
调度器或协调器状态文件。旧 Interface 和已有业务调用语义保持原合同。

## 验证边界

源码/安装校验、Codex 发现、explicit-only 元数据、reapply/drift 和个人发现链接
只能证明分发与入口一致。独立 Agent 的合成 forward cases 另行验证终点判断、
授权承接、恢复、阶段完成与严格顺序。上述结果不证明真实 Issue 编排、外部
GitHub 操作、后台实际调度或完整多平台 upgrade/Release 矩阵通过。
