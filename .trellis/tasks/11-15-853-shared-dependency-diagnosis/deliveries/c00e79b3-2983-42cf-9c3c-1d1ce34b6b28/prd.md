# D1：共享依赖差额判断的当前诊断与最小处理

## 1. 整体来源与术语

整体 authority 为 `../../prd.md`，公共 accepted_scope revision 为 `sha256:fc23ca2a6aa40c3041e44cee8f34f31e125a462f3b9e7bb0ef95263698f65065`。本批 DeliveryKey 为 `{task_id:853-shared-dependency-diagnosis,lifecycle_generation:0,delivery_id:c00e79b3-2983-42cf-9c3c-1d1ce34b6b28}`；planning_root 为 `deliveries/c00e79b3-2983-42cf-9c3c-1d1ce34b6b28`。实际 scope_ref 选择整体 R1–R8、AC1–AC4，未另选范围。

| 来源 | 角色与本批用途 |
| --- | --- |
| [#853 完整正文](https://github.com/castbox/guru-trellis/issues/853)，当前能力、行为与方案、验收及边界 | 唯一 Direct Source；决定诊断优先、条件调查、对象与证据区别、原 owner 和完成条件 |
| [接受评论](https://github.com/castbox/guru-trellis/issues/853#issuecomment-6893545774) | 需求审查结论，不是当前缺陷或修复效果证据 |
| 整体 PRD 第1–8节 | 已接受的完整整体定义；本批承接全部范围与排除项 |
| `trellis/presets/guru-team/spec/workflow/workflow-contract.md`，Candidate Applicability And Coverage | 现有消费者连续性和工程事实适用性约束 |
| `trellis/skills/guru-team/packages/guru-author-task-plan/references/planning-body.md`，第2–5节 | 现有来源、完整正文、交付与验证约束 |
| `trellis/skills/guru-team/packages/guru-reconcile-task-base/references/contract.md`，Actual integration entry／Bounded Reconciliation Owner | 实际整合的原职责与触发条件 |
| `docs/{requirements,design,test}/current/behavior-validation-method.md`，R735／D735／T735 | 已有行为验证与因果方法，复用其原 owner 和证据边界 |

本批“原入口”是实际负责处理具体共享差额、形成采用／等待判断的既有 Agent 入口。“当前对照”是为未决问题取得当前行为事实的有界观察，不是新增日常检查。已提交对象、在途草稿与冻结实验沿整体 PRD 第1、2节区分。

## 2. 整体与本批目标、非目标

历史 G07 在已知共享关系后仍从路径重叠过快推导重复实现和整项等待；补读事实后改判。这个历史偏差不能独立证明当前方法或消费仍有缺陷。D1 的独立交付目标是从原实际入口取得当前依据，判断是否存在消费缺口或具体方法缺口，再完成必要最小处理和适用行为验证；证据充分时可得出无需追加修复结论。

本批覆盖整体全部 R1–R8、AC1–AC4，保留整体 PRD 第3、6节全部非目标。具体不预定新增方法、gate、TaskCommit 检查、owner、阶段、wrapper、全量 Task 盘点、资源锁或协调状态；不实施 #848/#850，不重放原业务工作树、云端或模型运行，不扩完整多平台 Release 矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

首次 D1，无前序 Delivery 或已交付结果。工作分支 `codex/853-shared-dependency-diagnosis`，固定起点 `a72981db56d2070d8140b468cab3a97ae82effd3`，交付目标 `castbox/guru-trellis:main`。本批创建只建立规划身份；当前未激活实施、未运行行为验收、未确认修复。

已有输入为 #853 的历史调查与当前合同，及本次开工审查时核对的 S3–S5 无差额事实。历史 H/T、dirty 快照和 dev 整合结论仅按整体 PRD 第2节的观察范围使用，不伪称本批已运行。仍缺实际原入口及其真实加载、使用和判断依据。

本批没有已确定的后继切片责任，整体全部验收由 D1 承担。若证据不足，继续同一 D1 的有界诊断，不能把“仍需诊断”包装为完成。相关 #736/#747/#779/#822 继续其原作用，Issue 引用不形成整项等待。真实 scope 或时序选择才回 Clarify；真实 base 整合沿 Reconcile，不同步无关分支。

## 4. 本批调用方、场景与流程

| 场景 | 调用方及触发 | 本批处理与预期可观察结果 |
| --- | --- | --- |
| D1-S1 当前消费诊断 | 本 Task 原实施／影响评估 owner；尚缺原实际判断入口的当前依据 | 定位当前既有职责和日常入口，沿它观察必要正文是否被加载、怎样用于具体结论；不把所有 Skill 变为新增检查对象 |
| D1-S2 共享差额判断 | 原判断 owner；已知实质变化影响当前候选／必要消费者，或结论缺事实 | 比较具体实现、增量、签名与调用、生成链、验证范围，指出必要适配与独立工作；重叠路径或测试名称本身不推出实现归属 |
| D1-S3 三类证据并存 | 原判断 owner；材料含已提交、在途和冻结实验 | 保持对象身份；区别静态差异与已执行失败，保留旧本地有效结论，指出新组合缺口 |
| D1-S4 条件调查与合法整合 | 原阶段 owner；材料含普通共享调用／无影响变化／已有适用结论，或真实必要依赖 | 无调查必要者继续原路径；必要依赖落到具体结果，真实整合沿原 Reconcile；不因较新 SHA 或 dirty 数量统一排队 |
| D1-S5 最小处理与复核 | 原实施／审核 owner；消费、方法或无需修复结论已有足够当前依据 | 消费缺口只改原引用／调用位置；方法缺口只改唯一正文；无需修复不增规则；修订后验证实际消费和判断，仍不足则继续诊断 |

## 5. 完整行为、条件与约束

**D1-R1（整体 R1、R7）：** 从真实承担具体判断的原职责入手，核对日常入口到已有方法的实际路径。采用仍适用真实行为证据；不足时由原 owner 准备中性材料做有界当前对照。历史错误、正文存在或额外注入完整方法后的单次成功不能证明当前缺陷或修复。

**D1-R2（整体 R2）：** 只调查已知实质变化影响当前对象／必要消费者、或拟作结论缺事实的线索。适用已有调查直接复用，只补变化／缺失事实；普通共享调用、无影响版本变化、没有共享差额或已有适用结论时继续原路径。换 Agent、阶段、较新 SHA 和 dirty 数量不新增检查。

**D1-R3（整体 R3、R4）：** 已交付按实际提交／公开结果判断；在途只是当前草稿，不作为另一方正式结果或本轮必须采用需求，不自动导入 baseline。只读必要内容并说明未证实范围，不新增持久快照、hash bundle 或跨任务账本。冻结实验仅支持其原输入／依赖／环境；静态组合不匹配不称为已执行失败，环境验证待补不否定仍有效本地结果。

**D1-R4（整体 R4、R5）：** 按实际适用内容核对是否同一实现、两侧新增行为、共享函数与真实调用、SDK／生成器与生成物、原验证和当前组合缺口。无需固定填表或布尔证明。相同文件、测试名称和文本冲突只是线索；跨文件无文本冲突仍可能需要适配。只由当前未满足依赖形成必要先后，落到具体提交、接口或结果，独立部分继续；不得据此接管另一任务 scope／owner 或要求其整项 CLOSED。

**D1-R5（整体 R6）：** 明确必须纳入的依赖、实际冲突、具体集成失败或用户同步请求沿原 Reconcile 固定对象，保留 Task／Delivery 与内容范围。另一工作树草稿／未来消费者差额不自动触发最新 dev 合并；必要适配回原内容 owner。不自动修改其它任务、发送跨会话指令、cherry-pick 未提交内容或覆盖其工作树。

**D1-R6（整体 R7、R8）：** 当前观察区分消费缺口、具体方法缺口、已有能力满足或仍需诊断。只对已确认缺口选择最小落点，实质修订才回原受影响 owner 重新判断，不复制完整规则或新增长期 wrapper。例子去敏并沿原位置，不成为用户答案、运行状态或当前通过证据。未知项保留具体缺口和下一步。

**D1-R7（整体 R8）：** 检查真实受影响的接口、生成链和组合，复用适用工程事实，只补必要证据，不要求双方重跑全部实验。修订后保持 canonical／dogfood／实际受影响平台及唯一方法源，由原安装 owner 同步并做定向验证；无修改不制造分发。无公共 API 改变不增 schema／DTO／typed exit，真实变化须迁移合同。完整 Check、独立完整 Review、readiness、Completion 与 Closure／Finish 保持。

## 6. 本批验收、验证方式与未决项

| 本批验收 | 对应整体要求与场景 | 入口、输入与预期观察 |
| --- | --- | --- |
| D1-AC1 | AC1；D1-R1/6；S1/5 | 读取实际原入口、唯一方法与必要消费者；当前证据能支持四种诊断分类之一和对应处理。仍需诊断不是完成；不把历史原因、需求通过或规划充分称为当前根因已定位 |
| D1-AC2 | AC2；D1-R1/3/4/6；S1–3/5 | 从受支持既有 Agent 入口启动中性具体工作材料，prompt 不补完整方法、正确答案或额外日常加载步骤。实际观察加载、工具和结论，区分同一实现增量／两套实现、已交付／在途、静态／执行事实，并落到接口／消费者／验证。脚本只采事实，原审核 owner 语义判断；有修订验证修后，无修订也须足够当前依据 |
| D1-AC3 | AC3；D1-R2–5；S2–4 | 去敏材料保留七个 dirty 快照文本预演冲突、两个已提交 dev 实际文档冲突及 dev 未含在途适配。观察不混同对象、不泛化整项等待、不覆盖他人或否定适用本地验证；普通无影响材料继续原路径，真实依赖走原路径 |
| D1-AC4 | AC4；D1-R3/4/7；S2–5 | 受影响跨文件调用和冻结实验保持正确证据范围，只补必要组合验证。实际正文／入口修订后验证唯一来源、引用、原安装同步和定向分发；无修订不制造发布工作 |

当前需求没有待用户决定的产品问题。原入口选择、实际证据是否足够、是否修订及具体修订位置仍待本批规划／实施 owner 调查，不预定答案。技术方案在 candidate Architecture 后展开；不能在 requirements 阶段预填其行为通过。结果充分后停止对应调查，不设固定样本数、大规模 A/B、节省比例或重复绿轮次。

## 7. Canonical 引用与本轮差额

| Authority | 适用定义与本批差额 |
| --- | --- |
| `docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md` → 各 current 入口 | `guru-trellis-rdt` active／knowledge-navigation-1，按实际命中单元读取，不建第二总 authority |
| `docs/requirements/current/behavior-validation-method.md` R735-01..03；对应 design D735-01..03、test T735-01..07 | 沿用条件→动作→可观察结果、原因果和停止职责；本批增量是 #853 具体共享差额的当前诊断与必要最小处理，不修改通用验证权威 |
| `trellis/presets/guru-team/spec/workflow/workflow-contract.md` 消费者连续性；原 Author planning-body；原 Reconcile contract | 复用原唯一方法与职责。是否需要正文／入口差额仍待证据；当前不预定新增方法 |
| `docs/architecture/README.md`、`docs/architecture/00-foundation/design-constitution.md`、`docs/architecture/06-governance/change-contract.md` | 由原独立 Architecture 对实际候选判断影响，不由 PRD 预填 no-impact、贡献或 ADR |

EVO-001/003/004/005/007 的来源保留、authority、唯一判断职责、最小交互和分发目标适用于本批；EVO-002/006 由原 Architecture／生命周期承接。本项不实施 Evolution 大重构，也不把其历史方案、旧阶段顺序或 Release 矩阵提升为本 D1 新义务。
