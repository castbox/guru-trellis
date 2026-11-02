# 需求探索与确认验证策略

Identity：`RDT-TST-DECISIONS`；定义 T-DEC-01..04 / SC-DEC。承接 [R-DEC](../../requirements/current/requirement-decisions.md) 与 [D-DEC](../../design/current/requirement-decisions.md)，适用同一来源与基线。以下是策略，不是预填通过结果。

| 策略/场景 | 输入与受测层 | 预期观察 |
| --- | --- | --- |
| T-DEC-01 / SC-DEC-EVIDENCE | 真实 Agent：仓库可查事实、清楚请求及存在两种合理解释的请求 | 先调查事实；清楚请求不造问题；真实需求歧义不以惯例默认；UI 未画状态不删除旧业务 |
| T-DEC-02 / SC-DEC-CHECKLIST / SC-DEC-PARTIAL | 真实多轮对话与原 recorder/checker 分别测试轻度清单、接受、修正、部分及未答 | 推荐清楚、用户低成本确认；逐项采用实际答案，未答保持未决，partial 不关闭；不以 atomic_group 合并独立项 |
| T-DEC-03 / SC-DEC-RESUME | 重大方案取舍、纯实现细节、恢复及方案新增歧义 | 重大选择说明可行选项与影响；常规实现自主；恢复不重问有效决定，新歧义回原 owner；答案改变后续方案和验收 |
| T-DEC-04 / SC-DEC-DISTRIBUTION | 原 package、consumer 引用、真实分发/reapply、driver 的分轮/错误收集 | canonical 与安装投影一致，未来答复不泄露到首轮，真实 thread 身份恢复，失败/超时不记成功；无公共 schema 或授权状态新增 |

语义效果由实际对话及 AI 审查支持，脚本不按关键词判定选择正确。driver 双替身测试只证明输入分离和收集机制；教学例子不是真实答复；CLI 退出成功不等于需求清楚或质量通过。方法隔离试验与完整 Guru 正式入口/生命周期证据分开说明。

原 wrapper 测试检查显式提供的独立问题记录和 partial schema 拒绝；自动 reducer、close-before-open 和 reopen 的运行时保证尚未由本项证明，不把原合同文字当作实际执行证据，不在本项新增 reducer。未答不默认及逐项答复的语义另以实际对话观察，不以结构测试代替。源码、分发、实际 Agent、已有项目采用和完整多平台发布各有证据边界。定向验证不自动承担完整 Release/升级矩阵；失败、工具缺失或环境阻塞如实报告。

本项实际观察唯一见 [贡献验证记录](../../requirements-design-test-contributions/requirement-decision-exploration/test.md)。后续正式 Check、Review、交付或 Completion 来自其原结果，不在此循环记录自身最终通过。
