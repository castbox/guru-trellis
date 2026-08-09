# 技术设计

## 1. 设计原则与边界

Issue #191 以当前 `main@0835de402d2f3288e6ed83d826790536fe84359a`、live Issue #191、官方 Trellis custom-workflow/marketplace 文档及现行 Guru Team contracts 为 authority。Markdown workflow/Skill/spec 负责语义判断与路由，Python/Bash 只执行或校验确定性事实。不得读取、修改、清理或复用 #179 的 worktree、branch、task/runtime、remote branch 或 Finalizer plan；#179 只用脱敏、受控 fixture 重现顺序。

## 2. 身份模型

在 Finalizer preview 与 closeout plan 中增加最小双身份：

- `reviewed_content_head`：Branch Review 通过的 commit；其 content identity 只覆盖实现、测试、durable docs 与 Guru canonical bytes。
- `publication_head`：reviewed head 的后代，最多追加一次 provenance metadata-tail；PR/ref/remote-head/verification identity 绑定此 head。

plan、Publication DTO、Verifier evidence 与 archive summary 只携带各自 consumer 必需的 40-hex identity；完整 manifest scan、apply transcript、授权和 reviewer/process 元数据仍为 owner-private runtime。

## 3. Provenance-tail producer

新增 deterministic producer/validator（归属于 Finalizer/Verifier 共享 runtime，薄 wrapper 仅 dispatch）：

1. 从 reviewed head 创建独立 detached clean source checkout，并确认 `HEAD == reviewed_content_head`、无 tracked/untracked dirty state。
2. 通过 canonical preset/overlay apply 生成安装状态；禁止直接编辑 dogfood 副本。对 canonical、dogfood、selected platform、ownership、drift、manifest sidecars 执行既有 validator。
3. 读取 preimage/postimage，要求唯一 tracked diff 只落在 `.trellis/guru-team/extension.json` 允许字段：`installed_at`、`source.ref`、`source.commit`、`source.tree_state`、`source.is_mutable_ref`；要求 `source.ref == source.commit == reviewed_content_head`、`tree_state=clean`、`is_mutable_ref=false`，无其它 task content 或 sidecar。
4. 生成一个 metadata-tail commit，记录 parent reviewed head、changed-path/field proof、manifest digest 与 reviewed identity；禁止再次 apply 或将 tail 重新分类为 reviewed content。
5. 仅在上述事实全部通过且 remote branch 仍为 reviewed head/可 fast-forward 时返回 producer-passed DTO；其余返回 implementation-required 或 blocked，verifier 维持 `extension_source_not_clean` fail-close。

## 4. Verifier 与 Finalizer recovery

Verifier source selection 接受 manifest clean immutable provenance，并同时输出 reviewed/publication identity。Exact OID remote verification 要求 source checkout bytes 与 reviewed head 一致，target/ref/PR identity 与 publication head 一致；任何 identity drift/stale source 重新进入 owner gate。

Finalizer 在 `content_pushed` 且尚未 PR/archive/archive-commit 的窗口检查 failure classification。仅当 failure 是允许 tail 缺失/旧 plan publication head 失效，且 issue、scope、title/body、base、verification profile、reviewed content 与 remote FF 前置均未变化时：

- 将旧 plan、gate、verification request 标为 superseded 并删除短生命周期 runtime；不删除 tracked task artifact，不持久化授权。
- 返回 `reprepare_required`，workflow 通过现有 Finalizer consumer 自动进入 `reprepare_preview`。
- 重新执行 tail producer，构造 unchanged reviewed identity + new publication head 的新 plan/preview；旧确认不跨 plan 复用。
- 当前对话展示唯一新副作用计划，用户回复 `确认继续` 后 FF push publication head，重新 exact-ref verification，再继续 Draft PR/archive/Ready。

PR 已存在、archive 开始、scope/reviewed content 变化、non-FF、并行 consumer 或 provenance diff 越界均不适用，精确 blocked/implementation-required。

## 5. Public graph 与同步面

沿用 `guru-finalize-task` 的稳定 `reprepare_required` 出口；其 deterministic executor 在 tail 完成并删除旧 plan/gate/request 后，向 `reprepare_preview` 最小投影 `task_ref`、`reason_code`、`branch_review_commit`、`publication_head`，target 仅补 `profile/mode`。preview 直接校验 current HEAD、直接父提交和 allowlisted tail，不依赖已删除的旧 plan。更新 canonical packages/runtime 后，同步：

- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`；
- `trellis/skills/guru-team/packages/{guru-finalize-task,guru-verify-extension-installation,guru-create-task-commit}`、registry/interface/schemas/examples/tests；
- canonical preset/overlay、installed runtime、`.agents/.codex/.claude/.cursor` discovery copies；
- README 与 durable workflow/preset/docs specs。

## 6. Failure matrix

| 场景 | 结果 |
| --- | --- |
| detached clean source、唯一允许字段、reviewed/ref/commit 一致、无 sidecar | 生成一次 tail，publication head 前移 |
| dirty source、mutable ref、source commit mismatch | `extension_source_not_clean`/blocked |
| managed bytes、ownership、platform、drift 或 sidecar 不完整 | blocked，不生成 tail |
| 非允许 tracked diff 或混入 task content | implementation_required，不自动继续 |
| PR/archive 已开始、scope/content/base/profile 改变 | blocked 或 publication stale，回到既有 owner |
| remote 非 fast-forward 或存在并行 publication consumer | blocked |
| 仅 pre-PR tail 缺失且其它 identity 不变 | supersede + `reprepare_required`，新 plan/确认 |

## 7. Docs SSOT Plan

- 状态：`stale_docs`；策略：`ssot_first`。
- 先更新 `.trellis/spec/workflow/{workflow-contract,skill-package-contract,companion-scripts,data-contracts,quality-guidelines}.md`、`.trellis/spec/preset/{installer,overlay-guidelines,upstream-ownership}.md`、`.trellis/spec/docs/public-docs.md`，补充双 HEAD、tail producer、pre-PR supersession、side-effect/authorization 与验证矩阵。
- 再同步 canonical workflow/Skill/runtime/preset/README 和平台副本；不以 dogfood copy 反向定义 canonical 语义。
