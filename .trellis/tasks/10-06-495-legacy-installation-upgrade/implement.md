# #495 实施与验证计划草稿

## 规划修订时的事实快照（后续结果见验收贡献）

以下为构造执行前的规划快照；规划行为合同仍有效。后续实际结果由 [acceptance test](../../../docs/requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/test.md) 承载，不能把下文待执行状态当作当前验收结论。

当前固定 Guru 候选为 `6a563f5f06cb1284c0935b3a2be68524d93df988`，PR #496 OPEN / non-draft。固定 Fork 为 `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1` / CLI `0.7.0-castbox.2`，source lock 已同步。当前 RDT / Architecture authority 为 `current-main-0.6.17-guru.72`；后文 `.71` 的 initial planning 与 expected-current 信息仅是已执行阶段的历史说明，不作为本轮 gate 输入。

同一远端 `6a563f5f` 的 source_locked 七场景首轮 5/7、exit 1；两份原失败样本后续恢复及原 canonical 剩余断言通过，原失败日志保留。同 provider update/preview/force/reapply 与 actual installed 验证通过，3853 managed hash rows 无 mismatch、sidecars 为零。两次 initial 调用在目标写入前仅返回 internal_error，原因未知，不将其统称网络故障。该证据仍不证明完整 MIG-495-06、Issue Completion 或 Release。

MIG-495-06 构造在途 sample 尚未执行。[代表样本范围说明](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6028281048)已发布并复读为当前验收 authority；本轮规划按该说明更新，fresh gates 尚待执行。后续 RDT/Architecture 变更应新建 reviewed successor 并按 expected-current promotion，不覆写 immutable `.72` 的已发布历史合同。完整多平台 Release 矩阵与真实业务安装仍不在本任务验证范围。


状态：同范围规划；修订时的 Planning 待执行描述为历史快照，当前结果须由 fresh gate 判断。
行为与机制分别见 [prd.md](./prd.md)、[design.md](./design.md)。

## 原候选实施顺序与依赖（已执行阶段的历史计划）

1. 正式 task 创建后完成 planning wording、Architecture impact 与 Planning Approval；保留当前 base/Issue authority。展示三份正式规划后停在 plan review pause；当前对话明确接受该规划后才 activation/implementation。
2. 在用户指定 Fork checkout 重新读取 CLI/update/task schema/templates/test/build 合同，形成正式 Fork 迁移实现。Fork 的 branch/worktree/commit/push/CI 操作分别展示精确目标；不把本次 Guru task creation confirmation 解释成 Fork Git 操作授权。必要 Fork candidate 未固定前不声称集成完成。
3. 在 Guru canonical `trellis/skills/guru-team/packages/` 实现完整 migration semantic package 与独立 runtime modules/fixtures，更新 registry/interface/commands/manifest。只迁移 supported old profile，普通 current readers 保持不变。能复用的 core update、current preset、C4/C5/session/planning owner 直接复用。
4. 实现旧 provenance inventory/projection、task转换计划与 private backup/recovery/rollback。根据精确来源差异建立字段投影，旧 manifest 不通过伪造 current manifest 绕过 validator。
   直接复用 branch establishment → ensure → session owners：已提交旧 task 的 id/status 与 generation=0 匹配 current binding，转换后 working-tree task 满足 current schema；保留未提交业务工作。验证 dirty 已绑定接续与 clean acquisition 分离，不增加仅为迁移而存在的第二 binding writer。
5. 更新 Fork source lock 为正式已验证候选；锁的 commit/tree/parents/CLI/package manager/CI 依据真实 facts，不制造 SHA 或成功 CI。
6. 更新 marketplace workflow 路由/README、preset README、migration 使用说明、preset installer/upstream ownership 与 workflow skill-package/data-contract specs；执行 Docs SSOT Plan 的 isolated RDT 与 Architecture contributions。若实质扩大 owner/API/支持来源则 re-enter clarification/Architecture/planning，不得自行扩张。
7. canonical preset apply 同步 dogfood，解决 sidecars，执行 source/installed/inventory/platform/reapply/drift 的定向验证。固定 Fork 的 official template collectors/hash 同步实际漂移的 generated scripts、template-hashes 和 version，并执行 Official Source-Repository Dogfood Projection；不单独修改生成逻辑或 editable 平台配置。
8. 在隔离样本完成本地候选 public 入口、task owner re-entry、部分写入恢复及 post-write rollback，明确其 local candidate 边界；执行 MIG-495-06 可执行只读诊断并明确已有 PR/merge 的真实 live facts 与固定旧正式 writer 生成的隔离构造在途样本边界。
9. 对首个验收用候选 Delivery slice 重新完成 wording、Planning、Architecture、Phase 2、Task Commit 与独立完整 committed Branch Review；随后按 expected-current 执行该候选代码/合同范围的 RDT 与 Architecture serialized promotion，对 promotion-created diff 再执行 fresh Phase 2、Task Commit 和独立完整 Branch Review。当前 knowledge 只描述已经实现的候选与本地验证，明确保留 formal remote/MIG-495-06 未验证边界，不关闭迁移目标或 `ARCH-GAP-012`。经分别展示精确 Git 副作用后，发布 Refs-only Guru 候选 PR；不声明 #495 完成。
10. 固定远端可读 Guru commit 后，对该候选执行真实 source_locked public 升级及同源 workflow marketplace/provider 隔离验收。失败留在同一任务修复并重跑受影响 gates；正式验收与全部 MIG-495-01..09 真实证据齐备后，才进入 merge 和 Completion。

当前 Git 边界：Guru 使用同一 `codex/495-legacy-installation-upgrade` task checkout，TaskId/generation 不变。Fork PR #27 已合并，保留现有本地 checkout；该合并不授权 Guru commit/push/PR/merge、main 同步或 cleanup。下游源仓及其既有 worktree只读，预演只写隔离 temporary 样本。候选 Delivery 的每个 Git 副作用仍按精确当前 refs、文件及命令展示后分别执行。

## 拟修改范围

| 层 | 目标位置/职责 |
| --- | --- |
| Fork | CLI migration 注册/实现，core 旧 task 显式转换，update helper 的受管迁移复用，生成 Python/task schema 一致性与正式测试 |
| Guru canonical package | 新 migration package，Interface/input/output/consumer contracts/command wrappers/private modules/tests；current registry 与安装清单 |
| preset/source | `trellis/presets/guru-team/source/trellis-source.json`；独立 migration 入口与 source/bootstrap 支持，普通 apply 不增加 legacy fallback |
| workflow/docs/spec | `trellis/workflows/guru-team/`；preset README/迁移文档；`.trellis/spec/preset/`、`.trellis/spec/workflow/` 的 migration/current-only 边界 |
| dogfood | 由 canonical installer 生成的 `.trellis/guru-team`、`.agents/skills`、选定平台入口与 workflow 同步，不能单独 patch |
| task/RDT/Architecture | 三份 planning 与 isolated contribution；shared current promotion 按正式 owner 执行 |

非生成代码单文件不得超过 3000 行；不得把迁移代码塞进已过大的 installer。公共示例去敏，不包含实际业务 task、source 私有路径或本机绝对路径。

## 隔离预演设计

只读采集 `guru_ai_roleplay_dev` 及合适 worktree 的版本、tracked 树、task 格式、受管自定义与 Git lineage；构造独立 temporary repository/checkout 样本。不得在源仓运行 migration/update/apply，不 checkout/reset/clean 原 worktree。

主样本必须是 core `0.6.16` / Guru `0.6.16-guru.41`，保留来源中缺 generation/source/binding、subtasks、旧 branch/base/path 的结构。脱敏业务 private 内容，避免复制 .env/secret/raw traces；历史字节保留用非敏感代表样本或受控本地比较，证据不打印敏感正文。其它 core 0.6.5/0.6.7/0.6.15 样本只作为未支持来源诊断，不把它们偷换成主验收来源。

planning 与 unpublished in_progress 分别建立合法任务分支/registered checkout；后者含一个已有 commit、一个合法未提交业务改动和无关 dirty/untracked，以验证保留。该业务改动来自真实普通开发状态，不手工伪造 gate/hash/state。任务 source 在当前 AI review 中明确，旧 gate 仅作为历史不参与 current approval。

## 最小可靠验证集

| 场景 ID | 验证目标与执行证据 | 对应行为 |
| --- | --- | --- |
| S-MIG-495-PREVIEW | public source-loaded preview、支持来源/目标校验；repo 不写；显示 managed/local/task/session/Git 精确差异 | 01 |
| S-MIG-495-INSTALL | public migrate + workflow preview/apply + Guru reapply 真实成功；安装 manifest/版本/Fork source 一致，current-only runtime 可启动 | 02、08 |
| S-MIG-495-TASK | 完整旧及精简旧 schema 转换；非 UUID id、source/generation、subtasks/children/meta；合法 missing fields 补全，不丢未知业务数据 | 03、04 |
| S-MIG-495-PLAN | 已迁移 planning 通过当前 identity/branch/checkout/session owners 进入当前规划；真实脱敏项目 Architecture baseline、actual 两类 qualifications 与语义 gates；保留原规划 bytes | 04、05 |
| S-MIG-495-DEV | 未发布 in_progress 保留已提交/未提交业务工作；fresh 当前 plan review 后实际进入 current dev/check；旧 gate 不成为通过证据 | 04、05 |
| S-MIG-495-DELIVERY | 已有 PR/merge 读取真实 live facts；固定旧 .41 canonical harness 的正式 writer 写首次非 terminal push_content 后只读快照，原 Happy Path 正常完成；在快照真实 source_locked 迁移并 deferred/preserve 旧 task/事务/gate，逐案 pinned-old/manual，bytes/modes/local refs 不变；不重复副作用，不声称真实原始业务事务 | 06 |
| S-MIG-495-PRESERVE | business/spec/规划、.developer/journal/traces/archive bytes/modes 前后比对；有效 config/customization 设置保持并允许官方必要 additive 配置；无关 Git status 不变 | 02、03 |
| S-MIG-495-PARTIAL | core/task 已写、Guru 阶段因普通未解决受管本地修改停止；准确报告部分完成；处理后 public resume 成功且不重复转换 | 07 |
| S-MIG-495-ROLLBACK | 完成真实 managed update/task conversion 后、无新版业务工作，public rollback 恢复旧 runtime smoke、旧任务及定制；无历史重写 | 07 |
| S-MIG-495-NEW-WORK | 部分 core/task 写入且 Guru 普通冲突暂停期间 native task writer 产生新 meta/业务工作，resume 后 rollback 仍明确停止覆盖；完成后新任务/新业务工作同样保留 | 07 |
| S-MIG-495-REAPPLY | 同候选重复 update/reapply；source/installed package、platform projections、ownership inventory、managed runtime、drift 和 recursive zero sidecars | 08 |
| S-MIG-495-MIXED | 合法 current + 无关真实 known-legacy active；正式 creator、ref/id、branch/checkout/session 成功，旧原字节不变；direct old、目标占用/同身份冲突、坏 current/JSON/id 仍拒绝 | 09 |
| S-MIG-495-DEFERRED | 真正执行 migrate 仅转换所选任务、原地保留 reviewed deferred old active；installed inventory 与 current owners/新任务创建成功；omitted/未诊断旧 active 与普通 drift 阻塞；resume 不重复转换 | 09 |

新任务创建在 migrated fixture 通过 current `guru-create-task` 正式入口，核对 id/generation/source/binding/session；测试任务不是旧任务替代品。当前 task create 在 clean planning fixture，dirty in_progress binding 使用实际迁移/owner接续合同，不为了测试把未提交工作丢弃。

Fork 运行 CLI migration/core task conversion unit/integration/generated-template/build/typecheck；Guru 执行 migration package tests、registry/schema/consumer graph/source validation、installed验证与 preset installer/upgrade contract 测试。具体命令从最新 package 与 quality spec 读取，不凭旧命令推断通过。已有覆盖相同 public 入口与结果的正常 happy path 测试先复用，不增加攻击输入/压力竞态/超范围 fault injection。

source/installed + 全部声明平台投影可做静态字节/模式检查；真实完整累计 clean/existing/update/reapply/workflow-switch/release-candidate 多平台矩阵属于独立 owner。主迁移使用一个代表性 Codex 样本，若 live accepted scope 需要其它最小场景再按实际依赖增加，不能把本任务结果泛称 Release Gate。

## Docs SSOT Plan 与 gate

- RDT：isolated `docs/requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/`，manifest/requirements/design/test/traceability；逐行为→职责→场景映射。保留 predecessor #481 无人员模型，替换其迁移拒绝适用边界；history/tag 不改。
- Architecture：task-owned contribution，`legacy_boundary_convergence`，current/target owners、compatibility出口与删除条件、before/after、required concerns、fresh project-check protocol；ADR 候选仅承接迁移支持决策。
- 操作文档：固定版本/source升级 public 入口、参数、精确支持清单、逐任务处置、备份/部分恢复/实际回退、升级后新工作限制；不得发布虚构已可执行命令。
- Promotion：只有独立 committed full-diff Branch Review 后按 expected-current identity serialized promotion；promotion diff 再跑 Phase 2/commit/Branch Review。普通并行 task 不编辑 shared current。

## 当前状态与未验证边界

Delivery policy：同一 task 最终覆盖 MIG-495-01..09。首个 slice 是“用于正式验收的迁移候选代码与合同”，前置为正式 Fork merged OID/CI/source lock、本地 source/installed/reapply/drift、隔离迁移/lifecycle/恢复/rollback、可执行旧交付状态诊断及 fresh Planning/Architecture/Phase 2/commit/独立 full Branch Review；Publication 前完成该候选范围的 expected-current RDT/Architecture promotion，并对其新增 diff 再做 fresh Phase 2/commit/独立 full Branch Review。候选 knowledge 明确保留未验证项，不关闭迁移目标或 `ARCH-GAP-012`。候选 Refs-only PR 发布后，使用其固定远端 Guru HEAD 完成正式 source_locked/public/provider 验收；缺失的 MIG-495-06 live PR/merge 与明确标注的旧 writer 隔离构造在途证据继续显式保留。只有完整 MIG-495-01..09、RDT/Architecture promotion 与受影响 fresh gates 完成后才允许合并/Completion。完整累计多平台 Release matrix、软件发布和真实业务安装为 scope 外边界；候选发布不证明最终验收，也不以 local_candidate 冒充 source_locked。

初始 Intake 证据：指定业务 dev checkout 的固定 before Fork `update --dry-run` 拒绝 installed Trellis 0.6.16，只证明原入口拒绝。当前正式 task `495-legacy-installation-upgrade` / generation 0 为 in_progress，本机候选实现和隔离预演已进行；本轮加入 mixed/deferred inventory，并细化 partial-new-work、有效配置与真实 Planning 证明，须 fresh gates 后继续实现。真实业务仓保持只读，未执行升级。

Fork successor 已合并至 `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1`，tree 与已验证候选相同；PR CI 已通过，合并后 push CI `37473087582` 已 live 确认 success，source lock 已同步。本地 mixed/deferred、生命周期、partial-new-work 与真实 rollback 已有定向证据，须按本轮修订重新审查与 fresh gates，不能泛称最终验收。固定 Guru 6a 的正式 remote marketplace/source_locked/provider 已按首轮失败与原样本恢复事实取得证据；真实 live PR/merge 与 MIG-495-06 固定支持来源的隔离构造证据已按 acceptance test 取得；完整多平台 release matrix、tag/Release 和真实业务安装未执行。

core 预览需直接读取旧 `.template-hashes.json`，对照 current template/actions，显式列出旧 receipt 拥有而目标退役的路径并由 AI 作 remove/preserve 决策。只看 current actions 会漏掉旧引用，不能把未触碰当成已升级。old Guru manifest 未展开 hash 的 managed assets 必须从该 manifest 的 exact source.commit 获取旧字节；source checkout 需含该正式旧 OID，缺失时先按正式 remote 获取该 OID，再做 zero-write preview，不依赖常驻本机历史或增加自动网络 fallback。
