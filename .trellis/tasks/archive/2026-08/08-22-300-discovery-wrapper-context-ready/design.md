# #300 技术设计：Discovery wrapper 与 managed workflow switch 一致性修复

## 1. Design Boundary

本 task 不改变 #295 已发布的 Sync `base_current`、Discovery input 2.0、owner-result 3.0、
`context_ready|refresh_base|blocked` 或 Clarify projection。它修复两个现有合同的执行缺陷：

- semantic owner/checker 到 public dispatcher wrapper 的 transport/validation/projection；
- verifier 对受管理 global `.trellis/workflow.md` 的 preview、ownership 判断与显式替换。

## 2. Discovery Diagnostic Flow

```text
public invocation envelope
  -> declared package wrapper
  -> installed launch.sh / run-skill-command
  -> managed Python resolver
  -> package and command inventory validation
  -> Discovery runtime/invoke.py
  -> observe_base_current
  -> validate + check_owner_binding
  -> context_ready / refresh_base / blocked schema projection
```

对同一 fixture 依次记录 owner recorder stdout、checker stdout、package-local binding 与真实
wrapper stdout。首个结论分歧点拥有修复；下游不得吞掉可分类的正常错误后假装问题已解决。

## 3. Discovery Correctness Rules

- 合法 current envelope 只能投影 schema-valid `context_ready`。
- live base 正常 advance 投影 `refresh_base`；结构、authority、owner 或 runtime mismatch 投影
  现有声明的 `blocked`。
- dispatcher 只执行确定性 package/command/runtime 校验，不重新做 semantic 判断。
- public DTO 不新增 private payload、review evidence、绝对 locator 或诊断堆栈。
- 回归 fixture 必须从 public wrapper 进入；direct import 仅可用于定位首个分歧点。

## 4. Managed Workflow Switch Flow

```text
ownership/provenance precheck
  -> remove only stale expected preview owned by this verifier
  -> trellis workflow ... --create-new
  -> validate .trellis/workflow.md.new against expected marketplace candidate
  -> validate current workflow is known managed and replaceable
  -> trellis workflow ... --force
  -> validate active workflow bytes/markers
  -> consume expected preview and assert zero unresolved sidecars
```

若 current workflow 为未知或用户修改，流程在 `--force` 前稳定阻塞并保留原文件与 preview；
不得把“文件存在”或单个 marker 命中当作 managed ownership 证明。失败清理只处理本次 verifier
创建且已验证身份的临时对象，原始失败必须保持为唯一主错误。

## 5. Distribution And Documentation

- Canonical owner 位于 `trellis/skills/guru-team/**` 与
  `trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py`；受支持的
  single-repository compatibility 入口位于
  `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`，两者必须执行同一
  managed-before/preview/explicit-force 合同。
- canonical package/runtime、wrapper 或 overlay 变化后，通过 preset reapply 同步
  `.trellis/guru-team/**`、`.agents/.codex/.claude/.cursor` 声明投影，并运行 drift/sidecar
  检查。
- README 与 canonical `trellis/presets/guru-team/spec/workflow/quality-guidelines.md`
  必须与实际 verifier 一致描述 `--create-new` preview、受管理状态验证、显式
  `--force` 和 user-modified preservation；preset reapply 后 dogfood
  `.trellis/spec/workflow/quality-guidelines.md` 必须 byte-equal canonical，不得再声称
  preserve contract “never uses --force”。

## 6. Validation Design

### Discovery

- current owner：record/check/public wrapper 均通过且 public exit 为 `context_ready`；
- invalid schema、stale base、dirty/wrong/missing/ambiguous authority、owner mismatch；
- source wrapper、installed wrapper 与 managed Python resolver transcript；
- public output schema 与 Clarify projection。

### Workflow switch

- known managed workflow：preview 校验后 active switch 成功；
- unknown/user-modified workflow：保留原文件，不进入 force replace；
- malformed/mismatched preview、已有 `.new` / `.bak` / sidecar：稳定 fail closed；
- update/reapply 前后均验证 workflow bytes、ownership checkpoint 与零 sidecar；
- failure path 保留原始错误，不产生 cleanup 次生错误。
- 默认 matrix 与 `GURU_TEAM_THROWAWAY_SINGLE_REPO_COMPATIBILITY=1` 两个受支持入口均覆盖
  上述成功与 fail-closed 合同；后者不得删除未知 preview 或绕过 managed-before 判断。

### External boundary

- 一个 representative clean/isolated throwaway 属于 #300 accepted scope；
- #267 full multi-platform Release matrix 明确 deferred；
- 合并到 live `main` 后由 fresh #287 candidate 重跑其声明验证，结果不得由本地 candidate
  检查替代。

## 7. Architecture And Risks

本修复保持现有 owner、public graph 与交互方向，为 `no_architecture_impact`。主要风险与控制：

| Risk | Control |
| --- | --- |
| 测试只证明 direct import | success fixture 必须执行真实 wrapper |
| 修复放宽 fail-closed | current 与 invalid/stale/mismatch 配对测试 |
| `--force` 覆盖用户修改 | preview 前后均绑定 managed ownership；未知状态在 force 前阻塞 |
| 只修 dogfood 副本 | canonical 先改，reapply 后检查所有投影与 drift |
| #299/#287 scope 混淆 | ledger 不预先关闭 Issue；#299 为已完成前置，#287 仅消费 fresh evidence |
