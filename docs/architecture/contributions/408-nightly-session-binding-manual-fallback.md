# #408 Architecture Contribution

状态：`draft` / `not_promoted`。Baseline为 `current-main-0.6.5-guru.50`，authority为 [Architecture README](../README.md)。绑定 `guru-maintain-architecture-baseline:2.0`、`guru-trellis-design-constitution-v1`、`guru-trellis-architecture-change-contract-v1`。

需求/设计/测试增量见 [RDT traceability](../../requirements-design-test-contributions/408-nightly-session-binding-manual-fallback/traceability.md)。Planning-stage required concerns与ADR判断见 [task design](../../../.trellis/tasks/09-14-408-nightly-session-binding-manual-fallback/design.md) 的 Architecture Planning Contribution。

## Boundary 与 Before/After

| 表面 | Before `.50` | Candidate after |
| --- | --- | --- |
| Framework source | a2003296 / CLI0.6.17 | db4ca1df / CI34838784963 / CLI/core0.6.17；正式build、TypeCheck、dogfood update与本地candidate focused安装验证通过 |
| Session | 既有精确session隔离 | 同session跨linked-worktree解析由已修复Fork提供；canonical与dogfood/isolated-installed回归通过，primary调用更新脚本定位linked task；Guru不复制resolver |
| Automatic stop | Guru typed stop终止自动流程 | 保留stop；独立用户Git/GitHub请求通过既有AI/tool authority处理，不赋予Guru完成状态 |
| Owner / graph | 现有workflow/Skill与Git/gh，23/97/78 | owner和图不变，无恢复节点、无第二checkpoint/授权存储 |
| Normal authoring | Agent文档的包内路径与投影不一致；Clarification/Readiness要求调用方预填自身派生数据，fixture以private计算掩盖缺口 | D408-05直接落实原recorder确定性职责，真实installed路径与正常authoring接续到创建/校验/激活；不把脚本变成semantic reviewer |
| Retired state | developer/workspace journal、ledger inactive | 保持，不读写或迁移历史数据 |

唯一change path为 `target_native`：直接演进现有应用级authority，不代表实施#398。当前方案不改变既有架构决策、single-writer、GAP生命周期或兼容退出，因此无新增ADR。

D408-05属于既有R408-03/04覆盖补漏。Workspace writer已有双端mapping逻辑，不重写或新增恢复入口；checksum只是已有owner的局部一致性值，不作为授权或跨Skill语义authority。正常authoring与完整recorded result由同一现有命令处理，公开输出不变。

## Evidence 与 Promotion

Project descriptor 为 `guru-trellis-architecture-convergence:repository:1`，protocol见 [change contract](../06-governance/change-contract.md)；适用 `ARCH-GOV-006..009`、`ADR-005/009`、`ARCH-GAP-006/008`。本任务不关闭或重开这些GAP。

本贡献只能在#408 worktree写入。当前source与三平台Guru投影一致，focused验证覆盖一个Codex clean项目和两轮同candidate update/reapply；`local_workflow_sample=true`，不证明远端exact-ref发布或历史predecessor完整矩阵。已安装官方模板移除了旧Guru检索注入和Codex agent文件中的显式子代理features禁用项；`.trellis/config.yaml`原字节保持，检索合同继续由项目workflow/spec与dispatch持有。

Phase2 project checks与独立committed Branch Review必须由各自owner完成；只读Agent演练不能充当实际远端操作证明，未执行的远端操作仍为UNVERIFIED。只有各owner按expected-current进行串行promotion后才能更新shared current，promotion diff须重新check/commit/Branch Review。此文件不存授权、审批过程或runtime恢复信息。
