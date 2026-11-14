# Issue 最小审核评论

本正文由 Clarify 独占。Create Issue 和 Clarify 的评论写作均读取本文件，
不在入口复制第二套正文规则。评论供后续 AI 复核，不能自动放行 Task。

评论只说明实际审核对象和范围、所得结论，以及仍影响开工的未决项或前置条件。
仅当代码基线影响判断时说明该基线。采用清楚自然语言，不要求固定模板、label、
审核者资格、有效期、hash 链或长期审核账本。清楚充分的已有历史评论可继续采用。
局部需求或措辞审核须写明局部范围，不能声称已完成完整开工审核。

Create 在完整草稿审核及正式内容读回之后发布；只有评论发布并读回才完成创建。
Clarify 在用户主动复审且当前动作范围包含发布或修订时发布或更新。只读审核只返回
结论。准备完整准确的正文和精确 repo/Issue/comment 后沿原副作用边界执行。

Clarify 复用原 source_actions：新增评论 POST
`repos/{owner}/{repo}/issues/{number}/comments`；更新明确的评论 PATCH
`repos/{owner}/{repo}/issues/comments/{comment_id}`。GET Issue 与 comment，
核正文及所属 Issue，再记录真实 mutation_results。评论不代替请求的 Issue 正文编辑。
结果未知时先读回本次原动作；唯一对象已成功则恢复，未能确定则停止，不重复发布。
恢复只保留原 owner 确有直接 consumer 的最小短期事实，不存授权、审核历史或覆盖账本。

Readiness 亲自读取完整 Issue、有效讨论和评论、必要前置与相关代码变化。它判断评论
覆盖及结论当前是否仍适用；评论存在本身、换 Agent、换会话或时间经过均不决定路线。

完整 Issue 正文仍按原 [Issue 内容规范](issue-content.md) 写作和审核；本规则不替代正文方法。
