# Branch Review Round 2 问题闭环审查报告

## 审查身份与 freshness

- 逻辑角色：`问题闭环审查代理`
- Technical agent id：`/root/branch_review_112`
- 身份复用：本代理是 Round 1 finding owner，允许执行问题闭环审查；不能担任后续最终放行审查代理
- Primary issue：`#112`
- Finding baseline HEAD：`26a284477a1c1c21760ff7f93409466ebda9100f`
- Reviewed HEAD：`c032fa6f37e25bf5b4ed1227b8b2264eb580a8e3`
- Finding-fix diff：`26a284477a1c1c21760ff7f93409466ebda9100f..c032fa6f37e25bf5b4ed1227b8b2264eb580a8e3`
- 完整 Branch Review diff：`origin/main...c032fa6f37e25bf5b4ed1227b8b2264eb580a8e3`
- 修复提交：`fix(trellis): #112 隔离任务创建身份读取`，33 files，`1337 insertions / 309 deletions`
- 审查方式：只读语义闭环审查；除本 raw report 外未修改实现、Phase 2、commit plan、assignment、rollup 或 gate artifact，未 stage、commit、push、创建 PR 或关闭 Issue
- 禁止命令遵守：未运行 `review-branch.sh`、`check-review-gate.sh`、任何 `record-*`、commit、push 或 PR 脚本

Workspace boundary 检查通过：expected workspace 与 actual repo root 均为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/112-create-task-workspace`，source checkout 干净，suspicious source artifacts 为空。审查开始与报告写入前 HEAD 均精确等于 Reviewed HEAD。

## 审查输入与范围

- 读取 Round 1 raw report `reviews/001-final.md`，逐项复核两项 P2 与 exact issue body 观察项。
- 读取批准的 `prd.md`、`design.md`、`implement.md`、`check.jsonl` curated specs、planning approval、fresh `phase2-check.json`、implementation/Phase 2 handoff、issue ledger 与 task commit plan 002。
- 审查 finding-fix commit 的 33 个 committed paths，包括 canonical/installed runtime、package contract/tests、throwaway verifier、公开 requirements/spec/README、extension manifest 与全部平台副本。
- Planning approval 仍为 schema 1.2、`explicit-post-planning-review`、passed ambiguity review、zero unchecked normative hits；三份 planning artifact digest 与 approval 记录一致。
- Commit plan 002 的 commit SHA、parent、33 个 committed paths、expected/actual tree、33 条 blob/mode evidence 均与 Reviewed HEAD 完全一致，mismatch 为 0。

## Finding 生命周期

### P2-1：existing `.trellis/.developer` 污染 `task.json.creator`

状态：`closed`

- Runtime 新增隔离 subprocess adapter，调用 official `common.task_store.cmd_create`，仅在该 handler invocation 内将 module-local `get_developer` accessor 替换为 null result。
- Executor 不再检查 source/target `.trellis/.developer` 或 `.trellis/workspace/**` 是否存在，并把 result identity checker 扩展为 `creator=assignee=reviewed login`。
- Fresh focused unit test 真实复制 official `.trellis/scripts`，在 existing `name=legacy-identity` 下调用 adapter；结果 `creator=assignee=explicit-assignee`，identity bytes 未改变。
- Fresh installed normal-path verifier 在 source 与 target 都存在相同 identity bytes 时完成 production recorder/executor/checker：typed exit `created`、checker `passed`、`task_creator=fixture-maintainer`、source/target identity SHA-256 相同且保持不变、未创建 workspace journal。
- Throwaway initial no-identity 与 after-update existing-identity 两条路径均进入正式安装 runtime；Phase 2 记录完整 throwaway exit 0。
- Canonical runtime 与 dogfood runtime SHA-256 相同；canonical、installed、Agents、Codex、Cursor、Claude 的 contract/test copies 分别 byte-identical。

结论：Round 1 P2-1 已在受支持正常路径中关闭，未发现 adapter 绕过 official lifecycle、污染全局 module state或弱化 result checker。

### P2-2：`0.6.5-guru.15` manifest 与公开 README 漂移

状态：`open`

- 已关闭部分：`README.md:428`、`trellis/workflows/guru-team/README.md:58` 与 `trellis/presets/guru-team/README.md:303` 已改为 `0.6.5-guru.15`；canonical manifest 与 installed manifest 的 `extension.version` 也是 `.15`。
- 未关闭证据：`trellis/workflows/guru-team/README.md:33` 仍写“本分支 canonical `.13`”，同文件第 58 行却写待发布 `.15`。
- Round 1 P2-2 已明确把第 33 行列入 finding scope，因此不能把该残留归类为新发现或历史无关问题。
- Implementation handoff 声明“三份 README 统一到 `.15`”，fresh Phase 2 也声明 P2-2 resolved，但两份语义证据都没有覆盖当前 live README bytes。
- `ssot_first` 与 AC14 要求 root/workflow/preset README、manifest、durable specs 和安装副本当前一致；自动化测试与 byte parity 不能替代该公开文案的语义一致性审查。

结论：Round 1 P2-2 未完全关闭。Fresh `phase2-check.json` 中 “当前无 P0-P3 finding” 与 “README version drift resolved” 的结论不充分，必须保持阻塞。

## Exact Issue Body 观察项

状态：`closed observation`，未形成新 finding。

- `create_issue()` 不再对 reviewed title/body 执行 `.strip()`，也不再向 body append newline；temporary body file 使用 `newline=""` 并写入 exact reviewed string。
- Fresh adapter test 捕获传给 `gh issue create --body-file` 的 bytes，确认 title 未改变且 body 精确等于 reviewed UTF-8 bytes。
- Created issue 后续仍由 live reread 与 title/body/labels digest checker 绑定；任何 GitHub 返回内容漂移会 fail closed 到 refresh/review，而不是继续创建 workspace/task。
- 该改动没有扩大 GitHub 副作用范围，也未发现 current-scope regression。

## Docs SSOT

- Plan strategy：`ssot_first`。
- Identity adapter、creator/assignee contract、existing identity preservation 与 exact body 规则已经同步到 durable requirements、workflow/preset specs、package contract、root/preset/workflow README 和平台副本。
- `trellis/workflows/guru-team/README.md:33` 的 `.13` 与同文件 `.15` 仍冲突，因此 current-scope public Docs SSOT 未收敛。
- Task delta、Round 1 finding、implementation/Phase 2 handoff 与 commit evidence 正确保留为 task-history-only；问题不是 task-history merge，而是 live durable README 漏改。
- 当前报告只能作为 blocking closure report 汇入 `review.md`，不能支持 Branch Review Gate pass。

## 验证结果

- Fresh focused runtime tests：`2/2 passed`，覆盖 existing identity adapter 与 exact issue body bytes。
- Fresh installed existing-identity verifier：`status=ok`、typed exit `created`、checker `passed`、creator/assignee 正确、identity bytes 保持、workspace journal 未创建。
- Phase 2 五文件 Python suite：`Ran 638 tests in 184.401s, OK`。
- Phase 2 full throwaway：exit 0，覆盖 initial install、finish-work、update、workflow reselect、preset reapply、no-identity、existing identity 与 sidecar=0。
- Source/installed validators、upstream ownership、43 frozen overlays、dogfood drift、JSON/JSONL、`py_compile`、`bash -n` 与 `git diff --check`：通过。
- Commit plan 002：33 committed paths 与 commit path set 完全一致；HEAD tree=`11a96f6e0cc59c012d75c7b87d31d955ba12c14c`，expected/actual tree 相同，path evidence mismatch=0。

通过的测试未检测 workflow README 第 33 行的 stale `.13`，因此不能关闭 P2-2。

## 安全与部署

- `origin/main...HEAD` 未修改 CI/CD、Docker、Docker Compose、Kubernetes、Helm、数据库 migration 或 Makefile；无服务部署与数据库迁移影响。
- 高置信 added-line credential 扫描未发现 GitHub token、AWS key、private key、数据库凭据、签名 URL 或敏感原始数据。
- Identity adapter 的 monkeypatch 仅存在于独立 subprocess，进程退出后不影响调用方 runtime；existing identity bytes 不被修改。
- 当前变更的运行影响限于 Guru Team task workspace runtime、Skill contract/tests、preset/throwaway、公开文档与多平台安装副本。

## Findings 汇总

- P0：0
- P1：0
- P2：1
- P3：0
- Findings count：`1`

Open finding 是 Round 1 `P2-2` 的未完成闭环，不是新增 scope。

## 观察项

- 当前 reviewer session 的 `task.py current --source` 返回 stale 临时复现 locator `.trellis/tasks/07-19-review-explicit-assignee`；显式 #112 workspace boundary 仍通过，source checkout 无可疑 artifact，且该 session-local runtime 状态不在 committed diff 中。本轮始终使用显式 task path，未让 stale locator 改变审查范围。
- Remote branch/tag marketplace verification 尚未执行，仍应由 publish/finish gate 在真实 pushed ref 可用后完成；它不是本轮 open finding。

## 后续候选

无。P2-2 属于 #112 当前范围，应直接修复 `trellis/workflows/guru-team/README.md:33`，重跑 Docs SSOT/version scan 与 fresh Phase 2，再提交新的 finding-fix commit；不应外移为新 Issue。

## 证据交接

- Reviewed HEAD：`c032fa6f37e25bf5b4ed1227b8b2264eb580a8e3`
- Finding-fix diff：`26a284477a1c1c21760ff7f93409466ebda9100f..c032fa6f37e25bf5b4ed1227b8b2264eb580a8e3`
- P2-1：closed；P2-2：open。
- Findings count：`1`（`P2=1`）。
- Docs SSOT：`ssot_first` 未完成，fresh Phase 2 semantic conclusion 不充分。
- 部署影响：无 CI/CD、container、Kubernetes/Helm、database migration 或 Makefile 变更。
- 安全影响：未发现 credential/secret；adapter mutation 隔离在 subprocess。
- 本报告可供 main session 汇总 blocking `review.md`，不能支持 Gate pass、publish 或 Issue closeout。

## 结论

- Round 2 问题闭环审查：`阻塞`
- Round 1 两项 P2 中 1 项关闭、1 项仍开放
- Findings count：`1`
- 修复 P2-2 并取得 fresh Phase 2 后，需要新的问题闭环复核；全部 finding 关闭后还必须分配 fresh final reviewer，本代理作为 finding owner/closure agent 不能兼任最终放行。
