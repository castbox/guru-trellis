# #712 test delta

适用源：main `3a4b65ab08cdfe05d97f68e7f2e7512254d728f1:docs/test/current/completion-closure.md`。完整拟写位于 [proposed](proposed/docs/test/current/completion-closure.md)；按目标最终位置解析其相对引用。只调整原 schema1 限定并新增 T712，其它有效条件保持。状态 promoted；候选 Check 后由原 RDT owner 完成 current 整合与读回。

## 本批实际验证

- Reactivate 定向回归 18/18、既有实现 13/13、identity 20/20、archive resume identity 4/4，共 55 项通过。最后的 expected-key 兼容调整后，formal 子集 11/11 再次通过。五个变更 Python 文件语法检查和 diff-check 通过。
- 使用固定成对 CLI/Core `0.7.0-castbox.6` local_candidate 完成一个代表性 clean target 安装，并通过原 tools owner 更新工具。实际 installed Reactivate 返回 `session_binding_recovery_required`，原 Identity、Ensure、Bind 分别建立身份、定位 checkout、完成 generation 1 会话绑定。
- native continuation 和 JSON context 读取 generation 1、无当前 Delivery。原 Clarify 的 task-scope revision 实际返回 `scope_ready/no_change`，消费 BASE-01～05 的历史 accepted scope；未创建空 Delivery，也未声称后续编辑能力已经交付。
- 同一目标通过公共 projection 和原 Finish 确定性 archive helper 准备合法的再次归档代表状态。此准备不代表执行了正式 Completion/Closure 语义审核。实际 installed Guru identity、native Python collision、原 Reactivate archive/successor reader 均识别 generation 1 后继；native collision 为空，原 compact 归档十个文件仍与原 Git 版本逐字节一致。
- 原 tools owner 同步 dogfood；canonical、managed runtime 和平台 Skill 投影一致，dogfood drift 检查通过。无 formal fork source lock 更新。

以上 native 验证使用受控 GitHub provider 与隔离候选包，只证明本地集成和正常续接。没有修改真实业务历史任务，没有验证真实 GitHub backend 的业务恢复，也没有执行完整多平台累计升级或 Release 矩阵。最终正式 Check 与交付结果由各原 owner 独立产生，不由本记录推断。
