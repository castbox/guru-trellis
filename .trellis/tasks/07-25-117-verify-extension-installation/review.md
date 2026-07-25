# #117 Branch Review 汇总

## 审查身份与范围

- 独立 reviewer：`/root/issue117_branch_review_final`
- 角色：最终放行审查代理
- 审查 HEAD：`5ffa1077167d067130e72e3768c9e9097052f8a6`
- 完整范围：`origin/main...5ffa1077167d067130e72e3768c9e9097052f8a6`
- Merge base：`0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- 原始报告：[第 1 轮完整原始报告](reviews/001-final.md)

本轮只读覆盖 321 个 committed paths，包括 canonical Skill package、Interface、schemas、eval corpus、runtime executor/recorder/checker、public wrapper、registry、manifest、workflow graph、preset、installer、update/reapply、ownership、平台分发副本、规划 artifact 与 durable Docs SSOT。Reviewer 未修改、stage、commit、push 或创建 PR。

## Qualification 结论

### `BR-117-F1` P1：credential URL 脱敏漏检

场景属于 `normal_required_behavior`。`extension_verification_sensitive_text()` 使用 `r"https?://[^/\\s@]+@"`，raw 字符类中的 `\\s` 排除的是反斜杠与字母 `s`，不是空白。主会话只读 probe 复现：

```text
https://token@example.invalid/path        -> detected
https://user:secret@example.invalid/path  -> missed
```

AI-authored applicability、adequacy、finding 等 semantic evidence 会进入 recorder payload，而 Git remote URL parser 不覆盖这些字段。该缺陷违反 PRD 3.7、Issue #117 Redaction 和 package private-evidence 合同，可能把 credential URL 写入 tracked `marketplace-verification.json`。

状态：`open`

### `BR-117-F2` P1：task-bearing 调用未验证 task/worktree identity

场景属于 `normal_required_behavior`。`extension_verification_task_dir()` 只校验 `task_ref` 可解析为精确 `.trellis/tasks/**` 路径；execute、record、check 均未加载 `task-start-context.json` 或执行 workspace boundary 校验。主会话只读 probe 证明现存 archived task 也会被接受。

该缺陷违反 PRD 3.3 和 Interface `repository_identity` 的明确要求。普通 stale 或误路由的 `task_ref` 可把当前 worktree digest、owner artifact 与 route DTO 绑定到错误或 archived task。

状态：`open`

## 验证证据

- Runtime：584 passed，13 skipped
- Skill packages：175 passed
- Preset 与 ownership：54 passed
- Extension runtime 定向：11 passed
- Extension contract：7 passed
- Source/installed validators：12 Skills、46 exits、27 targets，通过
- Installed state：2322 managed files，0 sidecar，0 conflict
- 六份 package：各 44 files，byte digest 一致
- Overlay/ownership：43/43，drift check 通过
- `git diff --check origin/main...HEAD`：通过

既有测试全部通过，但没有覆盖上述两个正常路径缺陷。

## 文档、范围与影响

Docs SSOT strategy 为 `ssot_first`，task delta 已合并到 durable docs；但当前 runtime 未完整承接 durable redaction 与 repository identity 合同，因此实现与 Docs SSOT 不一致。Issue Scope Ledger 仍只关闭 #117；push 后 exact feature-ref clean install 保持 publication 前强制后置项。

无 CI/CD、容器、K8s、数据库 migration 或生产数据影响。`BR-117-F1` 存在 secret persistence 风险，`BR-117-F2` 存在跨 task artifact 污染和错误路由风险。

## AI Review Gate

主会话复核代码、已批准 PRD/Interface/package contract 与两个只读 probe 后，确认两个候选均为 current-scope `qualified_finding`，严重度均为 P1，且状态均为 `open`。

最终 typed exit：`implementation_required`

当前 committed branch 不得进入 publication；需返回实现阶段修复两项 finding，完成 fresh Phase 2、fresh task commit、finding closure 与 fresh final Branch Review。
