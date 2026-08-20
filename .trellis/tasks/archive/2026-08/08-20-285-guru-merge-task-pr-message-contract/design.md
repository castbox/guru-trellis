# #285 技术设计

## 1. 设计原则

- AI 负责 message authoring、充分性与一致性判断；Python 只做结构校验、live facts、确定性 merge 和 post-merge 验证。
- Public DTO 只携带 Merge Skill 直接消费的最小 reviewed message；用户授权只留在当前对话。
- expected-head、close scope、typed exits、terminal recovery 和资源清理边界保持不变。
- Active contract 通过显式新版本迁移；旧 1.0 schema/example bytes 不修改。

## 2. Public I/O

### 2.1 Finalizer -> Merge Skill

Finalizer `ready_for_merge` output 继续提供：repo、PR、expected head、base/head branches、close Issues。Finalizer Interface 的 consumer contract 增加 Merge owner authoring field：

```json
{
  "reviewed_merge_message": {
    "primary_issue": 285,
    "summary": "修复 Merge Skill 中文提交消息承接",
    "subject": "chore(merge): #<pr> 合并 #285 修复 Merge Skill 中文提交消息承接",
    "body": "<fixed Chinese merge body>"
  }
}
```

`ready_for_merge` 与 `standalone_merge` 共享同一 nested contract。subject/body 是 executor 的直接输入；primary Issue/summary 是 semantic gate 与 deterministic validator 的直接依据。

### 2.2 Versioning

- 新增 active 2.0 input aggregate/profile schemas、examples 和 private gate schema。
- Interface 1.4 仍保持 Interface 版本，但其 active profile 显式选择 2.0 schema id/path。
- 1.0 文件保留为 legacy inventory，测试同时固定其 bytes/hash 并禁止 active selector 回退。
- Finalizer output 1.0 不变；仅 consumer authoring seed contract 与 projection/eval expectation 更新。

## 3. Semantic gate 与 deterministic validation

### 3.1 Message builder/validator

在 package-local `guru-merge-task-pr` runtime 中建立单一 builder/validator：

- builder 使用 PR number、primary Issue、summary、head/base 生成 subject/body；
- validator 对外部 authored payload 做 exact reconstruction 比较；
- summary 至少含一个 CJK 字符且非占位文本；
- body 固定 `合并/范围/审计/PR/Refs` 段落，禁止 close keyword；
- standalone/workflow 共用相同实现。

legacy formatter 调用同一个 package-local builder/validator，但不得成为 current Skill 的隐藏前置文件/命令。

### 3.2 Live facts

pre-merge facts 增加 repo-bound expected base ref/head identity；继续读取 PR、checks、reviews、mergeability、policy、close Issues。facts digest 覆盖这些字段，checker 重读后必须完全相等。

### 3.3 Private gate

2.0 gate 保留 current input、facts digest、semantic review、route，并增加 reviewed message digest与 pre-merge base head 的明确 schema binding。授权状态不进入 gate。

## 4. Executor data flow

```text
reviewed public input
  -> semantic recorder + live facts digest
  -> checker rere读 PR/head/base/policy/Issue/message identity
  -> materialize ignored merge-body file
  -> gh pr merge --repo --match-head-commit --merge --subject --body-file
  -> always cleanup body file
  -> reread PR + commit + base ref + Issues
  -> terminal output persisted for idempotent recovery
  -> public invocation consumes output and retires gate/runtime residue
```

body file 固定位于现有 gate identity 目录中：

```text
.trellis/.runtime/guru-team/task-pr-merge/<identity>/merge-body.md
```

写入前验证目录、symlink 和 residue；使用 `try/finally` 清理。terminal recovery 入口也先执行同一 cleanup helper。

## 5. Post-merge verifier

通过 repo-bound `gh` 读取：

- merged PR identity；
- merge commit message 与 parents；
- expected base ref 当前 SHA；
- close Issue state/closed_at。

成功条件：

```text
merge commit SHA == PR mergeCommit.oid == remote expected base ref
parents == [pre-merge base head, expected head]
commit subject/body == reviewed subject/body
PR/primary Issue refs and close-keyword rule pass
all existing closure timing rules pass
```

任何 message/parent/base mismatch 在 merge 已发生时不得伪装成 `merged`；按当前 terminal failure contract fail closed，并保留足够诊断供 bounded recovery。不得用额外 Issue close 或 local main sync 修复。

## 6. Distribution 与一致性

Canonical package 是唯一源：`trellis/skills/guru-team/packages/guru-merge-task-pr/`。实现后通过 preset apply 生成/同步：

- `.trellis/guru-team/skills/packages/guru-merge-task-pr/`
- `.agents/skills/guru-merge-task-pr/`
- `.codex/.claude/.cursor` 及 manifest 声明的其他平台 copies
- registry/contracts/consumers/installed manifest 与 preset tests

不得手工只修 dogfood copy。若 apply 产生 `.new`/`.bak`，逐个审查并清零 sidecars。

## 7. Docs SSOT Plan

- Profile：`guru-maintain-requirements-design-test-ssot:task_impact_sync`。
- 预期 route：为 #285 建立 additive contribution，包含 `requirements.md`、`design.md`、`test.md`、`traceability.md`、`manifest.yaml`。
- Current `.37` 是否 promotion 由该 Skill 依据 contribution 完整性和 current authority 判定；任务代码不得自行改写入口矩阵。
- Architecture Baseline：`no_change`，因为域、组件、集成 ownership 和部署边界不变；只修复既有 Merge Skill 内部合同闭环。
- README/spec/data contracts/quality guidelines 属于 runtime-facing durable contract，随代码同步修改，不以 task-local PRD 替代。

## 8. 风险与回滚

- 风险：输入 schema 迁移漏掉 Finalizer consumer/evals/platform copy。控制：public graph、registry、installed discovery 和 all-platform parity tests。
- 风险：临时 body file 泄漏或 stale reuse。控制：gitignored fixed owner dir、symlink/residue guard、finally + recovery cleanup 测试。
- 风险：fake GitHub harness 只返回 SHA，未模拟 message/parents。控制：扩展 harness，并用真实隔离 GitHub repo 证明。
- 风险：post-merge 已发生后验证失败。控制：terminal output 不返回成功，输出明确诊断；不重复 mutation，不自动修复历史。
- 回滚：回退 active 2.0 selector与实现改动即可恢复旧路径；旧 1.0 assets 未改写。已产生的不合规真实 merge 不允许历史重写，只能作为失败证据。
