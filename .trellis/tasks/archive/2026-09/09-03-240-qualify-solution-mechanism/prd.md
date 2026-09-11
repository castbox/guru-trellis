# 建立 AI 驱动的解决机制资格合同，禁止业务能力下沉到 OS 原语

## Goal

解决 GitHub Issue #240：建立独立的 `guru-qualify-solution-mechanism` semantic owner，判断拟采用的解决机制是否把业务能力下沉到 OS 原语，并将该资格判断接入 Guru Team 的完整生命周期。

## Requirements

1. 解决机制资格必须与 `guru-qualify-normal-scenario` 的问题场景资格完全分离；前者只判断机制，后者只判断场景。
2. 以下机制不得承接业务正确性、业务身份、并发、fencing、monitor、inspection、cancel、恢复、发布门禁或业务 evidence：OS lock、`flock`、`fcntl`、lock file/inode ownership、`/proc`、PID/PGID/SID/process tree、生存扫描、FD identity/inheritance、signal/kill/process-group control，以及同类 kernel/process/descriptor authority。
3. 普通目录和文件的创建、读取、写入、重命名、移动、列举、删除、配置/日志/cache/artifact/durable state 保存及内容检查保持允许；文件存在、inode、FD、打开状态或 lock file 不得被解释为业务 authority、fencing、leader election 或并发协议。
4. 资格判断覆盖业务代码、Runtime、Infrastructure/deployment helper、Framework/shared library/internal platform，以及 monitor、inspection、cancel、recovery、validator 和 evidence producer；封装、测试通过、fail closed、race/TOCTOU 或生产压力不构成例外。
5. 新 Skill 必须直接读取当前 requirement、planning、architecture/spec、真实 dependency/caller graph、diff、tests 和 repository contract；不得使用关键词/import/命令名/路径扫描器替代 AI semantic judgment。
6. 缺少 live architecture、dependency graph 或完整 candidate set 时必须 `blocked`；命中禁止机制只能 `mechanism_revision_required`，路由回原 owner 删除或替换，不能降级为 scope confirmation。
7. Skill 不创建 tracked qualification report、candidate ledger、审批、签字、assignment、跨阶段 handoff 或持久化资格结果；输出只包含当前 invocation 的最小 typed result。
8. 既有违规业务实现只报告 repository、owner layer、consumer 和业务能力；本 Issue 不跨仓库迁移、不执行生产取消/恢复/部署/数据操作。

## Acceptance Criteria

- [ ] `guru-qualify-solution-mechanism` 是唯一解决机制 semantic owner，并有独立 Interface、contract、schemas、tests、runtime wrapper 和四平台投影。
- [ ] workflow 显式接入 planning approval、implementation discovery、Phase 2、Branch Review、Publication，以及 task-free 首次写入/机制演化；调用方只提交 candidate refs 和 live locators。
- [ ] `qualified_application_mechanism`、`mechanism_revision_required`、`blocked` 语义及唯一 consumer 映射闭合；禁止机制不会进入普通 scope confirmation。
- [ ] deterministic recorder/validator 只检查 shape、identity、freshness 和 consumer binding，不判断机制语义或架构充分性。
- [ ] paired production eval 覆盖 `/proc`/FD authority、隐藏 `flock`、PID/signals cancel/recovery、普通文件操作例外、lock-file 互斥、数据库事务/state machine，以及“已实现/已测试/安全/race/TOCTOU/fail-closed”压力框架。
- [ ] canonical、dogfood、Codex/Claude/Cursor、preset manifest、README/spec 与 workflow 投影一致，且无 `.new`、`.bak`、drift 或 caller-local 资格算法复制。
- [ ] targeted package/runtime、canonical/installed/platform/reapply/drift/sidecar 验证通过；完整升级/发布矩阵作为其专门 Issue 的边界，不在本 Issue 声称通过。
- [ ] 独立 Branch Review、PR readiness、merge 和 live Issue closure 完成后，本 PR 只关闭 #240。

## Non-goals

- 不修改 #237、#239，不成为 v0.6.5-guru.8 blocker。
- 不批量修改业务仓库，不新增人工审批或文件传递式协作流程。
- 不用静态关键词扫描取代 AI 判断，不把本 Skill 变成固定技术选型清单。
