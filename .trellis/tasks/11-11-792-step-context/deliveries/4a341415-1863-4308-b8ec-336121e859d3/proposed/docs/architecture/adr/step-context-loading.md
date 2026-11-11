# ADR-STEP-CONTEXT-LOADING：当前出口与步骤上下文加载

状态：proposed。来源为 [#792 隔离贡献](../contributions/792-step-context.md)及
[Issue #792](https://github.com/castbox/guru-trellis/issues/792)，固定 before Git 为
`05a16a5989669ca216d8ba34b9b419776410f04d`。只有原 Architecture owner 在完整候选检查后
经 final_integration 整合并读回，才形成共享当前决定；本拟写不证明该过程已经完成。

## Context

原 workflow 已拥有明确阶段、mandatory Skill、typed exits、consumer 和条件 router，
却把完整图和历史细节放在正常必读范围。原 discovery、Interface 与 native 提取已有
可复用边界。问题是当前步骤上下文的取得方式；不需要改变生命周期权威。

## Decision

采用一个 workflow-owned managed routing reference，保留原标记与完整 router/stop 条件。
原 Interface 继续拥有各 Skill 合同，runtime 校验二者一致并按 producer＋exit 提供直接
consumer 及入口/前置定位。正常新 runtime 只接受明确 reference；无 exit 的原合同查询保持。

通过 Guru Markdown 组织调整 Phase Index 和唯一 continuation 的提取内容，详细路由与
legacy 合同只在实际入口加载。原 AI owner 解释条件和判断充分性；脚本不选 profile、
不生成语义 pass，也不拥有执行资格。upstream native API 与公共 Skill/exit/consumer 保持。
完整能力、失败行为及 owner 定义只由 [ARCH-CONTEXT-001](../03-domains/workflow-context.md)
承载，本 ADR 不复制其执行正文。

## Alternatives 与后果

第二 JSON 表会引入第二活动映射；通用 include、wrapper 或长期缓存没有当前必要
consumer；脚本按 profile 选下游会转移语义权威；修改 upstream extractor/hook 则越过
官方扩展面。直接复用原查询、reader、原生提取与 preset 能承担当前要求，因此不采用这些方案。

本选择减少正常 AI 入口被要求加载的无关正文，但仍有确定性全图校验、一次出口查询及
matching 资产维护成本。文件长度或局部绿色不能证明整体运行效能，实际效果按唯一 Test
的观察层次判断，不设置固定成本降幅或完整平台矩阵。

## 与 ADR-035 的关系

本决定仅补充 [ADR-035](035-current-continuation-scope-routing.md)的发现、加载和分发组织。
其唯一 continuation、接收会话自身检查、公共 current、原 producer 恢复、scope 两次承接、
phase 非 gate 及终态 owner 全部保留。这里没有替代身份/selection/阶段资格，也没有新 pass adapter。

## 采用、退出与重评

原 preset/tools owner 成套采用 matching workflow、reference、runtime 和实际受影响投影。
缺失或混装时停止，由原 owner 修复，不能 fallback inline。旧安装保留原 provider，
通过原维护入口整体更新；不迁移 Task 状态或改历史字节。

原 verifier 只有显式旧 before-snapshot 的只读 inline 观察，不恢复正常 runtime 资格。
该观察由 verifier owner 在受支持 before 样本退出 inline 后删除。其他真实 legacy
维护仍由原 owner 保留准确来源、支持条件和恢复边界。

消费者、native 提取、权威职责或实际加载/维护成本出现实质变化时，回原 Architecture
及受影响 owner 重评。采用说明见 [MIGRATION-792](../../../trellis/presets/guru-team/MIGRATION-792.md)，
验证观察见 [#792 Test](../../requirements-design-test-contributions/792-step-context/test.md)。
本 ADR 不声明正式质量门禁、安装、业务效果或 Release 已通过。
