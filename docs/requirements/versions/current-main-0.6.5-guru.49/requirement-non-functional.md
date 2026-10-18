# 非功能需求与边界

当前 .49 来源：`castbox/Trellis@a2003296b4c4ce46c50d72ead3b2ec9c317f69fc` / CLI/core `0.6.17`；Guru manifest `0.6.16-guru.41`；repository release target `v0.6.16-guru.1`。Architecture public inheritance：`docs/architecture/README.md` / `current-main-0.6.5-guru.49` / `active`。
继承段落中的旧版本映射、矩阵及历史 promotion 只绑定其原版本，不声明当前 Fork 的完整兼容或 Release；当前 #329 增量见本文件末节及同版本 traceability。


版本：`current-main-0.6.5-guru.49`；状态：`active`；predecessor：`current-main-0.6.5-guru.48`；source baseline：reviewed #329 contribution + inherited immutable `.48` authority；精确 revision 由 containing Git object/tree identity 绑定。

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
- current source 为 Fork `a2003296...`、CLI `0.6.17`、`pnpm@10.32.1`；extension 仍为
  `0.6.16-guru.41`，released repository axis 仍为 `v0.6.16-guru.1`。
- 完整 source/focused/installed 验证可以支撑本 candidate，但不证明 push、PR、merge、tag、Release、
  marketplace publication 或业务生产结果；这些边界保持 `unverified` 直到对应 owner fresh 完成。
