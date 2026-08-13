# #219 实施计划

## 1. 建立依赖与 runtime 合同

- 新增 canonical dependency manifest/requirements lock，固定 `jsonschema` 与完整传递依赖版本和 hash。
- 新增 runtime identity、bootstrap、probe 和 resolver；错误输出遵循稳定 JSON 合同。
- 将新增文件纳入 extension public inventory、installer managed inventory 和 source ownership 验证范围。

## 2. 集成 preset apply/reapply

- 在 target managed assets 激活前执行 runtime preflight/bootstrap。
- 实现相同 identity 幂等复用、新 identity 候选构建、验证后切换与失败保留旧 active runtime。
- 保持 runtime root gitignored，不写 global/user site-packages，不覆盖 provenance 未知目录。
- 更新 installer JSON 结果，暴露最小 runtime action/identity 状态供测试和运维，不写授权或机器绝对路径到 public manifest。

## 3. 统一公开入口

- 修改 shared `launch.sh`、`run-skill-command.sh` 与其余 Guru-owned Python shell 入口，使实际 command 都通过 resolver。
- 保留 installer bootstrap/ownership validator 的明确例外，避免安装前循环依赖。
- 运行 preset apply 同步 dogfood installed runtime 与平台 projection；处理所有受管 `.new`/`.bak`，不触碰无关文件。

## 4. 补齐测试

- 扩展 `trellis/skills/guru-team/runtime/tests/test_runtime.py`，覆盖 identity、resolver、能力与错误合同。
- 扩展 installer tests，覆盖 fresh/reuse/identity change/corrupt/network or pip failure/recovery/unknown provenance。
- 移除必需 `jsonschema` 的 optional skip，并验证 Draft 2020-12 真实行为。
- 新增聚焦 clean runtime install test/runner，只覆盖 #219 要求的单 repo、单公开 wrapper schema 路径。

## 5. 文档与同步

- 更新 preset README 的安装、runtime identity、reapply、故障排查与快速发布边界。
- 更新 canonical `companion-scripts.md`、`quality-guidelines.md`，并通过 apply 同步 dogfood spec。
- 不修改 workflow 语义、#217/#218 合同或 #222 累计发布步骤。

## 6. 验证命令

- runtime/package unit tests（具体测试文件按实现后的 inventory 执行）。
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- focused clean runtime install runner，明确证明 PATH Python 无 `jsonschema` 且真实公开 wrapper schema 路径成功。
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 的 targeted dogfood reapply。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- canonical/installed runtime 与 lock equality 检查。
- `find`/测试中的递归 `.new`/`.bak` 未知 sidecar 断言为零。
- `guru-check-task` 语义检查当前 task 完整 scope。

明确不运行：完整 12-capability `guru-verify-extension-installation`、完整 marketplace、official Trellis update、全平台 throwaway、业务仓库 upgrade smoke、tag/Release。

## 高风险文件与回滚点

- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：激活顺序和现有 manifest 兼容性。
- `trellis/skills/guru-team/runtime/launch.sh` 及 shared dispatcher：所有公开 Skill command 的共同入口。
- extension/installed manifest inventory：漏项会造成 canonical/installed drift 或 upgrade 回退。
- runtime active pointer：必须只在候选完整验证后切换；失败路径不得破坏旧 runtime。

## 实现前门禁

- live Issue scope 与 `issue-scope-ledger.json` 一致，只关闭 #219。
- `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan 完整且无开放问题。
- planning wording review 与 `guru-approve-task-plan` 通过后才将 task 切换到 `in_progress`。
- 实现与检查由 Trellis `trellis-implement` / `trellis-check` 子代理执行；主会话负责协调、spec、commit 和 finish。
