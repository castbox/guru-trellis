# Issue #105 Branch Review Round 19 Replacement 问题闭环审查报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/round19_closure_replacement_105`
- reuse_decision：`replace`
- predecessor：`/root/final_release_review_105_round18`
- predecessor_event：`evt-0228-67f417ed36`
- replacement 原因：前任 Round 19 运行被人工终止且未完成，其部分输出全部弃用
- reviewed_head：`46c7ee508ef648c71214ed68593af302d56b0dfe`
- base：`3dec302206783fe4ac1296066e9a1789c995d58b`
- findings_count：`0`
- 结论：`pass-for-closure-only`
- 限制：本身份仅负责 Round 18 finding 闭环，不得担任最终放行 reviewer

## 审查范围

独立只读复核了 Round 18 六项 P1、stale `managed_backups` P2、13 个提交合同、Phase 2 postcommit 覆盖、规划三件套、Docs SSOT、Issue Scope Ledger、安全与部署影响。

未修改文件，未运行 Guru Team recorder/gate，未 commit、push、创建 PR 或关闭 issue。

## Round 18 问题闭环

### P1-1：history rewrite ledger 可移植性

结论：已闭环。

- `agent-assignment.json` 中除 `history_rewrite_reanchor.mappings[].old` 审计映射外，不再使用 rewrite 前 SHA。
- 独立枚举得到 14 个结构化生命周期 HEAD，全部是当前 HEAD 的可达祖先。
- 18 份既有 raw review report 的 SHA-256 与 size 均和 assignment 记录一致。
- tree sequence digest 保持为 `49ffd792ddb48d41fd99e28e4a4ebcef01355d8a31f3351b3affac665aebc78d`。
- Phase 2 已在 `--no-local` fresh clone 中确认旧 `b900a3c...` 对象不存在时 assignment validator 仍通过。当前结构不依赖 reflog、悬空对象或本机 GC 保留状态。

### P1-2：ordinary archived exact recovery 的 plan authority

结论：已闭环。

- `cmd_finish_work()` 对所有 archived task 均先进入 `assert_archived_committed_workspace_boundary()`，不再按 task context 是否存在决定 plan 来源。
- boundary 从当前 HEAD 的 archive plan blob 读取；仅 incomplete move 才使用同一 commit 中的 active evidence-plan blob。
- exact archive transaction 下，working-tree plan 删除、篡改、invalid、symlink 且保留 context 的生产式用例均能仅凭 commit blob 完成恢复。
- nonexact 或 incomplete archive 仍保留严格 working-tree、lineage 与 blob continuity 门禁。

### P1-3：formal workflow expected digest

结论：已闭环。

- `FinishWorkEntrypointContractTest` 覆盖 12 个 canonical、overlay 与 dogfood 入口。
- 所有 dry-run 命令不要求既有 digest；所有 formal 命令都携带 `--expected-plan-digest`。
- canonical workflow 与 `.trellis/workflow.md` 逐字一致，不再存在主示例与后部合同分叉。

### P1-4：official move 前 tracked blob/mode 连续性

结论：已闭环。

`validate_closeout_pre_move_continuity()` 在调用官方 `task.py archive` 前验证：

- live archive month 和 immutable plan 一致；
- `after_archive` hook state 未漂移；
- 全部 `move_paths` 是真实 regular file；
- tracked Git object 只能是 `100644`/`100755` blob；
- working mode 与 Git mode 一致；
- working bytes 与 evidence commit blob 一致；
- index 为空；
- dirty、staged、untracked 集合精确符合 planned final output。

tracked content、symlink、mode、额外 untracked/staged 路径的生产式故障均在 move 前保持 task active、PR draft。

### P1-5：跨月归档 scope cap

结论：已按用户确认边界闭环。

- stale-month plan 在 official move 前失败，task 保持 active。
- 同一入口重新 dry-run 生成新 digest，formal 只追加 plan/readiness evidence commit。
- `git.evidence_parent_head` 绑定前任 evidence commit，并递归验证 predecessor plan/evidence lineage。
- verifier、draft PR 与既有远端事实被复用。
- 未迁移 archive 目录、未重写历史、未引入通用时间框架，符合用户确认的 scope cap。

### P1-6：`after_archive` hook

结论：已按用户确认边界闭环。

- prepare 使用 installed official `parse_simple_yaml` 解析 `.trellis/config.yaml`。
- missing 或 empty `hooks.after_archive` 映射为固定 `{"commands":[]}` 并绑定 digest。
- non-empty、歧义、不可解析、NUL、symlink/dangling config 均在 push、PR、archive 前失败。
- pre-move 再次检查 hook state。
- 生产式 sentinel 测试确认被拒绝的 hook 没有执行，也没有进入分析或 transaction allowlist。

## stale managed_backups P2

结论：已闭环，未发现 installer 缺陷。

- 当前 manifest：71 个排序唯一且实际存在的 managed assets。
- `selected_platforms=[claude,codex,cursor]`，`all_platforms=true`。
- `managed_backups=[]`、`new_copies=[]`，仓库内 `.new/.bak` 为 0。
- preset suite 36/36 通过，overlay drift 检查通过。
- Phase 2 的临时仓库连续 apply 与 throwaway update/reapply 均未复现 stale backup；原问题与先前手工清理 `.bak` 后未重跑 preset 的状态一致。

## 验证证据

- canonical suite：411/411，`OK`
- preset suite：36/36，`OK`
- Python compile：通过
- `git diff --check`：通过
- overlay drift：通过
- canonical/dogfood Python、workflow、closeout schema、config template：一致
- 13 个提交均包含 `背景/变更/边界/验证/Refs #105`
- Phase 2 `dirty_paths` 共 28 项，与 `d8bde83..46c7ee5` 的 28 个提交路径集合和 digest 精确相等
- 当前无 non-metadata working-tree drift；仅 task metadata 与 raw review reports 未提交

## Docs SSOT

结论：通过。

`prd.md`、`design.md`、`implement.md` 已明确记录：

- commit-blob plan authority；
- formal digest handshake；
- pre-move blob/mode 门禁；
- active plan supersession，不迁移目录、不引入时间框架；
- `after_archive` unsupported-by-contract，只做 preflight rejection。

canonical workflow、dogfood、preset overlay、README、requirements 与 durable specs 对上述边界一致，未发现当前范围的 Docs SSOT 冲突。

## Ledger 与范围

分类正确且验收证据充分：

- close：`[105]`
- related：`[53,96,97,100]`
- follow-up：`[98,99,101]`

未把 related 或 follow-up issue 错误纳入关闭范围。

## 安全与部署

- 未修改 CI/CD、Docker、Compose、K8s/Kustomize、Helm、migration 或 Makefile。
- 未发现真实 token、secret、private key、`.env`、数据库 URL、客户数据或签名 URL。
- credential/userinfo 字符串仅存在于拒绝测试 fixture。
- 本次影响限于 Trellis workflow、preset、companion closeout、schema、平台入口与文档，不要求应用部署或数据迁移。

## 观察项

- 远端不存在 `v0.6.5-guru.3`，不得声称 stable-tag 安装已验证。
- 远端尚无 `fix/105-finish-work-closeout-transaction` 分支。
- current-branch remote marketplace 与真实 GitHub E2E 仍须由 publish-time fail-closed verifier 完成。
- manifest 的 `source.commit=d8bde83` 是最后一次 apply 的安装来源记录，不是当前 HEAD containment 声明。

## 后续候选

0。Round 18 六项 finding 已全部关闭；本轮未发现新增当前范围问题。

## 结论

Round 19 replacement closure：通过。

- P0：`0`
- P1：`0`
- P2：`0`
- P3：`0`
- findings_count：`0`
- reuse_decision：`replace`
- closure_status：`pass`

下一步必须派发一个从未参与前序 round 的 fresh `最终放行审查代理`，对 `base...46c7ee5` 完整 diff 做最终独立审查；本 replacement closure 身份不得复用为最终 reviewer。
