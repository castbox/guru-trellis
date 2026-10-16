# #575 发布准备设计

## D1. 设计依据与架构承接

整体需求由 `prd.md` 的 R575-01..07 单写。本设计承接 Architecture `current-main-0.6.17-guru.93/active`、constitution `guru-trellis-design-constitution-v1`、change-contract v1 与 RDT `current-main-0.6.17-guru.99/active`。使用各层 `docs/**/README.md` 的当前身份；落后的 spec usage projection 不选择 authority。

本候选独立 Architecture 判断为 `architecture_impact / legacy_boundary_convergence`，沿 ADR-024、ADR-027、ADR-028、ARCH-INT-014/015，不新增 ADR。首切片 task-owned 贡献为 `architecture/source-adoption.md`。原语义 owner、公共模型 writer、受管资产与私有控制 owner 保持；旧完整安装只持续到受支持的成套转换完成。`implement.md` 独占 Delivery Policy 和 Docs SSOT Plan。

## D2. 唯一 source-design disposition matrix

| 规范性来源与原承诺 | 处置 | 唯一落点与理由 | 影响和上游处理 |
| --- | --- | --- | --- |
| #575「正式依赖前置」：固定匹配 Fork source/build/CI，不用版本字符串或本地候选替代 | retain | D3、V1；采用 `prd.md` 的 #43 修复合并点 | 新来源仍为 CLI/Core `.3`；#40 原来源保留历史归属，#43 修复不在 Guru 重做 |
| #575「Stage 1」：完整版本、文档、投影、Docs 与定向验证 | retain | D3..D7；首切片不宣称整体完成 | 同 Task 保留剩余工作；不把迁移或最终投影移出整个准备范围 |
| 私有 release contract「Stage 1」：Planning→Check→Commit→全量 Review→串行 promotion→fresh Check/Commit/全量 Review→Delivery | retain | D4、V2；每次有 shared promotion 的切片均走完整链 | 不用旧 review 覆盖 promotion 新差额；无 promotion 时由原 owner 给出真实 no-change 路由 |
| 私有 release contract「Stage 2」：准备与 Finish 合并后 fresh main exact candidate | retain | D7；整任务终态不执行 tag/Release | Stage 2 重新核验前驱至最终候选；首切片不是发布候选 |
| 原 Author/Approval/Delivery policy：独立切片、显式 remaining 与整任务完成条件 | retain | implement.md P1；D4 首来源切片独立交付 | 策略为 staged，不缩减整体需求；首 PR 仅 Refs #575 |
| task-delivery-migration.md「尚未切换的旧安装继续运行自己的完整发行包」 | retain | D3、D5；当前旧 installed 图承接首切片 | 不提前复制新 Skill、移除旧 activation 或伪造 D1 |
| MIGRATION-566 与 tools/selected-task contracts：完整来源、独立操作、成套安装、原 owners、真实 native/下一 consumer | retain | D5；先 tools，再 selected Task，分别 review 与执行 | 公共 Task/session/binding 不由 Guru 手写；私有 controls 由原 Publish/Merge/Finish/Planning/Check/Review owners 处理 |
| 原 formal_guru_source：正式 canonical 必须已提交且干净，manifest 匹配 TARGET_GURU | retain | D3 的 `.3` 首切片与 D6 的同步 `.4` 断言更新 | 不绕过检查、不使用 local_candidate；最终修订只推进既有版本断言，不改公共 profile 或支持族 |
| AGENTS 第 6/7 节：定向验证、canonical 与 dogfood、受支持 update/reapply、用户修改保留 | retain | D6、V3..V7 | 首切片的安装边界明确；整体准备完成前交付真实投影，无全平台矩阵扩张 |
| AGENTS 第 10 节与私有 release contract：最小证据、不持久化授权、不创建动态发布状态 | retain | D7 与 implement.md Docs 计划 | 唯一 Test 拥有分层结果；不创建 release-notes/PR body handoff/gate 台账 |

以上均为现行约束，不包含作为合同使用的外部引文。没有 change/reject 项；技术顺序不改变需求或关闭意图。

## D3. 两个交付切片与一个既有维护边界

```text
当前完整旧安装 + 整体 Stage1 需求
  -> S1：正式来源采用（manifest 保持 .3）
  -> 原完整门禁、独立审查与 Refs-only 合并
  -> Completion 保留剩余责任
  -> M：clean committed source 上 tools-only + 所选 Task 转换
  -> target-native / 下一实际 owner / 真实 Delivery identity
  -> S2：fresh Delivery Planning、.4 与全部剩余投影/验证
  -> 整体 Completion、reference-only Closure、Finish
```

S1 的独立效果是：受审查的正式锁、构建入口与当前公开来源说明能从同一已提交源码消费。它保留 canonical manifest `.3`，满足现有 maintenance consumer，不声称 `.4` 已准备完毕。稳定已发布 `.3` 的 tag/provider/历史 lock 不变；当前未发布源码的 source adoption 与下一目标 `.4` 分别说明，不把新锁写成旧 tag 的内容。

M 是原有两个 standalone maintenance owners 的具体使用，不是新 Delivery、流程 owner 或恢复模型。M 前必须有 S1 实际 clean committed、远端可寻址的完整 source；不能以计划中的 SHA 代替它。工具预览的客观 source-clean 前置不得通过手工 metadata 或临时伪造来源满足。

S2 的 actual Delivery identity 在 M 后由公共转换/原 Creation 返回。首切片的旧 Task gate 只保留历史归属，不能替代 S2 的 Planning、Check、Review 或 Publication。

## D4. S1 的写集、门禁与边界

产品写集限定为 canonical `trellis/presets/guru-team/source/trellis-source.json`，根、workflow、preset 三份 README，`.trellis/spec/docs/public-docs.md` 的当前来源/发布文字，以及被这些精确断言触发的既有测试。调整当前说明，不改写归档、旧 tag、旧 manifest 或历史验证。

S1 明示以下剩余工作：upstream native scripts、Guru packages/registry/workflow/discovery/runtime 的 tracked dogfood 投影；同 Task 真实迁移与 native 续接；`.4` manifest 和原 maintenance target assertion；S2 定向安装、恢复与最终投影。它们不进入 S1 的已通过声明，但保留为整个 Task 的必需交付。

使用当前实际 installed workflow 的 Author、Wording、Architecture、Approval、Activation、Check、TaskCommit、BranchReview、Delivery、Publish、Merge 与 Completion。S1 先执行范围内 Phase 2 和 Task Commit，再执行完整 `origin/main...HEAD` 独立 Review；所需 task-owned Architecture/RDT 贡献在该 Review 后由原 owners 串行晋升，再 fresh Phase 2、提交和完整独立 Review。Publication 对未执行的 M/S2 作明确陈述。

S1 合并后立即消费真实 Merge 结果进入 Completion。任务仍有 M/S2 工作，不进入 Closure/Finish。沿其实际 remaining/下一交付规划出口保存同一身份与责任；不手填 route、不清空已交付历史。

## D5. M 的正常切换与历史处置

1. 从 S1 实际 clean committed source 加载完整 canonical `guru-upgrade-tools`。目标是本 Task 的唯一 registered checkout，平台为当前 `claude/codex/cursor` 加共享层。原 tools preview/prepare 冻结客观工具、workflow、Guru 资产和 checkout-local Python pointer 写集；确认后才 apply。Common/peer pointer、Task、规划、归档、session 和私有控制不属于 tools 写集。
2. 新工具由目标自身 resolver、installed validator 与 native entry 验证；旧 Task 得到原维护诊断，不为工具通过而先转换数据。成功只表示工具可用。
3. 原 `guru-maintain-legacy-task` inspect 同一 TaskId/generation；在转换之前调用原 Publish/Merge 的 `legacy_history_verification`，核实 S1 真实 PR/commit/source/base 与未完成责任。公共 projection 保留整体 scope、来源、全部原五规划文件和原始 Task 快照；历史事实按原 owners 归属，旧 gate 不形成新 pass。
4. 同 owner prepare 公共 Task2 与精确 artifacts/session/binding 处置；原私有 owners 逐一 inspect 所选 controls。未识别 owner/path、事实不能唯一归属、source/build 不匹配或冲突均写前停止，不制造空 owner。展示真实写集后才执行转换。
5. 由目标自身 native 与下一实际 owner 观察并 finalize。若实际转换结果属于 delivered/pending acceptance，先进入真实 Completion 的 `evidence_pending` 接续，不直接创建新 Delivery；补足原 owner 所需证据后，再沿实际 scope/下一 Delivery Creation 进入 S2。若输出为其它合法 continuation，消费其唯一原 consumer，不由本计划从旧 status 预选成功。
6. 真实 Creation 返回的 UUID、planning_root 和公共状态用于 S2 新规划；不从目录名、cycle_ref、首 PR 或旧 artifact 猜 identity。整体 TaskId/generation/source 保持。

工具与任务操作分别保留原 recovery ref；同操作恢复不 reprepare。回退先由公共 owner 校验工具/数据兼容，再由原 Guru owner 恢复自己的 preimages。转换后的数据不兼容旧工具时阻止单侧工具回退，不扩大原备份或 reset Git。用户定制和无关文件保持；任何必要的新写集重新展示。

## D6. S2 的目标内容和证明层次

S2 在真实新 Delivery 上重新 Planning→Wording→final Architecture→Approval→Activation。将 `trellis/guru-team-extension.json` 与原 `guru-upgrade-installation/runtime/owner.py` 的既有 `TARGET_GURU` 同步推进 `.4`，并更新其确切版本 fixtures/断言。保留 CLI/Core `.3`、公共输入/出口、合法版本族、source HEAD/clean/build 以及原 Plan2/rollback 合同。

成套安装以原 tools/preset owner 执行。Upstream `.trellis/scripts`、agents、模板 receipt、`.version` 由公共 tools 安装；Guru runtime、packages、registry、consumer schema、平台 discovery、workflow 与 overlays 由原 Guru installer 承接。后续 overlay 变更通过 canonical apply，同步 dogfood 并检查 drift；不得手改生成副本作为唯一源头。

整个 Stage 1 的最终验证包含：正式 Fork source/build/API；source 与 installed 各层；Shared/Codex/Claude/Cursor 声明投影；官方 dogfood upstream projection；ownership、三平台 apply/reapply/drift、执行权限、sidecar 和 diff/secret 扫描；一个代表性 Codex clean 样本；`.3` predecessor 的正式 source_locked tools/所选 Task native/下一 consumer、恢复及不兼容单侧回退。既有 local_candidate 测试只能作为其原层次结果，不能被重命名为正式采用证明。

source_locked 正式调用要求其执行来源 clean committed；S2 的这部分验证安排在实际任务提交和完整 Review 后，以该真实候选执行，结果由唯一 Test 归属。结果造成产品或贡献内容变化时，重新进入受影响的原 Check/Commit/完整 Review，再进行 Publication。需要远端 immutable provider 或最终 `.4` tag 才能取得的证据由 release Stage 2 重新完成，不伪装成当前本地证明。

## D7. 证据、完成与发布边界

逐切片的唯一 Test、双向 trace 与 task Architecture 贡献定位由 implement.md 定义。S1 的晋升不改写 #566、#40、#43 或已发布 `.3` 的证据；S2 使用不同贡献定位承接新差额。Shared authority 只在原 owner 的 expected-current 门禁下写入，不在 Planning 晋升。

全部 R575/A575、M 的真实 continuation、S2 的投影和定向结果完成后，才能通过整任务 Completion。reference_only Closure 不更改 #575；原 Finish 完成归档与独立 bookkeeping 合并。资源清理由其原 owner 的精确计划单独控制。

Stage 2 丢弃早期 candidate/gate，从准备及 Finish 合并后的 fresh origin/main 冻结 exact candidate，重新执行私有 release contract。完整多平台/native-host 矩阵、真实业务升级或生产验证不是本 Task 的已验证层次。不保存用户授权、动态发布 checklist、release-status commit、task-local release notes 或 PR/Release body handoff。
