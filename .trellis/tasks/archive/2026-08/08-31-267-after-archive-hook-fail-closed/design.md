# #267 after_archive hook fail-closed Release Gate 修复设计

## 1. Design Summary

把 official `after_archive` hook preflight 放到 `finalization_preview_context()` 的 common entry，位置
固定在 `finalization_eval_preview_context()` 之前。这样 normal、eval-staging、preview 与 execute 的
preview-context consumer 在选择任一 downstream context 前先完成同一 fail-closed 检查。

`prepare_closeout()` 中现有 preflight 保留，作为 direct caller 的独立 defense。本设计不引入新
dispatcher、public field、typed exit 或 runtime owner。

## 2. Current And Target Control Flow

### 2.1 Current failing flow

```text
preview / execute gate check
  -> finalization_preview_context
     -> finalization_eval_preview_context
        -> eval context exists
           -> early return
              -> official_after_archive_hook_state never runs
```

### 2.2 Target flow

```text
preview / execute gate check
  -> finalization_preview_context
     -> official_after_archive_hook_state
        -> non-empty hook: stable WorkflowError, zero side effects
        -> empty or absent hook: continue
     -> finalization_eval_preview_context
        -> eval context or normal closeout path
```

Direct caller 仍走：

```text
prepare_closeout
  -> official_after_archive_hook_state
  -> existing preparation logic
```

## 3. Runtime Change

canonical owner 的唯一行为修改：

```python
def finalization_preview_context(root, args, public_input):
    official_after_archive_hook_state(root)
    eval_context = finalization_eval_preview_context(root, public_input)
    ...
```

调用位置必须在 eval helper 之前。把调用放在 early return 之后、只放进 eval helper、或从
`prepare_closeout()` 删除既有调用，均不满足设计。

预期重复调用只发生在 normal path 进入 `prepare_closeout()` 时。函数是 read-only preflight；重复读取
config 不改变任何 repository 或 provider state。保留 direct-path defense 比消除一次读取更重要。

## 4. Test Design

### 4.1 Canonical focused preview test

fixture 固定满足：

- `GURU_TEAM_EVAL_STAGING=1`；
- eval context 已配置且本来会被 early return；
- `.trellis/config.yaml` 含一个非空 `hooks.after_archive` command；
- command 只会创建一个 test-local sentinel。

调用 `finalization_preview_context()`，断言：

- 抛出 `WorkflowError`；
- payload 精确包含 `stage=after-archive-hook-preflight`、`hook_executed=false`、
  `configured_command_count=1`；
- eval helper 未产生可消费 context；
- sentinel 不存在。

### 4.2 Canonical focused execute test

复用 execute 当前 gate-check 调用 `finalization_preview_context()` 的真实路径，断言同一 payload，并对
archive、push、PR create/edit/query 与 Ready mutation 使用 mocks 证明零调用。测试不得直接调用
preflight helper 来替代 execute-path coverage。

### 4.3 Existing coverage preservation

- `prepare_closeout()` direct caller tests 继续证明现有 defense 未删除。
- hook 缺失与空 list 正常路径继续通过。
- malformed config、非 regular config、unreadable parser 与非 string command 的既有 fail-closed
  coverage 继续通过。
- installed end-to-end fixture 保持 current assertions，不把 failure 改为 PASS/SKIP，并禁止
  publication-owner dirty-path rejection 替代 hook-preflight payload evidence。

## 5. Canonical Projection

实现顺序固定为：

1. 修改 `trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py`。
2. 修改 `trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py`。
3. 运行 focused canonical tests。
4. 执行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json`。
5. 检查 generated diff，只接受 Finalizer installed runtime projection、task artifacts 与
   canonical/installed contract projection。
6. 运行 dogfood drift、canonical/installed byte-mode parity 与 package/runtime suites。

预计 implementation file boundary：

- `trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py`；
- `trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py`；
- `.trellis/guru-team/skills/packages/guru-finalize-task/runtime/owner.py`；
- 本 task 的 planning/finish artifacts；
- `trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md`；
- `.trellis/guru-team/skills/packages/guru-finalize-task/references/contract.md`。

出现其它 tracked path 时停止并重新审查 scope，不自动吸收。

## 6. Contract And Compatibility

- public input/output schema：不变。
- typed exits 与 consumers：不变。
- Finalizer/Publication ownership：不变。
- `stage`、`hook_executed` 与 configured count payload：不变。
- normal closeout、eval-staging closeout 与 installed business-repository semantics：从 current bypass
  收敛到既有 fail-closed contract。
- migration：无数据迁移、config migration 或 tag migration。
- rollback：在提交前只撤销本 task 精确 delta；不得改写 main、删除 worktree/task、移动 tag 或修改
  business repository。

## 7. Docs SSOT Plan

采用 `no_shared_authority_change + canonical_contract_test_sync`：

- `.42` Requirements/Design/Test/Architecture authority 保持不变；
- 本任务不新增 contribution、ADR、GAP、owner 或 compatibility exit；
- runtime 与 owning tests 提供新证据；
- canonical Finalizer contract 增补 common preview/execute hook preflight 的既有 fail-closed invariant；
- installed projection 只由 preset apply 生成，不手工形成第二实现路径。

## 8. Architecture Impact

Planning impact：`no_architecture_impact`。

理由：变更恢复 current `.42` 已要求的 Finalizer fail-closed invariant；不改变 public API、system
boundary、Finalizer owner、source/target ownership、single-writer、Architecture decision、GAP lifecycle、
compatibility exit 或 Release identity。Implementation discovery 若要求新增 owner、公共合同版本、
parallel path 或 shared authority change，必须重新进入 Architecture impact review。

## 9. Risks And Controls

- 风险：只修 eval helper 会遗漏 execute 或其它 caller。控制：preflight 位于 common preview context
  entry，并用 preview 与 execute 两条 focused test 证明。
- 风险：删除 `prepare_closeout()` 调用造成 direct-path regression。控制：保留调用与现有测试。
- 风险：installed fixture 因 publication-owner dirty detection 提前失败，掩盖 hook contract。控制：
  focused test 精确断言 hook payload；installed fixture 继续接受两种既有 fail-closed owner evidence，但新
  matrix 必须整体 PASS。
- 风险：preset apply 产生边界外 delta。控制：审查 exact name-only diff；发现额外 path、`.new`、`.bak`
  或 sidecar 即停止。
- 风险：branch proof 被误当 Release proof。控制：post-merge 从 fresh candidate 重跑六单元 matrix 与
  全部 #267 pre-tag gates。
