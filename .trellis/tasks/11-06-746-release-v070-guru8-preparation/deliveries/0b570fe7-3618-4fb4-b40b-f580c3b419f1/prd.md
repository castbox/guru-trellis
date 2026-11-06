# v0.7.0-guru.8 准备交付需求

## 1. 整体来源与术语

整体 accepted_scope 为本 Task 根 prd.md 的实际 sha256 revision；本批 scope_ref 选中全部 R1–R7、AC1–AC5。来源是 #746 的“准备任务”及完整私有发布合同 Stage 1。extension 与 Fork CLI 版本分别读取，dogfood 是实际 Task checkout 安装。规划根为 deliveries/0b570fe7-3618-4fb4-b40b-f580c3b419f1。

## 2. 整体与本批目标、非目标

本批为全量准备 D1：将 extension/maintenance/schema 和公开说明收敛至 .8，修正实际 Codex 入口语义，并由原 tools owner 更新 dogfood。公开说明保留 .7 为已发布前驱、.8 为候选，Fork 保持 0.7.0-castbox.6。

不执行本批之外的 tag、Release、post-merge smoke、发布后主仓更新与 Issue 关闭。不迁移历史 Task、不改上游或全局包、不实施其它 Issue、不升级业务仓库或生产环境。

## 3. 本批起点、前序结果、依赖与剩余责任

尚无前序 Delivery。开发基线 main@338e8fdc4eee80ffa9c44c00d5030b5f240ad4cd，PR 目标 main。canonical extension .7；公开 README 仍保留 .6/.7 旧发布说明。当前 lock 为 castbox/Trellis@17015f987166f4106034f115d23212446f16d536，CLI/Core 0.7.0-castbox.6。

本批依赖完整当前 preset、原安装 owner、干净匹配 Fork 构建。完成后 Task 仍需原 Completion/Closure no_mutation/Finish/Cleanup；发布协调继续在 main fresh candidate 上完成 Stage 2。PR 合并不等于 Task Completion 或 Release。

## 4. 本批调用方、场景与流程

S1：发布 Agent 读取版本与已发布 tag，更新 canonical/current-only 版本约束和用户文档；观察唯一正确映射与可执行同源命令。
S2：Codex/Claude/Cursor 调用 Skill，依当前受管清单读取；迁移公共 Codex 根与私有发现投影分别处理，退休路径不复活。
S3：tools owner 从完整干净已提交源码 source_locked 更新本工作区；实际验证 managed bytes、source lock、CLI、provenance，同时保留 Task/session/user data。
S4：原 Check/TaskCommit/独立 Branch Review 在晋升前后分别审查完整内容；零开放 P0–P3 后进行中文 Refs-only 交付和正常终态。

## 5. 完整行为、条件与约束

R1：extension 和 maintenance target 统一 0.7.0-guru.8，相关 const/schema/必要测试按实际 consumer 更新；Fork 与 lock 不变，不改历史版本证据。
R2：root、workflow、preset README 和 public-docs 说明真实 .7 前驱与 .8 准备状态。发布前安装使用同一已存在 immutable tag 或实际 remote-addressable candidate SHA；不得把尚不存在 .8 tag 当可用 provider。
R3：私有 release 合同的 source/platform Gate 按当前 Codex shared root 调整，并核实际私有 Skill 副本，不进入公共 registry/manifest/package。
R4：真实 dogfood tools 更新必须通过原 owner；缺干净来源时采用其已提交来源路径。安装变更回原 Check/TaskCommit/完整 Review；throwaway 或历史 Task self-reapply stop 不替代真实安装。
R5：稳定 design/implement/Docs Plan；按规范性来源设计处置采用两次完整独立 Review、串行知识晋升和 fresh post-promotion Check。任何实质差额刷新受影响 gate。
R6：中文 PR 仅 Refs #746，不使用关闭关键词；Completion 只覆盖准备范围，Closure no_mutation，Finish/Cleanup 保留原职责。
R7：不生成发布状态持久化或授权记录，不把脚本当 semantic pass。保留未验证边界。

规范性来源设计逐项处置仅由本批 design 第3节维护；本需求不另建第二矩阵。

## 6. 本批验收、验证方式与未决项

AC1：读取 canonical/maintenance/schema、README 与 current public-docs，检查版本映射和真实状态；执行与版本 consumer 相关的现有验证。
AC2：执行 source、installed、当前 Shared/Codex/Claude/Cursor 投影验证和私有 release Skill 字节比对；检查私有 Skill 不在公共 inventory。
AC3：原 tools preview/prepare/invoke、实际 target/native-entry validation 证明真实 dogfood 与已审查来源一致；检查保留内容无损、sidecar 无未处理。
AC4：晋升前后两轮原 Phase 2/TaskCommit/独立完整 Branch Review；实际晋升字节包含在后续候选中。
AC5：Refs-only PR 与 public Delivery 正常交付，原 Completion/Closure/Finish/Cleanup 完成，main 可查终态归档，#746 保持开放。

无必要未决需求选择。实际源码、构建或验证缺口如实返回原 owner；不以计划预填 pass。

## 7. Canonical 引用与本轮差额

- .trellis/spec/docs/public-docs.md：当前版本/安装说明；本轮只修正现行发布段，不翻新历史观察。
- .trellis/spec/docs/requirements-design-test-ssot.md 与 docs/{requirements,design,test}/README.md：由原 RDT owner 判断当前知识差额与适用历史边界。
- .trellis/spec/architecture/baseline-usage.md 与 docs/architecture/README.md：由独立 Architecture owner 判断版本/投影/真实安装对现有边界的影响，不把发布等同架构改造。
- .trellis/spec/preset/installer.md：原 source_locked 安装与保留行为。
- .trellis/spec/workflow/quality-guidelines.md 的验证价值与范围：使用真实入口和必要回归，不制造固定版本自证测试。
