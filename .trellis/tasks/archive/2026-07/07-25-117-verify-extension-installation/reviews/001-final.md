# Branch Review 原始报告

## 审查范围

- HEAD：`5ffa1077167d067130e72e3768c9e9097052f8a6`
- Diff：`origin/main...HEAD`
- Merge base：`0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- 规模：321 files，36354 additions，942 deletions
- 角色：fresh final Branch Review，只读，未修改、stage、commit、push 或创建 PR

## 未修复问题

### P1 F1：credential URL 脱敏正则存在漏检

文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18218`

当前正则为：

```python
r"https?://[^/\\s@]+@"
```

raw regex 字符类中的 `\\s` 排除的是反斜杠和字母 `s`，不是空白字符。因此：

```text
https://token@example.invalid/...        -> detected
https://user:secret@example.invalid/...  -> missed
```

`parse_github_remote_repository_url()` 虽会拒绝带凭据的 Git remote，但不能保护 AI-authored applicability、adequacy、finding 等 semantic evidence。漏检内容可被 recorder 写入 task-local `marketplace-verification.json`。

Qualification：

- 场景：`normal_required_behavior`
- 结论：`qualified_finding`
- 违反：PRD 3.7、Issue #117 Redaction、package contract
- 影响：token、secret 或 credential URL 可能进入 tracked private artifact
- 修复要求：更正 URL 检测逻辑，并覆盖含 `s`、空白、用户名密码和多种 userinfo 的 artifact/wrapper/eval 回归

### P1 F2：task-bearing 调用未验证 task/worktree identity

文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:25221`

`extension_verification_task_dir()` 只确认 `task_ref` 能解析为精确路径。execute、record、check 均未加载 `task-start-context.json`，也未执行 workspace boundary 校验。

只读 probe 证明 archived task 也会被接受：

```text
.trellis/tasks/archive/2026-07/07-04-18-enforce-pr-publish-only-after
-> accepted as extension verification task_dir
```

随后 runtime 会把当前 worktree content digest 与该错误 task 拼接，并可能向错误 task 写入 owner artifact。Interface 的 `repository_identity` 明确要求 execute、record、check 前重建 task mapping；PRD 3.3 也要求 Validator 校验 task/worktree。

Qualification：

- 场景：`normal_required_behavior`
- 结论：`qualified_finding`
- 影响：普通 stale/misrouted `task_ref` 可污染其他或 archived task，并生成错误路由 DTO
- 修复要求：对 task-bearing workflow/standalone 统一加载 task context、验证 active task、branch/worktree/repository mapping，并补 wrong-task、archived-task、wrong-worktree 回归

## 已检查文件

- 完整 committed diff
- canonical Skill package、Interface、schemas、examples、eval corpus 和 wrappers
- runtime executor、recorder、checker、public wrapper
- registry、manifest、workflow graph 和 consumer contracts
- preset install、update/reapply、ownership、sidecar 和 overlay
- canonical、installed、Agents、Codex、Claude、Cursor 六份分发副本
- PRD、design、implement、planning、Phase 2、commit handoff 和 durable Docs SSOT

## 验证结果

- Lint：通过，`git diff --check origin/main...HEAD`
- TypeCheck：不适用；Python compile evidence 已由 current Phase 2 覆盖
- Runtime tests：584 passed，13 skipped
- Skill package tests：175 passed
- Preset/ownership tests：54 passed
- Extension runtime 定向测试：11 passed
- Extension contract tests：7 passed
- Source/installed validators：通过，12 Skills / 46 exits / 27 targets
- Installed state：2322 managed files，0 sidecar，0 conflict
- 分发一致性：六份 package 均为 44 files，byte digest 相同
- Overlay/ownership：43/43，drift check 通过

现有测试全部通过，但未覆盖上述两个正常路径缺陷。

## 证据交接

- Planning approval 与 Phase 2 evidence 均完整且绑定 committed HEAD。
- Docs SSOT strategy 为 `ssot_first`，task delta 已合并。
- Durable docs 明确要求 credential URL redaction 和 task/worktree mapping；当前 runtime 未完整承接，因此 current-scope Docs SSOT 与实现不一致。
- 唯一既有 nonblocking 后置项仍是 push 后 exact feature-ref clean install。
- 当前 worktree 有主会话 liveness 产生的两个 task artifact 修改；本审查固定 committed range，未触碰这些修改。
- 无 CI/CD、容器、K8s、数据库 migration 或生产数据影响。
- F1 具有 secret persistence 风险；F2 具有跨 task artifact 污染和错误路由风险。

## 结论

最终 typed exit：`implementation_required`

存在两个 open P1，当前分支不能通过 Branch Review Gate。该报告可作为 finding-fix 实现轮次和后续 fresh final review 的输入。
