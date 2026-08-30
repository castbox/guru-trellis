# #267 pre-tag findings 修复设计

## 1. Design Summary

本任务采用三个互相隔离的修复面：

1. Finalizer provenance reprepare 从 reviewed target manifest 派生精确 platform argv；
2. RDT 与 Architecture owner 对 active `.42` 执行 latest-stable fact repair；
3. 对 archived #312 单行机器路径执行 repo-neutral sanitation。

三项修复共享 #267 release owner，但不共享实现 owner。Finalizer canonical package 独占 runtime
行为，RDT/Architecture lifecycle 独占 shared authority，archived task 文件只承载历史文本修订。

## 2. Finalizer Platform-Preservation Design

### 2.1 Current Failure

`trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py` 的
`prepare_provenance_metadata_tail()` 在 isolated extension source checkout 中执行 canonical
preset apply，但 argv 固定含 `--all-platforms`。对只安装 Claude projection 的 target，该命令
会增加 Codex/Cursor managed paths，随后 `provenance_tail_git_status_paths()` 正确拒绝
manifest 之外的 dirty paths。

### 2.2 Single Derivation Path

新增一个 package-local pure helper，从 parent installed manifest 返回完整 apply platform argv。
helper 只读取以下 current manifest fields：

```text
install.selected_platforms
install.all_platforms
skill_packages.selected_platforms
overlays.selected_platforms
```

校验顺序固定为：

1. 四个 locator 存在且类型正确；
2. 三个 selected-platform lists 均为排序、去重、非空集合；
3. 每个成员属于 canonical `claude|codex|cursor` closed set；
4. 三个集合完全相同；
5. `all_platforms=true` 时集合必须与 canonical full set 完全一致；
   `all_platforms=false` 保留显式选择语义，可覆盖任意非空集合，包括显式选择完整三平台。

成功 projection：

```text
all_platforms=true
  -> ["--all-platforms"]

all_platforms=false
  -> ["--platform", platform_1, ..., "--platform", platform_n]
```

Finalizer 不依赖 preset 的 implicit platform fallback；重复 `--platform` 明确绑定 parent
installed identity。校验失败统一抛出 Finalizer `WorkflowError`，reason code 固定为新的
platform-selection invalid code，并发生在 apply subprocess 之前。

### 2.3 Preserved Invariants

- extension source checkout 只提供 canonical preset bytes；
- target reviewed checkout 独占 metadata mutation 与 commit；
- `reviewed_content_head` 不变；
- publication head 仍是单一 direct-child metadata tail；
- allowed manifest field set 不扩大；
- public Finalizer profiles、typed exits、schemas 与 consumers 不变。

### 2.4 Test Model

更新 Finalizer apply fixture，使 parser 接受 repeated `--platform` 与 `--all-platforms`，并记录
收到的 platform identity。测试矩阵固定覆盖：

| Parent selection | Expected argv | Expected target delta |
| --- | --- | --- |
| `claude` | `--platform claude` | manifest only |
| `codex` | `--platform codex` | manifest only |
| `cursor` | `--platform cursor` | manifest only |
| `codex,cursor` | repeated `--platform` | manifest only |
| full set + `all_platforms=true` | `--all-platforms` | manifest only |
| missing/unknown/duplicate/mismatched set | no apply call | zero target/source writes |

## 3. Active Authority Repair

### 3.1 RDT Repair

`guru-maintain-requirements-design-test-ssot:repair` owns the direct correction of
`requirement-main.md` latest-stable paragraph。新 current fact 固定为 `.2/.38/CLI 0.6.15` 与
live tag object/peeled commit。`requirement-non-functional.md`、test plan 与 design manifest
中的 `.10/.36/CLI 0.6.5` 是 existing-migration before-state，保持原文。

### 3.2 Architecture Repair

`guru-maintain-architecture-baseline:repair` owns `ARCH-CUR-005` 与 `EVD-002`。修订只替换
latest stable evidence，并保留 #275 replacement release history。该修复不改变 Architecture
decision、boundary、owner、single-writer、GAP、ADR 或 compatibility exit。

完成两项 repair 后重新调用
`guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`。预期 route 是
`baseline_current`，impact 是 `no_architecture_impact`：Finalizer 修复恢复既有 installed
platform identity contract，authority 修订恢复 live fact，不建立新 architecture mechanism。
若 owner 返回 impact/conflict/contract-incomplete，则停止 plan approval 并按该 typed route
处理。

## 4. Archived Path Sanitation

将 #312 archived `implement.md` 中的机器绝对路径替换为
`<business-repository-task-worktree>`。上下文继续表达 downstream live proof 的执行位置；文本
不再绑定用户名、home directory 或本机目录结构。该编辑不参与 current RDT/Architecture
authority。

## 5. Docs SSOT Plan

策略：`ssot_first`。

- Finalizer behavior SSOT：canonical package runtime 与 owning tests；installed package 只由
  preset apply 生成，禁止双写实现。
- latest stable Requirements SSOT：active `.42` `requirement-main.md`，通过 RDT repair owner
  写入。
- latest stable Architecture SSOT：`ARCH-CUR-005` + `EVD-002`，通过 Architecture repair
  owner 写入。
- historical migration before-state：`.10/.36/CLI 0.6.5` 原文保持，不提升为 latest。
- `.trellis/spec` 当前未把 `.10` 声明为 latest stable，也未定义相反 platform-reprepare
  机制；本任务无 spec projection 写入。Phase 3 fresh scan 若发现直接冲突，返回 Docs SSOT
  reconciliation，不在实现中临时复制 authority。
- #312 archived path sanitation 是历史 artifact hygiene，不形成新的 durable behavior authority。

## 6. Validation And Release Evidence

### 6.1 Branch-Level Proof

- Finalizer canonical/installed focused tests；
- platform selection unit matrix 与 zero-call failure tests；
- preset apply `--repo . --all-platforms --json`，随后 canonical/installed byte parity；
- dogfood overlay drift、package validator、registry/consumer graph、permission 与 sidecar-zero；
- active `.42` latest-stable uniqueness scan；
- scoped `/Users/` path scan；
- task validation、workspace boundary 与 `git diff --check`。

Branch evidence 证明修复实现，不证明 published exact candidate。

### 6.2 Post-Merge Exact-Candidate Proof

PR merge 后从 fresh remote `main` 记录 candidate commit/tree，重跑：

- required ancestor checks；
- predecessor `.2` tag object/peeled commit checks；
- predecessor-to-candidate full committed diff review；
- live-derived complete platform × clean/existing matrix，重点复核 `claude-clean`；
- installed business repository Publication/Finalizer provenance reprepare full chain；
- secret/sensitive-path/residue-zero scans。

任一 evidence 跨 SHA、FAIL、SKIP、stale 或 residue 非零时，candidate freeze 失效。

## 7. Risk And Rollback

- 平台字段校验过宽会保留错误 manifest，过窄会拒绝合法 subset；closed-set table 与五个
  positive cells、六类 malformed cases 共同锁定边界。
- authority 全仓替换会破坏 existing migration before-state；只修改三个 exact current paths。
- generator 可能产生边界外 drift；apply 后先审查 name-only 与 sidecar，再运行测试。
- rollback 只撤销当前 task 未提交 delta；不得删除 task/worktree、移动 tag、rewrite main 或
  修改业务仓。
