# D1 局部修复 Intake 与 Discovery 诊断设计

## 1. 设计目标、需求承接与内容基线

承接 [本批 PRD](prd.md) D1-R01..07、D1-S01..05 和 D1-AC01..04；整体责任由 [Task PRD](../../prd.md) R692-01..04/AC692-01..06 定义。D1 首次交付全部实现范围，Task Completion/Closure/Finish 另由原 owner 完成。

固定 development baseline B 为创建时已 Sync 的 main `6a65ec8afe6d180850760b3b2edf3f94be6e3b20`。这是 D1 内容比较起点；Planning H0 为该提交，PR 目标是 main。实施 HEAD 可前进；不得以漂移的 origin/main 替换 B。

阶段适用 authority：`docs/architecture/README.md` 的 `guru-trellis-architecture`、`docs/architecture/00-foundation/design-constitution.md` 的 `guru-trellis-design-constitution-v1` 和 `docs/architecture/06-governance/change-contract.md`。独立 Architecture candidate_assessment 已实际返回 `baseline_current/no_architecture_impact`；不建立 contribution 或 ADR。最终设计仍须在 Wording 后取得该 owner 的 final_plan，不把候选结论当最终规划通过。

## 2. 当前系统、边界与目标差额

当前 selector 已按实际范围和风险选路；草稿创建后进入 fresh Sync/Intake；Clarify 已消费 Discovery 的 duplicate snapshot；Author 已独占整体与切片正文，普通同范围装配恢复也已有合同。本批不重复建设上述能力或 #695/#694/#693 方法。

本批新增两项具体差额：原 owner 使用已读事实时明确“什么必须刷新、什么仍适用、当前还要判断什么”；Discovery 将原整体比较拆为字段诊断，并保留这些诊断直到当前执行 AI 能消费。没有本 Task 前序 Delivery，不推断业务 #372 的现场版本、实际路线或根因。

## 3. 来源设计处置（唯一）

| 来源/承诺 | 处置及具体落点 | 理由、影响与上游处理 |
| --- | --- | --- |
| #692 行为1：现有 selector/执行 owner、按实际影响选路，已有 Task 保留生命周期 | retain；第4节 owner 行与第6节 S01 | 细化购买提示/支付核心及 UI 风险边界，不改 mode DTO 或真实选择。无偏离。 |
| #692 行为2：正式身份、完整 live 正文和差额；原 owner 决定复用与重审 | retain；第4节逐 owner 表、第6/7节 | 保留 fresh Sync/Intake 全图；减少调查/装配重做，不复制旧 target pass。无跨 Skill 重入合同删除。 |
| #692 行为2：必要语义、真实选择、freshness、独立副作用；无变化 mapped 恢复自动承接 | retain；第4节恢复行和第7节 | 不新增确认状态、批准链或缓存；当前会话承担真实交互。 |
| #692 行为3：限定 Discovery 原公开链与实际共享校验；诊断实际字段/evidence 与原恢复 owner | retain；第5节入口/类别表 | 只拆现有比较、暴露原错误事实，不加强拒绝条件或增加 provider 调用。 |
| #692 行为3：摘要不证明 UTF-8 根因；保留错误合同及无敏感回显 | retain；第5/7/8节 | 只能定位 payload 绑定时明确该证据边界；JSON 读取错误继续归 #695。 |
| #692 行为4：AI/script、canonical/preset/dogfood、公共 I/O 兼容、最小证据 | retain；第4/5/7节及 implement 第6节 | 无新成功 DTO、typed exit、跨 Skill authority 或长期 evidence。check 的 additive 诊断和 stderr 承接在原合同显式说明。 |
| 当前用户验证限制与 #692 非目标 | retain；第8节及 implement 第3/5节 | 沿原正常质量链；不新增专项 replay/A-B/native eval、耗时测量、额外安装或矩阵。原业务与聊天只读。 |

## 4. 模块、职责与设计取舍

| 原 owner/源文件 | 本批行为差额及直接 consumer |
| --- | --- |
| `guru-select-workflow-mode/{SKILL.md,references/contract.md}` | 在原判断内具体区分“购买提示资格/展示”与价格、扣费、支付协议，并检查实际未改消费者和验证需要。保留高置信度自动选路、证据不足真实问题、已有 Task 的原路径；consumer 仍为原执行 owner 或 Sync。 |
| `guru-create-issue/SKILL.md` | 创建 readback 后，将正式 URL/完整正文（含原 marker）作为新 target。提示原 Discovery 使用同会话仍可核验的调查事实作线索；created DTO 不扩字段，下一步仍是 Sync。 |
| `guru-discover-change-context/references/contract.md` | 新身份/基线先 fresh 读取。原 owner 对已读 source/tests 的实际 revision、base 差额和当前目标相关性重审；未变且原完整内容仍可用的调查不用重新广搜。当前 duplicate search、history preview、Gate、record/check/invoke 保持。现场原记录缺失则保持未知。 |
| `guru-clarify-requirements/references/contract.md` | 使用当前 Discovery public output 与完整 live authority，先解决证据能回答的问题。已清楚的同范围事实不重复访谈或重装配 producer 私有结果；该 owner 亲自判断当前 intent、source role、disposition 与 scope。下一 consumer 仍为 Wording 或原 Author。 |
| `guru-author-task-plan/references/{authoring,planning-body}.md` | 整体 PRD 使用已完整读过的当前来源；D1 复用已接受整体定义的必要引用，展开本批目标、边界、起点、行为和验收，不再从零调查同一代码或重新访谈。Delivery design/implement 只拥有各自方案/步骤，不复制来源处置矩阵。每个阶段仍按模板完成自己的判断；失效事实回最早原 owner。 |
| Discovery `runtime/common.py` | 将现有复合相等判断拆为确定性的首个差异字段定位。嵌套输入/history 可定位键或数组位置；派生摘要只能定位到摘要绑定字段时不假称知道正文哪一字节有误。base 分类和原 code/status 不变。 |
| Discovery `runtime/{check,invoke}.py` | check 给当前 AI 完整诊断；invoke 对原先被降为 blocked 的错误写 stderr 三字段，保留唯一 stdout DTO。record 继续以原 CommandError 返回失败。 |
| 现有 canonical README/preset/source tests | README 只定位原 owner 的使用与诊断合同；受管机制同步 dogfood，包含基线已合入但尚未投影的 #706 内容，后者不计为本批新增成果。 |

选择直接修改既有 owner 和比较，避免新 recovery Skill、跨 Skill capsule、字段快照缓存或全局诊断框架。复用事实的依据是本轮 AI 对适用性的判断；Git identity 仅验证内容/版本，不能替代语义。原 #693 方法通过原引用承接，不复制其通用方法正文。

## 5. 接口与数据

所有公开 Skill input、成功 DTO、typed exit 与固定 consumer 保持。base 的 `current/refresh_base/blocked` 分类不变。原 record/check/invoke 参数仍使用 `--invocation` 的单 envelope，JSON carrier 失败仍由 #695 原读取层处理。

| 原公开入口与类别 | 当前不足 | 本批字段/evidence 与恢复 |
| --- | --- | --- |
| record：base observer/repository authoring | 部分只指 `base_current` 或 `repository` | 在原 `stale_identity`/`schema_mismatch` 内指到可判定的 mode、repository、selected-base、branch 或 base ref 字段。回原 Sync 或 Discovery authoring，不重写 producer。 |
| check/invoke：public input 与录制结果配错 | 多项比较仅指 `owner_result`；错误细节可被丢弃 | 首个实际差异定位 `owner_result.mode`、`change_input` 子字段或 `base_observation` 子字段。当前 Discovery owner 读取实际 public input 与 Sync transition，重建本 owner 最小结果。 |
| check/invoke：history/query/result identity | history 或 payload 差异共用整体对象诊断 | 指到 `history_preview` 的具体差异，或 `result_identity` 的实际绑定字段；history 变化回当前 Discovery 重读 preview/选择。payload 绑定差异须重读本 owner 当前证据和完整输出后重建；不得猜测 UTF-8 根因。 |
| record/check/invoke：base 正常变化/authority异常 | 有现成 reason，但恢复对象可能不明确 | 在现有 observer 分类内定位实际 ref/authority evidence；base 前进回原 Sync。dirty/错误 branch/缺失 authority 继续原 blocked，由原 owner处理事实后重入，不选替代基线。 |
| invoke：context_request 的目标身份不等 | 已有 `stale_identity` 与 `return_identity.target_locator` | 保留原直接错误 code/status/三字段形状，补充回原 Discovery/Clarify 取得当前 target 的支持入口。pre_task 没有该固定 target 输入，不增加新的目标比较或 provider read。 |
| 普通 live Issue 正文变化 | 本批没有新增 provider 比较 | AI 仍读正式身份和完整 live 正文；按原 fresh Intake 处理。不得把 local payload digest 验证描述为 live 正文已自动比对。 |

check 原 intermediate receipt 的 `result.status/typed_exit/reason` 保留，失败时 additive `result.diagnostic={code,field_path,remediation}`。它的直接 consumer 是当前 Discovery AI，用于解释、选择原恢复入口；不是新的 Skill output、审批或跨 Skill handoff。invoke 维持 `{exit_id:"blocked"}`，同三字段输出到 stderr；成功与 refresh DTO 保持，正常 blocked/refresh 的 objective reason 不改。原本直接抛出的参数、schema 或目标错误仍按原 error stdout/exit-status 处理，不统一改为 typed blocked。

诊断只包含固定字段位置和恢复说明，不包含 expected/actual 值、正文、原始字节或 OS exception。commands/catalog 与原调用说明明确上述 additive 信息；没有新 error code、schema reader、兼容分支或持久化。已有读取、secret redaction 和身份拦截不改变。

## 6. 状态、顺序、正常与失败流程

不新增公共 phase 或状态转换。S01 仍先 selector，再按实际出口进入原 task-free/standard 路径。S02 创建成功后保留 fresh Sync，再由 Discovery 对新 target 完成当前证据/Gate，Clarify/Wording/Readiness 各自判断和产生真实结果。

S03 整体 scope-only 写作、Clarify 接受、D1 创建、Author requirements、独立 Architecture candidate、Author solution、Wording、final Architecture、Approval、用户规划接受和 Activation 顺序不变。事实已经当前且同会话完整内容仍可用时，原 owner 直接核本轮差额和自己的独立判断，省去无依据的重新调查与重复访谈。

S04 先解析 JSON，再运行原一致性检查。失败仍失败；当前 owner 使用具体字段/evidence 诊断修复普通装配或输出读取，不把低层 checker 的 `status=passed` 当 semantic pass。S05 真实 base/target/source/scope 变化按原 route 重入；无新增副作用的同范围装配修正自动继续。缺事实或恢复有歧义时保留原 blocked，不制造成功。

## 7. 恢复、兼容、迁移与集成

错误后先区分 carrier/JSON、当前 local binding、正常 base变化、target/source变化。读取外部命令输出时捕获完整 bytes 再一次 UTF-8 解码，或用保留边界的 streaming decoder；不逐块独立解码再拼接。这个建议属于当前 owner 的读取方式，不新增 runtime parser 模式。诊断只证明所述绑定差异，根因仍须真实证据。

同源装配错误由原 Discovery 重建完整最小 authoring，经原 record→check→invoke；不局部修补录制结果中的 digest、producer transition 或旧 pass。真实正文/身份变化由原 Intake 读新 authority。base refresh 沿原 Sync。新副作用各自展示/确认，mapped 修复不新增继续问题。授权不持久化。

这是原字段诊断与 additive side-channel 的直接演进：原 inputs/code/status/DTO/consumer 保留；受控 check consumers 同批读 optional diagnostic，旧调用未读取该字段仍看相同阻塞结果，无长期双实现。没有业务数据迁移、支付接口迁移、外部部署或新安装要求。既有安装采用匹配完整 workflow/preset，保留用户改动、managed provenance 和 sidecar 处理；公共源码与 dogfood不证明外部已采用。

## 8. 验证设计

| 验证 | 层/输入与原入口 | 预期观察及证明边界 |
| --- | --- | --- |
| V692-01 | 原 Discovery runtime/真实 wrapper 回归；由真实 recorder 分别生成当前 workflow/standalone 结果，再普通误配输入与此前结果 | check 定位实际字段，invoke stdout 仍 blocked 且 stderr 给三字段；正常正确配对保留原成功。不是手改 hash/state 的攻击样本。 |
| V692-02 | 原 recorder 输出包含中文证据；以正常错误读取方式在多字节边界逐块解码，再交原 check/invoke；完整解码作正常对照 | 错误内容被原绑定检查拦截，定位 payload/result evidence，说明重读完整输出且不声称已识别解码根因；完整输出继续原链。只证明诊断与确定性行为。 |
| V692-03 | 原 observer/runtime tests 的正常 HEAD前进、dirty authority、错误branch，以及原 context_request目标配对 | 原 classification/code/status和consumer不变，字段/恢复说明准确；未触及 live 正文自动校验不作新通过声明。 |
| V692-04 | 原 Check/独立 Review 检查各 owner 合同、完整真实差额和未改消费者 | 核实触发/复用/重读/重审/consumer、原正式图及全部原子能力；不以文案存在或静态关键词宣称普遍 Agent 效果。 |
| V692-05 | 原 source/installed package validation、dogfood apply/reapply/drift、声明平台 bytes/mode、递归 sidecar、语法/Task context/diff检查 | 验证受管分发和当前运行副本；不新增 clean installation，不证明外部业务采用或完整多平台/Release矩阵。 |

所有 planned check 尚未执行；实际结果由 implement 的唯一 Test 落点记录。保留首次失败、具体恢复及未验证边界；不量化节省时间。

## 9. Canonical 引用、本轮差额与实际未决项

RDT 现行入口 `docs/{requirements,design,test}/README.md`；命中 `current/task-delivery-lifecycle.md` 的初始入口、唯一 Planning 和恢复职责，`current/json-input-carriers.md` 的读取分层，`current/knowledge-maintenance.md` 的原方法与原消费者。新增具体 Intake/诊断语义由原 RDT owner 形成完整隔离 proposed 单元及必要导航关系，沿 implement 第6节的 `delta_first` 在 candidate Check 后 final_integration 晋升，不提前改 shared current。

Architecture 使用第1节实际 authority，当前候选无影响，无 contribution/ADR。canonical Skill/runtime 是 step-local 行为源；README 只定位，不复制。没有必须由提交者选择的技术问题；后续真实遗漏回 Author，真实 scope变化回 Clarify。历史现场、业务效果与外部安装采用仍未知或未验证。
