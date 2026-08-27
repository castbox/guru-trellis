# #311 Requirements contribution

本 contribution 修复 `BEH-008` / `BEH-010` 的 installed business Finalizer 正常路径缺口，并保持
`REQ-014` / `DES-012` 的 terminal freshness 与 verifier 隔离边界。它只形成 task-isolated candidate；
shared current 仍由 expected `.40` 的 serialized promotion owner 单写。

- `R311-01`：provenance reprepare 必须建立互相独立的 `target_reviewed_checkout` 与
  `extension_source_checkout`，前者独占业务 repository mutation，后者只提供 canonical preset bytes。
- `R311-02`：Finalizer 必须从 target reviewed manifest 解析 source `repo/ref/commit/tree_state/
  is_mutable_ref`，拒绝缺失、malformed、dirty、mutable 与非完整 commit OID。
- `R311-03`：`self_hosted` 只在 target/source canonical repository identity 相等时成立，source commit
  固定为 target `reviewed_content_head`；不得回退到 manifest 的历史 commit。
- `R311-04`：`installed` 在 identity 不等时成立，source checkout 必须由 manifest-bound canonical
  GitHub repository 的 exact OID 建立，并满足 canonical `origin`、detached HEAD、exact HEAD 与 clean。
- `R311-05`：preset apply executable 必须来自 extension source checkout，`--repo` 必须精确指向
  target reviewed checkout；source apply 前后保持 clean 且 HEAD 不变。
- `R311-06`：metadata-tail parent 必须是 target reviewed head，changed path 只有 installed manifest，
  changed fields 仍受现有 allowlist 限制，每个 reviewed head 至多一个 valid tail。
- `R311-07`：post-apply source provenance 必须按 mode 绑定：self-hosted 绑定 reviewed head；installed
  保持 manifest-bound immutable extension repo/ref/commit，绝不写成 business HEAD。
- `R311-08`：首次 `publication_ready` preview 必须先分类 exact existing PR；无 PR、无 remote branch 且
  缺 metadata tail 时，`prepared` 直接返回 `reprepare_required/provenance_metadata_tail`，push、PR create、
  archive、Ready、Issue mutation 均为零。fresh/post-bind existing-PR recovery 仍先于 provenance inference；
  public profiles、typed exits、transaction、Draft/Ready/archive/Merge handoff 与 terminal freshness不变。
- `R311-09`：source binding 与 checkout helper 归 `guru-finalize-task` package-local runtime 所有；
  Finalizer 不调用或读取 verifier profile、gate、transaction、artifact、wrapper、owner state 或 exit。
- `R311-10`：source resolution、fetch、checkout、apply 或 tail validation 失败时，在 PR、archive、Ready、
  Issue mutation 前 fail closed，并只输出稳定的非敏感 error/field locator。
- `R311-11`：canonical、dogfood installed、Shared/Codex/Claude/Cursor package bytes/modes/contracts 必须
  经 preset reapply 同步，drift 与 recursive sidecar 为零；installed package tests 必须从当前
  package/shared installed runtime 解析依赖，不得要求业务 target 携带 canonical `trellis/**` source tree。
- `R311-12`：验证范围是 package/runtime、两种 binding、installed no-source-tree fixture、一个代表性
  clean business closeout；#267 release-wide matrix、tag 与 Release 保持独立未验证边界。
- `R311-13`：standalone extension verification 失败时，必须在 temporary workspace cleanup 前保留
  schema-valid 的 failure stage、适用的 matrix cell、稳定 command label、exit code 与 bounded error
  tail；现有 stdout/stderr hash/size 继续保留。failure detail 不得包含 credential、token、认证 remote
  或环境 secret。该 evidence 只服务 #311 normal closeout 诊断，不进入 Finalizer lifecycle authority。

本 contribution 不修改 playable-ads-guru #29，不重开或关闭 #191/#195/#267/#275，不改变
Finalizer public I/O，也不建立 legacy fallback、dual-read、shared source resolver 或 Finalizer-to-verifier
re-entry。standalone verifier 只增强自身失败证据，不获得 Finalizer transaction/profile/gate ownership。
