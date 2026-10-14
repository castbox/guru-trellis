# 验证夹具 Delivery 执行规划

## Delivery Policy

policy=full：本Delivery承接V557-01..03全部范围。夹具内容在交付前完成JSON/字段/字节核验；实际合入、原Merge恢复、history与Completion观测在发布合并后取得，由原whole-task Completion保留证据责任。没有剩余实现slice；任何未取得的实际结果都保持未验证。

## Docs SSOT Plan

strategy=no_docs_update_needed：夹具不改变Guru产品Requirements/Design/Test与Architecture合同，当前.95/.89不变。原guru-maintain-requirements-design-test-ssot在Phase2前复核该无产品docs增量判断。实际外部验证结果由Source #557唯一Test文档docs/requirements-design-test-contributions/557-manual-merged-delivery-recovery/test.md的原writer记录；本Task不复制实际结果历史，也不晋升shared authority。

## 执行顺序

1. 当前Author三文档 → Wording → fresh独立Architecture final_plan → 原Approval；展示当前计划后由原Activation记录public Planning。文件存在不代表批准或实施启动。
2. 添加精确validation/manual-merge-557.json，UTF-8 JSON解析、固定字段和固定payload字节摘要核验；不新增测试框架或CI。完成原RDT无增量调和、fresh独立Phase2 Architecture与完整Check。
3. 原TaskCommit审查届时精确必要文件和实际HEAD；独立完整committed Architecture/Review、Readiness后由原Publish发布中文Refs-only验证PR。各Git动作使用届时实际候选。
4. 读actual repo/PR/base/head、真实CI/reviews和Git内容；普通two-parent手动merge不创建Merge gate或Guru trailers。
5. 原Merge新profile亲自semantic review并正式恢复delivered；原query2只读回该事实；原Completion审查accepted scope、actual candidate/CI与required evidence后选择真实出口。记录后输出丢失由各原owner恢复同一结果，不重复merge。
6. Source #557 Test取得真实结果后重入其原完整Check；本验证资源后续收尾/cleanup另按其精确边界处理。

## 验证边界

交付前内容核验只能证明夹具候选。原Check/Review证明其实际范围；真实GitHub/public调用只能在对应实际动作后记录。missing/pending/cancelled/failed不冒充green，CI不自动新增scope；必要证据缺口保留原未完成出口。Source #557关闭、业务恢复与完整Release矩阵保持各自owner。本方案来源承诺处置只由design.md矩阵拥有。
