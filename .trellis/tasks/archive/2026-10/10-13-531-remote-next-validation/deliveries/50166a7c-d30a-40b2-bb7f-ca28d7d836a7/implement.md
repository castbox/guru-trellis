# D1 实施与验收计划

## Delivery Policy
full：本 D1 完整交付远端 Publish/Merge 输出恢复与 clean 候选接续样本；十五文件包含唯一 txt、task.json、Task root PRD、本 D1 三规划与两 context、七份 foundation。无剩余业务切片；完成条件是 AC01–AC07 的实际证据与整体 Completion 原判断，任何缺口不得声称 Task 完成。

## Docs SSOT 策略
no_docs_update_needed：现有最小 foundation 已由原 RDT/Architecture/Bootstrap 激活，本次不改变样本职责/接口。本 D1 design 来源矩阵为唯一处置来源；原 RDT 为任何真实 authority 变化的唯一 writer。安装失败修复 provenance 由本 design 显式保留，不偷换已激活 baseline 身份。

## 执行顺序
1. 原 Author→Wording 完整三规划→另一个 fresh Architecture final_plan→原 Approval；展示实际三规划后原 Activation。
2. 仅新增 validation/531-remote-next.txt；读取全部十五文件，fresh Architecture phase2 与原完整 Check。核验公开 scope/规划 key、唯一 source owner、scope-ref 同 result 恢复和 foundation 导航。
3. 原 TaskCommit 一次提交十五文件，中文消息；fresh Check 后原 clean 同 HEAD 接续，记录实际 HEAD/index不变、不重复 commit。
4. 原首次独立 Branch Architecture/full Review 覆盖 origin/codex/531-remote-next-base...HEAD，再 Readiness、Publish；真实 ready 输出暂不交下游，同计划重入恢复同 PR，然后继续 Merge。
5. expected-head merge 后原 terminal recovery，核同 merge facts和五 trailers；原 discovery 读回 delivered 历史。保留历史事实，不能补当前门禁。
6. 原 Completion 按整体责任独立核验；无缺口时正式收尾本样本。产品 #531 验收由产品原 owner 消费实际结果。

## 验证映射及边界
AC01/02 对应实际 Publish 与同 PR 输出恢复，AC03 对应实际 Merge/terminal 恢复，AC04 对应 discovery，AC05 对应 clean TaskCommit，AC06 对应新副本写集与原树只读，AC07 对应实际十五文件与同 D1 scope 接续。包装器通过只说明机器事实，所有 semantic gate 分别由 AI 执行。真实 PR/merge 未执行前保持未验证，不扩 Release/provider/业务 scope。出现 stale 或普通错误按 design 正常返工路径恢复。
