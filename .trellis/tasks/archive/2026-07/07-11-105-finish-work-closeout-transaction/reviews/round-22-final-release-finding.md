# Issue #105 Branch Review Round 22 最终放行审查报告

## 审查身份

- 逻辑角色：最终放行审查代理
- technical agent：`/root/final_release_review_105_round22`
- 独立性：未参与实现、Phase 2、Round 1-21、finding 发现或问题闭环
- reuse_decision：`new-agent`
- reviewed_head：`9642ea0e7e35aea31a44e051941315cd24de2930`
- base：`3dec302206783fe4ac1296066e9a1789c995d58b`
- findings_count：`1`
- 结论：`fail`

本轮严格只读，未修改文件，未运行 Guru recorder/gate，未 commit、push、创建 PR 或关闭 issue。

## 审查范围

独立读取 live Issue #105、规划/approval/Phase 2/ledger/assignment、Round 1-21 raw reports、14 个提交与 60 文件完整 diff，以及 canonical/dogfood workflow、companion、schema、preset、overlay、平台入口、durable docs、closeout prepare/remote/PR/archive/recovery/resolver/hook/cross-month/parent-child/history portability、installed closeout、scope、安全和部署影响。

## 最终审查

### P1：archive destination 的祖先 symlink 未在 prepare 阶段拒绝

证据：

- `assert_closeout_archive_locator_available()` 只对最终 destination 调用 `os.path.lexists()`。
- 当 `.trellis/tasks/archive` 或 `archive/YYYY-MM` 是 symlink 且最终 task destination 尚不存在时，`lexists(destination)` 返回 false，dry-run/formal prepare 均会通过。
- `validate_closeout_pre_move_continuity()` 校验月份、hook、move files、mode/blob 和 dirty/staged/untracked 集合，但没有逐组件 `lstat` archive destination ancestors。
- 官方 `archive_task_dir()` 执行 `month_dir.mkdir(..., exist_ok=True)` 和 `shutil.move(source, dest)`，会沿祖先 symlink 把 active task 移到仓库外。
- post-move layout 只检查 final component 的 `archived.is_symlink()`；祖先 symlink 下 final task directory 本身不是 symlink。
- 现有 production collision test 只覆盖最终 locator 已存在，没有 archive root/month ancestor symlink 用例。

影响：formal 路径可能已完成 reviewed content push、remote verifier、evidence commit/push、draft PR 和 final projection，随后 official archive 才把 task 移到仓库外，并在 Git/layout 校验阶段失败，重新形成 #105 要消除的 moved-but-unpublished 中间状态和任务资产越界写入风险。

修复要求：

- shared prepare 对 `.trellis/tasks/archive`、月份目录和最终 destination 的所有既有组件执行 lexical `lstat`，拒绝任意祖先或 final symlink。
- official move 前再次执行相同 preflight，防止 prepare 与 move 之间漂移。
- 增加 archive root symlink、month symlink和仓库内外目标的 production dry-run/formal 用例。
- 断言失败发生在任何 Git/GitHub/recorder mutation 前，task 保持 active，local/remote HEAD、PR、plan/readiness/ledger 均不变，hook/verifier/archive transition 未发生。
- 同步 durable path-safety 合同和 installed smoke 覆盖。

## 问题生命周期

Round 1-21 已登记 finding 的 closure 未发现回退。Round 18 六项 P1 与 manifest P2 已由 Round 19 关闭；Round 20 locator collision P1 与 parent/child P2 已由 Round 21 关闭。本轮 P1 是独立新 finding，Round 22 因此成为 finding owner，后续只能用于 closure。

## 通过证据

- canonical `417/417`、preset `36/36` 通过。
- Python compile、Bash syntax、`git diff --check` 通过。
- `46c7ee5...9642ea0` 的 12 个 postcommit paths 与 Phase 2 dirty paths 完全一致。
- canonical/dogfood script、workflow、schema 字节一致。
- manifest 71 assets，`managed_backups=[]`、`new_copies=[]`，`.new/.bak=0`。
- initial #105/update #106 installed closeout 通过。

这些验证未覆盖 archive ancestor symlink finding，不能支持放行。

## Docs SSOT

现有流程文档事务顺序一致，但 path-safety 行为未满足 #105 archive 前完整路径验证合同。修复后必须把 archive ancestor lexical preflight 写入 durable SSOT 与测试。

## Issue Ledger

- close：`[105]`
- related：`[53,96,97,100]`
- follow-up：`[98,99,101]`

本 P1 属于 #105 archive transaction 和 preflight 核心范围，不应拆为后续 issue。

## 安全与部署

- 未发现 secret、token、客户数据或签名 URL 泄露。
- 未修改 CI/CD、容器、K8s、数据库 migration 或 Makefile。
- archive ancestor symlink 可导致 task metadata 被移动到仓库外，属于本地路径完整性和事务安全阻塞项。
- 修复应局限于 companion、测试和 durable docs，不扩展为通用 resolver 重构。

## 观察项

- current-branch remote marketplace 与真实 GitHub E2E 尚未验证，只能由 publish-time verifier 承接。
- `v0.6.5-guru.3` 不存在，不得声明 stable-tag 安装已验证。
- throwaway marketplace 使用 public sample；当前分支 companion 由本地 preset 安装验证。
- 当前未提交内容仅为 task-local metadata 与 review reports。

## 后续候选

0。本轮唯一 P1 属于当前 #105 范围。

## 结论

- P0：`0`
- P1：`1`
- P2：`0`
- P3：`0`
- findings_count：`1`
- reuse_decision：`new-agent`
- 最终结论：`FAIL，Branch Review Gate 阻塞`
