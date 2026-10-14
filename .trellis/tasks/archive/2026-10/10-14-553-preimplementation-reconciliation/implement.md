# #553 执行与验证

## Delivery Policy

policy=full；一个Delivery交付R553-01..07的当前支持组合修复及证据。原Task Completion判断全scope；未实现业务功能不属于本Task，也不是baseline前置。旧不匹配安装的D2迁移、backend业务恢复和完整Release矩阵由原owner承担，保持未验证事实，不冒充本次通过。

## Docs SSOT Plan

策略delta_first。原 `guru-maintain-requirements-design-test-ssot` 拥有本Task唯一RDT contribution：`docs/requirements-design-test-contributions/553-preimplementation-reconciliation/{requirements,design,test,traceability}.md`；`test.md`独占实际结果及fixture/native/未验证边界。Final Phase2前task_delta_reconciliation；shared current若需晋升，只在第一次独立committed full review后由原owner按当时expected version晋升，并fresh Check/commit/full review。Architecture no-impact不制造贡献/ADR或晋升。

## 实施顺序与文件范围

1. 保存本轮first failure与固定组合内容核验事实；完成Author→candidate Architecture→Wording→final Architecture→Approval→计划展示/接受→原Activation。
2. 由Trellis implement子agent修改原Reconcile runtime（提取共用resolved事实/临时index helper，原execute dispatch调用）、两个私有request schema、step-local合同/SKILL、workflow post_plan路由及精确有行为价值的回归；必要README只指向原owner。无其它owner职责变更。
3. package/runtime回归：合法文档冲突、Planning已批准但business Check不存在、带pending staged/unstaged/untracked的精确tree提交、同请求恢复不新增commit；普通selected-base/HEAD变化、unresolved、受审路径unstaged/index变更停止且保留内容。保留39项既有Reconcile回归，特别实施后resolved和no-conflict路径。共享helper修订才追加对应定向case。
4. 公开consumer回归：原pair guard new_pair→原post_plan语义result→exact executor→record/check/invoke实际stdout→原Activation同Task/gen/Delivery恢复实施。对未实现business范围，不调用Check并断言其slot无pass。fixture语义输入只证明transport；实际AIbaseline review与installed/native证据另列。
5. 一个已建立的schema2 clean installed样本使用固定CLI5aeeb81/Core45bbfee，完整source preset安装。更新后reapply同样本，逐个处置owned .bak，确认无unknown .new、manifest-selected Shared/Codex投影bytes/modes与source一致、native context/continuation同Task身份。声明平台投影执行定向descriptor/load验证；不跑全部平台安装矩阵。
6. current source/dogfood字节与drift检查分层：当前完整旧dogfood拒绝D2切换为已知既有安装边界，保持其完整原owner。禁止复制新package到旧dispatcher或新旧DTO拼接；报告拒绝，不声称已切换。新模型投影在完整matching installed样本核验。
7. 原RDT reconciliation、fresh独立Architecture phase2及完整semanticCheck；准确TaskCommit；fresh不同reviewer Architecture+完整origin/main...HEAD BranchReview。若有scope/authority变化，先返回原owner。
8. 原readiness/Refs-only Publication、Delivery merge、wholeTask Completion、独立Closure、Finish与精确资源Cleanup。每个真实Git/GitHub副作用独立展示当时目标，当前确认不扩为发布/合并/清理授权。

## 已有事实

当前main=3d68f0e4c；固定tar与installed983文件bytes/modes核验PASS。受支持组合baseline39项runtime PASS；合法conflict原ordinary executor返回reconciliation_failed且HEAD保留。一个clean current样本已安装；首次不完整source复制失败已保留，改用完整source installer恢复。以上不是本Task实现Check、BranchReview或Delivery通过。
