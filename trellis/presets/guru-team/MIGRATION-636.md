# #636：提前 Draft 与最终门禁的成套迁移

本迁移直接演进原 TaskCommit、Publication、Branch Review 和受控 consumer。
它不改变 upstream Delivery API 1.0、Task schema 2.0、Task/Delivery 身份或公共 phase。
旧固定安装继续使用其固定版本。当前 runtime 不双读旧 candidate/transaction，
也不将历史 schema 当 current fallback。安装新源码不代表已有项目已迁移。

## 当前切换集合

| 原 owner / consumer | 新 current 合同 | 保留与退出 |
| --- | --- | --- |
| TaskCommit prepare/invoke、receipt recovery | 私有 candidate/result delivery-2.0 的 draft/final 闭合 union；公共 aggregate 2.0；新 delivery_draft_commit、delivery_draft_committed_reentry 和 draft_committed | 最终 Check 输入、committed DTO 和语义保持；未执行 1.0 candidate 重新 prepare，不机械转换成早期通过 |
| Publication preview/invoke/same-plan recovery | 私有 transaction 2.0 的 action/terminal；公共 aggregate 2.0；draft_publish、return_to_draft、draft_published、draft_revision_ready | Draft 不写 PublicationFact；Ready 仍消费真实 readiness。1.0 事务只由原迁移命令读取一次 |
| Branch Review early feedback / formal Review | 独立 early input/output；Delivery aggregate 3.0 和含 legacy maintenance 的 index 3.0 | early 不写 full_review；正式 Check predecessor、alignment、continuity 和 archive profiles 保持 |
| Workflow / continuation | 五个唯一 Draft routers 与显式原 Skill 调用；同 B/H 的独立内容分析和 HEAD 验证并行 | 不添加 public phase、统一候选账本或跨阶段 review cache；最终完整链保持 |
| Preset / platform | matching packages/runtime/interfaces/schemas/consumer schemas/workflow/22 finish launchers/managed specs | 不单独复制一个 package 或覆盖用户文件；保持官方 marketplace 与完整 preset 机制 |

早期 TaskCommit 的完整 dirty 分类、精确 staging、敏感内容检查、真实 hooks、
隔离事务、无关状态保留和同提交输出恢复保持。其输入没有 check_result_id，
其输出只能进入 Draft router。最终 committed 不能接收 early DTO。

## 在途任务与恢复

- implementing：保留 accepted_scope、Planning、identity 与固定 B。没有 Check 时可经
  早期入口提交/发布；未接受 Planning 回原 Planning owner。
- checking/reviewing：可完成原最终链。需要先发布修订时，由当前 owner 合法 rework
  到 implementing。活动 merge/sequencer 仍由原 Git integration owner 完成；原 Reconcile
  已生成真实 integration commit 后，可用 early clean reentry，不额外要求 Check。
- publishing：由原 Publication delivery_return_to_draft 回读原 PR/HEAD/state、确认 Draft
  并 rework 到 implementing，清除受影响 check/full_review/readiness。身份、Planning 和
  历史 PublicationFact 保留。新 HEAD 不能消费旧 readiness。
- delivered/stopped、归档和无 PR 的任务：不转换为活动 Draft，不重开 Issue，不新建 Delivery。

旧 TaskCommit 已成功 receipt 必须先由匹配旧 producer 恢复原提交输出，再切换。
未执行 candidate 在新完整安装后按实际 dirty、所选 profile 和新语义审查重新 prepare。
不造空提交、不 stage runtime、不把旧 Check 改名为 early pass。

## Publication 1.0 → 2.0 一次性转换

由原 Publication AI owner 读取实际 Task/key、原事务、PR/HEAD、载荷、stage 和已执行动作，
完成有界语义核对后调用原命令：

```text
scripts/migrate-delivery-transaction.sh --root <checkout> --input <publication_transaction_636> --owner-result <review> --preview
scripts/migrate-delivery-transaction.sh --root <checkout> --input <publication_transaction_636> --owner-result <review>
```

独立 input schema 为 private-publication-transaction-636-input.schema.json，字段是
profile=publication_transaction_636、task_ref、delivery_key、transaction_ref。
review 使用原 private-delivery-migration-review-1.0.schema.json，不含授权信息。

原 terminal Ready 只在实际 PR/HEAD/title/body/非 Draft 读回一致时转换。
pending Ready 还需原 current readiness 与候选适用。转换保留 transaction_ref、原 input、
stage、public_candidate、PR binding 和 mutation decisions，仅补入 current action=ready、
terminal=ready、schema_version=2.0 并重算局部一致性 digest。它不执行远端 mutation，
不写 gate，也不将旧 Ready 意图改成 Draft。pre-Delivery cycle 的旧显式迁移继续由其原
独立 profile 处理，输出也进入 2.0；不是当前 runtime 的兼容分支。

输出丢失先恢复原 producer 再切换。PR 或动作匹配不明确时停止并给出具体缺口，
不猜测身份/载荷、不合成 readiness。新事务通过原 same-plan profile 恢复；新动作先
核对并退休上一已完成事务，保留的只是一份同操作输出恢复状态，不积累历轮审计。

## 安装、回退与验证边界

选定精确来源和目标后，用官方 marketplace matching workflow 和完整 preset reapply。
先保留本次受影响 owner-private 事务的有界 backup；按原 upgrade owner 的精确 write set
恢复或回退，不自行改官方 .trellis/scripts/common。保留用户修改及 template hashes，
逐项处理 .new/.bak，核验 actual package/discovery、可执行权限与 drift。

定向验证覆盖公共 wrapper 无 Check 真实提交、同提交恢复、同 PR Draft 更新、先 Draft 后
push、Draft/Ready 状态输出丢失恢复、新 HEAD 旧 gate 拒绝、固定 B/H、无 merge ref 的 HEAD
验证合同和一次性转换。provider fixture 不是实际 GitHub 成功；源码检查不是安装或业务 CI
通过。完整多平台 Release 矩阵继续由专门 owner 承担。
