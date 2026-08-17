# #242 v0.6.5-guru.8 执行计划

## Phase A：Planning 与任务激活

- [x] live 读取 Issue #242、related/follow-up/excluded Issue、fresh main、tags、Releases、
  AGENTS、canonical workflow、public Skills/spec、preset/installer/release docs。
- [x] 确认 base reconciliation 后 `v0.6.5-guru.7..origin/main` 为 26 个 commit、1008 个
  path；#208/#164/#236/#237/#243 是累计 payload，bootstrap 与 #243 task archive commits
  不扩张功能 scope。
- [x] 创建独立 branch/worktree/task/runtime mapping，未复用 #222/#236/#237/#243 资源。
- [x] 固定 `.33`/`guru.8`/CLI `0.6.5` 版本映射与 bytecode/model evidence 边界。
- [x] 完成 `prd.md`、`design.md`、`implement.md`、Docs SSOT Plan 与 curated
  `implement.jsonl`/`check.jsonl`。
- [x] 运行 planning wording review、planning scenario qualification 与
  `guru-approve-task-plan`；只消费唯一 `approved` exit。

## Phase B：Release preparation 实现

- [x] 通过 `trellis-before-dev` 重新注入 docs/preset/workflow specs。
- [x] 将 `trellis/guru-team-extension.json` 从 `0.6.5-guru.32` 更新为
  `0.6.5-guru.33`。
- [x] 更新 `README.md`、workflow README、preset README 中的 stable tag/source/version
  mapping、initial install、preview/switch、update/reapply 与验证声明。
- [x] 更新 `public-docs.md`、`installer.md`、`data-contracts.md` 的 current release
  mapping；不修改 #239 canonical bytecode contract。
- [x] 更新 canonical `guru-verify-extension-installation` execution/marketplace examples、
  contract tests、throwaway verifier expected version 与 preset installer regression test。
- [x] 新建 task-local `release-notes-zh.md`，覆盖 #208/#164/#236/#237/#243、升级步骤、版本
  映射、无 live 模型证据声明、安全与部署影响。
- [x] 运行 preset `apply.sh --repo . --all-platforms`，只接受预期 dogfood/platform
  projection；逐项检查 `.new`、`.bak`、conflict、removal、unknown sidecar。
- [x] 运行无落盘 `compile()` syntax check；不得在 source/snapshot 写入 bytecode。

## Phase C：Phase 2 验证与 semantic check

- [x] 验证 canonical/dogfood/platform byte equality、extension version、managed inventory、
  executable mode、ownership、registry/workflow graph 与 overlay drift。
- [x] 运行 manifest/schema/package/integration/eval targeted suites、preset regression、
  throwaway Python routing tests、normal-scenario qualification tests与 finish-family tests。
- [x] 运行 clean throwaway initial install、preview/switch、official update、preset reapply、
  linked worktree/closeout 与双 PATH README verifier。
- [x] 在 production/throwaway staged roots 首次执行前执行 bytecode exact-path scan，要求
  零命中；staging copy 显式排除 `__pycache__/`、`*.pyc`、`*.pyo`。
- [x] postflight 再次扫描 staged roots并要求零命中；source ignored bytecode 不参与
  identity/freshness/blocking evidence。
- [x] 运行 #237 deterministic/no-model/fake-production、sandbox、schema/route、安装投影
  与独立 review；明确不运行 live GPT-5.6 Sol matrix。
- [x] 使用 Trellis implement/check sub-agent 取得独立当前 worktree evidence。
- [x] 运行 `guru-check-task`；finding 修复后按影响范围重新运行 qualification 与验证。
- [x] 验证 `python3 ./.trellis/scripts/task.py validate
  .trellis/tasks/08-16-242-release-v065-guru8` 与 `git diff --check`。

## Phase D：Commit、Branch Review 与 PR

- [ ] 展示 exact staged paths、commit message、命令和副作用；取得“确认继续”后执行。
- [ ] 运行 `guru-create-task-commit`，只提交 #242 task 与 release-owned paths。
- [ ] 对完整 `origin/main...HEAD` 运行独立 fresh-final `guru-review-branch`；不复用 Phase 2
  或旧 `review.md`。
- [ ] 关闭全部当前 P0/P1/P2/P3 finding，并重跑受影响门禁。
- [ ] 完成中文 PR title/body、scope ledger、验证、安全、部署、配置与未验证边界的 PR
  readiness review。
- [ ] 分别展示 push 与 PR 创建的 exact command/payload/副作用；各自取得“确认继续”后执行。
- [ ] live 回读 PR head/base/body/checks；merge 前再次冻结 expected head。
- [ ] 只有收到精确文本“合并PR”后执行 PR merge，并 live 回读 merge commit 与 #242
  仍 OPEN。

## Phase E：Fresh candidate 与累计 pre-tag gate

- [ ] PR merge 后读取 fresh `origin/main`；要求 clean checkout 且 HEAD/local/remote 三方一致。
- [ ] 冻结 candidate commit/tree、26 个当前 commit 加 release preparation commits、完整
  path 集合、五个 payload Issue/PR 与唯一 `.33` version。
- [ ] 正式执行 `guru-verify-extension-installation` source-repository public wrapper。
- [ ] fresh 执行 canonical/source/installed/platform equality、ownership、overlay drift、
  package/integration/eval、clean install、preview/switch、official update 与 reapply。
- [ ] fresh 执行 linked worktree/closeout、双 PATH interpreter identity、bytecode staging
  preflight/postflight、零 sidecar/removal/conflict。
- [ ] fresh 执行 deterministic/no-model/fake-production、sandbox、schema/route、安装投影
  与独立 review；Release evidence 明确无 live GPT-5.6 Sol production semantic evidence。
- [ ] 任一 candidate byte 或 release-owned metadata 变化时重新冻结并重跑绑定证据。

## Phase F：Tag、tag-pinned smoke、Release 与 closure

- [ ] 展示 annotated tag object/message/candidate、`git tag -a`、exact push refspec 与副作用；
  取得“确认继续”后执行。
- [ ] 创建并 push immutable `v0.6.5-guru.8`，live 回读 tag object/type/message、peeled
  commit、candidate tree、manifest version 与 source bytes。
- [ ] 展示 tag-pinned fresh clone smoke 的 `mktemp` root、clone/checkout/install/update/
  reapply 命令、本地文件副作用与删除策略；取得“确认继续”后执行。
- [ ] 从全新 clone checkout immutable tag，执行真实 README clean install/upgrade smoke；
  不使用 branch、本地 checkout 或旧 clone。
- [ ] 展示 GitHub Release title/body/target/assets 与 `gh release create` 副作用；取得
  “确认继续”后执行。
- [ ] 创建非 draft、非 prerelease Release 并 live 回读 target/assets/notes/version mapping。
- [ ] 展示 `gh issue close 242` 的 exact command 与副作用；取得“确认继续”后执行。
- [ ] 关闭 #242，最终 live 回读 tag、peeled commit、Release 与 Issue state；确认 excluded/
  follow-up Issue 和既有资源未变化。

## 核心验证入口

```bash
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-16-242-release-v065-guru8
python3 trellis/skills/guru-team/tests/test_skill_packages.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
python3 trellis/presets/guru-team/scripts/python/test_verify_throwaway_python_routing.py
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-managed-python-runtime.sh --repo . --json
git diff --check
```

正式 verifier invocation、candidate identity、staging roots、PATH A/B 构造、normal-scenario
profile 集合与最终 Release payload 均从执行时 live contracts 生成。Planning 不预填 PASS。
