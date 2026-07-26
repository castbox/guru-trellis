# #117 Branch Review 汇总

## 审查身份与范围

- 当前 reviewed HEAD：`a28b38e5a8894e3d60b9e9694a92ed610f763f25`
- 完整 committed 范围：`origin/main...a28b38e5a8894e3d60b9e9694a92ed610f763f25`
- Merge base：`0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- 最终结论：`passed`

本轮汇总消费 Round 1-11 的完整 finding、closure、fresh final lineage。Round 10
由未参与 F10 发现与实现的独立 closure reviewer 关闭 `BR-117-F10`；Round 11
再由不同身份、且未参与任何 earlier finding 或 closure 的 fresh final reviewer
覆盖完整最终范围。Round 11 没有新的 qualified finding、scope proposal 或 blocker。

## 原始报告

- Round 1/2：[初始 finding 报告](reviews/001-final.md)
- Round 3：[F1/F2 closure 报告](reviews/002-closure.md)
- Round 4：[F7 finding 报告](reviews/003-final.md)
- Round 5：[F7 closure 与 F8 finding 报告](reviews/004-f7-closure.md)
- Round 6：[F8 closure 报告](reviews/005-f8-closure.md)
- Round 7：[fresh final-intent 与 F9 finding 报告](reviews/006-final.md)
- Round 8：[F9 closure 报告](reviews/007-f9-closure.md)
- Round 9：[fresh final-intent 与 F10 finding 报告](reviews/008-final.md)
- Round 10：[F10 closure 报告](reviews/009-f10-closure.md)
- Round 11：[fresh final 放行报告](reviews/010-final.md)

## Finding 闭环

### `BR-117-F1` P1：credential URL 脱敏漏检

状态：`closed`

Round 3 复核 authority-userinfo 检测、artifact write 前 fail-closed、generic public
error、独立 probes、production eval、secret scan 与 canonical/installed bytes。

### `BR-117-F2` P1：task-bearing 调用未验证 task/worktree identity

状态：`closed`

Round 3 复核 active task、task-start-context、repo、branch、active pointer 与
workspace boundary 统一 gate，以及 wrong task、archived task、wrong repo、
wrong branch、wrong worktree 与 taskless standalone。

### `BR-117-F7` P2：recorder 未执行输入 schema，并接受不存在的 supersession lineage

状态：`closed`

Round 5 复核 schema-before-access、受控 `WorkflowError`、no-prior/wrong-prior
拒绝、exact-prior supersession、changed-plan re-entry、runtime/package tests 与
六处分发一致性。

### `BR-117-F8` P3：closure raw report 的 EOF 多余空行

状态：`closed`

Task commit 004 删除 `reviews/002-closure.md` 的一个 EOF 多余空行。Round 6 对
exact blob、commit tree、完整 range 与 dirty whitespace gate 完成独立复核。

### `BR-117-F9` P2：annotated stable tag 未绑定实际 checkout commit identity

状态：`closed`

Task commit 005 分离 direct ref object 与 peeled commit，按 resolved commit
checkout，并在 throwaway 前执行 `git rev-parse --verify HEAD^{commit}` 后精确比较。
Round 8 复核 branch、lightweight tag、annotated tag、mismatch fail-closed、
checker freshness、public projection、contract、tests、commit tree 与六处分发。

### `BR-117-F10` P2：成功 executor 未保留 installed asset digests

状态：`closed`

Task commit 006 增加 retained installed inventory，按
workflow/preset/schema/skill/platform 五类保存 closed expected surface、digest、
source relation 与逐 capability coverage；recorder、checker、schema、example、
tests、canonical/installed runtime 和六处分发同步承接。Round 10 对完整
`origin/main...a28b38e5` 复核 source 与 installed validator、throwaway、
inventory mismatch/missing/duplicate/unexpected/relation fail-closed，以及
owner-private/public projection 边界，确认 `BR-117-F10` 已关闭且没有新 finding。

## Qualification-first 结论

### `RC-F10-INVENTORY-COLLECTOR`

- 场景：`normal_required_behavior`
- 处置：`rejected_candidate`
- 候选：retained collector 单层不枚举任意额外文件，可能遗漏安装目录中的 arbitrary
  extra。
- 反证：Issue #117 当前 acceptance 是 closed expected install surface；完整
  throwaway 还同时执行 installed package、manifest、platform、managed inventory
  与 sidecar validators。正常受支持路径中的 package/platform/managed extra 会使
  executor 非零退出，不能进入 `passed`。
- 边界：不夸称 collector 单层能够扫描任意项目目录；也不把 hostile/tamper、
  race/TOCTOU/locking、fault injection、crash consistency 或 cross-OS atomicity
  重新引入当前范围。

### `OBS-F10-POST-PUSH`

- 场景：`out_of_scope` for local closure
- 处置：`observation`
- Exact pushed feature-ref clean installation 尚未执行。
- 当前没有 push/publication 授权，本地 unpublished source throwaway 不能证明
  remote ref identity。
- 该证据保留给 mandatory post-push publication gate，不构成 current
  implementation finding，也不阻塞本地 Branch Review。

## 验证证据

- Runtime：600 passed、13 skipped
- Skill integration：175 passed
- Preset 与 ownership：54 passed
- 12 个 package contracts：114 passed
- Canonical/installed verifier contracts：各 9 passed
- Source Skill validator：12 Skills、46 exits、27 targets、0 legacy
- Installed validator：2,322 managed files，0 sidecar/removal/conflict
- Static、distribution、runtime/adapter equality：全部通过
- Shared source/installed：各 7/7 passed
- Codex source/installed：各 7/7 passed
- Claude clean-auth source/installed：各 7/7 passed
- Cursor source/installed：各 7/7 expected unsupported
- Full throwaway：exit 0
- Retained inventory：expected/observed/matched=`231/231/231`，
  `complete=true`；missing/duplicate/unexpected/mismatched/relation errors 全空
- Final workspace boundary：passed；source checkout clean，suspicious paths 为 0
- `git diff --check origin/main...HEAD` 与 working-tree diff check：passed

Claude evaluation 由 outer runner 清除 `ANTHROPIC_AUTH_TOKEN` 与
`ANTHROPIC_BASE_URL` 后执行。没有把 Claude auth source 或本地 credential 写入
task artifact。

## Docs SSOT 与影响

Docs SSOT strategy 为 `ssot_first`。Issue #117、PRD、design、implementation、
公共 Skill package、schema、example、tests、marketplace/preset README 与
canonical/installed/Agents/Codex/Claude/Cursor 分发已经同步；task-local report
只保留审查与验证历史。

当前完整范围没有 CI/CD、容器、Compose、K8s/Kustomize、数据库 migration、
Makefile、dependency manifest 或生产数据面变化。变更只影响 Guru Team extension
verification 的 workflow、Skill、runtime、schema、examples、tests、distribution
与文档合同；所有 artifact 只保存去敏 path/digest/category/relation facts。

## 最终路由

所有 current-scope qualified findings 均已闭环。Round 11 fresh final reviewer
覆盖完整最终范围并返回 0 finding、0 scope proposal、0 blocker；唯一 current
candidate 已按证据记为 `rejected_candidate`。Branch Review typed exit 为
`passed`。

本汇总与 gate 不授权 push、PR、Issue #117 closure、publication 或
`finish-work`。Exact pushed feature-ref clean installation 必须由后续
publication gate 使用真实 remote feature ref 完成。
