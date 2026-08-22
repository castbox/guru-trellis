# #295 Requirements contribution

本 contribution 修复 `BEH-001` 标准 Intake 中 Sync `synced` 到 mandatory Discovery
`pre_task` 的 public handoff 断链。它保持 `base_current` 为 Sync 唯一 public
transition，并把 live base observation 与 semantic result 归还 Discovery owner。

- `R295-01`: Sync `synced` 必须保持 output 2.0 和 `base_current` 1.0 public shape；private `guru-base-sync-result-1.0`、facts digest 和 private locator 不得进入 consumer DTO。
- `R295-02`: Discovery 必须发布 versioned pre-task input 2.0；旧 1.0 schema id/bytes 仅作为 immutable legacy asset 保留，不得进入 active graph。
- `R295-03`: Discovery 2.0 input 只包含 profile、source exit、mode、change clues 和 continuation identity；repository/base authority 仅来自独立 `base_current`。
- `R295-04`: Discovery 必须发布 owner-result 3.0，以 owner-private `base_observation` 取代 Sync private result、`base_sync_facts_sha256` 和同义 digest chain。
- `R295-05`: Discovery 在 Issue、Docs、code、test 或 history read 前，必须 live 验证 authority checkout、repo identity、selected base、branch/ref、decision/local/remote HEAD 和 clean state。
- `R295-06`: public identity 正常推进或 stale 时返回 `refresh_base`；dirty、wrong/missing ref、repo mismatch、ambiguous authority 或 invalid structure 返回 `blocked`；Discovery 不执行 Git mutation。
- `R295-07`: actual Sync wrapper stdout 必须经声明 projection 进入 actual Discovery wrapper，再把 actual `context_ready` 投影到 Clarify；不得重建 private result、调用低层 Sync executor或 import private runtime。
- `R295-08`: no-impact、existing Issue、proposed draft、zero-history、refresh 和 blocked 支持路径不得回退，pre-task route 不新增 tracked handoff、journal、shared cache 或 cross-Skill checkpoint。
- `R295-09`: package/runtime tests 与产品 verification 必须通过 checkout-managed Python resolver 或 public wrapper；bare PATH Python import 不得决定产品依赖结论。
- `R295-10`: missing/stale managed pointer、missing interpreter 和 dependency/inventory drift 必须保持声明的稳定错误，缺失依赖不得误报通过。
- `R295-11`: canonical、dogfood installed、Shared/Codex/Claude/Cursor、workflow/spec、preset/installer、update/reapply/drift、sidecar、interfaces/schemas/examples/tests/evals 必须作为一个 active unit 收敛。
- `R295-12`: 本 task 只执行 accepted scope 的 targeted validation 和一个代表性 clean throwaway；不承担 release-wide matrix、tag、Release 或任何排除 Issue。

本 contribution 在 independent review 与 serialized promotion 前不修改 shared current
RDT/Architecture authority，也不开始 #286。
