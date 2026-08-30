# #267 Release routing caller inventory 修复执行计划

## Phase 1: Planning

- [x] fresh 读取 live Issue #267 body `2026-08-30-r19`、current main 与失败证据。
- [x] 确认 root cause、exact stale/new identity、单文件实现边界与 Release 后续边界。
- [x] 编写 `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan。
- [ ] 完成 planning-artifacts wording review；retained hit 全部具有确定性分类。
- [ ] 完成 `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`。
- [ ] 完成 `planning_scenario_set` qualification 与 `guru-approve-task-plan` 八维语义审查。
- [ ] 展示 approved plan；取得新的明确确认前不启动 task 或修改 inventory。

## Phase 2: Single-Row Implementation

- [ ] 在 `trellis/presets/guru-team/tests/throwaway-python-callers.json` 通过旧 `id` + 完整旧
  `anchor_sha256` 定位唯一 object，并校验 owner/kind/classification/launcher/ordinal。
- [ ] 只替换该 object 的 `id` 与 `anchor_sha256`，保留其它五个字段和数组位置。
- [ ] 使用 JSON parser 验证结构；断言新值各出现一次，旧值出现次数为 `0`。
- [ ] 审查 exact dirty paths；实现 diff 只接受 inventory 文件和本 task 文件。

## Phase 2: Targeted Validation

- [ ] 执行 caller inventory checker，要求 missing/stale 均为空。
- [ ] 执行 routing 定向 suite，要求 `44/44` 通过且 error/failure 均为 `0`。
- [ ] 执行 task validation、JSON structural check、sidecar/secret scan 与
  `git diff --check`。
- [ ] fresh 调用 Architecture `task_impact_sync(stage=phase2)` 与 `guru-check-task`；修复
  全部 P0-P3 finding 后才进入 commit 计划。
- [ ] 明确记录完整多平台 Throwaway/Release matrix 未在 task branch 执行，由 post-merge
  #267 exact candidate 独占。

## Phase 3: Commit, Review And PR

- [ ] 展示 exact stage paths、中文 Conventional Commit message 与预期 HEAD；取得独立确认后
  创建 task commit。
- [ ] 对 fresh `origin/main...HEAD` 完整 committed range 执行 independent Branch Review；
  P0/P1/P2/P3 未关闭 finding 必须全为 `0`。
- [ ] push、PR create、Finalizer 与 merge 分别展示精确副作用并取得对应确认。
- [ ] PR title/body 使用中文，body 只使用 `Refs #267`；不得关闭 #267 或 #311。

## Post-Merge: Exact Candidate Re-Freeze

- [ ] fresh fetch 并确认 local `main`、`origin/main`、GitHub remote main 完全一致；记录新
  candidate commit/tree。
- [ ] 重新验证 `5b3b7bef...`、`21c7da147...`、`3efcce72...` 均为 candidate ancestor。
- [ ] 重新验证 predecessor `.2` tag object/peeled commit，且 `.3` tag/Release 不存在。
- [ ] 在新 candidate 单一 SHA 上重跑 live Issue #267 r19 的十三项 pre-tag gates；不得复用
  `736ef333...` 的 pass assertion。

## Release Side-Effect Stops

- [ ] 十三项 gate 全部通过后，展示 candidate SHA/tree、annotated tag message 与精确 push
  refspec；取得独立确认后才创建/push `v0.6.15-guru.3`。
- [ ] tag-pinned smoke 通过后，展示 GitHub Release title/body/target/draft/prerelease/assets；
  取得独立确认后才创建 Release。
- [ ] Release live reread 通过后，#267 closure 仍使用独立确认。
- [ ] 正式 `.3` 业务仓安装、原 Finalizer 失败路径与错误文件重试全部通过后，#311 才进入
  独立 closure review；任一缺口都保持 OPEN。

## Stop Conditions

- fresh discovery 不再生成 exact new identity，或旧 `id` + 完整旧 `anchor_sha256` preimage
  不是唯一一条。
- 实现需要修改 Finalizer runtime、caller discovery、public API、schema、Release mapping 或
  `.42` authority。
- dirty path 超出 exact file boundary，或出现 `.new`、`.bak`、未声明 sidecar、secret。
- main、Issue #267 current body、predecessor tag 或 Release identity 发生漂移。
- 任一 required check 返回 FAIL、SKIP、stale、unknown、multiple 或 unmapped exit。
