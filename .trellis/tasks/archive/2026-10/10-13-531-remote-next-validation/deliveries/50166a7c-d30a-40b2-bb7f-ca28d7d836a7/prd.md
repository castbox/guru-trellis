# D1 真实远端事务恢复验收需求

## 身份与范围
Task 531-remote-next-validation/gen0；本 Delivery 为 50166a7c-d30a-40b2-bb7f-ca28d7d836a7。
整体责任见 ../../prd.md 的“验收责任”；本 D1 覆盖这一个完整验收切片，no_issue，不关闭任何 Issue。base codex/531-remote-next-base，head codex/531-remote-next-delivery。

## 交付内容
唯一验证文本 validation/531-remote-next.txt，正文为“#531 真实远端事务恢复专用样本；不承载业务功能。”加 task.json、Task 整体 PRD、本 D1 三规划与两 context，以及整体 PRD 列出的七份最小 foundation，共十五文件。由原公开 TaskCommit 提交一次。Foundation 已经原 Architecture/RDT/Bootstrap owners 审查激活；该结果不代替本 D1 的独立 Planning 或任何远端验收。

## 验收
AC01：原完整 Planning/Check/TaskCommit/Branch Review/Delivery Review 后，Publish 在真实 GitHub 创建且 Ready 唯一 PR，目标专用 base，中文正文无关闭 Issue 语义。
AC02：成功 stdout 未交 Merge 后，原 same-plan resume 返回同 PR/head/body/readiness/publication_result，GitHub 无第二PR或push。
AC03：expected-head merge 成功后，原 terminal recovery 返回相同 merge SHA/message/parents/base ancestry 和 schema2 五trailers，无第二merge。
AC04：原 discovery 读回 Delivery 历史事实。已交付事实不补当前门禁；无自然公共投影缺失时明确仅包回归覆盖该子场景。
AC05：候选提交后 fresh Check 和 clean 同HEAD接续不stage/commit/hook；index和HEAD不变，不重复提交。
AC06：只写新样本；原业务树/旧样本只读；既有#531开发Task身份不变。
AC07：七份 foundation 与实际 README、安装依赖及需求→设计→测试导航一致，真实纳入候选，不隐藏 dirty；同 D1 的 scope_ref 由原 stage owner 接续到实际 accepted_scope，输出丢失恢复同 key，不创建第二 Delivery。

## 返工与退出
stale或缺失结果回原producer。真实范围变更先原Clarify/Task整体PRD/accept_scope，再由当前stageowner合法rework，保持Delivery UUID及历史事实。输出丢失恢复同一结果，不新建对象。

## 排除
不做业务实现、provider接管、V07旧clean迁移、Release矩阵或正式source-lock。公共状态属于上游，Guru只通过薄projection承接原团队门禁与私有事务。
