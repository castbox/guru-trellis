# #418 Design Contribution

状态：draft、unpromoted；Architecture继承 `.52/active`。完整接口由各canonical package独占；task设计用于本轮实施定位，promotion后将长期规则提升到版本化Design。

- D418-01：Finalizer验证精确committed archive后更新同一task的既有双端locator；boundary与preview只读，禁止通用rebuild。
- D418-02：Merge发生点分类错误，经共享CommandError传递code/field/remediation；完整输入的semantic出口与输入diagnostic分离。
- D418-03：Merge archived_review_request -> review_refresh_required -> Branch Review archived_review -> archived_review_passed -> Publication archived_publication_review -> archived_ready -> Finalizer archived_review_refresh -> 原ready_for_merge。
- D418-04：H由committed summary生成的commit集合的唯一祖先支配tip确定；A绑定当前独立复审；B绑定真实完整复审范围并交由Publication/Finalizer核对。三者不能互换。
- D418-05：title/body snapshot只服务读期间一致性。新Publication重新审查现有bytes；专属semantic variant真实保留metadata/task_work/external finding，失败停止不修改PR。
- D418-06：三个Architecture阶段分别消费新source_exit；语义owner在只读范围下选择current或blocked，validator拒绝其它写入continuation，普通source不变。

不新增Skill或command，不保存授权或跨owner private state。新profile/output独立schema和唯一consumer；普通profile的status、review-anchor、confirmation和mutation约束保持。

新增Architecture contribution和ADR在独立committed-diff review后才能promotion；promotion-created diff必须重跑Phase2/Commit/Review。Shared current不在普通task并行写入。
