# #819 Issue 审核评论与 Intake 迁移

## 当前边界

完整 matching provider 同批采用 workflow/routing、六个受影响公共包、Create Task
消费说明、schemas、commands、examples 与 extension manifest。没有新 Skill 或生命周期
writer。AI 判断覆盖、适用性与路线；脚本仅校验对象、相邻调用结果并执行明确副作用。
原 Task/gen/Delivery、#813 的 Creation 2.0/共享 Creation 3.0 和资源检查不变。

## 公共选择器与消费者

路径相对 `trellis/skills/guru-team/packages/<owner>/`，安装后对应
`.trellis/guru-team/skills/packages/<owner>/`。当前 Interface 选择下表 successor。已替换的 selector 和旧调用边界不作为 runtime fallback，
也不转换旧结果。仍受支持的原 profile 可以被 successor 确定性引用：Sync current input
3.0 引用 current input 2.0 的原普通/资格确认分支；Readiness ready 7.0 引用原完整链
ready 6.0；共享 semantic envelope 2.0 引用仍服务原完整链的 1.0。这些是当前独立
profile 的明确消费者，不是无人消费的历史资产，也不增设旧版本探测或兼容 parser。

| owner | 原选择 | 当前选择及唯一消费 |
| --- | --- | --- |
| Sync | current input 2.0，baseline_ready/synced output 2.0，固定 Discovery consumer | call-local current input/envelope 3.0；专用 issue-review-refresh input 1.0；两个 output 3.0 → guru-issue-intake-base-router。原资格确认返回仍进原 Discovery。 |
| Readiness | aggregate 1.0；仅本轮完整前序 profile | aggregate 2.0，新增 existing_issue_intake/issue_review_return 1.0。原 current_issue/proposed_draft/standalone_request 保真实完整 transition。 |
| Readiness ready | ready 6.0（文件名 public-ready-output-5.0） | selected ready 7.0，分别选择原完整链或独立 issue-ready 1.0 → 原 task-intake router。 |
| Discovery | aggregate 5.0/context_request 3.0/context_ready 6.0 | aggregate 6.0、context_request 4.0、context_ready 7.0；新增 issue_readiness_supplement/supplemented 1.0。supplemented 只回 Readiness；Clarify 的 context_request 只回原 Clarify。 |
| Clarify | delivery index 3.0/needs_context 4.0 | delivery index 4.0、needs_context 5.0；局部 input/supplemented 1.0。保原 source_actions 和 source_selection；同 Issue 事实往返回局部 profile。 |
| Wording | aggregate 1.0 | aggregate 2.0、局部 input/supplemented/requirements_gap 1.0。仍使用原完整标题/正文 scanner、record/check 和实际 receipt。两个局部出口只回 Readiness。 |
| Create Issue | input 1.0；created 表示 Issue 读回 | input 2.0 新增必填 review_comment_body；created 原形状保留，完成语义增加评论发布与读回。原 check 只读；recover 可补已确认未完成的剩余评论。 |
| Create Task | public profile 2.0/shared creation 3.0 | 版本保持；新增 ready 消费说明。Issue/base_source 薄投影，集成 branch 与 delivery target 仍独立审定。 |

包内独立 local owner schema 为 `issue-review-owner-1.0.schema.json`，只服务相邻
record/check/invoke；不进入公共 output、Task 或持久覆盖账本。Clarify 的独立
issue-clarification-1.0 复用原问答/开放问题/source_actions 定义，不要求全链 duplicate
snapshot、disposition token 或前序 receipt。Readiness 三种局部返回
按 context_result/requirements_result/wording_result 闭合区分，Wording 的 requirements_gap
独立区分。源摘要来自真实 producer stdout，不重建其私有 result 或完整前序 transition。

Registry 继续选择原 stable skill id 和各自现有 Interface schema 家族。extension manifest
更新实际 public input/output/private schema inventory；production-current-v6 仍仅选择其原
四包评测子集，不把 Intake 的新增能力伪装成该子集的新评测结果。

## 正向执行与来源

已有 Issue：实际 Sync → 原 Readiness。充分且适用则 ready；其余依缺口进入原
Discovery/Clarify/Wording，每次补足后回同次 Readiness；依据不足才执行必要全链。
只有真实基线失效回 Sync。原完整 Sync stdout 丢失时回原 producer 恢复，不能从三字段
反拼带 provenance/digest 的完整 transition。专用固定源恢复检查原精确 commit，保留
selected_ref；不重新解析后来前进的同名 ref。

新 ready 的 base_source.kind/selected_ref/commit 原样投影为
creation.reviewed_base_source；Issue 投影为原 reviewed_source，disposition 仍由 Create Task
审核。selected_base_ref 和 delivery_target 由原创建 owner 独立核定，不从来源推断。
synced_branch 保原标准化 branch 关系；新建前核 local HEAD，已成功恢复不因后来的 ref
前进重复创建。详见 MIGRATION-813，不能复加 retired reviewed_base_head 公共输入。

无 Issue 的讨论/草稿仍走完整必要调查和审核。只讨论/草稿到请求结果结束；仅创建到
Issue、评论及读回结束；还要求开工才以正式 Issue/真实评论进入 Sync → 已有 Issue
Readiness。no_issue 的原完整 standalone_request 审核不要求不存在的评论。

## 评论和在途恢复

评论正文规则只有 Clarify 的 `references/issue-review-comment.md`。Create 必须先正式
内容读回，再 POST/GET 评论，才能 created；Clarify 只在实际发布或修订范围内复用原
source_actions。只读审核不写。评论说明真实范围、结论、未决条件；没有机器 pass 标记
或资格体系。Create 的 attempt marker 只定位原对象，不能证明审核充分。

旧未完成 create/comment 操作使用实际操作时的完整固定 provider 恢复同一 Issue 事实。
本批前驱是 `4f2adef1f7b099f78bb8429e8b8facd66dce3bfc`；更早操作用其实际完整版本。
新安装重新完成必要语义审核后，仅对同一正式 Issue 明确补评论，不重新创建 Issue，
也不把旧 created 自动升级成新完成结果。新 recover 先找同 Issue，再查该 attempt 评论；
唯一已成功评论读回即返回，成功完整 listing 证实未发布才补剩余 POST。未知、多候选或
正文不符停止查明；不盲目再发。check 命令始终只读。

旧 Readiness/局部 receipts 不转换成新 pass。重新读取当前对象，进入适用原 owner。
活动 Task 继续当前 Identity/Ensure/session/Delivery 及实际阶段，不重置整体范围或身份。

## 分发与证据

已有 checkout 由原 guru-upgrade-tools 完整更新，保 Task/session 和用户内容；处理每个
.new/.bak 后做 installed、平台、mode、drift 与定向 reapply。不能手抄受管副本或因旧 Task
阻塞改用普通 apply。新安装采用原 installer。失败沿原同操作 resume/rollback，外部
Issue/comment 成功事实不能被本地回退抹除。

source wrapper fixture、真实 Agent、live GitHub 与 installed/reapply 是不同证据。
没有 live 发布/回读就不宣称 AC1/AC3 外部部分完成。本项不新增完整多平台 Release 矩阵。
