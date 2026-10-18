# Trellis 扩展技术基线 1.0

Identity：`trellis-extension-stack`；version：`1.0`；状态：`accepted`。本页拥有此版本的完整通用技术定义。接受不证明任一消费项目已经实现或通过安装验证。

## 范围与维护方

本基线适用于通过官方扩展面交付 AI 开发流程、工程约定和确定性 companion tools 的 Trellis 扩展。它不选择业务应用语言、数据库、云平台或 UI 框架，也不替代 Trellis 自身的框架合同。

公共技术基线维护方通过 `guru-maintain-architecture-baseline` 维护本页。消费项目的 Architecture owner 维护独立选择投影，固定本基线 locator/version、适用范围、项目约束和差异。项目变更只在自身范围生效；需要改变通用定义时，另向公共源提出隔离贡献，由源维护方审查并发布 successor。

## 完整技术选择

| Stable ID | 选择及完整适用条件 |
| --- | --- |
| `TES-EXT-001` | 使用 Trellis workflow marketplace 发布流程，用 spec template marketplace 发布可复用工程约定。workflow id、template id 和 preset 路径是公共接口。消费项目固定匹配的 Trellis 与扩展版本；本基线不指定某个项目的框架 commit 或软件 Release。 |
| `TES-AI-001` | 使用 UTF-8 Markdown 定义 AI 运行时流程、独立 Skill 行为、工程约定和平台入口。全局 workflow 负责阶段顺序、mandatory invocation、跨 Skill transition 和唯一 typed-exit consumer；Skill 独占本步骤的 preconditions、语义判断、恢复和出口。平台入口只加载和路由。不得通过 hook、上游源码、全局 npm 或 `node_modules` 实现流程分叉。框架自身缺陷由框架维护方修复，消费项目固定其受审版本。 |
| `TES-EXEC-001` | companion tools 使用 Python 3 实现结构化读取、确定性执行、校验和最小结果记录；需要平台 shell 集成时使用 Bash 薄入口。脚本不判断需求含义、设计充分性、finding、Issue 关闭意图或 PR readiness。需要 AI 判断的 Skill 由 AI 先作判断，再调用 recorder/validator。确定性 Skill 只有在整个输入、转换、副作用和结果条件均可机器验证时才使用 deterministic profile。 |
| `TES-DATA-001` | 使用 JSON 表达公共机器接口和结构化事实，以声明版本的 JSON Schema 校验 shape。项目配置可使用 YAML，必须由所属配置合同定义字段。不要把完整内部 artifact 作为 public handoff；只传唯一直接 consumer 必须消费的 identity 或结果。派生 Git facts、digest 和短期恢复内容留在原 owner 的私有运行状态；无直接 consumer 的状态不写入。用户授权只存在于当前对话。 |
| `TES-GIT-001` | 使用 Git commit/ref/worktree 表达内容、分支和隔离 checkout；使用显式绑定目标仓库的 `gh` CLI 读取及执行 GitHub Issue/PR 操作。AI 判断对象、scope、风险和必要副作用；工具按精确输入执行并重读真实结果。分支名、路径和会话摘要不能代替 Task identity、已审内容或 semantic pass。普通 dirty/过期/目标错配按原 owner 恢复，保护无关修改。 |
| `TES-DIST-001` | canonical workflow、Skill、preset、spec 和 platform overlay 是长期源。workflow marketplace 只交付 workflow；完整 preset 交付匹配的 packages/runtime/schema/config/声明平台投影。dogfood 与 installed 副本通过原 installer/apply 生成。官方 update 后重新选择匹配 workflow 并 reapply preset；按管理 hash 保护用户修改，逐个处理 `.new`/`.bak`，再验证 drift。不能以一次手工 patch 作为长期扩展机制。 |
| `TES-TEST-001` | 对 Python 使用项目声明的定向测试，对 Bash 入口检查语法和实际调用；同时验证公共接口、canonical/dogfood/installed 关系及受影响的平台投影。涉及安装时使用受支持的 clean/update/reapply 入口。需要证明 Agent 行为时，用实际独立会话验证，不能用字符串、schema 或链接检查代替。普通变更只运行 accepted scope 必需的可靠验证；累计兼容、框架升级和 Release 的完整矩阵由其专门合同拥有。 |
| `TES-KNOW-001` | 使用带稳定身份的 Markdown 完整知识单元和薄导航。Requirements、Design、Test 保持可追踪关系；Architecture 保留 FOUNDATION/CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE 职责。当前定义展开必要条件、否定、例外和顺序；历史贡献记录来源，不成为普通查询必须回放的正文拼接链。原维护方将隔离贡献晋升为完整一致单元。必要来源缺失、断链、冲突或迁移未完成时明确受影响结论，回原 repair，不推定完整或实现通过。 |

上述语言、格式和工具是此基线的技术选择。具体 Python/Bash/Node/CLI 版本、包依赖与平台支持由消费项目固定并验证；未固定或未验证的项目不能据此声称可运行。没有真实 consumer 时，不新增数据库、检索服务、自动 authority 选择器、长期遥测或状态协调服务。

## 读取、修订与兼容

查询时先读项目选择投影，再读本页的准确版本和相关项目约束。需要解释决策原因才展开来源历史；导航不能替代正文。通用定义与项目差异冲突时，明确对象和适用性，回原 Architecture owner 判断，不自动覆盖任一方。

修订通用定义时，源维护方核对现有条款及依赖，保留未改变的身份和条件。插入或移动不重编号无关对象；删除、替换、拆分和合并保留前驱/后继定位。接受后的本版本不追溯改写，新版本明确替代范围。项目 owner 决定合法采用时点；无关源推进不强制旧 Task/阶段重选版本。旧版本只读依赖结束后退出普通读取，历史继续可追溯，不保留双写。

## 依据与证据边界

- [Trellis 官方文档](https://docs.trytrellis.app/index.md)：框架入口。
- [Customizing the Workflow](https://docs.trytrellis.app/advanced/custom-workflow.md)：workflow Markdown 的运行时职责。
- [Custom Spec Template Marketplace](https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md)：可复用工程约定的官方分发面。

本基线声明扩展技术约束。它不是安装 receipt、生产采用证据或 Release gate；每个消费项目由自身 Test/EVIDENCE 说明实际验证与缺口。
