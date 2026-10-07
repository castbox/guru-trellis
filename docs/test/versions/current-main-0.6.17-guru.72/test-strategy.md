# 旧安装迁移测试策略

版本：`current-main-0.6.17-guru.72`；状态：`active`；predecessor：`current-main-0.6.17-guru.71`。完整继承[不可变前驱合同](../current-main-0.6.17-guru.71/test-strategy.md)；除下文明确修订的独立迁移边界外，既有 requirement/design/test、无人员模型、source disposition、owner、历史拒绝边界、NFR 与 trace 继续有效。前驱 source、计数和证据只表示历史快照。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.72` / `active`。知识版本不是软件发布。

| Strategy | 代表性场景 | 验证层 |
| --- | --- | --- |
| `T495-PREVIEW` | 精确来源、受管/本地编辑及所有任务投影；preview 零 repo 写入 | public source-loaded wrapper/private inventory |
| `T495-INSTALL` | core/task 转换 + workflow/preset 实际安装；config/spec/platform 定制保留 | 隔离 core0.6.16/Guru41 业务样本 |
| `T495-TASK` | 完整旧记录、两种精简记录、非 UUID、generation/source、关系/未知字段 | Fork unit + current writer |
| `T495-RESUME` | planning 与 dirty unpublished in_progress；真实项目 Architecture baseline、actual 两类 qualifications 与 fresh semantic plan 后 dev/check；新 task 正式创建 | 当前 owners public wrappers |
| `T495-DELIVERY` | PR/merge/旧在途分别诊断，provider 只读、不重复操作 | live Git/GitHub 与代表性样本 |
| `T495-RECOVERY` | core 已更新后 Guru 普通本地冲突停止；恢复不重复转换 | public resume |
| `T495-ROLLBACK` | 真实更新后 rollback、旧 runtime smoke；部分 core/task 写入 + Guru 普通冲突停止，native task writer 新增 meta 后 resume/rollback 仍保护新工作；完成后新任务/业务工作同样阻止回退 | public rollback/bytes/modes |
| `T495-DISTRIBUTION` | source/installed/platform、canonical/dogfood、runtime、同候选 update/reapply、drift、zero sidecar | 定向包/安装验证 |
| `T495-MIXED` | current + 无关真实 known-legacy active；creator、ref/id、branch/checkout/session 正常接续；direct old/目标占用/同身份碰撞/坏 current/JSON/id 拒绝 | runtime unit + actual installed owners |
| `T495-DEFERRED` | migrate 转换所选任务并原地保留 reviewed deferred old active；installed inventory/current owners 成功；omitted 旧 active/drift 仍阻塞，旧 bytes 不变 | Fork public migrate + Guru public/installed/reapply |

本表定义验收策略，不把未执行项计为通过；[本版 test-plan](./test-plan.md)拥有真实证据及剩余边界。[唯一双向 trace](./traceability.md)保留全部 MIG-495-01..09。
