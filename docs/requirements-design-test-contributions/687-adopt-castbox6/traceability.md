# #687 双向追踪与替代边界

适用基线：Git `7718d129bcb2055d77c7f43d0e4edca9aee313ea`。唯一拟生效正文在 `proposed/` 下按最终 repository-relative 路径镜像；镜像正文的相对链接按最终目标路径解释。正式 current 的三个文件在 candidate Check 前保持不变。

| 要求 / 行为 | 完整需求正文 | 设计责任 / 合同 | 测试策略 / 验收 |
| --- | --- | --- | --- |
| R687-01 / BEH687-SOURCE；R630-05 | [Requirements](./proposed/docs/requirements/current/native-compatibility.md) | [D687-01 / D630-05](./proposed/docs/design/current/native-compatibility.md) | [T687-01/02](./proposed/docs/test/current/native-compatibility.md)；AC1/2 |
| R687-02 / BEH687-TOOLS；R630-03/05 | 同一完整 Requirements | D687-02 / D630-02/05；原 tools-only source_locked 合同 | T687-03/05；AC3/5 |
| R687-03 / BEH687-STOP；原 R657-03 | 同一完整 Requirements；[原 lifecycle](../../requirements/current/task-delivery-lifecycle.md) | D687-03；[原 D657-03](../../design/current/task-delivery-lifecycle.md) | T687-04；[原 T657-05](../../test/current/task-delivery-lifecycle.md)；AC4 |

## 必要原来源与消费者

- 前驱完整单元：基线同 tree 的 `docs/{requirements,design,test}/current/native-compatibility.md`，保留 R630/D630/T630 稳定身份和未改变条件。#630 的 .5 和当时观察继续由 [原唯一 Test](../630-native-compatibility/test.md) 拥有。
- 严格维护：[#566 Requirements](../566-single-checkout-upgrade/requirements.md) R566-02/06、[Design](../566-single-checkout-upgrade/design.md) D566-01/06，以及 [canonical tools-only contract](../../../trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md) 的 source_locked、执行/保留与同次恢复。未迁移的升级范围继续按 [RDT109-INSTALL-UPGRADE](../331-current-effective-knowledge/traceability.md) 读取实际原来源；本贡献不声称迁完该范围。
- 来源和安装责任：[canonical lock](../../../trellis/presets/guru-team/source/trellis-source.json)、[ownership spec](../../../.trellis/spec/preset/upstream-ownership.md)；Architecture 公开身份见 [entry](../../architecture/README.md)，本轮差额见 [Architecture contribution](../../architecture/contributions/687-adopt-castbox6.md)。
- 当前候选 Check 读完整 proposed 正文；原 RDT owner 在 candidate_checked 后执行 final_integration；最终 Check/独立 Review 审实际写入；Completion 消费实际验收与交付事实。本文只定位关系，不复制 gate 或完成账本。

## 替代与保持

这是既有 native-compatibility 单元的窄 modification/addition。当前维护来源选择从历史 .5 采用关系接续到本轮锁定 .6；#630 的原 scope、.5 构建观察和历史身份仍可定位。原严格校验、解释器、LF/用户编辑、ownership 和恢复条件不删除。没有 requirement 删除、身份拆分/合并或全局版本递增；其它单元和历史贡献不写入。实际执行及首失败由 [本轮 Test](./test.md) 单写，未发生的采用和 promotion 不预填完成。
