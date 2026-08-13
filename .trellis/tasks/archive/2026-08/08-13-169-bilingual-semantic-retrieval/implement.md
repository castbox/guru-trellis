# 实施计划

## 顺序

1. 枚举现有 canonical spec、Guru Skill package、Trellis agent/bundled skill 与 installer ownership，建立 source -> installed -> platform projection 清单。
2. 新增版本化 semantic retrieval SSOT 和 spec index 入口，覆盖概念族、exact literal、最小查询、否定结论、AI/script 与 artifact 边界。
3. 修改 `guru-discover-change-context`、`guru-clarify-requirements`、`guru-check-task`、`guru-review-branch` canonical contracts，只引用 SSOT 并声明 owner-local gate 使用点。
4. 修改 `trellis-research`、`trellis-session-insight`、`trellis-implement`、`trellis-check` canonical agent/skill 来源，保持平台角色和写入边界。
5. 添加 semantic eval fixtures，覆盖双向语言、legacy alias/literal、错误否定、exact symbol/error 和现有 fail-closed 行为。
6. 更新 preset managed inventory、README 或安装验证中实际需要的分发声明；不在 workflow/platform launcher 复制合同。
7. 运行 preset apply 同步 dogfood，处理 `.new/.bak`，执行 overlay/managed-copy drift 校验。
8. 执行 targeted unit/schema/eval、完整 preset tests、clean throwaway marketplace/preset install、reapply、update/upgrade 与平台 discovery 验证。
9. 运行 `trellis-check` 和 `guru-check-task` 完整九维语义检查；修复 finding 后全量重跑当前 scope。

## 重点文件

- Canonical semantic retrieval spec 与其 index/managed inventory。
- `trellis/presets/guru-team/**` 下的 canonical Skill packages、agent/skill sources、installer 和验证脚本。
- Dogfood `.trellis/guru-team/**`、`.trellis/spec/**`、`.agents/**`、`.codex/**`、`.claude/**`、`.cursor/**` projection。
- 各 owner 的 `evals/evals.json` 与 semantic fixtures。

## 验证命令

具体命令以仓库当前脚本和测试入口为准，最低包含：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py --repo .
python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p 'test_*.py'
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

还需运行 owner package contract/eval 的既有测试入口、source/installed package 校验、platform discovery、update/upgrade/reapply 与 `.new/.bak` 检查。若完整命令需要远端 ref 或外部依赖，明确记录实际执行范围和未验证边界，不用静态检查替代 live evidence。

## 完成门槛

- PRD AC1-AC12 均有代码/测试或安装验证证据。
- source/installed/dogfood/platform projection 无漂移。
- 没有 `implementation-handoff.md`、tracked raw search report、新 public DTO/query digest/授权记录。
- `guru-check-task` 返回 `passed` 后才进入 commit 阶段。
