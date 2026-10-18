# Reference-only 验证计划与边界

版本：`current-main-0.6.17-guru.71`；状态：`active`；predecessor：`current-main-0.6.17-guru.70`。本版以薄继承保留[不可变前驱的完整合同](../current-main-0.6.17-guru.70/test-plan.md)；未由本版显式替换的 requirement/design/test、owner、边界、NFR 和 trace 全部继续有效。前驱版本身份、旧 source pin、历史计数与验证结果仅表示当时快照，当前版本事实以下文为准。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.71` / `active`。

已独立检查 pre-promotion 证据：正式 creator 16/16、lifecycle 152/152、Closure 18/18、dogfood 9/9；source/installed/platform validator 和 183-file official projection 通过，upstream main CI 37179218822 success。Focused Codex local-workflow sample clean/init/preset、两次 same-candidate update/reapply、session binding 与 template drift 通过，native load 为 projection_parity，未证明 native-host。

Promotion 后重新读本版 trace、导航、Architecture/projection 与完整当前 diff，执行适用 docs-link/identity/immutable-history 检查和 fresh Phase 2；新 Task Commit 后由不同 reviewer 执行完整 origin/main...HEAD 审查。pre-promotion review 不替代该 gate。

#489 独立完成 predecessor 0.6.17 update 拒绝且数据不变证明、remote marketplace、完整 release matrix、fresh frozen-main exact candidate、tag-pinned smoke、tag/Release 和 Issue closure。本版不把这些未验证项计为通过，也不把它们计作 #490 的当前缺陷。
