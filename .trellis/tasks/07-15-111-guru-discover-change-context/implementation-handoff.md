# #111 `guru-discover-change-context` 实现交接

## 1. 当前状态

- 当前实现 owner：`/root/issue111_impl_eighth_chain`（第九轮续接，逻辑角色仍为
  实现代理）。本代理从已落盘的第八轮实现继续，重新读取 live task、官方 Trellis
  文档、Docs SSOT、schema、runtime、workflow、validator 与 throwaway diff；无法恢复的
  旧 throwaway session 不作为通过证据，而是重新运行带 `pipefail` 的完整验收并取得
  明确退出码。
- Docs SSOT strategy：`ssot_first`。
- 当前结论：首轮 Phase 2 的 7 项 finding、第二轮 5 项 finding、第三轮 2 项、
  第四轮 2 项、第五轮 3 项、第六轮 3 项、第七轮 1 项、第八轮 1 项与第九轮 2 项
  P1 finding 均已完成修订；第五轮恢复审计另发现并修复单段未知 POSIX 绝对路径
  漏检。第九轮复核未发现新的实现缺口；dogfood 同步、全仓测试与 throwaway 验证
  已 fresh 通过，可交给独立
  `trellis-check` 执行 fresh Phase 2 语义复核；
  本文不是 `phase2-check.json`，不声明 Phase 2、Branch Review 或发布门禁通过。
- 当前边界：未 commit、未 push、未创建 PR、未归档 task，也未运行主会话
  recorder。
- Implementation finalizer status：`completed`；下一步是新的独立 Phase 2 checker，
  不是由本实现代理自证通过。

## 2. Docs SSOT Reconciliation

实现前先把 task delta 合并到以下 durable sources，再以其作为代码、schema、
workflow、preset 与测试的 primary input：

- `docs/requirements/README.md`
- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `.trellis/spec/workflow/index.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `.trellis/spec/preset/upstream-ownership.md`
- `.trellis/spec/docs/public-docs.md`
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`

已合并的长期合同包括：current-before-history 固定顺序、workflow/standalone
precondition parity、freshness/re-entry、score v1、query/manifest/preview digest、
invalid isolation、selected-task deep-read、mem gate、same-snapshot persistence、三个
typed exits、no-workspace/no-cache 边界，以及 canonical/installed/platform/update
分发规则。Durable docs、package contract、interface、schema、runtime 和 tests 使用
同一组 stable ids 与行为定义，没有另建 inline workflow SSOT。

第三轮 `ssot_first` checkpoint 先在 `skill-package-contract.md`、
`data-contracts.md`、`companion-scripts.md`、`public-docs.md`、durable requirements 与
三个 public README 定义两项增量：direct active task mode 在 unchanged snapshot HEAD
上绑定 `task.json.branch`，pre-task/standalone 继续绑定 decision branch；zero candidate
固定 empty selected/excluded/deep-read evidence 与一致的 `mem_review=not_needed` shape，
禁止进入 mem 或其它历史源。随后才更新 package contract、schema、runtime 与 tests。

第四轮 `ssot_first` checkpoint 先在 `data-contracts.md`、
`companion-scripts.md`、`skill-package-contract.md`、durable requirements 与三个 public
README 定义两项增量：reviewed Git evidence 必须解析为 exact `blob` object；作为发现
源输入的 live issue 可为 `open` 或 `closed`，但 draft-created `issue_binding` 与 duplicate
candidate 继续只允许 `open`。随后才更新 package contract、schema、runtime 与 tests。

第五轮 `ssot_first` checkpoint 先把三项 P1 修订写入 `workflow-contract.md`、
`data-contracts.md`、`companion-scripts.md`、`skill-package-contract.md`、preset/docs specs、
durable requirements 与三个 public README：deep-read 必须按 task artifact / canonical
GitHub issue-or-PR / exact Git object-or-ref 使用 closed source-specific locator union，且
全 payload 拒绝 POSIX/Windows/UNC/home/temp machine-local path 与 AWS/GCS/Azure/generic
signed-query credential；`task_branch_stale` 是可验证的 `refresh_base` stale code；
`guru-clarify-requirements` 是现有 Phase 0 workflow continuation，不是尚未实现的 #113
active Skill。随后才更新 schema/interface/runtime、workflow target markers、validators 与
tests，已批准 planning 三文件保持 byte-identical。

第六轮 `ssot_first` checkpoint 已在 `workflow-contract.md`、`data-contracts.md`、
`companion-scripts.md`、`skill-package-contract.md`、durable requirements 与三个 public
README 中定义三项增量：recorder/checker 必须先执行 pure structural/schema/digest/
security gate，再执行 base-only live gate，只有 fresh base 才能读取 repo-bound locator、
live issue、reviewed blob 与 archive/history；`change_input` 十组 clue arrays 至少一组非空
且 workflow/standalone 完全一致，`issue_binding` 与 `canonical_query` 不得替代 entry
clue；portable scan 只豁免完整 slash-command span，同时继续拒绝真实 POSIX、Windows、
UNC 与 signed-query credential。随后才更新 schema/runtime/tests；本 replacement 逐项复核
已落盘 diff，没有进一步放宽安全边界，已批准 planning 三文件仍保持 byte-identical。

第九轮 `ssot_first` checkpoint 已在 `workflow-contract.md`、`data-contracts.md`、
`companion-scripts.md`、`skill-package-contract.md`、`quality-guidelines.md`、
`public-docs.md`、durable requirements 与三个 public README 中定义两项增量：长度为
`N` 的 refresh history 除 `N` 个 oldest-to-direct-prior `context_ready` ancestors 外，还
必须提供 `N-1` 个独立保留的 prior `refresh_base` receipts，逐 hop 证明前一 ancestor
的唯一 append projection 与下一 ancestor history prefix；所有 task-local recorder/checker
必须以 `git check-ignore --quiet --no-index -- <target>` 证明精确 artifact target 不受
repository、`.git/info/exclude` 或 `core.excludesFile` 影响。随后才同步 package/interface、
runtime、tests、throwaway 与 dogfood copies；artifact schema 未增加 receipt 字段，已批准
planning 三文件仍保持 byte-identical。

## 3. 实现结果

- 新增 active semantic package `guru-discover-change-context`，包含短 `SKILL.md`、
  `references/contract.md`、interface 1.2、`guru-context-discovery-1.0` schema、
  去身份化 example、三个 dispatcher-only wrappers 与 package tests。
- Registry、extension manifest 和 runtime public API 已发布三个 companion commands：
  `preview-change-context-history`、`record-context-discovery`、
  `check-context-discovery`；extension version 更新为 `0.6.5-guru.10`。
- Canonical workflow 在 `guru-sync-base:synced` 后 mandatory invoke新 Skill，并唯一
  消费 `context_ready`、`refresh_base`、`blocked`；`guru-sync-base:synced` 的
  consumer 已由 workflow inline route 改为 skill consumer。
- Runtime 实现 canonical query、NFKC/casefold/tokenization、固定 exact/token score、
  index-only archive manifest、stable digests、invalid isolation、稳定排序/limit、
  stdout-only pre-task recorder、task-local same-snapshot recorder/check 和 live
  base/issue/draft/blob/archive freshness。
- Runtime fail-closed 加固包括：移除 `--no-live-check` 绕过；archive root symlink
  拒绝；`context_ready` 强制 Docs/code/tests 三组均有证据；preview/selection/
  duplicate identity 与 digest shape 检查；task artifact deep-read 必须位于所选
  archived task 且为逐组件 non-symlink regular file。
- Revision 加固包括：实际执行 published Draft 2020-12 result schema；只接受 direct
  active `planning` / `in_progress` task；写入后重新读取 exact bytes 并复核
  identity/structural/live freshness；按 `base_evidence.remote` 绑定 selected remote；
  任一 base error 在读取 live change/blob/archive 前短路；拒绝 macOS/Linux home path、
  GitHub/Bearer token、private key 与 database URL；archive walker 把 symlink/unreadable
  subtree 记录为 portable invalid row。
- 第二轮 Revision 加固把完整 `guru-base-sync-result-1.0` 嵌入 discovery evidence，
  复核 sync facts/post-sync digest、decision branch、remote refs 与 HEAD projection；
  `refresh_base` 绑定实际 live stale codes；draft-created issue 绑定 live repo/number/
  URL/state/body digest；recorder 用 `lexists`/`lstat` 拒绝 dangling symlink、目录、FIFO
  和不同 regular bytes；used mem 与 passed AI Gate 都要求非空 semantic evidence。
- 第三轮 Revision 保留 pre-task snapshot 内完整 base-sync provenance 与 decision branch，
  但 direct active task recorder/checker 改为复核 live branch 等于 `task.json.branch`；
  unchanged HEAD、selected local/remote base refs、strict repository identity、task
  status/locator 与 task-local-only dirty scope 继续 fail closed。Schema/runtime 同时把
  zero candidate 收紧为 empty selection/deep reads 与 exact `not_needed` mem shape；
  candidate-present 的既有四源 insufficiency mem gate 不变。
- 第四轮 Revision 先解析 `HEAD:<path>` 并核对 expected OID，再用 `git cat-file -t`
  强制 reviewed Git evidence 的 object type 为 exact `blob`；tree、gitlink commit、missing
  object 和 OID mismatch 均返回 `reviewed_blob_stale`，既有 64-character content SHA
  freshness 行为不变。Runtime 同时把 GitHub issue state 规范化为 `open|closed`：source
  live issue 接受二者，draft-created binding 与 duplicate candidate 仍保持 open-only。
- 第五轮 Revision 把 `deep_reads[]` 收敛为三分支 closed union：task artifact 必须在所选
  archived task 内且为 non-symlink regular file；GitHub 只接受无 query/fragment 的
  canonical issue/PR URL；Git 只接受 `git:object:<40-oid>` 或
  `git:ref:<full-ref>@<40-oid>` 并验证 live object/ref。底层 Git locator probe 的
  `OSError` 只返回固定非泄露错误码。全 payload string scan 同时覆盖任意嵌套字段，
  包括 `/workspace`、`/custom` 这类单段未知 POSIX 绝对路径；普通 URL、repo-relative
  path、exact Git locator 与 `/trellis:continue` 不被误拒。
- 第五轮把 `task_branch_stale` 加入 refreshable live errors，并在真实 feature worktree
  中证明 recorder/checker 可持久化同一 `refresh_base` snapshot；`invalid_task_branch`
  等 malformed task facts 仍返回 `refresh_base_has_non_refreshable_error`。
- 第五轮 source/installed validator 新增 active Skill consumer resolution 与唯一
  workflow/stop target resolution。Canonical/dogfood workflow 声明 6 个 target markers；
  `context_ready` 唯一映射到现有 `workflow:guru-clarify-requirements` continuation，未实现
  #113。Missing、multiple、kind mismatch、dangling target 全部 fail closed。
- Installer recovery 同时修复 known managed upgrade 的可恢复 provenance：只有
  `conflicts=[]` 且全部 declared sidecar 是绑定当前 managed file 的 `.bak` 时，重复
  apply 才能保留 backup gate；全部 backup 清理后下一次 apply 转为 `status=ok`。
  `.new`、unknown edit、异常路径和真实 conflict 继续 fail closed。
- Preset installer 已纳入 canonical/installed/shared/Codex/Cursor/Claude package、
  runtime commands 与 executable inventory。Canonical 与 dogfood workflow 字节一致；
  installed manifest 为 `status=ok`，三个 active skills、9 个 exit markers、128 个
  managed Skill files、0 conflict、0 sidecar。
- Transitional legacy overlay payload 和 43 条 frozen ownership baseline 均未修改；
  新 package 只使用既有 `guru_owned` namespace。
- 第九轮把多轮 refresh 的 trust chain 扩展为 ancestors + independent receipts：每份
  receipt 单独校验 closed shape、`typed_exit=refresh_base`、expected digest、唯一 append
  projection 与 next-ancestor prefix；current candidate 继续只能是 direct prior 的单步
  projection。所有外部 ancestor/receipt 文件在 task 写后重新读取，任一漂移统一返回
  `prior_snapshot_changed_during_record`，且 external bytes 不进入 artifact。
- 第九轮为 task-local recorder 写前/写后及 checker 的所有 task invocation 增加 Git
  trackability gate，覆盖 `.gitignore`、`.git/info/exclude`、global excludes 与 already-tracked
  target；稳定错误为 `context_discovery_target_ignored` 和
  `context_discovery_target_trackability_unreadable`。Pre-task stdout-only mode 不执行该门禁，
  既有 regular-file、symlink、idempotency 合同保持不变。

## 4. Phase 2 Finding 修订闭环

### 首轮 7 项

| Finding | 修订 | Fresh regression |
| --- | --- | --- |
| P1 closed schema 未执行 | `context_structural_errors` 加载并执行 `guru-context-discovery-1.0`；共享 validator 补齐本 schema 使用的 Draft 2020-12 keywords、union type、format 与 limits | `test_published_schema_rejects_47_closed_shape_const_and_format_errors` |
| P1 recorder 可写 archived/completed task | `context_active_task_dir` 只允许 `.trellis/tasks/<direct-task>` 且 status 为 `planning` / `in_progress` | `test_task_recorder_rejects_archived_and_non_active_tasks` |
| P1 写后未复核 | recorder 写后 `lstat`、读取 exact bytes、解析 JSON、复核 snapshot identity，并重跑 structural/live freshness | `test_task_recorder_detects_post_write_tamper_before_success` |
| P2 remote hard-coded `origin` | result schema/example 增加 `base_evidence.remote`，live check 使用 `refs/remotes/<remote>/<base>`；throwaway 从 validator-passed sync result 承接 remote/HEAD/clean/digest | `test_live_base_uses_selected_upstream_remote` + throwaway sync/discovery |
| P1 stale base 未短路 | `context_live_errors` 在任一 base error 后立即返回，不读取 live change、reviewed blobs 或 archive preview | `test_stale_base_short_circuits_all_later_live_reads` |
| P1 portable/secret scan 不完整 | 增加 `/home`、GitHub token、Bearer token、database URL 与 private-key 检测 | `test_structural_gate_rejects_home_token_bearer_and_database_secrets` |
| P1 archive subtree 被静默跳过 | 用逐目录 `os.scandir` + component `lstat` walker 替换 `os.walk`，symlink/unreadable subtree 形成排序稳定的 invalid row | `test_preview_isolates_symlinked_and_unreadable_archive_subtrees` |

上述修订没有把 AI relevance/sufficiency/finding/route 判断下沉到脚本；recorder 和
validator 仍只校验 AI 已提供的结构化结论与 live deterministic facts。

### 第二轮 5 项

| Finding | 修订 | Fresh regression |
| --- | --- | --- |
| P1 base evidence 可伪造 | `base_evidence.sync_result` 执行完整 sync schema、facts/post-sync digest、remote repository、decision branch、selected refs 与 HEAD projection 复核；`snapshot_identity` 增加两个 sync digest | `test_live_base_rejects_forged_full_provenance_and_git_status_failure` |
| P1 `refresh_base` 不是可验证出口 | `refresh_history[].error_codes` 必须等于 stable live stale codes；recorder/checker 只验证调用方选择的 route，stale evidence 不得返回 `context_ready` | `test_refresh_base_record_and_check_require_matching_live_stale_evidence` |
| P1 draft issue 未绑定 live body | draft 带 created issue ref 时执行 live `gh issue view`，绑定 repo/number/url/state/time/body/facts digest，live body digest 必须等于 reviewed draft body digest | `test_draft_issue_binding_reads_live_body_and_rejects_mismatch_or_missing` |
| P1 recorder existing target 可绕过 | 用 `os.path.lexists` + `lstat` 区分 missing、dangling symlink、目录、FIFO 与 regular file；只有 exact bytes regular file 可幂等 | `test_task_recorder_rejects_dangling_symlink_directory_and_fifo_targets` |
| P2 semantic evidence 可为空 | `mem_review.status=used` 要求非空 summary；passed Gate 要求非空 `reviewed_scope` 与 `load_bearing_conclusions`；schema/runtime 都只做结构校验 | `test_structural_gate_enforces_order_selection_mem_and_snapshot` |

第二轮仍保持 semantic profile：脚本不生成 stale route、mem necessity、scope、finding、
sufficiency 或 pass 结论，只验证 AI 已形成的选择和 evidence。

### 第三轮 2 项

| Finding | 修订 | Fresh regression |
| --- | --- | --- |
| P1 feature-worktree task mode 被 pre-task decision branch 阻塞 | `context_live_base_errors` 在 pre-task/standalone 继续绑定 `decision_checkout.branch`；direct active task mode 重新验证 task locator/status，并绑定 `task.json.branch`，同时保留 same HEAD、完整 sync provenance、selected refs、repo identity 与 task-local dirty scope | `test_feature_worktree_task_mode_records_same_snapshot_and_rejects_drift` 使用真实 `git worktree add -b`，覆盖 positive record/check 及 wrong HEAD/remote ref/repo/non-task dirty/task branch negative |
| P1 zero candidate 仍可进入 mem | Draft 2020-12 schema 增加 zero-candidate conditional，runtime 增加 stable zero/mem shape errors；`not_needed` 固定 null question/summary 与四个 false source flags，candidate-present `used` gate 保持四源 true + non-empty question/summary | `test_zero_candidate_schema_and_runtime_require_not_needed_mem_shape` + candidate-present mem regression + throwaway installed negative cases |

第三轮没有改变 AI 对 candidate selection、mem necessity、sufficiency 或 Gate pass 的
所有权；schema/runtime 只校验 live issue #111 已明确的零候选 no-other-history-source 与
task/worktree Git 事实。

### 第四轮 2 项

| Finding | 修订 | Fresh regression |
| --- | --- | --- |
| P1 reviewed Git path 未约束 object type | `context_reviewed_blob_errors` 解析 `HEAD:<path>`、核对 expected OID，并以 `git cat-file -t <oid>` 要求 exact `blob`；tree、gitlink commit、missing object 与 OID mismatch 统一 fail closed | `test_reviewed_git_evidence_requires_blob_object_type` 使用真实 repo 覆盖 Docs/code/tests 三组的 file-blob positive 与 tree/gitlink negative |
| P1 closed source issue 被错误拒绝 | live source issue state 规范化并只接受 `open|closed`；schema 放行 source issue 的二态，draft-created binding 保持 open-only，duplicate candidate 明确只允许 `state: open` | `test_closed_source_issue_passes_and_closed_duplicate_is_rejected` + throwaway installed source/duplicate assertions |

第四轮只增加 Git object type 与 GitHub issue state 的 deterministic freshness/shape
校验，没有把 source relevance、duplicate 判断、candidate selection 或 route intent 下沉
到脚本。

### 第五轮 3 项

| Finding | 修订 | Fresh regression |
| --- | --- | --- |
| P1 deep-read 与全 payload portable/security gate 可接受 signed URL 和任意本机绝对路径 | Schema 使用 task/GitHub/Git closed locator union；runtime 验证 selected task boundary、canonical GitHub URL、live Git object/ref，并全量扫描 machine-local path 与 AWS/GCS/Azure/generic signed-query credential | `test_candidate_selection_requires_one_to_three_and_deep_read` + `test_structural_gate_rejects_machine_paths_tokens_and_signed_credentials` + clean throwaway installed positives/negatives |
| P1 `task_branch_stale` 被错误判为 non-refreshable | 加入 `CONTEXT_REFRESHABLE_LIVE_ERRORS`，但保持 malformed task errors 非 refreshable | `test_feature_worktree_task_mode_records_same_snapshot_and_rejects_drift` + clean throwaway recorder/checker refresh 与 `invalid_task_branch` negative |
| P1 `context_ready` 指向不存在的 Skill 且 validator 不验证 consumer | `context_ready` 改为 `workflow:guru-clarify-requirements`；workflow/stop target markers 显式声明，source/installed validator 验证 active Skill 或唯一同 kind target | `test_consumer_targets_require_unique_matching_declarations`、`test_skill_consumer_must_resolve_to_active_registry_entry`、`test_installed_validator_requires_unique_matching_consumer_targets` |

第五轮仍遵守 AI/script boundary：locator、Git/object freshness、portable payload、target
resolution 与 stale-code matching 是确定性校验；duplicate reuse、新 issue、relevance、
sufficiency、candidate selection、finding、Gate pass 与 route intent 仍由 semantic Skill/
workflow AI 拥有。

### 第五轮 stale replacement 恢复审计

前任的第五轮 diff 已逐项重新审阅；三项 P1 主合同均保持闭合。恢复审计额外发现
whole-payload gate 只拒绝多段路径和已知根目录，未知单段 POSIX absolute path（例如
`/workspace`）仍可漏过。Runtime 新增 generic POSIX absolute token 检测并显式保留
slash-command allowlist；canonical regression 与 clean throwaway 同时加入
`/workspace`、`/custom` negatives，以及普通 HTTPS、repo-relative、exact Git locator 和
`/trellis:continue` positives。该补修没有改变 AI judgment ownership，也没有修改已批准
planning 三文件。

### 第六轮 3 项

| Finding | 修订 | Fresh regression |
| --- | --- | --- |
| P1 stale base 的 recorder/checker 生产入口仍可能触碰 repo-bound evidence | recorder/checker 与写后复核固定执行 structural/schema/digest/security -> base-only live gate -> fresh-only locator/issue/blob/history；base stale 时仅校验 caller-authored `refresh_base` identity、stable codes 与 superseded digests | `test_recorder_and_checker_short_circuit_repo_reads_at_the_production_entry` 使用真实 repo 同时追踪 recorder/checker，stale 时 archive/Git locator/live issue/reviewed blob/history preview 五组读取计数均为 0，fresh 时均实际读取 |
| P1 `change_input` entry clue 可被空数组或下游 projection 冒充 | published schema 对十组 closed clue arrays 使用 `anyOf + minItems`；runtime 单独执行 `change_input_has_no_clues`，workflow/standalone 使用相同 gate，`issue_binding` 与非空 `canonical_query` 不计入 entry clue | `test_change_input_requires_one_real_clue_in_schema_and_runtime` + package schema regression 覆盖十组 single-clue positives、双 mode empty negatives 与 binding/query masquerade negative |
| P1 slash-command portability 修订可能放过真实本机路径或误拒 Markdown/中文文本 | whole-payload scan 仅移除边界完整的 `/<namespace>:<command>` span；URL/signed-query 先独立扫描，span 外的 POSIX/Windows/UNC/home path 仍 fail closed | `test_slash_command_spans_are_portable_without_weakening_path_rejection` 覆盖裸文本、inline code、bold、英文句中、中文标点 positives，以及 POSIX、Windows drive、UNC、home、signed URL 与 slash-command-plus-path negatives |

第六轮保持 semantic ownership 不变：脚本没有生成 clue、判断 relevance/sufficiency、
选择历史候选、决定 mem、形成 finding 或替 AI Gate/route 作结论。pure structural/security/
digest 与 live freshness 仍是 fail-closed deterministic validation；stale short-circuit 只是
阻止读取已无效 snapshot 的下游证据，不会把 malformed/non-refreshable error 降级为
`refresh_base`。

### 第七轮 1 项

| Finding | 修订 | Fresh regression |
| --- | --- | --- |
| P1 `refresh_history[-1].superseded_snapshot_sha256` 只受当前新 snapshot self-hash 约束，可改为任意 64hex 后重算 identity | `refresh_base` 的 recorder/checker 增加成对外部证据 `--prior-snapshot-input` 与 `--expected-prior-snapshot-sha256`；pure gate 重算 prior `context_ready` identity，绑定 superseded query/snapshot digests，并要求当前 payload 只能由 prior 的完整对象 append 一条 refresh entry、切换 typed exit、重算新 identity 得到。Prior bytes 不进入新 artifact；task 写后再次读取同一外部证据。多轮 refresh 只允许 freshly re-entered `context_ready` 携带旧 entries 后顺序 append 一条，禁止改写、重排或跳过。 | `test_refresh_binding_requires_real_prior_snapshot_at_production_entries` 同时覆盖 record/check real-prior positive、all-f tamper + 重算 current identity、missing/wrong/stale prior negative、pure gate 的 0 live read 与两轮顺序 append；既有 feature-worktree 与 production short-circuit 回归继续通过。Clean installed throwaway 同时执行 tampered record/check negative 与真实 prior refresh positive。 |

第七轮只增加确定性的 pre-refresh evidence/identity/projection gate，不生成 stale code、
route intent 或 semantic 结论。该 gate 位于 base-only live gate 前，因此既能阻止 self-hash
伪造，也不会在 stale base 上触发 archive、Git locator、GitHub issue、reviewed blob 或
history preview。Durable Docs、public README、canonical package/interface、runtime CLI、
installed copies 和 throwaway 使用同一参数与 freshness 合同；已批准 planning 三文件未改。

### 第八轮 1 项

| Finding | 修订 | Fresh regression |
| --- | --- | --- |
| P1 多轮 refresh 只绑定 direct prior，无法从外部证据证明更早的 `refresh_history` entry 没有被改写、跳过或替换为 non-parent snapshot | 保留公共参数名并改为 repeatable pairs：每条 `refresh_history` 必须按 oldest `context_ready` ancestor 到 direct prior 的顺序提供一对 `--prior-snapshot-input` / `--expected-prior-snapshot-sha256`。Pure gate 校验 chain/pair 数量、每层 structural/context-ready identity、独立 expected digest、snapshot 唯一性、history length/prefix、逐层 superseded query/snapshot link，以及 current 相对 direct prior 的唯一单步 projection；missing、duplicate、wrong order、skip、rewrite 与 non-parent 全部 fail closed。Ancestor bytes 仍不写入 task artifact；task 写后重新读取完整链，任一外部证据漂移返回 `prior_snapshot_changed_during_record`。 | `test_refresh_binding_requires_real_prior_snapshot_at_production_entries` 覆盖完整两层 positive、missing/duplicate/wrong-order/rewrite/skip/non-parent 与写后 ancestor drift。Clean throwaway 使用 production recorder/checker 覆盖完整 repeatable pair positive，以及 missing、wrong-order、rewrite、skip negatives；fixture 同时保证各独立 task 只暴露声明的 live stale code。 |

第八轮只加强确定性的完整 ancestry identity、顺序、parent link 与 freshness 校验，不持久化
ancestor payload，也不生成 stale code、选择 route 或替代 semantic Gate。Artifact schema
没有增加 ancestry 字段；公共 CLI 参数保持兼容，单次 refresh 的原单对调用不变。

### 第九轮 2 项

| Finding | 修订 | Fresh regression |
| --- | --- | --- |
| P1 多轮 ancestor chain 仍可由当前 candidate 自行重建，缺少上一轮 production `refresh_base` 结果作为独立信任锚 | 新增 repeatable `--prior-refresh-receipt-input` / `--expected-prior-refresh-receipt-sha256`；长度为 `N` 的 history 必须提供 `N-1` 个 oldest-to-newest receipts。每份 receipt 必须是前一 `context_ready` ancestor append 对应完整 entry 后的唯一 canonical projection，其 history 必须与下一 ancestor prefix 完全相等；receipt bytes/digest 独立校验、task 写后重读，且不持久化到 artifact。`N=1` 保持原单 ancestor pair CLI 兼容。 | `test_refresh_binding_requires_real_prior_snapshot_at_production_entries` 扩展 prior0 -> receipt0 -> context_ready1 -> receipt1 -> context_ready2 -> current refresh，覆盖 missing、wrong order、digest/projection/history-prefix mismatch、ancestor/current rewrite 与 ancestor/receipt post-write drift；throwaway installed production path覆盖两份 receipts positive 和 receipt negatives。 |
| P1 task-local `context-discovery.json` 可能被 `.gitignore`、`.git/info/exclude` 或 global excludes 忽略，无法满足“必须被 Git 跟踪并随 task archive”的合同 | Recorder 在写前和写后、checker 在所有 task-local invocation 执行 `git check-ignore --quiet --no-index -- <repo-relative-target>`；`--no-index` 保证 already-tracked target 也按当前 ignore rules 检查。Ignore match 与 unreadable Git check 分别返回稳定错误码，pre-task stdout-only 不执行该 gate。 | `ChangeContextDiscoveryTests` 覆盖 repository ignore、info exclude、`core.excludesFile`、already-tracked、recorder 写后规则漂移、checker `--input + --task` 与规则清除后的恢复；throwaway installed path执行 ignore negative。 |

第九轮只记录/校验外部 evidence identity、projection、文件 freshness 与 Git trackability
事实；receipt 不能由当前 candidate 自授权，脚本也没有生成 route、finding、sufficiency 或
AI Gate 结论。两项修订保持 `judgment_mode=semantic`、artifact schema 与单轮 CLI 兼容。

## 5. 变更文件与分发范围

- Canonical Skill package：
  `trellis/skills/guru-team/packages/guru-discover-change-context/**`、registry、interface
  schema 和 `guru-sync-base` exit consumer。
- Canonical workflow/runtime：`trellis/workflows/guru-team/workflow.md`、三个 discovery
  wrappers、`guru_team_trellis.py` 及 runtime regression tests。
- Preset 与安装验收：extension manifest、preset installer/tests、ownership tests、
  `verify-throwaway-install.sh` 和 preset/workflow README。
- Durable Docs SSOT：`docs/requirements/**`、`.trellis/spec/workflow/**`、
  `.trellis/spec/preset/**`、`.trellis/spec/docs/public-docs.md` 与 root `README.md`。
- Dogfood installed copies：`.trellis/workflow.md`、`.trellis/guru-team/**`、shared、
  Codex、Cursor、Claude Skill package copies；all-platform apply 负责 managed hash 与
  executable mode。
- Task-local evidence：当前 task 的 planning、assignment、JSONL 与本 handoff。Finding
  修订没有修改已批准的 `prd.md`、`design.md`、`implement.md`，planning digest 仍 fresh。

## 6. Task-History-Only 内容

以下内容只保留在 task 目录，不进入公共 package、marketplace、preset 或 durable
contract：

- #111 intake、规划确认、agent assignment 与本轮执行流水；
- 历史候选 #120、#110、#97 的选择/排除理由及当前 task 的 evidence 判断；
- 本地 throwaway 临时仓库、模拟 issue/PR、临时 Git SHA 与运行时间；
- 本文中的一次性验证计数和未发布分支状态。

## 7. Fresh 验证证据

- 全仓 pytest 使用 `PYTHONDONTWRITEBYTECODE=1` 与
  `--import-mode=importlib -p no:cacheprovider` 隔离同名 package tests 与缓存副作用：
  `606/606` passed，耗时 183.51 秒。
- 受影响完整矩阵 fresh `595/595` passed：`guru-discover-change-context` package `5`、
  shared package/distribution validator `71`、canonical runtime `474`、preset installer
  `39`、upstream ownership `6`。当前 `ChangeContextDiscoveryTests` 共 30 个 case，新增
  receipt chain 与 Git trackability positives/negatives 均包含在全仓和受影响矩阵中。
- 第九轮回归覆盖 prior0 -> receipt0 -> context_ready1 -> receipt1 -> context_ready2 ->
  current refresh、两份 receipts wrong-order/missing/digest/projection/history-prefix mismatch、
  ancestor/receipt post-write drift，以及 `.gitignore`、`.git/info/exclude`、
  `core.excludesFile`、already-tracked、checker `--input + --task` 与 ignore 清除恢复。
- Source Skill validator passed：active ids 为 `guru-create-task-commit`、
  `guru-discover-change-context`、`guru-sync-base`，invoke/exit/target markers 为 `3/9/6`。
  Installed validator passed：Claude/Codex/Cursor，128 managed files，markers `3/9/6`，
  0 conflict、0 sidecar、0 removal。
- Canonical all-platform idempotent reapply：128 个 managed Skill files 全部 unchanged，
  `installed/new/updated/backup/conflict/sidecar` 均为空。Canonical/dogfood workflow、
  runtime、installed/shared/Claude/Codex/Cursor package 字节一致；wrapper executable mode、
  dogfood overlay drift 与 43 条 frozen upstream ownership baseline 均通过。第九轮不把
  无法恢复退出码的旧 throwaway session 当作完成证据；本轮 fresh reapply 没有产生
  `.new`、`.bak`、updated managed file 或 conflict，后续 installed validator 再次证明
  sidecar 为 0。
- Clean throwaway exit 0：公共 marketplace init/preview/switch + 本地未发布 canonical
  workflow sample、preset apply、source/installed target resolution、zero/candidate preview、
  source-specific task/GitHub/Git locator 正负例、single/multi-segment machine path 与
  signed-query 正负例、external ancestor/receipt 的 installed record/check tamper negative、
  两份 independently retained receipts 的完整 ancestry chain positive 与 missing/wrong-order/
  digest/projection/rewrite/skip negatives、task-local ignored-target negative、pre-task zero-write、
  真实 `git worktree add -b` 上 candidate/zero same-snapshot record/check、
  `task_branch_stale` refresh record/check、`invalid_task_branch` non-refreshable negative、
  reviewed blob/closed issue、base sync、两轮 closeout、`trellis update --force`、workflow/
  preset reapply、再次 discovery/closeout 与最终零 `.new/.bak` 全部通过，process exit 0。
  当前 exact feature ref 的 `git ls-remote --exit-code` 返回 2，
  因未 push 明确不计入 throwaway pass。
- `jq empty`、隔离 pycache 的 `py_compile`、相关 `bash -n`、planning
  approval、task validate、source/installed workflow marker parser 与 `git diff --check`
  均通过。Planning hashes 保持
  `b869afdb...aff7` / `05fe5822...8682` / `b697c34d...91e0`；source checkout clean，
  worktree 无 `.new`/`.bak`，测试 `__pycache__` 已清理。

## 8. 未验证项与风险

- 当前分支未 push，因此 exact remote feature-ref marketplace install/update verifier
  尚未运行。Throwaway 只证明公开 marketplace discovery 加本地未发布 canonical
  workflow sample；远端当前分支证据必须由后续 `trellis-finish-work` 在 push 后绑定
  exact ref/HEAD 生成，在此之前不得宣称远端开箱验证完成。
- 当前 extension compatibility / throwaway update 目标是 Trellis CLI `0.6.5`；运行时
  npm registry 已显示 `0.6.7`。本任务没有扩张 compatibility target，`0.6.7` upgrade
  行为未验证，不能从本 handoff 推导兼容结论。
- 本轮没有 Docker、K8s、数据库 migration、Makefile、服务配置或业务部署影响；存在
  public workflow/skill/schema/command、preset installed asset 与多平台 package
  inventory 影响。
- 独立 checker 仍需按 PRD R1-R10、AC1-AC16 审查 AI/script boundary、Docs SSOT、
  current/history 顺序、freshness、distribution、upgrade/update 与安全边界。任何
  finding 都必须返回实现修订，不能以本地命令通过替代 Phase 2 semantic gate。
