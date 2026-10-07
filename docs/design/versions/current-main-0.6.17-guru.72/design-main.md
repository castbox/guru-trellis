# 独立迁移设计

版本：`current-main-0.6.17-guru.72`；状态：`active`；predecessor：`current-main-0.6.17-guru.71`。完整继承[不可变前驱合同](../current-main-0.6.17-guru.71/design-main.md)；除下文明确修订的独立迁移边界外，既有 requirement/design/test、无人员模型、source disposition、owner、历史拒绝边界、NFR 与 trace 继续有效。前驱 source、计数和证据只表示历史快照。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.72` / `active`。知识版本不是软件发布。

- `D495-INVENTORY`：独立 semantic `guru-upgrade-installation` 从目标 Guru source 加载，拥有来源、任务映射、本地修改、live delivery 与恢复/回退适用性的 AI 判断。其 public profiles/outputs 分别定义，完整 inventory/action plan 留在 call-local/private 恢复边界。
- `D495-CORE`：Fork 正式 `trellis migrate --from 0.6.16 --plan <private-plan> [--dry-run]` 复用官方模板/update ownership；只执行 AI 已确定任务投影与文件动作。普通 update、init 和 task writer 不放宽。
- `D495-MIXED`：当前严格目标 reader 与 raw identity reservation 复用；正向 known-legacy 识别仅提取 id/ref 占用，不作 current candidate。Fork 私有 `deferred_tasks` 只含 reviewed TaskRef 与 expected 原字节 hash，明确 preserve；Guru installed validator 同步该处置，未诊断旧 active/普通 drift 仍阻塞。不得 catch-all 跳过当前格式错误，也不得生成旧 binding/gate authority。
- `D495-GURU`：专用 migration 校验旧 provenance 和 exact managed bytes，备份后显式退役旧 Guru 管理资产，再使用当前 marketplace/preset owners。不得伪造 current manifest，不把 upstream-owned entry 移入 Guru ownership。
- `D495-LIFECYCLE`：复用 establish → ensure → bind-session → fresh Planning。已提交旧 task 的 id/status 和 generation 0 可建立现有绑定，转换后的 working-tree task 支持 dirty resume；不添加第二 binding writer 或迁移专属长期 profile。
- `D495-RECOVERY`：备份仅实际动作路径、control/session 变更与新增路径；最小 checkpoint 记录完成动作供同 owner 恢复。按 old/target bytes 识别完成，普通 drift 重新预览。rollback 不 reset Git、不重复发布，只在无新版工作时恢复原 bytes/modes。

部分 core 成功后按 coreplan.tasks 固定 rollback 直接消费的 task-content token 与相关非 preset control 初始基线；resume 不重新取 task 当前 bytes 作可覆盖基线。历史/业务/spec/规划精确字节保留，config 以有效设置保持并允许正式 owner 必需添加。Planning 接续须真实项目 baseline 与实际 qualifications/semantic gates。
- `D495-DISTRIBUTION`：canonical package/registry/manifest 和 workflow routing 是长期源头；正式 preset apply 同步 dogfood。Fork source lock 只能记录真实 commit/tree/parents/build/CI；本地候选不等于远端同源验收。

正式 Fork 固定 commit/tree/parent/build/CI，Guru canonical/preset 与平台投影仍各归原 owner。完整决策见 [ADR-017](../../../architecture/adr/017-legacy-installation-upgrade.md)；R495/D495/T495 的唯一映射见 [trace](./traceability.md)。

serialized promotion 绑定 expected `.71`，晋升候选代码/合同与本地证据，保留远端来源和旧交付样本未完成；晋升产生的 diff 必须重新 fresh Phase 2、Task Commit 与不同 reviewer 的完整 Branch Review 后才进入 Delivery。
