# 发布准备设计

## 唯一路径与责任
直接修改现有版本/安装说明，复用既有官方 marketplace、preset 与 guru-upgrade-installation；不添加发布脚本、状态文件、兼容 wrapper 或第二 authority。用户已选定 .3 版本映射；predecessor .1 的历史拒绝语义作为历史边界保留。

## D500-01 版本文本
README 的版本表分清目标 repository tag、extension、Fork source/CLI 与 knowledge identity。workflow/preset README 采用同一映射。描述 .3 为本次正式发布目标；发布前仍是候选，不宣称软件发布完成。安装 source 在 candidate 阶段使用完整远端 SHA，完成 Stage 2 tag 验证之后使用 immutable v0.7.0-guru.3。

## D500-02 Docs SSOT Plan
Strategy: ssot_first。先校准 .trellis/spec/docs/public-docs.md 的目标版本与来源使用合同，再同步根/workflow/preset README。durable paths：
- .trellis/spec/docs/public-docs.md
- README.md
- trellis/workflows/guru-team/README.md
- trellis/presets/guru-team/README.md
- .trellis/spec/architecture/baseline-usage.md
- .trellis/spec/docs/requirements-design-test-ssot.md
- trellis/presets/guru-team/MIGRATION-495.md

Architecture current 读取 docs/architecture/README.md 的 current-main-0.6.17-guru.76；constitution 为 docs/architecture/00-foundation/design-constitution.md / guru-trellis-design-constitution-v1；project contract 为 docs/architecture/06-governance/change-contract.md / guru-trellis-architecture-change-contract-v1。修正 usage .75 投影只镜像已有 .76 authority，不改变 owner/decision/GAP/compatibility。Architecture owner 仍须逐阶段判断。RDT 以三个 README 指向的 .76 为唯一 authority；已接受迁移合同不重写。若 owner 发现真实增量，使用 docs/requirements-design-test-contributions/500-release-v070-guru3-preparation/ 和 docs/architecture/contributions/500-release-v070-guru3-preparation.md 的隔离贡献，独立 review 后再 promotion；无增量不制造新知识版本或 ADR。

四处当前投影以 #503 的 .76 与 5c760463 为准；RDT usage 的 active identity/source/freshness 镜像三份 README，不复制新的产品合同。MIGRATION-495 的旧 source lock 改为明确历史验收来源，再单列当前 lock。EVD-051 与 ecd152 保持不变，当前 #503 EVD-052 不冒充最终 Release 门禁。

## D500-03 兼容与减法
只替换 current-facing 候选/目标说明；旧 .1、.2 source 与早期 evidence 保留明确历史归属。既有迁移支持范围及 rollback/deferred 保持不变，不实施新兼容代码，不退役仍有历史 provenance consumer 的文档。canonical 文档是源头；dogfood 投影通过现有 preset apply 与 drift owner 同步，不独立 patch 安装 runtime。

## D500-04 交付与验证
task 为 reference_only，PR Refs #500。准备范围可在发布尚未发生时独立合并，因为其文本明确候选状态与后续门禁。源码/安装、平台 parity、ownership/drift 和 diff hygiene 证明准备文档与分发合同；不能证明 tag/Release 或最终 candidate 的远端安装/迁移。最终候选只能由 Stage 2 在准备与 Finish 合并后的 fresh origin/main 重新冻结。

## 风险与停止
公开措辞若需要扩大迁移支持、改 managed-byte/API/owner 或新增产品修复，停止当前实现，通过 Scope Change owner 再规划。promotion 产生的字节变化必须重新检查与 review。真实业务升级、业务原始在途、production 和完整多平台/native-host 矩阵保持未验证。
