# #600 ADR 候选：在最终 Check 前晋升受审架构差额

状态：`draft`。本候选尚未激活 shared Architecture authority。

## 决策

将 ADR-005 及其后继合同中“先完整 committed Branch Review，再晋升，再重做完整 Review”的顺序片段，替换为现有 Phase2 独立 Architecture 评估及拟写审查 → 原 owner expected-current 分支内晋升 → 最终 Check → Task Commit → committed 独立 Architecture 及一次完整 Branch Review。一次只约束稳定正常候选，不限制 finding 修复、多 Delivery 或合法提交后绑定刷新。

晋升前 authority 继续是比较起点，新 CURRENT 自身属于受审变更。来源是当前 #600，不因原基线已经存在而禁止真实演进，也不以新 CURRENT 自证实现正确。ADR-019 的独立输入、原 finding lifecycle、ADR-028 的阶段适用性和 ADR-029 的工程事实采用保持。

## 取舍与边界

同一评估不新增审批阶段。原 Architecture 仍单写 CURRENT；script 只执行和校验事实。窄引用/状态修订只对齐已有事实，由原 Review owner 经明确输入和正式 passed consumer 覆盖最终候选；Git continuity 只用于真实整合。

partial promotion 和在途迁移沿原 owner 恢复，不新增账本、长期审查历史、第二状态机或授权记录。完整版本安装是切换边界；未验证 Release、业务采用、部署不作通过主张。
