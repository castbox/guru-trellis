# #267 r20 Release Gate blocker 修复设计

## 1. Design Summary

本任务采用两个隔离修复面：

1. compatibility matrix runner 独占 before-tag availability；
2. Finalizer 与 Publication 的 package-local provenance validators 独占 safe action transition。

standalone verifier 继续负责构建 exact-SHA detached source checkout 与调用 canonical throwaway
entry。matrix runner 继续负责 matrix precondition。preset installer 继续负责生成 manifest action。
本设计不把 tag 解析移动到 verifier，不把 provenance 判断移动到 installer。

## 2. Before-Tag Resolution Design

### 2.1 Current Failure

standalone verifier 对 exact 40-hex ref 执行 `git fetch --depth=1 origin <sha>`，随后建立 detached
source checkout。`verify_trellis_compatibility_matrix.py` 在 `pre-matrix` 直接执行：

```text
git rev-parse v0.6.5-guru.10^{}
git rev-parse v0.6.5-guru.10
```

shallow checkout 没有该历史 tag，第一条命令以 exit 128 结束。runner 尚未创建任何 matrix cell。

### 2.2 Single Resolution Path

在 matrix runner 增加一个 package-local helper，输入 `repo_root` 与 `before_tag`，输出：

```text
before_tag
before_tag_object
before_commit
fetch_performed
```

执行顺序固定为：

1. 将 `before_tag` 规范化为单个 tag name；拒绝空值、parent traversal、revision operator 与非
   `refs/tags` identity。
2. 检查 exact local `refs/tags/<tag>` 是否存在，并执行 local
   `rev-parse --verify <tag>` 与 `rev-parse --verify <tag>^{commit}`。
3. local ref 存在且两项解析都成功时返回，`fetch_performed=false`。
4. local ref 存在但 tag object 或 peeled commit 任一项不可解析时，立即抛出
   `MatrixError`；不得 fetch。现有 outer terminal 将其投影为 `stage=pre-matrix`、
   `cell_id=null`，且 matrix cell count 为 `0`。
5. 只有 local ref 不存在时才执行：

   ```text
   git fetch --no-tags --depth=1 origin refs/tags/<tag>:refs/tags/<tag>
   ```

6. fetch 成功后重新执行两项 `rev-parse --verify`；两项都成功时返回，
   `fetch_performed=true`。
7. fetch 或重解析失败时抛出 `MatrixError`。现有 outer terminal 将其投影为
   `stage=pre-matrix`、`cell_id=null`、确定 command label/exit 与 credential-safe tail。

fetch 只新增 exact tag ref 与其 reachable object，不修改 checkout HEAD、index、tracked bytes、
untracked bytes 或 file modes。runner 的 source before/after identity 检查继续验证工作树未变化。

### 2.3 Test Model

focused fixture 使用本地 bare `origin`，创建一个 annotated before tag 与一个较新的 candidate commit；
source clone 只 shallow fetch candidate commit。测试固定覆盖：

| Fixture | Expected result |
| --- | --- |
| local tag absent, remote tag present | exact fetch once, object/peeled identity match |
| local tag present | zero fetch, object/peeled identity match |
| local tag present, object or peeled commit invalid | pre-matrix failure, zero fetch, zero cells |
| remote tag absent | pre-matrix failure, zero cells |
| malformed before-tag | pre-matrix failure, zero fetch, zero cells |

standalone verifier focused test继续断言 exact-SHA source checkout 使用 depth-1 fetch，并增加回归断言：
canonical throwaway/matrix path不依赖 clone 时自动取得全部 tag。

## 3. Provenance Action Transition Design

### 3.1 Current Failure

Finalizer 与 Publication 的 `provenance_tail_flatten_manifest()` 只递归 dict；list 被视为一个 scalar。
preset 初次 apply 记录每个 managed file 的 `action=installed`，reapply 对 byte-identical 文件记录
`action=unchanged`。因此 current diff 产生三个 field groups：

- `installed_at`；
- `skill_packages.files`；
- `overlays.files`。

current allowlist只包含 `installed_at`、source identity 与单个 semantic spec hash；后两个 container
因此被拒绝。

### 3.2 Closed Container Comparator

在 Finalizer 与 Publication 两个 owner 中各自增加相同语义的 package-local pure helper：

```text
provenance_tail_safe_file_action_transition(before, after, container)
```

helper 只处理 `skill_packages.files` 与 `overlays.files`。对每个 container：

1. 读取 before/after list；
2. 验证 list 长度与顺序相同；
3. 验证每个条目都是 dict；
4. 复制每个条目并移除 `action`；
5. 验证剩余 object 逐字段一致；
6. 验证 before action 是 `installed`；
7. 验证 after action 是 `unchanged`。

所有条目通过时，该 container path 从 `unexpected` 集合移除。任一条目失败时，该 container path
保持 unexpected，现有稳定 error code 不变。

`PROVENANCE_TAIL_ALLOWED_FIELDS` 不加入通配 container 字段。该常量继续表示无条件合法字段；safe
action transition 由额外结构化 comparator 判定。此设计防止 files list 中的 path/hash/mode/source/
destination/platform 变化借 action transition 绕过检查。

### 3.3 Preserved Invariants

- before manifest 继续决定 self-hosted/installed source binding；
- after source repo/ref/commit/tree-state/mutability 继续绑定 expected source；
- target checkout 继续只有 extension manifest 一个 dirty path；
- metadata-tail commit 的 parent 继续绑定 reviewed content head；
- publication head 继续是唯一 direct child；
- public profiles、schemas、typed exits 与 consumers 不变；
- installer action vocabulary `installed|unchanged|updated_managed` 不变。

### 3.4 Test Matrix

Finalizer 与 Publication owning tests 使用同一语义表：

| Before | After | Other bytes | Expected |
| --- | --- | --- | --- |
| installed | unchanged | identical | pass |
| installed | updated_managed | identical | block |
| unchanged | installed | identical | block |
| installed | unchanged | path changed | block |
| installed | unchanged | hash/mode/source changed | block |
| installed list | entry added/removed/reordered | n/a | block |

positive fixture 同时包含 skill package 与 overlay files。negative fixture逐一破坏一个 invariant，
并断言 error code 仍是 `provenance_tail_manifest_fields_outside_allowlist`。

## 4. Canonical Projection

实现先修改 `trellis/**` canonical sources。完成 focused tests 后运行：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json
```

preset apply 生成 `.trellis/guru-team/**`、`.trellis/spec/workflow/**` 与 extension manifest。实现阶段
审查 generated name-only diff，只接受 PRD 中列出的 managed projections。随后执行 dogfood drift、
canonical/installed byte parity、mode、permission、registry、consumer graph 与 sidecar-zero。

## 5. Docs SSOT Plan

策略：`no_shared_authority_change + canonical_contract_sync`。

- current Requirements `.42` 的 `REQ-017` 已规定 existing matrix 使用 immutable
  `v0.6.5-guru.10`；本任务恢复其执行前提，不修改 requirement identity。
- current Test `.42` 已拥有 exact-candidate matrix 与 pre-matrix failure contracts；本任务补 owning
  regression，不创建新 test authority。
- current Architecture `.42` 已定义 standalone verifier bounded failure、Finalizer source/target
  ownership、metadata-tail lineage 与 `.3` unverified boundary；本任务不改变 Architecture decision、
  owner、single-writer、GAP、compatibility exit 或 ADR。
- canonical contract wording在 Finalizer contract、Publication contract、quality guidelines 与
  companion scripts 中补充 exact before-tag fetch 和 closed action transition。
- `.trellis/spec/workflow/**` 只由 preset apply 从 canonical spec projection 同步。
- 不创建 RDT contribution、Architecture contribution、ADR 或 successor shared authority。

若 Planning Architecture owner 返回 architecture impact、contract incomplete、conflict 或 sync route，
本 Docs SSOT Plan 立即失效并按 typed route重做。

## 6. Validation Strategy

### 6.1 Branch-Level Proof

- matrix before-tag helper focused fixtures；
- verifier source/throwaway focused regression；
- Finalizer canonical tests；
- Publication canonical tests；
- all-platform preset apply；
- Finalizer/Publication installed tests；
- matrix/upgrade contract tests；
- source/installed package validators；
- canonical/dogfood/platform byte-mode parity；
- dogfood drift、permission、registry、consumer graph、recursive sidecar-zero；
- task validation 与 `git diff --check`。

### 6.2 Post-Merge Exact-Candidate Proof

PR merge 后从 fresh remote `main` 重新记录 candidate SHA/tree，并从零运行：

- required ancestor checks；
- predecessor `.2` 到 candidate 的 full committed diff review；
- standalone source verifier；
- 六个 platform/scenario matrix cells；
- installed business repository Publication/Finalizer full chain；
- secret、credential、private-key、signed-URL、machine-path 与 residue-zero scans；
- tag/Release existence 与 release identity checks。

branch proof不得替代 post-merge exact-candidate proof。

## 7. Architecture Impact

Planning impact：`no_architecture_impact`。

理由：本任务恢复 current `.42` 已声明的 before-state matrix 与 provenance metadata-tail normal path；
不改变系统边界、runtime owner、source/target checkout ownership、public API、typed exit、single writer、
GAP、ADR 或 compatibility exit。Implementation discovery 若要求新的 fetch owner、dual checkout role、
public contract 或宽化 allowlist，必须重新进入 Architecture impact review。

## 8. Risks And Rollback

- tag fetch refspec 过宽会污染 source identity；固定 exact `refs/tags/X:refs/tags/X` 与 `--no-tags`。
- container comparator 只看 action 会隐藏 managed drift；先移除 action，再要求剩余 object
  逐字段一致。
- Finalizer/Publication 两份实现语义漂移；两套同表 tests 与 canonical/installed parity共同门禁。
- preset apply 生成边界外文件；出现边界外 delta 或 sidecar 时停止，不覆盖、不清理证据。
- rollback 只撤销本任务未提交 delta；不得删除 worktree/task、改写 main、移动 tag 或修改业务仓。
