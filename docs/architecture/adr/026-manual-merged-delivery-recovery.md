# ADR-026 candidate：手动合并事实由原 Merge 归属

状态：proposed，Task-owned #557 candidate；补充ADR-024。尚未独立完整committed Review或shared promotion，不是current实现证据。

公开Task/Delivery模型是唯一身份authority。普通用户合并已有正式Delivery PR是正常外部事实，不保证Guru merge message、trailers、pre-merge gate或receipt存在。只以这些生成副产物识别结果，会丢失实际已发布/合入的正式Delivery。

决定：原Merge owner根据已有唯一public Task/generation/Delivery/Publication关联与真实PR/commit/two parents/target ancestry进行语义归属，调用原public historical_success记录actual immutable候选。没有充分public关系时不导入或创建身份。当前bounded方法支持ordinary two-parent merge，squash/rebase尚无本版机制。

结果恢复与当前gate适用性分离；真实CI/验证状态、head/content/authority差额由原owner判断后交原Completion，其整体scope职责不变。输出丢失重入读取同一事实，history只读该public记录；任意historical PR/bookkeeping不建立Delivery。新远端Guru merge继续原expected-head/message/trailers，不在恢复中再次merge。

不采用通用importer、新Skill、私有ledger、消息重写/重复merge/emptyDelivery，或用恢复自动完成Task。query2明确读取public事实；既有schema1/2及query1原历史职责和matching旧安装退出由原migration owners维护，不混旧checkpoint和新DTO。

实现/验证/兼容及remaining boundaries由#557唯一RDT贡献与Test承接。源旧完整carrier与新完整matching安装分别报告；不授权业务采用、backend现场恢复、软件Release或完整矩阵。shared ADR导航/current记录只在正式独立Review后由原promotion owner更新。
