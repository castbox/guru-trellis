# #481 设计

## 来源与版本

精确上游候选：`castbox/Trellis@64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac`，parent `8336e78b8fafe2a4bc4ea3d01815a61cf4f08983`，tree `a964088ffa3f8df0deafc8f042f91911e3e8ecbe`，main CI `36755826713` 成功，CLI/core `0.7.0-castbox.1`，`pnpm@10.32.1`。本地冻结安装和构建、CLI 版本及单平台 clean init 已成功；后续仍须验证 Guru 安装投影和候选 source validator。来源锁只在验证后更新，README/manifest/installed record 同步。

## 合同变化

1. `guru-create-task` 直接迁移 public input 1.0 的 task object，移除 `creator`/`assignee`，调用上游 `task.py create` 时只传 title、description、slug、TaskId、source、base 与 no-start。旧字段由闭合 public schema 拒绝。上游 task schema 的字段集是 current authority；Guru 不再把 `delivery_target` 写入 task.json 顶层。创建调用的 reviewed delivery target 仍由调用方提供，创建器校验其 repo_ref 与当前 GitHub 仓库精确相同，branch_ref 与选定交付分支精确相同；新任务只持久化官方 `base_branch`。后续交付目标由各阶段既有的独立 reviewed input 与 live repo facts 获取，不从 task.json、人员身份或自由文本恢复。逐一检查当前读取 `task.json.delivery_target` 的 consumer，并随创建路径同步收敛。
2. current task reader、TaskId 唯一性与 archive discovery 分离：当前/正常归档必须完整符合当前上游 schema；旧归档只读 `id` 作防复用碰撞检查，绝不读取人员字段。针对显式 TaskId 或 Issue 的旧档案只读定位并返回 unsupported-legacy 诊断。结构化 source 存在时只匹配 `issue + exact_source + exact repo_ref/number`；缺 source 才考虑精确 finish-summary Issue 索引或 canonical scope，两种线索冲突或候选不唯一报歧义。缺线索时不猜测，也不阻塞无关当前任务。不得用这些线索恢复生命周期。
3. Reactivate、Finish re-entry、session/branch recovery 的入口使用同一当前 schema 边界。符合当前 schema 的归档继续遵守 #454 的终态 Git identity；旧档案只拒绝。C4/C5 结构、所有权和终态退役时机保持原样。
4. `trellis-brainstorm` 的安装投影采用上游新需求探索文本；当前 `guru-clarify-requirements` 只消费探索产物。Phase 1 author 的全局替换留给 #292。
5. canonical Skill package/runtime、preset/overlay、dogfood 与声明平台从同一源同步。当前主动询问或提供人员参数的上游模板投影随精确 Fork 候选更新；历史任务、归档、旧迁移说明可保留退役字段名称作为诊断文案，不作为活动接口。公开 schema/CLI 破坏性边界在迁移文档与 README 中写明，拒绝旧输入而不加适配器。现有 C4/C5 branch/session/resource store 原样保留其独立 ownership 语义；不引入兼容双读、人员别名或迁移写入。

## 版本与文档权威

本次 Fork 的 CLI/core 版本是 `0.7.0-castbox.1`；extension revision 随新受测 Fork 边界前进为 `0.7.0-guru.1`。当前未发布的仓库目标 tag `v0.6.17-guru.2` 先保留为独立轴，不在 #481 制造 tag/Release；后续发布 owner 必须基于合并后的精确候选重新决定 tag。manifest、source lock、安装 provenance、README 与 current RDT/Architecture 投影分别标明这些轴，不能沿用旧 `0.6.17` 安装证明。

## 风险与证据

- 当前 Guru dogfood 使用旧上游模板，且旧归档含人员字段。要区分合法历史的只读 ID/Issue 诊断与当前任务 reader，避免把存在本身视为当前候选。
- 任务创建、source lock、installer 和 package/平台投影跨层；测试必须覆盖调用链，不只比对字符串。
- Source commit 的 CI 与本地 clean init 已有初步证明；Guru installed 与 update/reapply 结论只能由本次候选的实际运行给出。完整多平台矩阵保持 deferred。
