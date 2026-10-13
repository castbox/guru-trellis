# D1 真实远端事务恢复设计

## 唯一 authority 与边界
本 D1 使用现有公共 Task/Delivery API1/Task2，Task 531-remote-next-validation/gen0 的 UUID 为 50166a7c-d30a-40b2-bb7f-ca28d7d836a7。公共 store 是唯一状态 authority；Guru 原语义门禁和 Publish/Merge 私有事务只通过薄 projection 调用。整体需求在 ../../prd.md；本 D1 只拥有自己的五份规划/context，不写 Task-root design/implement。

## 现有能力与来源处置矩阵
| 来源 | 原承诺 | 处置及实际落点 | 理由与影响 |
| --- | --- | --- | --- |
| docs/design/README.md 与 DEC-531-OWNER-1 | 原 owner、公共状态单一来源 | 保留，各原 Skill 执行；不新增模型 | 独立候选评估为 no_architecture_impact |
| 原 Publish contract 的 same-plan 恢复 | 真实成功后恢复同 PR/readiness | 保留，在首次 ready 输出后暂不交 Merge，再同 owner 重入 | 真实 GitHub 读回；不能由包测试替代 |
| 原 Merge contract 的 terminal recovery | 同 merge facts、schema2 trailers | 保留，成功后再次原 owner 重入 | 不重复 merge，保持历史事实与当前 pass 分离 |
| 原 TaskCommit clean 合同 | 已提交稳定身份/五规划不重复提交 | 保留，十五文件一次提交，fresh Check 后同 HEAD clean 接续 | index/HEAD 不变；不得用重复提交补 gate |
| 原 scope_revision owner | 同 Delivery scope 与 root accepted_scope 接续 | 保留，本 D1 已由原 Activation scope-revision 接续；旧输出恢复同 key | 不建立新的 UUID 或 scope authority |

没有新增公共接口、writer 或平台入口。七份本仓 foundation 由原 Architecture/RDT/Bootstrap 激活，仅为样本 authority，不证明 Planning 或远端成功。

## 阶段 writer 与 consumer
Author 写本 D1 规划；Wording 只审查受控语言；独立 Architecture final_plan 后 Approval 作最终规划判断；Activation 写公共 Planning acceptance。实施只新增 validation/531-remote-next.txt。原 Check 作完整语义核验，TaskCommit 仅提交十五文件；首次完整 Branch Review 覆盖专用 base...HEAD；Delivery Review/readiness、Publish、Merge 分别由原 owner 消费各自最小 DTO。Completion 另读实际 Delivery 事实，不由 stopped 或旧 gate 推断 delivered。

## 正常恢复及证据失效
Publish 首次成功 stdout 保留在当前 owner 内存，暂不交下游；同计划重新调用原 Publish，实际 GitHub 同 PR/head/title/body/readiness/result 相等且无第二对象，再交 Merge。Merge 成功后同 owner terminal 恢复同 merge SHA/message/parents/base ancestry，保留五 trailers。若正常 re-entry 发现 stale authority、HEAD、scope 或外部事实，返回原 producer fresh 重审；不能复制历史 pass。历史 merge/PR 是不可被重新审查替代的事实。

## 返工与退出
范围变化回 Clarify→Task整体 PRD→accept_scope→当前阶段原合法 rework→同 D1 Author；机制变化重进 candidate assessment/final_plan。规划和 gate 输出丢失 fresh 重入原 owner。真实 blocker 记录具体缺口，不手改公共 state；无自然投影缺失仅声明包回归覆盖，不伪造 live 恢复。

## 候选与限制
冻结安装修复 source 的 managed identity 为 294178ce16ec15d034395d9d1160f7c6b2ca1982107e010750fca02891ac43cb；mixed CLI tar 5aeeb81ca72508081b7dd94ddb7a19f69444714f78b3a38858d908196cc77916，Core tar 45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967。漏 scope_revision 模块的旧安装失败保留；新安装/reapply 证据不等于 Release 矩阵。上游 CI 尚不能记为通过。业务原树和旧样本只读。
