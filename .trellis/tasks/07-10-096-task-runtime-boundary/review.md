# Issue #96 Branch Review 最终汇总

## 审查轮次

| 轮次 | Reviewed HEAD | 角色 | Findings | 结论 |
| --- | --- | --- | --- | --- |
| Round 1 | `a84e5720d0ea18482b46b165062930e50cf54b34` | 问题发现审查 | P1 × 4 | 阻塞 |
| Round 2 | `90a2d45c823775ff0eaa485ef10640d8b4aa96f5` | 问题闭环审查 | P1 × 1、P2 × 1 | 阻塞 |
| Round 3 | `f05cd662e852984f7f07cf6336d0867eb6532302` | 问题闭环审查 | 0 | 建议进入最终放行审查 |
| Round 4 | `f05cd662e852984f7f07cf6336d0867eb6532302` | 最终放行审查 | P1 × 1 | 不放行 |

最终审查覆盖 `origin/main...HEAD` 完整三提交与 64 文件累计 diff，并独立读取 Issue #96、planning/Phase 2/ledger/assignment、Round 1/2/3 raw reports、spec/research/durable docs、canonical/dogfood/overlays、代码与测试；未仅依赖 Round 3。

## 问题生命周期

- Round 1 SHA producer→task-start-context 映射 P1：已由 `local_head_after` / `remote_head` 正确映射及 fresh/remote-only/fetch-failed 回归测试闭环。
- Round 1 clean clone obsolete fixture P1：已由固定 fixture 文件及 clean clone 30 项 preset tests 闭环。
- Round 1 push 后 marketplace verifier P1：执行链已闭环；publish 在 `gh pr create` 前强制远端 init/preview/switch/preset reapply、artifact、ledger、双文件 metadata tail 和 remote HEAD 交叉校验。
- Round 1 ledger evidence / Round 2 AC9 P1：代码合同已闭环；当前真实 evidence 仍为 required/pending，不能满足最终 publish，也不会被伪造为 passed。
- Round 2 failed verifier artifact schema P2：已由 runtime/schema contract 与 early/partial/passed 回归测试闭环。
- Round 4 新 P1：active start/continue 平台入口、README、requirements 与 workflow specs 仍把已删除的 handoff `workspace_path` 或不存在的 `task-start-context.workspace_path` 当现行 workspace boundary 合同，尚未闭环。

## 最终审查

### P1：旧 intake handoff workspace 合同仍存在于 active SSOT

Issue #96 要求代码、schema、workflow、skill、prompt、config 和 public API 完整删除原 Guru Team handoff 概念；任务启动上下文 schema 不包含 `workspace_path`，validator 也禁止该字段。但以下现行入口仍要求 agent 读取或使用 handoff `workspace_path`：

- `.agents/skills/trellis-start/SKILL.md:34`
- `.codex/skills/trellis-start/SKILL.md:34`
- `.agents/skills/trellis-continue/SKILL.md:19`
- `.agents/skills/trellis-continue/SKILL.md:56`
- `.codex/prompts/trellis-continue.md:13`
- `.codex/prompts/trellis-continue.md:50`
- `.codex/skills/trellis-continue/SKILL.md:19`
- `.codex/skills/trellis-continue/SKILL.md:56`
- `.cursor/commands/trellis-continue.md:13`
- `.cursor/commands/trellis-continue.md:50`
- `README.md:295`
- `README.md:296`
- `README.md:307`
- `docs/requirements/README.md:35`
- `.trellis/spec/workflow/companion-scripts.md:69`
- `.trellis/spec/workflow/companion-scripts.md:179`
- `.trellis/spec/workflow/workflow-contract.md:28`

该冲突会使新安装或 dogfood agent 查找一个不存在且被 schema 禁止的字段，并在无法显式设置 `workdir` 时失去合法 task worktree absolute path 来源。当前 239+30 tests 和 dogfood drift 未覆盖此 active-reference contract，因此这是当前范围 Docs SSOT / 平台行为一致性阻塞项。

## 证据

- Reviewed HEAD：`f05cd662e852984f7f07cf6336d0867eb6532302`。
- Diff：`origin/main...HEAD`，3 commits，64 files。
- Clean clone core tests：239 tests，通过。
- Clean clone preset tests：30 tests，通过。
- Python compile、shell syntax、task validation、JSON/JSONL parse：通过。
- Commit messages：3 commits，通过。
- Dogfood overlay drift、canonical/dogfood helper/schema/workflow equality、`.new/.bak` 扫描、`git diff --check`：通过。
- Task-start/runtime/workspace/parallel/obsolete/verifier/ledger/exact two-file tail 定向测试：通过。
- 真实 GitHub remote branch：当前不存在；`marketplace-verification.json` 缺失，primary/close ledger 均为 `required=true,status=pending`。
- Publish fail-closed：代码在 verifier passed、ledger passed、artifact + ledger 精确双文件 tail push、远端 HEAD 与 gate 复核前不会执行 `gh pr create`。
- Issue scope：仅 #96 为 close；#53 为 related；#97/#98/#99/#100 为 followup。
- 安全/部署：未发现 secret 或敏感数据；无业务部署、数据库、容器、Kubernetes、CI/CD、Makefile 影响。

## 观察项

- Round 4 开始时 `agent-assignment.json` 尚未记录本轮 assignment/review round；应由主会话 recorder 在消费 raw report 时补充，不由 reviewer 修改。
- “implementation handoff”“agent handoff”“handoff_summary”属于 agent 交接语义，不在本 P1 范围；需删除的是仍作为 Guru Team intake/workspace 公共 API 的 handoff 引用。
- 真实远端 marketplace 验证仍 pending；这是预期 fail-closed 状态，不是 passed 证据。

## 后续候选

- 修复 active start/continue overlays、README、requirements、workflow specs，统一使用 current checkout、repo-relative `task_artifact_dir`、`git worktree list` 和 `.trellis/.runtime/guru-team/**` 重算 workspace boundary。
- 运行 preset `apply.sh --repo . --all-platforms` 同步 dogfood，并复核无 `.new` / `.bak`、dogfood drift 为零。
- 增加 active-reference regression test，禁止现行 workspace/intake contract 再引用旧 handoff 或不存在的 task-start-context `workspace_path`。
- 新 HEAD 形成后重新执行 clean clone 239+30、完整 diff 独立审查；正式 publish 时再生成真实 remote marketplace passed artifact 与 ledger evidence。

## 结论

- 最终 findings：P0 0、P1 1、P2 0、P3 0。
- 历史 findings 已闭环，但最终 HEAD 仍有 1 个当前范围 P1。
- **不建议通过 Branch Review Gate，不予最终放行。**
