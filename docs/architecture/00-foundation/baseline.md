# FOUNDATION

- `ARCH-FND-001`：官方 Trellis 优先。Workflow/preset/spec marketplace 与 Skill/platform entry 是支持的扩展面；不得修改上游源码、全局 npm 或 `node_modules`。
- `ARCH-FND-002`：Markdown/Skill 控制过程与语义判断；script 只做 executor、validator、recorder。semantic gate 与持久化解耦。
- `ARCH-FND-003`：系统运行在 honest-but-fallible 正常协作模型；版本 freshness/digest 用于一致性而非 hostile authenticity；secret 与副作用边界仍必须保护。
- `ARCH-FND-004`：stable Skill/exit/schema/workflow/preset/command identity 是 public API，破坏性调整需要新 id 或迁移合同。
- `ARCH-FND-005`：只保留不可重建且有直接 consumer 的最小状态；授权从不进入 tracked/ignored/public artifact。
- `ARCH-FND-006`：本 Architecture Baseline 必须唯一声明 current 设计宪法的 authority locator 与 version/content identity。Guru Team public contract 只消费五个稳定 identity/short name；原则正文、解释、适用性判断和例外仍由该 locator 唯一拥有。

Current design constitution：[`design-constitution.md`](./design-constitution.md) / `guru-trellis-design-constitution-v1` / `current`。

Provenance：`source_confirmed`，来自 repository AGENTS.md、active package contracts 与 #283 reviewed promotion。
