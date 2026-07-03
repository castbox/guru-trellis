# 设计方案

## 范围

本任务修改 Guru Team reusable workflow 的发行资产：

- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/config-template.yml`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `trellis/presets/guru-team/overlays/` 下 start / continue / finish-work 入口提示

不修改 Trellis upstream、全局 npm package、`node_modules`、业务仓库生成副本，不新增项目私有规则。

## 架构边界

`workflow.md` 是详细规则 SSOT：

- Phase 1 增加 planning-time docs SSOT discovery 和 Middle-platform Knowledge Gate。
- Phase 2 增加 implementation 前知识核对，确保进入代码修改前已检索 / 警告 / 阻塞。
- Phase 3 增加 Docs SSOT reconciliation，要求在 commit / Branch Review Gate / finish-work 之前记录结果。
- Branch Review Gate 证据要求补充 docs SSOT reconciliation 覆盖。

`config-template.yml` 只暴露配置 knob：

```yaml
middle_platform_knowledge:
  mode: optional_warn
```

缺失 key 的运行解释由 workflow 文案负责，preset installer 继续保留“已有 `.trellis/guru-team/config.yml` 不覆盖”的语义。

Platform overlays 只做短提醒：

- start：初始化时提示遵循 workflow 的 knowledge gate 和 docs SSOT 规则。
- continue：planning / in_progress / after commit 的路线增加知识门禁和 docs reconciliation。
- finish-work：提示 finish 前已通过 Branch Review Gate 且 gate 证据覆盖 docs SSOT reconciliation。

## 中台知识门禁语义

配置解析：

- `off`：不检查、不告警、不要求持久化。
- `optional_warn`：默认；相关任务能检索就检索并持久化 citation，不可用就显式告警并继续。
- `required`：相关任务必须完成检索并持久化 citation；MCP 不可用、检索失败或无可引用证据时阻塞 design / implementation 继续推进，直到用户调整配置或补齐知识来源。
- 缺失 `middle_platform_knowledge.mode` 解释为 `optional_warn`。

触发条件：

- 当前任务涉及或可能涉及 Guru Team middle-platform SDK / framework。
- 示例关键词包括 `go-guru`、`proto-guru`、ORM / Repo Proto 生成、server framework、Unity3D / Flutter Guru SDK。
- 若不相关，记录“不适用”即可，不做无意义检索。

AI 执行步骤：

1. 检查可用工具 / MCP server 中是否有 `guru-knowledge-center`。
2. 如可用，使用 `project_domain=middle-platform` 和当前任务上下文检索。
3. 把 citation 或摘要写入 `design.md`、`implement.md` 或 `{TASK_DIR}/research/middle-platform-knowledge.md`。
4. 如不可用，根据配置 warning / block / skip。

## Docs SSOT reconciliation 语义

Planning-time discovery：

- 检查目标 repo 是否存在 `docs/` 或等价 durable docs library。
- 识别已存在类别：requirements、designs、testplans、deploy / operations、versioned design docs。
- 在 `prd.md` / `design.md` / `implement.md` 中记录本任务相关 durable docs、待更新 docs 和不需要更新的理由。

Finish-time reconciliation：

- 判断是否改变长期产品、架构、API、数据、部署、运维或测试合同。
- 记录已更新 docs、从 task artifact 合并回 durable docs 的内容、仅保留为 task history 的内容。
- 三类仓库的结果必须明确：
  - 完整 docs：更新对应 docs 或记录无需更新理由。
  - partial docs：补充已有 docs 或记录缺口 / follow-up。
  - 无 docs：创建新 docs、确认暂不创建，或说明 task artifact 仅作为归档证据。

## 兼容性与迁移

- 新安装通过 `config-template.yml` 显式看到 `middle_platform_knowledge.mode: optional_warn`。
- 已安装项目如果已有 `.trellis/guru-team/config.yml`，preset installer 不覆盖、不合并补 key；workflow 对缺失 key 使用 backward-compatible 默认。
- 不新增 shell detection，因为 MCP availability 是 AI runtime capability。

## 风险与缓解

- 风险：规则散落在 README / overlay 导致漂移。缓解：详细规则只写 `workflow.md`，其他文件只摘要和指向。
- 风险：`required` 被误当全局默认。缓解：多处明确 required 是 opt-in only，missing key 是 optional_warn。
- 风险：Docs reconciliation 成为口头检查。缓解：Phase 3 和 Branch Review Gate evidence 都要求记录 reconciliation 结论。

## 中台知识依据

本任务检索了 `guru-knowledge-center`，trace id 为 `6218cc88-6450-427f-8b4f-79be47d49944`。返回 evidence 已保存到 `research/middle-platform-knowledge.md`。这些 citation 用于证明 workflow 中示例关键词的通用性，不把 go-guru 具体实现规范内嵌进 workflow。
