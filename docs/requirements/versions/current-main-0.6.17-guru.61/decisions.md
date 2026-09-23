# Requirements 决策与 provenance

当前 .61 来源：`castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296` / CI `35621578090` / CLI/core `0.6.17`；Guru manifest `0.6.17-guru.42`；repository release target `v0.6.17-guru.1`。Architecture public inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.61` / `active`。
完整继承 immutable `.60` 业务合同，当前增量为 #454 C3 checkout acquisition provenance；当前 registry 保持 32 packages / 142 exits / 102 commands并增加一个 planned ID，production workflow 保持 22 mandatory invokes / 98 exits。

`.61` 完整继承 `.60`，吸收 reviewed #454 C3 provenance contribution；RDT 与 Architecture current 均为 `.61/active`。promotion-created diff 必须重新通过 fresh Phase 2、Task Commit、完整 Branch Review 后才能进入 Publication；本文不声明 C4-C7、D443、D436、E434、tag 或 Release 已完成。

- `RDEC-001`（accepted）：current knowledge authority 为 `current-main-0.6.17-guru.61`，与 extension `0.6.17-guru.42`、CLI/core `0.6.17`、repository target `v0.6.17-guru.1` 独立；旧 release mapping 仅为继承历史。
- `RDEC-002`（accepted）：旧 requirements 文件改为导航，避免双 current authority。
- `RDEC-003`（accepted）：从 current workflow/registry/interface 恢复的行为标为 `code_recovered`，不冒充原始产品 intent。
- `RDEC-004`（accepted）：#263/#264/#265 PR body 中的测试数字只作为 historical focused evidence，不自动转写为本次 PASS。
- `RDEC-005`（accepted historical boundary）：#260 建立 Trellis `0.6.15` compatibility；#267 当时独占
  `v0.6.15-guru.3` / extension `0.6.15-guru.39` 的 exact-candidate lifecycle。其历史 promotion/package
  evidence 不晋升为 #332 `.5/.40` Release Gate proof。
- `RDEC-006`（source_confirmed）：#262 以“当前无法复现、证据不足”关闭；其关闭评论记录 exact source targeted 10/10 与 suite 44/44 PASS，但没有 code fix，也不能证明 current main 或后续 release candidate。
- `RDEC-007`（accepted）：`.agents` 是每个声明平台 cell 的 shared public projection，不是第四个 Trellis CLI platform；package-private validator wrappers 不分发到 platform roots。
- `RDEC-008`（accepted）：A/B compatibility harness 只产生 #248/#252 可消费的事实，不新增 Acceptance、Finish 或 cleanup public owner。
- `RDEC-009`（accepted）：Architecture Baseline 是全 task lifecycle 的唯一项目架构 authority；双维 identity 只在 task-local change contract 相交，shared current 只经 independent review 后的 expected-current-bound serialized promotion 前进。
- `RDEC-010`（accepted）：设计宪法正文归项目 Architecture authority；公共合同只投影五个稳定 identity/short name，不建立 scorecard、逐项 verdict 或第二 authority。
- `RDEC-011`（accepted）：base selection 与 authority checkout binding 是两个顺序固定的确定性阶段；detached session 仅承载调用，selected-base authority checkout 独占同步、clean 与三向 equality，下游按 source 与完整 candidates 重新验证 provenance。
- `RDEC-012`（accepted）：installed Finalizer 将 extension source checkout 与 target reviewed
  checkout 分离，使用 closed `self_hosted|installed` binding；standalone verifier failure evidence
  保持独立 owner。该 knowledge promotion 不证明真实 fixture closeout、生产发布或错误文件重试。
- `RDEC-013`（accepted）：#267 reviewed contribution 先由 Architecture owner、后由 RDT owner 绑定
  expected `.41` 串行提升为 `.42`；`.42` 只更新 release/current facts、navigation、traceability 与
  evidence，不改变产品行为、公共 Skill API、Architecture decision、owner、GAP 或 compatibility exit。
- `RDEC-014`（accepted）：#335 将 `release-guru-trellis-version` 定义为仅属于本仓库的正式发布
  编排 Skill。它不进入 Guru Team 公共 registry、marketplace、preset 或业务仓库 installed projection，
  也不执行或替代任何发布 mutation owner。
- `RDEC-015`（accepted）：正式发布分为 preparation PR 与 post-merge exact candidate 两阶段；稳定
  delivery bytes 进入既有 Phase 2/commit/review/publication/finalization 生命周期，运行态 Gate 与外部
  副作用状态只由 live facts 或 owner-private checkpoint 承接，不写入 tracked authority。
- `RDEC-016`（source_confirmed + reviewed）：#332 以 latest stable `v0.6.15-guru.4` / extension
  `0.6.15-guru.39` 为 predecessor，将 `.5/.40/CLI 0.6.15` 固定为唯一 current target。#311 已完成的
  source/target provenance 前置由 #332 exact-candidate installed business-repository Release Gate fresh 消费；
  历史 package/Issue/PR evidence 不晋升 tag、Release、smoke 或 closeout 状态。
- `RDEC-017`（accepted）：#240 的场景/机制双 owner 与 OS primitive authority 禁止合同经 PR #346
  独立 Branch Review 后由 `.44` promotion 接受为 `ADR-008`；普通文件/目录例外保持。
- `RDEC-018`（accepted）：#348 的 Merge task-work re-entry 与 archived-task recovery 经 PR #351
  独立 Branch Review 后进入 `.44`；它复用既有 lifecycle recovery model，不新增 ADR。
- `RDEC-019`（accepted）：reviewed #332 original-entry contribution 绑定 expected `.44` promotion 为
  `.45`；四阶段原 wrapper/command 保持 public identity，Interface 成为 generic wrapper selection 唯一
  authority，23/97/77 为 current graph。该 promotion 不证明 release，也不复用旧 candidate evidence。
- `RDEC-020`（accepted）：reviewed #376 contribution 绑定 expected `.45` serialized promotion 为 `.46`；
  Reconcile 继续拥有 semantic classification 与唯一 local expected-head commit，Review Branch 只拥有 bounded
  continuity judgment，Publication 继续严格绑定 current reviewed-content identity。该 direct evolution 不新增
  public Skill/exit、compatibility branch、第二 writer、remote mutation、ADR 或 Release proof。

- `RDEC-021`（accepted）：#378 将 expected immutable `.46` 承接为唯一 current `.47`；R378 IDs 保持稳定，原来源入口直接迁移到固定 Fork，不保留长期双源 fallback。Guru manifest `0.6.15-guru.40`、Fork CLI `0.6.16` 与 Docs `.47` 是独立版本轴，均不证明 npm/tag/Release 已发布。

- `RDEC-022`（accepted historical #392 contract）：#392 将 reviewed contribution
  `architecture-contribution-392-release-v0616-guru1-v2` 与五文件 RDT contribution 绑定 expected
  immutable `.47`，serialized promotion 建立当时唯一 active `.48`。其 release mapping 收敛为
  `v0.6.16-guru.1` / extension `0.6.16-guru.41` / CLI `0.6.16` / fixed Fork full SHA；public graph
  保持 23/97/78。promotion 不授权 Publication、merge、tag、Release、full matrix、business smoke 或 Issue
  closure；promotion-created diff 必须重新进入 fresh Phase 2、task commit 与独立完整 Branch Review。

- `RDEC-023`（accepted）：#329 以 `target_native` 将 expected immutable `.48` serialized promotion 为
  唯一 active `.49`。固定 framework source 前进到 `a2003296...`、CLI `0.6.17`、package manager
  `pnpm@10.32.1`，并使受控 lifecycle 完全退出 developer identity 与 legacy workspace journal consumer；
  既有数据原字节保留。extension `0.6.16-guru.41`、released `v0.6.16-guru.1` 与 23/97/78 public graph
  不变；不新增第二 authority、adapter、compatibility layer、owner、GAP 或 ADR。


- `RDEC-025`（accepted）：#408 以 immutable `.50` 为 predecessor，`.51` 承接
  R408-01..08。仅 current source pin 前进，R329 developer-free、R378 session
  隔离及旧 lifecycle 继续适用；旧 pin 与旧 promotion 只绑定历史版本。独立手动请求不追认 Guru
  完成，不扩张 #398/#407、Evolution、GAP 或 ADR；实际证据只在 Test 层维护，知识提升不代表发布。

## #418 决策

R418-01..07 以 immutable .52 为 predecessor，由 .53 完整继承并增加隔离只读复审。
原 Merge 四出口与 Restore 不变；新增出口只接续新审查，不复制旧 pass。
release/source 四轴与 #305 Evolution target 不变。来源为
[#418 contribution](../../../requirements-design-test-contributions/418-closeout-identity-recovery/manifest.yaml)，
当前定义与双向关系为 [requirement-main.md](./requirement-main.md)、[traceability.md](./traceability.md)。

## #419 决策

- `RDEC-026`（accepted）：#419 以 `target_native` 绑定 expected immutable `.53`，由 Architecture/RDT
  serialized owners 建立唯一 active `.54`。Guru workflow 的唯一 continuation 区块独占 detailed route；
  adjacent DTO 直接消费，lost deterministic result 回原 producer，lost semantic result fresh 重跑。
- `RDEC-027`（accepted）：upstream merge candidate
  `43fffc170927c85d9f7fc106cc5a059e80d4530b` 独占 thin entry/extractor ownership；Guru 不 patch upstream
  start/continue/hooks/platform/meta。#410 独立拥有 post-merge Release Gate matrix。

## #435 决策

- `RDEC-028`（accepted historical）：#435 以 `target_native` 绑定 expected immutable `.54`，由 RDT serialized owner
  建立唯一 active `.55`；Architecture owner 同步把 reviewed contribution 与 ADR-012 提升为 `.55/active`。
- `RDEC-029`（accepted）：三个 Delivery packages 进入 active registry 与完整 distribution，但 workflow
  integration 保持 `deferred`。#434 是 production graph activation 唯一 owner；#436 是 Completion、Closure、
  Finish、Cleanup 与 Reactivate 唯一 owner。
- `RDEC-030`（accepted）：Delivery identity 使用 GitHub PR/merge、merge commit、parents、repository/base 与
  versioned trailers 重建，不新增 ledger、PR-body identity authority、adapter、dual graph 或第二 writer。
  当前 26/114/96 与 production 22/98 分开建模；完整 Release matrix 保持 `unverified`。

## #436 决策

- `RDEC-031`（accepted）：Completion、Closure、Finish、Cleanup 与 Reactivate 保持五个独立 semantic owners；任何一个 owner 的 success 不替代其它 owner 的判断或 mutation。
- `RDEC-032`（accepted）：#436 以 expected `.55` serialized promotion 建立唯一 active `.56`；五个 lifecycle packages 进入 31/136/101 registry closure 但保持 workflow-deferred，#434 仍独占 production graph activation。

## #443 决策

- `RDEC-033`（accepted）：stable task identity 与 official Trellis active-task/session store继续作为 authority；`guru-bind-task-session` 只增加 lifecycle-aware semantic owner和deterministic validator/writer，不创建第二 binding ledger、resolver或tracked session authority。
- `RDEC-034`（accepted）：#443 以 expected `.56` serialized promotion 建立唯一 active `.57`；`guru-bind-task-session` 以 active/deferred 进入 32/142/102 registry closure，production workflow保持22/98，#434仍独占global route activation和旧edge retirement。

## #452 决策

- `RDEC-035`（accepted）：平台 authority 收敛为 pinned upstream `AI_TOOLS` 完整 inventory 与目标业务仓库 exact installed selection 两层；删除 Guru-supported、dogfood-supported、deferred/unsupported 等中间集合解释。当前 pinned inventory cardinality 为 22。
- `RDEC-036`（accepted）：公开 installer 只保留重复 `--platform <cli-flag>`，用于选择去重稳定 subset；完整删除 `--all-platforms` 选项及其 manifest、upgrade、throwaway 和测试状态。canonical inventory 同时保留唯一映射的 `AITool` id 与 `cliFlag`；未指定 `--platform` 时只采用 `claude,codex,cursor` 新安装默认值，upgrade/reapply 以 manifest/provenance exact `cliFlag` selection 为准。
- `RDEC-037`（accepted）：#452 以 expected immutable `.57` serialized promotion 建立唯一 active RDT `.58`；Architecture inheritance 仍为 `.57/active`。`guru-trellis` dogfood exact selection 仍为 Claude、Codex、Cursor；OpenCode 是 upstream inventory 普通成员，不自动进入 dogfood。该 promotion 不证明实现、测试、#434 activation、tag、Release 或生产验证。

## #454 决策

- `RDEC-038`（accepted）：TaskId、TaskRef 与 lifecycle generation 分别承载 immutable identity、mutable locator 与 incarnation；named closed DTO 只携带 direct-consumer fields，Fork official primitives 保持唯一 framework authority。
- `RDEC-039`（accepted）：D0 的 old/new base、integration commit 与 review anchors 只属于当前 operation；pre-review committed reconcile、full-review ancestry 与 bounded continuity 分属 Reconcile、Task Commit、Branch Review owner，不进入 durable task identity。
- `RDEC-040`（accepted）：#454 以 expected immutable `.58` serialized promotion 建立唯一 active RDT `.59`，Architecture inheritance 为 `.59/active`。本次只提升 C2+D0；32/142/102 registry 与 22/98 production graph 不变，C3-C7、D443、D436、E434 保持后续边界。
- `RDEC-041`（accepted）：C3 checkout plan/candidate/resolution/selection、machine path 与 transaction identity 只存在于 call-local DTO/runtime；live authority 来自当前 Git common-dir/worktree facts，不建立持久 checkout path authority。
- `RDEC-042`（accepted）：#454 C3 以 expected immutable `.59` serialized promotion 建立唯一 active RDT `.60`，Architecture inheritance 为 `.60/active`。`guru-ensure-task-checkout` 仅为 planned ID；32/142/102 active registry 与 22/98 production graph 不变，完整 package/activation 仍由 E434 拥有。
- `RDEC-043`（accepted）：#454 C3 provenance 以 expected immutable `.60` serialized promotion 建立唯一 active RDT `.61`；recovery ownership只由原 acquisition marker与fresh live facts共同证明，marker不是 durable lifecycle authority。
