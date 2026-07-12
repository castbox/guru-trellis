# Issue #105 Branch Review Round 14 问题闭环报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/final_release_review_105_round9`
- 复用依据：finding owner，仅允许 closure
- reviewed_head：`6177fe9d7eee875a5ca44f293f1301d857534942`
- diff_range：`origin/main...HEAD`
- reuse_decision：`reuse-for-closure`
- findings_count：`1`
- 结论：`fail`

## 审查范围

只读复核了basename ordinary candidate pre-resolve `lstat`、matching/unmatched alias、候选顺序、raw locator、committed boundary、exact fast-path、strict incomplete recovery、remote identity、active validators及全部前序P1/P2。

## 问题生命周期

### Round 13 basename matching alias P2

状态：主体已关闭

已确认以下matching aliases在普通resolver前失败：

- repo-root basename alias
- `.trellis/tasks/<basename>` active alias
- 普通archived task alias
- 恢复`task.json`后的plan-only archive alias

candidate-order、普通active/archive优先、唯一plan-only fallback、多月份歧义、path-like raw preflight、committed recovery均未回退。

## 发现项

### P2：不匹配的direct basename alias仍会误阻断后续真实候选

证据：

- `preflight_finish_work_basename_candidates()`先检查`root/<basename>`和`.trellis/tasks/<basename>`。
- 对这两个direct candidates直接调用`reject_closeout_symlink_components()`。
- 一旦candidate为symlink，该调用立即抛错；代码没有像archive candidates一样先保存symlink evidence，再判断该alias是否真的满足普通task匹配条件。
- 因此无`task.json`的repo-root同名alias会遮蔽真实`.trellis/tasks/<basename>` active task。
- 同理，无匹配内容的active-path alias会遮蔽后续真实ordinary archive。
- 当前“unmatched alias不误阻断”测试只覆盖archive candidate，没有覆盖两个direct candidates。

影响：

合法active或ordinary archived task可能仅因更早候选位置存在无关同名symlink而无法进入finish-work。没有发现错误发布风险，但违反本轮明确的“不匹配alias不误阻断”合同，属于P2。

建议：

- direct candidates采用与archive candidates相同的两阶段逻辑。
- 捕获仅含`symlink_component`的错误，随后用普通resolver同等follow-symlink predicate判断该candidate是否实际匹配。
- 只有matching alias才重抛；unmatched alias继续检查下一候选。
- 增加repo-root unmatched alias + real active、active-path unmatched alias + real ordinary archive测试。

## 验证证据

独立复跑：

- canonical tests：`402/402 pass`
- targeted closeout：`55/55 pass`
- WorkspaceBoundaryGuard：`19/19 pass`
- preset tests：`36/36 pass`
- overlay drift：pass
- canonical/dogfood equality：pass
- `git diff --check`：pass
- Phase 2的13个`dirty_paths`与`305179a..6177fe9`非metadata路径精确一致
- Phase 2记录23项finding为resolved，但没有覆盖direct unmatched alias误阻断

## Docs 与 Ledger

Docs已声明matching alias拒绝且unmatched alias不遮蔽后续候选；实现仅对archive candidates满足后半项，Docs closure为`fail`。

Ledger primary/close evidence逐字一致，`402/402`、`55/55`、`19/19`、`36/36`、71 assets及两轮installed smoke均唯一完整。scope保持close `[105]`、related `[53,96,97,100]`、follow-up `[98,99,101]`。

## 部署与安全

未修改CI/CD、容器、Docker Compose、Kubernetes/Kustomize、migration或Makefile。未发现真实secret、token、私钥、`.env`、客户数据或签名URL。

## 观察与后续

- dogfood保持三个平台、71 assets、无sidecar/backups。
- current-branch remote marketplace与真实GitHub E2E仍由publish-time verifier承接。
- 远端不存在`v0.6.5-guru.3`。
- follow-up candidate：0。

## 结论

Round 14 closure失败，`findings_count: 1`，`reuse_decision: reuse-for-closure`。matching basename alias已关闭，但direct unmatched alias误阻断仍需在当前Issue内修复并再次closure。
