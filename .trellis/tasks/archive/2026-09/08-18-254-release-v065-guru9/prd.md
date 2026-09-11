# #254 v0.6.5-guru.9 累计发布需求

## 目标

在 #220、#251、#253 已合并的 fresh `main` 上完成一次 release-owned preparation，补齐仓库级 Claude 支持，并发布 `v0.6.5-guru.9`。本任务唯一拥有发布准备、累计验证、immutable annotated tag、tag-pinned smoke、GitHub Release 和 Issue #254 live closure authority。

版本身份固定为：repo tag `v0.6.5-guru.9`、Guru Team extension revision `0.6.5-guru.34`、official Trellis CLI baseline `0.6.5`。发布 preparation PR 只使用 `Refs #254`，不得在 PR merge 时关闭 Issue。

## 范围

- 累计验证 #220 Phase 1 pause、#251 Finalizer same-plan recovery/legacy archive、#253 planless publication stale route；不重新实现三项 payload。
- 新增根目录 `CLAUDE.md`，内容与根目录 `AGENTS.md` 逐字节一致。
- 核对并补齐 canonical、installed dogfood、Shared/Codex/Claude/Cursor 的 Claude 入口、commands/hooks/agents/skills 分发、inventory、ownership、mode、registry、workflow graph、overlay drift 与 byte equality。
- 将 release identity、README、workflow/preset 文档与 verifier fixtures/tests 收敛到 `.34`/`guru.9`，并通过 preset 生成 dogfood/platform projections。
- 在同一 exact candidate 上运行 source/package/runtime/integration、deterministic/no-model/fake-production、sandbox/schema/route、clean initial install、preview/switch、official update、preset reapply、linked worktree/closeout、双 PATH verifier 及零 sidecar 检查。
- 创建 annotated tag，运行 tag-pinned fresh clone smoke，创建非 draft/非 prerelease GitHub Release，全部 live 回读后单独关闭 #254。

## 明确边界

- 不修改 Trellis upstream、全局 npm、系统 Python 或真实业务仓。
- 不启动 #223/#239，不吸收 #247/#248，不扩大到其它新功能。
- 不运行 live GPT-5.6 Sol production/pressure matrix；公开与 task-local 结论必须明确未取得该语义证据。
- 不把 focused smoke、旧 evidence、SKIP、source ignored bytecode 或局部通过当作发布完成。
- 每个 commit、push、PR、merge、tag、tag-pinned smoke、Release、Issue closure、cleanup 都必须在当前 live 重读后单独确认。

## 验收标准

1. fresh candidate 只含 #220/#251/#253 累计 payload 与本任务 release-owned metadata，revision 唯一为 `0.6.5-guru.34`。
2. `CLAUDE.md` 与 `AGENTS.md` 字节完全一致；Claude public entry 在 clean install/update/reapply 后无缺失、drift、`.new`、`.bak`、removal 或 unknown sidecar。
3. 完整累计 source/installed/throwaway/update/linked-worktree 验证与独立 Branch Review、PR readiness 绑定当前 candidate。
4. annotated tag peeled commit 必须与冻结 candidate 完全匹配；tag-pinned fresh clone smoke 真实通过。
5. GitHub Release live、非 draft、非 prerelease，notes、target、revision、payload、验证边界和空 assets 准确；只在此后关闭 #254。
