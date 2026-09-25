# 非功能需求与边界

当前 .65 来源：reviewed #454 D443 contribution + inherited immutable `current-main-0.6.17-guru.64` authority；上游固定为 `castbox/Trellis@eb370008c7689d4e272ae626bd002190ecbb3296` / CI `35621578090` / CLI/core `0.6.17`，Guru manifest `0.6.17-guru.42`，release target `v0.6.17-guru.1`。Architecture inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.65` / `active`。
完整继承 immutable `.64`，当前增量为 #454 D443 非激活 Bind canonical package major；active registry 保持 32 packages / 142 exits / 102 commands 与六个 planned IDs，production workflow 保持 22 mandatory invokes / 98 exits。

`.65` 完整继承 immutable `.64` 并吸收 reviewed #454 D443 contribution；RDT 与 Architecture current 均为 `.65/active`。提升前 focused evidence 不证明 promotion-created diff；该 diff 仍须 fresh Phase 2、Task Commit 与完整 Branch Review，D436、E434、#434 activation、installed/platform 和 Release matrix 均未完成或验证。

版本：`current-main-0.6.17-guru.65`；状态：`active`；predecessor：`current-main-0.6.17-guru.64`；source baseline：reviewed #454 D443 contribution + inherited immutable `.64` authority；精确 revision 由 containing Git object/tree identity 绑定。

C5 不增加独立 NFR identity：沿用 `NFR-002/003/005` 的最小 DTO、stale fail-closed 与敏感信息边界；
runtime 只保存 Git common-dir 的 portable ownership/incarnation，不记录绝对 checkout locator、用户授权或第二
session store。C5 focused `113/113` 与 schema evidence 只支持提升前 candidate，不替代 post-promotion gates。

- `NFR-001`：canonical source 是长期源头；dogfood 与平台副本必须可从 preset/overlay 重建。
- `NFR-002`：public DTO 只携带唯一 consumer 必需的最小 identity/freshness；Git/live 可重建事实与授权不得持久化。
- `NFR-003`：unknown/multiple/unmapped exit、stale identity、缺失 mandatory Skill 必须 fail closed。
- `NFR-004`：验证按 Issue ownership 最小化；普通 docs/spec Bootstrap 与 repo-private release
  orchestration contract task 不运行完整累计多平台或 exact release-candidate matrix。
- `NFR-005`：日志、Issue、PR、task、evidence 不得泄露 secret、token、数据库 URL、客户数据。
- `NFR-006`：release orchestration 不保存 tracked release lifecycle、动态 checklist、payload body、
  用户授权或可重新推导状态；reviewed-content 只覆盖实际 delivery bytes，owner-private checkpoint
  保持最小且在 consumer 完成后退休。
- `NFR-007`：developer-free lifecycle 不以 legacy identity/workspace 数据的存在与内容改变结果；
  受控更新必须保持这些用户历史数据的 path、mode 与 bytes，且不为其建立 adapter 或第二 authority。
- `NFR-008`：framework source、CLI、package manager、generated assets 与 installed source record 必须
  exact 一致；任一 stale/mismatch 在写入或成功声明前 fail closed，不回退到全局或可变来源。

## 兼容与未验证边界

| 边界 | 当前状态 | Owner |
| --- | --- | --- |
| Trellis CLI `0.6.15` source/dogfood | `verified`：manifest、project version、ownership 与 drift gate | #260 current source |
| `0.6.5 -> 0.6.15` official migration | `verified`：三个 existing platform cell | #260 |
| replacement release `v0.6.5-guru.10` | `published`：annotated tag、zero-asset non-prerelease Release 与 consumer proof | #275 historical baseline |
| 完整多平台 Throwaway matrix | `verified`：`claude|codex|cursor × clean|existing` 6/6，sidecar/unknown drift 均为 0 | #260 |
| latest stable `v0.6.15-guru.4` / extension `0.6.15-guru.39` / Trellis `0.6.15` | `published`：作为 #332 predecessor 与 current stable 使用 | live Release / Issue #332 |
| historical #332 target `v0.6.15-guru.5` / extension `0.6.15-guru.40` / Trellis `0.6.15` | 历史 evidence 边界 | Issue #332 exact-candidate Release lifecycle |
| 正式 `.5` installed business-repository Publication/Finalizer 全链 | `unverified`；#311 已完成前置，fresh release 安装态验收由 #332 承接 | Issue #332 Release Gate |
| workflow source | `public_plus_local_candidate`；证明 public marketplace + exact local candidate compatibility，不证明 `.37` tag-pinned install | #260 / 重构前稳定版 Release boundary |

普通 task 的文档增量进入 `docs/requirements-design-test-contributions/<task-ref>/` 或经 semantic owner 判定的 narrow direct sync；两个并行 task 不写同一个 shared current 文件。Architecture 变化使用独立 impact/promotion route。该规则是维护责任边界，不是锁或并发协议。

## #378 当前边界

| 边界 | 当前状态 | Owner |
| --- | --- | --- |
| 固定 Fork CLI/core 0.6.16 | reviewed source/installed focused evidence；不是发布证明 | #378 |
| 完整历史 predecessor / 多平台矩阵 | `unverified`；定向调度测试不替代执行 | 专项 compatibility / #332 Release owner |
| 独立 TypeCheck | `unverified`；build/test 通过不替代独立检查 | Fork/source validation owner |
| 真实业务 #31/#127 接续 | `unverified` | 各业务 owner |
| remote tag / npm / GitHub Release / tag-pinned smoke | `unverified` | 独立发布 owner |

前表的 official 0.6.15 与六 cell PASS 为继承历史，不适用于当前 Fork 0.6.17 candidate。

## #392 非功能与证明边界

| 边界 | 稳定合同 | Owner |
| --- | --- | --- |
| `.48` Architecture/RDT authority | historical `reviewed_promoted`；现为 immutable superseded，`.47` 为其 predecessor | serialized Architecture/RDT promotion owners |
| release mapping | reviewed historical contract：`v0.6.16-guru.1` / `0.6.16-guru.41` / CLI `0.6.16` / fixed Fork full SHA | #392 preparation delivery |
| post-promotion fresh Phase 2/commit/Branch Review | promotion-created diff 必须绑定 fresh identity；完整 review 前 Publication 不可达 | Phase 2 / Task Commit / Branch Review owners |
| preparation merge 与 post-merge exact candidate | merge 使用 reviewed expected head；随后 fresh-fetch `origin/main` 并冻结唯一 candidate | Publication / Finalizer / Merge / release owner |
| full throwaway matrix、business smoke、secret scan、residue gate | 只接受同一 exact candidate 的 live proof；历史或 focused evidence 不可复用 | #392 exact-candidate Release Gate |
| annotated tag、tag-pinned smoke、GitHub Release、Issue close、cleanup | 每项 fresh-read live authority，并保持独立 mutation boundary | 各 live action owner |

该 `.48` 历史 promotion 不新增 public Skill、typed exit、schema、compatibility adapter、第二 release
state machine 或 runtime owner artifact；public graph 保持 23 Skills / 97 exits / 78 commands。

## #329 非功能边界

- legacy absent/present-A/present-B 只作为 preservation fixture，不成为身份、恢复或 authenticity boundary。
- #329 原 source 为 Fork `a2003296...`，该 pin 现由 R408-01 替代；CLI `0.6.17`、`pnpm@10.32.1`；extension 仍为
  `0.6.16-guru.41`，released repository axis 仍为 `v0.6.16-guru.1`。
- 完整 source/focused/installed 验证可以支撑本 candidate，但不证明 push、PR、merge、tag、Release、
  marketplace publication 或业务生产结果；这些边界保持 `unverified` 直到对应 owner fresh 完成。


## #408 继承与证明边界

R408-01..08 定义于 [requirement-main.md](./requirement-main.md)，不新增非功能机制。
NFR-001..008、developer retired-zero、旧 lifecycle 与 23/97/78 graph 完整继承。
同源构建、明确 session、普通 stale/mismatch 与独立操作报告属于正常正确性边界；不引入锁、
TOCTOU、进程/FD authority、自动恢复或对抗性测试。

已审查的 source/installed/native 证据和 mock/远端未验证限制只在
[Test 计划](../../../test/versions/current-main-0.6.17-guru.56/test-plan.md) 维护。
本知识 snapshot 不声明新的 runtime 执行、post-promotion gate、远端 mutation 或 Release 完成。

## #418 兼容与证据边界

R418-01..07 复用 NFR-001..008，不增加锁、并发压力、TOCTOU、crash consistency 或对抗性机制。
仅 Finalizer 原 executor 拥有既有映射的精确归档收敛；四个新 profile 都保持零业务 mutation。
在 #418 增量完成时，23/100/78 与业务 22 invokes/98 exits 是 additive graph；`.54` 吸收 #419
producer recovery command 后的历史 graph 为 23/100/79。该增量不替换普通 Merge 四出口、Branch Review
input 4.0/gate 7.0、原 mutation path、closure ownership 或 Restore。新增 input 5.0/archived-1.0
的实际定义由 canonical package 持有，见同版本 Design。

继承版本的 pin、graph、矩阵和发布状态只绑定其历史版本；.54 不改变 extension 0.6.17-guru.42、
CLI/core 0.6.17、repository axis v0.6.17-guru.1 或 fixed Fork 43fffc170927c85d9f7fc106cc5a059e80d4530b。
pre-promotion 证据与未验证项集中见 [Test 计划](../../../test/versions/current-main-0.6.17-guru.56/test-plan.md)；
native 语义执行、原业务实例、完整 Release matrix 仍 unverified。

## #419 非功能与验证边界

- continuation authority 只存在于 canonical workflow 的唯一结构化区块；不新增 global stage store、
  semantic resolver、持久化 confirmation 或跨 Skill private-state reader。
- recovery 必须保持 producer ownership、exact task/base/HEAD/content/authority freshness 与 fail-closed route。
- exact upstream 只证明 continuation thin-entry 依赖；#419 不执行 throwaway、安装、更新、workflow-switch
  或 release-grade preset-reapply matrix，也不把中断结果记为缺口或证据。
- promotion-created diff 必须 fresh 通过 Phase 2、Task Commit 和独立完整 Branch Review 后才能进入 Publication。

## #435 非功能与验证边界

- Delivery Review、Publish、Merge 各自保持 semantic owner、owner-private short-lived state、closed typed exits
  与唯一 consumer；确认只存在当前对话，不进入 tracked authority、checkpoint、DTO 或 archive。
- 三个新 package 是 active/deferred：canonical、installed、Shared/Codex/Cursor/Claude 与 installer inventory
  必须一致，但 #434 前不得进入 production workflow mandatory marker graph。
- Delivery history 只使用正常 Git/GitHub/task identity facts；不新增 ledger、PR-body identity reader、旧输出
  adapter、dual runtime graph、squash/rebase fallback 或第二 lifecycle router。
- #435 predecessor registry 为 26 packages / 114 exits / 96 commands；promotion 后 `.56` current registry
  为 31 packages / 136 exits / 101 commands；production workflow 仍为 22 mandatory invokes / 98 exits。
  #434 独占 graph activation，#436 独占 Completion/Closure/Finish/Cleanup/Reactivate。
- pre-promotion package、integration、representative clean install/reapply 与 independent Branch Review 证据不跨
  `.55` content identity 复用。完整 Release matrix 仍 `unverified`。

## #443 非功能与验证边界

- session binding 是短生命周期 owner-private state；public output 排除 runtime binding id、绝对路径、完整 live snapshot、authorization、semantic pass 与 recovery internals。
- base provenance 只能来自 task metadata 或既有 mapping，不能从调用时 live base HEAD 反推；missing/stale/mismatch 在任何 binding/mapping write 前停止。
- 五个 profile/route 对形成 schema/runtime 闭集；合法重试复用同一 official mapping，不新增第二 resolver、binding ledger、lifecycle store、adapter 或 dual graph。
- #443 integrated range 为 `a74d729e..4dd9f7b7`；当前 canonical package 26 tests PASS。current registry 为 32/142/102，production workflow 保持 22/98。
- package 保持 workflow-deferred；完整 Release matrix、#434 activation、真实生产 binding 与 promotion-created diff 的 fresh gates 仍需独立完成。

## #452 非功能与验证边界

- 平台集合只有 pinned upstream inventory 与目标仓库 exact installed selection 两层；默认三平台、`guru-trellis` dogfood 三平台及 OpenCode 的成员身份都不得被解释为额外支持层。
- upstream inventory 当前基于固定 source identity 为 22 个平台；重复 `--platform` 形成 exact subset。公开 CLI 不提供全集安装选项，旧 `--all-platforms` 作为未知参数在写前失败。
- 无参数默认选择只适用于新安装的 Claude、Codex、Cursor；upgrade/reapply 必须读取并原样保持已安装 selection，不得因默认值、dogfood 或 inventory 演进扩张或收缩。
- canonical 全平台 projection 与当前 dogfood installed selection 分开验证；`guru-trellis` dogfood 仍只安装 Claude、Codex、Cursor，OpenCode 仅作为 upstream inventory 普通成员参与显式选择。
- 本 `.58` 是 Requirements knowledge promotion，不是实现或测试证据。#434 production graph activation、完整 release matrix、annotated tag、tag-pinned smoke、GitHub Release、业务仓库生产验证与 Issue closure 均保持 `unverified` 或未授权，直到各自 owner fresh 完成。

## #454 非功能与验证边界

- TaskId、TaskRef 与 lifecycle generation 必须分离；公共 DTO 使用 closed schema，并排除 machine path、session、authorization、generic evidence 与未声明 Git facts。
- Fork official task/session primitives 保持唯一 framework authority；Guru C2 runtime 不写 task/session/mapping，不修复 metadata，不选择 semantic route，也不持久化 validation result。
- Schema loader 只读取固定 sibling contract root，拒绝 remote/parent refs、nested `$id`、symlink escape 与 unknown DTO；schema/runtime repository 与 branch value domain 必须一致。
- 不建立第二 store、durable identity index、workspace mapping reader、compatibility alias、dual-read 或 dual-write；operation-scoped base pair 不得成为长期 identity。
- `.59` 只提升 C2+D0；C3-C7、D443、D436、E434、registry activation、完整 installer/upgrade/Release matrix 与生产 mutation 保持后续边界。

## #454 C3 非功能与验证边界

- checkout path、candidate snapshot、selection 与 transaction identity 只保留在 call-local runtime；不得进入 durable task、session、branch association、resource ledger 或跨 Skill public handoff。
- live facts 必须来自当前 common-dir 与 registered worktrees；不读取 workspace mapping、历史 checkout path 或 installed runtime state作为 authority。
- rollback 只删除本 transaction 创建且 identity 仍匹配的资源；caller-owned resource 永不由 C3 删除或改写，output-loss recovery 只读。
- recovery continuity 由 Git administrative directory 中的 owner-private marker 与 fresh live facts共同证明；marker 不是 durable task/session/branch/resource authority。
- same-path/same-branch/same-HEAD replacement 缺少原 marker时必须 fail closed；不得仅凭 path、branch、HEAD 或 live existence投影 Guru cleanup ownership。
- direct handoff 在 consumer invocation 前 retire marker；existing-checkout reuse不写 marker，marker lifecycle失败只回滚本 transaction创建且仍匹配的资源。
- planned ID 不等于 active package。active selector、workflow、graph、installed/platform bytes 不得因 C3 promotion 改变。
- `.61` 只提升 C3 provenance delta；package `19/20`、shared runtime `119/128`、lifecycle integration `38/44`、preset 272 with 2 errors/3 skips、完整 Release matrix 与生产 mutation 保持未通过/未验证边界。

## #454 C4 非功能与验证边界

- Durable branch binding 严格排除 path、HEAD、session、authorization、ownership payload 与 transaction snapshot；这些事实只服务当前 operation。
- Candidate label/id 不是 freshness token；所有 mutation 与 recovery 必须以 reviewed expected HEAD、epoch/revision、exact task artifact 与 fresh live Git facts闭合。
- same-checkout route 必须保持 HEAD、真实 index bytes、Git-visible working-tree bytes 与 status identity；existing-target route 不迁移内容且要求 clean/ancestor-compatible。
- C4 不新增 C5 ledger representation、第二 branch/session store、alias、dual-read、dual-write、锁、TOCTOU 或 crash-consistency协议。
- 三个 lifecycle owner IDs 保持 planned；active registry 32/142/102、production workflow 22/98、installed/platform bytes 均不因 `.62` promotion改变。
- Focused lifecycle `93/93` 是提升前 candidate evidence；preset `85/86` 未通过，完整 Release matrix 与 promotion-created diff 的 fresh gates 保持未验证。

## #454 D443 验证边界

- Bind canonical source 需通过 package graph、实际 Fixed Fork schema-2 fixture、真实 Git checkout 与
  TaskId/generation（含 0）路由测试；旧 mapping/path 无 target reader/writer。
- 本轮提升前 Bind 12/12、source graph 与 Python compile 通过；全局 package 19/20 的 Closure `$ref`
  错误不归因 D443，也不报告全量通过。E434 installed/platform 与 #410 Release matrix 未验证。
