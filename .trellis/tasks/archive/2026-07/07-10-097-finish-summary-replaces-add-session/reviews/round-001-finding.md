# Issue #97 Branch Review Gate 第一轮问题发现审查

## 审查身份

- 逻辑角色：`问题发现审查代理`
- Technical agent id：`/root/issue97_branch_finding`
- 审查轮次：`round-001`
- Reviewed HEAD：`53f265f3949ca8374c7b534da309a4c924325450`
- Diff range：`origin/main...HEAD`
- Base HEAD：`ff8c03abb259c2a048626ea72e0bf57138db2c14`
- 审查模式：只读审查；除本 raw report 外未修改实现、规划、durable docs、测试、gate、ledger 或发布产物，未 stage、commit、push、创建 PR 或调用 finish-work。

## 审查范围与证据

- Live scope：实时读取 `castbox/guru-trellis#97`，核对 workspace non-read/non-write、finish-summary 字段、安全路径过滤、diff 失败降级、PR URL 两阶段回写和 `0/1/>1` recovery 合同。
- 规划与执行证据：读取批准版 `prd.md`、`design.md`、`implement.md`、`implementation-handoff.md`、`phase2-check.json`、`issue-scope-ledger.json`、`agent-assignment.json`、`pr-body.md` 和 task research。
- 完整分支：核对 `origin/main...53f265f3949ca8374c7b534da309a4c924325450` 的 1 个 commit、45 个文件、5396 additions / 2094 deletions及完整 commit subject/body。
- 代码与测试：逐段审查 `finish_summary_git_path_snapshot()`、schema/Python validator、normal/backfill parity、`publish_recovery_command()`、`resolve_open_pull_request_for_recovery()`、`create_pull_request()`、marketplace evidence、summary rewrite/commit/push、preset installer、throwaway verifier和相关测试。
- Canonical/dogfood：workflow、companion、finish-summary schema、marketplace schema及 Codex/Claude/Cursor/shared finish entry canonical/installed copies逐字一致；dogfood overlay drift 为零。
- 官方边界：实时读取 Trellis `custom-workflow.md` 与 `custom-spec-template-marketplace.md`；本分支继续使用 Markdown workflow/marketplace/preset 扩展面，未修改 upstream、全局 npm 或 `node_modules`。

## 问题清单

### F-001 P2：Guru Team 标准 context 入口仍读取 `.trellis/workspace/**`

- Live #97 明确要求 Guru Team 不再读取 `.trellis/workspace/**` 作为 finish/readiness/context 证据；canonical workflow 同时声称 Guru Team `never uses it for finish/readiness/context evidence`。
- 但 `trellis/workflows/guru-team/workflow.md:384-390` 与 `.agents/skills/trellis-start/SKILL.md:14-19` 仍要求执行默认 `python3 ./.trellis/scripts/get_context.py`。
- 官方脚本的默认模式在 `.trellis/scripts/common/session_context.py:435-445` 调用 `get_active_journal_file()` 并读取 journal 行数，在 `:621-644` 输出 active journal、line count 和 workspace path。现场运行也实际输出了 `## JOURNAL FILE` 与 `Workspace: .trellis/workspace/wumengye/`。
- 影响：新安装 repo 即使把 workspace gitignore，Guru Team 启动/context 路径仍会枚举本机 journal 并把其 path/size 注入 AI context；当前 scope 的 non-read 合同没有完成，且 workflow 的 durable 声明与运行行为相反。
- 需要：不修改官方 upstream 的前提下，为 Guru Team 提供或选择不读取 journal/workspace 的 context 路径，并同步 canonical workflow、start/平台入口、preset/dogfood与 sentinel 测试；测试应在 workspace 含现有 journal 时证明 Guru Team context 不访问、不输出该目录。

### F-002 P2：recovery 没有把首次 `publish_inputs` 快照绑定到后续调用

- Live #97、`design.md` 与 durable workflow 要求任何中断保存同一 `repo/base/head/title/body/draft`，0-open 分支只用这些同一输入重试 create。
- `publish_recovery_command()` 在 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:8527-8553` 只保存 `--body-file` / `--body-artifact` 路径和可选 title/draft，不保存首次 body bytes、digest 或完整输入 artifact。recovery 再次进入 `cmd_publish_pr()` 时在 `:8870-8886` 重新读取当前文件并重新计算 title/draft，然后在 `:8938-8945` 创建一个新的 `publish_inputs`；0-open 分支在 `:9083-9087` 直接使用这些重新读取的值。
- 现场 probe 显示当前 `pr-body.md` SHA-256 为 `6cd188780a8f4a7bafb601508f5b2379d2e654766f9128468d0e5b7e6ab8f7dd`，但 recovery command 只含文件路径，完全不含该 digest。现有所谓 same-input 测试 `test_publish_pr_zero_open_single_retry_failure_keeps_summary_and_same_recovery_command` 在两次调用间不修改 body/title/draft，因此没有覆盖漂移。
- 影响：normal create 客户端失败后，只要 task-local body/readiness 或 task title/default draft 在恢复前改变，0-open recovery 就可能创建一个输入不同的 PR；1-open 竞态分支则可能复用按旧 body 创建的 PR，却把新 body 当作本次 recovery 的 `publish_inputs`，无法证明 AI-reviewed readiness 与实际远端 PR 一致。
- 需要：把首次发布输入或至少其严格 digest/字段快照写入可恢复的 task-local publish metadata，并在 PR query/create 前 fail closed 校验；0-open create 必须消费已保存的原输入。增加两次调用间篡改 body/title/draft 的负向测试，以及 1-open PR title/body/draft 不匹配的拒绝测试或等价远端一致性证明。

### F-003 P2：live #97 的 diff 计算失败降级合同未实现，规划与 durable docs 也漏承接

- Live #97 字段规则明确写明：无法计算 diff 时必须把两个 path 数组写成 `[]`，并在 `index.contract_changes[]` 记录原因。
- `finish_summary_git_path_snapshot()` 在 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:713-731` 对 `git diff` 或 initial `git ls-files --others` 非零直接抛出 `WorkflowError`，既不生成空安全集合，也不追加原因 fact。隔离 probe 稳定返回 `Could not calculate finish-summary changed paths.` / exit code 2。
- 批准版 `prd.md`、`design.md`、`implement.md` 和 durable workflow/data/companion specs 均没有把该 live 条款收敛成可执行合同，Phase 2 因而也没有对应测试。
- 影响：base ref 缺失、shallow/ref 异常或 Git 命令失败会在 task 已 archive 后中断 finish，无法产生 issue 承诺的 schema-valid initial summary，也没有专用 recovery evidence；这是 live scope、规划、代码、测试和 Docs SSOT 的一致性缺口。
- 需要：先在规划与 durable SSOT 明确失败原因 fact 的固定/受限结构和 normal/backfill行为，再实现确定性降级并补 initial/final 两条命令失败测试；若团队决定改为 fail closed，必须先显式修改 live #97 和重新取得 planning approval，不能用当前实现静默覆盖 issue 合同。

### F-004 P2：durable 全流程文档仍把 Guru Team finish 描述为 `add_session.py / workspace journal`

- `docs/requirements/README.md:14` 把 `docs/requirements/guru-team-trellis-flow.md` 列为对外演示的当前完整流程文档，不是历史 task artifact。
- 该文档仍在 `:18` 把 companion 责任写成 `archive/journal/publish`，在 `:77` 把 finish 写成 `archive task + journal + metadata commit`，在 `:353-359` 的主时序中执行 `add_session.py -> workspace journal`，在 `:375` 声称 dry-run 只是不写 journal，在 `:398` 把 workspace journal 列为 finish-work 产物，并在 `:412` 再次说明 finish-work 会 archive/journal。
- 影响：对外演示 SSOT 与本分支 canonical workflow、README、requirements-main、finish skill 和代码完全冲突；reviewer/采用方会被指引到已删除的写路径，`ssot_first` 的实现交接和 Phase 2 Docs SSOT pass 结论不成立。
- 需要：同步该文档的总图、finish/publish 时序、readiness表、artifact责任表与讲解主线，表达 initial/final finish-summary、protected path filter、marketplace verifier、query-first recovery及 workspace non-write/non-read；同时复核 `docs/requirements/README.md` 的 #97 closeout索引。

### F-005 P3：throwaway verifier 成功退出后残留 `.trellis/workflow.md.new`

- `verify-throwaway-install.sh:149` 只在 workflow preview 前检查 `.new/.bak`；随后 `:266-275` 删除旧 preview、运行 `trellis workflow ... --create-new` 生成 `.trellis/workflow.md.new`，再强制切换 workflow，但脚本未删除或在最后重新检查 sidecar。
- 现场运行脚本返回 `Verified throwaway Guru Team Trellis install`，随后仍可见 `<throwaway>/.trellis/workflow.md.new`；两轮 `trellis update --force` 还把该 sidecar带入 `.trellis/.backup-*`。这与实现交接“update/reapply 后无残留 `.new/.bak`”及仓库 upgrade/update 门禁不一致。
- 影响：开箱验证给出 false positive，并把未处理冲突预览遗留在安装验证目录；真实 update证据不能仅凭该脚本成功退出认定无漂移。
- 需要：在 forced switch 后明确处理 preview sidecar，并把最终递归无 `.new/.bak` 校验放在脚本末尾；补测试证明 preview/switch 与 update/reapply 都不会以残留 sidecar成功退出。

## 观察项

- 方案 A 的 raw path 排序去重、workspace/runtime过滤、两个 path 数组同源、固定 fact 唯一且不披露 path/basename/count，以及 schema/Python全 path fail-closed在成功获取 Git paths 时实现一致。
- normal/backfill schema与 Python validator 的字段、path、artifact存在性、PR URL、retrieval派生和条件分支总体一致；无 site-packages运行 `FinishSummaryContractTests` 为 `25 passed, 1 optional jsonschema skip`。
- query-first `0/1/>1` 分支、create single-attempt、race reuse、marketplace recovery只复用 passed evidence、summary-only commit/push/remote SHA主路径有测试覆盖；除 F-002 输入绑定外未发现新的状态机分支错误。
- `check-phase2-check.sh` 的普通 current-head模式在 work commit 后按预期报告 stale；Branch Review 使用的内部 `validate_phase2_check(..., allow_committed_head=True)` 对当前 HEAD返回 `errors=[]`，全部 committed非 metadata path均被 pre-commit `dirty_paths`覆盖。
- Live #97 body 当前代码块中的双引号呈现为 `&#34;`，部分 angle-bracket占位符被清空；合同文字仍可取证，但后续同步 issue时宜恢复可读 Markdown。

## 后续候选

- 无 scope 外 follow-up candidate；上述 5 项均属于 #97 当前 scope，不能下沉到 #98/#99/#100。

## Docs SSOT 判断

- 批准策略：`ssot_first`。
- 已一致：canonical workflow、`.trellis/workflow.md`、workflow/data/companion/preset specs、root/workflow/preset README、requirements-main、finish entries、schema、companion、preset与dogfood copies。
- 阻断：F-001 证明 durable workflow的 workspace non-read声明与实际 context入口不一致；F-003 证明 live issue的 diff失败合同未进入规划/durable docs；F-004 证明当前对外全流程文档未合并 task delta。因此 Docs SSOT reconciliation 未完成，Branch Review Gate不能通过。

## 部署与安全

- 完整 diff 不修改 GitHub Actions/其他 CI/CD、Dockerfile/Docker Compose、Kubernetes/Kustomize/Helm、数据库 schema/migration/seed/backfill入口或 Makefile；本次是本地 CLI/workflow/preset/schema/docs行为变更，不需要业务服务部署资产同步。
- 变更会影响 Guru Team workflow/preset安装、finish/publish metadata与本地 context读取行为，合并后采用方需重新选择 marketplace workflow并 reapply preset；真实 current-ref remote marketplace verifier仍必须在 PR create前执行。
- 对新增 diff与被删除 journal执行强特征 secret扫描，未发现 concrete credential、private key、数据库 URL或签名 URL。finish-summary成功路径的 protected path过滤不写入具体 workspace/runtime路径。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：`293 tests`，通过。
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：`33 tests`，通过。
- `PublishBoundaryTest + FinishSummaryContractTests`：`70 tests`，通过。
- `PYTHONPATH=... python3 -S -m unittest test_guru_team_trellis.FinishSummaryContractTests`：`25 passed, 1 optional jsonschema skip`。
- Python compile、canonical workflow/preset Bash syntax、仓库 JSON解析 `259`、`git diff --check`：通过。
- Planning approval `--allow-committed-head`、workspace boundary、commit message validator：通过；source checkout `main...origin/main` clean。
- Canonical/dogfood byte equality与 `check-dogfood-overlay-drift.sh`：通过；worktree本身无 `.new/.bak`。
- `git ls-files '.trellis/workspace/**'`：空；`origin/main...HEAD`保留3条预期 `D`。
- Fresh public marketplace init/preview/switch + current preset install：通过；finish/publish direct-entry guards通过。两轮 `trellis update --force` + preset reapply确认 schema/companion/config/ignore可恢复，但暴露 F-005 的 preview sidecar残留。
- 隔离负向 probe：Git diff失败直接抛错，确认 F-003；recovery command只携带 body path、不携带 SHA-256或冻结输入，确认 F-002。

## Liveness 与 reuse 判断

- `agent-assignment.json` 已记录本代理 `assigned`：event `evt-0037-2a0039efb6`，logical role和 reviewed HEAD匹配本轮。
- 本轮产生 current-scope findings，因此 `/root/issue97_branch_finding` 成为 finding owner，不得担任最终放行审查代理。
- 闭环应优先复用同一 technical agent作为 `问题闭环审查代理`，记录 `reuse-for-closure`并仅核验上述5项；若无法复用，必须按 workflow记录 fresh closure或replacement链。所有 finding闭环后仍需派发从未出现在 earlier review rounds中的 fresh `最终放行审查代理`。

## 结论

- Findings count：`5`（`P2 x4`, `P3 x1`）。
- Observations：`5`。
- Follow-up candidates：`0`。
- 结论：`FAIL / Branch Review Gate blocked`。当前 HEAD不得记录 passing review gate，不得进入 finish-work、push或PR发布；修复任一非 metadata项后必须回到Phase 2/check、重新commit，再由finding owner闭环并执行fresh final review。
