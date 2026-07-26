# #117 Branch Review 汇总

## 审查身份与范围

- 当前问题发现 reviewer：`/root/issue117_branch_review_final_afterfix`
- 审查 HEAD：`538def79408d417107c3adae61c4466116395d96`
- 完整范围：`origin/main...538def79408d417107c3adae61c4466116395d96`
- Merge base：`0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Round 1/2 原始报告：[初始 finding 报告](reviews/001-final.md)
- Round 3 原始报告：[F1/F2 closure 报告](reviews/002-closure.md)
- Round 4 原始报告：[新 finding 报告](reviews/003-final.md)

Round 3 独立复核确认 `BR-117-F1` 与 `BR-117-F2` 已关闭。Round 4 原本按 fresh final review 分派，但完整审查当前 committed range 后发现新的 current-scope finding，因此已透明登记为问题发现审查轮，不能作为 zero-finding 最终放行。

## 已关闭 finding

### `BR-117-F1` P1：credential URL 脱敏漏检

状态：`closed`

Round 3 复核了 authority-userinfo 检测、artifact write 前 fail-closed、generic public error、5 类独立 probe、Shared production eval、secret scan 与 canonical/installed bytes。关闭证据绑定 [F1/F2 closure 报告](reviews/002-closure.md)。

### `BR-117-F2` P1：task-bearing 调用未验证 task/worktree identity

状态：`closed`

Round 3 复核了 active task、task-start-context、repo、branch、active pointer 与 workspace boundary 统一 gate，并覆盖 wrong task、archived task、wrong repo、wrong branch、wrong worktree 与 taskless standalone。关闭证据绑定 [F1/F2 closure 报告](reviews/002-closure.md)。

## 当前 open finding

### `BR-117-F7` P2：recorder 未执行输入 schema，并接受不存在的 supersession lineage

场景属于 `normal_required_behavior`。Package 已发布 `semantic-review-input.schema.json` 与 `execution-facts.schema.json`，但 recorder 只检查顶层 keys；普通嵌套类型错误会在字段访问时抛出未捕获 `AttributeError` 或 `TypeError`，而不是稳定的 `WorkflowError`。没有 prior `marketplace-verification.json` 时，任意 `supersedes_verification_ref` 也会被持久化并产生 checker-valid 的错误 lineage。

该问题违反 PRD 3.3、Design 5.2/5.3 以及 package `Private evidence`、`Exits and re-entry` 合同。输入结构错误和首次调用误带 stale re-entry ref 都是 honest-but-fallible 的正常路径，不依赖恶意篡改、伪造或非常规并发。

状态：`open`

修复必须在访问嵌套字段或写 artifact 前执行已发布 schema 校验并统一转换为受控 `WorkflowError`；`supersedes_verification_ref` 只能在 exact prior owner artifact 存在且匹配时出现。需要补 malformed nested type、missing/invalid enum 与 no-prior/nonmatching/exact-prior supersession 回归。

## 验证证据

- Runtime：588 passed，13 skipped
- Skill packages：175 passed
- Preset：45 passed
- Ownership 与 extension contract：16 passed
- Source/installed validators：12 Skills、46 exits、27 targets
- Installed state：2322 managed files，0 sidecar/removal/conflict
- Shared、Codex source/installed production eval：各 7/7
- Full local-source throwaway：exit 0
- `git diff --check origin/main...HEAD` 与相关 `compileall`：通过

既有自动化通过，但未覆盖 F7 的 malformed recorder input 和 no-prior supersession 正常负例，不能反证该 finding。

## 文档、范围与影响

Docs SSOT strategy 为 `ssot_first`。Canonical package contract、workflow specs、durable requirements、README、registry/manifest、installer 与平台分发副本总体同步；但 runtime 尚未完整承接已声明的 schema 与 supersession freshness 合同，因此实现和 Docs SSOT 仍不一致。

Issue Scope Ledger 仍只关闭 #117。Exact pushed feature-ref clean install 保留为授权 push 后、创建 PR 前的 publication gate，当前 local-source throwaway 不冒充该证据。

完整 diff 未修改 CI/CD、容器、Compose、K8s/Kustomize、数据库 migration、Makefile、dependency manifest 或生产数据面。F7 影响 recorder correctness 与 gate lineage，不扩大生产或数据副作用。

## AI Review Gate

主会话复核 raw reports、已批准 PRD/Design/package contract、当前代码路径与独立复现后，确认 `BR-117-F7` 是 current-scope `qualified_finding`，严重度 P2，状态 `open`。

最终 typed exit：`implementation_required`

当前 committed branch 不得进入 publication。修复 F7 后必须重新完成完整 Phase 2、fresh task commit、finding closure 与独立 fresh final Branch Review。
