# v0.6.5-guru.9 发布说明（草案）

## 累计内容

- #220：恢复 Phase 1 规划人工审阅停点与简洁确认推进。
- #251：修复 Finalizer post-bind same-plan recovery 与 legacy closeout-plan 归档缺口。
- #253：修复 planless `publication_review_stale` 路由校验。
- #254 release-owned：补齐仓库级 Claude 支持，新增与 `AGENTS.md` 逐字节一致的根目录 `CLAUDE.md`。

## 版本与升级

- repo tag：`v0.6.5-guru.9`
- Guru Team extension revision：`0.6.5-guru.34`
- official Trellis CLI：`0.6.5`
- workflow/preset source：同一 immutable `v0.6.5-guru.9` tag

升级时使用 pinned marketplace/workflow source，执行 official Trellis update 后重新 apply Guru preset，并核对 Claude/Codex/Cursor/Shared projection、inventory、ownership、mode 与 overlay drift。

## 验证与边界

发布门禁覆盖 source/package/runtime/integration、deterministic/no-model/fake-production、sandbox/schema/route、clean initial install、existing-repo preview/switch、official update、preset reapply、linked worktree/closeout、双 PATH verifier、tag-pinned fresh clone smoke 与 live Release 回读。

本发布未取得 live GPT-5.6 Sol production semantic evidence；deterministic/no-model 结果不能证明 pressure matrix、模型稳定性或未来模型行为。预期 Release 不携带额外 assets。

## 安全与部署

不包含 secret、credential、客户数据或真实业务仓部署。Claude 支持通过仓库级规则与现有 Trellis platform projection 提供；不修改 Trellis upstream、全局 npm 或系统 Python。
