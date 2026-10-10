# #396 实施与验证计划

## Phase 1 entry
当前仅 planning。先完成 planning Wording、独立 Architecture 与 Plan Approval；展示当前方案后由 workflow 取得接受，再经 guru-activate-task 进入 Phase2。
规划文件不代表实现或任何完成门禁；授权信息只在当前对话。

## 执行顺序
1. 重读 live #396、current authority、canonical contract/examples/runtime 与既有回放入口，复现合法最小 draft 链；记录既有能力和真正缺口。
2. 修订 existing readiness contract/Skill 导航及 producer-bound 最小示例，清晰声明 source/target/transition 与三项派生字段 owner；不新增 wrapper/API/缓存。
3. 扩展 stage0_fixtures.py/test_stage0_fixtures.py 现有 fixture：以实际 transition 构建最小 authoring，实际 record.result 整体替换/check receipt/invoke，覆盖五误用后重建、正文刷新和真实缺前序。producer 未改是关键观察。
4. 扩展既有 formal_exit_boundary.py 的 readiness continuation，执行真实 native Agent 恢复与缺前序运行，AI 阅读实际 transcript 分别判定；无需重复确认同范围无副作用恢复，真正外部/Git 副作用继续停在其 owner。
5. 合法链路若复现 runtime 缺陷，先定位 causal failure、重新 qualification 和必要 Planning/Architecture，再最小修复并加入该合法失败回归。不存在合法 defect 时不修改 runtime。
6. 执行 Docs SSOT Plan，通过 RDT owner 维护 isolated contribution、trace 与唯一 test.md 结果。Architecture contribution/ADR/晋升依赖独立 owner 真实结果，不预填 pass，不竞争 shared current。
7. apply/reapply 同步 dogfood 与完整代表性安装，source/installed/声明平台 projection、drift/hash/mode/sidecar 定向验证；逐个处理 .new/.bak。
8. 配置要求的 implement/check dispatch 仅做 approved scope；真实全 task Phase2、Task Commit、独立 origin/main...HEAD 完整 Branch Review。晋升产生新 diff 时重跑。
9. Delivery Review 后单独展示 commit/push/PR、Merge、Completion/Closure、Finish 与 Cleanup 精确边界。caller_owned app worktree/branch 予以保留，Cleanup 依据实际 ledger 给出处置。

## 验证映射
| Requirement | Responsibility | 必要证据 |
| --- | --- | --- |
| R396-01..03 | D396-01/02 | managed production wrapper draft chain，最小 Gate/authoring，实际 record/check/invoke stdout 与 ready |
| R396-04/05 | D396-02/03 | 五误用各自观测、准确错误、完整消费者重建、producer 相等；不强制 extras 拒绝 |
| R396-06 | D396-02/03 | 新正文真实上游刷新、新 authority、旧 digest 拒绝、缺前序如实出口/stop |
| R396-07 | D396-04 | 实际 native transcript + AI semantic review，行为和客观结果分别报告 |
| R396-08 | D396-05 | canonical/dogfood/installed/声明平台 parity、apply/reapply/drift/hash/mode/sidecar、隔离资源清理 |
| R396-09/10 | 全体与 lifecycle owners | 因果区分、runtime 改动依据或无改动说明、真实 gates 与 live merged-main/Issue/Finish disposition |

## 最小可靠验证集
复用 ReadinessAdapterTests 的生产链与 package tests；仅增加能检出 distinct mistake/recovery/content/missing behavior 的 cases。固定文案自我对比或测试计数不证明合格。
用 trellis/skills/guru-team/runtime/resolve-python.sh 的 managed runner；不以 PATH Python 代替。被改非生成 code file <=3000 行，达到阈值前先审查机械拆分。
真实 native CLI 通过现有入口运行；缺 capability/认证/执行证据明确 unverified。fake gh/fixture 结果仅证明测试层，不证明真实业务 production。
未执行 full installer/upgrade/update/Release matrix，业务仓安装/生产部署、gitlink修复或 #250/#292/#521。这些不构成本 Task 的额外验收。
当前已取得基线只有 draft/standalone managed test passed；新最小 authoring、五误用、native、installed 与后续 gates 都待实施。

## 退出与持久化
测试临时资源使用既有 TemporaryDirectory 生命周期；不创建真实用户 Issue/Task/worktree 作为测试输入，不污染业务仓。
示例替换不保留旧误导路径，历史 recorded-result 示例继续明确其完整结果用途。长效合同归 package；fixture/native runtime 只负责执行事实。
无 tracked receipt、授权文件、review history、private linkage helper 给 Agent、第二 fixture happy path或永久 eval cache。验收结果/风险由唯一 Test contribution 最小承接。
