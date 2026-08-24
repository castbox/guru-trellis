# Requirements 决策与 provenance

- `RDEC-001`（accepted）：current knowledge authority 使用 `current-main-0.6.5-guru.40`，明确区别于 extension candidate `0.6.5-guru.37` 与已发布 replacement baseline `v0.6.5-guru.10`。
- `RDEC-002`（accepted）：旧 requirements 文件改为导航，避免双 current authority。
- `RDEC-003`（accepted）：从 current workflow/registry/interface 恢复的行为标为 `code_recovered`，不冒充原始产品 intent。
- `RDEC-004`（accepted）：#263/#264/#265 PR body 中的测试数字只作为 historical focused evidence，不自动转写为本次 PASS。
- `RDEC-005`（source_confirmed + verified）：#260 负责 Trellis `0.6.15` current compatibility；独立的重构前稳定版 Release Issue 独占 `v0.6.15-guru.1` / extension `.37` 的 stable tag、GitHub Release 与 tag-pinned release smoke；#267 属于后续重构链；#275 已完成 `v0.6.5-guru.10` replacement release。
- `RDEC-006`（source_confirmed）：#262 以“当前无法复现、证据不足”关闭；其关闭评论记录 exact source targeted 10/10 与 suite 44/44 PASS，但没有 code fix，也不能证明 current main 或后续 release candidate。
- `RDEC-007`（accepted）：`.agents` 是每个声明平台 cell 的 shared public projection，不是第四个 Trellis CLI platform；package-private validator wrappers 不分发到 platform roots。
- `RDEC-008`（accepted）：A/B compatibility harness 只产生 #248/#252 可消费的事实，不新增 Acceptance、Finish 或 cleanup public owner。
- `RDEC-009`（accepted）：Architecture Baseline 是全 task lifecycle 的唯一项目架构 authority；双维 identity 只在 task-local change contract 相交，shared current 只经 independent review 后的 expected-current-bound serialized promotion 前进。
- `RDEC-010`（accepted）：设计宪法正文归项目 Architecture authority；公共合同只投影五个稳定 identity/short name，不建立 scorecard、逐项 verdict 或第二 authority。
- `RDEC-011`（accepted）：base selection 与 authority checkout binding 是两个顺序固定的确定性阶段；detached session 仅承载调用，selected-base authority checkout 独占同步、clean 与三向 equality，下游按 source 与完整 candidates 重新验证 provenance。
