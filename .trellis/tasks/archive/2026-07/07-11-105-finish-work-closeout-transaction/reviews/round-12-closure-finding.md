# Issue #105 Branch Review Round 12 问题闭环报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/final_release_review_105_round9`
- 复用依据：Round 9-11 finding owner，仅允许 closure
- reviewed_head：`7950c4fea3760cd4144281500b362bdb9871f64f`
- diff_range：`origin/main...HEAD`
- reuse_decision：`reuse-for-closure`
- findings_count：`1`
- 结论：`fail`

## 审查范围

只读复核了 Round 9-11 同一 P1、Phase 2 新增 locator P2、plan-only committed boundary、raw locator alias矩阵、exact fast-path、strict incomplete recovery、production no-mock、普通 discovery、remote identity、active validators、Docs、ledger、部署与安全。

## 问题生命周期

### Round 9-11 P1：post-archive 本地 artifact 阻断

状态：`closed`

- plan-only boundary 从 committed plan blob恢复，不再依赖缺失的 task context。
- repo root、configured/effective remote、branch/base、digest、locator identity、HEAD/parent/path/tree/blob/task.json全部绑定。
- production missing/tampered archived artifacts通过真实 `cmd_finish_work()` 和 `resume_archived_closeout()`，未 mock workspace boundary或metadata recovery。
- exact committed fast-path成功后只执行push、remote identity、三方HEAD和ready。
- incomplete/mismatched commit仍回落严格layout、dirty/staged、blob与lineage恢复。

### Phase 2 P2：raw locator symlink canonicalization绕过

状态：`closed`

- finish-work专用resolver在普通resolve前执行lexical containment和逐组件`lstat`。
- repo内外relative/absolute ancestor、final、multilevel、dangling、loop alias均拒绝。
- 恢复`task.json`不能绕过raw locator检查。
- 仅保留经固定结构验证的Darwin `/var -> /private/var`映射。
- 普通`resolve_existing_task_dir()`未接受plan-only archived directory。

## 发现项

### P2：finish-work候选顺序让旧plan-only archive抢占同名active task

证据：

- `resolve_finish_work_task_dir()` 对basename和精确`.trellis/tasks/<name>` locator都设置`lookup_by_basename=True`。
- `guru_team_trellis.py:3931-3942` 随后先扫描所有archive月份并返回首个同名plan-only目录。
- 普通resolver直到`3943-3945`才执行。
- 普通resolver自身在`3831-3833`明确优先active task，但finish-work专用resolver绕过了这个优先级。
- 当前9项WorkspaceBoundaryGuard测试覆盖plan-only发现和alias，但没有同名active/archive collision。

影响：

存在同名active task和旧plan-only archive时，用户传basename或精确active locator仍会被路由到archive。dry-run会错误报告 archived recovery不支持新dry-run，formal会被digest或boundary阻断；未发现错误发布风险，但正常active closeout不可用，并违反“普通discovery不放宽”。

建议：

- 对raw path-like输入先完成现有lexical/symlink preflight。
- preflight通过后优先调用普通resolver，保留active及普通archived `task.json`顺序。
- 只有普通resolver找不到任务时，才扫描plan-only archive fallback。
- 增加同名active + archived plan-only用例，覆盖basename、精确active relative path和absolute path。

## 验证证据

独立复跑：

- canonical tests：`392/392 pass`
- targeted closeout：`55/55 pass`
- WorkspaceBoundaryGuard：`9/9 pass`
- preset tests：`36/36 pass`
- overlay drift：pass
- canonical/dogfood Python与workflow equality：pass
- `git diff --check`：pass
- Phase 2的13个`dirty_paths`与`c8ad047..7950c4f`非metadata路径精确一致
- Phase 2记录21项finding为resolved，但未覆盖同名active/archive候选冲突

## Docs 与 Ledger

Docs已同步plan-only专用boundary、exact fast-path、strict incomplete recovery和raw locator规则；但“普通discovery不放宽”与实际候选优先级不一致，因此Docs closure为`fail`。

Ledger primary/close证据逐字一致，`392/392`、`55/55`、`9/9`、`36/36`、71 assets及两轮installed smoke均唯一完整。scope保持close `[105]`、related `[53,96,97,100]`、follow-up `[98,99,101]`。

## 部署与安全

未修改CI/CD、容器、Docker Compose、Kubernetes/Kustomize、migration或Makefile。未发现真实secret、token、私钥、`.env`、客户数据或签名URL。

dogfood保持`claude/codex/cursor`、`all_platforms=true`、71 assets，无sidecar/backups。

## 观察与后续

- current-branch remote marketplace与真实GitHub E2E仍由publish-time verifier承接。
- 远端不存在`v0.6.5-guru.3`，不得声明该tag路径已验证。
- follow-up candidate：0。

## 结论

Round 12 closure失败，`findings_count: 1`，`reuse_decision: reuse-for-closure`。Round 9-11 P1和Phase 2 locator P2已关闭，但新发现的同名active/archive候选优先级P2必须在当前Issue内修复并再次closure。
