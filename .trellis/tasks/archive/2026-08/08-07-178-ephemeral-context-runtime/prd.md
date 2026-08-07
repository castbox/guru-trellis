# #178 将 context discovery 与 owner checkpoints 收敛为短生命周期 runtime

## 1. Goal

在 #177 已合并的 reviewed-content identity / freshness 合同上，将 change-context discovery 与 owner-private evidence 从“长期 task artifact + 多轮 supersession 链”收敛为“AI 直接读取 live authority + 最小 public DTO + 仅为真实恢复 consumer 创建的短生命周期 private checkpoint”。正常 Intake、standalone 与 terminal 路径不得留下无直接 consumer 的 tracked 或 ignored runtime。

Live authority：<https://github.com/castbox/guru-trellis/issues/178>。

## 2. Confirmed Facts

- 前置 #177 已合并；本 task 基于 fresh `main` commit `596a6a9ca0819f0c7ebac6adb1e9ac20cce806b5` 创建。
- 当前 `guru-discover-change-context` 仍把完整 `guru-context-discovery-1.0` snapshot 声明为 `task_local_tracked`，任务内目标固定为 `context-discovery.json`。
- 当前 discovery public input 同时存在 `pre_task` 与 `task_local_reentry`；后者通过 `prior_snapshot_locator=context-discovery.json` 维持 replacement/supersession 链。
- 当前 `context_ready` output 与 `guru-clarify-requirements:initial_change_request` input 通过 `handoff_context_locator -> context_locator` 绑定 producer-private snapshot；Change Request Review 与 Workspace planning 仍继续携带或解析该 locator/完整 prerequisite artifact。
- pre-task recorder 已支持 stdout-only 返回，但 public wrapper 仍要求 repo-relative `--owner-result` 文件，因此正常 side-effect-free 路径尚未闭合。
- shared runtime 已有 `.trellis/.runtime/guru-team/owner-checkpoints/<task-key>/`、`ai_first_owner_checkpoint_path` 与 `ai_first_retire_owner_checkpoints`；Planning、Phase 2、Branch Review、Publication 和 Finalizer 已分别使用其中明确列出的短生命周期 checkpoint，但缺少对 discovery 与 terminal residue 的统一生命周期证明。
- workflow/preset/Skill 的 canonical source 位于 `trellis/**`；`.trellis/**`、`.agents/**`、`.codex/**` 及其它平台目录是安装副本，必须通过 preset overlay 同步，不能单独手改后宣称完成。

## 3. Requirements

### R1. Discovery normal path is ephemeral

- 新任务、pre-task workflow 与 standalone discovery 均不得生成 tracked `context-discovery.json`。
- pre-task/standalone 的完整 semantic evidence 只存在于当前 AI 会话、stdout 或调用期临时输入；不得要求在仓库内创建 owner-result 文件才能调用 public wrapper。
- `context-discovery.json` 从 current canonical package、manifest、installed assets、README、schema/example/eval/test 和 runtime reader/writer 中退役；历史 archive 保持只读，不做历史迁移或改写。

### R2. Minimal producer-to-consumer DTO

- `context_ready` 只向唯一 consumer `guru-clarify-requirements:initial_change_request` 传递其下一步必需的 route/target identity：exit、profile、mode、target locator 与 continuation id。
- 删除 `handoff_context_locator`、`context_locator` 及所有同义 artifact locator；Clarify、Change Request Review、Workspace 不得读取 discovery private snapshot 或要求理解 producer recorder 实现。
- Clarify 根据最小 DTO、当前 AI 已完成的 discovery cognition 与 fresh Git/GitHub/Trellis/docs/code/tests 重新读取完成自身 semantic gate；live facts 每次从 authority source 重读，不复制到长期 handoff。
- producer output 到 consumer input 的 projection 仍必须由 Interface 1.3 静态、确定性验证；每个 output 字段必须有唯一直接 consumer use。

### R3. True recovery only, lazy private checkpoint

- 正常 mapped exit 不创建 checkpoint，也不请求额外 handoff/确认。
- 仅当 active-task owner loop 确实需要跨调用 re-entry/recovery 时，才在 `.trellis/.runtime/guru-team/owner-checkpoints/<task-key>/` 惰性创建最小 checkpoint；pre-task/standalone 不以 repo runtime 代替 stdout-only 路径。
- 删除 `task_local_reentry`、prior snapshot replacement、`superseded_snapshot_sha256`、refresh-history supersession 及其 schema/fixture/eval/test/文档链。
- stale context 通过重读 live authority 并完整重跑当前 semantic owner 处理，不维护 snapshot 版本历史。

### R4. Consume-and-clean lifecycle

- public wrapper 成功完成 objective check、output projection 与 output schema validation 后，立即删除它拥有的 input/checkpoint/result/temporary projection；失败时只保留同一 owner 下一次修复确实需要的最小 checkpoint。
- 下游 consumer 只消费 DTO 与 live facts，不读取、不解释、不删除上游 private checkpoint。
- task completion、publication/finalization terminal exit 与 cleanup 验证必须证明无 superseded input/checkpoint/result 或空 owner-checkpoint directory 残留。
- 任何 artifact 均不得持久化用户授权、完整 scan/history、文件 size/mtime/hash bundle、reviewer/process metadata 或可由 Git/GitHub/Trellis 重读的完整 facts。

### R5. Canonical and installed closure

- 同步修改 canonical workflow、`guru-discover-change-context`、直接 consumers、shared runtime、schemas、examples、evals、tests、extension manifest、preset installer/README、workflow README 与 durable specs。
- 使用 preset installer 同步 dogfood 与全部受支持平台 discovery copies，处理并报告所有 `.new` / `.bak`，最终 dogfood drift 为零。
- 不修改 Trellis upstream 源码、全局 npm 包或 `node_modules`；workflow 判断继续由 Markdown/Skill 承担，脚本只执行 recorder/validator/executor 的确定性事实。

### R6. Current-contract-only boundary

- 本 Issue 的 breaking scope 是对 #178 明确列出的 current discovery/checkpoint contract 做 current-only 收敛；不得保留旧 reader、alias、migration wrapper、tombstone 或“为了兼容”继续发布旧 artifact/profile/field。
- 历史 archived task artifact 不进入 current runtime contract，也不作为需要迁移的输入。
- 不提前删除 `finish-summary-index.json` 或压缩完整 Finalizer transaction；这些属于后续 Issue。

## 4. Acceptance Criteria

- [ ] A1 / R1：fresh task、pre-task workflow 和 standalone invocation 均不创建 tracked `context-discovery.json`，并证明 repository side-effect-free。
- [ ] A2 / R2：`context_ready` 与 Clarify initial input 不含 artifact locator；Interface projection 静态通过，每个字段均有直接 consumer。
- [ ] A3 / R2：Clarify、Change Request Review、Workspace 正常路径不读取 discovery snapshot，且 mapped exit 自动进入 consumer，无额外确认。
- [ ] A4 / R3：current package/runtime 中不存在 `task_local_reentry`、prior snapshot replacement 或 superseded discovery 链；stale 路径从 live authority 重跑。
- [ ] A5 / R3：真实 active-task recovery 使用最小 ignored checkpoint 恢复；没有真实 recovery 时 checkpoint 不存在。
- [ ] A6 / R4：producer wrapper 成功消费后删除其 owner-private material；terminal runtime 无 superseded input/checkpoint/result 与空目录。
- [ ] A7 / R4：自动扫描证明 active output/private schema/runtime 不持久化授权过程、完整 scan/history、size/mtime/hash bundle 或 reviewer/process metadata。
- [ ] A8 / R5：canonical、dogfood、preset/overlay、extension manifest、schema/example/eval/test、README/spec 与支持平台副本一致。
- [ ] A9 / R5：source/installed package closure、dogfood drift、clean throwaway install、existing-project workflow preview/switch、Trellis update/reapply、零 `.new`/`.bak` 通过。
- [ ] A10 / R5：Codex、Claude、Cursor 与 manifest 声明的其余平台入口不保留旧 discovery contract。
- [ ] A11 / R6：历史 archive 未改写；`finish-summary-index.json` 与完整 Finalizer transaction 未被本 task 提前整改。
- [ ] A12：独立 current-HEAD semantic review 覆盖完整 `origin/main...HEAD` diff，且无未关闭 P0-P3 finding。

## 5. Docs SSOT Plan

Strategy: `ssot_first`。

- 先修订 `.trellis/spec/workflow/skill-package-contract.md` 的 Public Skill I/O / private checkpoint lifecycle，以及 `.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/workflow/companion-scripts.md` 中仍把 discovery snapshot 当长期合同的段落。
- 再同步 canonical Skill contracts、`trellis/workflows/guru-team/README.md` 与 `trellis/presets/guru-team/README.md`，只描述 current ephemeral contract。
- `.trellis/workflow.md` 与平台副本由 canonical workflow/preset/overlay 同步；不新增平行 durable design 文档。
- 本 task 的 `prd.md`、`design.md`、`implement.md` 只用于任务规划与执行追踪，不替代上述 durable SSOT。

## 6. Out of Scope

- 删除或压缩 `finish-summary-index.json`、完整 Finalizer transaction、其它后续整改 Issue 的 owner state。
- 迁移或重写 `.trellis/tasks/archive/**` 中的历史 context artifact。
- 会话全文/raw JSONL、本机绝对路径或业务私有数据进入公共 Skill package。
- 恶意 actor、对抗输入、故意伪造/篡改 artifact、锁、竞态压力、TOCTOU、fault injection、跨 OS crash consistency。
- commit、push、PR、merge、finalization 与 cleanup 副作用；这些仍需在对应 workflow 边界单独处理。

## 7. Open Questions

无。当前 live Issue、现有 Interface 1.3/private-state SSOT 与代码/测试已足以确定交付边界。
