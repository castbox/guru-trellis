# ADR候选：Phase 2 recorder 输入职责收敛

状态：proposed；Task=710-phase2-recorder-authoring；owner为原Architecture maintenance。源为live #710，before为2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30。实施后拟晋升到docs/architecture/adr/phase2-recorder-input.md，当前不写shared current。

## 问题、依据与决定

原recorder同时接受11字段语义输入和完整schema6结果。正式说明缺实际Recorder Authoring，完整结果例子混作输入，诚实Agent须自行选择并可能把候选token填入Phase2私有字段。原最小语义输入已经正确生成客观事实；根治机制是说明、例子和实际输入支持共同收敛。诊断改善仅辅助，不能代替首次native验收。

选择target_native：正常record只消费既有封闭语义内容；客观字段全部由原recorder生成。同步迁移本仓record调用/模板，以显式MIGRATION-710退出完整6.0 record输入，不增加长期compat开关/双reader。保留命令id/argv、完整6.0输出schema、checker/invoke/maintenance完整消费及stale恢复。原AI九维、qualification/Architecture、public候选/Planning身份及全部typed exits不变；两个token仍分别服务原consumer。

该决定窄替代record.py的完整结果输入能力及把输出示例称authoring的现行说明；不替代checker/invoke结果消费，不改变历史版本、不重算旧结果。消费者处置见D1 design第7节，发现真实不能同步迁移的支持consumer时先回原Author/Architecture修方案，不能静默破坏。

## 替代与代价

仅补文档而无依据长期留双输入，会继续保留无需承担的选择和维护边界；统一摘要算法会改变两类consumer；自动重算完整旧结果会使过期语义继续通过；新wrapper/schema/通用恢复状态没有直接consumer，均不采用。当前代价是同步更新必要record调用测试、说明和完整matching安装，显式表达旧支持退出；旧结果消费测试必须保留。

## 实施、采用及验证边界

原Check package、preset和eval owner按D1实现；RDT/Architecture先准备各自完整隔离拟写，原候选Check后final_integration写入/readback，actual after重绑后最终Check和独立完整committed Review。旧完整安装在成套采用前保持旧合同；原工具owner保留Task/session与用户修改，不迁历史Task。

V710-01至05证明合同/命令/兼容；V06/07必须真实native首次candidate/final及finding，无host pass/答案/纠偏；V08证明受管分发。当前没有修复后的实现、native、安装或发布成功事实。#713完整链另验，但不能替本项完成这些责任。
