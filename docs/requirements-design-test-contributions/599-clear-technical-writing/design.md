# #599 设计增量

本文件定位本次责任和实现。唯一规则正文为 [clear-technical-writing.md](../../../trellis/presets/guru-team/spec/workflow/clear-technical-writing.md)，不在 docs 复制规则或示例。

| Identity | Responsibility / contract | Landing | Requirement | Test |
| --- | --- | --- | --- | --- |
| D599-01 / CON599-01 | 版本化正式来源与规则/例外/示例正文的唯一owner | canonical spec → .trellis/spec/workflow/clear-technical-writing.md | R599-01/02 | T599-01/02 |
| D599-02 / CON599-02 | 写作owner自检、审核owner原范围内语义判断；wording固定合同保持 | 各原Guru owner的短引用与共享正文职责段 | R599-02/06 | T599-02/06 |
| D599-03 / CON599-03 | 现有managed-spec、AGENTS有界区块、workflow及22平台入口装配 | MANAGED_SPEC_PATHS、canonical workflow/skills/overlays | R599-03/05 | T599-03/05 |
| D599-04 / CON599-04 | 完整原生注入消费或child自行读取；缺失暂停依赖正文，恢复继续 | 现有manifest/dispatch与共享加载合同 | R599-04/06 | T599-04/06 |

Architecture contribution：[599-clear-technical-writing](../../architecture/contributions/599-clear-technical-writing.md)。沿用 target_native 的common-spec与原semantic owners，不增加public DTO、wrapper Skill、语言审批、runtime state或hook。

已有安装通过匹配workflow更新及preset reapply采用本规则；源码提交不代表旧安装已经更新。用户区块、未知本地编辑和sidecar由原installer职责处理。完整多平台upgrade/Release矩阵仍由专门Issue承担。
