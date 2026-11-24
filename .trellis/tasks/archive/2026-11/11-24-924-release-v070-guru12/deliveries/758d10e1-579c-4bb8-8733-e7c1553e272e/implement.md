# D2 升级候选版本同步实施计划

## 1. 输入和引用

读取整体 PRD、本批 PRD、design 第3节及当前升级入口。使用 #925 已交付源码作为开发基线。读取现有升级 schema、consumer 及上次版本同步的实际修改。

## 2. 步骤和责任

1. 将现有 `TARGET_GURU` 和升级结果版本约束及示例同步至 .12。修改范围为 canonical 包的 owner、两处包内结果与消费 schema、示例，以及共享消费 schema。
2. 执行现有安装升级合同测试、源码包检查和临时受管投影验证。临时干净测试源码验证真实 `source_locked` preview。通过后按正式 TaskCommit 和独立审核交付本批。
3. 本批按 `Refs #924` 合入。后继从实际已交付源码执行 AC02。

## 3. 验证

- V1：运行 `trellis/skills/guru-team/packages/guru-upgrade-installation/tests/test_contract.py` 的原测试套件、`check-skill-packages.sh --mode source` 与 `git diff --check`。
- V2：用 `verify-throwaway-install.sh --mode focused --platform codex`、已匹配的 Fork 与 registry/workflow 同字节的已交付 `51a859b8` 作为 marketplace，验证真实投影。
- V3：从隔离干净测试源码运行 `guru-upgrade-tools/scripts/preview.sh`，给定 `source_locked`、真实匹配 Fork 和准备工作区，观察版本拒绝消失并取得可以审查的预览。保留预览的结论和导致阻塞的实际证据。

## 4. 停止与恢复

若只读预览发现无法解释的受管编辑或来源缺口，先用原 owner 的预览和真实 preimage 查清原因，失败仍保留阻塞。临时验证保留与正式交付、真实目标采用的边界。

## 5. Delivery Policy

`staged`。本批只交付 AC02a 的版本约束和验证。后继仍须完成 AC02 的实际工具采用和 AC03 的整体收尾。源码交付就绪不依赖后继安装先完成。

## 6. Docs SSOT Plan

`no_docs_update_needed`。该修正保持现有升级与分发定义，只同步本发行的固定目标值及其示例。按原 Architecture 和 RDT owner 核对现行定义仍完整。
