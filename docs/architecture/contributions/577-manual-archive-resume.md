# #577 人工旧归档恢复：Architecture contribution

状态：`reviewed_promoted`；change_path：`legacy_boundary_convergence`。Task：`577-manual-archive-resume / generation 0`；D1：`bfcecca6-7d49-4f5f-a816-12859b893f5c`。本轮原 Architecture owner 在独立 Phase2 评估完整候选和拟写内容后，按 expected `current-main-0.6.17-guru.97/active` 晋升 `.98`。比较起点为 `ef0fcdf0c3746e6d84f97732b9ab776a4bf7703e:docs/architecture/`；constitution、change-contract 与 concern-set 均为原 v1。非 Planning 合同为 `guru-maintain-architecture-baseline:4.0` / Delivery2.0。

唯一行为要求为 [#577](https://github.com/castbox/guru-trellis/issues/577)，公共能力由 [Trellis PR #52](https://github.com/castbox/Trellis/pull/52) 拥有。ADR-024/027 继续拥有公共模型、独立维护与兼容退出；ADR-030 拥有本轮晋升时机，不新增 ADR。ARCH-GAP-006/008/012 生命周期保持，不以本增量关闭正式来源或业务采用缺口。

## 责任与局部收敛

Before：原维护只支持活动转换/历史保留，transport 对旧三项能力严格相等；current reservation 把同 ID 的保留 archive 与恢复 active 判重复。原工具升级遇到 dirty receipt 的真实 provenance commit 与整体 metadata 不同时，尚未进入逐路径 bytes 核验即拒绝。

After：原维护新增闭合 `archive_resume`，公共 Trellis 仍单写投影、归档关系、generation、session/binding 和恢复回退。Guru 提供经语义审查的输入并消费 `resumed_task`；原六个私有 owner 用物理 `source_task_ref` 读取归档来源，用原活动 `task_ref` 核对 controls，分别冻结、退役和恢复自己精确资产。正式终态与未完成 closeout 各回原 Reactivate/恢复 owner，不制造业务完成。

current Identity/Bind 共用目标 installed 官方 active resolver 与选定 checkout；首次 C4 前只经公共 parser 和 active 占用检查交原 binding owner，绑定后继续公共解析。创建/历史 reservation 保留，旧 archive 不成为第二 current authority。目标 installed native continuation 和真实 Clarify/Completion 或新切片的 CreateDelivery/Author 由原语义 owner 验证。

原 upgrade owner 对 receipt 明确记录 dirty 的真实 provenance commit 只恢复逐路径历史候选资格，不接受完整 dirty source 身份，不替换为 HEAD。原 per-path bytes 检查、未知 preimage 显式 preserve/replace、clean mismatch 和缺对象阻塞保持。

## 项目合同承接

| Concern | 适用性与责任 |
| --- | --- |
| authority-binding | applicable；本轮 `.97` 原 authority、4.0/Delivery2.0 和项目 v1 绑定；`.98` 自身是受审差额。 |
| constitution-binding | applicable；必要能力复用公共恢复及现有 owners，没有第二 converter/updater、生命周期或授权持久化。 |
| boundary-and-decision | applicable；公共 Task/Delivery/session/binding 与原 Guru 语义/控制边界保持，ADR-024/027 无新决定或例外。 |
| owner-and-single-writer | applicable；公共数据、各私有 controls、Author、原升级与 Architecture/RDT 晋升各归原单写 owner。 |
| compatibility-and-exit | applicable；旧格式只在 maintenance 入口解释，普通 lifecycle current-only；真实旧 consumer 退出后由原明确 migration 删除 legacy profiles/readers。 |
| gap-and-deviation | applicable；局部收敛 transport/current identity 与 dirty provenance 的原逐路径来源资格；既有 GAP 保持，无新双 authority。 |
| parallel-scope | applicable；只写本 Task 的 canonical delta 与受审 Architecture targets；不触碰其它 Task、真实业务或未重读的 shared-current。 |
| evidence-and-freshness | applicable；独立评估绑定完整 candidate、原 authority 和精确拟写 targets；实际工程结果只读唯一 Test。 |
| review-and-promotion | applicable；原 owner 写前 expected-current、写后实际适用性、最终 Check、Task Commit 及 committed 独立完整审查各按原职责执行；Planning pass 不替代本轮评估。 |

Project check descriptor 为 `guru-trellis-architecture-convergence:repository:1`，id/version 为 `guru-trellis-architecture-convergence/1`；入口 `docs/architecture/06-governance/change-contract.md`，result contract2.0，原 ARCH-GOV-006..009、ADR-005/009 和 ARCH-GAP-006/008 保持。公开结果只投影下一 consumer 所需字段；完整 target bytes 和局部恢复意图不进入 tracked 审计。

## 验证与剩余边界

职责落点由 [唯一 Design](../../requirements-design-test-contributions/577-manual-archive-resume/design.md) 承接；实际命令、目标 installed/native/下一 owner、历史核验、恢复、首次失败和未验证边界由 [唯一 Test](../../requirements-design-test-contributions/577-manual-archive-resume/test.md) 单写。正式 Fork pin 不变，matching `local_candidate` 只证明隔离开发；实际安装 mode 差额不被 source_locked 放宽。完整 Plan2 安装矩阵、正式来源采用、真实业务恢复、软件发布及完整多平台 Release 矩阵按各原 owner 的证据边界报告。

本状态只记录 Architecture 晋升。最终 Check、Task Commit、committed 独立 Architecture 与完整 Branch Review 仍须覆盖实际 `.98` 候选，不由本文件预写为通过；Delivery、Completion/Closure/Finish 和软件发布也不由知识晋升推导。
