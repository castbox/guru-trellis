# #17 Improve Guru Team PR body quality standards

## 目标

把 Guru Team `finish-work` / `publish-pr` 生成 PR body 的质量标准从口头期望变成 workflow、AI 入口和 companion script 共同执行的发布合同。未来非 draft PR body 必须面向不了解 Trellis task 的 GitHub reviewer 自解释，不能用“当前 Trellis task”“已提交实现与文档更新”这类低信息量摘要替代真实变更说明。

## 背景与证据

- Source issue: https://github.com/castbox/guru-trellis/issues/17
- 参考 PR: `castbox/go-guru#184`、`castbox/go-guru#95`。两者共同特征是 `变更摘要` 按问题修复 / 新增功能 / 文档更新 / 重构等类型分组，bullet 描述具体行为变化，`影响范围` 明确列出受影响模块，`关联议题` 明确 close/ref 语义，`附加说明` 用自然语言解释目的与风险边界。
- 当前代码证据：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 的 `build_pr_body()` 仍硬编码 `本 PR 承接当前 Trellis task 的已提交实现与文档更新。`，且缺少对 AI 审阅后的 PR body artifact / body file 的优先使用路径。
- 官方 Trellis 文档核对：`workflow.md` 是 workflow 行为主控制面，workflow marketplace 不需要改上游源码；spec template marketplace 只放可复用规范、目录/API/测试/错误处理/review checklist 和去敏例子，不放 active task 或 runtime state。

## 需求

1. PR body 内容质量标准必须写入 canonical Guru Team workflow，并同步 dogfood active workflow。标准要说明 PR body 是给 GitHub reviewer 看，不是给 Trellis session 看。
2. `trellis-finish-work` / publish 前必须要求 AI 生成或审查 PR body readiness，检查摘要是否自解释、具体、可审阅，并覆盖影响范围、验证结果、Review Gate、Issue 关闭范围、安全与部署影响、附加说明 / 风险边界。
3. `publish-pr` 必须支持并优先使用 AI 审阅过的 body file 或 readiness artifact；脚本只做客观结构、必填 section、低信息量占位文本和 close/ref 语义校验，不替代 AI 判断内容是否真实充分。
4. non-draft publish 在缺少具体 `变更摘要`、`影响范围`、`验证结果`、`安全/部署影响` 时必须阻塞。低信息量默认摘要必须失败。
5. 自动 fallback body 不能再使用“当前 Trellis task”类摘要；若没有 body file，fallback 也必须从 Review Gate、validation、Issue Scope Ledger 生成更具体的结构，并通过同一结构校验。
6. README、workflow README、preset README 或相关 spec checklist 必须记录 PR body 质量标准与脚本/AI 边界。
7. 增加单元测试或 dry-run 覆盖：低信息量摘要失败，包含具体摘要和必填 section 的 body 成功，body file 优先于 fallback。

## 非目标

- 不修改已经存在的 GitHub PR 正文。
- 不要求所有 PR 使用完全相同 emoji 或章节标题；脚本只要求核心中文 section 和可审阅内容。
- 不让脚本判断“业务内容是否真实充分”；真实性仍由 AI PR readiness review 和 Branch Review Gate 判断，脚本只验证机器可判定的结构和禁用短语。
- 不把 active task、PR runtime state 或项目私有规则写入 spec template marketplace。

## Repo Docs SSOT

本仓库没有独立 `docs/` durable docs 目录；长期用户文档 SSOT 是 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` 与 `.trellis/spec/`。本任务会更新这些现有公开文档和规范，不新增 `docs/` 目录。

## Middle-platform Knowledge Gate

本任务只修改 Trellis workflow/preset/publish helper，不涉及 `go-guru`、`proto-guru`、ORM、Unity3D SDK 或 Flutter SDK 等 Guru Team 中台 SDK/framework。Middle-platform Knowledge Gate 不适用。

## 验收标准

- [ ] canonical workflow、dogfood workflow、finish-work 入口都明确 PR body 面向 GitHub reviewer，禁止低信息量 Trellis 内部语境摘要。
- [ ] `publish-pr` 支持 AI 审阅后的 body file / artifact，并优先使用该内容。
- [ ] `publish-pr` 对 non-draft PR body 校验必填 section、低信息量短语、具体 validation、影响范围、安全/部署影响。
- [ ] 单元测试覆盖低信息量摘要失败、合格 body 通过、body file 优先级。
- [ ] README / workflow README / preset README / `.trellis/spec` 的质量标准与实现一致。
- [ ] 如果修改 preset overlays，已运行 `apply.sh --repo .` 同步 dogfood 副本并通过 `check-dogfood-overlay-drift.sh`。
- [ ] 运行 workflow/preset 必要验证命令，记录未覆盖的 throwaway 安装或 upgrade/update 风险。
