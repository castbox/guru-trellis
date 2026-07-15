# #111 `guru-discover-change-context` 实现计划

## 1. 实现前门禁

- [ ] 主会话展示 `prd.md`、`design.md`、`implement.md` 链接并取得用户在阅读后的明确实现确认。
- [ ] 主会话记录 schema 1.2 `planning-approval.json`；`ambiguity_review.status` 必须为 `passed`，`unchecked_normative_hits` 必须为空。
- [ ] `check-workspace-boundary.sh` 与 `check-planning-approval.sh` 必须通过。
- [ ] 运行 `task.py start` 后再派发 `trellis-implement` sub-agent；主会话不得直接实现。
- [ ] 实现代理运行 `trellis-before-dev`，加载 workflow、docs、preset specs、task context 与本计划。
- [ ] 中台知识门禁按 `not_applicable` 执行，不查询 `guru-knowledge-center`。

## 2. Durable Docs SSOT checkpoint

执行 `design.md` 第 11 节的 `ssot_first` 策略：

- [ ] 更新 `docs/requirements/README.md`、`requirement-main.md` 与 `guru-team-trellis-flow.md`，把 inline route 替换为 active Skill contract。
- [ ] 更新 `.trellis/spec/workflow/index.md`、`workflow-contract.md`、`skill-package-contract.md`、`data-contracts.md`、`companion-scripts.md` 与 `quality-guidelines.md`。
- [ ] 更新 `.trellis/spec/preset/installer.md`、`overlay-guidelines.md`、`upstream-ownership.md` 与 `.trellis/spec/docs/public-docs.md`。
- [ ] 更新 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- [ ] Durable docs 必须明确 fixed order、mode parity、freshness、score v1、manifest/preview digest、invalid isolation、deep-read/mem gate、same-snapshot persistence、typed exits 与 no-workspace/no-cache 边界。
- [ ] 在 schema/runtime/package 改动前复核 durable docs 互相一致；该复核是代码阶段入口 checkpoint。
- [ ] 不修改 transitional legacy overlay payload；只在 durable ownership 文档中说明新 `guru-*` package 命中既有 `guru_owned` anchored rule。

## 3. Canonical package 与 interface

- [ ] 在 registry 激活 `guru-discover-change-context`，声明 workflow route、validator command 与 shared/Codex/Cursor/Claude platform destinations。
- [ ] 创建短 `SKILL.md`，只保留 trigger、routing、execution entry 与 fail-closed 规则。
- [ ] 创建 `references/contract.md`，完整承接 design 的 modes、五阶段、固定顺序、Gate、history、artifact、refresh 与 exits。
- [ ] 创建 interface schema 1.2 instance，声明 `judgment_mode=semantic`、两种 mode 一致 preconditions、runtime dependency、artifact/schema/validators、三个 exits 与 re-entry。
- [ ] 创建 `guru-context-discovery-1.0` Draft 2020-12 schema与去身份化 example。
- [ ] 创建三个 thin package wrappers，只经 `run-skill-command` 调用 declared runtime commands。
- [ ] 增加 package contract tests，证明 package 非 self-contained 且 discovery copies 与 canonical identity 一致。

## 4. Current-state forward behavior

- [ ] 在 workflow/package contract 固定 fresh base -> live change -> duplicate -> Docs -> code/contracts -> tests -> query clues 的调用顺序。
- [ ] 复用现有 GitHub auth/repo facts与 duplicate search 基础函数；拆出 deterministic fact adapter，禁止脚本作 reuse/new target 决策。
- [ ] 实现 live issue facts digest 与 proposed draft digest；proposed draft 路径保持 GitHub/repo 零写入。
- [ ] 定义 AI current review rows：portable path、blob/content digest、purpose、observation、query clues。
- [ ] 确保 current Docs/code/tests review 完成前 history preview command不可调用。
- [ ] 确保 Skill 内 human confirmation 状态固定为 `not_required`，duplicate 终局决策留给 clarification route。

## 5. History engine 与 AI evidence

- [ ] 实现 canonical query、NFKC/casefold、exact path identity、独立 `terms`/`queries`、tokenization、canonical JSON 与 `query_sha256`。
- [ ] 实现 `guru-context-history-score-1.0` 的 issue/PR/branch/path/term/query exact 权重、token cap、tie sort、positive-score filter 与 limit 20。
- [ ] 只枚举 archived `finish-summary.json`，只投影 `index.*`；拒绝 workspace/runtime/cache/`finish-summary-index.json`。
- [ ] 实现 component `lstat`、containment、regular-file、JSON/index shape checks 与 stable error codes。
- [ ] 实现 valid/invalid manifest rows、`archive_manifest_sha256`、candidate projection 与 `preview_sha256`。
- [ ] 保证 mixed invalid/valid 隔离，invalid rows 不泄露 raw content 或本机绝对路径。
- [ ] 实现 candidate selection schema：有候选时 1 至 3 个、逐项 excluded reason、portable deep-read refs；零候选时成功空 selection。
- [ ] 实现 mem gate schema 与 validator；四类主证据 insufficiency 未全部满足时拒绝 `mem_review.status=used`。
- [ ] 实现 AI Review Gate schema checks；script 只校验 AI 已写结论，不生成 semantic pass。

## 6. Recorder、validator 与 refresh

- [ ] 新增 canonical runtime commands 与 Bash wrappers：`preview-change-context-history`、`record-context-discovery`、`check-context-discovery`。
- [ ] Pre-task recorder 只从 stdin 读取并输出 canonical result + snapshot digest；执行前后证明 repo zero-write。
- [ ] Pre-task validator 复核 schema、payload/snapshot digest、clean fresh Git、live issue/draft digest、reviewed blob identity、query digest 与 archive manifest digest。
- [ ] Task-local recorder 必须要求 `--task` 与 `--expected-snapshot-sha256`，并只写 `{TASK_DIR}/context-discovery.json`。
- [ ] Post-task recorder 必须复核 HEAD 未变且 tracked dirty paths 只位于新 task 目录；proposed draft 已创建 issue 时验证 reviewed draft/body digest 一致但不改写 snapshot。
- [ ] 写入目标已存在且 bytes 不一致时失败；不得生成 `.new`、`.bak` 或覆盖未知内容。
- [ ] 实现 stale reason 与 superseded query/snapshot digest record；任何 freshness drift 返回 `refresh_base` 并要求整步 re-entry。
- [ ] 实现 stable `blocked` error codes，不输出 secret、private raw text 或本机绝对路径。

## 7. Workflow、preset 与 dogfood

- [ ] Canonical workflow 在 `guru-sync-base:synced` 后添加一次 mandatory invoke marker。
- [ ] 添加 `context_ready -> guru-clarify-requirements`、`refresh_base -> guru-sync-base`、`blocked -> change-context-blocked` 唯一 exit markers。
- [ ] 删除 inline route 的 step-local 重复正文，只保留 global transition 和现有 clarification/intake consumer route。
- [ ] 更新 `trellis/guru-team-extension.json` 的 patch version、active ids、artifact schema ids、artifact contracts、companion commands 与 managed paths。
- [ ] 扩展 preset installer 的 canonical/installed/platform inventory、executable assertions 与 runtime command manifest。
- [ ] 运行 canonical preset apply 同步 `.trellis/workflow.md`、`.trellis/guru-team/**` 与 selected `guru-*` platform copies。
- [ ] 检查 legacy overlays 保持 baseline bytes；发现 drift 必须回滚该 drift。
- [ ] 逐个处理 `.new`/`.bak`，最终 sidecar 集合必须为空。

## 8. 自动化测试

- [ ] 在 `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 增加 query/score/manifest/preview/record/check/refresh 单元与集成矩阵。
- [ ] 在 `trellis/skills/guru-team/tests/test_skill_packages.py` 增加 active package、semantic profile、mode parity、runtime command、schema、marker/exit 与 platform copy tests。
- [ ] 在 package `tests/test_contract.py` 增加 wrapper、interface、example、schema 与 fail-closed contract tests。
- [ ] 在 preset tests 增加 selected platforms、managed hash upgrade/conflict、executable mode、manifest inventory 与 legacy no-drift tests。
- [ ] 扩展 `verify-throwaway-install.sh`，覆盖 direct discovery、workflow route、candidate/zero-candidate preview、same-snapshot task record、update/reapply 与 zero sidecar。
- [ ] 运行 upstream ownership fixtures，确认无 new legacy path、baseline rewrite 或 unclassified asset。

## 9. Phase 2 验证命令

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json \
  --task .trellis/tasks/07-15-111-guru-discover-change-context

python3 -m unittest \
  trellis/skills/guru-team/packages/guru-discover-change-context/tests/test_contract.py \
  trellis/skills/guru-team/tests/test_skill_packages.py \
  trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py \
  trellis/presets/guru-team/scripts/python/test_upstream_ownership.py

python3 -m py_compile \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py \
  trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py

bash -n trellis/workflows/guru-team/scripts/bash/preview-change-context-history.sh
bash -n trellis/workflows/guru-team/scripts/bash/record-context-discovery.sh
bash -n trellis/workflows/guru-team/scripts/bash/check-context-discovery.sh
bash -n trellis/presets/guru-team/scripts/bash/apply.sh
bash -n trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/07-15-111-guru-discover-change-context
git diff --check
git status --short --branch
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
```

## 10. Phase 2 check 与提交边界

- [ ] 实现代理交付 handoff，必须说明 `ssot_first` 执行结果、durable docs 更新、task delta 合并、task-history-only 内容、验证状态与风险。
- [ ] 独立 `trellis-check` sub-agent 覆盖 PRD R1-R10、AC1-AC16、Docs SSOT、current/history 顺序、AI/script boundary、schema、tests、preset、dogfood、upgrade/update 与安全边界。
- [ ] 任一 finding 返回实现代理修复，再由 checker 完整复验；主会话不得用命令通过代替 AI check。
- [ ] Phase 2 pass 后记录并校验 `phase2-check.json`，再 mandatory invoke `guru-create-task-commit`。
- [ ] 只 stage #111 的 durable docs、canonical package/schema/runtime/workflow/preset、dogfood copies、tests 与 task evidence。
- [ ] 不 stage其它 worktree、source checkout、workspace/runtime、未处理 sidecar、legacy payload drift 或用户无关改动。
- [ ] Commit 后独立 Branch Review 覆盖 `origin/main...HEAD` 全 diff；任意 P0/P1/P2/P3 finding 都返回实现与 Phase 2。
- [ ] Branch Review Gate pass 后停止；push、PR、archive、remote verifier 与 issue close 只能由后续 `trellis-finish-work` 显式入口执行。

## 11. 风险与回滚点

| 风险 | 阻断或回滚点 |
| --- | --- |
| Current/history 顺序被实现合并 | 顺序 trace test 不通过即回滚调用链，禁止发布 |
| History reader 读取 index sibling 或整个 archive | 路径/字段 access test 失败即删除越界 reader |
| Score 受输入枚举顺序影响 | permutation test 失败即修复 canonicalization，不保留非稳定输出 |
| Invalid summary 阻塞全部 valid candidates | mixed fixture 必须证明 isolation；失败即回滚 manifest implementation |
| Pre-task 产生 repo 写入 | zero-write snapshot test 失败即停止，移除写入路径 |
| Task-local snapshot 与 stdout snapshot 不同 | expected digest mismatch 必须失败并保留目标现状 |
| Script 代替 AI Gate | 发现自动生成 relevance/sufficiency/pass 即回滚该逻辑 |
| Preset 覆盖用户 Skill | unknown edit fixture 必须保留 target 并产生 conflict evidence |
| Legacy overlay 被扩写 | upstream ownership 或 baseline drift 失败即回滚 legacy change |
| Update 后 package 消失或 sidecar 残留 | throwaway reapply/final sidecar gate失败即禁止 publish |
| Remote verifier 尚未运行 | PR body 与 handoff 明确标记远端验证留给 finish-work |

## 12. 完成条件

- [ ] PRD、design、implementation plan 的每条合同均有代码、schema、test 或 durable docs 承接。
- [ ] `context_ready`、`refresh_base`、`blocked` route evidence 均唯一且 validator-passed。
- [ ] Clean throwaway 与 dogfood gates 完成，未验证项在 Phase 2 report 和 PR body 中逐项披露。
- [ ] Issue scope ledger 只有 #111 位于 `close_issues`。
- [ ] 任务 work commit、Branch Review Gate 与后续 finish-work 均遵守 Guru Team workflow。
