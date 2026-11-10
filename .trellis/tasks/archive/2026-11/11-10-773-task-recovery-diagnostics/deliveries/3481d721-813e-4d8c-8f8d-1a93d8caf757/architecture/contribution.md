# #773 Architecture contribution：工作区原 Task 的初次恢复关联

状态：proposed；owner 为原 Author/Architecture；来源为 #773 R1/R2 和本 Delivery design。基线 `313d80215f65777fc70893a90c6d8dce8005d6dd:docs/architecture/` 保持可重读。本文件不修改共享 authority，不证明实现或安装通过。

## 完整局部规则

同身份恢复先固定原 Git 载体并核唯一 schema2 TaskId/generation、source/scope、Delivery、完整规划及真实历史缺口。AI 判断恢复意图、载体充分性、目标基线和精确写集；Git 恢复原文件，原 task.py 写所选基线。原 Identity 验证工作区 Task。普通未绑定候选仍从 HEAD 树验证，不通过重复 discovery、隐含 commit 或私有 JSON 修补恢复。

新增 Branch `delivery_restored_checkout` 只承接上述已恢复工作区的显式初次／补缺 C4/C5 关联。它验证当前注册 checkout 的分支/HEAD、active Task 身份及既有控制冲突。matching 项复用；只有缺失项经原事务建立，同 key/branch/revision 必须一致，不覆盖其他关联。C4 仍通过原 OwnershipPort 调 C5，保留 snapshot/rollback/readback；不新建 authority 或 store。缺失 ownership 时 branch 为 caller_owned，primary worktree 为 not_applicable，linked 为 caller_owned；既有权属保留。

新 profile 不继承 Creation 的 primary/non-base 限制。普通 HEAD discovery/排序及 Rebind 准入不变。成功只输出原 TaskKey，交 Ensure 解析唯一 checkout，再由接收聊天自身 Bind 并读 current/continuation。关联、session、Delivery 和 Task Completion 分别表达；Publication/Delivery/full_review/readiness 缺口不补造。输出丢失走原 discovery/read-only recover，不把状态写入恢复账本。

## 九项 concern 与变化

| Concern | 适用性、事实与处置 |
| --- | --- |
| authority-binding | applicable；原 Planning 3.0 candidate/final，后续 phase2/final integration/committed Review 均由原 owner，baseline identity 不变。 |
| constitution-binding | applicable；完整五原则已读。显式窄准入解决真实公开缺口，原 owner/port 隔离职责，不预留未来恢复机制。 |
| boundary-and-decision | applicable；target_native；保留 ADR-PORTABLE-SHARED-LIFECYCLE，新增 proposed ADR-TASK-RECOVERY-ASSOCIATION 说明工作区恢复准入。 |
| owner-and-single-writer | applicable；Author 规划、Branch/C4/C5 原事务、Git/task.py/Bind 原 writers、RDT/Architecture 晋升分别保留。 |
| compatibility-and-exit | applicable；旧 profile 和 outputs 保持，新 profile/aggregate identity 显式升级；无 legacy adapter/dual-read，旧完整安装不热解释新输入。 |
| gap-and-deviation | applicable；关闭本 Task 已核的“工作区恢复无法首次关联”局部缺口；不关闭 ARCH-GAP-006/008，不新增通用恢复或历史 gate 承诺。 |
| parallel-scope | applicable；先只写本 Task 隔离贡献/完整 proposed targets；共享 C4/C5 真实关系仅由原 Architecture final_integration 结合 live 原文整合。 |
| evidence-and-freshness | applicable；design 第8节 V1–V5；实际结果待执行。candidate 只在当前八事实/六约束下适用，完整新实现和拟写须独立重审。 |
| review-and-promotion | applicable；本贡献与必要 ADR 先 final_plan；实施阶段准备全部 targets，经独立 phase2 和 candidate Check 后晋升/readback，再最终 Check/commit/完整 Review。 |

## 共享目标、原 writer 与验证边界

Architecture 拟写 `docs/architecture/03-domains/ownership.md` 中原 C4/C5 关系及 `docs/architecture/adr/task-recovery-association.md`。前者须展开当前 owner/输入边界和原消费者，不能只登记本 Issue；后者写完整决定、替代与代价。实施阶段准备完整 after，在独立 phase2/candidate Check 前可读。原 promotion owner 写前核 expected-current，写后核真实内容，再重绑最终质量链。

RDT 原 owner 用三个独立 task-carrier-recovery 叶子写完整 R/D/T，不向根或索引登记。验证是共用缺失诊断、代表性 Git carrier→新 Branch→同身份 Bind、控制边界和受管投影；不重做 #223、native Agent 全链或 Release 矩阵。当前所有实施与运行证据均未发生。
