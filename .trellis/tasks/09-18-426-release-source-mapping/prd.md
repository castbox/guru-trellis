# #426 修正 v0.6.17-guru.1 release-facing Fork source 映射

## 目标

修正当前三个 release-facing README 对 Fork source commit 与 Nightly CI 的陈旧声明，使公开安装与发布说明重新与 canonical source lock 一致，并解除 Issue #410 Stage 2 的版本轴阻塞。

## 背景与确认事实

- Issue #410 的 Stage 1 preparation 已完成并合并；当前正式发布仍由 #410 独占。
- current `main` 的 canonical 与 dogfood source record 已一致固定为：
  - repository：`castbox/Trellis`
  - commit：`43fffc170927c85d9f7fc106cc5a059e80d4530b`
  - ordered parents：`db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0`、`df12903220ce22b2c84782968ed5c93406b5738b`
  - tree：`02fc0922f535200f67de7f6ba7920e3c763d7e95`
  - CI：`35190729418`
  - CLI/core：`0.6.17`
  - package manager：`pnpm@10.32.1`
- `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` 仍把旧 parent commit `db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0` 与旧 CI `34838784963` 描述为当前 source identity。
- 现有 `test_fork_preparation.py` 验证根 README 的准备命令和 stale build 行为，但没有同时约束三份 release-facing README 的 current source/CI 映射。
- 该文件的 stale-build fixture 在临时 Fork 新增 commit 后只更新 `lock.commit`，未同步新 commit 的 ordered parents/tree，导致测试在目标 stale-build 断言前被 source-lock identity 校验截断。

## 范围内

1. 将三个 README 的 current Fork commit 与 Nightly CI 更新为 canonical source lock 的当前值。
2. 保持 README 中 CLI/core `0.6.17` 与 package manager `pnpm@10.32.1` 的现有映射不变。
3. 在现有 `trellis/presets/guru-team/scripts/python/test_fork_preparation.py` 中增加定向断言：
   - 三份 README 均包含 canonical commit 与 CI；
   - 三份 README 均不再包含旧 CI `34838784963`；
   - 期望值从 canonical `trellis-source.json` 读取，不建立第二份 source identity。
4. 修正同文件 stale-build fixture：临时 Fork commit 变化后同步该 fixture lock 的 ordered parents/tree，使测试继续验证原有 stale-build marker 行为，不放宽生产 validator。
5. 运行 source/installed projection、preset reapply、dogfood drift、diff/residue 与完整 committed diff 审查。
6. repair PR 引用 `Refs #410`，关闭 #426，但不得宣称 #410 Stage 2 或正式发布已经完成。

## 范围外

- 不修改 canonical 或 dogfood `trellis-source.json`。
- 不修改 repository tag `v0.6.17-guru.1`、extension `0.6.17-guru.42`、CLI/core `0.6.17` 或 package manager。
- 不修改 Trellis upstream、npm package、业务仓库、生产环境、数据库、容器或基础设施。
- 不在任何 #410 candidate checkout 上修改文件。
- 不复用旧 #410 candidate、#419 matrix 或 throwaway 验证结果。
- 不创建 task-local release notes、动态 checklist、Release body handoff 或 tracked release-state artifact。
- 本任务不创建 tag、GitHub Release，不执行 tag-pinned smoke，也不关闭 #410。

## 需求

### R1 当前来源映射单一化

三个 release-facing README 的 current source commit 与 CI 必须分别与 canonical source lock 的 `commit` 和 `ci_run_id` 完全一致；不得继续把 ordered parent 当作 current source commit。

### R2 独立版本轴保持不变

文档修复不得改变 repository release target、extension revision、CLI/core 或 package manager，仅修正 Fork source/CI 轴的投影。

### R3 定向回归保护

现有 fork preparation 测试必须从 canonical source lock 派生期望值，并覆盖三份 README 的 current commit/CI 映射以及旧 CI 退出。

### R4 发布证据边界

本任务的验证只证明 delivery bytes 已修复并可进入 #410 的新 candidate freeze；它不构成 #410 Stage 2、tag、Release 或关闭证据。

## 验收标准

- [ ] 三份 README 均声明 commit `43fffc170927c85d9f7fc106cc5a059e80d4530b` 与 CI `35190729418`。
- [ ] 三份 README 均不再包含旧 CI `34838784963`。
- [ ] repository tag、extension、CLI/core 与 package manager 声明保持 `v0.6.17-guru.1`、`0.6.17-guru.42`、`0.6.17`、`pnpm@10.32.1`。
- [ ] canonical 与 dogfood source record 字节一致，且 source lock 内容未被本任务修改。
- [ ] 定向文档映射测试、现有 fork preparation 测试、preset source projection 测试通过。
- [ ] stale-build 测试在完整新 commit identity 下到达并拒绝旧 build marker，而不是被 parents/tree mismatch 提前截断。
- [ ] preset reapply 后没有 unexpected mutation，dogfood overlay drift 检查通过。
- [ ] `git diff --check` 通过，递归不存在 `.new`、`.bak`、`__pycache__`、`.pyc`、`.pyo` residue。
- [ ] committed `origin/main...HEAD` 独立 Branch Review 的 P0-P3 findings 为零。
- [ ] PR 正确关闭 #426、仅引用 #410，并明确 #410 必须从新 `origin/main` 重新冻结 candidate 和重跑 Stage 2。

## 风险与回退

- 风险：只改其中一份 README 会继续造成 projection conflict。通过同一测试覆盖三份文档并执行 installed/dogfood 验证降低风险。
- 风险：误把 parent commit 从历史/parent 语境中删除。实现只替换 current source claim，不禁止 ordered parent 在正确语境出现。
- 回退：本任务仅涉及文档与一项定向测试，可通过回退本任务提交恢复；不需要数据、配置或运行时迁移。
