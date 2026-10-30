# JSON 输入载体测试策略

Identity：`RDT-TST-JSON-INPUT`；适用来源为 `8d746ce561c464ca28af4dc91adf085132e4098c`。本单元只拥有测试策略；实际结果和观察截止由 [#695 Test](../../requirements-design-test-contributions/695-json-input-carriers/test.md) 单写。要求与设计分别见 [R695](../../requirements/current/json-input-carriers.md)、[D695](../../design/current/json-input-carriers.md)。

| Identity | 行为关系 | 入口与可观察结果 |
| --- | --- | --- |
| T695-01 / SC695-READ | R695-01/02/04；D695-01/02 | shared runtime tests 执行真实 reader/decoder，观察合法 inline/stdin/普通文件、文件优先、原 symlink 支持与长 inline；对明确缺失、非普通载体、读取/UTF-8、空、语法、非 object 和 mixed 歧义核对 code/field/status/恢复与无敏感回显。依赖模拟只用于普通读取失败，不建立额外 failure matrix。 |
| T695-02 / SC695-BIND | R695-01/03/04；D695-03/04 | 原 Bind runtime/contract/recovery tests 和原 wrapper 验证双 - 在读取前冲突、zsh process substitution 准确拒绝、完整双文件及 stdin+inline 的正常 resume。正常 wrapper 使用真实 TaskKey/session 和已完成的原语义 owner 结果；核对原合法出口与同 Task Delivery selection 保留。空 object 的 schema failure 不算完整成功。 |
| T695-03 / SC695-CONSUMER | R695-01/04；D695-02/04 | 受影响 Publish/Merge/Finish profile 预读执行已读正文 decoder；原 downstream loader 保持。定向 qualifiers/envelope-only 回归验证其各自准入不改变；不以 shared tests 声称所有业务 lifecycle 通过，不触发远端写入。 |
| T695-04 / SC695-INSTALL | R695-05；D695-05 | source/installed package validation、实际 help/error schema、选定平台 bytes/mode、plain apply、原 tools-only 同步、reapply/drift 及递归 sidecar。区分 source 通过、apply preflight 拒绝与真实目标采用；不手改 provenance。 |
| T695-05 / SC695-GATES | 全部 R695/D695 | 原 candidate Check → RDT final_integration → 实际 candidate 重绑 → Architecture/final Check → commit → 独立完整 Branch Review/readiness 覆盖最终范围。基础 syntax/JSON/Bash/Task/diff 检查按既有质量合同；未执行 gate 不预填 pass。 |

沿用 [T630-02/07](native-compatibility.md) 的原公开输入与分发责任；本策略不改其历史证据或接管累计矩阵。环境缺口记 SKIP/阻塞；源码、单元、installed/真实 wrapper、业务现场和 Release 分开报告。不增加专项回放、A/B、native eval、固定 case 数、耗时统计、额外 clean installation、真实多平台 Agent 或完整升级/Release 验证。
