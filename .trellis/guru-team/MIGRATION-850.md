# #850：独立 Wording 退出

本迁移将当前默认链改为 Discovery → Clarify → Readiness，以及 Author → final
Architecture → Approval。原内容、Architecture、Approval 和 Readiness owners 保留
各自完整语义判断。删除独立 `guru-review-contract-wording` 包、scanner、词表分类、
专属 record/check/invoke 与仅服务它的路由；不提供替代 gate、alias 或双读。

## 当前公共合同

以下路径相对于 `trellis/skills/guru-team/`。当前 Interface、consumer 与 runtime
同时选择后继。已发布的前代 schema 保持其原 path、id 和字节，只供固定旧版本或
明确的历史合同验证；它们不提供当前 runtime fallback。

| 原合同 | 当前选择 |
| --- | --- |
| Clarify private owner 3.0 | `requirements-clarification-6.0.schema.json`；绑定 caller 捕获的源内容，和原 semantic identity 分开 |
| Clarify full-chain clear 4.0、clear index 3.0 | full-chain `public-clear-output-5.0.schema.json`、clear index 4.0；`clarity-current-4.0` 增加 `source_content_sha256` |
| Clarify public input aggregate 4.0 | aggregate 5.0，选择 local supplement 2.0 和 standalone_wording_review 1.0 |
| Readiness private owner 3.0 | `change-request-review-4.0.schema.json`，仅消费真实 Clarity；无 Wording linkage |
| Readiness source profile 1.0、input aggregate 2.0 | 三种 source profile 2.0、input aggregate 3.0；local return 2.0 仅含 context_result 或 requirements_result |
| `public-ready-output-5.0.schema.json`，实际 `$id= guru-stage0-review-change-request-output-ready-6.0` | 新 `public-ready-output-6.0.schema.json`，独立 `$id= guru-stage0-review-change-request-output-ready-full-chain-6.0`；aggregate 8.0 明确选择它及未改的 existing-Issue ready 1.0 |
| `wording_current` → Readiness | `clarity_current` 4.0 → Readiness；`readiness-current-4.0` 不含 Wording 对象或专属字段 |
| `supplement_wording` | 原 `supplement_requirements` 2.0，明确 `review_focus=requirements|wording_only`；同 Issue/source/continuation/gap 返回 |
| Discovery local context-return 1.0 | local context request/ready 2.0；context-request aggregate 5.0、input aggregate 7.0、context-ready aggregate 8.0 保留 review_focus |
| Author aggregate 2.0、delivery_wording_reentry | aggregate 3.0、delivery_content_revision 1.0；保同 Task/Delivery 与实际 change_refs |
| shared semantic-owner envelope 2.0 | current envelope 3.0；原命令 transport 与载体字段 `schema_version=1.0` 保持，选择当前 profile/result 合同 |
| 显式 Issue/draft 措辞请求 | 原 Clarify standalone_wording_review 1.0，终止于用户答复 |
| 显式 Markdown 措辞请求 | 原 review-change aggregate 2.0 / explicit_files 1.0 / wording_only；全文 snapshot 包括未变更文件。原 range profile wires 和完整独立审核方法保持 |

源 token 由单一纯函数 `runtime/content_identity.py::title_body_identity(title, body)`
计算。Clarify record/check 从调用期 `owner_context.change_request` 核对象、正文和更新
身份，保留最小 token，不保存原始快照。Readiness 比较实际当前 title/body identity。
Create Issue 使用同一函数计算原 target 的对应组合项，其其它身份与恢复合同保持。
任何 token、receipt 或 checker 成功都不代表语义通过或用户授权。

## 在途接续

- 完整 Intake 尚待 Wording：保留当前对象、原 Discovery/Clarify 有效覆盖，回原
  Clarify 补齐实际新增源身份判断，再进入 Readiness。不重启无变化的访谈或调查。
- 已有适用内容判断、待 Readiness：原 Readiness 复核当前对象与覆盖。缺后继源身份时
  回原 Clarify；不将旧 Wording 输出改标签为新通过。
- #819 原 supplement_wording 或未消费返回：原 Readiness 用同 Issue、source、
  continuation 与真实 gap 构造 Clarify wording_only。旧 wording_result 不进入新 return。
- 原 Planning content_changed：原 Author 读取真实 change_refs 与当前规划，进入同一
  Delivery 的 content_revision。等义修改只刷新直接依赖；需求、机制、Architecture
  或验收变化回最早受影响原 owner。不清空规划、不重建 identity、不首次激活。
- 接近 final Architecture/Approval：复用仍适用覆盖，只刷新受当前内容或合同变化
  影响的判断；不索取退役证明。
- 固定旧 provider 已开始创建 Issue、评论或其它副作用：先用同一完整旧 provider
  完成或恢复原操作，再更新工具。不把旧 envelope 交给新 runtime，不重复远端动作。

真实缺失来源或结果仍回原 producer。公共 Task/Delivery、scope、阶段、绑定、合法
选择与其它 freshness 检查不变。共享 schema 中保留的旧字面不激活已退役步骤。

## 匹配采用与退役

源码修改不会更新已有安装。已有 checkout 使用完整 matching source 的原
`guru-upgrade-tools` preview/prepare/invoke/readback/reapply；开发候选保持
`unverified=[formal_fork_source_lock]`，不能称为正式发行或 Release Gate 通过。
执行前按原 owner 展示精确目标、source、写入与删除集，并遵守真实副作用边界。

原 installer 的 stale managed removal 退休 Skill 包和平台投影；旧根 record/check
wrappers 进入原已知 legacy removal。未改 managed 文件可删除；用户修改保留并进入
原冲突/sidecar owner。不手抄 dogfood，不编辑 manifest 来隐藏差额。保 Task、Delivery、
规划、session、配置与并行 checkout；不迁移其它 Task，不修改共享 journal。

采用后分别验证实际 target resolver、installed packages、native entry、声明平台
bytes/modes、退役文件、用户修改/sidecar、Task/session 保持和 drift。源码/机械检查、
真实 Agent 行为、安装采用和外部结果分别报告；本文件不声明这些验证已通过。
