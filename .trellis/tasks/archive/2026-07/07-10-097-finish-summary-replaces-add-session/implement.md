# Issue #97 实施计划

## 1. 执行前门禁

- [ ] 用户审核 `prd.md`、`design.md`、`implement.md` 后明确批准进入 Phase 2。
- [ ] recorder 写入 schema-valid `planning-approval.json`。
- [ ] `check-planning-approval.sh` 通过。
- [x] 主会话已通过 GitHub MCP/API 同步 issue #97 body 的安全过滤合同，并经 live reread 确认。
- [x] 主会话已通过 GitHub MCP/API 把 recovery 的精确 0/1/>1 open PR 状态机同步到 live #97 body，并再次 live reread 确认。
- [ ] commit 后 Branch Review 的 5 个 finding 已完整写入本轮三文档，并取得新的 post-planning approval；approval recorder/validator 完成前不得恢复 Phase 2。
- [ ] `task.py start` 把 task 状态改为 `in_progress`。
- [ ] `trellis-before-dev` 重新读取本 task、spec index、workflow/preset/docs/guides。

## 2. 实施顺序

### Step 1：schema 与 validator

- [ ] 新增 canonical `finish-summary.schema.json`，包含正常 finish 和 backfill 条件分支。
- [ ] 新增 input/final validator、path validator、重复/填充 validator、`retrieval_text` builder；final summary 的任一 path 字段必须拒绝 workspace/runtime 受保护前缀。
- [ ] 新增正常、backfill、路径、长度、数量、枚举、重复、派生值负向测试；受保护前缀不得存在任何 path 字段例外。
- Checkpoint：schema JSON 解析通过，定向 validator tests 通过。

### Step 2：finish recorder 与 dry-run

- [ ] finish parser 加入 `--finish-summary-index-file`，删除 journal 参数和 `--skip-journal`。
- [ ] dry-run 返回 summary input 检查、目标 archive path 和无副作用计划。
- [ ] 正式 finish 在 archive 流程中生成 initial summary，不执行 `add_session.py`。
- [ ] recorder 对 raw diff 排序去重后过滤受保护前缀；过滤集合非空时追加固定且不含路径的 contract change 事实，过滤集合为空时不追加。
- [ ] initial diff、initial untracked snapshot、final/recovery diff 任一失败时清空两个 path 数组，只追加一次固定 snapshot-unavailable fact，不保留任何路径结果或 stderr，并重新派生 `retrieval_text`。
- [ ] metadata commit 只处理 task archive/review/summary 文件。
- Checkpoint：finish unit tests 证明 archive/summary 调用顺序，sentinel `add_session.py` 调用数为零。

### Step 3：publish 回写与 recovery

- [ ] publish 创建 PR 后回写 URL、PR ref 和安全过滤后的 final changed paths；两个 path 数组必须完全一致。
- [ ] 新增精确 summary tail commit/push/remote SHA validator。
- [ ] 扩展 task-local `pr-readiness.json`：记录 repo/base/head branch、reviewed HEAD SHA、exact title、task-local body source、body SHA-256、draft、reviewed source 与 canonical snapshot SHA-256；在首次 create 前随 metadata commit 推送。
- [ ] normal `gh pr create` 客户端失败和 PR-exists summary write/validation/commit/push 失败必须进入同一 recovery；payload 保存 snapshot digest、失败阶段、已知 PR URL 和 recovery command。
- [ ] recovery command 只引用 archived readiness artifact；在 PR query/create 前验证 artifact/body clean、committed Git blob、snapshot/body digest、review gate reviewed HEAD、repo/base/head identity 与 current/remote HEAD，拒绝 title/body/draft override。
- [ ] recovery 在 PR 查询/创建前重验 branch/base identity、AI-reviewed body/readiness、review gate、current HEAD 与 remote HEAD。
- [ ] marketplace-required recovery 只复用并严格 validate 既有 passed verifier evidence，不运行 verifier；normal publish 仍运行 verifier。
- [ ] recovery 查询 current head branch open PR 后只走一个分支：1 个复用；0 个以同一输入只重试 `gh pr create` 一次；多于 1 个 fail closed。
- [ ] 取得 URL 后 normal/recovery 共用 idempotent summary rewrite、精确 metadata commit/push、remote SHA 校验；dirty/staged summary 可接续，额外路径必须拒绝。
- Checkpoint：normal create failure -> 0 open -> retry create success、客户端失败但已有 1 open -> 复用、多于 1 open -> fail、PR exists dirty/staged summary recovery、stale/tampered verifier fail closed、单次 retry 再失败保持 initial summary/同一 recovery command，以及 readiness/body/title/draft/repo/base/head mutation 全部在 query 前 fail closed 的测试通过。

### Step 4：preset、config、ignore 与 workspace 清理

- [ ] installer 管理 finish-summary schema。
- [ ] installer 写 `session_auto_commit: false` 与 `.trellis/workspace/` ignore。
- [ ] installer 移除 workspace index 文案扫描。
- [ ] 删除本仓库 tracked workspace 文件，更新 `.gitignore` / `.trellis/.gitignore`。
- [ ] Phase 2 pre-commit 使用 `git diff --name-status` 验证三个 tracked workspace 路径在 working tree 中均为 `D`，且不进入 finish-summary 任一 path 字段。
- [ ] preset tests 覆盖首次安装、重复安装、true/false/invalid config、workspace 不写入。
- Checkpoint（Phase 2 pre-commit）：三个目标路径的 working-tree status 均为 `D`，dogfood config 为 false；此阶段不得用 `git ls-files '.trellis/workspace/**'` 无输出作为通过条件。

### Step 5：durable docs 与平台入口

- [ ] 更新 canonical workflow、workflow README、preset README、root README、requirements、workflow/preset spec。
- [ ] 完整修订 `docs/requirements/guru-team-trellis-flow.md` 的总图、finish 图、dry-run、Artifact 责任图、companion 职责和讲解主线，删除 journal/add_session 旧合同并加入完整 finish-summary/recovery tail。
- [ ] 更新 shared finish skill 与 Codex/Claude/Cursor canonical overlays。
- [ ] 更新 shared `trellis-start` 固定组合 phase/packages/task/Git facts；从 Codex/Cursor session-start canonical overlays 删除 journal helper import/call；不得修改 upstream `session_context.py`。
- [ ] extension manifest 加入 finish-summary artifact contract。
- [ ] 执行 all-platform preset apply，同步 `.trellis/guru-team/**`、`.trellis/workflow.md` 和平台 dogfood copy。
- Checkpoint：workspace access guard 和 fresh sentinel 证明 shared/Codex/Cursor 启动不打开、不枚举、不读取、不输出 journal；overlay drift 为零，canonical/dogfood byte equality 通过，无 `.new` / `.bak`。

### Step 6：完整验证与 Phase 3 post-work-commit 检查

- [ ] canonical companion tests。
- [ ] preset installer tests。
- [ ] finish-summary search quality fixture pre-PR/post-PR。
- [ ] finish-summary 路径过滤 fixture：全过滤为空、混合路径只保留普通路径、无过滤项保留完整排序去重结果。
- [ ] finish-summary snapshot failure fixture：initial diff、initial `ls-files --others`、final/recovery diff 分别失败时两个 path 数组为空、unavailable fact 恰好一次、filtering fact 不存在、retrieval text 一致。
- [ ] 固定 contract change fixture：有过滤时恰好追加一次且不含具体路径，无过滤时不追加。
- [ ] normal create failure -> 0 open -> 同参数 retry create success fixture。
- [ ] `gh pr create` 客户端失败但查询到 1 个 open PR -> 复用且 create 总调用一次 fixture。
- [ ] 查询到多于 1 个 open PR -> fail closed 且不调用 create fixture。
- [ ] PR exists + dirty/staged summary -> 不重跑 verifier 并完成 idempotent rewrite/commit/push fixture。
- [ ] marketplace verifier artifact/ledger/HEAD tampered 或 stale -> recovery 在 PR 查询前 fail closed fixture。
- [ ] readiness/body/title/draft/repo/base/head/reviewed HEAD/source/digest mutation -> recovery 在 PR 查询前 fail closed fixture。
- [ ] 0 open 的单次 create retry 再失败 -> initial summary 空 URL/ref 不变并返回同一 recovery command fixture。
- [ ] throwaway install + shared/Codex/Cursor workspace sentinel + finish/publish/recovery smoke。
- [ ] throwaway workflow preview 校验并删除预期 `.new`，再执行 switch、`trellis update --force`、workflow/preset reapply；末尾递归 `.new/.bak` 扫描必须为空。
- [ ] Phase 2 pre-commit 完成 task validation、planning approval、Python compile、shell syntax、JSON、workspace boundary、working-tree 删除状态与 `git diff --check`。
- [ ] Phase 3 work commit 后执行 `git ls-files '.trellis/workspace/**'`，结果必须为空；再执行 `git diff --name-status <base>...HEAD -- '.trellis/workspace/**'`，结果必须保留三个 `D` 删除记录。
- [ ] Phase 3 post-work-commit 检查通过后再进入 Branch Review Gate；实现代理与阶段二检查代理不得在 pre-commit 阶段宣称该检查已满足。

## 3. 子代理编排

- 实现代理：按 Step 1-5 修改代码、测试、schema、docs 和 canonical source，不执行 commit/push/PR。
- 阶段二检查代理：覆盖需求、设计、代码、测试、spec、跨层数据流、5 个 Branch Review finding、Docs SSOT、部署/安全影响，并修复发现；旧 `phase2-check.json` 不得作为本轮 PASS 复用。
- Branch Review Gate：问题发现、问题闭环、最终放行使用 workflow 规定的独立代理身份与轮次 ledger。
- main session：维护规划、issue scope、spec 决策、commit plan、commit、finish 与 publish。

## 4. 验证命令

```bash
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 -m json.tool trellis/workflows/guru-team/schemas/finish-summary.schema.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-10-097-finish-summary-replaces-add-session
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task .trellis/tasks/07-10-097-finish-summary-replaces-add-session
git diff --name-status -- .trellis/workspace/index.md .trellis/workspace/wumengye/index.md .trellis/workspace/wumengye/journal-1.md
git diff --check

# Phase 3 post-work-commit：只在 work commit 完成后执行
git ls-files '.trellis/workspace/**'
git diff --name-status main...HEAD -- '.trellis/workspace/**'
```

## 5. 回滚点

- Step 1：schema/validator 单独回滚，不影响当前 finish 路径。
- Step 2：finish recorder 未通过前不进入 publish 修改。
- Step 3：publish recovery 未通过前不清理 workspace tracking。
- Step 4-5：canonical 与 installed copy 必须同批回滚，禁止只回滚 dogfood copy。
- 正式 commit 前保留单一工作树 diff；不得用脚本返回值代替 AI check 和 Branch Review Gate。

## 6. 完成定义

- live #97 body 的 recovery、diff failure 与 context non-read 合同已由实现和测试承接，本轮三份规划文档已取得新的 post-planning approval，planning validator 通过。
- Phase 2 check 为 passed，findings 为空。
- 全部 durable docs 与代码行为一致。
- work commit 使用中文 Conventional Commits。
- Branch Review Gate 覆盖 `origin/main...HEAD` 全量 diff，最终 P0/P1/P2/P3 均为零。
- finish-work dry-run 展示 summary/archive/publish 计划且无 journal。
- 正式 finish 归档 task、生成 summary、创建 PR、回写 URL、推送 metadata tail。
