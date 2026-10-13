# #531 真实远端事务恢复验收样本整体需求

## 需求来源与对象
当前 no_issue 请求为独立验收样本；原请求 locator：draft:3aacf5989fc7f6c51cafa7f1d168bc7275830871d25d3990a9b5116b6840e41e。#531 是产品验收背景，不是本 Task 的 Direct Source，不产生 Issue 关闭效果。
Task 为 531-remote-next-validation/gen0，整体 scope 与完成责任由 Task 保留。base 为 codex/531-remote-next-base；head 为 codex/531-remote-next-delivery。Delivery 单独拥有 Planning 与生命周期。

## 整体范围
建立一个 pull_request Delivery。唯一验证文本是 validation/531-remote-next.txt，文本说明这是 #531 专用远端恢复样本。验收与稳定规划候选为该 txt、task.json、整体 prd.md、该 Delivery 的 prd.md/design.md/implement.md/implement.jsonl/check.jsonl 八文件，另纳入下列七份最小样本基础文件，合计十五文件。基础仅描述新样本README与冻结安装依赖，不复制产品authority或旧gate。
通过原唯一语义 owners 完成 Planning、Check、TaskCommit、Branch Review、Delivery Review、Publish、Merge。公共 Task/Delivery 模型及转换属于已安装上游 API1/Task2；Guru 承接团队门禁和原私有事务，不新增状态 authority。

## 验收责任
- Publish 真实成功后先不交 Merge consumer，再以原公开 same-plan 恢复入口获得同一个 PR、head、正文、readiness 和 publication result；不得第二次 push/create/Ready。
- Merge 真实成功后先不交 Completion consumer，再由原公开入口重建同一 merge fact；核对 merge SHA、message、两 parent、base ancestry、五个 schema2 trailers；不得第二次 merge。
- 原公共 discovery 读回 first-parent 与 GitHub 的历史事实，区分已交付历史和当前门禁。
- TaskCommit 只提交十五文件候选一次；提交后同内容 clean 接续不产生第二个、空或重复提交。
- 所有声明必须限定真实执行层；自然未出现的公共投影暂缺，不伪称已真实复现，由 #531 独立 Check 判断 package 回归加远端事实的充分性。

## 退出与返工
缺失或 stale gate 返回其原 owner；真实 scope 变化先 Clarify 和整体 PRD，再影响本 Delivery。输出丢失只重入原 producer，禁止重造 Task/Delivery/PR/merge。失败保留原事实，不将历史提交/PR当当前 pass。

## 非目标与完成边界
不改产品/provider业务、业务原树或旧验证样本，不关闭任何 Issue，不执行完整 Release 矩阵，不把本样本当 V07 旧clean迁移或正式 source-lock。
本 Task 的完成要求是上述实际验收与剩余未执行边界均准确读回；#531 设计、实现、联合验证、原业务会话恢复须分别判断。本 PR 只合到专用 base。

## 样本基础前序与写集
- docs/architecture/README.md
- docs/architecture/00-foundation/design-constitution.md
- docs/architecture/06-governance/change-contract.md
- docs/requirements/README.md
- docs/design/README.md
- docs/test/README.md
- .trellis/spec/architecture/index.md

原Bootstrap按upstream spec bootstrap、原RDT foundation与原Architecture foundation、cross-SSOT语义审查、minimal spec projection及原validator完成。不得以installer或文件count替代。基础文档真实纳入当前diff，不隐藏dirty。
