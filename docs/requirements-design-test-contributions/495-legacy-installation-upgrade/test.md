# #495 验证贡献

状态：正式 Fork 依赖已固定且本地候选定向验证已执行；正式同源远端与 live delivery 全部验收尚未闭环。本表为策略，结果见下方，不代表发布通过。

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

初始证据：#495 live 正文 `updated_at=2026-10-06T08:19:13Z`；实际 downstream 当前 Fork `update --dry-run` 拒绝 0.6.16，源仓 clean。该命令证明现有拒绝，未证明迁移。

## 当前本地候选证据

- Fork：migration integration 9、core projection 5、native task/session 50、其它 task scripts 36、完整 regression 449 通过；lint、lint:py、typecheck、build、release:check 通过。Python 检查只有未修改历史模块的 48 个 warnings，无 error。
- Guru：migration package 14、task lifecycle 154、upgrade contract 73、temporary lifecycle 6、workflow prose 18、manual Git 5 通过。runtime 原完整轮 63 项通过，唯一不完整 current fixture 修正后单项通过。preset installer 原完整轮 100 项通过，剩余 manifest 版本/数量断言随候选更新后单项通过；未把它写成整套最终重跑。
- opt-in `test_495_migration_lifecycle.py` 最终实际 public 6/6 通过：完整 planning、精简 dirty in_progress、延期旧 notes、无新工作实际回退、新 current meta、正式 creator 与旧 TaskId/casefold 占用。来源受管资产读取真实 core0.6.16/Guru41；业务与历史内容为脱敏代表样本，真实下游 HEAD/status 每场景前后不变。
- 两个业务接续实际调用 identity、branch、checkout、session、normal-scenario、solution-mechanism、Architecture、wording 与 Planning 入口。当前 AI 独立阅读样本业务规划与 Architecture authority后判断 no-impact；测试中的固化 authoring 仅为协议回归，不作为语义判断的来源。
- 普通 preset 冲突恢复后，未新增工作时 actual rollback 恢复所有 Git-visible bytes/modes、HEAD/status、旧任务与版本，消费 backup，旧 `task.py list` smoke 通过。partial native meta 与 deferred notes 两条正常新增工作路径实际阻止覆盖；失败 resume 刷新 baseline 后固定锚点仍检测 deferred 差异。
- canonical/source/installed、Claude/Codex/Cursor projections、reapply 和 dogfood drift 通过：35 packages / 159 package exits / 106 commands，business graph 33 invokes / 153 exits，recursive sidecars 为零。安装产生的四份旧 HEAD backups 与后续六份旧候选 backups 逐个审核后移至仓库外保留。

## 正式 Fork 固定后的本轮证据

- Fork PR #27 已合并；正式 source lock 为 `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1`，parent `9c36002a324c16a09a85b6aa5a380b74aabf801f`，tree `3741c14ccd36289584697c4c57c9daf2dd979f5f`，CLI/core `0.7.0-castbox.2`，pnpm `10.32.1`。合并后 push CI `37473087582` live 确认 success；candidate 与 merge tree 相同，candidate core 411 pass / 1 历史 SQLite skip、CLI 1879 pass，lint/typecheck/build 通过。正式干净 checkout 已完成 frozen offline install/build；`validate-source` 核对实际 HEAD、tree、parent、build marker 与版本通过。
- official collector/hash 同步实际漂移的三份 dogfood Python script、对应 template receipts 和 `.version`。Official Source-Repository Dogfood Projection 实际比较 183 文件通过，独立 dogfood projection 9 tests 通过；editable 平台配置由原 owner 保持。
- canonical preset apply/reapply、source/installed package graph、Claude/Codex/Cursor dogfood drift 均通过；两个新 sidecar 逐个审查后可恢复地保留在仓库外，当前 recursive sidecars 为零。upgrade contract 最终完整 73 项、installer 最终完整 101 项、ownership 9 项、migration package 14 项通过。shared runtime 完整 64 项中 62 项通过，2 项 hash-locked dependency 安装失败；不改代码/测试原样重试两项后均通过，不将该组合结果称为完整单轮通过。
- 使用正式合并 Fork 重新执行六场景 public lifecycle：6/6 pass，159 秒。证明规划与未发布开发任务接续、creator/mixed/deferred、普通部分恢复、无新工作精确回退以及新增 meta/notes 阻止覆盖。真实业务仓全部 10 个现存 checkout 与正式 Fork 的 HEAD/Git status 前后相等。样本业务内容脱敏，真实源仓只读；preset bootstrap 可使用共享 managed Python cache，不声称所有文件系统写入均在样本目录。
- 已迁移隔离 planning fixture 实际执行同一正式 Fork `update --dry-run`（无写入）、`update --skip-all`（成功补入官方 `.trellis/.gitignore` 与 receipt），再执行同一 canonical 本地 workflow 投影及 current preset apply/reapply。installed core `.2` / Guru `.2` 与 canonical 一致，3844 条 package/overlay hashes 校验零错误；重复应用没有 footprint drift/new copies/backups，sidecars 为零。原任务/deferred/历史/业务/config bytes/modes 与 AGENTS 用户段保持，10 个真实业务 checkout 及 Fork 状态保持。manifest 如实记录当前 Guru HEAD 与 dirty source，不伪造 clean provenance；这是 local_candidate 的实际 current-update 证明，不是 remote provider 验收。
- GitHub 连接恢复；本轮重新读取 #495 正文及两条范围/顺序说明，Issue 仍 open。MIG-495-06 可执行只读诊断确认 PR #195 open，exact head `a9e65e0419c1e35f73ca6faf3c7b09d2ce370d4c`，存在同 branch 的真实旧任务；该任务 `pr_url=null` 不代表未发布，不能重走新发布。live base 与旧 task base 不同，需逐案核对。PR #210、#58 均已 merged，作为实际终态只读诊断，不能冒充旧在途事务。PR #195 exact remote head 的完整 Guru manifest provenance 尚未闭合；支持来源中尚未取得真实旧 Finalizer/Finish 在途代表。

上述隔离升级仍为 `local_candidate`，不是正式 `source_locked`/remote provider 证明。首个 Delivery slice 只交付正式验收用候选代码与合同；按[顺序说明](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6018378988)，固定远端可读同一 Guru HEAD 后才执行正式 public/provider 验收。MIG-495-06 的来源与真实在途缺口继续保留，全部 MIG-495-01..09 齐备前不进入 merge/Completion。此前 blocked Phase 2 不复用；首 slice 的 fresh Architecture/Phase 2 仍待执行。

独立 committed full-diff review 与 RDT/Architecture serialized promotion 仍待执行，shared `.71` 未改。完整多平台矩阵、新 tag/Release、真实业务安装由各自独立边界承担，未执行。
