# #553 Design/Contract追踪

状态：candidate。行为细节由[原Reconcile合同](../../../trellis/skills/guru-team/packages/guru-reconcile-task-base/references/contract.md)独占；此文只拥有职责与双向trace，不作为第二step-local合同。

| Design / contract | 归属和直接consumer |
| --- | --- |
| D553-01 / CON553-PAIR | 原Reconcile post_plan读取当前authority/Planning、operation pair；原Activation消费既有reconciled handoff |
| D553-02 / CON553-CANDIDATE | 原candidate命令客观验证resolved tree/paths及显式baseline argv；AI独占冲突内容和路径选择 |
| D553-03 / CON553-COMMIT | 原exact executor用临时index提交受审tree；原真实index/worktree与pending内容保持；原recorder/checker读committed tree |
| D553-04 / CON553-RECOVERY | 同请求exact parents/tree/message恢复已有commit；原owner处理freshness/authority变化 |
| D553-05 / CON553-GATES | 后续完整businessCheck、TaskCommit、首次完整BranchReview、readiness职责不变；baseline不占这些gate slot |
| D553-06 / CON553-PROJECTION | 完整matching current安装消费新私有输入；旧完整安装由原D2迁移边界管理，禁止半投影或跨模型借用DTO |

当前Architecture .89/current及constitution v1保持；实际独立candidate/final assessment为no_architecture_impact。此结论不替代Phase2、完整committed Review或测试。
