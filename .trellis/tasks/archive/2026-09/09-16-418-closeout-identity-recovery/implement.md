# #418 执行计划草稿

状态：D418-03 source实现、new-main无提交快进及dogfood reapply完成；当前candidate验证证据如下，正式门禁状态只由原owner结果承接。未创建commit或push。

## 1. 规划收敛

- [x] 创建唯一 task/branch/worktree，通过正式 checker 与 created 投影。
- [x] 阅读 live Issue、current owners、architecture authority 与定向 tests。
- [x] 正式 Merge preview 只读复现已知缺失输入被折叠为 internal_error。
- [x] 从正式 Branch Review checker 验证相同 stale 文案包含 checkpoint 缺失情形；原业务实例作为后续对照边界，不作修复前提。
- [x] D418-03 已替换为专用只读profiles，区分 snapshot、A/H、新Publication authority与原归档事实。
- [x] 完成修订方案的normal-scenario与solution-mechanism qualification。
- [x] 完成planning wording、Architecture Planning及guru-approve-task-plan。
- [x] 完成修订方案展示；当前处于后续实施与验证阶段。

## 2. 实施顺序

1. 用正常 producer 生成 archive/stale/re-entry fixture，先验证失败路径。
2. 修正 Finalizer transaction 与已有 archived recovery 的映射收敛。
3. 修正 Merge package 已知错误分类与所有正式 wrapper 的传播。
4. 完成修订方案资格、Architecture、Planning 审查并展示，再进入下列新增实现。
5. 先按设计建立独立profile/exit/schema/consumer/eval资产；用机器验证薄投影闭包，不以新增optional字段扩展旧DTO。
6. 实现 Branch Review archived_review 的完整复审及checkpoint退休、Publication archived_publication_review 的专属只读preflight。普通active入口保持原约束。
7. 实现 Finalizer archived_review_refresh：推导H、验证H/A与archive连续性、校验新Publication bytes，直接返回原ready_for_merge，禁止进入mutation loop。
8. 实现 Merge archived_review_request及review_refresh_required，只生成复审快照，禁止选择merge mutation。新增三条direct edges经原workflow消费。
9. 运行一个真实installed fixture的全链联接回归；补齐失败与零副作用断言，收敛Docs和四平台投影。
10. 完成首轮Phase 2、task commit与独立完整Branch Review后，由Architecture/RDT owner提升各task-owned contribution，再重跑promotion-created diff的Phase 2/commit/review。尚未完成这些步骤前不得进入Publication。
11. 在既定稳定边界处理new-main pair，保留dirty，不擅自stash、merge或commit；远端操作保持独立确认。

## 3. 验证集合

| ID | 场景 | 通过条件 |
| --- | --- | --- |
| T418-01 | 正常创建后归档 | 双端 mapping 为同一 archived locator，boundary 通过 |
| T418-02 | 同一事务 archived re-entry | 精确旧 projection 收敛，无重复 archive/commit/push/PR mutation |
| T418-03 | 缺失或冲突身份 | 明确诊断，零猜测修复 |
| T418-04 | 已知 Merge input/identity 错误 | 正式 wrapper 不返回无诊断 internal_error |
| T418-05 | stale review 与 fresh re-entry | 原 owner 拒绝当前不可用证据；完整当前审查与记录后重建 input，preview 成功；正常已退休 checkpoint 不阻塞 Ready 链路 |
| T418-06 | 真实内容/authority 漂移 | 不复用旧 pass、Publication payload 或 merge confirmation |
| T418-07 | 分发一致性 | source/installed checks、平台投影、reapply/drift/residue 通过 |
| T418-08 | archived只读完整链 | 正常producer生成completed archive和Ready PR，真实wrappers依次输出review_refresh_required、archived_review_passed、archived_ready、ready_for_merge；最后preview成功 |
| T418-09 | A/H分离 | summary commit集合唯一原tip H，H先于archive parent且内容连续；新复审A为当前archive HEAD，不能用A替换H；source/target task、archive bytes、PR状态和远端refs完全不变 |
| T418-10 | 快照与新Publication审查 | 新入口无旧handoff时只产生snapshot；中途body/head/state变化阻塞，只有十维新审查通过的实际PR bytes进入Finalizer；不能用snapshot冒充旧或新pass |
| T418-11 | 原路径不回归 | 普通Publication仍拒绝completed，原Finalizer锚点约束不变；正常Ready不重审退休checkpoint，旧输入/旧exit/旧command行为保持 |
| T418-12 | Architecture三阶段只读 | 三个新source_exit分别触发branch_review/publication/acceptance_finish；证据不足或需写入的语义结果为blocked，零promotion/repair/业务写入；错误需写出口在边界拒绝 |
| T418-13 | truthful Publication finding | metadata/task_work保留真实分类并只读blocked，external_blocker保留blocked维度，全部current才archived_ready；旧profile语义不放宽 |
| T418-14 | B与PR payload漂移 | Branch Review输出真实B；Publication/Finalizer拒绝base ref前进到B'；title或body变化拒绝旧snapshot，不丢失B、复用旧审查或继续写入 |

T418-05 必须从确定的支持入口出发，不手改 hash/artifact/state 构造故障。不得以底层 mock exception 替代正式 wrapper 回归。

T418-08使用正常workspace/任务/归档producer，现有fake provider只隔离远端传输，不代替formal owner结果或output projection；保存测试内的原始fixture比较快照，不保存用户授权。AI语义执行证明与deterministic fixture证据分别报告，不能以host预填pass或关键词断言宣称native语义链已通过。真实业务实例仍独立标记unverified。

四个新增profile的写入范围仅为原owner-private recorder/checker的短期结果及退休；T418-08/09对task/归档/branch/remote/PR/Issue断言零mutation，并对旧映射状态验证明确停止而非只读入口修复。

## 4. 命令与范围

每次 task worktree 写入前执行：

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --root . --task .trellis/tasks/09-16-418-closeout-identity-recovery --json
```

从 live package commands 与 managed Python runtime 解析测试命令，不导入 eval/private helper 生成 gate。实施后使用已有分发命令：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

本普通 Issue 不执行完整多平台 throwaway 矩阵。accepted scope 需要 clean install 证明时，仅运行一个代表性实例；exact-candidate Release evidence 由 Release owner 负责。

## 5. 当前局部实现与证据

- Finalizer 已增加双端 task locator 收敛与精确 committed archive recovery；修改范围仅该 package runtime/tests，workspace mapping 与 boundary validator 保持原边界。
- Merge 已从发生点显式传播 known input/provider/stale 诊断，补充 commands/error catalog；四个 public exits 与 DTO shape 不变。
- managed Python 执行 Finalizer `unittest discover -s trellis/skills/guru-team/packages/guru-finalize-task/tests -p 'test_*.py'`：100 tests，33.608s，通过。
- managed Python 执行 Merge `unittest discover -s trellis/skills/guru-team/packages/guru-merge-task-pr/tests -p 'test_*.py'`：51 tests，9.580s，通过。
- 现有 reviewed-content integration：2 tests，10.221s，通过；不证明 D418-03 的新复审链。
- source `runtime.validate --root . --mode source --json`：23 active packages、78 commands，通过；`git diff --check` 通过。
- 仍未完成：D418-03、正式 preview-to-archive-recovery 全链、installed/dogfood apply 与 drift、完整 Phase 2、任务分支和新 main 的基线协调。
- 主检出 main 已为 `78651e2068184e9e52a778fe33eda8b2bd7c8e0b`；task HEAD 仍为初始 `57e8b5df10aedc4f218a4685e819d25a44aa8928`，局部改动未提交。没有 push、PR、merge 或业务状态修改。

## 6. D418-03 本轮实现验证

- 新增四个profile、三个success exits及三个Architecture只读source/stage限制，原mutation路径保留。
- Publication从错误workspace字段读取locator的问题已删除，使用真实task identity loader；测试不再构造workspace.task_artifact_dir。原stdin parser多余参数已精准修复。
- 五个package定向结果：Finalizer 108、Merge 61、Branch Review 34、Publication 67、Architecture 26项测试通过。Publication修正后主会话复跑67项通过。
- `test_archived_review_integration.py`：3项，67.078s，通过。实际installed wrappers依次输出三项新success结果及原ready_for_merge，最后原Merge preview成功；验证A/H/B、title/body/head/Ready drift、checkpoint退休和业务状态零mutation。
- `test_archived_fixtures.py`：3项，79.242s，通过，覆盖8个installed post-owner recipes及完整前序真实DTO；只证明deterministic staging/transport，不声称fresh native semantic authoring。
- `test_skill_packages.py`：14项，28.235s，通过；source包校验23 packages/78 commands通过；新增exit总数从live Interface派生为100。修改过的非生成Python文件均不超过3000行。
- 后续必须基于新main重跑适用验证，再执行source/installed/platform/reapply/drift及完整Phase 2。原业务实例、fresh native语义执行和Release矩阵仍独立unverified。

## 7. 新基线与投影验证

- Task分支无新commit地快进至 `78651e2068184e9e52a778fe33eda8b2bd7c8e0b`，与origin/main一致。六个重叠文档三方合并无冲突，其余120个既有dirty文件逐一hash一致，暂存区为空。
- 新基线上：installed全链3项（67.410s）、Publication67项（9.221s）、Finalizer108项（89.005s）、Merge61项（49.333s）、Branch Review34项（32.877s）、Architecture26项（18.891s）通过。
- post-owner staging3项（91.182s）通过；source package校验通过。
- 同步canonical workflow后使用 `apply.sh --repo . --all-platforms --json`，完整保留Claude/Codex/Cursor与Shared投影。137个自动生成的旧bak逐一核对HEAD与canonical后保存在本轮workspace外备份目录，未删除其内容；再apply后status=ok、installed=passed、sidecar=0。
- `check-dogfood-overlay-drift.sh`通过；无冲突路径、无mode变更、`git diff --check`通过，主检出保持clean。
- 本节更新前两节的旧基线/未reapply状态，不将历史结果改成新candidate证据。独立committed review、Architecture/RDT promotion、fresh native语义执行、原业务实例与Release矩阵仍未完成。

## 8. 配置回归闭环

- Branch Review的空runtime_root/publish.remote恢复既有default语义；Merge使用configured同仓库publish remote，空值和非dict保持原fallback，不新增输入字段或Yaml能力。
- 修正后完整Merge65项（91.159s）、Branch Review35项（48.397s）、installed全链3项（73.519s）通过。独立检查确认两个配置finding闭合，无剩余finding。
- 修正后重新三平台apply，9个自动生成bak按前一installed manifest逐一核对后保存到本轮备份目录；最终installed=passed、sidecar=0、drift通过。其它三个package的108/67/26项验证不受该config修正影响。
- 五个package当前合计301项测试通过；全链、post-owner staging与native/业务/Release边界继续分别报告，不将fixture或schema通过当作新的AI批准。
