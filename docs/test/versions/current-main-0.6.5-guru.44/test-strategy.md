# 当前测试策略

版本：`current-main-0.6.5-guru.44`；状态：`active`；predecessor：`current-main-0.6.5-guru.43`。

## Evidence 分层

| ID | 层级 | 能证明 | 不能替代 |
| --- | --- | --- | --- |
| `TST-001` | static/docs | 格式、链接、结构、scope、context 可加载 | runtime 行为 |
| `TST-002` | package/unit | interface/schema/runtime 局部合同 | installed graph 与外部服务 |
| `TST-003` | semantic eval/review | normal-path 语义、finding 与 route 充分性 | deterministic side effect |
| `TST-004` | integration | producer -> consumer、task/history/recovery 数据流 | 多平台安装 |
| `TST-005` | distribution/throwaway | canonical/installed/platform/preset 实际一致 | 未执行的 upgrade/release candidate |
| `TST-006` | SSOT | RDT/Architecture/Bootstrap locator、traceability、freshness | 产品 runtime |
| `TST-007` | compatibility | public id/schema/exit/command closure | 未来版本兼容，除非 exact matrix |
| `TST-008` | live/external/release | GitHub、tag、Release、exact candidate 与目标环境 | static/unit 或 skipped test |
| `TST-009` | business parallel matrix | 两个 task 的 worktree/contribution/Finish/cleanup 隔离 | 单 task package test |
| `TST-010` | history/acceptance | task index、archive、finish-summary、retained ref 与查询可发现性 | PR body 声明 |
| `TST-011` | recovery | base/provider stale、partial recovery、re-entry 与零重复副作用 | happy-path static check |
| `TST-012` | terminal projection | retired locator + archive summary + current ready facts 的正向投影与 stale 负例 | pre-archive Publication authority |
| `TST-013` | inventory derivation | canonical registry/interface-derived ids/commands/complete packages 与 installed equality | 固定 magic count |
| `TST-014` | full platform matrix | live-derived platform × clean/existing 的 official install/update 与 installed behavior | representative single-repo throwaway |
| `TST-015` | capability preservation | before/after `workflow`、`task_data`、`docs_authority` equality | Skill API/schema/distribution/install consistency 检查 |
| `TST-016` | installed SSOT contracts | RDT/Architecture/Bootstrap profiles 与双 SSOT projection 保持 | package discovery 或 `--help` |
| `TST-017` | A/B lifecycle and live provider | 独立 Finish routes、recovery、merge order、reachability 与真实 GitHub expected-head merge/closure | fake provider 单独结论 |
| `TST-018` | architecture stage lifecycle | Planning/discovery/Phase 2/Branch Review/Publication/Acceptance invocation、freshness、unique consumer 与 post-promotion re-entry | 任一旧阶段结果或测试数量 |
| `TST-019` | design constitution | unique locator + current version/content identity + exactly five stable identity/short names；正文 authority 隔离 | score、required verdict 或公共 checklist |
| `TST-020` | architecture path | `target_native|legacy_boundary_convergence|dedicated_refactor_slice` 互斥，no-impact 独立 | 文件路径/数量分类 |
| `TST-021` | task-local change contract | 双维 authority、required concern applicability、owner/single-writer、compatibility exit、parallel scope、deviation、evidence、review/promotion 完整 | optional 空字段或默认 route |
| `TST-022` | project architecture check | current descriptor/result 一一绑定、before/after、blocking、evidence/unavailable reason、freshness 与 regression route | generic runtime 代替项目语义 |
| `TST-023` | contribution and ADR | task-owned contribution 隔离、ADR trigger、independent review 与 expected-current-bound serialized promotion | implementation tests 代替 promotion |
| `TST-024` | parallel stale | 独立 contribution scope、shared current/GAP/owner 禁止竞争、successor 后旧 task re-entry | 锁、shared ledger 或 TOCTOU 协议 |
| `TST-025` | Architecture 2.0 atomic projection | schema/runtime/canonical/dogfood/installed/platform/consumers 无 legacy selector 或 dual-read | 部分投影或隐式 migration |
| `TST-026` | #283 targeted validation | package/runtime/eval、十场景、preset reapply/drift/sidecar 与一个代表性 clean install | 重构前稳定版 exact-candidate matrix/tag/Release/smoke |
| `TST-027` | base selection and binding | explicit/config/ordered/remote-default precedence、same-common-dir exact checkout、missing/dirty/mismatch blocked | public publication 或多平台 release proof |
| `TST-028` | authority synchronization | detached/current session、remote-ahead fast-forward、post-sync three-way equality 与 locator continuity | non-fast-forward recovery |
| `TST-029` | downstream provenance | producer transition 到 workspace consumer 的 source/base/full-candidates exact freshness | producer private runtime 或历史 checkpoint |
| `TST-030` | #290 distribution | canonical/installed/platform parity、inventory、reapply/drift/mode/sidecar-zero 与代表性 Codex detached wrapper | 独立的重构前稳定版 Release matrix/tag/Release |
| `TST-031` | Finalizer source/target binding | closed mode、双 checkout、immutable source、apply target、tail lineage 与 postimage | 真实 GitHub fixture 或生产结果 |
| `TST-032` | Initial reprepare and fail-close | existing-PR precedence、prepared-state inference、absent/exact remote 与 pre-mutation failure | archive 后 terminal live facts |
| `TST-033` | Installed distribution isolation | canonical/installed package、verifier-zero dependency、preset projection、mode/drift/sidecar | release-wide matrix |
| `TST-034` | Representative installed closeout | release-installed business repo 从 ready 到 Ready PR/terminal projection | 未 fresh 重试时保持 `unverified` |
| `TST-035` | Structured verifier failure | stage/cell/command/exit/bounded safe tail、outer parse 与 postcheck classification | Finalizer lifecycle authority |
| `TST-036` | historical #267 authority uniqueness | #267 `.41 -> .42` promotion 后 RDT/Architecture 只存在一个 active `.42`，`.41` 为 superseded，predecessor/successor 一致；`.43` 是后续 successor history，当前唯一 active 为 `.44` | runtime behavior |
| `TST-037` | historical release identity mapping | #267 历史 authority 只声明 `.3/.39/CLI 0.6.15` target，历史 `.37` 仅存在于明确 superseded/released evidence；当前 `.44` 的 `.5/.40/CLI 0.6.15` target 由 `TST-046` 独立覆盖 | tag、Release 或 smoke 已完成 |
| `TST-038` | historical fact-only semantic diff | #267 `.41...42` 不新增 behavior、public API、Architecture decision、owner、GAP、compatibility exit 或 ADR | downstream Phase 2/Branch Review |
| `TST-039` | historical promotion lifecycle freshness | #267 contribution review、RDT/Architecture serialized promotion、fresh Phase 2/commit/Branch Review 与 closure boundary | 任一旧 gate 或 package PASS |
| `TST-040` | repo-private projection boundary | Shared/Codex/Claude/Cursor private definitions parity，public package/marketplace/preset/installed inventory zero inclusion | 公共 Skill installation |
| `TST-041` | invocation and owner composition | 六项输入、fresh authority、两阶段 classification、既有 lifecycle owner composition 与 unsupported route fail closed | 复制 owner internal procedure |
| `TST-042` | honest-path and reconciliation | production preview/recorder/checker/public wrappers 的稳定计划到 Finalizer 单次 Review 路径，以及 planless base reconciliation | 实际 PR/merge/release |
| `TST-043` | reviewed-content freshness | lifecycle checkpoint 创建/替换/退休不改 identity；Skill/docs/config/schema/script/test delivery drift 使 gate stale | malicious tamper model |
| `TST-044` | live payload and action boundary | PR/Release payload 即时 authoring、forbidden tracked artifacts、每项外部动作独立 confirmation | payload 或 mutation 已发布 |
| `TST-045` | scoped post-merge contract | exact candidate、minimum gates、sidecar/residue、FAIL/SKIP/stale/cross-SHA stop 与零真实 release mutation | 累计 Release Gate matrix |
| `TST-046` | release identity and authority | `.44` unique current、latest stable `.4/.39`、target `.5/.40/CLI 0.6.15` 与历史 facts 保留 | tag/Release 已创建 |
| `TST-047` | merged prerequisite consumption | fresh candidate 重新消费 #311/#333/#339/#358/#361 与 installed business-repository contract | 历史 Issue/PR 自述替代 fresh proof |
| `TST-048` | serialized RDT promotion | Architecture `.44/current` inheritance、expected `.43`、完整 RDT version/navigation/traceability 与 post-promotion re-entry | promotion runtime 代替 Phase 2/Review |
| `TST-049` | exact-candidate pre-tag gate | predecessor full diff、版本面、package/registry/ownership、四平台与 install/update/reapply 绑定同一 candidate | cross-SHA、SKIP 或 focused package result |
| `TST-050` | immutable release lifecycle | installed business-repository chain、secret/residue、annotated tag、tag-pinned smoke、Release/closure/cleanup 独立 transaction | 任一 mutation 的预授权或推定成功 |
| `TST-051` | current graph closure | registry/interface/workflow/preset exact 派生 23 Skills / 97 exits / 81 commands，22 integrated + 1 standalone | 历史固定计数替代 current inventory |
| `TST-052` | solution mechanism qualification | paired semantic cases 覆盖 OS primitive replace、普通 file/state qualified、DB/application state qualified 与 pressure framing 不改变结论 | keyword/import/path scanner 替代 AI judgment |
| `TST-053` | merge Phase 2 re-entry routing | current-scope task-work finding 唯一进入 `phase2_reentry_required`，external blocker 保持 `merge_blocked` 且无 GitHub mutation | 把 CI/provider blocker 伪装为 task work |
| `TST-054` | archived-task restore transaction | 原 identity 恢复、status/mapping/pointer/stale authority cleanup、idempotent retry 与 dirty/duplicate/stale/merged zero-write negatives | 创建替代 task/branch/worktree/PR |
| `TST-055` | reviewed contribution promotion | PR #346/#351 independent review、merge/Issue closure、ADR-008 与 `.44` RDT/Architecture traceability 闭合 | 旧 pending 文案或 PR 自述单独冒充 post-promotion gate |

## 核心场景

- `SCN-001`：标准 Intake 从 current base/context 到唯一 workspace，无 pre-task tracked residue。
- `SCN-002`：Planning/Phase 2/commit/review 对 content freshness fail closed，并支持 finding fix + fresh final review。
- `SCN-003`：Finalization/merge 使用 expected HEAD，archive/history 可发现且 close issues 精确。
- `SCN-004`：base/provider evolution 自动进入唯一 reconcile/recovery route，不复用 stale evidence。
- `SCN-005`：canonical、dogfood、installed、Shared/Codex/Claude/Cursor byte/mode/graph 一致；preset reapply 不留未知 sidecar。
- `SCN-006`：RDT 与 Architecture version/status/traceability 对齐；Bootstrap projection 最小且不形成第三 authority。
- `SCN-007`：同一 clean base 的 A/B task 使用独立 worktree、branch、task 与 contribution；
  Planning/Check/Review/Finish/cleanup 不读写对方 tracked state，也不要求合并对方 bookkeeping commit。
- `SCN-008`：provider failure、stale evidence 与 partial finalization 由 exact owner 恢复；已发生副作用
  不重复，unsupported/mismatch fail closed。
- `SCN-009`：task 已归档且 owner state 正常退休后，精确 retired locator 可重建 schema-valid `ready_for_merge`；缺 locator、archive/head/PR/scope drift 继续 fail closed。
- `SCN-010`：新增或移除 active Skill 时 verifier 从 registry/interface 自动取得 inventory，并与 installed projection 做 exact equality。
- `SCN-011`：`claude|codex|cursor × clean|existing` 六个独立 cell 全部使用 Trellis `0.6.15` 结束，sidecar 与 unknown template drift 为零；matrix `source_state` 绑定 HEAD、tracked/untracked candidate bytes/modes 与 candidate tree，run 前后 identity 一致。
- `SCN-012`：existing cell 从 official `0.6.5` + `v0.6.5-guru.10` 运行 upgrade/update dry-run、条件式 migrate、workflow preview/switch 与 preset reapply。
- `SCN-013`：before/after `workflow`、`task_data`、`docs_authority` 三组无未审查
  capability loss；active id、interface/schema/exit/command/consumer/route、Skill package、
  ordinary managed asset、overlay executable mode、template hash、sidecar 与 extension identity
  另由 consistency/installation gate exact 验证，任一漂移仍独立阻塞。
- `SCN-014`：每个 cell 运行 RDT、Architecture、Bootstrap 全 profile installed eval，并保持 #266 docs authority 与最小 spec projection。
- `SCN-015`：local A/B 完成两种 merge order、零 metadata intersection、task-local archive、Finish/provider/cleanup 同 owner recovery 与 cleanup 后 reachability；B 的 GitHub 调用为零；A archive 后 history query 返回唯一 `PR #301` finish-summary candidate。
- `SCN-016`：真实 A disposable repo 的 PR #2 在 expected source head 上 rebase merge，Issue #1 在 merge 后关闭；remote branch/repo cleanup 后 retained-ref proof仍成立。
- `SCN-024 no-impact`：fresh minimal current result，不创建 contribution/ADR/project-check burden。
- `SCN-025 target-native`：直接建立 target boundary 与唯一 owner；新增 legacy authority、dual-read 或 adapter 被阻断。
- `SCN-026 legacy-boundary convergence`：decision/GAP、remaining debt、compatibility owner/exit 与 forbidden scope 完整且只收敛局部旧边界。
- `SCN-027 dedicated refactor slice`：行为/API/规则不变，单一主写，小切片可验证、观测、回滚并有旧实现删除条件。
- `SCN-028 scope expansion`：persistence/SDK/owner/boundary 等材料扩大使 Planning result stale 并 re-entry。
- `SCN-029 fitness regression`：第二 authority、legacy owner 扩大、无退出双写或 closed GAP 重现返回 `fitness_regression`。
- `SCN-030 parallel stale`：task A promotion 后，task B 的旧 current identity 返回 `sync_required`。
- `SCN-031 unpromoted contribution`：实现/测试通过但 contribution/ADR/review/promotion 缺失时 Publication/Finish 阻断。
- `SCN-032 next-task consumption`：successor baseline/constitution/decision/GAP/owner 是下一次 Planning 唯一 current input。
- `SCN-033 missing external evidence`：保持 `evidence_gap|unverified`，不虚构 pass、GAP closure、排期或发布。
- `SCN-034 explicit/config selection`：显式或 config `release/1.3.0` 在 clean main checkout 存在时仍只绑定 release authority。
- `SCN-035 ordered no-fallback`：`dev -> main` 同时存在时选择 dev；dev checkout 缺失或 dirty 时 blocked，不回退 main。
- `SCN-036 detached authority`：detached session 与 clean selected-base authority 同处 common-dir 时完成同步，handoff/transition locator 指向 authority。
- `SCN-037 identity mismatch`：missing、ambiguous、dirty、inventory HEAD/branch/ref mismatch 分别稳定 fail closed。
- `SCN-038 fast-forward continuity`：remote advance 只前进 authority checkout，detached session 不变，post-sync decision/local/remote heads 相等。
- `SCN-039 source-aware freshness`：explicit/config/config-candidate/remote-default 的 source、selected base 与完整 candidates exact 匹配时通过，任一 drift 在 workspace preparation 前拒绝。
- `SCN-040 distribution boundary`：canonical/installed/package/platform/reapply/drift/sidecar 和代表性 installed detached wrapper 通过，但不声明重构前稳定版 release-wide proof。
- `SCN-041 self-hosted binding`：source repository identity 等于 target 时，extension source 固定为
  reviewed head；apply 仍只修改独立 target checkout。
- `SCN-042 installed no-source-tree`：business target 不含 `trellis/presets/**`，Finalizer 从 manifest
  immutable source commit 建立 clean detached extension checkout，并生成唯一 manifest tail。
- `SCN-043 invalid source`：missing/malformed/dirty/mutable/mismatched source 或 postimage 在任何
  push/PR/archive/Ready/Issue mutation 前 fail closed。
- `SCN-044 initial publication`：无 existing PR/remote/tail 的 `prepared` 输入返回 provenance
  reprepare；absent 或 exact reviewed remote 可执行，非空 drift 继续拒绝。
- `SCN-045 installed projection`：canonical/installed/平台 package 与 reapply bytes/mode 相同，
  Finalizer 对 verifier lifecycle 保持零依赖。
- `SCN-046 verifier failure evidence`：matrix 与 postcheck failure 在 cleanup 前形成 closed structured
  facts，credential-safe tail 有界，failed + null 被拒绝。
- `SCN-047 representative live closeout`：现有真实 fixture fresh reinstall 后完成 Publication/
  Finalizer/Ready/terminal flow；在该复跑实际完成前状态为 `unverified`。
- `SCN-048 historical release authority promotion`：#267 Architecture owner 先激活统一 `.42`
  baseline，RDT owner 后建立 `.42` versioned authority；任一 expected `.41` mismatch、multiple active、
  active `.37` 残留或 traceability 缺失均 fail closed，promotion diff 重新进入 Phase 2/commit/Branch
  Review；该场景是 `.43` 继承的历史合同与证据。
- `SCN-049 repo-private preparation honest path`：稳定 planning 与最终 delivery commit 后执行唯一一次
  complete-range Branch Review，再进入 Publication 与 Finalizer，不产生 tracked release-status metadata commit。
- `SCN-050 planless base reconciliation`：Finalizer 前发生正常 base 前进时，exact base facts 先得到
  `base_reconciliation_required`，不因通用 plan identity 为空而误拒绝，也不执行 closeout mutation。
- `SCN-051 lifecycle checkpoint stability`：owner-private checkpoint 创建、替换和退休不改变
  reviewed-content identity 或 delivery commit。
- `SCN-052 delivery drift staleness`：修改 Skill、durable docs、配置、schema、script 或 test bytes 时，
  受影响的 Phase 2/Review/Publication/Finalizer/exact-candidate gate stale。
- `SCN-053 private inventory isolation`：四个 project-local projection 存在且一致，但公共 registry、
  marketplace、preset、overlay、extension manifest 与 installed inventories 均不存在该 Skill ID。
- `SCN-054 v0.6.15-guru.5 exact candidate`：`.44` authority 只投影 `.5/.40/CLI 0.6.15` current
  target；preparation merge 后从 fresh main 冻结同一 candidate，完成 `v0.6.15-guru.4..candidate`
  full diff、四平台/install/update/reapply、installed business-repository Publication/Finalizer、secret 与
  residue gate。tag、immutable-tag smoke、GitHub Release、#332 closure 与 cleanup 分别 fresh 确认并回读。
- `SCN-055 forbidden mechanism`：已资格化正常问题拟使用 OS lock、`/proc`、PID/FD/signals 等承接
  业务 authority 时返回 `mechanism_revision_required`，已实现、已测试、P0/P1、race/TOCTOU 或
  fail-closed framing 不改变结论。
- `SCN-056 ordinary state exception`：普通文件/目录保存 state/artifact/log/cache/config，或数据库
  事务/durable state machine 承接业务身份与并发时 qualified；文件存在/inode/FD/lock-file 互斥不 qualified。
- `SCN-057 archived task work recovery`：Open same-head PR 的 current-scope finding 经 Merge 最小 DTO
  恢复原 task 到 Phase 2，清理旧下游 authority，并强制重跑 Phase 2 到 Merge。
- `SCN-058 archived recovery blocked`：external blocker、scope/head/branch/PR/archive drift、dirty worktree、
  duplicate active task、merged PR 或不安全路径均 fail closed 且零业务写入。
- `CASE-001`：每个 active interface 的 external exit 恰有唯一 consumer 或 stop，registry/interface/workflow 闭包。
- `CASE-002`：semantic gate 发生在 recorder/validator 前，脚本不接收或持久化授权。
- `CASE-003`：missing/multiple input、live mismatch、cross-candidate、lineage gap、FAIL、SKIP、stale
  或 unsupported exit 均在 mutation 前失败，不存在 fallback。
- `CASE-004`：merge、tag、tag-pinned validation、Release、Issue closure 与 cleanup 的 action-local
  confirmation 互不授权，旧确认不能跨动作复用或持久化。

## 选择规则

先读取 `.trellis/spec/workflow/quality-guidelines.md` 的 `Validation Scope Ownership`。普通 feature/docs/spec Issue 运行与 accepted scope 相关的最小可靠集合；完整多平台 Throwaway 只属于专项兼容/upgrade/release Issue。任何 SKIP、未配置 live 环境或历史 PR 声明都明确写成 `unverified`。

完整矩阵只证明其绑定 candidate 的 compatibility；`.44` 是 knowledge identity。latest stable
`v0.6.15-guru.4` / extension `0.6.15-guru.39` 与 current target `v0.6.15-guru.5` /
extension `0.6.15-guru.40` 是独立 release axes；`.5` 在 #332 exact-candidate matrix、tag、GitHub
Release 与 tag-pinned smoke 完成前必须继续标记为 `unverified`。
