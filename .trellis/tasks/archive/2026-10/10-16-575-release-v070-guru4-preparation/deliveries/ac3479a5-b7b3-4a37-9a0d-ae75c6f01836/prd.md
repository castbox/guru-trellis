# #575 S3：修复工具升级的来源校验并交付可消费来源

## 1. 来源与整体范围

本切片继续承接整体根PRD R575-01..07 / A575-01..08，live [#575](https://github.com/castbox/guru-trellis/issues/575)「正式依赖前置」「Stage 1：发布准备任务」「Stage 2：同一 exact candidate 的发布门禁」「非目标与完成条件」，以及私有 `.agents/skills/release-guru-trellis-version/references/contract.md` Two-Stage Lifecycle 的规范性约束。整体 accepted scope不变，根PRD不改写。

已选来源包含 #578/PR#581 的依赖感知工程执行事实采用合同、#579/PR#582 的批量对象读取修复及各自终态归档；其产品实现和验收保留原任务归属。当前切片固定内容B仍为S2已交付head，既有整合来源与受管安装事实分别判断，不把旧installed `.3` 结果说成 `.4` 正式安装成功。

正常source==target的原tools-only路径先退休旧Guru manifest，再调用preset的source-only ownership校验；该校验在 `validate_installed=False` 时仍无条件读取已退休的installed manifest，阻断正常安装。修复该不可分前置属于现有准备责任。新的正式 `source_locked` 操作需要真实已提交修复源，因此当前S3先独立交付来源修复，后续Delivery消费它完成原定完整投影、正式样本与最终Docs；不降低整体验收。

## 2. 当前切片必须满足的行为

### R575-S3-01：source-only ownership校验只读取其声明的来源事实

修复 canonical `trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py` 的installed manifest读取边界。`validate_installed=False` 的来源校验不得要求target installed manifest存在；installed/default `True` 路径仍必须读取并验证实际安装证据，不能因本次修复放宽其缺失、错误或漂移诊断。

不绕过ownership验证、不制造manifest、不改变tools顺序、清单、公共API、schema、原恢复锚点或旧归档guard。判断参数语义和事实归属，不用特殊路径或异常吞掉错误。

### R575-S3-02：在原失败入口证明根因修复与既有语义保留

用同一个source==target原调用链复核：旧manifest按原owner退休，preset以source-only模式调用ownership校验时能够继续，不再因不存在的installed manifest失败。验证默认installed路径仍拒绝缺失或无效installed证据；测试样本由正常配置/安装路径形成，不手工伪造recovery、digest或控制状态。

区分根因定向回归、完整工具安装、目标native/next owner与业务完成。真实正式安装必须使用已提交且canonical clean的修复源，归后续Delivery；本切片测试或修复提交不冒充该正式结果。失败、SKIP及未完成层次如实保留。

### R575-S3-03：先形成可供新工具操作消费的实际已提交来源

当前切片的code、必要回归和isolated RDT delta通过完整当前Check、TaskCommit与独立committed全范围Review后，以中文Refs-only交付。其独立价值是可审查的普通缺陷修复及可由下一正式tools operation消费的committed `.4` source，不要求在该提交存在前执行依赖该提交的source_locked安装。

当前旧operation只由原tools owner从原不变source与原recovery处理；来源修复不能进入它的resume，也不能替换冻结plan/source或扩大备份。新的tools操作只在后续Delivery取得实际修复来源后由原owner重新prepare，不能把新operation叫旧operation恢复。

### R575-S3-04：保留最小真实Docs与历史边界

原RDT owner在既有贡献根 `docs/requirements-design-test-contributions/575-release-preparation/` 收敛当前修复的requirement/design/test/traceability，Test只记实际已执行结果、失败链及后续正式验证边界。当前delta final Phase2前reconcile，shared current不提前晋升。

后续完整投影与正式证据补齐后，再按私有release合同首次完整committedReview→必要串行RDT/Architecture promotion→freshCheck/TaskCommit/完整独立Review完成最终共享收敛。不得用S3来源修复Review代替后续安装/晋升差额审查。

## 3. 后续同Task必须完成的责任

原Completion在本切片实际交付后判断剩余义务，经additional_delivery_required与原Creation建立下一Delivery；当前不预建其UUID、规划或资源。后续仍须完成：

- 原tools owner从完整已提交修复源执行source_locked `.4` packages/runtime/schema/workflow及Shared/Codex/Claude/Cursor投影，保留Task2/session3、五规划、raw历史、配置/定制及peer/common pointer。
- archive-bearing当前目标通过受支持的tools-only更新、installed/targetnative、四平台bytes、ownership及只读dogfood drift；普通三平台apply/reapply只在无旧归档同来源代表性隔离样本执行，不迁移无关archives或放宽guard。
- 一个focusedCodex clean/local-workflow与真实stable `v0.7.0-guru.3` predecessor分离工具/选定旧活动Task维护，目标自身native及下一实际owner、正常同operationresume与不兼容单侧toolsrollback阻塞，全部按实际层次报告，不用preset替身或外部source代跑target。
- 最终唯一RDT/Test/双向trace和必要shared晋升，晋升前后独立门禁；完整WholeCompletion、reference-onlyClosure no_mutation、正常Finish/archive/bookkeeping。

后续owner采用#578工程事实必须独立判断真实依赖和适用性；未知、缺失、变化或新义务补受影响检查，不继承旧语义pass/token。#579实际目标传输与正式入口按同样规则复核。上述责任未完成不能宣称整体准备完成。

## 4. 当前切片验收与不变非目标

| 验收 | 可观察结果 | 整体承接 |
| --- | --- | --- |
| A575-S3-01 | source-only不存在installed manifest仍按source事实完成；default/installed验证语义保留 | R575-03..04 / A575-03..04 |
| A575-S3-02 | 原失败链同输入或等价正常样本定向回归可核实，正式安装明确留给真实修复源后续操作 | R575-01、03、04 / A575-05 |
| A575-S3-03 | 当前独立来源修复经完整Check/commit/Review、Refs-only实际交付，剩余责任可被WholeCompletion消费 | R575-05..07 / A575-06..08 |

最终main exact-candidate、远端immutableprovider、最终predecessor→candidate diff、tag-pinned smoke、Release与#575关闭仍归Stage2，当前source修复或隔离测试不代替发布证明。

不实现#577/上游#46人工旧归档激活，不改upstream/global/node_modules，不迁移CMS/业务/生产，不新增公共owner、状态、兼容reader、恢复框架或累计矩阵。不覆盖并行工作、历史Task/归档和原受管前像。当前PRD只定义要求；design独占来源处置和机制，implement独占DeliveryPolicy与DocsSSOTPlan。实际激活与Git/GitHub副作用仍沿各原owner边界。
