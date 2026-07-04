# Guru Team Trellis 已实现扩展总览

本文按重要性说明本仓库已经在官方 Trellis 之上建设的扩展。内容基于本 repo 全量
GitHub issue / PR 历史，包括已 closed issue、已 merged PR 和已 closed 未合并 PR。

重点不是重新写一份抽象流程，而是把历史迭代已经沉淀出的 Trellis 扩展能力分类，并说明
每类能力的职责边界、实现资产和历史来源。

## 1. P0：Workflow 主合同与日常入口

`guru-team` workflow 是本仓库最核心的扩展。它通过官方 Trellis workflow marketplace
机制安装到目标仓库，并把 Guru Team 的任务流程定义为 Markdown 合同，而不是依赖脚本
或 hook 分叉。

历史来源：

- Issue #1 / PR #4：中台知识门禁与 Repo Docs SSOT。
- Issue #2 / PR #3：对齐 Trellis auto-bootstrap start model。

Canonical 资产：

- `trellis/index.json`
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/README.md`
- 本仓库 dogfood 运行副本 `.trellis/workflow.md`

已实现能力：

| 能力 | 说明 |
| --- | --- |
| 固定 marketplace id | `trellis/index.json` 暴露 `guru-team` workflow，供 `trellis init --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis` 安装。 |
| Phase 0 intake | 文件变更类任务先进入 issue intake、duplicate search、base branch 选择和 worktree preflight；默认 planner 不写 task artifact。 |
| Phase 1 planning | Trellis task 创建后写中文 `prd.md` / `design.md` / `implement.md`，并要求规划审查证据后才能进入实现。 |
| Phase 2 execute/check | 实现后运行完整 `trellis-check`，检查需求、设计、代码、测试、spec、docs 和部署影响，不用少量命令通过替代完整检查。 |
| Phase 3 finish/publish | commit 后经过 Branch Review Gate，再由 `trellis-finish-work` archive task、记录 journal、提交 metadata 并发布非 draft PR。 |
| Auto-bootstrap 日常入口 | 用户日常直接描述任务、贴 issue URL 或说 issue number；`trellis-start` 是 fallback / explicit orientation，不是每个任务的必需入口。 |

边界：

- Workflow 行为写在 Markdown 合同中，不通过修改 Trellis 上游源码、全局 npm 包、
  `node_modules` 或 hook hack 实现分叉。
- `trellis-continue` 只推进到 Branch Review Gate，不 push、不创建 PR、不调用
  `finish-work`。
- `trellis-finish-work` 是正常 closeout 与 PR publish 的唯一用户入口。

## 2. P0：Intake / worktree / no_task 副作用边界

这类扩展解决的是“AI 何时可以造成副作用”。历史问题集中在 freeform 请求、duplicate
issue、worktree、branch、task 创建和当前 checkout 直改上。

历史来源：

- Issue #6 / PR #14：`prepare-task` 默认路径改为无副作用 planner。
- Issue #15 / PR #16：`no_task` 当前 checkout 直接修改必须显式审批。
- Issue #26 / PR #28：worktree 创建后继承或初始化 Trellis developer identity。

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Side-effect-free prepare | `prepare-task.sh --json` 默认只输出 stdout JSON，不创建 GitHub issue、worktree、branch、Trellis task，也不写 handoff。 |
| Duplicate / proposed issue review | freeform 请求先输出 proposed issue、duplicate candidates、base branch、branch name、workspace path 和后续命令，由 AI 展示给用户确认。 |
| Confirmed issue creation | 创建 GitHub issue 必须使用 `--create-issue-confirmed --issue-title ... --issue-body-file ...`，标题和正文来自 AI/human 已审阅内容。 |
| Worktree executor boundary | `--create-worktree` / `--create-task` 只在 handoff review 和用户确认后使用，并把 handoff 写入选定 workspace。 |
| Base freshness | executor 路径创建 worktree 前刷新 base branch，只允许安全 fast-forward，本地 base 分叉或 freshness 不明时 fail closed。 |
| Developer identity | 新 worktree 优先复制 source checkout 的 gitignored `.trellis/.developer`；缺失但有 `--assignee` 时初始化；两者都没有则阻塞并给恢复命令。 |
| no_task direct edit override | 当前 checkout 直改必须由用户明确批准跳过 issue、Trellis task、worktree 和 branch；批准不包含 commit、push、PR 或 issue close。 |

实现资产：

- `trellis/workflows/guru-team/scripts/bash/prepare-task.sh`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
- `trellis/workflows/guru-team/workflow.md`
- `.agents/skills/trellis-start/SKILL.md`
- `.codex/prompts/trellis-start.md`

## 3. P0：Planning / check / Branch Review Gate 证据链

这类扩展解决的是“通过 gate 必须留下什么证据，以及脚本不能冒充 reviewer”。

历史来源：

- Issue #5 / PR #12：Branch Review Gate 前必须先执行 AI review prompt。
- Issue #8 / PR #25：增加 planning approval 与 phase2 check 可审计证据。
- Issue #20 / PR #22：Branch Review Gate 每次必须产出 task-local `review.md`，并由
  `review-gate.json` 记录 digest。
- PR #21：`#20` 的早期 closed 未合并实现，由 PR #22 替代。

已实现能力：

| 能力 | Artifact / 脚本 | 说明 |
| --- | --- | --- |
| Planning start gate | `planning-approval.json`、`record-planning-approval.sh`、`check-planning-approval.sh` | 记录 planning artifact hash、reviewer、user confirmation、HEAD；`task.py start` 只是状态写入。 |
| Phase 2 check gate | `phase2-check.json`、`record-phase2-check.sh`、`check-phase2-check.sh` | 记录完整 `trellis-check` 覆盖范围、验证命令、findings、dirty state；命令通过只是 evidence 的一部分。 |
| AI review prompt | workflow / overlay 文案 | Branch Review Gate 前必须先审查 `origin/<base>...HEAD` 完整 diff。 |
| Review report 必填 | `review.md` | AI/human review 判断的主证据，必须 task-local。 |
| Review gate recorder | `review-branch.sh`、`check-review-gate.sh`、`review-gate.json` | 固化 review result、review report digest、base/head、evidence、findings；脚本不是 reviewer。 |
| Independent review source | `--review-source independent-agent` | 通过 gate 不能来自 `self-review` 或 `*-main-session`。 |
| Metadata tail 规则 | `finish-work.sh` / gate 校验 | review 后只允许 Trellis metadata tail；非 metadata 变更会使 evidence stale。 |

覆盖范围：

- docs、code、tests、Trellis artifacts
- preset overlay、companion scripts、schema、config
- CI/CD、container、Kubernetes/Kustomize/Helm、DB migration、Makefile
- Issue Scope Ledger、publish readiness、部署影响和安全风险

## 4. P0：Finish / publish / PR readiness

这类扩展解决的是“PR 何时发布、由谁判断 PR body 是否足够，以及 dry-run 是否真的无副作用”。

历史来源：

- Issue #18 / PR #19：PR publish 只能发生在 finish-work 之后。
- Issue #17 / PR #23：PR body 质量标准，禁止低信息量默认摘要。
- Issue #7 / PR #24：publish 前必须有 AI-reviewed body file 或 readiness artifact。
- Issue #27 / PR #29：`finish-work --dry-run` 成为真正无副作用 readiness preview，同时修正
  Codex 默认 dispatch 为 `sub-agent`。

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Publish after finish | 普通 `publish-pr` 直接调用被阻塞；正常发布只能由 `finish-work.sh --from-trellis-finish-work` 在 archive / journal / metadata commit 后内部触发。 |
| Recovery/debug 明确化 | 直接 publish 只保留显式 recovery/debug 路径，并必须通过 review gate、dirty state、issue ledger、base branch 和 GitHub auth 校验。 |
| Non-draft body source | non-draft publish 必须传入 AI 审查后的 `--body-file` 或 `--body-artifact`；generated body 只可用于 draft/preview。 |
| PR body 质量门禁 | 变更摘要、影响范围、验证结果、Review Gate、Issue 关闭范围、安全说明必须具体，禁止“当前 Trellis task”“详见 artifact”等低信息量短语作为主要摘要。 |
| Issue close 语义 | `Closes #xx` 只能来自 task-level `issue-scope-ledger.json` 的 `close_issues`，`related_issues` / `followup_issues` 不得被关闭。 |
| Archive path rewrite | finish-work archive 后，active task 下的 body/readiness path 会重写到 archived task artifact path 再读取。 |
| Dry-run readiness preview | `finish-work --dry-run --from-trellis-finish-work` 只校验 readiness 并输出 archive / journal / publish plan，不移动 task、不写 journal、不 commit、不 push、不创建 PR。 |
| Codex default dispatch | 缺省或非法 `codex.dispatch_mode` 回落到 `sub-agent`，显式 `inline` 保留为调试/降级模式。 |

实现资产：

- `trellis/workflows/guru-team/scripts/bash/finish-work.sh`
- `trellis/workflows/guru-team/scripts/bash/publish-pr.sh`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/presets/guru-team/overlays/**/trellis-finish-work*`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/companion-scripts.md`

## 5. P1：Preset installer 与平台 overlay

Preset installer 把 workflow 之外的 Guru Team companion assets 和平台入口安装到目标仓库。
它不运行 `trellis init`，不修改官方 Trellis 生成脚本，也不改上游源码。

历史来源：

- Issue #9 / PR #13：保持 dogfood installed overlays 与 canonical preset overlays 同步。
- Issue #11 / PR #30：preset installer 只安装所选平台 overlay。
- Issue #31：Guru Team extension version manifest 与 installed provenance。

Canonical 资产：

- `trellis/presets/guru-team/scripts/bash/apply.sh`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/README.md`
- `trellis/presets/guru-team/overlays/`

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Managed assets 安装 | 安装 `.trellis/guru-team/config.yml`、schema、bash scripts、Python helper。 |
| 幂等更新 | 同内容跳过；Guru-managed 文件升级 active 文件并保留 `.bak`；未知本地改动写 `.new`。 |
| 配置保护 | 已有 `.trellis/guru-team/config.yml` 不为补 key 被覆盖；`middle_platform_knowledge.mode` 缺失时按 `optional_warn`。 |
| Codex dispatch 默认 | 物化 `.trellis/config.yaml` 的 `codex.dispatch_mode: sub-agent` 默认，显式 `inline` 保留。 |
| 平台可选安装 | 默认安装 shared + Codex + Cursor；支持重复 `--platform codex|cursor|claude`；支持 `--all-platforms`。 |
| 未选择平台不恢复 | 默认 Codex + Cursor 安装不创建 `.claude/`；重复 apply 不会恢复未选择平台目录。 |
| Extension version/provenance | `trellis/guru-team-extension.json` 是 Guru Team extension canonical version；installer 写入 `.trellis/guru-team/extension.json` 记录安装版本、source ref/commit、source tree state 和 selected platforms。 |
| Dogfood drift check | canonical overlay 与本仓库安装副本可通过 `check-dogfood-overlay-drift.sh` 比对。 |

平台 overlay 当前覆盖：

| 平台/层 | 文件 |
| --- | --- |
| Shared skills | `.agents/skills/trellis-start`、`trellis-continue`、`trellis-finish-work` |
| Codex | `.codex/prompts/*` 与 `.codex/skills/*` |
| Cursor | `.cursor/commands/trellis-continue.md`、`.cursor/commands/trellis-finish-work.md` |
| Claude | `.claude/commands/trellis/continue.md`、`.claude/commands/trellis/finish-work.md` |

## 6. P1：安装、升级与开箱验证

这类扩展证明 `guru-team` 不是 dogfood 仓库里的局部 patch，而是可以安装、升级、抽样验证的
团队扩展。

历史来源：

- Issue #10：README 安装命令必须非交互且可开箱验证。
- Issue #9 / PR #13：dogfood overlay 同步。
- Issue #11 / PR #30：平台选择安装验证。
- Issue #27 / PR #29：finish-work dry-run readiness 和 Codex default dispatch 让新装项目不在 closeout 阶段卡死。
- Issue #31：安装/升级后用户和 AI 可直接查看 Guru Team extension version 与来源 provenance。

已实现验证能力：

| 能力 | 入口 | 说明 |
| --- | --- | --- |
| Non-interactive install | `README.md` | 默认命令使用 `trellis init -y ... --workflow guru-team --workflow-source ...`，不进入交互式 spec template picker。 |
| AI install / upgrade prompt | `README.md` | 提供可复制到目标业务仓库 AI session 的安装、升级、spec bootstrap prompt。 |
| Throwaway install | `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` | 创建临时 Git repo，运行非交互 `trellis init`、应用 preset、检查 workflow、脚本、平台选择和 `check-env --json`。 |
| Extension version check | `.trellis/guru-team/scripts/bash/version.sh --json` | 读取 installed manifest，输出 Guru Team extension version、workflow template id、source ref/commit、source tree state 和 selected platforms。 |
| Existing workflow preview/switch | `trellis workflow --marketplace ... --template guru-team --create-new` / 无 `--create-new` | 验证已有项目可以预览并切换 active workflow。 |
| Dogfood overlay drift | `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` | 比对 canonical overlay 与本仓库安装副本，防止 dogfood 文件漂移。 |
| Installer unit tests | `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` | 覆盖平台选择、Codex dispatch 默认、unknown platform fail closed 等 installer 行为。 |
| Workflow helper tests | `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` | 覆盖 intake side-effect boundary、planning/phase2 gate、review/publish/finish 边界等行为。 |

维护规则：

- README 命令必须真实可执行，不依赖本机隐藏状态。
- 修改 `trellis/presets/guru-team/overlays/` 后，要重新 apply 到本仓库并运行 dogfood drift
  check。
- 修改 workflow/preset/overlay/脚本后，需要说明 throwaway install 或 upgrade/update
  验证覆盖了什么，未覆盖什么。

## 7. P2：Docs、spec 与 knowledge 协同

这类扩展不直接创建 task 或发布 PR，但决定长期维护质量。

历史来源：

- Issue #1 / PR #4：Middle-platform Knowledge Gate 与 Repo Docs SSOT。
- Issue #10：README install / upgrade prompt 需要包含 spec bootstrap 边界。
- Issue #9：overlay 与 dogfood 副本同步属于公共 docs / spec 可维护性问题。

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Middle-platform Knowledge Gate | 当任务涉及 Guru Team 中台 SDK / framework 时，AI 检查当前平台是否可用 `guru-knowledge-center` MCP，并将 citation 写入 task artifact。 |
| Configurable knowledge mode | `middle_platform_knowledge.mode` 支持 `off`、`optional_warn`、`required`；缺失时按 `optional_warn`。 |
| Repo Docs SSOT reconciliation | Planning 阶段识别 durable docs；finish 前记录哪些 docs 更新、哪些 task 内容合并回长期文档、哪些只保留为 task history。 |
| Spec bootstrap 边界 | 安装后发现 `00-bootstrap-guidelines` 时只报告并询问，不把 spec bootstrap 作为安装副作用静默完成。 |
| Spec update 判断 | 每个任务 closeout 前判断是否需要更新 `.trellis/spec/`，但不把 active task 或私有业务 PRD 放入公共 template / marketplace。 |
| Public docs 规范 | `.trellis/spec/docs/public-docs.md` 约束 README 安装/升级 prompt、Git 发布预检、安全和 SSOT 一致性。 |

## 8. 历史覆盖矩阵

| Issue | 状态 | 对应 PR | 已沉淀扩展 |
| --- | --- | --- | --- |
| #1 | closed | #4 merged | Middle-platform Knowledge Gate；Repo Docs SSOT reconciliation。 |
| #2 | closed | #3 merged | Auto-bootstrap 日常入口；`trellis-start` fallback 定位。 |
| #5 | closed | #12 merged | Branch Review Gate 前先执行 AI review prompt；脚本只是 recorder / validator。 |
| #6 | closed | #14 merged | `prepare-task` 默认无副作用 planner；confirmed issue creation。 |
| #7 | closed | #24 merged | publish 前必须有 AI-reviewed PR body / readiness artifact。 |
| #8 | closed | #25 merged | `planning-approval.json` 与 `phase2-check.json` 可审计 gate。 |
| #9 | closed | #13 merged | canonical overlay 与 dogfood installed copy 同步；drift check。 |
| #10 | closed | 已体现在 README / verification | 非交互安装命令、AI install/upgrade prompt、开箱验证要求。 |
| #11 | closed | #30 merged | preset installer 支持 platform overlay selection。 |
| #15 | closed | #16 merged | `no_task` 当前 checkout 直改必须显式审批。 |
| #17 | closed | #23 merged | PR body 自解释质量标准与低信息量摘要阻塞。 |
| #18 | closed | #19 merged | PR publish 只能发生在 finish-work 后。 |
| #20 | closed | #22 merged | Branch Review Gate 每次必须产出 `review.md` 并记录 digest；#21 为 closed 未合并尝试。 |
| #26 | closed | #28 merged | worktree 创建后继承或初始化 Trellis developer identity。 |
| #27 | closed | #29 merged | `finish-work --dry-run` 真正无副作用；Codex 默认 `sub-agent` dispatch。 |
| #31 | open | 当前任务 | Guru Team extension canonical manifest、installed provenance、`check-env` / `version.sh` 可观测入口。 |

## 9. 当前扩展边界

已经实现的边界：

- 本仓库维护 `guru-team` 可复用 workflow 与 preset，不 fork 官方 Trellis。
- 脚本可以执行事实动作、校验 JSON/hash/HEAD/diff/dirty state，但不替代 AI 判断。
- Platform overlay 是 harness 适配层，不是新的 workflow source。
- Task artifact 是任务证据，不是 durable docs 的替代品。
- PR publish 必须经过 finish-work 与 review/readiness evidence，不能由普通 `publish-pr` 直接触发。

尚未在本目录展开的内容：

- 每个 companion script 的完整 CLI 参数合同。
- 每个 platform overlay 的逐文件行为差异。
- Throwaway install 在不同 Trellis CLI 版本上的兼容性矩阵。
- 完整 upgrade/update 漂移测试记录。
