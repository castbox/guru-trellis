# Issue #131 Branch Review 汇总

## 最终结论

- Task：`.trellis/tasks/07-23-131-guru-review-branch`
- Branch：`codex/131-guru-review-branch`
- Base：`origin/main`
- Committed HEAD：`c18efe0f73f03d216a7f4e873907569922e800be`
- 完整范围：`origin/main...c18efe0f73f03d216a7f4e873907569922e800be`
- Diff：328 files changed，38333 insertions，1326 deletions
- Review intent：`fresh_final_review`
- 最终审查代理：`/root/issue_131_branch_review_final4`
- 当前 findings：P0=0、P1=0、P2=0、P3=0
- Scope proposals：0
- 建议 typed exit：`passed`

Round 12 的全新 technical reviewer 未参与 implementation、Phase 2、task commit
或 Round 1–11 discovery/ownership/closure/final review，并独立覆盖了完整
committed range、live Issue #131、planning、fresh Phase 2、commit 005、全部历史
review 报告、canonical/installed package、五个平台入口、ownership、Docs SSOT、
upgrade/update、throwaway、安全与部署影响。它也独立复核了 Round 11 对单次
recorder 瞬时失败候选的 `rejected_candidate` disposition。全部历史
current-scope findings 已关闭，未发现新的 current-scope P0–P3 finding。

## Issue 与范围

- Live `castbox/guru-trellis#131` 仍为 open，accepted-current comment
  `#issuecomment-5045031945` 仍是最新 scope authority。
- `issue-scope-ledger.json` 的关闭候选只有 `#131`。
- `#127`、`#130`、`#144`、`#146` 仅为 related issues。
- `#116`、`#132` 为 follow-up issues，不由本 task 关闭。
- 当前授权不包含 push、PR、publication、issue close 或 deploy。

## 审查轮次与原始证据

1. Round 1 问题发现：
   [reviews/01-problem-discovery.md](reviews/01-problem-discovery.md)，
   SHA-256 `1fa16331617f20efd2855373abee6f9c9cd8e3d36b3b3dd6ae0e4abf3439d35b`；
   发现 P1×1、P2×2、P3×1。
2. Round 2 问题闭环：
   [reviews/02-finding-closure.md](reviews/02-finding-closure.md)，
   SHA-256 `013ab622c3281f00264721f4c9f5868bb5d053dd13a403ad5722a26679857ee4`；
   关闭 Round 1 四项 finding，新发现 P2×1。
3. Round 3 问题闭环：
   [reviews/03-finding-closure.md](reviews/03-finding-closure.md)，
   SHA-256 `26a1d264d30f043c79b78fb85ebd20c66c1bd5f82a8dae4a8a356d4e1d52f323`；
   关闭 `F-131-BR2-01`，新 finding 0。
4. Round 4 独立最终审查：
   [reviews/04-final-release.md](reviews/04-final-release.md)，
   SHA-256 `7701f3157748a3550a6dca780341461d952aad210e2a924fda61722c1f8a56f2`；
   发现 `F-131-BR4-01` P2。
5. Round 5 问题发现角色重入：
   [reviews/05-problem-discovery.md](reviews/05-problem-discovery.md)，
   SHA-256 `307ce3ac653840730b330f8c3c1a4119b911cadcc1b58b59538c023cf4ef54e4`；
   固定 `F-131-BR4-01` 的合法 owner evidence。
6. Round 6 问题闭环：
   [reviews/06-finding-closure.md](reviews/06-finding-closure.md)，
   SHA-256 `64f985bcf4e70e5db36a16978d3eaffc165e058d3804018c69ef702c3b12bbcb`；
   关闭 `F-131-BR4-01` 与 `F-131-P2-R5-01`，新 finding 0。
7. Round 7 独立最终审查：
   [reviews/07-final-release.md](reviews/07-final-release.md)，
   SHA-256 `023b3e780b10a23757af281192ff7ff61a66a329495fc054bd4a2798e423ca69`；
   发现 `F-131-BR7-01` P2 与 `F-131-BR7-02` P3。
8. Round 8 问题发现角色重入：
   [reviews/08-problem-discovery.md](reviews/08-problem-discovery.md)，
   SHA-256 `2e1cf5b90c3ad2223159d20d9480bf3e22591f86c60632e4031ad40d14edb491`；
   固定两项 BR7 finding 的合法 owner evidence。
9. Round 9 问题闭环：
   [reviews/09-finding-closure.md](reviews/09-finding-closure.md)，
   SHA-256 `6ce6546b0a1b81fc0e3590d8fad5bc4016384a1dd7369a1391140a7e2bc49155`；
   原 finding owner 关闭两项 BR7 finding，新 P0–P3 为 0。
10. Round 10 全新独立最终审查：
    [reviews/10-final-release.md](reviews/10-final-release.md)，
    SHA-256 `34c630307da1fe318faecacb5c8084c8b5e66ca9aa20ef2048d1cd8276f1bde7`；
    完整 fresh final review 后 P0–P3 为 0、scope proposals 为 0，建议
    `guru-review-branch:passed`。
11. Round 11 问题发现角色重入：
    [reviews/11-problem-discovery.md](reviews/11-problem-discovery.md)，
    SHA-256 `487ae97d488b2e020a034fd00172a1c316d555715b6e6944e82982bc38fdfe5f`；
    首次 recorder 单次失败的初始根因被代码与同状态成功重试推翻，候选记为
    `rejected_candidate`，P0–P3 与 scope proposals 均为 0。
12. Round 12 全新独立最终审查：
    [reviews/12-final-release.md](reviews/12-final-release.md)，
    SHA-256 `b47f8903a32bdc2d30ab416e1835a3b4c12cee0978828568ebc7d5adb19f03b7`；
    独立复核完整 range 与 Round 11 disposition 后 P0–P3 为 0、scope proposals
    为 0，建议 `guru-review-branch:passed`。

## Finding 生命周期

| Finding | 严重度 | 场景 | 最终状态 | 闭环证据 |
| --- | --- | --- | --- | --- |
| `F-131-BR-01` | P1 | `normal_required_behavior` | closed | Round 2 replacement recovery fixture |
| `F-131-BR-02` | P2 | `normal_required_behavior` | closed | Round 2 ordinary metadata boundary regressions |
| `F-131-BR-03` | P2 | `normal_required_behavior` | closed | Round 2 rejected-candidate persistence |
| `F-131-BR-04` | P3 | `normal_required_behavior` | closed | Round 2/3 diff and lifecycle evidence |
| `F-131-BR2-01` | P2 | `normal_required_behavior` | closed | Round 3 exact closure-round binding |
| `F-131-BR4-01` | P2 | `normal_required_behavior` | closed | Round 6 global workflow ownership closure |
| `F-131-P2-R5-01` | P2 | `normal_required_behavior` | closed | Round 6 marketplace/throwaway closure |
| `F-131-BR7-01` | P2 | `normal_required_behavior` | closed | Round 9 five-entry thin routing closure |
| `F-131-BR7-02` | P3 | `normal_required_behavior` | closed | Round 9 active 10/39 Docs SSOT closure |

Round 12 未仅依赖历史结论，而是对上述 closure 对应的当前代码、文档、
validators、tests、Phase 2 与 commit-tree continuity 重新做了独立复核。

## 当前合同与实现证据

### Branch Review 所有权

- `guru-review-branch` 是唯一 Phase 3.5 semantic owner。
- Package SKILL/contract 独占 independent reviewer dispatch、
  qualification-first、finding lifecycle、closure/fresh-final、AI Review Gate、
  confirmation 与四个 typed exits。
- Global workflow 只保留 mandatory invocation、四个唯一 consumers、re-entry 与
  fail-closed stop。
- `invoke.sh`、`review-branch.sh`、`check-review-gate.sh` 仅执行确定性的
  dispatch、record、schema/identity/freshness/lifecycle validation，不决定 scope、
  severity、充分性、pass 或 route。

### 五个平台入口

五个 canonical `trellis-continue` entries 及五个 installed copies 只保留六字段
public input：

- `profile`
- `mode`
- `task_ref`
- `base_ref`
- `committed_head`
- `review_intent`

并只消费四个 typed exits：

- `passed`
- `implementation_required`
- `scope_confirmation_required`
- `blocked`

十个入口文件均不再复制 recorder、gate、assignment、finding closure 或 fresh-final
私有生命周期。五对 canonical/installed bytes 一致，missing、unknown、multiple、
stale、unmapped 结果均 fail closed。

### Ownership 与 upgrade/update

- Issue #128 frozen/active path count：43/43，removed=0。
- Historical path-set digest：
  `56874019bb93b6669aaeb36b7ca9506aed9127a28ef9f81637ea428a6b0a838b`。
- Historical identity：
  `1e1faf9ffa95e1cbb1650c4eb9da1ceac035d045be70132b5c0b92ec5ccfc473`。
- `current_payload_sha256` 精确存在于五个 active continue entries，其他 38 项仍只
  使用 historical baseline。
- Current active payload aggregate：
  `ab94576c8d2d8768ffd50d1757179d8678de3a67923aeef3cd00ef006f76a86a`。
- Dogfood drift、double apply、installed inventory 与 no-sidecar checks 通过。

### Docs SSOT 与 public I/O

- Registry 当前为 10 active、1 planned、1 reserved。
- 十个 active Interfaces 共 39 external exits。
- Source/installed validators 均为 10 invokes、39 exits、23 targets。
- Installed inventory 为 1903 managed files、0 sidecar、0 removal、0 conflict。
- `production-minimal-handoff-v1` 独立保持 3 packages、11 exits、4 authoring seed
  edges；未与 active 10/39 混写。
- Root/workflow/preset README 与 durable specs 都把 `guru-review-branch` 记录为
  唯一 Phase 3.5 semantic owner。
- Public outputs 是每个 exit 的最小 handoff DTO，private gate evidence、digest、
  reviewer history 与 runtime state 没有进入跨 Skill handoff。

## 验证证据

Fresh Phase 2 与 committed tree 连续：

- `phase2-check.json`：schema 2.0、`typed_exit=passed`、
  `facts_sha256=043e257e7de4405cdf5578762bd8281f1337a61c68a1d5e0ee5e19facffa7261`。
- Runtime：566 passed，13 conditional skipped。
- Skill package：171/171 passed。
- Preset installer：45/45 passed。
- `guru-review-branch` contract：8/8 passed。
- Ownership：9/9 passed。
- Source/installed shared eval：各 7/7 passed。
- Static：2632 JSON、295 shell、116 Python compile passed。
- Clean throwaway：exit 0，覆盖 public marketplace discovery、本地 unpublished
  current canonical、fresh init、existing preview/switch、三平台 install、official
  update、workflow/preset reapply 与最终 no-sidecar。
- Task commit 005：commit `c18efe0f73f03d216a7f4e873907569922e800be`，
  parent `f4e2a62b8264dceb5078fd3ceb2caa3e46c97a53`，
  tree `84bf7f71f924c2e3434b340ec949440906e17191`，44/44 blob/mode match，
  `hook_mutation=false`、`unrelated_preserved=true`。

Round 10 与 Round 12 又分别独立执行 focused checks；当前最后一轮 Round 12 覆盖：

- `git diff --check origin/main...HEAD` 与 `git diff --check origin/main`。
- 16 项 focused tests。
- Direct ownership validator。
- Dogfood overlay drift。
- Source/installed package validators。
- Source/installed real-wrapper eval。
- Canonical/installed package、runtime 与五平台入口 parity。
- Commit 005 tree/path continuity。
- Unmerged/symlink/debug marker scan。
- Secret literal scan。

上述检查全部通过。仓库未配置独立 `ruff`、`shellcheck`、`mypy` 或 `pyright`
gate，因此没有把这些未运行工具写成已通过。

## 候选资格化与非阻塞限制

- `C-131-R10-01`：完整 range 的 ownership、I/O、lifecycle、distribution、
  Docs、upgrade normal path；当前证据未证明违反要求，记为
  `rejected_candidate`。
- `C-131-R10-02`：当前 branch 未获 push 授权，remote exact feature ref 不存在；
  记为 publication 前 `followup_candidate`，不得用 public main 冒充验证。
- `C-131-R10-03`：continue entries 中 pre-existing planning schema 1.2 文案存在于
  `origin/main`，不属于 Issue #131 Branch Review 收敛范围；记为
  `observation`，不赋 P0–P3。
- `C-131-R10-04`：敌对篡改、恶意伪造、TOCTOU、锁、额外并发/原子性与 fault
  injection 明确超出本仓库 honest-but-fallible 范围；记为
  `rejected_candidate`。
- `C-131-R11-01`：首次 final recorder 曾单次 fail closed，但同一 HEAD 与
  artifacts 上的 planning False/True、planning projection、allow-committed
  Phase 2 随后均成功，且初始“未透传”根因与真实代码不符；按正常路径可复现门禁
  记为 `rejected_candidate`，不赋 severity。

不存在 `unconfirmed_nonstandard_proposal`，无需用户进行新的 scope confirmation。

## Docs、安全与部署

- Docs strategy：`ssot_first`，task delta 已合并进 durable/public SSOT。
- 完整 range 不含 GitHub Actions、Docker/Compose、Kubernetes/Helm/Kustomize、
  业务数据库 migration、Makefile、生产配置或应用 runtime 变化。
- `production-minimal-handoff.json` 是 Skill API migration manifest，不是数据库
  或 deployment asset。
- 未发现 secret、credential、private key、`.env`、客户数据、本机绝对路径或
  signed URL。
- 无需部署或数据迁移。

## 放行边界

当前 committed branch 的 Branch Review semantic gate 可以记录为 `passed`。
这只表示 Issue #131 的本地 committed implementation 通过完整 fresh final review。

`passed` 的唯一 consumer `guru-review-task-publication` 仍是 planned/missing
（follow-up `#116`）。因此 workflow 到达 publication 边界后必须 fail closed；本
汇总不授权也不执行 push、PR、publication、issue close 或 deploy。
