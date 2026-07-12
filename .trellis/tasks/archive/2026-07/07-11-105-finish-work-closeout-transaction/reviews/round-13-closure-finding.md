# Issue #105 Branch Review Round 13 问题闭环报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/final_release_review_105_round9`
- 复用依据：finding owner，仅允许 closure
- reviewed_head：`305179a7c016872bb89998a25765d26adf521c50`
- diff_range：`origin/main...HEAD`
- reuse_decision：`reuse-for-closure`
- findings_count：`1`
- 结论：`fail`

## 审查范围

只读复核了 Round 12 candidate-order P2、raw locator preflight、普通resolver优先级、plan-only fallback、多月份歧义、symlink矩阵，以及 Round 9-11 P1、committed boundary、fast-path、strict incomplete recovery、remote identity、active validators和前序finding回归。

## 问题生命周期

### Round 12 candidate-order P2

状态：`closed`

- raw path-like输入仍先执行lexical containment和逐组件`lstat`。
- 普通resolver已提前到plan-only fallback之前。
- active task和普通archived `task.json`优先。
- 普通resolver明确not-found后才进入plan-only fallback。
- exact archive locator只检查指定候选。
- basename匹配多个plan-only月份时fail closed并要求exact locator。
- active basename、relative/absolute active locator、普通archive、唯一plan-only、exact plan-only及多月份歧义均有测试。

### Round 9-11 P1及Phase 2 locator P2

状态：主体保持closed

committed-plan boundary、exact archive fast-path、strict incomplete recovery、production no-mock、remote body digest、bound PR、fork/multi/mismatch、active完整validator、archive lineage/blob/task.json保护均未发现回退。

## 发现项

### P2：单组件basename仍可绕过raw symlink preflight

证据：

- `resolve_finish_work_task_dir()` 在`guru_team_trellis.py:3889-3893`遇到单组件basename时直接设置`lookup_by_basename=True`。
- 该分支没有调用`reject_closeout_symlink_components()`。
- 随后普通resolver会检查`root/<basename>`和`.trellis/tasks/<basename>`；`Path.is_dir()`、`task.json.is_file()`及最终`.resolve()`都会跟随symlink。
- 因此`.trellis/tasks/<basename>`或repo-root同名入口为symlink，且目标存在`task.json`时，finish-work仍会接受并解析真实target。
- 这与Phase 2 P2的“raw locator在resolve前检查，恢复task.json也不能绕过alias”合同冲突。
- 当前15项WorkspaceBoundaryGuard测试只覆盖带路径的relative/absolute alias，没有basename symlink。

影响：

basename形式仍可绕过专用raw locator边界。后续plan、workspace、digest门禁通常会阻止错误发布，但raw alias证据已在普通resolver中丢失，违反fail-closed定位合同，属于P2。

建议：

- basename分支在调用普通resolver前，分别检查可能被普通resolver消费的`root/<basename>`和`.trellis/tasks/<basename>`。
- 任一现存组件为symlink时立即拒绝。
- 保持不存在的basename可继续普通resolver和唯一plan-only fallback。
- 补basename symlink指向active、普通archive及恢复`task.json`后的plan-only archive用例。

## 验证证据

独立复跑：

- canonical tests：`398/398 pass`
- targeted closeout：`55/55 pass`
- WorkspaceBoundaryGuard：`15/15 pass`
- preset tests：`36/36 pass`
- overlay drift：pass
- canonical/dogfood Python与workflow equality：pass
- `git diff --check`：pass
- Phase 2的12个`dirty_paths`与`7950c4f..305179a`非metadata路径精确一致
- Phase 2记录22项finding为resolved，但未覆盖basename symlink入口

## Docs 与 Ledger

Docs已同步普通resolver优先、唯一plan-only fallback、exact locator和多月份歧义规则；但raw locator“resolve前逐组件检查”的声明仍强于basename实现，Docs closure为`fail`。

Ledger primary/close evidence逐字一致，`398/398`、`55/55`、`15/15`、`36/36`、71 assets及两轮installed smoke均唯一完整。scope保持close `[105]`、related `[53,96,97,100]`、follow-up `[98,99,101]`。

## 部署与安全

未修改CI/CD、容器、Docker Compose、Kubernetes/Kustomize、migration或Makefile。未发现真实secret、token、私钥、`.env`、客户数据或签名URL。

## 观察与后续

- dogfood保持三个平台、71 assets、无sidecar/backups。
- current-branch remote marketplace与真实GitHub E2E仍由publish-time verifier承接。
- 远端不存在`v0.6.5-guru.3`。
- follow-up candidate：0。

## 结论

Round 13 closure失败，`findings_count: 1`，`reuse_decision: reuse-for-closure`。Round 12 candidate-order P2已关闭，但basename raw-symlink preflight缺口必须在当前Issue内修复并再次closure。
