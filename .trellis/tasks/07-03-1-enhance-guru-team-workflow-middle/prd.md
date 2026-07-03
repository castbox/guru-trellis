# #1 Enhance guru-team workflow with middle-platform knowledge lookup and docs SSOT reconciliation

## 目标

增强可复用的 `guru-team` Trellis workflow，使 AI 在设计和实现阶段能显式处理两类容易漂移的上下文：

- 当任务涉及 Guru Team 中台 SDK / framework 时，按配置执行中台知识检索、引用和失败处理。
- 当业务仓库存在长期 `docs/` 文档体系时，Trellis task artifact 与 durable docs SSOT 协作，不形成静默并行真相源。

## 背景与已确认事实

- 来源 issue：<https://github.com/castbox/guru-trellis/issues/1>，当前无评论冲突。
- 当前仓库的主要交付面是 `trellis/workflows/guru-team/workflow.md`、`trellis/workflows/guru-team/config-template.yml`、workflow / preset README、以及 `trellis/presets/guru-team/overlays/` 下的平台入口文本。
- 官方 Trellis 文档确认：`workflow.md` 是 phase、skill routing、per-turn workflow-state breadcrumb 的主控制面；`.trellis/config.yaml` 缺省 key 走内置默认；hooks 主要做上下文注入和提醒，hook 失败不应作为核心阻塞门禁。
- 当前运行环境可用 `guru-knowledge-center` MCP；已用 `project_domain=middle-platform` 和本 issue 上下文检索到 go-guru 文档入口、ORM proto 规范、统一 ORM 指南和服务开发指南等 citation。该事实只作为本任务 research 证据，不把任何单一业务仓库的私有规则写进 workflow。
- 本 issue 要求保持官方 custom workflow marketplace / preset overlay 架构方向，不修改 Trellis upstream、全局 npm 包、`node_modules` 或业务仓库生成副本作为长期来源。

## 需求

### R1 中台知识门禁

- `guru-team` workflow 必须在 planning / design / implementation planning 中说明：当任务可能涉及 Guru Team 中台 SDK / framework 时，AI 应检查自身可用能力中是否有 `guru-knowledge-center` MCP。
- 检索目标应使用 `project_domain=middle-platform`，query 使用当前任务上下文，并覆盖相关 SDK / framework 指南，包括但不限于 `go-guru`、`proto-guru`、go-guru ORM / repo proto 生成约定、server framework、Unity3D / Flutter Guru SDK。
- 检索到的知识或 citation 必须持久化到 task artifact：优先写入 `design.md` 的 `中台知识依据`、`implement.md` 的 `实现前知识核对`，或 `{TASK_DIR}/research/middle-platform-knowledge.md`。
- 若 MCP 不可用，默认不全局阻塞，但必须显式警告用户；只有项目配置 opt-in 为 required 时才阻塞设计/实现推进。
- 门禁模式必须可配置为 `off | optional_warn | required`；缺失 `middle_platform_knowledge.mode` 必须解释为 `optional_warn`。
- 新安装的 `config-template.yml` 应显式展示默认 `middle_platform_knowledge.mode: optional_warn`；preset upgrade 不得为了补 key 覆盖已有目标仓库 `.trellis/guru-team/config.yml`。
- workflow 不应假设 shell companion script 能检测 MCP 可用性；MCP availability 属于 AI 平台运行时能力，由入口文本和 workflow 指示 AI 自检。

### R2 durable docs SSOT 对齐

- planning 阶段必须检测目标仓库是否有 durable docs library，通常在 `docs/` 下，类别包括 requirements、designs、testplans、deploy / operations、versioned design docs 等。
- 当完整或部分 docs SSOT 存在时，`prd.md`、`design.md`、`implement.md` 只记录 task-scoped delta、决策、证据和链接，并列出本任务需要更新的 durable docs；不得静默成为并行长期真相源。
- finish-work / publish 前必须执行 Docs SSOT reconciliation：判断本任务是否改变长期产品、架构、API、数据、部署、运维或测试合同；记录哪些 docs 被更新、哪些 task artifact 内容被合并回 durable docs、哪些仅保留为 task history。
- 若目标仓库没有完整 docs 系统，task artifact 可作为当前任务临时 SSOT，但 finish-time reconciliation 必须明确记录：创建新 durable docs、补充已有 partial docs，或确认当前仓库暂不设 durable docs SSOT 且 task artifact 仅作为归档证据。

### R3 同步 workflow 发行面

- `trellis/workflows/guru-team/workflow.md` 是详细规则 SSOT。
- `trellis/workflows/guru-team/config-template.yml` 同步新增配置 knob。
- `trellis/workflows/guru-team/README.md` 与 `trellis/presets/guru-team/README.md` 说明新增门禁、默认行为和安装/升级注意事项。
- 相关平台 overlays 只做入口提醒和路由提示，详细规则仍指向 `.trellis/workflow.md`。
- preset installer 如无必要不新增 merge 行为；既有 config preserve 语义必须保留。

### R4 通用性与安全边界

- 不写入 `chengtuo-resume` 或其他单一业务仓库的私有规则。
- 不把核心阻塞门禁放入可能静默失败的 lifecycle hook。
- 不输出 token、私钥、`.env`、数据库 URL、signed URL 或敏感 raw record。

## 验收标准

- [ ] AC1：`guru-team` workflow 文档化 Middle-platform Knowledge Gate，并覆盖 design / implementation planning。
- [ ] AC2：缺失 `guru-knowledge-center` MCP 的默认行为是 `optional_warn`，不是 hard block。
- [ ] AC3：workflow 和配置模板支持 `off | optional_warn | required`。
- [ ] AC4：workflow 要求 MCP 可用时持久化中台知识或 citation 到 task artifact。
- [ ] AC5：workflow 文档化 planning-time repo `docs/` SSOT discovery。
- [ ] AC6：workflow 文档化 finish-time Docs SSOT reconciliation。
- [ ] AC7：完整 docs、partial docs、无 docs 三类仓库都有明确处理规则。
- [ ] AC8：变更保持 Guru Team workflow 通用，不编码单一业务仓库私有规则。
- [ ] AC9：workflow、config template、README、平台 overlays 同步，不产生互相冲突的门禁说明。
- [ ] AC10：验证命令至少覆盖 issue 建议的 JSON、bash syntax、Python compile、`git diff --check`；若 overlay / installer 行为变化，再用临时 Trellis 项目验证 preset installer preserve / `.new` 语义。

## 非目标

- 不实现项目特定的 `chengtuo-resume` 策略。
- 不要求所有团队安装 `guru-knowledge-center`。
- 不在 `guru-knowledge-center` 不可用时全局阻塞所有 Trellis 工作。
- 不把 durable 产品 / 架构文档整体迁移到 `.trellis/tasks/`。
- 不用隐藏 lifecycle hook 实现这些门禁。

## 当前开放问题

无阻塞开放问题。issue 已给出配置默认、迁移约束和建议文件；仓库 inspection 已确认交付面。
