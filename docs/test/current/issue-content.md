# Issue 内容的测试策略与观察

#819由原RDT owner在完整实施和真实工程结果后完成final_integration并读回；状态为integrated_pending_review，尚待TaskCommit及独立committed Review。固定before=4f2adef1f7b099f78bb8429e8b8facd66dce3bfc，来源与替代边界见[#819追踪](../../requirements-design-test-contributions/819-issue-review-intake/traceability.md)。以下旧观察保其原截止；本轮实际结果由[#819 Test](../../requirements-design-test-contributions/819-issue-review-intake/test.md)拥有。

Identity：`RDT-TST-ISSUE-CONTENT`；状态：`current`。导航别名：`T153`、`T153-01..05`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。来源为[#153 历史 Test](../../requirements-design-test-contributions/153-issue-content-ssot/test.md)与 #818 的实际 old/new、正常返修、分发及目标采用观察。

本单元由原 RDT owner 在 #818 批准 Planning、实际实现及工程结果完成后，于 `codex/818-issue-minimal-sufficiency` 的 final_integration 实际整合。整合前重读真实目标、适用来源及必要关系，写后逐项 readback；整合状态为 `integrated_pending_review`，尚待 TaskCommit 与独立 committed Review。该事实不产生 Check/Review pass 或 Task Completion。原基线为 Git `fd0ee32618433a92ae934e29afb5b72e7136b4f7`；本次来源及精确替代范围见 [#818 贡献](../../requirements-design-test-contributions/818-issue-minimal-sufficiency/traceability.md)，普通当前读取无需拼接提案。

本单元承接 `.109` 测试入口所连接的 Issue 内容测试策略及历史身份，不迁移其余继承范围。规则正文仅由 [canonical Issue 内容规范](../../../trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md)维护。行为、机械分发、代表安装和外部结果分开；知识整合不产生质量或整体验收通过。

## 保留的测试责任与历史观察

| 身份 | 策略与原观察边界 | 对应责任 |
| --- | --- | --- |
| T153-01 | 修改前通过真实原入口调查既有能力，区分已有可用行为与本次差额。#153 曾实际得到草稿 `ready`，只证明当时正向链可用。 | R153-01；D153-01 |
| T153-02 / T153-03 | 从当前来源执行原写作、完整正文审核、必要修订和适用回读，核来源、条件、局部语言范围及只读边界。#153 的 V1–V7、#619 创建/修订及缺失恢复均为该次历史结果。 | R153-02/03/04/05；D153-01/02 |
| T153-04 | 用真实 preset writer 核完整 package、声明平台、引用、reapply、用户保留与 sidecar；分发通过不证明平台 Agent 行为。#153 具体次数、耗时和首次设施错误保留历史。 | R153-03/05；D153-03 |
| T153-05 | 在代表目标由原 tools owner 完成匹配安装、重应用和实际 readback，核 Task/session、配置、native 入口、installed 和 drift。#153 的 local_candidate 成功不证明正式 source lock。 | R153-05；D153-03 |

全部 #153 原始事实和当时未验证边界保持在 [历史 Test](../../requirements-design-test-contributions/153-issue-content-ssot/test.md)。这些固定案例与外部对象不成为后继任务的普遍执行义务，也不能作为 #818 新行为或新安装已经通过的依据。原 T153 身份继续检索策略与历史，当前 #818 结果由下列 T818 身份单独承担。

## #818 策略与当前观察

### T818-01 / SC818-WRITING：实际写作与修订

使用原 Clarify 入口和已有简略/修订示例的等价正常请求，区分原始要求、未采用建议和当前草稿。验收侧核完整输出是否收敛无依据要求及派生义务，同时保留同源保护和真实适配；被测 Agent 不取得预期 Finding。旧版无需先失败，不把示例或静态文本比较当真实写作证据。

旧安装首轮已实际指出“全平台保障”草稿中的审计落盘、渲染注册表、固定设备/样本及后续 Issue 义务与来源冲突，并查明 source/installed JSON 形状不同。实际完整修订稿保留 JSON 模式兼容和退出码，摘要采用同一次 validator 结果。首轮语义观察当时缺少 upstream DTO，没有伪造正式 blocked/pass/ready。

新安装上的首次等价请求已真实执行，未读取 #818 规划、canonical 新方案、RDT 提案或旧观察修订。首次完整修订删除了上述扩张并保留原 JSON/退出码、同一次结果和只读保护，但仍加入“未传 --json 即显示摘要”和“摘要必须展示模式统计”两项未由原请求选择的要求。主协调器读取完整稿后识别这两项残留；现有统计不自行授权展示义务，摘要启用机制应留原规划。首次稿及其已取得结果保持原样，不改称首次无遗漏。

同一 run 的后继正常返修已完成。最终完整稿撤去两项无来源要求及派生验收，保留 source/installed 两个真实入口、同一次原 validator、各 mode JSON 兼容、原退出码、只读及失败诊断责任。主要结果的验收在前；配额、审计、渲染注册表、自动修复和后续 Issue 义务没有进入最终稿。启用方式和排版明确交原规划 owner，统计字段只保留为原 JSON 兼容事实。该稿仍是尚未实现摘要功能的需求，不能把样例未来功能验收写成通过。

### T818-02 / SC818-REVIEW：四原职责及正式结果

通过原 Wording/Readiness 审核同一未完成草稿及修订稿；Create Issue 只做创建前原语义核对并停在外部写入前。审核者独立读取完整正文和来源，分别说明多余要求、必要遗漏及适用重审结果。scanner 命中、维度字段和上游通过不替代判断。

旧安装实际公共链为 `baseline_ready → context_ready → clear → pass → ready`，各原脚本退出码为0。Wording 对完整修订标题/正文完成 scan 和语义判断，Readiness 完成十维；Create Issue 核对实际 ready 的内容身份及当前 duplicate 查询，但未 invoke 创建。该结果是一个 Agent 在原职责内的真实执行，不证明多个独立 reviewer、其他平台或新安装行为。

新安装首次语义观察保留在 Clarify 修订之前。首次 Wording 后补执行 scan/record/check，当时缺少正式 Clarify 前序，没有 public invoke；首次 Readiness 的缺 clarity 回送经过 record/check，但 public invoke 在 `stdout.transition.candidate` 返回 `schema_mismatch`，没有正式出口。该现存路径已由原协调器判定不进入 #818 的 Intake runtime/I/O 改动范围；此处只保留本轮出口与证据边界，不产生本项修复、测试或后续放行义务。

随后真实原链完成 Clarify `refresh_context`，再经 Sync/Discovery、Clarify `clear`、Wording `pass`、Readiness `ready`，Create Issue 完成写前核对。首次完整修订仍含 T818-01 所述两项要求，说明该轮原审核漏检，不能将 formal ready 描述为无遗漏。新链另有一次 Discovery authoring 使用旧 selected_ref 导致 `stale_identity`；执行者以实际 Sync 输出完整重建本 owner 结果后成功，没有改 producer 或把失败冒充通过。

正常返修后，原 invoke 实际依次返回 `refresh_context → baseline_ready → context_ready → clear → pass → ready`，均退出0。Create Issue 再次独立核对完整实际标题/正文、当前前序和 repo/duplicate，但未调用创建 invoke 或 record-plan。已核对最终完整稿、原 formal stdout、写前核对和 provider 连续性；20份 provider 正文未变，返修没有修改 canonical/installed。该结果证明本次受支持返修和原 Gate 能形成符合来源的最终正文；不证明首次盲测无错、多个独立 reviewer、普遍性能改善或其他平台行为。

### T818-03 / SC818-DISTRIBUTION：真实 writer 与回归

`test_issue_content_distribution.py` 通过真实 writer/reapply，覆盖完整 installed 和22个声明平台的受影响正文、示例、四入口/三个合同、来源依赖、用户保留及零 sidecar；本轮通过，耗时188.944秒。

共同规范有真实差额，因此运行 `test_review_sufficiency_distribution.py`。首轮八个 subtest 因旧固定 loader 措辞断言失败：recovery-only 的原 Check 仍要求加载规范，但不使用被正则锁定的句式。经原 implementation_discovery 接纳此验证修正后，仅删除固定措辞/命中断言和重复 spec 读取，保留十二 consumer 的完整 installed/platform 字节、provider spec/manifest、引用、reapply、用户内容和 sidecar 检查。原完整测试重跑通过，耗时53.922秒；没有改 Skill 迎合测试，也没有增加关键词规则。

本轮采用实施 owner 已执行的 source package43/command126、upstream ownership、394个 Python 文件内存语法、Task context validation 及 diff 格式通过事实。这些事实与当前无脚本运行逻辑变化相符，只提供其各自层级证据，不证明 #818 Agent 方法效果或完整安装矩阵。

### T818-04 / SC818-ADOPTION：本 checkout 的匹配采用

原 `guru-upgrade-tools` 从完整 matching canonical candidate 完成本目标 preview、prepare 和 invoke，实际返回 `tools_upgraded`，版本为 `0.7.0-guru.8`。执行 owner 已回读33个内容投影与 frozen source 一致，声明平台为 Claude/Codex/Cursor；manifest 的 new_copies 和 managed_backups 均为空，3,345个 Task/session/配置文件比较无变化。该事实来自原安装执行者的实际终态与 readback，不声称由本 RDT owner 重新安装。

同一操作随后按原 installer 的 `tools_only=true`、冻结 public plan 和同一 upstream_ref 完成 reapply，没有 prepare 或创建第二操作。skill/overlay 均为 `ok`，installed validation 返回0，new_copies/managed_backups 仍为空。最终 source/installed package 验证均通过，source 为43 packages/126 commands，installed errors=[]。dogfood drift、其内 upstream ownership 与声明平台/native root 检查通过，workflow/platform/spec 与 canonical 一致；目标自身 resolver 可执行，native continuation 返回0。

reapply 后再次比较3,345个 Task/session/AGENTS/配置文件，differences={}；原 tools owner 通过同一 complete checkpoint 完成 peer/common pointer 与 physical write isolation 校验。原 Delivery current 仍为同一 key、implementing，原 planning accepted 不变。上述命令均实际退出0，V4 的本目标采用验证已完成；新安装行为另由 T818-01/02 记录，`formal_fork_source_lock` 保持未验证。

## 证据定位、停止条件与未验证范围

本轮观察绑定 TaskId=`818-issue-minimal-sufficiency`、generation=`0`、DeliveryId=`8d34df6b-a0f0-4066-9dfd-c1e2fb7d354b` 和 Git 基线 `fd0ee32618433a92ae934e29afb5b72e7136b4f7`。观察截止于本次 final_integration 前已完成的原安装/reapply及新行为正常返修。真实结果由执行者回报，本 owner 已核对旧首轮/修订报告、新首轮及后继完整稿/报告/正式出口/写前核对、两项分发终态及最终 reapply/source/installed/drift/continuation/Delivery current。临时原始日志保持其原观察，不把运行目录或逐轮 scan 搬入长期证明账本。

本轮分别提供 #818 AC1 的实际写作/审核/正常返修证据和 AC2 的分发/本目标采用证据。主协调器完整复核最终正文后确认 engineering_ready；该事实不是 Check/Review pass。现有证据足以进入本次原文档整合，不追加没有具体问题的实验。未执行正式 GitHub 创建/正文修订及其 live readback、其他平台实际 Agent、完整多平台升级/Release 矩阵、formal Fork source-lock、正式发布或业务仓采用。原创建 executor 本轮无差额，不为补证据制造外部对象。TaskCommit 与独立 committed Review 尚未发生，文档整合不证明 Task Completion。

## T819-01 / SC819-COMMENT：评论生产与读回

从原Create/Clarify入口验证实际评论内容与本次覆盖/结论/未决一致。Create的完整草稿审核、正式内容一致读回、评论发布/读回和created终点顺序必须被实际executor测试观察；Clarify局部覆盖不冒充全审，POST/PATCH对象和readback一致。隔离gh替身只证明执行层，不宣称live成功。对应R819-01、D819-01。

## T819-02 / SC819-RECOVERY：只读与同对象恢复

纯只读Clarify零comment mutation；本次发布/更新结果不明时先沿原owner找回唯一已成功对象，不重复Issue或评论。Create部分完成/输出丢失与Clarify原source_action恢复分别观察，不借人工改hash/state构造排除场景。实际GitHub创建/评论的目标和payload先明确，live readback与mock分开；没有外部执行就保持未验证。原Readiness消费及三补审/来源/安装证据见local-fix-intake的T819-03/04/05。

本次实际结果由[#819 Test](../../requirements-design-test-contributions/819-issue-review-intake/test.md)单写。#153/#818的旧案例、失败、未验证边界保原截止；本提案不把新评论或分流机制宣称为既有已验证能力。
