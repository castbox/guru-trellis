# #396 设计候选

## 当前对象与调用图
canonical Skill：trellis/skills/guru-team/packages/guru-review-change-request/。
生产链：Sync -> Discovery context_ready -> Clarification clear -> Wording pass -> Readiness record/check/invoke -> ready。
public transition 是唯一前序入口，producer-private owner result 不跨 Skill。readiness runtime/common.py 负责 normalize_target、invocation、linkage、validate_semantics、build_result；record.py 已派生 Gate 三项，dispatcher 已把中间 stdout 包成 formal_exit=false/result。
现有 stage0_fixtures.py 的 readiness_context/readiness_prerequisites/build_readiness_owner 与 test_stage0_fixtures.py 的 ReadinessAdapterTests 负责真实 wrapper 隔离链；formal_exit_boundary.py 提供既有 native continuation runner。

## D396-01 最小 authoring
直接修订 existing package contract 的 Installed Authoring 与 draft 恢复说明，SKILL.md 显式引导读取该段；修正 public-proposed-draft-input.json 和 change-request.json source 示例的一致身份。
示例是可执行构造 recipe：输入实际 producer transition/source，直接取 transition.target_locator，不把虚构前序 pass/hash/receipt 写成生产证据。
draft authority digest 只计算 canonical JSON 的以下 projection：
{kind:"draft", repo:<normalized repo>, issue_number:null, url:null, state:"draft", updated_at:null, body_sha256:<current UTF-8 body SHA>}。
target 只携带该 profile authority fields；title/body hash 各有用途，不等于 authority digest。十维 summaries/evidence/findings/scope conclusion/Gate/route 由当前 AI 真正审查，示例数据不提供 semantic pass。
最小 authoring 省略 reviewed_linkage_sha256、scope_conclusion_sha256、findings_count，不调用 private linkage/normalization helper 来完成正常 Agent authoring。

## D396-02 receipt 消费与恢复
原脚本与公共参数保持。record 完成后把实际 stdout.result 整体替换 envelope.owner_result；同一 public_input/source/transition 送 check；加入实际 checker.stdout.result.validation_receipt，再 invoke 并消费其实际声明出口。
同范围参数错误触发当前 owner 重入：读当前合法 source 与真实前序输出，一次性重建最小 authoring，不从旧完整 result 局部补算，不改 producer transition；当前 AI 重审仍适用的十维事实。不涉及外部或 Git 副作用，不再请求确认。
真实正文/authority 变化则走既有 Sync/Discovery/Clarification/Wording 刷新，不能把旧 transition 修改成新内容。缺前序仅消费可用实际阶段的声明 re-entry，缺少必要原始阶段/receipt 时如实停止，不能合成。

## D396-03 五类误用与观测
| 正常误操作 | 预期观察/恢复 |
| --- | --- |
| proposed_draft 携带 caller_locator/request_id | 观察现有 normalization 是否忽略非必要字段；不新增额外拒绝。若 draft_id/digest 错误仍失败，重建 target。 |
| body SHA 作为 source_request_sha256 | 实际 recorder 报错；以当前完整 authority projection digest 重建后通过。 |
| 另造 draft_id | 真实 producer locator 与 source/target/public 不一致时失败；使用原 producer locator 重建，producer 不变。 |
| 从含 linkage_sha256 的 linkage 再求 digest | 显式提供的错误 reviewed_linkage_sha256 失败；恢复省略派生字段，由 recorder 构造。 |
| 旧完整 owner_result 只补局部字段 | 观察 stale/schema/linkage 不一致；丢弃该 consumer result，以当前 source/transition 最小 authoring 完整替换。 |

复用已有 fixture 的实际前序 wrapper 输出，并捕获 envelope 边界；扩展现有 helper 暴露/支持最小 authoring，避免另造平行 happy-path fixture。私有 helper只用于已有客观 fixture，新的正常 authoring recipe 不依赖它们。
正文修订样本重新执行实际前序链，检查新内容与旧摘要拒绝；不断言跨版本 locator 恒定。
runtime 修改是条件路径：只有独立合法 source/transition + 最小 authoring 经真实入口失败、且定位到 runtime 后，回到 qualification/必要 Planning 重入，再做最小修复；未发现合法失败时 runtime 不变。

## D396-04 真实 Agent 回放
复用 formal_exit_boundary.py 的 native continuation 结构与 managed launcher，加入 readiness recovery 场景而非新独立 evaluator。
隔离 repo 用真实 production commands 生成 Discovery/Clarification/Wording 输出，提供正常误调用 envelope、实际报错、当前 source 和 producer public output；native Agent 读 installed Skill/contract，形成自己的完整 readiness judgment，再自动构造合法输入到实际出口。
native prompt 只给事实、目标和边界，不提供 expected class/pass、手写 receipts 或 private runtime helpers。逐次真实 stdout 保留给 AI 审查；Python 不用计数/字符串替代 semantic grading。
AI 检查 Agent 是否读合同、保留 producer、完成十维判断、按 receipt 顺序到 ready、没有向用户重复请求同范围无副作用确认、没有 Git/GitHub/Task 副作用。缺前序场景检查如实停止。工具不可用记 unverified，不能宣称行为已修复。

## D396-05 分发与 owner
通过 preset canonical source 生成 .trellis/guru-team/skills/packages、.agents/skills 与当前 selected platform skill roots 的 projections；修改 canonical 后 apply --repo .，处理每个 .new/.bak，再检查 drift/source/installed。
一个代表性 clean installed target + 同一 target reapply，验证示例/合同和实际 ready 链；完整 update/upgrade/multiplatform release matrix 不进入本 Task。
Markdown 拥有 semantic/recovery 意图；脚本只构造/执行/校验确定性事实，不生成审查或用户授权。
不新增 store、公共 DTO/Schema/Skill/exit、所有权变更或兼容分支；现有 freshness/identity 保持。Architecture 是否受影响由独立 owner 对本设计与现有 consumer graph 判定。

## 替代方案与取舍
直接完善已有合同、示例与回放，使正常 authoring 更明确；不重做 Phase0 或把 Agent 恢复写进 runtime。
保留原 rejection 与 normalization：新增“所有多余字段一律失败”会改变 accepted legal behavior，没有当前必要性。
objective replay 证明参数正确性，native run 证明协作行为；两层证据分别报告，缺一不能由另一层推定。
