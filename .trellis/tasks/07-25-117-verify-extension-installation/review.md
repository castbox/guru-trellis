# #117 Branch Review 汇总

## 审查身份与范围

- 当前实现前 reviewed HEAD：`3bfbd100c8d75a619da19627e7da276a3f2e367b`
- 完整 committed 范围：`origin/main...3bfbd100c8d75a619da19627e7da276a3f2e367b`
- Merge base：`0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Round 1/2 原始报告：[初始 finding 报告](reviews/001-final.md)
- Round 3 原始报告：[F1/F2 closure 报告](reviews/002-closure.md)
- Round 4 原始报告：[F7 finding 报告](reviews/003-final.md)
- Round 5 原始报告：[F7 closure 与 F8 finding 报告](reviews/004-f7-closure.md)

Round 3 独立复核关闭 `BR-117-F1` 与 `BR-117-F2`。Round 4 发现
`BR-117-F7`；Round 5 独立复核关闭 F7，同时发现 `BR-117-F8`。本文件记录当前
implementation candidate，不替代下一轮 fresh Phase 2、task commit、finding closure
或 zero-finding final review。

## 已关闭 finding

### `BR-117-F1` P1：credential URL 脱敏漏检

状态：`closed`

Round 3 已复核 authority-userinfo 检测、artifact write 前 fail-closed、generic public
error、独立 probes、production eval、secret scan 与 canonical/installed bytes。

### `BR-117-F2` P1：task-bearing 调用未验证 task/worktree identity

状态：`closed`

Round 3 已复核 active task、task-start-context、repo、branch、active pointer 与
workspace boundary 统一 gate，以及 wrong task、archived task、wrong repo、
wrong branch、wrong worktree 与 taskless standalone。

### `BR-117-F7` P2：recorder 未执行输入 schema，并接受不存在的 supersession lineage

状态：`closed`

Round 5 已复核 schema-before-access、受控 `WorkflowError`、no-prior/wrong-prior
拒绝、exact-prior supersession、changed-plan re-entry、runtime/package tests 与六处分发
一致性。关闭证据绑定 [F7 closure 与 F8 finding 报告](reviews/004-f7-closure.md)。

## 当前 finding

### `BR-117-F8` P3：closure raw report 的 EOF 多余空行

Reviewer-owned gate 状态：`open`

Implementation candidate 状态：`resolved_pending_closure`

Round 5 对未篡改 committed range 执行 `git diff --check`，命中
`reviews/002-closure.md:189` 的 EOF 多余空行。本轮实现只删除该一个空行，不改写
Round 3 的语义结论、验证声明或 closure recommendation。

由于当前 HEAD 仍是修复前的 `3bfbd100...`，`origin/main...HEAD` 只有在下一次 task
work commit 纳入本候选后才能反映 F8 修复。正式关闭仍要求 fresh Phase 2、task commit、
独立 finding closure；随后由未参与 closure 的 fresh final reviewer 覆盖最终完整范围。

## 文档、范围与影响

Docs SSOT strategy 继续为 `ssot_first`。F8 只修正 task-local raw review report 的格式，
不新增公共 Skill、workflow、runtime、schema、installer、overlay、README 或 durable
requirements 语义，因此没有新的 durable docs delta。既有 #117 task delta 已由前序实现
合并到 durable owners；本轮 `reviews/002-closure.md`、本汇总与实现交接仅保留 task
history 和 gate evidence。

Issue Scope Ledger 仍只关闭 #117。Exact pushed feature-ref clean install 继续作为授权
push 后、创建 PR 前的 publication gate；当前 local-source throwaway 不冒充该证据。

本轮没有修改 CI/CD、容器、Compose、K8s/Kustomize、数据库 migration、Makefile、
dependency manifest 或生产数据面，也没有新增部署或安全影响。

## 当前路由

现有 reviewer-owned `review-gate.json` 的语义仍为
`implementation_required`，实现代理不改写该 gate。下一步必须先完成 assignment
report digest 的受支持 freshness 处理，再由独立 `trellis-check` 对当前候选执行完整
Phase 2；不得直接进入 publication、push、PR 或 Issue closure。
