# #311 技术设计：Finalizer extension source 与 target reviewed checkout 分离

## 1. Design Principles

1. `target_reviewed_checkout` 拥有业务 repository mutation；`extension_source_checkout` 只提供
   canonical installer implementation。
2. target commit lineage 与 extension source provenance 是两个身份域；validator 分别绑定，不把
   业务 HEAD 写成外部 extension commit。
3. Finalizer package-local helper 独占 source binding 与 checkout，不调用 verifier lifecycle。
4. self-hosted 与 installed 使用一个 binding model 的两个 closed mode，不建立 dual-read 或 fallback。
5. Python 只解析 manifest、检出 Git object、执行 preset、校验 diff 与 commit；AI/workflow 继续拥有
   publication readiness、route 与副作用授权。
6. canonical source、installed runtime 与平台 discovery copy 作为一个 managed delivery unit 同步。

## 2. Current To Target

```text
Current
target business repo @ reviewed_content_head
  -> detached checkout named source
  -> look for target/trellis/presets/.../apply_guru_team_trellis_preset.py
  -> path missing in installed business repo
  -> Finalizer stops before metadata-tail

Target
target business repo @ reviewed_content_head
  -> detached target_reviewed_checkout
  -> read installed manifest source binding
  -> resolve detached clean extension_source_checkout @ exact source commit
  -> extension-source/apply_guru_team_trellis_preset.py --repo target-reviewed
  -> validate binding-aware manifest-only diff
  -> commit one target metadata-tail child
  -> ff target branch to publication_head
```

## 3. Private Binding Model

Finalizer runtime 在当前调用内构造一个 private binding；不写 tracked 或 ignored artifact：

```json
{
  "mode": "self_hosted | installed",
  "target_repo": "owner/repo",
  "target_reviewed_head": "<sha40>",
  "source_repo": "owner/repo",
  "source_locator": "https://github.com/owner/repo.git",
  "source_ref": "<sha40>",
  "source_commit": "<sha40>"
}
```

Binding rules：

- `self_hosted`：`target_repo == manifest source.repo`。本次 source commit 固定为
  `target_reviewed_head`；source checkout 从 target Git object 建立 detached worktree。
- `installed`：`target_repo != manifest source.repo`。本次 source repo/ref/commit 固定为 manifest
  的 clean immutable identity；source checkout 通过 canonical locator 与 exact-OID fetch 建立。
- 两种 mode 均要求完整 source commit、clean checkout、detached HEAD、canonical `origin` 与
  `HEAD == source_commit`。
- repo identity 相同但 reviewed head 缺 canonical apply entry 属于 self-hosted contract failure；不得
  回退到 manifest 的旧 commit。
- repo identity 不同但 manifest source 不完整属于 installed contract failure；不得搜索本机 checkout、
  `main`、PATH package 或 global install。

## 4. Source Resolution

### 4.1 Manifest read

从 target reviewed commit 中读取 `.trellis/guru-team/extension.json`，校验：

- current manifest schema 与 extension identity；
- source repo 是 canonical GitHub locator；
- source ref 与 commit 存在，commit 是 40-hex OID；
- `tree_state=clean`；
- `is_mutable_ref=false`。

解析在任何 source fetch 或 target apply 前完成。错误输出保留 field/reason 定位，不包含 remote
credential 或敏感 header。

### 4.2 Installed exact-OID checkout

installed mode 使用独立临时目录执行：

```text
git init <extension-source>
git remote add origin <canonical-source-locator>
git fetch --depth=1 origin <source-commit>
git rev-parse --verify FETCH_HEAD^{commit}
git checkout --detach <source-commit>
```

随后验证 remote identity、HEAD、detached state 与 clean status。fetch result 必须精确命中 manifest
commit；短 SHA、branch tip、mutable `main` 与 peeled mismatch 均阻断。

### 4.3 Self-hosted checkout

self-hosted mode 从 target repository 创建独立 detached worktree，commit 固定为 reviewed head。
它与 target reviewed checkout 路径分离，因此 apply script 的 source root 与 `--repo` target root
始终不同。

### 4.4 Reuse boundary

实现固定在 `guru-finalize-task` package 内增加私有 source binding 与 checkout helper。它复用该
package 已有的 GitHub repository normalization、Git command 与 error primitives，不抽取 verifier
owner code，不新增 shared source-resolution API，也不迁移 verifier profile、schema、gate、evidence、
transaction 或 typed exits。

## 5. Apply And Tail Validation

执行入口固定为：

```text
<extension_source_checkout>/trellis/presets/guru-team/scripts/python/
  apply_guru_team_trellis_preset.py
    --repo <target_reviewed_checkout>
    --all-platforms
    --json
```

apply 后执行四层校验：

1. source checkout 仍保持原 HEAD 与 clean status；
2. target status 只有 `.trellis/guru-team/extension.json`；
3. manifest field diff 位于 `PROVENANCE_TAIL_ALLOWED_FIELDS`；
4. post-apply source binding 与本次 private binding 一致。

Binding-aware postconditions：

| Mode | target parent | post-apply source repo | post-apply source ref/commit |
| --- | --- | --- | --- |
| `self_hosted` | reviewed head | target canonical repo | reviewed head |
| `installed` | reviewed head | manifest canonical source repo | manifest immutable source commit |

`source.repo` 不进入新增 allowlist；它必须与 preimage 保持一致。`installed_at` 与已声明的
`semantic-retrieval.md` managed hash 继续服从现有 allowlist。任一额外 path、field、sidecar、mode、
task content 或 config 变化均阻断 commit。

commit 后验证：

- parent 只有 reviewed head；
- changed path 只有 installed manifest；
- postimage binding 与 mode 一致；
- current HEAD 是新 publication head；
- reviewed head 是 publication head 的直接 parent。

## 6. Pre-PR Detection And Recovery

`finalizer_pre_pr_provenance_tail_required()` 使用同一 binding resolver：

- self-hosted manifest 已绑定 reviewed head 且 clean immutable 时不创建 tail；否则进入现有
  `provenance_tail_required` reprepare。
- installed target 在 current HEAD 仍是 reviewed head 时进入一次 metadata-tail reprepare；已有
  binding-aware valid tail 时由 `finalizer_publication_identity()` 识别并禁止第二个 tail。
- matching post-bind existing-PR transaction 继续短路 pre-PR inference。

public graph 不变：

```text
ready
  -> preview reprepare_required
  -> checked Finalizer side-effect gate
  -> prepare source/target checkouts + one target tail
  -> reprepare_preview
  -> ordinary publication transaction
  -> ready_for_merge
```

source-resolution failure 不生成新 public exit；它沿 current `blocked` contract 停止，并保留当前
Finalizer owner 的可恢复状态。

## 7. Test Design

### 7.1 Focused unit/contract

- binding resolver：self-hosted、installed、repo mismatch、manifest missing/malformed、dirty、mutable、
  non-OID commit。
- source checkout：canonical origin、exact-OID success、fetch mismatch、dirty checkout、apply entry
  missing。
- tail validator：self-hosted reviewed binding、installed extension binding、source repo drift、business
  HEAD 被误写为 source commit、allowlist 越界、extra path、second tail。
- recovery ordering：post-bind transaction 先行；pre-PR only；remote/plan/scope drift 保持阻断。

### 7.2 Installed package regression

构造不含 canonical source tree 的 clean business repository，安装 current candidate，创建 task
reviewed commit，再从 installed Finalizer wrapper 执行：

```text
Publication ready -> preview -> reprepare_required -> execute
-> reprepare_preview -> deterministic transaction fixture -> terminal projection
```

fixture 必须断言 apply executable 来自 extension source checkout，所有 target mutation 位于 business
checkout，Finalizer verifier call count 为零。

### 7.3 Representative closeout

在 disposable GitHub business repository 执行一个 closeout，证明 exact remote push、唯一 Draft PR、
archive、Ready 与 archive 后 `ready_for_merge`。该验证在执行前单独展示 repository、branch、Issue、
PR 与 cleanup 副作用并取得当前对话授权。它不声明 #267 release-wide compatibility。

## 8. Distribution And Docs

Canonical edit surface：

- `trellis/skills/guru-team/packages/guru-finalize-task/**`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 与 installer tests，前提是
  source provenance contract 必须调整
- `trellis/presets/guru-team/**`、`trellis/workflows/guru-team/**` 的说明与 managed inventory
- `.trellis/spec/workflow/**`、`.trellis/spec/preset/installer.md`、`.trellis/spec/docs/public-docs.md`
- task-owned RDT/Architecture contribution 与 ADR candidate

运行 canonical validation 后，用 preset `apply.sh --repo . --all-platforms` 同步
`.trellis/guru-team/**`、`.agents/**`、`.codex/**`、`.claude/**`、`.cursor/**`。任何 conflict、
`.new`、`.bak` 或 sidecar 必须先精确检查，再进入后续 gate。

## 9. Architecture And RDT Impact

- Architecture impact：`architecture_impact`。
- Change path：`target_native`。
- Current boundary：一个 target checkout 同时被误当成 business mutation owner 与 extension source
  implementation owner。
- Target boundary：target reviewed checkout 只拥有业务 repository tail；extension source checkout
  只拥有 canonical implementation bytes。
- Current/target semantic owner：`guru-finalize-task` deterministic runtime；installer 继续拥有 manifest
  source provenance；verifier owner 不进入 business Finalizer。
- Single writer：task worktree 写 task contribution；shared current 只由 Architecture/RDT promotion
  owner 写入。
- Compatibility exit：旧 single-checkout assumption 在本 task 完成后删除，不保留 fallback 或 dual-read。
- ADR：`required=true`，因为本 task 改变 checkout ownership、source binding 与 target commit lineage
  之间的 architecture decision。
- RDT impact：新增 #311 requirement/design/test trace，shared `.40` 在 task implementation 阶段不直接
  修改。

## 10. Risks And Controls

| Risk | Control |
| --- | --- |
| external source commit 被业务 HEAD 覆盖 | mode-specific postcondition 与 regression fixture |
| source fetch 未配置 canonical origin | 固定 init/origin/fetch 顺序并校验 remote identity |
| apply 错写 source checkout | apply `--repo` 只接受 target reviewed path，前后分别检查两棵 worktree |
| verifier lifecycle 被复用进 Finalizer | static call scan 与 package boundary test |
| mixed canonical/installed graph | all-platform reapply、package validator、byte/mode parity、sidecar-zero |
| shared current 并行冲突 | task-owned contribution + expected `.40` serialized promotion |
| 验证扩张到 Release Gate | focused package + 一个 representative closeout；#267 matrix 保持独立 |

## 11. Rollback

- source validation 或 focused tests 失败时，不执行 preset reapply。
- reapply 产生 conflict 时，停止 activation，保留 target 与 sidecar 证据；不得强制覆盖。
- representative closeout 失败时，保留现有 release/PR/Issue state，按同一 Finalizer transaction
  诊断；不得重复创建 PR 或手工绕过 gate。
- 若实现要求改变 public exit、transaction state、verifier boundary 或 Issue scope，立即返回 Phase 1。
