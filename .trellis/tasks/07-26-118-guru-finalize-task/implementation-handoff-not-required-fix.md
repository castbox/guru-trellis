# Issue #118 `not_required` Producer Edge 修复交接

## 1. 结论

本轮已完成 `F-NOT-REQUIRED-EDGE-01` 的实现边界：#117 保留既有 workflow
`verification_not_required` API，同时把实际可达的 task-bearing standalone
`not_required` 输出投影为 `repo_ref`、`resolved_head`、`verification_ref`；#118 新增
`standalone_verification_not_required` profile，并只由 target authoring 提供 `profile`、
`mode`、`task_ref`。`plan_ref` 没有加入 producer DTO，same-plan 绑定只从 task-local #117
evidence、immutable private plan、repository 与 reviewed HEAD 重建。

Production eval 不再绕过 producer：它真实执行 #117 public wrapper，应用 interface 声明的
`project_not_required` projection，执行 no-overwrite authoring merge，再真实执行 #118
public wrapper。该 case 的 source/installed Shared 与 Codex native 结果均为
`actual_exit=published`。

未执行 commit、push、PR、archive、Issue mutation、deploy 或 production write。#119 继续
拥有 global Finish family activation/combined acceptance，#132 继续拥有 upstream overlay
cleanup。

## 2. Requirement 与 Design 承接

- 保留 #117 public `not_required` output 的 workflow/standalone schema compatibility；只把
  active consumer edge 指向实际可达的 standalone branch。
- 新 profile 的 producer seed 与 target authoring 精确分区，零 overlap、零 overwrite、
  零 runtime semantic authoring。
- Finalizer runtime 校验 task-local #117 owner evidence 的 task、repository、resolved HEAD、
  verification ref 与 private plan；通用 #117 checker 未放宽。
- Same-plan recovery 可复用同一 private binding，但 producer public DTO 不新增 plan identity。
- Eval adapter 保留 actual-exit schema selection 先于 `expected_exit` assertion；
  `expected_exit` 不进入 native request。
- Global workflow、upstream `trellis-finish-work` family、official `.trellis/scripts/task.py`
  与 preset overlays 保持无 diff。

## 3. 本轮实现文件

Canonical source：

- `trellis/skills/guru-team/packages/guru-finalize-task/interface.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md`
- `trellis/skills/guru-team/packages/guru-finalize-task/schemas/public-input.schema.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/schemas/public-standalone-verification-not-required-input.schema.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/schemas/task-finalization-gate.schema.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/examples/public-standalone-verification-not-required-input.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/examples/public-standalone-verification-not-required-authoring.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/evals/evals.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/evals/files/verification-not-required-input.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/evals/files/not-required-reentry-published-facts.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py`
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/interface.json`
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/references/contract.md`
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/examples/public-not-required-output.json`
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/tests/test_contract.py`
- `trellis/skills/guru-team/adapters/eval/native_adapter.py`
- `trellis/skills/guru-team/tests/test_skill_packages.py`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`

Distribution、installer 与 durable docs：

- `trellis/guru-team-extension.json`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- `README.md`
- `trellis/presets/guru-team/README.md`
- `trellis/workflows/guru-team/README.md`
- `.trellis/spec/docs/public-docs.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/workflow/index.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/workflow-contract.md`

Generated dogfood copies：

- `.trellis/guru-team/extension.json`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/guru-team/skills/adapters/eval/native_adapter.py`
- `.trellis/guru-team/skills/packages/guru-finalize-task/**` 对应上述 package delta
- `.trellis/guru-team/skills/packages/guru-verify-extension-installation/**` 对应上述 package delta
- `.agents/skills/guru-finalize-task/**` 与
  `.agents/skills/guru-verify-extension-installation/**` 对应 package delta
- `.codex/skills/`、`.claude/skills/`、`.cursor/skills/` 下同名两个 package 的对应 delta

## 4. Docs SSOT Plan

批准策略为 `ssot_first`。主要实现输入是 durable package/workflow/preset contracts，task
`prd.md`、`design.md`、`implement.md` 与 finding 提供本轮 delta。

Durable delta 已合并：finalizer 现为 seven input profiles/six exits；#117 reachable
standalone `not_required` producer edge、minimal seed、target-owned authoring、private plan
binding、real two-wrapper eval 与四平台 distribution 已写入 package contract、workflow
contract、preset/docs navigation 和 README。未把 recovery 算法复制到 README。

Task-history-only 内容为 finding 复现、50 个 `.bak` 的逐文件处置、命令 transcript、外部
Claude/marketplace failure 和本 handoff。Global Finish route 与 upstream overlay 的 durable
状态没有改变，仍明确交给 #119/#132。

当前 PR 限制：用户禁止 push，因此不能从远端 exact feature ref 安装当前 dirty branch；
throwaway 使用脚本支持的 public-marketplace bootstrap + local canonical workflow overlay
路径。该路径第一轮完成大部分 matrix 后在后续 `trellis init` 遇到 registry timeout，第二轮
在首个 registry fetch 遇到同一 timeout，完整 throwaway gate 未通过。

## 5. Preset Apply 与 Sidecar 处置

- 首次默认 apply 选择 `codex,cursor`，错误缩小平台集并产生 520 个 Claude managed
  removals、49 个 package `.bak` 及 1 个 runtime `.bak`。
- 逐一确认 50 个 `.bak` 都 byte-equal 于对应 tracked path 的当前 HEAD 旧版本，且不含用户
  唯一内容；随后精确删除这些可由 Git 恢复的 backups。
- 以 `apply.sh --repo . --all-platforms --json` 重跑成功，恢复 Shared/Codex/Claude/Cursor
  distribution；manifest 为 2659 managed files、0 removal、0 conflict、0 sidecar。
- 最终递归 inventory 为 `.new=0`、`.bak=0`；canonical、installed shared、Agents、Codex、
  Claude、Cursor 的两个 package byte-identical，runtime/adapter canonical 与 installed copy
  byte-identical。

## 6. 验证结果

- Finalizer package：5 passed。
- Verifier package：10 passed。
- Focused runtime：3 passed。
- Runtime full：604 passed、13 skipped。
- Skill package graph/full production eval：179 passed。
- Preset apply + ownership tests：54 passed。
- Source/installed skill validation：均 passed；13 active、0 planned、0 legacy；installed
  2659 managed files、0 removal/conflict/sidecar。
- Shared real-wrapper edge eval：source passed、installed passed，均
  `actual_exit=published`。
- Codex native edge eval：passed，`actual_exit=published`。
- Cursor native edge eval：按 adapter contract 返回稳定 `unsupported`，没有伪造 pass。
- Claude native edge eval：`execution_error`；CLI 返回 `401 Invalid API key`、0 tokens、无
  permission denial，属于外部认证阻塞。
- Clean throwaway：第一轮完成 initial install/reapply/update、source/installed validation、
  ownership/drift、两轮 installed closeout 与 package/wrapper smokes，后段 no-developer
  fixture 的 registry fetch timeout；完整重试在首个 fetch 同样 timeout。最终 rc=1，不能
  声称 full throwaway passed。
- Dogfood overlay drift、explicit no-diff boundaries、Python compile、JSON parse、
  `git diff --check` 均通过。
- Worktree 与 source checkout 的 `__pycache__/.pyc/.pyo` 已清理；最终复核命令不得重新
  生成 cache。

## 7. 交给 `trellis-check`

1. 复核 #117 stable public schema 与 active producer projection 的兼容关系，确认 workflow
   `verification_not_required` API 未被删除或重解释。
2. 复核 new profile 的 seed/authoring partition、no-overwrite merge 与 private plan binding，
   尤其确认 public DTO 不包含 `plan_ref`。
3. 复核 standalone #117 evidence 的 task/repo/head/ref/plan currentness 以及 same-plan resume；
   通用 checker 和非-`not_required` 路径不得被放宽。
4. 复核 production eval 的真实 #117 wrapper -> declared projection -> #118 wrapper chain，
   actual-exit schema ordering 与 adapter trace isolation。
5. 按 `ssot_first` 复核 durable docs reconciliation、README 导航边界和 #119/#132 no-write
   scope。
6. 把 Claude 401 与重复 registry timeout 作为真实未通过的外部验证记录，不得改写为 pass；
   在凭据/registry 恢复后补跑对应 native eval 与完整 throwaway verifier。
7. 运行完整 Phase 2 semantic check 并记录新的 owner gate；本实现角色没有运行
   `trellis-check`、没有写 `phase2-check.json`。

## 8. Remaining Risks

- Claude native behavior 尚未获得当前环境的成功 trace，阻塞条件是外部 API key。
- 当前分支未 push，且 registry 连续 timeout；exact feature-ref marketplace install 与完整
  throwaway terminal pass 尚缺 fresh evidence。
- Main-owned task metadata 与 Round 7/8 reports 是并行会话内容，本实现没有修改、恢复或
  重新解释它们；Phase 2 必须基于最终 working tree 重新建立 current evidence。
