# 当前测试策略

版本：`current-main-0.6.5-guru.40`；状态：`superseded`。

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
- `CASE-001`：每个 active interface 的 external exit 恰有唯一 consumer 或 stop，registry/interface/workflow 闭包。
- `CASE-002`：semantic gate 发生在 recorder/validator 前，脚本不接收或持久化授权。

## 选择规则

先读取 `.trellis/spec/workflow/quality-guidelines.md` 的 `Validation Scope Ownership`。普通 feature/docs/spec Issue 运行与 accepted scope 相关的最小可靠集合；完整多平台 Throwaway 只属于专项兼容/upgrade/release Issue。任何 SKIP、未配置 live 环境或历史 PR 声明都明确写成 `unverified`。

完整矩阵只证明 `public_plus_local_candidate` 与 current source compatibility；`.40` 是 knowledge identity，`.37` stable tag、
GitHub Release 与 tag-pinned release smoke 必须继续标记为独立的重构前稳定版 Release boundary。
