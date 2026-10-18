# 非功能需求继承

版本：`current-main-0.6.17-guru.71`；状态：`active`；predecessor：`current-main-0.6.17-guru.70`。本版以薄继承保留[不可变前驱的完整合同](../current-main-0.6.17-guru.70/requirement-non-functional.md)；未由本版显式替换的 requirement/design/test、owner、边界、NFR 和 trace 全部继续有效。前驱版本身份、旧 source pin、历史计数与验证结果仅表示当时快照，当前版本事实以下文为准。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.71` / `active`。

本次未增加非功能要求、兼容层、锁、并发协议或额外状态。honest-but-fallible、secret redaction、权限和 destructive action 边界继续由前驱合同约束；普通 freshness/mismatch 仍 fail closed。
