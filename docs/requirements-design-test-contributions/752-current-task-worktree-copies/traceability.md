# Current-schema Task copies：双向追踪与替代边界

适用基线为 Git `2ab135ed2d3908966785bb23ad42ada0790f0c81`。唯一完整拟生效正文位于 `proposed/` 下的最终 repository-relative 路径；镜像内相对链接按最终目标解释。当前三个共享单元在候选 Check 前不写入。

| Requirement / behavior | 完整需求正文 | Design / contract | Test / acceptance |
| --- | --- | --- | --- |
| R752-01 / BEH752-AUTHORITY | [Requirements](./proposed/docs/requirements/current/native-compatibility.md) | [D752-01](./proposed/docs/design/current/native-compatibility.md) | [T752-01/02](./proposed/docs/test/current/native-compatibility.md)；Task R1/AC1 |
| R752-02 / BEH752-PRESERVE | 同一完整 Requirements | D752-02/03/04 | T752-01/02/03；Task R2/AC2 |
| R752-03 / BEH752-REJECT | 同一完整 Requirements | D752-01/02/03 | T752-01/02；Task R3/AC3 |
| R752-04 / BEH752-RECOVERY | 同一完整 Requirements | D752-04 | T752-02/03；Task R4/AC4 |
| R752-05 / BEH752-PAIR；R630-05/R687-01/02 | 同一完整 Requirements | D752-05；D630-05/D687-01/02 | T752-03/04/05；Task R5/AC5 |

## 原来源与必要 consumers

- 来源：[Issue #752](https://github.com/castbox/guru-trellis/issues/752) 完整语义、所选 Delivery 的三份正式规划与根 accepted scope；不将上游 wire 机制提升为源需求。
- 原迁移合同：[delivery-migration.md](../../../trellis/skills/guru-team/packages/guru-upgrade-installation/references/delivery-migration.md)，保留完整 inventory、原 binding、公私 owner、frozen preimages、恢复与rollback；新增 selector2由 Fork公共 schema/executor拥有。
- 来源：[canonical lock](../../../trellis/presets/guru-team/source/trellis-source.json)、[PR #66](https://github.com/castbox/Trellis/pull/66) 与精确合并源码；同版本号不能代替完整 source/build与installed验证。
- Architecture：[公开入口](../../architecture/README.md)、[本批隔离贡献](../../architecture/contributions/752-current-task-worktree-copies.md)；原 ARCH-DOM-043 / ARCH-INT-046、ADR-024/017承接所有权和采用边界。
- 独立 Architecture/候选 Check读取完整proposed。candidate_checked后原 RDT/Architecture owners分别 final_integration，implementation重绑actual after；最终Check/独立Review覆盖实际写入。Completion另审整体Scope及真实验收。

## 替代与保持

这是 native-compatibility 单元的 addition/modification，无旧要求删除、身份拆并或全局版本递增。R630原三系统规则、R687 tools-only/stop约束及其历史采用保持；本节只接续 current-copy 的 successor采用，不追改旧贡献。未迁移的旧安装升级知识仍按 RDT根入口保留其原完整来源，本贡献不声称整体知识迁完。实际执行与首次失败只由 [Test](./test.md) 单写；共享current晋升和Task/Delivery结果来自原owners，不生成第二完成账本。
