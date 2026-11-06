# v0.7.0-guru.8 准备交付设计

## 1. 设计目标、需求承接与内容基线

本批承接全部 R1–R7/AC1–AC5。development baseline B 是显式 main 的 338e8fdc4eee80ffa9c44c00d5030b5f240ad4cd；Planning H0 仅为该起点观察，最终 H 由原 candidate constructor 读取。PR 目标为 main；内容范围为固定 B 到实际 H 加 dirty 增量，不以发布前驱替代 Delivery B。

Architecture authority 为 docs/architecture/README.md 的 guru-trellis-architecture，constitution 为 docs/architecture/00-foundation/design-constitution.md 的 guru-trellis-design-constitution-v1，change-contract 为 docs/architecture/06-governance/change-contract.md。prewrite 独立 assessment 将本候选定为 no_architecture_impact：只更新版本、发布事实和已接受 Codex 根的使用说明，不改变公共接口或 owner，因此不创建 Architecture contribution/ADR。该判断不替代 final_plan、Phase 2、独立 Branch Review。

## 2. 当前系统、边界与目标差额

没有前序 Delivery。trellis/guru-team-extension.json 是 extension revision canonical；guru-upgrade-installation/runtime/owner.py 的 TARGET_GURU 与两个 package/aggregate consumer schema 拥有升级目标。它们从 .7 更新到 .8；检查所触及测试的真实用途，只更新需要代表当前目标的 fixture，不把所有历史 .7 改成 .8。

README.md、workflow/preset README 和 .trellis/spec/docs/public-docs.md 拥有当前安装与发布说明。真实 .7 peeled 为 7718d129bcb2055d77c7f43d0e4edca9aee313ea，自身 lock 是 Fork 79a97ed60fe19e8f287eaddfa74722b5250ced35 / CLI .5。当前 .8 准备来源 lock 为 17015f987166f4106034f115d23212446f16d536 / CLI .6；不更改 lock。

私有 release Skill 的 .agents canonical 与真实 Claude/Cursor/Codex 发现副本保持一致。Codex 公共 root 只使用 .agents/skills；私有 Skill 是否存在额外发现副本按实际仓库清单核对，不能据旧四根 loop 创建退休公共 .codex/skills/guru-*。

## 3. 来源设计处置（唯一）

| 来源条款 | 原承诺 | 处置 | 落点、理由与影响 |
| --- | --- | --- | --- |
| #746 版本轴 | .8 extension/tag，Fork .6 固定 | retain | 第2、4节；版本目标变化，依赖 lock 不变。 |
| 私有发布合同 Stage 1.1–2 | 稳定规划与真实 source_locked dogfood | retain | 第4、6节；完整干净已提交来源走原 tools owner。 |
| Stage 1.3–7 | 原 TaskCommit、晋升前后两次完整独立 Review | retain | 第6节；不以一次 Review 覆盖新增字节。 |
| Stage 1.8–11 | Refs-only、Completion 准备范围、Closure no_mutation、独立 Finish/Cleanup | retain | 第6、7节；#746 保留后续发布责任。 |
| release Gate 四根 parity loop | 所有实际有效平台合同一致 | change | 以 current ownership/MIGRATION-724 的公共三根 .agents/.claude/.cursor 核对，Codex 由 shared root 承接；私有 Skill 另按实际副本完整比对。此为现行 #724 consumer 适配，原独立 Gate 不减弱。 |
| Stage 2 candidate 与本地收尾 | fresh main、tag/smoke/Release、主仓安装、Issue关闭 | retain | 本批之外，准备输出交发布协调；不在本 Task 伪造未来通过。 |
| Forbidden Persistence | 不创建 notes/body handoff/status commit/ledger | retain | 第5、7节；实现计划稳定，不记录动态状态。 |

## 4. 模块、职责与设计取舍

版本 worker 仅修改 canonical extension、现行 maintenance target/schema 和必要 fixture。文档 worker/主会话修改三个 README 和 project public-docs 当前发布段；保留历史观察及未验证矩阵。私有 release Skill 修正 Gate locator，不修改公共 workflow owner 图。

dogfood 不手工 patch。主会话作为原 guru-upgrade-tools owner，先通过原 TaskCommit 取得完整干净的准备 source，再从该 source 执行 preview→单次 prepare→invoke/同操作 recovery。目标为本 Task checkout。真实安装产生的 managed scripts/schemas/projections/manifest 进入本次最终 diff。

选择原 source_locked 路径，是因为 local_candidate 不能证明本次 release 的正式来源，普通 full apply 又保留历史 Task inventory guard。不扩大为旧 Task migration，不改模板 mode 或全局 npm 包。

## 5. 接口与数据

无新公共 API、schema field、Skill id 或出口。现行 upgrade target const 的值跟随 canonical .8，调用方仍使用原 public-upgraded-output 与 consumer schema。私有 release 合同仍为无 public DTO 的编排。

原 Author/Architecture/Wording/Approval/Activation 和 Check/Commit/Review/Publish/Merge/Completion/Closure/Finish/Cleanup 接口原样使用。安装 input 仍为 profile=install、source_ref、dependency_mode=source_locked、精确 checkout；prepare 独占冻结 plan，invoke 不手改 manifest 或授权字段。

## 6. 状态、顺序、正常与失败流程

先规划完成并由当前 Approval/Activation 进入实施。实施更新 canonical/docs/private Skill，完成 source 定向检查与敏感内容审查。原 TaskCommit 的已审核 early source 路径提供干净已提交 source；原 tools owner 实际更新 dogfood，回原 Phase 2、TaskCommit 与第一轮完整独立 Branch Review。

第一轮零开放 P0–P3 后，原 Architecture/RDT owners 串行判断和执行实际需要的 final integration；无差额不制造空贡献。任何真实晋升字节重新构造 candidate、begin_check、最终 Phase 2、原 TaskCommit 和第二次完整独立 Review。即使 no-change 不写共享 authority，也保留 release 合同要求的两次独立审查。

随后 Architecture publication、Delivery Review、中文 Refs-only readiness、原 Publish/Merge。准备范围 Completion 完成才进入 Closure no_mutation；Finish 和 Cleanup 各沿原 owner。source/identity stale 返回原 producer；测试或安装失败不生成 pass，原 tools partial 操作只用同 frozen plan recovery。

## 7. 恢复、兼容、迁移与集成

公共 Codex 迁移已经由 #724 定义，本批只修正私有检查 consumer，不重新做迁移框架或恢复旧 root。原 installer 依 previous managed provenance 保留用户修改、按 current root 校验、无未处理 sidecar 后才报告成功。

真实 dogfood 使用匹配 Fork clean build，保留 Task/archive/workspace/session/user config/peer pointer。若需要干净 source，使用已提交 source 的 detached source acquisition，不在 target 中改 provenance。Finish 不补 release-status commit；Stage 2 只从准备和归档合并后 fresh main 取 candidate，不能重复本批 Review 当发布 Gate。

没有业务数据迁移、DB、容器或生产部署，因此不新增回滚协议。Git 工作与 tools rollback 分别沿原 owner，保留其它人的并行内容。

## 8. 验证设计

| 验证 | 要求/AC | 入口与观察边界 |
| --- | --- | --- |
| V1 | R1/AC1 | 原 source validator 与 upgrade-installation 定向测试；current revision、schema consumer 和正常 target 输出一致。不新增版本常量自证测试。 |
| V2 | R2–R3/AC1–2 | 三 README/当前 public-docs 逐段语义审查；source validator 对实际 .agents/.claude/.cursor root；私有 Skill 全部有效副本逐字节一致，不存在退休公共 Guru root。 |
| V3 | R4/AC3 | 原 guru-upgrade-tools preview/prepare/invoke；目标自己的 resolver、installed package validation 和 native entry，全部 managed bytes/modes、lock、CLI/来源匹配，保留数据无损。 |
| V4 | R3–R4/AC2–3 | check-upstream-ownership.sh --repo . --json 与 check-dogfood-overlay-drift.sh --repo .；检查 recursive .new/.bak、pycache 和 diff hygiene。 |
| V5 | R5–R7/AC4–5 | 原两次完整独立 Branch Review、串行知识 owners、中文 Refs-only 交付与原终态；不以测试数量、文件存在或单项合并替代。 |

采用受影响 package 的现有行为测试和真实安装输出，不新增镜像实现测试。先验证 canonical，再更新实际安装，再 final Check/Review；证据足够即停止重复。正式 fresh candidate focused clean/update/reapply、predecessor existing upgrade、真实 secret scan 和 tag smoke 属 Stage 2，本批不预填其结果。完整累计多平台矩阵、全部 host 和真实业务升级未覆盖。

## 9. Canonical 引用、本轮差额与实际未决项

docs/{requirements,design,test}/current/codex-skill-distribution.md 的 R724/D724/T724 定义 current shared discovery、旧根退出和用户保护；本批遵从既有规则，无新增行为定义。Architecture 保持原 identity，不制造 contribution/ADR。

.trellis/spec/docs/public-docs.md 当前版本事实需要更新；三个 README 是其派生说明。原 RDT owner 在 Phase 2 判断这些说明是否触及已生效知识单元；若只是版本事实维护，则 no-change 无空贡献；若有真实定义差额，先隔离完整 proposal，经 candidate Check 后原 final_integration 再写 current。没有必要未决产品问题。
