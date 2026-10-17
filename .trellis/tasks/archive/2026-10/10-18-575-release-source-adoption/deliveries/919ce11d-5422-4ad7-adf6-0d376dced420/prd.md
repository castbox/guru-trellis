# D1：正式来源采用与发布准备路径

## 来源、身份与边界

Direct Source 为 [Issue #575](https://github.com/castbox/guru-trellis/issues/575) 的正式依赖前置、Stage 1 和 Stage 2 第 2、4、6 项。选择的规范性约束为 `trellis/presets/guru-team/MIGRATION-577.md` 的依赖与采用边界。当前用户要求完成 Guru `.4` 发布；本 Task 只拥有下列独立准备单元。

TaskId 为 `575-release-source-adoption`，generation0。来源 disposition 为 `reference_only`，准备 PR 使用 `Refs #575`。旧准备 Task 与 #577 的完成和历史归档保持。本 Task 不重建或重开旧 Task，不承担 tag、smoke、GitHub Release、发布 Issue 关闭或资源清理；这些操作由 #575 Stage2 原 owner 单独完成。

## 当前缺口与要求

### R1：正式采用完整配对来源

采用正式 `castbox/Trellis` PR #52 merge `7bcbeaad31380e7a29c97898cb947c6120a61775` 的完整 commit/tree/parents/成功 CI、CLI/Core `0.7.0-castbox.4` 和 `pnpm@10.32.1`。唯一 source lock、受管来源投影及当前公开直接映射必须一致。实际采用使用干净匹配 workspace source build；已有 `/tmp/guru575-fork-7bc-source` 仅是调用期机器位置，不进入共享来源合同。

严格 `source_locked` 的 source/build/bytes/modes、版本、manifest、API/capability 检查保持。packed tar 的 Python mode 差异不能通过绕过校验解决。不得修改上游、全局 CLI、node_modules 或发布 Fork/npm。README 和 MIGRATION577 只追加本次真实采用边界，不将 #577 的 local_candidate 历史改写为正式采用。

### R2：支持正式 clean workspace 的原 Plan2 路径

原 Plan2 `delivery_upstream.packages()` 将 Core 固定为 CLI 父目录下 `trellis-core`，正常 source workspace 的实际 Core 位于 `packages/core`。原只读 preview 在公共迁移前报缺 `packages/trellis-core/package.json`。通过 CLI package 的正常 Node dependency resolution 定位 matching Core，复用现有公共包，不新增公共模型、owner 或备选迁移路径。

保留 packed matching layout 的正常支持及匹配版本/API拒绝语义。原 Plan2 全 inventory 的 `history_only` 正常审查、迁移与 reapply 由原升级 owner 完成；不伪造 checkpoint，不绕过旧归档 guard，不修改历史 Task 为符合预检而制造状态。用户任务、归档、会话、绑定和配置按原迁移写集与保留合同处理。

### R3：分别绑定 predecessor 与当前 CLI 轴

私有 release contract 的 predecessor upgrade cell 必须从真实 predecessor tree 的 manifest/source lock 推导 `predecessor_cli_version`，与同来源 `predecessor_fork_commit` 一起传给原 verifier 的 `--before-cli`。当前 `official_cli_version` 继续表示当前候选 CLI；不能用当前 `.4` 替代 predecessor `.3`。同步私有 Skill 四份合同，不增加第七发布输入，不放宽 verifier。

### R4：定向工程验证与真实采用

验证三类差额：正式 source/build/API 与 lock/公开映射；Plan2 workspace 与 packed 正常解析、错误配对版本拒绝及同 inventory 原 preview→正式 history_only 路径；predecessor tree 自身 CLI 推导和四份合同 byte parity。source/installed、Shared/Codex/Claude/Cursor 投影、ownership、dogfood reapply/drift、sidecar/权限、diff hygiene 和变更范围真实 secret scan 依实际改动覆盖。

至少一个代表性隔离旧安装须经原 source_locked tools/Plan2 owner 实际采用匹配来源，目标自身原生 continuation 和下一实际 consumer 的可用性按层次报告。保留首次失败、同输入修复后结果与未验证边界，不以静态字段、历史单测或上游 CI 替代本仓实际采用。最终 main exact-candidate、远端 provider、tag smoke 与软件发布留 Stage2 fresh gate；完整多平台/native-host/真实业务/生产链路不由此准备单元宣称。

本轮真实采用发现：公开 tools writer 的 AGENTS target 与随后原 Guru installer 写入的合法 Guru block 不同，导致正常成功升级后的原 public rollback 报 later_work_conflict。R4 增补限定修复：由原 Guru tools prepare owner 在第一次 public apply 及 checkpoint 冻结前，合成 Core 公开 plan 的 AGENTS target 与 canonical Guru-owned block。原 public writer 写入该固定目标；保留 operation/source/candidate/guard、原 Task/session compatibility 检查及原 rollback 顺序，不修改已失败 checkpoint，也不提前恢复 Guru 内容来绕过 Core 检查。公开 plan 的字段可读写本身不构成机制合法性；其消费及 Guru block 所有权必须由原合同具名说明。模板 hash 仍描述原 Core 模板基线，不冒称包含 Guru 定制。

原失败样本保持，修复使用等价新 predecessor 隔离样本。验证实际 upgrade→目标原生 continuation/下一 consumer→原 source rollback，并证明 managed block 外内容与原 Task/session 保留；恢复失败不以 preview 或字段检查冒充成功。新增 owner 协作风险由 fresh Architecture implementation_discovery、候选和最终计划评估承接，再走原 Check/Review。

### R5：长期文档与完整交付

原 RDT owner 为本次需求、设计与测试建立唯一长期增量，实际执行结果只由该唯一 Test 维护。Architecture 影响由独立 owner 判断；有真实贡献时在原 Phase2 promotion 机制执行，不为留证明写重复文档。本 Task 用一个 pull_request Delivery 完整覆盖 R1–R5，依原 Check、Task Commit、独立完整 Branch Review、Delivery、Completion、reference-only Closure 和 Finish 完成。

## 验收责任

| 验收 | 可观察结果 |
| --- | --- |
| AC1 | 正式 PR52 commit/tree/parents/CI/CLI/Core/package manager 相符；唯一 lock、受管投影和直接公开映射一致。 |
| AC2 | 严格 source_locked 从真实干净配对 source workspace 成功采用；版本/API/mode 检查未放宽，历史 #577 结果保持原归属。 |
| AC3 | 原 Plan2 在实际 workspace 与 matching packed 布局解析正确 Core；错误配对版本拒绝。相同旧 inventory 沿原 preview/history_only/reapply 成功，保留数据与原写集。 |
| AC4 | predecessor CLI 从自身 manifest/lock推导，原 verifier 接受正确旧轴；私有合同四份 byte parity，发布输入仍六项。 |
| AC5 | 实际改动的 source/installed/投影/ownership/drift/sidecar/权限/secret/diff 定向检查和唯一长期追踪完整；未验证层次明确。 |
| AC6 | 准备 Delivery 与 Task 正常终结，#575保持 OPEN；未创建 tag/Release，未修改旧归档或实际业务安装。 |

以上是要求，不是通过声明。具体机制、源约束处置与固定内容基线由本 Delivery 的 design 独占；Delivery Policy 和 Docs SSOT Plan 由 implement 独占。

本 Delivery 交付整体 R1–R5 / AC1–AC6，没有后续准备切片。
