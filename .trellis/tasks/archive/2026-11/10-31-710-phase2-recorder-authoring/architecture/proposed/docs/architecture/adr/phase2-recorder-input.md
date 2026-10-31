# ADR-PHASE2-RECORDER-INPUT：Phase 2 recorder 输入职责收敛

状态：accepted。来源为 Issue #710；适用 before 为 Git 2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30。原 Architecture owner 维护本决定；实际采用和验证由 #710 Test 的原始结果定位，不从决定生效推断。

## 问题、依据与决定

原recorder同时接受11字段语义输入和完整schema6结果。正式说明缺实际Recorder Authoring，完整结果例子混作输入，诚实Agent须自行选择并可能把候选token填入Phase2私有字段。原最小语义输入已经正确生成客观事实；根治机制是说明、例子和实际输入支持共同收敛。诊断改善仅辅助，不能代替首次native验收。

选择target_native：正常record只消费既有封闭语义内容；客观字段全部由原recorder生成。同步迁移本仓record调用/模板，以显式MIGRATION-710退出完整6.0 record输入，不增加长期compat开关/双reader。保留命令id/argv、完整6.0输出schema、checker/invoke/maintenance完整消费及stale恢复。原AI九维、qualification/Architecture、public候选/Planning身份及全部typed exits不变；两个token仍分别服务原consumer。

该决定窄替代record.py的完整结果输入能力及把输出示例称authoring的现行说明；不替代checker/invoke结果消费，不改变历史版本、不重算旧结果。消费者处置见 MIGRATION-710，发现真实不能同步迁移的支持consumer时先回原Author/Architecture修方案，不能静默破坏。

## 替代与代价

仅补文档而无依据长期留双输入，会继续保留无需承担的选择和维护边界；统一摘要算法会改变两类consumer；自动重算完整旧结果会使过期语义继续通过；新wrapper/schema/通用恢复状态没有直接consumer，均不采用。当前代价是同步更新必要record调用测试、说明和完整matching安装，显式表达旧支持退出；旧结果消费测试必须保留。

## 实施、采用及验证边界

原Check package、preset和eval owner按各自原职责实现；RDT/Architecture先准备各自完整隔离拟写，原候选Check后final_integration写入/readback，actual after重绑后最终Check和独立完整committed Review。旧完整安装在成套采用前保持旧合同；原工具owner保留Task/session与用户修改，不迁历史Task。

验证策略与实际结果由 docs/test/current/knowledge-maintenance.md 的 T710 和 #710 Test 定位。合同/命令/完整消费、首次 candidate/final native 与 finding、受管分发分别证明；只有其真实原结果支持对应结论。#713 完整链另验，不能替 #710 完成自身责任。重新出现不能同步迁移的实际 recorder 完整输入 consumer、真实字段职责变化或原阶段前提变化时，由原 Author/Architecture 重审。
