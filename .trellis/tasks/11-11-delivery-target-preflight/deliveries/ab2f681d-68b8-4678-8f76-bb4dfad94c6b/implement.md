# D1：五处规划文本的实施与验证计划

## 1. 输入与引用

实际输入为 [整体PRD](../../prd.md)、[本批PRD](prd.md)、[design](design.md) 全文及其第3节唯一来源处置。原source_selection为空保留，唯一request仍按PRD第1节精确locator读取；proposal仅是拟改候选。实际Architecture candidate_assessment为no-impact，后续独立final_plan仍需完成。

本批从固定main `e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e` 独立开始，目标main观察为同一提交，无未交付继承前驱。五处源码与三层RDT单元、原安装机制和冻结行为协议的用途沿design第4/7/8/9节。实施前读取必要引用的完整条件，不以链接存在替代读取。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、原owner与文件 | 动作及完成观察 |
| --- | --- | --- |
| I1 完成规划 | 当前D1 PRD、真实candidate_assessment；唯一Author写本root | 完成design/implement和official contexts，原Author plan_ready→Wording→独立final_plan→Approval/Activation。不得提前把文件当批准。 |
| I2 五处源码 | 原激活后的实施owner；design第4节五文件 | 按已审proposal和design落点补共享第4节主定义、三模板短引用与Approval原维度消费；核diff不新增runtime/schema/phase或第二方法正文。 |
| I3 原分发 | I2可审核；原guru-upgrade-tools owner | 从完整新source preview精确目标，审写集、Task/session及并行保留范围，再prepare/invoke，同步shared package与Claude/Codex/Cursor；处理实际sidecar，读回工具升级结果及drift。 |
| I4 RDT隔离候选 | 源码方法确定；原guru-maintain-requirements-design-test-ssot | 在Task-owned位置准备既有三层生命周期单元的完整proposed及必要关系，保留现有定义，补本轮差额；不直接写shared、不新建平行current或README/index。 |
| I5 定向验证 | I2与可用安装；实施/验证owner，主会话协调行为回放 | 执行第3节V1–V3，采用仍适用事实，保留首次输出/失败与成本；独立观察AC3所需两分支。 |
| I6 原质量/晋升 | 完整源码/投影/RDT候选/工程结果；各原owner | 原候选Check→原RDT final_integration/readback→实际after重绑→最终Check及后续独立审查。no-impact无Architecture contribution/ADR，原阶段判断仍需真实结果。 |

每批写入前核同Task/generation、C4/C5、registered checkout、实际Git分支和公共Dkey/root。只改本Task范围，保留并行改动。提交或远端动作不包含在上述实现动作中。

## 3. 验证入口、输入与预期观察

| 验证 | 入口、输入与执行责任 | 预期与停止条件 |
| --- | --- | --- |
| V1（AC4） | `git diff --check`；原source/installed验证器；原 `trellis/presets/guru-team/scripts/python/test_planning_body_distribution.py` 的真实unittest入口；原安装owner的preview/prepare/invoke和 `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` | 五处语义差额可审，managed投影/三平台一致，Task/session保留，无未处理sidecar。选用当前managed Python与原测试模块环境，不为本改动新增关键词断言。命中验证完成即停。 |
| V2（AC1/AC2/AC5） | 外部冻结 `delivery-target-preflight-behavior-protocol.md` 四case；主会话调度同模型 `gpt-6.1-sol / medium`、同工具/预算的旧/新方法消费 | 每case最多300秒；记录首次输入/命令/输出、exit、耗时/调用、干预及判断。控制四case已经正确，候选未验证；正确性/成本分开，不预设新版胜出。 |
| V3（AC3） | 优先检查V2是否真实独立观察缺安排和完整安排；否则主会话增加一个极短Approval-only paired输入，同事实仅Policy完整性不同 | 缺安排被指出，完整可执行安排不误阻塞。该证据是方法回放，不是正式独立Approval；已有足够观察则不重复。 |
| V4（正式质量） | 原Check/Architecture阶段/独立Review公开入口，精确Dkey及完整实际候选 | 保留既有原门禁与Docs晋升要求，不以V1/V2/V3替代正式gate。未执行即报告未执行。 |

验证采用design第8节独立行为断言；机械、安装、Agent、正式gate分别陈述。完整Release/升级矩阵、真实业务部署/生产采用与缺陷率未验证。不追加惯例rollback/red-green或重复全链实验。

## 4. 停止条件与适用回退点

scope或真实承诺变化回原Clarify；机制/Architecture变化回原Author与独立Architecture；普通文本遗漏在原写作范围修订。安装source/target漂移、sidecar冲突或Task/session差异回原安装owner，不手补受管副本。RDT缺完整proposed或候选未通过不得晋升。

候选漏检、不可执行安排或误阻塞是有效失败，不修改冻结输入或用控制结果冒充候选。设施反复失败先有界诊断并标记依赖结论未验证，不无限扩成产品前置。正确但额外阅读/调用成本增加时如实报告，收窄重复表述；无增量收益也照实保留。

本改动没有数据迁移或远端发布副作用，因此不造数据库/发布回滚协议。必要文本回退仅撤回本Task精确差额并沿原安装owner处理对应投影，保留他人改动与原始证据。后续commit/push/PR/merge/归档均归原owner的独立动作边界。

## 5. Delivery Policy（唯一）

选择 `full`：D1覆盖当前整体R1–R6及AC1–AC5，没有隐藏分配给后继的需求。可独立交付条件是五处文本、必要受管分发和三层RDT真实差额完成，所需定向验证及原正式质量结果满足当前候选；不以方法回放或文件存在代通过。

实际起点/固定B为e30，Planning H0同e30，计划目标main当时同e30。当前无未交付继承差额，故本批无需等待旧Task交付，独立写作、实施和验证可继续。旧Task保持其原owner和交付责任。对未来实际依赖，仅原动作需要的真实条件成立时执行，不把无关main前进作为同步/Reconcile/重审前置。

本请求当前不含远端交付，后续如进入发布，原Delivery Review/Publish/Merge需读取实际候选、目标与支持条件，不能据本Policy自动push或Ready。公共“合并/完成/关闭”仍分别判断。没有后继片责任不等于验收已完成，Task Completion仍保整体责任。

## 6. Docs SSOT Plan（唯一）

当前文档状态为 `complete_docs`：既有三层生命周期单元完整存在，但缺本轮跨Task目标安排的明确方法。选择 `delta_first`；源码与Task-owned完整RDT拟写先形成候选，在最终Phase2前由原RDT owner完成reconciliation/promotion/readback，不让Task文档长期替代shared authority。

| 当前单元与位置 | 本轮差额、原writer及直接consumer |
| --- | --- |
| RDT-REQ-LIFECYCLE：`docs/requirements/current/task-delivery-lifecycle.md` | 原RDT writer在既有Planning/固定范围定义中补必要跨Task目标判断和合法独立路径；原Author/Check/Review消费。 |
| RDT-DES-LIFECYCLE：`docs/design/current/task-delivery-lifecycle.md` | 原RDT writer说明共享方法、模板与Approval消费关系；不新增生命周期或发布能力。 |
| RDT-TST-LIFECYCLE：`docs/test/current/task-delivery-lifecycle.md` | 原RDT writer补首次识别/误阻塞与证据层次边界；方法回放不等正式Approval/生产改善。 |

隔离候选由原维护owner选取Task-owned实际位置并准备完整单元，不预建空贡献。只写命中单元，不共享README/index/manifest，不新增平行current文件。Architecture为真实no-impact，无contribution/ADR/共享晋升写入；后续有实质变化才回其原owner。
