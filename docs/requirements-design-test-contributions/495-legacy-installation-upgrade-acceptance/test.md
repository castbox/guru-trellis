# #495 固定来源最终验收证据

状态：隔离验收贡献，非 Release Gate。继承 [`.72` Test strategy](../../test/versions/current-main-0.6.17-guru.72/test-strategy.md)；本页补充固定远端验收与 `T495-DELIVERY` 来源增量，不重写前驱失败记录。

固定 Guru：`6a563f5f06cb1284c0935b3a2be68524d93df988`，独立远端 fetch、clean/nonmutable；provider：`gh:castbox/guru-trellis/trellis#6a563f5f06cb1284c0935b3a2be68524d93df988`。固定 Fork：`8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1`，CLI `0.7.0-castbox.2`，合并后 main CI `37473087582` success。目标 Guru `0.7.0-guru.2` 未发布。

## 正式 public/provider 七场景

首轮 **5/7，exit 1**，保留原日志；两份原失败 fixture 后续同 owner 恢复及原 canonical remaining assertions 通过，终态七场景证据齐备，未称整套单轮 7/7。

| 场景 / strategy | 实际结果 |
| --- | --- |
| 完整 planning / T495-RESUME | initial resume_required，两次原 resume 后 upgraded；actual installed、identity/branch/checkout/session、两类 qualification、Architecture/wording/fresh Planning 通过，原数据保留。 |
| 精简 unpublished in_progress / T495-TASK, T495-RESUME | 同类恢复成功；进入当前 dev/check session，已提交/dirty/untracked 保留，未知 createdAt 保持空字符串。 |
| 退役目录含普通 local-notes / T495-DISTRIBUTION | installed 与 resume 阻塞未知非空目录；处理三处 local 内容后原 resume 成功，未削弱 validator。 |
| partial deferred 新 notes / T495-RECOVERY, T495-ROLLBACK | 原 resume 拒绝 changed deferred，rollback 以 task_work_since_core_migration 拒绝覆盖，新增内容保持；该部分目标未升级完成是预期边界。 |
| 普通 preset 冲突、无新工作 / T495-RECOVERY, T495-ROLLBACK | 原 resume 成功后实际 rollback；全部 repo bytes/modes、HEAD/status、旧 task/version 恢复，旧 runtime smoke 通过。 |
| partial native 新 meta / T495-ROLLBACK | 首轮 FAILED；后续原样本首次 resume upgraded，installed 通过；原 canonical 断言证明 meta 保留且 rollback 拒绝覆盖，恢复脚本 exit 0。 |
| current creator / T495-MIXED, T495-DEFERRED | 首轮零写入 internal_error/FAILED；后续原样本同 plan initial upgraded，installed 通过；正式 creator、identity/checkout/native session、direct old 与 casefold 占用拒绝及旧 bytes 保留断言通过。 |

两次 initial 零写入 internal_error 原因未知；`Command failed (1): node` 也未归类，不统一称网络根因。首次 provider force 明确 registry timeout；同 provider 重试后 update dry-run/skip-all、workflow create-new 字节审查后 force、preset apply/reapply 成功。actual installed/shared/Codex/source 通过；3853 managed hash rows 零 mismatch、可执行模式匹配、recursive sidecars 零，workflow/source lock 字节相等，重复应用无漂移。声明平台静态投影沿 `.72` 定向证据继承，真实 native 主迁移为 Codex，不泛称多平台 Release 矩阵。

## MIG-495-06：真实交付与构造在途分别验证

真实 PR #195 OPEN，head `a9e65e0419c1e35f73ca6faf3c7b09d2ce370d4c`，branch `feat/chat-entry-opening-latency`，base `claude/requirement-implementation-3983cf`；exact HEAD provenance 为 core `.16` / Guru `.41` / clean source `a32ffdca61f432bc6c3e0557fe68486c1422d08f`。脱敏 faithful task 的旧 base `release/1.7.0` 与 pr_url null 均不作当前 authority。原隔离 fixture 首轮零写入 internal_error，same input/plan 重试 source_locked 升级成功；deferred task bytes 保留、无关 current owners 通过、direct old 拒绝，live PR 前后不变。处置 pinned-old/manual，未发布新 PR。PR #58/#210 均 live merged，但缺 confirmed TaskRef/trailers，不能投影为当前 MergeResult/Completion。

构造样本固定旧 a32，使用正式 native task `synthetic-old-inflight-495` 和真实临时 Git/bare。旧正式 writer 产出 schema `3.0`、`next_transition=push_content`、未绑定 PR 的非 terminal 快照；原路径正常返回 ready_for_merge 并完成 terminal cleanup。实际本地 push 2 次；test provider create 1、edit 0、ready 1；终态后 operation 0。旧正式 builder、gate recorder/checker、serializer/schema、writer/executor、archive、local commit/push 未替换。

构造 test doubles：load_task_runtime_identity、assert_workspace_boundary、prepare_closeout、finalization_publication_owner_result、require_gh_auth、validate_github_remote_repository、resolve_closeout_pull_request、resolve_closeout_terminal_pull_requests、create_pull_request、update_pull_request_metadata、run_gh_command、finalization_live_open_close_issues、finalization_package_root。它们只供旧 harness 固定 fixture facts，不证明真实 GitHub 发布、原始业务在途或当前 gate。

成功原生样本前的失败保留：首次 managed runner 路径错误；精简 task 的早期样本被正式 Fork preview 拒绝为非 known-legacy；两次 native start 因 context 空停止，正式 add-context 后成功。未改生产代码或手填生命周期，早期精简样本不计最终验收。

快照在独立复制 repo/bare 使用相同固定新 source 的 public preview 与 source_locked upgrade：preview 识别唯一完整旧 task，managed 4896、hash conflicts 0、reviewed core conflicts 0、sidecars 0。tasks 转换列表为空，明确 deferred 旧在途；7 个 reviewed retired core paths 删除，3 个脱敏 core 修改 replacement。首轮 resume_required，preset detail 为未归类的 node 失败；一次原 public resume 返回 upgraded/unverified=[]。目标实际 installed 校验 passed，旧任务/规划/context/transaction/gate/runtime/history 共 **16 文件 bytes/modes 一致**，本地 HEAD/全部 refs/复制 bare refs 未变，事务仍 push_content，无重复 commit/push/PR/merge。直接旧 identity 返回 unsupported_legacy_task；同 migrated fixture 正式 native current creator 创建无关任务，identity_established，之后旧 16 文件/refs 与 actual installed 再次通过。

## 结论与边界

上述证据覆盖 MIG-495-01..09 的固定代表性迁移、最低任务接续、旧交付诊断、保留、恢复/回退与 distribution；构造样本只关闭 accepted MIG06 来源缺口，不扩张为旧事务自动接续。真实业务 checkout/worktrees、用户指定 Fork 与固定 source 的 HEAD/status 核验保持，未升级真实业务仓。

本贡献供最终审查/晋升消费；独立 committed full-diff review、expected `.72` successor promotion、promotion 后 fresh Phase2/commit/review 与最终 Publication/merge/Completion 尚未完成。完整累计多平台矩阵、tag/Release、真实业务安装未执行。本页只保留这些直接 consumer 所需的结果，不携带原始业务记录、本机路径、授权过程或 qualifier 恢复状态。
