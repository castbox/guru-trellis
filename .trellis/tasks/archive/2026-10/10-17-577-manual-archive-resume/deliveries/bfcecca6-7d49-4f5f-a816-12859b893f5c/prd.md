# D1：人工旧归档恢复执行

## 切片与来源

本 Delivery 覆盖 Task 整体 [PRD](../../prd.md) 的 R1–R7、AC1–AC6，不拆出后继实施责任。Direct Source 为 [Issue #577](https://github.com/castbox/guru-trellis/issues/577)；配对公共恢复合同来自 [Trellis #46 / PR #52](https://github.com/castbox/Trellis/pull/52)。没有额外选定的规范性设计。来源和机制的最终处置由本目录 design 独占。

## 要求

- 从完整匹配来源的 `guru-maintain-legacy-task` 显式选择人工历史归档，不依赖目标旧 dispatcher、预先绑定或搬移。AI 审查原 Task、人工归档说明、历史交付、当前来源、原路径、session/binding和未完成责任。
- 只恢复同一 TaskId，采用公共返回的 generation/活动 locator。公共上游拥有受支持格式、归档/活动关系、转换、精确公共绑定、同操作恢复与回退；Guru 不复制算法。原归档和转换来源可读且仅作历史/溯源，当前 authority 唯一。
- 人工旧归档、正式 Finish/合法人工 Cleanup 的 Reactivate、未完成 Closure/Finish/旧 Finalizer 分别进入原合同对应 owner，不补造完成、seal、gate 或空 Delivery。历史 PR/commit由原事实 owner核验；缺失事实保留未知。
- 当前补差若改变 scope，由原 Clarify 承接并保留历史范围。仅补证据/验收进入对应实际 owner。只有真实的新实现切片才创建 Delivery；本次恢复不产生业务完成。
- 精确写集限所选Task、必要规划、明确关联session/binding与恢复状态。工具安装使用独立升级 owner，分别审查工具写集和数据兼容。保护其他任务/会话/checkout、dirty/untracked和后续工作，不强制全仓转换或清理。
- 同operation普通重试、丢输出、部分写入恢复及回退不重复导入历史或推进 generation。source stale、identity冲突和tools/data不兼容给出具体 owner、缺失输入及恢复入口，不循环重装或覆盖后续工作。
- 在一个代表性隔离旧安装拓扑中调用目标自身native identity/continuation及下一实际Guru owner，核验同一公共TaskKey和真实session或合法explicit-task路由。报告工具、数据、历史、session、native、业务验收各层事实。JSON/DTO或外部代执行不单独构成恢复成功。

## 验收映射

| 整体验收 | 本切片必须提供的证据 |
| --- | --- |
| AC1 | 人工旧归档、原规划/真实交付历史、无Finish seal，经完整来源维护恢复，目标native和下一Guru owner实际承接；原归档可读，当前路由唯一。 |
| AC2 | 历史交付与当前补差同存，scope按原Clarify处理，旧gate不通过、无替代Task/空Delivery。 |
| AC3 | 正式Reactivate/人工Cleanup、旧活动转换、history_closeout、完整Plan2及未完成closeout路由定向兼容回归。 |
| AC4 | 缺证据/不支持格式/歧义/stale/mismatch/依赖缺失均有具体诊断；只读入口不要求预修旧runtime或绑定。 |
| AC5 | 同operation重试、丢输出、普通部分写入/回退和后续工作保护；不重复历史、不额外generation，未选资源不变。 |
| AC6 | 实际source/build/API，canonical/dogfood/installed、声明平台投影、reapply/drift、sidecar和目标native联合结果。最多一个旧安装拓扑。 |

## 非目标与阶段边界

沿整体PRD非目标：不改实际CMS/业务数据，不跨仓实现，不改全局CLI/node_modules，不执行Release或完整累计矩阵，不扩张为通用恢复/攻击/锁/TOCTOU/并发压力框架。本文件仅定义要求，不批准方案或激活实现。上游包同版本标签及Issue关闭不构成匹配证明；具体已验证与未验证结果由本任务唯一Test记录。
