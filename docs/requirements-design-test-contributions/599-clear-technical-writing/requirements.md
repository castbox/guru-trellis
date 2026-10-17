# #599 需求增量

provenance=source_confirmed。唯一来源为 [#599](https://github.com/castbox/guru-trellis/issues/599) 的 R1-R5/AC1-AC8。继承 RDT .102/active 与 Architecture .94/active。本文件记录需求与责任定位；写作规则正文仅由 [canonical spec](../../../trellis/presets/guru-team/spec/workflow/clear-technical-writing.md) 拥有。

| Identity | 来源 | 增量责任 | Design | Test |
| --- | --- | --- | --- | --- |
| R599-01 / BEH599-01 | R1 / AC1 | 明确正式来源版本、已核对采用内容及项目规则元信息 | D599-01 | T599-01 |
| R599-02 / BEH599-02 | R2/R3 / AC3/AC4 | 全自然语言范围、原文与字面例外、准确语义及双语示例 | D599-01/02 | T599-02 |
| R599-03 / BEH599-03 | R4 / AC2/AC7 | 单一 canonical、managed-spec 与全部声明入口引用 | D599-03 | T599-03 |
| R599-04 / BEH599-04 | R4 / AC5 | 主/恢复/独立child在首次实质文本前实际读取；缺失诊断及恢复继续 | D599-04 | T599-04 |
| R599-05 / BEH599-05 | R4 / AC6 | 完整匹配安装与reapply保留用户指令，dogfood零漂移 | D599-03 | T599-05 |
| R599-06 / BEH599-06 | R5 / AC7/AC8 | 原owner范围内自检/审核；区分语义与机械、源码/投影/实际行为证据 | D599-02/04 | T599-02/03/04/06 |

完整标准认证、历史全仓重写、软件发布、自动业务仓库升级与完整Release矩阵不进入本增量。AC5最低行为证据缺失时，本Issue不得验收通过。
