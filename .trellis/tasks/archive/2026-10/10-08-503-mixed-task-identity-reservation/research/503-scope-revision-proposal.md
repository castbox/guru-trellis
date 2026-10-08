# #503 职责边界修订提案

此文件是待审阅提案，不替代 live Issue、批准规划或当前架构 authority。

## 拟发布到 Guru #503 的评论正文

正式 source 与 clean installed 创建测试暴露了两层相同根因：Guru `prepare_creation_inputs -> task_identity_reservation -> _read_identity` 和锁定 Fork `task.py create -> require_unique_task_id -> read_task_inventory_record`，都在比较 requested TaskId 之前，要求无关任务满足完整 current/受限 legacy schema。扩大 Guru legacy 白名单仅能越过第一层，正式 Fork 仍拒绝混合 header，不能完成本 Issue 验收。

修订本 Issue 合同为按 consumer 职责读取：

1. 身份占用扫描继续覆盖既有历史、registered worktrees、branch history 和 resource ledger；只消费身份所需的合法 TaskId、canonical locator 与冲突事实，不判定无关记录是否具有当前生命周期执行能力。
2. 目标 TaskRef 已占用、同 TaskId/casefold collision 继续拒绝。活动 metadata 的坏 JSON、非 object、缺失/非法 id 无法建立身份，继续具体拒绝。archive 与 branch-history 的既有缺损处理不在本次悄然扩张；保持其现有行为并定向验证。
3. 无关 metadata 中 source/generation/status/非身份字段不作为创建阻塞条件；合法 id 仍保留占用。这不是接受该记录为 current task，也不迁移其数据。
4. selected ref/id resolution 先用身份投影定位与检查唯一性，再对选中的目标严格校验完整 current schema、source、generation；旧/混合或无效目标继续给出 locator 与正式升级/逐案处置入口。
5. 升级 inventory/disposition 仍由升级 owner 使用完整 schema 分类，不复用身份占用投影作为 migration/lifecycle authority。创建后校验仍严格验证刚创建目标的 current metadata、gen0、planning、source 与 base。
6. Guru 本 Issue 替换原 legacy 白名单候选，修订对应 task-owned Requirements/Design/Architecture、spec 与验证；历史记录不批量改写。

Fork 官方 writer/身份扫描缺陷需独立 Issue 与正常 intake 承接；#503 的正式端到端成功依赖该修复及正式 source-lock/install 集成，不 patch Backend 或 installed Fork 副本绕过。当前两项正式创建测试仍失败，不声明 Phase 2 通过。

验收重点：同一合法 id 的历史记录仅改变无关 source/generation/header 字段时，身份占用结论不变化；但直接选择该无效目标仍拒绝。正式创建、ensure/bind/ref-id resolution、重复身份拒绝、坏身份拒绝与历史 bytes/modes 保持，在 source 和 clean installed 均验证。

## 拟创建的 Fork Issue

仓库：`castbox/Trellis`

标题：修复 task.py 身份占用扫描越界校验无关任务生命周期 schema

### 问题与证据

Guru #503 的真实正式创建路径在 Fork `0.7.0-castbox.3` / `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` 仍失败：`cmd_create -> require_unique_task_id -> task_id_collisions -> read_task_inventory_record` 在 requested id 比较之前返回 `task_metadata_unsupported-fields`。

正常历史记录含合法 id、旧 creator/assignee/subtasks 与 lifecycle_generation:1，缺少 source/completedAt。目标身份全新，创建只需要知道旧 id 是否相同，却要求旧记录具备完整 current/known-legacy schema。上游 Guru 白名单修订不能修复该官方 writer 失败。

### 需要解决

在 canonical `packages/cli/src/templates/trellis/scripts/common/` 修复身份读取职责。唯一性扫描只读取合法 id/locator 并比较 exact/casefold collision；selected task/session lifecycle 校验和 upgrade/inventory 分类按自己的 consumer 继续严格执行。审查复用同一 inventory reader 的真实 consumer，避免全局放宽 schema。坏 JSON/缺失非法 id 与 archive 既有处理必须明确，不 catch-all 跳过。

范围为上述缺陷直接涉及的 create、唯一性复用点及目标解析 consumer、合同与定向测试；不泛化重构全部脚本。dogfood 和正式安装投影同步，不修改业务仓安装副本，不批量迁移历史记录。

### 验收

- 正式 task.py create 在 registered historical worktree 混合 header 共存时可创建未占用身份。
- 合法 id 的无关非身份字段改变不影响占用判断；exact/casefold collision 与目标目录占用仍拒绝。
- 直接选择旧/混合或无效 current 任务仍拒绝；当前有效目标不被其他无关任务的非身份字段阻塞。
- 坏身份拒绝、失败资源不半创建、历史 bytes/modes 不变，canonical/dogfood/clean installed 一致。

关联：castbox/guru-trellis#503。由正常 intake 决定精确实施合同；本提案不包含 commit/push/PR/merge、发布、业务安装或部署。
