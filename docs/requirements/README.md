# Guru Team Trellis Extensions

本目录说明本仓库已经建设的 `guru-team` Trellis 扩展能力。

这些文档不是通用产品需求模板，也不绑定 Codex、Claude、Cursor 或任何单一 AI coding
harness。它们用于回答一个问题：Guru Team 已经在官方 Trellis 之上扩展了什么能力，
这些能力如何分类、哪些最关键、哪些是安装与维护支撑。

## 文档

| 文档 | 内容 |
| --- | --- |
| [requirement-main.md](./requirement-main.md) | 基于本 repo 全量 issue / PR 历史整理的已实现 Trellis 扩展总览。 |
| [guru-team-trellis-flow.md](./guru-team-trellis-flow.md) | 面向演示的 Guru Team Trellis 全流程图：从 Codex prompt hook 触发 pre-task intake 到 `trellis-finish-work` closeout，并用颜色区分官方 Trellis 原生机制、Guru Team 扩展、平台入口和 companion scripts。 |

## 历史扫描范围

本轮整理已扫描 `castbox/guru-trellis` 的 GitHub issue 和 PR 历史，包括 closed / merged
记录：

- Issues：15 个，全部 closed。
- PRs：15 个，其中 14 个 merged，1 个 closed 未合并。
- Comments / reviews：基本没有额外决策；issue #6 有 `closed by #9` 补充，PR review
  comments 为空。主要产品决策和验收信息来自 issue body 与 PR body。
- 后续维护补充：active issue #51 已沉淀为 `prepare-task` 命名质量门禁能力，合并后应随
  对应 PR 更新到历史索引。

## 扩展重要性分层

| 层级 | 类别 | 历史来源 | 说明 |
| --- | --- | --- | --- |
| P0 | Workflow 主合同与日常入口 | #1, #2, #57 | `guru-team` marketplace workflow 定义 Phase 0-3、auto-bootstrap 日常入口、业务项目中文文档默认规则、知识门禁和 docs SSOT。 |
| P0 | Intake / worktree / no_task 副作用边界 | #6, #15, #26, #51 | 创建 issue、worktree、branch、task 或当前 checkout 直改前必须有 AI/human handoff、用户授权和语义命名门禁。 |
| P0 | Planning / check / Branch Review Gate 证据链 | #5, #8, #20, #44, #62, #72 | planning、phase2 check、独立 review、review report digest、任意 finding 阻断、fresh 最终放行审查、sub-agent wait/termination 恢复链和 gate artifact 形成可审计链路；默认 sub-agent mode 下 implement、check、Branch Review 都必须有真实 sub-agent evidence。 |
| P0 | Finish / publish / PR readiness | #7, #17, #18, #27 | PR 发布只能在 finish-work 后发生，且必须有 AI 审查过的 reviewer-facing body 与 readiness evidence。 |
| P1 | Preset installer 与平台 overlay | #9, #11 | preset 安装 companion assets 与平台入口，支持 overlay 选择，并保持 canonical / dogfood 同步。 |
| P1 | 安装、升级、开箱验证 | #10, #27 | README 非交互安装、throwaway install、dry-run readiness 和 Codex 默认 sub-agent 让新项目可开箱使用。 |
| P2 | Docs / spec / knowledge 协同 | #1, #9, #10, #57 | task artifact、durable docs、`.trellis/spec/`、中台知识引用、业务项目中文语言规则和公开安装文档协同。 |

## Canonical Source

本仓库的扩展长期源头位于：

- `trellis/index.json`
- `trellis/workflows/guru-team/`
- `trellis/presets/guru-team/`
- `trellis/presets/guru-team/overlays/`
- `.trellis/spec/`
- `README.md`

`.trellis/workflow.md`、`.agents/skills/`、`.codex/prompts/`、`.codex/skills/`
等 dogfood 文件是本仓库安装后的运行副本；维护时应从 canonical source 同步，而不是把
dogfood 副本当成唯一来源。

## GitHub 历史索引

| 主题 | Issues | Merged PRs |
| --- | --- | --- |
| 中台知识门禁与 Docs SSOT | #1 | #4 |
| Trellis auto-bootstrap 日常入口 | #2 | #3 |
| AI review prompt 与 Branch Review Gate | #5, #20, #44 | #12, #22 |
| prepare-task 无副作用 planner 与命名质量门禁 | #6, #51 | #14；#51 对应 PR 待发布 |
| PR readiness 与 PR body 质量 | #7, #17 | #23, #24 |
| Planning / phase2 可审计证据 | #8 | #25 |
| Dogfood overlay 同步 | #9 | #13 |
| README 非交互安装与开箱验证 | #10 | 历史合并已体现在 README / validation 脚本中 |
| Preset 平台选择 | #11 | #30 |
| no_task 直接编辑审批 | #15 | #16 |
| publish 只能发生在 finish-work 后 | #18 | #19 |
| Worktree developer identity | #26 | #28 |
| finish-work dry-run readiness / Codex dispatch | #27 | #29 |

Closed but unmerged PR：

- PR #21：`#20` 的早期实现尝试，已关闭并由 PR #22 替代。
