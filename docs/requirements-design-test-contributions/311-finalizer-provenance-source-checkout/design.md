# #311 Design contribution

## Closed binding resolver

- `D311-01`：Finalizer 从 target reviewed commit 读取 installed manifest，复用 package-local GitHub
  repository normalization 与 Git command primitives，构造 invocation-local closed
  `self_hosted|installed` binding；binding 不持久化，也不进入 public DTO。
- `D311-02`：binding 分别包含 target repo/reviewed head 与 source repo/locator/ref/commit。target 与
  source identity 相等时只选择 `self_hosted`；不等时只选择 `installed`，没有 fallback 或 dual-read。
- `D311-03`：`self_hosted` 从 target Git object 创建独立 detached source worktree；`installed` 在独立
  tempdir 执行 `git init -> remote add origin -> exact-OID fetch -> checkout --detach`，随后复核 canonical
  origin、HEAD、detached state 与 clean status。

## Apply and validation ownership

- `D311-04`：target reviewed checkout 始终由 target repository 在 reviewed head 建立；apply script 从
  extension source checkout 定位，`--repo` 只接收 target reviewed path。
- `D311-05`：apply 后依次验证 source checkout identity/clean 不变、target dirty path 精确为 manifest、
  manifest diff 位于既有 allowlist、postimage source binding 与 mode 一致，之后才创建 target tail commit。
- `D311-06`：tail commit validator 同时消费 reviewed target lineage 与 source binding。它复核 direct
  parent、single commit、manifest-only path、mode-specific repo/ref/commit 与 current publication head。
- `D311-07`：`finalizer_publication_identity()`、pre-PR detector、prepare/commit/validate 使用同一 private
  binding contract。preview 先执行 side-effect-free existing-PR classification；无 PR 且初始 state 为
  `prepared` 时，再以同一 detector 映射 provenance reprepare。首次 reprepare preflight 接受 absent remote
  或精确 reviewed head，仅拒绝非空且不匹配的 remote head；fresh/post-bind recovery 均在 source resolution
  之前保持优先级。
- `D311-08`：source checkout 与 target checkout 分别 cleanup；任一失败均不触碰 caller/sibling
  worktree，不产生 public新 exit，也不继续远端 mutation。

## Distribution and authority

- `D311-09`：semantic source 只在 canonical Finalizer package、直接 owning specs/README 与 preset
  source中修改；all-platform preset apply 生成 dogfood/Shared/Codex/Claude/Cursor copies，生成副本不反向
  成为 source。package tests 通过当前 package root 定位 shared runtime/adapter，使同一测试在
  canonical 与 installed layout 中成立，不建立对 target canonical source tree 的隐式依赖。
- `D311-10`：installer 继续独占 installed manifest provenance production；Finalizer只消费并为当前
  tail重放 canonical apply。verifier 仍是 standalone source-repository lifecycle owner，与 business
  Finalizer 零依赖。
- `D311-11`：task worktree 单写本 RDT/Architecture candidate；shared `.40` 不在实现阶段直接修改，
  independent full-diff review 后由两个 promotion owner 串行生成 successor。
- `D311-12`：compatibility matrix runner 在 pre-matrix、matrix-cell 与 post-matrix 异常边界投影 bounded
  structured failure；throwaway wrapper 透传该终态，`guru-verify-extension-installation` outer owner 在
  cleanup 前解析并绑定到 command evidence。schema/example/tests 同步收敛，无法解析的 failure output
  显式分类，不静默退化为 hash-only。成功路径、asset inventory、capability 与 Finalizer verifier-zero
  dependency 保持不变；matrix 外 command 或 inventory/ownership/sidecar/capability postcheck 失败以
  `postcheck_failure` 收敛，failed execution 禁止 null failure。

架构 before/after、required concerns 与 compatibility exit 由
`docs/architecture/contributions/311-finalizer-provenance-source-checkout.md` 和 ADR-007拥有；本文只承接
RDT design responsibilities，不复制 Architecture判断。
