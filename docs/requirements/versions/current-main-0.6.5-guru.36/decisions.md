# Requirements 决策与 provenance

- `RDEC-001`（accepted）：current authority 使用 `current-main-0.6.5-guru.36`，明确区别于 released `v0.6.5-guru.9` 与 replacement candidate `v0.6.5-guru.10`。
- `RDEC-002`（accepted）：旧 requirements 文件改为导航，避免双 current authority。
- `RDEC-003`（accepted）：从 current workflow/registry/interface 恢复的行为标为 `code_recovered`，不冒充原始产品 intent。
- `RDEC-004`（accepted）：#263/#264/#265 PR body 中的测试数字只作为 historical focused evidence，不自动转写为本次 PASS。
- `RDEC-005`（unverified）：Trellis `0.6.15` 与后续累计 release 由 #260/#267 的责任门禁决定；#275 只拥有 `v0.6.5-guru.10` replacement release。
- `RDEC-006`（source_confirmed）：#262 以“当前无法复现、证据不足”关闭；其关闭评论记录 exact source targeted 10/10 与 suite 44/44 PASS，但没有 code fix，也不能证明 current main 或后续 release candidate。
