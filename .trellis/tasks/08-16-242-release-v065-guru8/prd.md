# #242 v0.6.5-guru.8 累计发布需求

## 目标

从已完成 base reconciliation 的
`origin/main@09d29ad3b37e681b3cede129028e161ab9b1d682` 准备本次
release-owned bytes，合并 preparation PR 后冻结唯一 exact candidate，并完成
`v0.6.5-guru.8` 的累计发布闭环。版本映射固定为：

- repo tag：`v0.6.5-guru.8`；
- Guru Team extension version：`0.6.5-guru.33`；
- official Trellis CLI：`0.6.5`。

发布闭环包含 preparation、完整发布门禁、immutable annotated tag、独立
tag-pinned fresh clone smoke、非 draft/非 prerelease GitHub Release，以及只关闭
Issue #242。

## 当前事实

- 最新稳定 tag/Release 为 `v0.6.5-guru.7`；tag peeled commit 为
  `9b054f01ead8edf03a5713ec10aa7c3e1a4d99d1`，stable extension version 为
  `0.6.5-guru.31`。
- task branch 起点为 `0e315fcf41c6fc918364927b93f4b84c9b944aba`；#243 修复合并后已
  fast-forward 并完成 all-platform preset reconciliation，当前 HEAD 与 fresh
  `origin/main` 均为 `09d29ad3b37e681b3cede129028e161ab9b1d682`。
- `v0.6.5-guru.7..origin/main` 包含 26 个 commit 与 1008 个 path。累计 payload
  为 #208、#164、#236、#237、#243；`c8c2409cbb79759dae8be8ce95ce03655d5cf518`
  与 PR #245 的 #243 task archive 进入候选字节，但不形成新的功能声明或关闭对象。
- 当前 canonical/dogfood extension version 为 `0.6.5-guru.32`；本发布只分配一次
  新 version `0.6.5-guru.33`，不复用 `.31`、`.32` 或旧 candidate evidence。
- live `v0.6.5-guru.8` tag 与 GitHub Release 均不存在。
- #242 是唯一 close issue。#222、#208、#164、#236、#237、#243 是 related issues；
  #240 是发布后的独立 follow-up。
- #127、#220 禁止修改、恢复、评论、关闭或清理；#223 没有 live guru.8 依赖；
  #239 不是本发布 blocker；#240 的实现不属于本任务。

## 发布需求

### R1：累计 payload 与版本身份

1. 发布 payload 必须完整包含 #208、#164、#236、#237、#243 的 merged bytes；#243
   必须保持 versioned `production-current-3.0.json` 的 immutable SHA-256
   `98f632f815351ae3f84af081613c1b4cde6eab7bc1341af00467755f2f4acacb`。
2. canonical manifest、dogfood manifest、public README、workflow/preset README、
   release-identity examples/tests 与最终 Release notes 必须一致指向
   `v0.6.5-guru.8` / `0.6.5-guru.33` / CLI `0.6.5`。
3. preparation branch HEAD 不是发布 candidate。只有 preparation PR 合并后重新读取的
   clean `origin/main` commit/tree 才能成为 candidate。
4. 任一 candidate byte 或 release-owned metadata 变化都会使绑定它的证据 stale；
   必须重新冻结并重跑受影响门禁。

### R2：canonical、dogfood、ownership 与投影

1. canonical source、installed dogfood、Shared/Codex/Claude/Cursor public projection
   必须满足当前 inventory、mode、ownership、schema、registry/workflow graph 与 byte
   equality 合同。
2. canonical 变更后必须通过 preset `apply.sh --repo . --all-platforms` 生成 dogfood
   与平台投影，再通过 ownership 和 overlay drift 检查。
3. source、installed、production snapshot 与 throwaway snapshot 均不得出现未知
   `.new`、`.bak`、conflict、removal 或 sidecar。

### R3：安装、更新与解释器身份

1. clean throwaway initial install 必须真实执行 marketplace workflow install、preset
   initial apply 与公开 wrapper。
2. existing-repo 路径必须真实执行 workflow preview、switch、official `trellis update`
   与 preset reapply。
3. README 原始 verifier 必须在 PATH Python 缺少 `pip/jsonschema` 和 PATH Python 已有
   `jsonschema` 两个环境运行；每个 checkpoint 必须核对 managed launch path、实际
   `sys.executable`、runtime identity 与 dependency-lock identity。
4. linked worktree/task closeout 路径必须通过，且最终不存在 `.new`、`.bak` 或未处理
   workspace drift。

### R4：正常场景资格与模型证据边界

1. 按 #237 当前 live authority 执行 deterministic、no-model、fake-production、sandbox、
   schema/route、安装投影与独立 review 门禁。
2. 禁止运行 `160x5`、`160x1` 或其他 live GPT-5.6 Sol production matrix。
3. Issue、PR、README、Release notes 与最终结论必须明确：本发布未取得 live GPT-5.6
   Sol production semantic evidence。
4. 禁止声明 pressure matrix、模型稳定性、永不复发或未来模型行为已经通过。

### R5：临时 Python bytecode 隔离

1. `.pyc`、`.pyo`、`__pycache__` 不进入 release、package、managed 或 snapshot
   identity。
2. production/throwaway snapshot staging 必须显式排除 bytecode；首次执行前与
   postflight 对 staged roots 执行精确 path scan，结果必须为零。
3. source checkout 中 ignored bytecode 的 count/path/size/mtime/hash aggregate 不属于
   产品 identity、freshness 或 blocking evidence；不得稳定、恢复或因其变化使证据 stale。
4. 语法检查优先使用无落盘 `compile()`；若第三方工具必须产生 bytecode，只能写入
   snapshot/source 外的 owner-private 临时目录。
5. staged snapshot 中发现 bytecode 时，按精确路径报告 staging/runner hygiene failure，
   不称为 candidate identity drift。
6. 任何绑定 source bytecode aggregate 的旧 evidence 全部失效。本任务只修正本次发布
   计划和本轮 evidence，不创建或实现 #239 的 canonical spec/runtime、多 consumer 或
   Trellis 0.7 多 workflow 范围。

### R6：完整 Trellis 生命周期

1. Planning 必须包含 `prd.md`、`design.md`、`implement.md`、Docs SSOT Plan、planning
   wording review 与 `guru-approve-task-plan`。
2. Phase 2 必须完成实现、targeted validation、independent implementation/check work、
   `guru-check-task` 及 finding 修复后的受影响重跑。
3. commit 前必须展示精确 stage/commit 计划并取得当前确认；之后依次完成 fresh-final Branch
   Review、PR readiness、push、PR 创建与 PR merge 门禁。
4. PR merge 只接受总编排发送的精确文本“合并PR”。

### R7：tag、tag-pinned smoke、Release 与 closure

1. pre-tag 门禁全部通过后，单独展示 annotated tag 的对象、message、commit、命令、
   push refspec 与副作用；取得“确认继续”后执行。
2. tag 必须是 immutable annotated `v0.6.5-guru.8`；peeled commit 必须与冻结 candidate
   相同。
3. 单独展示 tag-pinned fresh clone smoke 的临时目录、clone/checkout、安装命令与本地
   副作用；取得“确认继续”后执行；不得用 branch、本地 checkout 或旧 clone 替代。
4. 单独展示 GitHub Release 的 title/body/target/assets 与副作用；取得“确认继续”后执行；
   Release 必须非 draft、非 prerelease。
5. 单独展示 Issue #242 close 的精确命令与副作用；取得“确认继续”后执行；最终 live 回读
   tag、peeled commit、Release 与 Issue state。

## 非目标与安全边界

- 不重新实现 #208、#164、#236、#237、#243 的功能。
- 不实现或吸收 #223、#239、#240；不触碰 #127、#220 的任何资源。
- 不复用 #222、#236、#237、#243 的 task、worktree、branch、runtime、executor 或 evidence。
- 不修改 Trellis upstream、全局 npm、系统 Python 或 user site-packages。
- 不升级、提交、push 或部署 `guru_ai_roleplay_dev` 或其他真实业务仓。
- 不读取或发布 secret、credential、数据库 URL、客户数据、签名 URL 或敏感日志。
- SKIP、局部通过、旧 evidence、取消的 live 模型矩阵或 source bytecode aggregate 均不能
  作为发布完成证据。

## 验收标准

1. `v0.6.5-guru.7..candidate` 的 commit/path/payload 映射完整，extension version 唯一为
   `0.6.5-guru.33`。
2. canonical/dogfood/platform bytes、inventory、ownership、mode、registry/workflow graph、
   overlay drift 与 package/integration/eval 门禁全部通过。
3. clean initial install、preview/switch、official update、preset reapply、linked worktree/
   closeout 与双 PATH managed interpreter identity 全部 fresh 通过。
4. deterministic/no-model/fake-production、sandbox、schema/route 与独立 review 全部通过；
   发布文案准确披露无 live GPT-5.6 Sol production semantic evidence。
5. staging preflight/postflight 的 bytecode 精确 path scan 均为零，bytecode 未进入任何
   release/package/managed/snapshot identity。
6. Planning、Phase 2、fresh-final Branch Review、PR readiness 与 PR merge 对完整当前
   candidate 均通过。
7. annotated tag 的 peeled commit 与冻结 candidate 相同；tag-pinned fresh clone smoke
   真实通过。
8. GitHub Release 非 draft、非 prerelease，target/assets/notes/version mapping 正确并已
   live 回读。
9. 最终只关闭 #242；所有排除和 follow-up Issue 及其资源保持不变。
