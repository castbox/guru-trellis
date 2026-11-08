# #752 D1 current-schema Task 副本迁移需求

## 1. 整体来源与术语

整体 authority 为 Task 根 prd.md，accepted_scope revision 为 sha256:3c1042cdabe62cb5ca9f398c2e4ac40eac80364ce0afb9f9fc689e66860d4e98。本 DeliveryKey 为 ce0248be-6b58-4239-8c1f-7444625adf73 / generation 0 / cffee5bc-4a87-465e-b056-534b530951d5；scope_ref 选择 R1–R5 和 AC1–AC5，planning_root 为本目录。

Direct Source 为 https://github.com/castbox/guru-trellis/issues/752 完整正文，角色为要求。原 migration owner 合同 trellis/skills/guru-team/packages/guru-upgrade-installation/references/delivery-migration.md 是约束；source lock 是起点事实。current-schema、authority 和 peer 采用根 PRD 第1节定义；wire schema 属于 Fork。

## 2. 整体与本批目标、非目标

本批是全量 D1，完成正常 inherited current Task 多 worktree topology 的完整迁移能力：唯一 authority、合法 peer 保留、普通 mismatch 阻塞、恢复/回滚与完整匹配 source pair 实际安装。本批覆盖整体全部要求，不能把上游组件测试当整体完成。

保留根 PRD 第3节全部非目标：不改写、合并、删除或重建用户 Task/binding/session/Delivery/archive，不忽略 root、伪装 legacy、patch installed CLI/node_modules/tag。不增加攻击或非常规并发加固，不发布 Guru tag/npm release。

## 3. 本批起点、前序结果、依赖与剩余责任

尚无前序 Delivery。Guru 固定 main 2ab135ed2d3908966785bb23ad42ada0790f0c81；当前 source lock 固定 Fork ca0e8b931d19ccb87802d6866abd2113a6f707c0 / CLI-Core 0.7.0-castbox.6。上游 migration2.ts defer 仍调用 predecessor validator，current peer 缺少合法语义。

本批需要 Fork successor schema/executor 和匹配 Core/CLI build，随后 Guru 投影、source lock 与安装 owner 成套采用。上游 PR/CI/source 固定、Guru 验证和代表性 installed 验证分别提供事实。预期没有后继切片；若实绩留下必要责任，由 Completion 据真实缺口处理，不提前删减范围。

## 4. 本批调用方、场景与流程

| 场景 | caller、前置及动作 | 处理和观察 |
| --- | --- | --- |
| D1-S1 | Upgrade owner 纳入全部 registered workspaces；同 current Task 来自正常 checkout；提交原 binding | 公共 preview 验证唯一 live authority；执行保留 peer 原 bytes/metadata/modes |
| D1-S2 | 正常内容、generation、source、binding、checkout stale/mismatch 或 authority 歧义 | preview 阻塞，原数据不变，回原 owner fresh prepare |
| D1-S3 | 原 owner 对同冻结 source/Plan2 执行或 resume | 不刷新计划或 rollback anchors，peer 不进入 lifecycle/selection/Delivery/private conversion |
| D1-S4 | 原 owner 审查 rollback 条件并回滚 | Task/session 原 bytes/modes 恢复，不 reset Git 或改远端 |
| D1-S5 | 匹配 pair 在真实多 worktree 代表性目标升级 | 实际 installed runtime 读取 authority、Task/session、peer 和 private-owner exclusion |

## 5. 完整行为、条件与约束

- D1-R1 承接 R1：完整 roots inventory；原 binding 与 live checkout 选出唯一 authority。缺失、歧义或 mismatch 阻塞。
- D1-R2 承接 R2：合法 peer 和业务元数据保留；不形成额外 current lifecycle、Delivery、session selection 或 private-owner migration。
- D1-R3 承接 R3：内容、generation、source、binding、checkout 不一致拒绝，禁止合并/丢弃。
- D1-R4 承接 R4：dry-run/migrate/resume/rollback 使用同完整 topology、冻结计划和原 anchors，并独立断言 Task/session。
- D1-R5 承接 R5：上游公共 schema/executor 拥有复制组合法性；Guru 只投影事实、编排原私有 owner 和安装。source lock、canonical/dogfood/installed 和声明平台保持匹配，处理原 .new/.bak/mode。
- AI 负责选择、充分性和 route；确定性脚本不承担判断。设计不得通过过滤 root 或 legacy fallback 改变可接受输入。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应 | 入口、输入及预期 |
| --- | --- | --- |
| D1-AC1 | R1/S1 | 公共 Plan2 preview，多 current copies 与原 binding；完整 roots，唯一 authority |
| D1-AC2 | R2/S1/S3/S5 | migrate/resume/installed query；peer bytes/metadata/modes 保留且不进入 lifecycle/selection/Delivery/private migration |
| D1-AC3 | R3/S2 | 普通 mismatch/歧义输入；preview 阻塞，Task/session 不变 |
| D1-AC4 | R4/S3/S4 | 同冻结计划 dry-run/执行/恢复/回滚；原 Task/session 保留或恢复，不刷新 anchors |
| D1-AC5 | R5/S5 | 完整匹配 source pair build、实际多 workspace 升级与 installed runtime；受影响 canonical/dogfood/platform、drift、sidecar 和 mode 验证 |

没有未解产品选择。具体 Plan2 wire 与实现由 Author/Architecture 决定，不要求来源先给代码。实际验证尚未执行；完整多平台 Release 矩阵及原业务项目升级不由本批证明。

## 7. Canonical 引用与本轮差额

已读 docs/requirements/current/native-compatibility.md R630-05 与 R687-01/02、docs/design/current/native-compatibility.md D630-05/D687-01/02、docs/test/current/native-compatibility.md T687-01/02/03/05：继承完整匹配 source/build、原安装 owner、用户数据/peer 保留和分层证据边界；本轮新增 current-schema copies 的完整迁移，不重写 .6 历史采用。

架构 authority 入口为 docs/architecture/README.md，职责为公共 Task/schema 与 Guru 安装/私有 owner 的隔离。原独立 Architecture owner 按 authority-first 读取完整适用单元并评估候选。原 migration 合同和 trellis/presets/guru-team/source/trellis-source.json 提供当前 consumer 与来源；本轮差额为 successor peer 语义及实际采用。当前共享 CURRENT 不因本规划写入而改变；RDT/Architecture 拟写经独立候选 Check 后由原 final integration owner 晋升。
