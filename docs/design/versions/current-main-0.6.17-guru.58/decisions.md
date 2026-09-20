# Design 决策

当前 .58 来源：`castbox/Trellis@43fffc170927c85d9f7fc106cc5a059e80d4530b` / CI `35190729418` / CLI/core `0.6.17`；Guru manifest `0.6.17-guru.42`；repository release target `v0.6.17-guru.1`。Architecture public inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.58` / `active`。
完整继承 immutable `.57` 业务合同，当前增量为 #452；当前 registry 为 32 packages / 142 exits / 102 commands，production workflow 保持 22 mandatory invokes / 98 exits。

`.58` 完整继承 `.57`，吸收 reviewed #452 contribution；RDT current 为 `.58/active`，Architecture inheritance 仍为 `.57/active`。promotion-created diff 必须重新通过 fresh Phase 2、Task Commit、完整 Branch Review 后才能进入 Publication；本文不声明实现、测试或下游门禁已通过。

- `DDEC-001`（accepted）：文档只索引 registry/interface，不复制 schema 字段，避免 drift。
- `DDEC-002`（accepted）：current as-built 与 released tag 分开建模；manifest revision 不等于 release。
- `DDEC-003`（accepted）：Bootstrap 不合并 RDT 与 Architecture owner，只编排 minimal typed outputs。
- `DDEC-004`（accepted）：`.trellis/spec` 是 locator/usage projection，不是第三 authority。
- `DDEC-005`（inferred, not current）：未来 Phase owner 解耦可能改变 orchestration；在独立 Issue 接受前只列 GAP/TARGET。
- `DDEC-006`（accepted）：Finalizer terminal public projection 使用精确 retired locator、durable archive summary 与 current ready facts；不恢复已退休的进行中 gate/transaction/plan，也不放宽真实 stale 校验。
- `DDEC-007`（accepted）：verifier inventory 只消费 canonical registry/interface validation，不维护固定数量副本。
- `DDEC-008`（accepted）：完整 compatibility matrix 使用 pinned upstream 22-platform inventory；每个 cell 同时安装 shared `.agents` public projection 与其 exact selected platform projection，目标 selection 不从 installed 目录或 overlay 反推。
- `DDEC-009`（accepted）：existing migration 以 `v0.6.5-guru.10` 为 immutable before-state；official update 产生的已知 replacement `.bak` 必须逐项 reconciliation，最终 recursive sidecar count 为 0。
- `DDEC-010`（accepted）：A/B compatibility 与真实 GitHub A route 是验证 harness，不新增 #248 Acceptance 或 #252 cleanup public API。
- `DDEC-011`（accepted historical boundary）：`.39` docs 可以记录 #267 preparation/source proof，但
  `v0.6.15-guru.3` tag/Release、tag-pinned install 与 post-publish smoke 只能由其历史 exact-candidate
  lifecycle 晋升，不能替代 #332 `.5/.40` evidence。
- `DDEC-012`（accepted）：Architecture Baseline 与 Guru Team lifecycle 保持双维 authority，只在 task-local change contract 相交；项目 constitution/change contract 拥有具体语义，public package只拥有 shape、stage routes 与 deterministic validation。
- `DDEC-013`（accepted）：shared Architecture/RDT current 只由各自 semantic owner在 independent review 后串行 promotion；Architecture promotion 必须绑定 expected current 且强制 post-promotion Phase 2/commit/Branch Review。
- `DDEC-014`（accepted historical #267 contract）：`.42` 是 #267 完成时的 knowledge identity，extension
  candidate 为 `0.6.15-guru.39`；当前 `.44` 继承 knowledge/release identity separation，knowledge
  promotion 不隐式授权 push、tag、GitHub Release 或 Issue closure。
- `DDEC-015`（accepted historical #267 contract）：#267 promotion 由 Architecture owner 激活统一 `.42` baseline，随后由 RDT owner 建立完整 `.42` versioned authority；两步均绑定当时 expected `.41`，且 promotion-created diff 重新进入 Phase 2、commit 与 Branch Review。该 `.42` authority 现为 `.43` 的 superseded predecessor。
- `DDEC-016`（accepted）：`guru-sync-base` 以 selection -> authority binding 两阶段实现 detached normal path；worktree inventory 只服务 selected-base 后的 exact binding，不成为 base selection authority，也不引入 fallback、dual-read 或第二 resolver。
- `DDEC-017`（accepted）：Finalizer 使用独立 target/source checkout 与 closed mode binding，删除
  installed single-checkout 假设；verifier structured failure evidence 由 verifier 自治，不形成 shared
  resolver 或跨 lifecycle owner。
- `DDEC-018`（accepted）：`release-guru-trellis-version` 是 repo-private semantic orchestration，
  不新增公共 package/interface/schema/typed exit 或确定性发布脚本；它只按阶段调用既有 lifecycle
  owners，并保持每个外部 mutation 的独立确认与 live-fact recovery。
- `DDEC-019`（accepted historical #335 boundary）：preparation delivery content 与 lifecycle metadata 分离；
  owner-private checkpoint 不改变 reviewed-content identity，任何实际 delivery/durable/config/script/test
  bytes 变化仍使相应 gate stale。#392 由 `DDEC-027` 将 shared-authority promotion 前后两次完整 review
  明确为唯一后继合同。
- `DDEC-020`（accepted）：#332 authority promotion 更新 current release facts、
  history/navigation/traceability 与 evidence，并把 #240/#348 已合入、已独立审查的 owner/RDT/ADR
  authority 串行提升到 `.44`；不新增实现、第二 current writer、GAP 或 compatibility path。#311 的正式
  release 安装态 proof 由 #332 exact candidate fresh 承接。
- `DDEC-021`（accepted）：Release Gate evidence 以 post-merge fresh main candidate 为唯一聚合 identity；
  preparation、historical focused 或 package evidence 只作定位，不可跨 SHA 晋升。tag、immutable-tag smoke、
  GitHub Release、Issue closure 与 cleanup 保持独立 mutation owner 和确认边界。
- `DDEC-022`（accepted）：#240 采用独立 scenario/mechanism semantic owners；机制 owner 禁止 OS primitive
  承接业务 authority，正式决策为 `ADR-008`。
- `DDEC-023`（accepted）：#348 在现有 lifecycle recovery model 内拆分 Merge classification 与 archived-task
  restoration owner；该缺失恢复边不改变既有 architecture decision，因此不新增 ADR。
- `DDEC-024`（accepted）：#332 使用 `dedicated_refactor_slice` 将 PR #341 的第二 public facade 层收敛
  回四个原 command；Interface 独占 wrapper path，compatibility 只由旧参数触发。该修正恢复既有设计宪法，
  不新增 ADR、owner、GAP 或第二 current writer。
- `DDEC-025`（accepted）：#376 使用 `target_native` 在既有 Reconcile owner 内增加 package-private
  expected-head executor，并由 Review Branch 承接 bounded continuity。prior full review 与 current reconciled
  HEAD 分离建模，Finalizer-to-Reconcile 使用显式 public projection；该直接演进不新增兼容分支、第二状态机、
  owner、GAP、ADR 或 remote writer。

- `DDEC-026`（accepted）：#378 复用 Fork 自身构建、Node CLI、原 verifier 和现有 snapshot promotion，不引入第二框架、launcher 或基础设施；source lock 单一拥有来源，installed record 仅为受管投影。构建标记只校验普通 source/build mismatch；#388/#389 和既有 semantic owners 不变。

- `DDEC-027`（accepted）：#392 以 `target_native` 绑定 expected immutable `.47`，由 Architecture/RDT
  serialized owners 建立唯一 active `.48`。pre-promotion Phase 2/commit/full review 与 post-promotion fresh
  Phase 2/commit/full review 是两个独立 content gates；第二次 review 前 Publication 不可达。mapping 固定为
  `v0.6.16-guru.1` / `0.6.16-guru.41` / CLI `0.6.16` / fixed Fork full SHA，不新增公共 API、
  second writer、compatibility layer、ADR 或 release state machine。

- `DDEC-028`（accepted）：#329 继续使用 `target_native` 与现有 official-extension/single-writer 设计，
  将 framework source 直接前进到 developer-free `0.6.17`，受控 consumer 从 task/Git/runtime mapping 与
  explicit caller authority 取得 identity。legacy identity/workspace 数据只保留 bytes，不进入 current flow；
  不引入 adapter、dual-read/write、第二 resolver、owner、GAP、ADR 或基础设施层。


- `DDEC-030`（accepted）：#408 使用既有 source record、Fork 正式生成、workflow/Skill owner 与
  Clarification/Readiness recorder 的确定性职责直接演进。D408-01..05 不新增 resolver、wrapper、
  recovery checkpoint、public graph 或第二 closure authority。完整 `.50` 为 immutable predecessor，
  `.51` 继承同版本 Architecture；Constitution/change-contract/GAP/ADR/Evolution 保持不变。

## #418 决策

D418-01..06 使用 target_native 的隔离只读机制：四个新增 profile、三个新 success exits、
三个 Architecture 既有 source/stage 配对；Architecture 不新增 profile，也不新增 Skill、command、公共 facade 或第二 writer。
H/A/B、PR snapshot 与新 Publication 判断分别建模；原 mutation path、closure ownership 和 Restore 保持。
普通 Branch Review input 4.0/gate 7.0 与 additive input 5.0/archived-1.0 并列，由 canonical package 定义实际 shape。
项目决策只引用 [ADR-010](../../../architecture/adr/010-archived-review-authority.md)；
来源见 [#418 contribution](../../../requirements-design-test-contributions/418-closeout-identity-recovery/manifest.yaml)，
责任与双向索引见 [design-main.md](./design-main.md)、[traceability.md](./traceability.md)。

## #419 决策

- `DDEC-031`（accepted）：单一 workflow continuation block 是 active-task detailed routing authority；
  producer recovery 与 semantic fresh rerun保持原 owner，不新增 global resolver或持久化 stage。
- `DDEC-032`（accepted）：activation使用 exact-pair-first `initial|recovery`；Phase 2复用现有 rematerialization，
  Task Commit复用same-candidate recovery，Branch Review与Publication lost output fresh重跑。
- `DDEC-033`（accepted）：upstream candidate拥有thin entries；Guru只定义workflow内容及owner recovery。
  #410独立执行release matrix。

## #435 决策

- `DDEC-034`（accepted）：Delivery Review、Publish、Merge 分为三个 semantic owner；每个 owner 独占自己的
  public DTO、owner-private recovery 与 mutation boundary，不能把 Delivery cycle 折回 Finalizer/Merge PR owner。
- `DDEC-035`（accepted）：跨 branch/worktree Delivery history 由 GitHub PR/merge、merge commit、parents、
  repository/base 与 closed trailers 重建；不新增 ledger、PR-body identity reader 或 compatibility adapter。
- `DDEC-036`（accepted）：三个 package 以 `active/deferred` 进入 26/114/96 registry closure，#434 前不进入
  22/98 production graph。#436 保持 terminal lifecycle owner；完整 Release matrix 保持 `unverified`。

## #436 决策

- `DDEC-037`（accepted）：Completion、Closure、Finish、Cleanup 与 Reactivate 保持五个独立 semantic owners；任何一个 owner 的 success 不替代其它 owner 的判断或 mutation。
- `DDEC-038`（accepted）：#436 五个 packages 以 `active/deferred` 进入 `.56` registry closure；#434 是 production graph activation 与旧 edge retirement 的唯一 owner，不新增 adapter、ledger、dual graph 或旧 output reader。

## #443 决策

- `DDEC-039`（accepted）：task identity与official Trellis active-task/session store保持authority；新package只拥有lifecycle-aware binding语义、boundary validation和最小mapping/binding write，不引入第二resolver、ledger或tracked session state。
- `DDEC-040`（accepted）：#443 package以`active/deferred`进入`.57`的32/142/102 closure；五个成功routes加一个blocked exit保持exit-specific minimal DTO，production graph仍为22/98且只由#434后续激活。

## #452 决策

- `DDEC-041`（accepted）：平台 authority 只保留 pinned upstream 22-platform inventory 与目标仓库 exact `selected_platforms` 两层；默认集合、dogfood 状态、canonical ownership 和 overlay cardinality 均不形成第三层 authority。
- `DDEC-042`（accepted）：argparse 只声明重复 `--platform`；显式值形成 exact subset，未指定时选择 Claude、Codex、Cursor。`--all-platforms` 及其 manifest/upgrade/throwaway 状态被完整删除。
- `DDEC-043`（accepted）：升级 selection 只从目标仓库 current manifest/provenance 恢复并以重复 `--platform` reapply；缺失、空、unknown 或跨 section 不一致在文件 mutation 前 fail closed。
- `DDEC-044`（accepted）：`guru-trellis` dogfood 是 exact three-platform business-repository selection；OpenCode 是 upstream inventory 普通成员，不因 canonical capability 自动进入 dogfood。
- `DDEC-045`（accepted）：全平台 descriptor、ownership 和 projection 完整性由 #452 后续实现与测试证明；Design promotion 不等于 implementation/test PASS，#434 production activation 与 release/tag 保持独立 owner。
