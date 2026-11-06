# v0.7.0-guru.8 准备交付实施与验证计划

## 1. 输入与引用

读取本批 prd.md、design.md，整体根 prd.md 的 R1–R7/AC1–AC5，#746 准备章节及私有 release 合同。规范性来源处置只在 design 第3节。实际加载 .trellis/spec/workflow/clear-technical-writing.md、quality-guidelines.md 验证价值/范围、.trellis/spec/preset/installer.md 的工具维护/Codex迁移条款、当前 R724/D724/T724 完整定义。

没有前序 Delivery。开发 B 为 main@338e8fdc4eee80ffa9c44c00d5030b5f240ad4cd；PR target main。Fork commit/CLI 与前驱配对按 design 第2节读取。

## 2. 有依赖顺序的步骤与文件责任

S1：Trellis implement worker 修改 canonical trellis/guru-team-extension.json、guru-upgrade-installation/runtime/owner.py、其 public schema、package/aggregate stop consumer schema、必须随 current target 变化的现有 fixture。保留历史 .7 示例含义；不得直接改 dogfood。同步正式source lock至ca0e8b931d19ccb87802d6866abd2113a6f707c0及真实parents/tree/CI42016570304，CLI/Core保持.6。

S2：同一 worker 更新 README.md、trellis/workflows/guru-team/README.md、trellis/presets/guru-team/README.md、.trellis/spec/docs/public-docs.md 的现行发布段；使用已发布 .7 provider，.8 明确尚未发布。按实际完整差额描述能力，保留历史证据边界。同步私有 release Skill canonical 与所有实际有效发现副本，current Codex 公共根为 shared .agents；不新增 retired 公共副本。

S3：主会话原 TaskCommit owner 在最低自检和敏感审查后取得可供真实安装的干净已提交来源。原 tools owner 使用 source_locked、完整干净 source、匹配 Fork build，对当前 Task checkout 执行 preview→prepare一次→invoke。检查真实目标/native entry 和 preservation，安装差额进入后续候选。

S4：原 RDT owner 评估当前知识差额，原 Architecture Phase2 和完整 Check、原 TaskCommit、第一次独立完整 Branch Review。只有零开放 finding 后才串行进入原 Architecture/RDT final integration；no-change 不制造文件。出现实际晋升差额则重绑 candidate，并重新最终 Check、原 TaskCommit、第二次独立完整 Branch Review。

S5：主会话沿原 publication/Delivery/Completion/Closure/Finish/Cleanup 完成准备交付。只 Refs #746；Closure no_mutation。Finish bookkeeping 正常合并后，发布协调在 fresh main 继续 Stage 2；不以本批完成替代最终发布。

## 3. 验证入口、输入与预期观察

V1：./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json；预期 source graph/schema/current target 一致，关联 AC1–2。使用 source managed resolver 执行受影响 upgrade-installation 现有 tests，观察正常输出与 consumer，而非新增固定版本字符串断言。

V2：source validator 分别指定 --platform-root .agents/skills、.claude/skills、.cursor/skills；实际私有 release SKILL.md/contract 全副本字节比对；检查无 managed .codex/skills/guru-*，关联 AC2。该确定性结果不等于所有宿主 native 运行验证。

V3：原 tools preview/prepare/invoke 和目标自己 resolver、installed validation、实际 native entry；核 extension .8、CLI .6、source lock、provenance 与完整 canonical bytes/modes，关联 AC3。重跑合法父仓gitlink的candidate_content_ref与GitCandidateContent同身份验证，并执行匹配上游maintenance-formal-reactivation.integration.test.ts的实际已完成归档后继场景，分别覆盖schema1与compact。用户数据/会话/其它 worktree pointer 保留；不手造安装 manifest。

V4：./trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json；./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .；git diff --check；递归查 .new/.bak 与 Python residue。预期无未处理冲突、漂移或敏感内容，关联 AC2–3。

V5：原 Check、晋升前后两次完整独立 Review、Delivery/Completion/Closure/Finish/Cleanup 的实际正式结果及 PR/Git live facts，关联 AC4–5。无 findings 不从命令 pass 推断；中文 PR 含 Refs #746 且无关闭关键词。

沿 design 第8节采用现有足够覆盖，不新增低价值测试或重复回退。Stage 2 的 exact-candidate 安装/升级/secret scanner/tag smoke 不在本批预填 pass；完整多平台累计矩阵和业务生产不覆盖。

## 4. 停止条件与适用回退点

source/lock/build 缺失停止真实安装，由原 tools owner 恢复匹配依赖。dirty 或 source drift 不强行安装。原 tools partial 只用原 recovery_ref/frozen plan；未知编辑保留，按原冲突处置，不重新 prepare 掩盖操作。

范围或规范性来源变化回 Clarify/Author，机制变化回独立 Architecture，当前 semantic finding 回最早受影响 owner。验证失败保留首失败和真实边界，不声称通过。证据充分后停止额外验证；设施反复失败则选择可观察同一行为的受支持方法或报告缺口。

不 reset、revert 或提交无关并行内容。没有业务数据/生产发布动作，故本批不造业务回滚协议；Git 与 tools bounded rollback 保持原独立 owner。

## 5. Delivery Policy（唯一）

policy=full。本 D1 覆盖全部准备 R1–R7/AC1–AC5，以可审查版本、文档、投影和真实 dogfood 为独立交付单位。准备 Task 仍需全部准备范围 Completion、Closure no_mutation、终态归档与资源收尾；Delivery 合并不代替整体完成。

post-merge fresh candidate、tag、smoke、Release、主仓最终安装和 #746 关闭不属于本 Task，由发布协调保留。准备 PR 不依赖这些未来动作已成功，因此没有循环先决条件。没有本批范围内延期切片或新增临时限制。

## 6. Docs SSOT Plan（唯一）

strategy=ssot_first。真实文档差额是现行版本、前驱/候选/Fork 配对及ca0e8正式来源事实和私有 release consumer 的 current-root 对齐。project public-docs 先与三个 README 同步，不修改历史证据或全局 knowledge identity。

原 writer 为 guru-maintain-requirements-design-test-ssot；直接 consumer 是当前 Check/Review 与后续 release coordinator。它读取 docs/{requirements,design,test}/README.md、current/codex-skill-distribution.md、completion-closure.md 的R712/D712/T712及父仓Git内容Architecture authority，判断是否有真实定义差额。既有 R724/D724/T724 行为未变化时返回 no-change，不创建空 contribution 或改共享导航。若实际定义有变化则转为原 owner 隔离 proposal/candidate Check/final_integration，刷新受影响规划和 gate，不擅自直接修改 shared current。

原 Architecture owner 对 no-impact 承接无共享写入，保留#739限定历史采用观察；真实必要差额才由原 owner 在第一轮 Review 后串行晋升。最终 Phase 2、TaskCommit 和第二次完整独立 Review 覆盖所有真实写入，之后才进入 publication。
