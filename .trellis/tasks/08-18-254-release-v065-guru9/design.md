# #254 v0.6.5-guru.9 发布设计

## 身份与 candidate

起点是 fresh `origin/main@f50975191b99caaee973c222974f4993dd466a18`，稳定 tag 为 `v0.6.5-guru.9`，目标 tag 为 `v0.6.5-guru.9`。preparation branch 不是 candidate；只有 preparation PR 合并后重新读取并三方核对的 clean `origin/main` commit/tree 才是 candidate。任何 candidate bytes 或 release-owned metadata 变化都会使绑定 evidence stale。

## Source of truth 与投影

canonical owners 是 `trellis/` 下 workflow、preset、extension manifest、README、verifier fixtures/tests 与 overlay；dogfood `.trellis/`、`.agents/`、`.codex/`、`.claude/`、`.cursor/` 是由 preset 生成的 projections。根目录 `CLAUDE.md` 是仓库级 Claude 规则入口，直接复制 `AGENTS.md` bytes，不建立第二套规则。canonical 修改后运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`，再检查 source/installed/platform equality、ownership、mode、registry/workflow graph 和 overlay drift。

## Claude 支持模型

Claude 的 discovery surface 包括 `.claude/commands/`、`.claude/skills/`、`.claude/agents/`、`.claude/hooks/` 与 settings 注册；canonical 对应位于 `trellis/presets/guru-team/overlays/.claude/`。验证目标是当前入口与 Shared/Codex/Cursor 语义一致，且 clean install、official update、preset reapply 不丢失 Claude managed files。不得通过修改 Trellis upstream 或 hook/script 替代 Markdown workflow/skill 合同。

## 验证分层

Phase 2 仅证明 preparation branch；PR merge 后重新冻结 candidate，再执行完整 throwaway initial install、existing-repo workflow preview/switch、official update、preset reapply、linked worktree/closeout、双 PATH managed interpreter identity、deterministic/no-model/fake-production、sandbox/schema/route 和独立 review。staged roots 在 preflight/postflight 均扫描 `__pycache__/`、`*.pyc`、`*.pyo`，必须为零；source ignored bytecode 不参与 identity。

模型证据固定披露：本发布未取得 live GPT-5.6 Sol production semantic evidence；deterministic/no-model 结果不能证明压力矩阵或未来模型稳定性。

## Docs SSOT Plan

- `ssot_first`：版本、tag、revision、CLI baseline 的 durable owner 是 extension manifest 与 canonical public README；workflow/preset README 承接安装、preview/switch、update/reapply 合同。
- Claude 支持的 durable owner 是 canonical `.claude` overlay 与根目录 `CLAUDE.md`；dogfood/platform files 只由 preset projection 生成。
- verifier fixtures/tests、inventory、ownership 和 drift 输出只记录直接 consumer 所需的 candidate identity 与结论，不保存授权过程、secret、完整临时日志或机器绝对路径 bundle。
- task-local `release-notes-zh.md`、candidate freeze、验证摘要和 PR body 作为本任务历史；不扩写 #239 的 canonical bytecode/multi-workflow SSOT。

## 状态机与恢复

Planning approved -> implementation/check -> confirmed task commit -> fresh-final Branch Review -> PR readiness -> separately confirmed push/PR/merge -> fresh candidate freeze -> pre-tag gate -> separately confirmed annotated tag -> separately confirmed tag-pinned smoke -> separately confirmed Release -> separately confirmed Issue closure。任一 stale/mismatch、required gate failure、unknown typed exit、SKIP 或 live authority 缺失都 fail closed；tag 创建后 smoke 失败时不移动或删除 immutable tag。
