# #120 架构证据

## 官方 Trellis 依据

- `https://docs.trytrellis.app/index.md`：Trellis 项目内 workflow、spec、tasks 和平台集成是扩展工作的本地边界。
- `https://docs.trytrellis.app/advanced/custom-workflow.md`：workflow marketplace 管理 `.trellis/workflow.md`，支持 `trellis init --workflow` 和 `trellis workflow --marketplace`。
- `https://docs.trytrellis.app/advanced/custom-skills.md`：skills 通过平台 skill roots 被发现，`SKILL.md` 是 skill 入口。
- `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`：spec marketplace 承载可复用工程约定，不承载 active task 或平台运行状态。

本任务结论：workflow marketplace 不承担 external skill package 安装；Guru Team preset 必须继续作为完整 extension configurator。

## 当前仓库证据

- `AGENTS.md:44-85` 已定义 Skill-first SSOT、closed-loop 顺序、typed exits、拆分判定、stable id 和 package state 边界。
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 当前把 companion assets 复制到 `.trellis/guru-team/`，并从 overlay root 选择 shared/Codex/Cursor/Claude 文件。
- 同一 installer 当前只在 installed extension manifest 记录 managed path 集合，没有公共 skill 的逐文件 previous hash 和 package/interface provenance。
- `.trellis/spec/preset/installer.md` 当前规定 overlay heuristic replacement、unknown edit `.new`、update/reapply 和 platform selection；公共 skill package 必须新增 exact managed hash 路径，不能复用 heuristic replacement。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 已覆盖 workflow preview/switch、`trellis update --force`、preset reapply 和最终 sidecar scan，适合扩展公共 skill discovery/installed validation。
- `docs/requirements/requirement-main.md` 与 `guru-team-trellis-flow.md` 已覆盖 workflow/preset/installer，但未定义公共 closed-loop skill package、registry/interface 或 typed exit machine evidence，因此 docs state 为 `partial_docs`。

## 历史决策

- #109 只把 Skill-first 原则写入根 `AGENTS.md`，明确把 canonical package/distribution 拆到 #120。
- #109 的 `commit-message-loop-analysis.md` 推荐后续实现 `guru-create-work-commit`，并明确它必须在 #120 之后由独立 issue 实现。
- `trellis mem` 检索到的既有 #120 规划讨论选择：canonical root `trellis/skills/guru-team/`、installed root `.trellis/guru-team/skills/`、production registry 仅 reserved `guru-create-work-commit`、active lifecycle 只用 fixture 证明。

这些历史内容只作为设计来源；最终合同以 live issue、当前仓库文件、官方文档和本任务经用户批准的规划为准。
