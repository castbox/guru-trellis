# Issue #105 Branch Review Round 21 问题闭环审查报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/final_release_review_105_round20`
- 复用依据：Round 20 两项 finding owner，仅允许 closure
- reviewed_head：`9642ea0e7e35aea31a44e051941315cd24de2930`
- base：`3dec302206783fe4ac1296066e9a1789c995d58b`
- reuse_decision：`reuse-for-closure`
- findings_count：`0`
- 结论：`pass-for-closure-only`

## 审查范围

仅复核 Round 20 两项 finding 及其直接修复面：initial archive locator collision 的 shared prepare 门禁、parent task children 的官方 lifecycle 兼容、提交 `9642ea0`、对应 production/unit tests、Phase 2 postcommit 覆盖、planning scope、Docs SSOT、Issue Ledger、commit、安全与部署影响。

全程只读，未运行 recorder/gate，未修改文件，未 commit、push、创建 PR 或关闭 issue。

## 问题生命周期

### Round 20 P1：archive destination collision 延迟到远端副作用后才发现

状态：`closed`

实现证据：

- `assert_closeout_archive_locator_available()` 使用 `os.path.lexists()`，目录、普通文件和 dangling symlink 均视为冲突。
- `build_closeout_plan()` 在形成 move set、写 plan、Git/GitHub/recorder mutation 之前调用该门禁。
- dry-run 与 formal 共用相同 `prepare_closeout()` / `build_closeout_plan()` 路径，错误 stage 固定为 `archive-locator-preflight`。

生产测试确认 dry-run/formal 连续返回同一 stage；task 保持 active 且 `status=in_progress`；local HEAD 保持 reviewed HEAD；remote branch、PR、plan、readiness 均不存在；transition event 集合为空；未进入 push、verifier、evidence commit、draft 或 archive。

结论：Round 20 P1 已完整闭环。

### Round 20 P2：children 门禁误伤 archived-child parent

状态：`closed`

实现证据：

- `children` 缺失按 `[]`；其余值严格要求 `list[str]`。
- malformed dict、string 或包含非 string 元素时，在 `task-children-preflight` fail closed。
- `official_active_task_match()` 逐字复刻官方 `find_task_by_name()`：exact active directory 优先，其后按 directory iteration 做 suffix match。
- `official_archive_would_handle_child_metadata()` 复刻官方 `read_json` 失败返回空及 truthy `child_data` mutation guard。
- 只有官方 archive 会实际改写的 active child 被阻塞；archive tree 内的 historical child 不参与 active lookup。

测试确认 active exact/suffix child 均阻塞，malformed children 在 dry-run/formal 同 stage 无副作用失败，archived child 的 parent 则完成完整 closeout，task archived、PR ready，local/remote/PR HEAD 相同。

结论：Round 20 P2 已完整闭环，未修改官方 `task.py archive`，也未扩展 resolver/symlink 行为。

## 验证证据

本轮独立执行：

- Round 20 专项：`6/6`，OK
- Phase 2 postcommit audit：`errors=[]`
- Phase 2 12 个 dirty paths 与 `46c7ee5..9642ea0` 精确同集，digest 一致
- commit message contract：`14/14 errors=[]`
- canonical/dogfood Python、workflow：byte equality
- overlay drift：通过
- manifest：71 assets，`managed_backups=[]`、`new_copies=[]`
- `.new/.bak`：0
- `git diff --check`：通过
- planning 三文档 SHA-256 与 approval 中 reviewed/approved artifacts 一致

Phase 2 记录并核对：canonical `417/417`、targeted closeout `68/68`、locator `21/21`、entrypoint/workspace `23/23`、preset `36/36`、initial #105/update #106 installed closeout、fresh-clone assignment、compile、Bash、JSON/schema、overlay/equality 和 sidecar 均通过。

## Docs SSOT

durable docs 已同步 planned archive locator 的 shared prepare 前置门禁，以及 children 缺失/`list[str]`、官方 active exact/suffix lookup、truthy metadata guard、active child 阻塞和 archived child 不阻塞 parent 的合同。

覆盖 canonical/dogfood workflow、requirements、README、workflow/preset README 和 companion/data/workflow durable specs。Docs SSOT：`pass`。

## Planning 与范围

planning approval schema `1.2` 有效，三份规划文档 digest 一致。本轮没有引入通用 hook 引擎、archive 迁移、时间框架、resolver 扩张或 Trellis upstream 修改。

- close：`[105]`
- related：`[53,96,97,100]`
- follow-up：`[98,99,101]`

primary 与 close acceptance evidence 一致。

## 安全与部署

- 未修改 CI/CD、Docker、Compose、K8s/Kustomize、Helm、migration 或 Makefile。
- 未发现 token、secret、private key、`.env`、数据库 URL、客户数据或签名 URL。
- 无应用部署、数据迁移或运行配置变更。
- 修复仅影响 closeout prepare 的确定性 fail-closed 判断及文档/测试。

## 观察项

- 远端不存在 `v0.6.5-guru.3`，不得声明 stable-tag 安装已验证。
- 当前工作分支尚未推送。
- current-branch remote marketplace 与真实 GitHub E2E 仍由 publish-time fail-closed verifier 承接。
- 当前未提交内容仅为 task metadata/reviews tail，无 non-metadata drift。

## 后续候选

0。Round 20 两项 finding 均已在当前范围闭环，本轮未发现新增问题。

## 结论

Round 21 问题闭环审查通过。

- P0：`0`
- P1：`0`
- P2：`0`
- P3：`0`
- findings_count：`0`
- closure_status：`pass`
- reuse_decision：`reuse-for-closure`

本轮不能作为 Branch Review Gate 最终放行依据。下一步必须由未参与实现、Phase 2、Round 1-21 或任何 finding closure 的 fresh technical agent，对完整 `base...9642ea0` diff 执行最终放行审查。
