# D1 验证与实验方法设计

## 1. 设计目标、需求承接与内容基线

本批承接PRD R1–R5/AC1–AC5。开发基线B固定为 f16bb562e4ea844939786cebd5c6c20e686914b2，来自正式Intake采用的Git对象；Planning H0同B，未来内容范围为完整B..实际HEAD及dirty增量，PR目标main独立。Architecture候选实际返回baseline_current/no_architecture_impact，authority为guru-trellis-architecture、constitution guru-trellis-design-constitution-v1，candidate freshness sha256:169c411b792429214627c413e00bb4e2eb5fd3a979e3a123ec2932a31f1474c4。该结果只支持当前方案写作，不代替final_plan或实现Review。

## 2. 当前系统、边界与目标差额

quality-guidelines Test And Validation Value已有行为层级、因果依据、证据复用与停止方法。Author planning-body §3及原Review引用该正文。现有eval runner/adapters提供原生执行事实；其自身代码不是业务Agent读取的生产方法。本批直接在同一规范补两段完整方法，不新增Skill、schema、runtime、installer、阶段或公共DTO。首次D1无前序结果。

## 3. 来源设计处置（唯一）

| 来源与承诺 | 处置与落点 | 理由、影响、上游处置 |
| --- | --- | --- |
| #826 R1/R2：优先复用真实入口、可用就绪、证据清理后保留与维护 | retain；§4项目验证方法与§8 V1/V2 | 保留完整调用和失败语义，无上游变更 |
| #826 R3/R4：同材料、事前标准隔离、先匿名评价、原owner判读、复用runner、真实失败与小样本边界 | retain；§4对照方法、§6、§8 V3 | 方法正文与实际实验分开，无新评分authority |
| #826 R5：原职责消费、canonical分发并保留定制/session | retain；§4、§7及implement Docs Plan | 不新增总控或公共Skill，无上游变更 |

pstack两项方法仅为advisory，不继承其总入口、权限、固定并行或形式化验证要求。

## 4. 模块、职责与设计取舍

唯一生产方法正文位于 trellis/presets/guru-team/spec/workflow/quality-guidelines.md 的 Test And Validation Value，下设项目行为验证与维护、真实Agent方法对照两节。原Author计划验证时消费；原实施者执行；原Review判证据充分性。保持原owner不复制标准。若已存在引用不能使调用方找到新方法，只在原 planning-body §3 和 review-method 的验证段补精确小引用，不重复正文。

项目方法先调查真实启动/数据/依赖/入口和已有设施，再形成项目本地操作说明，包含启动、可用就绪、操作与结果、证据、清理、维护触发。目标项目已有方法能覆盖时直接采用。生成方法须实际跑通；写成draft但未运行不能算交付。维护以行为和入口为线索核对受影响路径，不建全局feature账本。

对照方法由原owner事前冻结具体问题、相同任务材料、评价准则和现行/候选方法版本。执行Agent只读任务和对应方法，不读host准则或另一侧结果。评价者以A/B中性标签读取真实输出和工具轨迹，先形成判断，再由owner揭示映射并解释差异。使用同模型与执行设置，差异如实报告，不新增模型默认值。优先复用原采集；现有runner若不适合独立中性材料，使用已有原生 codex exec --ephemeral --json 事实采集方式，不为此扩runner协议。工具只启动与保存原始事实，不决定通过。外部临时实验目录存材料和输出，只有直接复核需要时保留；tracked正文只记录最小结论和可定位来源。

独立Skill方案不选：本批无独立生命周期/出口/恢复职责，现有instruction_only还限Codex；新增wrapper或扩installer不能增加已确认用户价值。共用规范现有分发已覆盖三平台，无新分发路径。

## 5. 接口与数据

无API/schema/状态字段变更。原Author→验证计划→实施事实→原Review的接口保留。新增方法只定义同职责输入：项目与目标行为，或任务材料与比较问题；输出为项目可执行说明/执行事实，或对照判读和边界。不是新公共Skill DTO。项目本地方法路径由其已有约定决定；不强制公共仓库携带私有路径。临时采集不存授权状态、secret或业务私有原始数据。

## 6. 状态、顺序、正常与失败流程

项目验证：调查→选够用入口→完善说明→启动及就绪→真实操作→断言结果/副作用→清理本轮资源→回读证据。行为或入口变化→定位影响→更新→重跑受影响路径。依赖或环境失败保留为未验证；真实路径断言失败记录行为失败，均不能报pass。

对照：先固定标准与材料→分离A/B运行目录→同设置独立执行→保存失败与真实输出→匿名评价→owner解释映射和结果→满足问题即停止。不能因候选输掉而改标准或删旧失败。新证据缺口需要补实验时说明具体问题与决策用途，沿R735原停止规则。

## 7. 恢复、兼容、迁移与集成

现有方法、public API与状态兼容，无数据库迁移或新恢复协议。普通运行失败修复装配后重跑，保留原失败，禁止混成目标产品RED或覆盖旧结果。证据和项目脚本不随清理删除。canonical变更由原guru-upgrade-tools在本checkout同步受管副本，保留Task/session及用户内容，冲突/sidecar沿原owner；不手改dogfood。外部业务仓库采用尚未验证。

## 8. 验证设计

| ID | AC与入口 | 输入、动作、预期观察及限制 |
| --- | --- | --- |
| V1 | AC1/4，原生Agent读取候选方法并操作去敏CLI项目 | CLI将用户输入写JSON后读回，现有启动/脚本线索供调查。Agent建立或复用方法，实际操作真实CLI，捕获结果与文件副作用，清理临时数据后证据可读。仅证明该CLI样本 |
| V2 | AC2/4，维护同项目 | 普通入口参数或行为发生明确变更，Agent更新方法并重跑受影响路径；无关功能保持。失效旧说明应被识别，不预置具体答案 |
| V3 | AC3/4，现行/候选方法各一次原生执行与匿名评价 | V1/V2的同一初始项目副本、同请求和执行设置；host在运行前冻结准则：真实入口、可用就绪、独立结果/副作用、清理后证据、变更维护、诚实边界。评价者先匿名读取实际输出/工具记录，报告改善/退化/未证；无统计胜出要求 |
| V4 | AC5，受管分发/reapply/drift | 复用现有planning-body及review-sufficiency分发测试中的真实installer覆盖，针对新方法可读性补必要行为验证；实际tools owner同步dogfood并检查sidecar、三平台方法引用与Task/session保持。结构不代替V1–V3 |

V1/V2先走足够小的完整路径，V3复用相同事实不制造重复回归。host准则不传执行者；不会要求每条测试回滚旧版本。环境不可执行时报告缺口而非声明AC通过。

## 9. Canonical 引用、本轮差额与实际未决项

RDT current/behavior-validation-method.md R735/D735/T735需由原RDT owner准备完整增量：新增项目方法和对照实验定义及测试关系，不建立第二当前单元；共享晋升在实施和真实验证后、TaskCommit前。Architecture候选无影响，无贡献/ADR。quality-guidelines为唯一方法正文；必要消费者只有小引用。无未决产品选择。真实Agent和安装结果尚未执行；final_plan与Approval仍待当前方案审查。
