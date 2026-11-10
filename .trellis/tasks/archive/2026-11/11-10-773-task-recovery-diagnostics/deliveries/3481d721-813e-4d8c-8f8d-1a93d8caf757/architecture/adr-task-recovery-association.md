# ADR-TASK-RECOVERY-ASSOCIATION：已恢复工作区的显式 Task 关联

状态：proposed；来源：#773 R2；基线：`313d80215f65777fc70893a90c6d8dce8005d6dd`。接受与生效须经原 Architecture 最终整合，不因候选文件存在而成立。

## 问题与决定

原 Git 载体中的 schema2 Task、Delivery 和完整规划可恢复到目标 checkout，Identity 能读取工作区。但原初次 Branch 候选按 HEAD 树读取，未跟踪恢复目录不能成为候选；Rebind 又要求已有绑定。现有公开能力之间缺少首次关联动作。要求恢复者提交或手编本机 controls 均超出原恢复合同。

在原 Branch owner 增加显式 `delivery_restored_checkout` profile，输入最小 TaskKey/TaskRef、明确 branch_name 和 expected_head，root 为当前注册 checkout。客观验证恢复后的 active schema2 身份、注册分支/HEAD 与 C4/C5 冲突后，原事务只建立缺失控制、复用匹配控制。C4 使用原 OwnershipPort，不直接写 C5 ledger。新缺失权属采用 caller_owned，primary worktree 为 not_applicable，linked 为 caller_owned；已有权属保留。

普通 HEAD 候选/排序、Creation 和 Rebind 不变。输出仍为原 TaskKey/typed exits，Ensure→接收聊天 Bind→continuation 保持原 consumers。Git 文件恢复、目标基线 writer、身份、关联、会话和历史 gate 分别表达；没有新身份、授权记录、store 或空 Delivery。

## 替代、代价与重评条件

仅补文字不能执行首次关联；强制 commit 添加无必要副作用；放宽普通 discovery 会改变所有正常调用的 HEAD 准入；复用 Creation 会重建身份并错误继承非 primary/non-base 限制；复用 Rebind 不满足其已有控制及 clean 前提。新 owner/通用恢复框架无当前必要性。

显式 profile 增加一个有直接 caller/验收的输入分支，代价为 schema/interface/示例/迁移说明及定向测试维护。通过原事务复用限制重复 writer。旧 profile/output 保持，新 aggregate schema identity 和 matching tools 升级明确，不热迁移旧安装。

当公共 Trellis 提供等价首次恢复关联、当前 C4/C5 authority 改变或普通 HEAD 候选合同实质演进时，由原 Branch/Architecture 重评并显式迁移，不预留策略或适配器。当前无宪法例外，不改变 portable shared lifecycle，不关闭已有全局 GAP。

## 验证与晋升

一条去敏代表场景从固定 Git 载体恢复未提交工作区，实际调用新公开 Branch，再观察原 Bind 的同身份结果及历史缺口；另保必要普通失配/复用回归。静态说明与组件 fixture 不证明 native Agent 全链。完整实现及全部拟晋升 after 先经独立 Architecture 和 candidate Check，再原 owners 晋升/readback、重绑 after、最终 Check/commit/独立完整 Review。实际结果由 Test 记录，本决定不声明已通过。
