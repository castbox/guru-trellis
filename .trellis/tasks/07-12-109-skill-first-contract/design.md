# #109 技术设计

## 1. 变更边界

本任务只在根 `AGENTS.md` 增加一个独立的“Skill-first 闭环流程模块化”章节，不修改 runtime 资产。该章节是仓库级 AI 行为规范，不是 skill package、workflow route、schema 或 installer 实现。

## 2. 章节位置

新章节放在现有“核心边界：Markdown 定义流程，脚本执行事实”之后、“Companion Script 的允许角色”之前。该位置形成以下阅读顺序：

1. 官方 Trellis 扩展面优先。
2. Markdown 与 script 的总体责任边界。
3. Skill-first 对 Markdown 控制面的进一步模块化约束。
4. Companion Script 的 executor/validator/recorder 细则。

现有后续章节编号顺延，内容不做无关改写。

## 3. 新章节结构

### 3.1 SSOT 分层

- Global workflow SSOT：全局 phase、mandatory invocation、transition、typed exit consumer、stop。
- Step-local skill SSOT：entry preconditions、正向行为、AI Gate、human confirmation、recorder/validator、artifact/freshness、typed exits。
- Platform entry：只负责加载/调用，不复制 skill 内部正文。

### 3.2 闭环与调用模式

- 固定闭环顺序。
- Workflow mode 复用 current upstream evidence。
- Standalone mode 自检 preconditions，但不能绕过同一 AI Gate 和 script boundary。
- Missing skill、unknown/multiple/unmapped exit 和无 consumer 统一 fail closed。

### 3.3 拆分触发与禁止拆分

- 强制拆分条件使用可审查的结构事实描述。
- 禁止拆分条件防止为了形式创建 wrapper skill。

### 3.4 Public API 与 package state

- `guru-<action>-<object>` 命名规则。
- Stable ids/exits/schema/scripts 的迁移约束。
- 公共 package 禁止携带 task/request/private/runtime 状态。

## 4. 避免重复 SSOT

新章节只定义 Skill-first 特有合同。以下内容继续引用现有章节，不重复展开：

- 官方文档与 marketplace 原则保留在第 1 节。
- executor/validator/recorder 的完整允许与禁止角色保留在 Companion Script 节。
- AI 必须执行的具体研发门禁清单保留在“必须保留的 AI 判断门禁”。
- 安装、upgrade/update、throwaway 和发布规则保留在现有对应章节。

## 5. Docs SSOT Plan

- docs state：`complete_docs`。
- strategy：`ssot_first`。
- affected durable file：`AGENTS.md`。
- checked but unchanged：`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/quality-guidelines.md`。它们用于一致性审查，不属于用户确认的修改范围。
- task artifact delta：仅保存本次章节结构、审查与验证证据，不向其它 durable docs 合并。
- merge checkpoint：实现完成后，trellis-check 必须确认 `AGENTS.md` 单文件 diff 已完整表达本 PR 范围。

## 6. 验证

- 对新增章节做受控措辞扫描与 AI classification。
- 对照现有 `AGENTS.md` 第 1、2、3、4、6、7、9、11 节检查重复和冲突。
- 运行 `git diff --check`。
- 审核最终业务 diff 只有 `AGENTS.md`；task artifact 作为 Trellis 元数据单独记录。

## 7. GitHub Scope 一致性

GitHub #109 正文已收敛为 `AGENTS.md` 单文件原则任务；被迁移的通用闭环合同与 Canonical 分发内容由 #120 独立承接。PR readiness 必须重读两个 live issue，确认当前 PR 只声明满足 #109，不借此关闭 #120。
