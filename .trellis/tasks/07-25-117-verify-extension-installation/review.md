# #117 Branch Review 汇总

## 审查身份与范围

- 当前 reviewed HEAD：`3281db77b8f829e850064a33190838eb17ca4c31`
- 完整 committed 范围：`origin/main...3281db77b8f829e850064a33190838eb17ca4c31`
- Merge base：`0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Round 1/2 原始报告：[初始 finding 报告](reviews/001-final.md)
- Round 3 原始报告：[F1/F2 closure 报告](reviews/002-closure.md)
- Round 4 原始报告：[F7 finding 报告](reviews/003-final.md)
- Round 5 原始报告：[F7 closure 与 F8 finding 报告](reviews/004-f7-closure.md)
- Round 6 原始报告：[F8 closure 报告](reviews/005-f8-closure.md)
- Round 7 原始报告：[fresh final-intent 与 F9 finding 报告](reviews/006-final.md)

Round 6 独立复核关闭 `BR-117-F8`，没有发现新的 qualified finding。Round 7 由未参与
任何 earlier finding/closure 的 fresh reviewer 覆盖完整最终范围，但资格化新的
`BR-117-F9`；因此该轮必须透明登记为问题发现审查，不能冒充 zero-finding final pass。

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

### `BR-117-F8` P3：closure raw report 的 EOF 多余空行

状态：`closed`

Task commit 004 仅删除 `reviews/002-closure.md` 的一个 EOF 多余空行。Round 6 在
`3281db77...` 对 exact blob、commit tree、`git diff --check origin/main...HEAD`、
base-to-working-tree 与 dirty whitespace gate 完成独立复核，关闭证据绑定
[F8 closure 报告](reviews/005-f8-closure.md)。

## 当前 finding

### `BR-117-F9` P2：annotated stable tag 未绑定实际 checkout commit identity

状态：`open`

Round 7 对 README 默认 annotated stable tag `v0.6.5-guru.2` 执行正常路径复现：

- direct tag-object OID：`77ced9be88fd15bc50f3b22f889ccefe0f8a11ea`
- checkout/peeled commit：`c2d4b0395c78f8af6b1a21fc99a6bb31e04f1d6f`

当前 executor 记录 `git ls-remote` direct ref OID 并执行 `git checkout --detach`，但
checkout 成功后没有执行 `git rev-parse --verify HEAD^{commit}`，也没有记录或比较实际
checkout HEAD。Execution facts、private artifact 与 standalone `resolved_head` 因而
可能继续传播 annotated tag object OID，而不是被真实安装/验证的 commit identity。

该场景由已批准 PRD 的 remote/ref/reviewed HEAD binding、design 6.1 的“Clone 后复验
checkout HEAD”、Package Interface `remote_identity` 与 durable companion-script
合同直接触发，属于 `normal_required_behavior`，不涉及恶意输入、伪造、竞态或其它已
排除场景。Required closure 见
[Round 7 原始报告](reviews/006-final.md)。

## 验证、文档与影响

Round 7 fresh 验证通过完整 range whitespace、4 个 commit message、workspace、
planning、assignment、Branch Review committed-head entry、focused runtime 19/19、
canonical/installed package contract 8/8、source/installed validators、overlay drift、
ownership、六处分发、JSON/Bash/Python syntax。F8 Phase 2 的 runtime 592/13 skipped、
Skill 175、preset 45、ownership 9、Shared/Codex/Claude 最终 7/7、Cursor
`unsupported` 与 full local-source throwaway 仍绑定同一 code tree；这些长矩阵没有
覆盖 F9 的 annotated-tag identity assertion。

Docs SSOT strategy 继续为 `ssot_first`。Interface、package contract、approved design
与 durable runtime contract 已要求 cloned checkout HEAD；F9 是 runtime/tests 未完整
承接既有 SSOT，不能通过弱化文档关闭。修复必须同步 canonical、installed 与平台分发
副本，并重新执行完整 Phase 2、clean install/update/reapply 和 upgrade/update 抗漂移
门禁。

当前完整范围没有 CI/CD、容器、Compose、K8s/Kustomize、数据库 migration、Makefile、
dependency manifest 或生产数据面变化。F9 是 extension verification provenance/
correctness 问题，不新增 hostile-input/security scope，也未发现新的 credential 或
secret persistence。

Claude installed 前两次 6/7 瞬态与第三次 clean-auth 7/7 已透明保留；Cursor 按合同
返回 `unsupported`。Exact pushed feature-ref clean installation 仍是授权 push 后的
publication gate，当前 local-source throwaway 不冒充该证据，也不替代 F9 修复。

## 当前路由

当前 Branch Review typed exit 必须为 `implementation_required`，唯一 open finding 是
`BR-117-F9`。实现 owner 修复后，必须重新完成 `guru-check-task`、fresh task commit、
独立 finding closure 与独立 fresh final review。

本汇总和 raw reports 不授权 publication、push、PR、Issue #117 closure 或
`finish-work`。
