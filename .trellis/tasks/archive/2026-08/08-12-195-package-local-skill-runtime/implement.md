# #195 实施计划

## 执行原则

- 所有步骤在现有 `feat/195-package-local-skill-runtime`、现有 worktree 和现有 task 内完成。
- 先建立 live ownership inventory，再改 shared schema/kernel/installer；package 迁移按 A-F 顺序推进。
- 每个 checkpoint 的 targeted tests、source/installed validator 和 ownership scan 全部通过后才能进入下一 checkpoint。
- Semantic review 始终由 Markdown Skill 的 AI owner 完成；Python/shell 只执行、记录或校验确定性事实。
- 共享文件由主执行流串行修改。若启用 sub-agent，各 agent 只拥有互不重叠的 package paths，不修改 shared kernel、registry、installer 或 aggregate integration tests。

## 0. 实现前基线

- [ ] 重新读取 issue #195、#156、#205、live `main`、registry、15 个 interfaces 和 `.5` tag；记录 exact OID 与 current package set。
- [ ] 生成 machine-readable inventory：Skill、judgment mode、workflow integration、validator command、wrapper、shared function ranges、tests、evals、installed paths、platform projection。
- [ ] 对 62,356 行单体/聚合测试建立 function/test 到 package owner 映射；未归属条目阻塞 A。
- [ ] 运行当前 source/installed validators、package tests、eval discovery、dogfood drift，保存基线命令与真实结果。
- [ ] 确认 issue-scope ledger 只关闭 #195，并确认没有 `implementation-handoff.md`。

验证：

```bash
jq -r '.skills[] | select(.state == "active") | .id' trellis/skills/guru-team/registry.json
wc -l trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
rg -n 'guru_team_trellis|run-skill-command' trellis .trellis .agents .codex .claude .cursor
```

Rollback point：纯 inventory 与基线，无 runtime mutation。

## A. Schema、kernel、installer 与 pilots

### A1 Command/error schema 与 validator

- [ ] 新增 `commands.json` 与 `errors/catalog.json` schemas、canonical validators 和代表性 positive/negative fixtures。
- [ ] 校验 command id 全局唯一、owner 与 package/registry/interface 一致、entrypoint/wrapper 存在且 mode 正确、interface validators 全覆盖。
- [ ] 校验 error code package 内唯一、command reference 闭合、exit status/remediation/locator 完整。
- [ ] 定义 `--help`/`--json` machine-verifiable output contract 与 side-effect-free help harness。

### A2 Shared kernel

- [ ] 仅迁入具有两个或更多相同语义 consumers 的 JSON/schema/path/dispatch/Git primitives。
- [ ] 为每个 primitive 在 inventory 记录 consumer ids；新增禁止 Skill/profile/exit branching 的 architecture test。
- [ ] shared dispatcher 只根据 registry + commands metadata 定位唯一 package entrypoint。

### A3 Installer/projection

- [ ] 更新 preset installer、extension manifest、ownership schema/fixtures、source/installed validator 和 removal inventory。
- [ ] 完整 package runtime 安装到 `.trellis/guru-team/skills/packages/**`，kernel 安装到 `.trellis/guru-team/runtime/**`。
- [ ] 四个平台只安装 public projection；recursive test 拒绝 runtime/tests/error implementation。

### A4 Pilot migrations

- [ ] 迁移 deterministic `guru-sync-base` 的 sync/check/invoke commands。
- [ ] 迁移 semantic `guru-clarify-requirements` 的 record/check/invoke commands。
- [ ] 将对应 monolith tests 移到两个 package，并增加 help/JSON/error/public-only tests。
- [ ] 证明 pilots 不 import/read/call monolith，semantic/deterministic ownership 保持不变。

Targeted validation：两个 package tests、kernel tests、command/error schema fixtures、source/installed validator、selected-platform projection、两个 public-only eval。

Rollback point：pilots 可单独回退；在 A gate 通过前不迁移 B-E。

## B. Remaining Intake packages

- [ ] `guru-select-workflow-mode`：迁移 invoke route objective validation，不把 caller classification 移入 runtime。
- [ ] `guru-discover-change-context`：迁移 preview/record/check/invoke，保持 live/archived authority 与 owner-private recovery。
- [ ] `guru-review-contract-wording`：迁移 scanner/record/check/invoke，保留 AI classification 与 fixed profile ownership。
- [ ] `guru-review-change-request`：迁移 record/check/invoke，保持 prerequisite/readiness semantic gate。
- [ ] `guru-create-task-workspace`：迁移 plan record/exact execute/result check/invoke，保持 side-effect confirmation dialogue-local。
- [ ] 逐 package 更新 commands/errors、tests/evals 与 inventory，删除其 monolith function/test owner blocks。

Targeted validation：五个 package tests/evals、完整 Phase 0 public command graph、workspace create dry fixture、source/installed validator、platform public-only traces。

Rollback point：按 package 回退；shared contract 变化返回 A review。

## C. Planning、Check、Commit 与 Branch Review

- [ ] `guru-approve-task-plan`：迁移 record/check/invoke，保持 planning composite freshness 与八维 AI review。
- [ ] `guru-check-task`：迁移 Phase 2 record/check/invoke，保持完整 task scope adequacy 与 finding=0 pass。
- [ ] `guru-create-task-commit`：迁移 prepare/check/execute/invoke，保持 exact staging、message review 与 current HEAD binding。
- [ ] `guru-review-branch`：迁移 review record/check/invoke，保持完整 base...HEAD、finding closure 与 fresh-final round。
- [ ] 将对应 tests/evals 分层为 package-local contract 与跨阶段 public integration。

Targeted validation：四个 package tests/evals、planning re-entry、Phase 2 finding paths、commit candidate sandbox、full-diff review fixtures、source/installed validator。

Rollback point：按 package 回退；不得用聚合 fixture owner result 绕过真实 invocation。

## D. Publication 与 Extension Verification

- [ ] `guru-review-task-publication`：迁移 record/check/invoke，保持十维 readiness、metadata-only revision 和真实 PR payload。
- [ ] `guru-verify-extension-installation`：迁移 execute/record/check/invoke，保持 source-repository-only clean throwaway verification。
- [ ] 删除 target-business-repo verifier compat profiles/routes/artifacts 的残留，保持 #205 的 `standalone_only` registry 与不可达业务路径。
- [ ] public-only eval 从 source repo 调用 verifier；business fixture 断言 verifier command/artifact count 为 0。

Targeted validation：两个 package tests/evals、publication re-entry、source throwaway fixture、business unreachable negative route、redaction、source/installed validator。

Rollback point：两个 package 独立回退；不得恢复 #205 前的业务 verifier route。

## E. Finalizer 与 Merge

- [ ] `guru-finalize-task`：迁移 preview/record/check/execute/invoke，保持 confirmation budget、immutable push、single PR、archive transaction、resume/reprepare。
- [ ] `guru-merge-task-pr`：迁移 preview/record/check/execute/invoke，保持 Ready gate、expected-head mutation、GitHub auto-close 和 closure mismatch recovery。
- [ ] Finalizer 输入、输出、checkpoint 和 recovery scan 均不引用 verifier consumer/artifact。
- [ ] 将 transaction tests 留在 package；跨 Finalizer/merge workflow test 只调用 public commands。

Targeted validation：两个 package tests/evals、transaction recovery matrix、expected-head mismatch、closure mismatch、business closeout no-verifier trace、source/installed validator。

Rollback point：在 F 删除前保留 monolith 文件，但 E gate 要求 E commands 的 active route 已完全指向 package owner。

## F. 删除单体与全量收敛

### F1 删除前门禁

- [ ] inventory 显示 15/15 Skills 与全部 commands 唯一归属。
- [ ] source/installed invocation trace 对两个单体的 call/read/import count 为 0。
- [ ] 全仓静态 scan 对 monolith、compat dispatcher/fallback 和聚合 test dependency 的 active reference count 为 0；仅 migration history/明确删除说明可留存。
- [ ] A-E package、kernel、integration、eval 与 staged install validation 全部通过。

### F2 删除与引用清理

- [ ] 删除 canonical `guru_team_trellis.py` 与 `test_guru_team_trellis.py`。
- [ ] 删除 installed copies、legacy bash forwarders、manifest entries、installer copy rules、compat import/fallback 与 dead fixtures。
- [ ] 更新 workflow/preset/root README、extension docs、ownership inventory、schemas/examples 和 dogfood copies。

### F3 全量验证矩阵

- [ ] 运行全部 package-local tests、kernel tests、integration tests、eval discovery/runner、source validator 和 installed validator。
- [ ] 执行 clean repo initial install 与 README 逐字列出的 workflow marketplace/preset commands。
- [ ] 执行 exact remote candidate install。
- [ ] 从 `v0.6.5-guru.5` existing repo 执行 upgrade，验证 old managed monolith 删除与 user-modified sidecar fail-closed。
- [ ] 执行 official Trellis update 后 workflow/preset reapply，处理全部 `.new`/`.bak`，再运行 drift。
- [ ] 执行 shared/Codex/Cursor/Claude discovery、wrapper invocation、typed output 与 private-path denial。
- [ ] 在一个代表性业务仓库安装方式上执行 closeout smoke，记录 no-monolith/no-verifier/no-artifact trace，并标注非生产证明。
- [ ] 运行递归引用 scan、manifest file/mode equality 与 `git diff --check`。

计划命令入口：

```bash
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh
trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --json
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
git diff --check
```

具体参数以实现后的 `--help` 和 README contract 为准；命令与实际证据不一致时，以 fail closed 处理并修正文档。

Rollback point：若 F 暴露遗漏 owner，恢复删除前文件并返回所属 checkpoint；若 upgrade/update 投影失败，保留 package runtime 实现并修复 installer provenance，不建立双 runtime。

## Docs reconciliation

- [ ] 更新 package `SKILL.md`/contract/interface/commands/errors，确保 step-local SSOT 一致。
- [ ] 更新 `.trellis/spec/workflow/skill-package-contract.md` 与 companion-script/data/quality specs 的通用规则。
- [ ] 更新 canonical workflow 与 dogfood workflow，只保留 global routing。
- [ ] 更新 preset/workflow/root README 的 install、upgrade、projection、CLI 和验证命令。
- [ ] 运行 Markdown link、command reference、deleted-path 与 controlled wording scan。

## 最终 gates

- [ ] PRD、design、implement 和 Docs SSOT 与最终实现一致。
- [ ] `guru-check-task` 对完整 task scope 返回 pass，findings 为 0。
- [ ] task commit 只 stage 本 task 文件，提交信息与 current diff 一致。
- [ ] independent Branch Review 覆盖 `origin/main...HEAD` 完整 diff，fresh-final findings 为 0。
- [ ] Publication review 验证中文 PR title/body、真实验证、安全/部署影响与唯一 `Closes #195`。
- [ ] Finalizer 和 merge 仅在各自后续明确授权及 live gate 通过后执行。
