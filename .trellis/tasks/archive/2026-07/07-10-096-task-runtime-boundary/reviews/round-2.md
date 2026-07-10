# Branch Review Round 2：问题闭环审查报告

## 审查元数据

- 审查角色：Branch Review Round 2，问题闭环审查代理。
- 审查 HEAD：`90a2d45c823775ff0eaa485ef10640d8b4aa96f5`。
- 审查范围：`origin/main...HEAD`；merge base / `origin/main` 为 `59d6c0caf404c4c927fe8aada92811d1ced907d5`。
- 提交序列：`a84e5720d0ea18482b46b165062930e50cf54b34`、`90a2d45c823775ff0eaa485ef10640d8b4aa96f5`。
- 完整 diff：63 个文件，`3564 insertions(+), 1228 deletions(-)`。
- Workspace boundary：expected workspace 与 actual repo root 均为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/096-task-runtime-boundary`；source checkout 无改动、无 suspicious source artifacts；本轮开始时 task worktree 仅 `agent-assignment.json` 为审查 metadata dirty。
- 审查输入：Round 1 原始报告、最新 `phase2-check.json`、`issue-scope-ledger.json`、`agent-assignment.json`、`planning-approval.json`、`implementation-handoff.md`、`prd.md`、`design.md`、`implement.md`、`check.jsonl` 引用的 spec/research、Issue #96 实时正文以及完整 committed diff。
- 审查行为：未修改实现、未 commit、未 push、未创建 PR、未记录 `review-gate.json`。

## Round 1 Finding 生命周期

### Finding 1 — P1：SHA 映射

- Round 1 状态：阻塞。
- Round 2 状态：已闭环。
- 证据：`build_task_start_context()` 读取 `base_freshness.local_head_after` 与 `base_freshness.remote_head`；`fresh` 要求二者非空且相等，`remote_only` 和 fetch/remote 异常状态也有 fail-closed 约束。
- 测试：`TaskRuntimeBoundaryContractTest` 覆盖 fresh SHA copy、mismatch reject、remote-only、fetch-failed；定向测试通过。

### Finding 2 — P1：clean clone preset fixture

- Round 1 状态：阻塞。
- Round 2 状态：已闭环。
- 证据：旧 schema 固化为 committed fixture `trellis/presets/guru-team/scripts/python/fixtures/intake-handoff.schema.json`，测试不再调用 `git show HEAD:path`。
- 复现：在 `git clone --no-local` 的干净 clone 固定 checkout 到审查 HEAD 后，preset suite `Ran 30 tests`、`OK`；fixture 在 Git index 中存在且可直接读取。

### Finding 3 — P1：push 后 marketplace verifier

- Round 1 状态：阻塞。
- Round 2 状态：主执行链已闭环，但新增 verifier 仍有一个 P2 artifact-contract 问题，见新 Finding 2。
- 真实执行点：`cmd_publish_pr()` 在 `git push -u` 后、`gh pr create` 前调用 `execute_marketplace_verification()`；通过后仅提交 `marketplace-verification.json`，再次 push，并调用 `validate_marketplace_verification()`。
- Metadata-only tail：`commit_marketplace_verification_artifact()` 只允许 verifier artifact 为 dirty path，其他 task metadata 也会 fail closed。
- Identity：校验 `repo`、`remote`、`branch`、`marketplace_source`、`task_dir`。
- Digest：校验 installed workflow、preview workflow、installed task-start-context schema 与当前 canonical digest 一致。
- Obsolete absence：校验 `.trellis/guru-team/handoff.json` 与 `schemas/intake-handoff.schema.json` 不存在，并校验 `.trellis/.runtime/` ignore。
- Stale：verified content HEAD 到 publish HEAD 只允许 verifier artifact；其他路径阻塞。
- Remote HEAD：首次 verifier 要求远端 content HEAD 等于 expected HEAD；metadata tail push 后要求远端 HEAD 等于当前 publish HEAD。
- Fail-closed：verifier missing/failed/stale/identity/digest/obsolete/remote HEAD mismatch 均在 `gh pr create` 前阻塞；定向负向测试通过。
- 当前远端事实：`origin/codex/096-task-runtime-boundary` 尚不存在，`marketplace-verification.json` 尚未生成；本轮不能把远端 branch 安装结果声明为已通过。

### Finding 4 — P1：Issue Scope Ledger acceptance evidence

- Round 1 状态：阻塞。
- Round 2 状态：仍未闭环，见新 Finding 1。
- 已改善：ledger 已列出 AC1-AC10，不再是空数组。
- 未闭环原因：AC9 明确写的是“当前未 push，未来由 verifier 生成”；`validate_ledger_for_publish()` 只判断 acceptance_evidence 列表非空，不校验证据状态，也没有任何 publish 路径在 verifier 成功后回写 ledger。因此 deferred 文字会在真实远端验收发生前通过 ledger validator，且 verifier 成功后 AC9 仍不会变成真实 passed evidence。

## 问题清单

### Finding 1 — P1：Issue #96 的 AC9 仍是 deferred 说明，publish 不会把真实远端 verifier 结果写回 ledger

- 文件：`.trellis/tasks/07-10-096-task-runtime-boundary/issue-scope-ledger.json:16`、`.trellis/tasks/07-10-096-task-runtime-boundary/issue-scope-ledger.json:35`。
- 代码：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:2406`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:7497`。
- 事实：AC9 自述“当前未 push，不伪造 passed”；远端 branch 和 verifier artifact 当前都不存在。
- 事实：`validate_ledger_for_publish()` 的 `issue_has_evidence()` 只要数组中有非空字符串就视为有 evidence；本轮直接调用 validator 返回空错误列表。
- 事实：`cmd_publish_pr()` 先执行 ledger validator，后 push/verifier；verifier 成功后只写并提交 `marketplace-verification.json`，不会更新 `issue-scope-ledger.json`，也不会再次验证“close issue 的每项 acceptance 已真实 passed”。
- 影响：Round 1 要求“按 Issue #96 验收项补齐真实命令、文件和结果；远端 marketplace gate 只能记录真实 push 后结果，不得用 deferred 说明替代 passed evidence”。当前实现仍允许 deferred AC9 被当作 close evidence，并且没有闭环机制把真实远端结果纳入 ledger / Branch Review 覆盖。`Closes #96` 的验收证据仍不充分。
- 建议：把 AC9 表达为结构化 pending/passed evidence，publish verifier 成功后由 recorder 更新 task-local ledger 并重新执行 publish validator；或者在最终放行前先执行独立 push-only verifier，提交真实 artifact 和 ledger evidence，再由新的 reviewer 覆盖 metadata tail。不能继续以非空 deferred 文本满足 close evidence。

### Finding 2 — P2：`marketplace-verification.json` 的失败 payload 不符合其公开 schema

- 文件：`trellis/workflows/guru-team/schemas/marketplace-verification.schema.json:16`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:7367`。
- 事实：schema 允许 `status: failed` 和空 `remote_head`，但同时强制三个 asset digest 为 64 位 SHA，并强制 runtime ignore / obsolete absence 为 `true`。
- 事实：当 `git ls-remote`、clone、init、preview、switch 或 preset 在生成资产前失败时，executor 仍会写 `status: failed` artifact；三个 digest 为空，runtime ignore 可能为 `false`。本轮用 `ls-remote` failure probe 生成 payload 后，`jsonschema.validate()` 失败。
- 影响：公开 schema 无法描述 companion recorder 实际承诺写出的失败证据；下游如果按 schema 接收 artifact，会把最需要审计的失败记录视为 malformed，而不是合法 failed evidence。extension manifest 将该 schema 暴露为公共 artifact contract，因此属于新 gate 自身的一致性问题。
- 建议：对 `status` 使用条件 schema：`passed` 强制完整 digest/true 条件，`failed` 允许空 digest/false 并依赖 `steps` 保存失败事实；同时增加 executor failure payload 的 schema validation 测试。

## 完整 HEAD / Diff 证据

- `git rev-parse HEAD`：`90a2d45c823775ff0eaa485ef10640d8b4aa96f5`。
- `git rev-parse origin/main`：`59d6c0caf404c4c927fe8aada92811d1ced907d5`。
- `git merge-base origin/main HEAD`：`59d6c0caf404c4c927fe8aada92811d1ced907d5`。
- `git log --reverse origin/main..HEAD`：2 个提交，提交信息检查通过。
- `git diff --name-status origin/main...HEAD`：63 个文件，覆盖 canonical workflow/script/schema/config、preset installer/fixture/overlays、dogfood copies、README/requirements/spec、任务 artifacts 与 Round 1 报告。
- `git diff --check origin/main...HEAD`：通过。
- Phase 2 post-commit audit：`phase2-check.json.head` 为 `a84e5720d0ea18482b46b165062930e50cf54b34`；Round 1 修复提交的非 metadata 路径均被 `dirty_paths` 覆盖，`validate_phase2_check(..., allow_committed_head=True)` 返回无错误。

## 验证结果

- Clean clone core tests：`python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`，230 tests，通过。
- Clean clone preset tests：`python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`，30 tests，通过。
- 定向 tests：SHA、marketplace metadata-only、执行顺序/digest、publish verifier fail、stale、tampered identity，共 12 tests，通过。
- Python compile：通过。
- Shell syntax：通过。
- JSON / JSONL parse：通过。
- Task context validate：9 implement + 10 check entries，通过。
- Commit messages：2 个提交，通过。
- Dogfood overlay drift：通过。
- Canonical/dogfood：workflow、Python companion、verifier shell、verifier schema、config template 字节一致。
- Finish-work overlays：Agents/Codex/Claude/Cursor canonical overlay 与 dogfood copy digest 一致；均描述 push 后 verifier、metadata-only tail、fail-closed 和 PR 前执行点。
- 真实远端 marketplace：未执行；远端 branch 不存在，不能声称通过。

## Docs SSOT

- Plan strategy：`ssot_first`。
- Durable docs：canonical workflow、workflow/companion/data specs、README、workflow README、preset README、requirements docs 已同步 remote marketplace gate 与 task runtime boundary。
- Canonical/dogfood/overlay：同步通过；未发现 finish-work 平台入口仍停留旧流程。
- Task artifacts：planning、handoff、Phase 2、ledger、assignment 与 Round 1 报告已纳入审查。
- 当前不一致：durable workflow 说 AI 必须判断 verifier evidence 是否充分且真实；但 publish executor 不会把真实结果回写 close issue ledger，ledger validator 又接受 deferred 非空文本。因此 Docs SSOT 的判断责任与 deterministic evidence chain 尚未真正闭环。

## AI / 脚本边界

- 正确部分：脚本只执行 push、远端命令、digest/HEAD/schema/path 校验和 artifact 记录；没有替代 AI 判断 PR readiness 或 issue close scope。
- 风险部分：ledger validator 把“存在任意非空文字”等同于验收证据充分，会让 deferred 声明机械通过。该规则不是 AI 判断，但会错误放行缺少真实 evidence 的 close scope；需要结构化状态或新的 AI review 后 evidence recorder 来闭环。

## 安全与部署影响

- 安全：committed diff 未发现 token、private key、`.env`、数据库 URL、签名 URL或客户数据；task-start context 当前未包含本机绝对路径。
- 临时目录：verifier 使用 `TemporaryDirectory`，命令证据隐藏 remote URL 和 temp path，避免把本机路径写入 artifact。
- 部署：不涉及业务服务、容器、Kubernetes、数据库 migration、CI/CD 或 Makefile；影响集中在开发工作流、marketplace/preset 安装、task metadata、finish/publish 门禁。
- 发布风险：Finding 1 会影响 `Closes #96` 的真实性；Finding 2 会影响失败 verifier artifact 的可审计与 schema 消费。

## 观察项

- Round 1 的 SHA、clean clone fixture、marketplace 执行链三个 P1 已有代码与测试闭环。
- Phase 2 报告把 ledger P1 标为 resolved，但其 resolution 明确承认 AC9 未执行；这与 Round 1 的“必须是真实结果”不一致。
- `marketplace-verification.schema.json` 当前没有被 Python executor runtime 调用；公开 schema 与手写 validator 同时存在，后续容易继续漂移。
- 旧 `handoff` 字符串在 active implementation 中仅用于 forbidden-key/obsolete absence/cleanup fixture；另有 `.trellis/spec/preset/overlay-guidelines.md` 的历史措辞，不影响本 issue runtime public API，但可在后续 spec 清理时统一。

## 后续候选

- 为 ledger acceptance evidence 定义结构化 `status`、artifact digest、verified HEAD、command result，并让 publish 在 verifier 后重新校验。
- 为 marketplace verifier 的 passed/failed payload 都加入 JSON Schema validation 单测。
- 在 release/合并后执行 stable tag marketplace 验证；不得以当前 branch 单测替代稳定 tag 证据。

## 结论

- Findings：2 个，其中 P1 1 个、P2 1 个；无 P0。
- Round 1 生命周期：Finding 1 已闭环；Finding 2 已闭环；Finding 3 的主执行链已闭环但产生一个新 P2；Finding 4 未闭环。
- 当前不建议进入最终放行审查，不可生成通过型 `review-gate.json`，不可执行 finish/publish，不可使用 `Closes #96`。
- 修复 ledger 的真实验收 evidence 闭环和 verifier failed schema 后，应更新提交并由新的 reviewer 覆盖新的 `origin/main...HEAD` 完整 diff。
