# #383 唯一 Test 结果

本文件承接当前贡献的实际证据；规划与字段齐全不是通过。

| Strategy | 当前执行事实 | 边界 |
| --- | --- | --- |
| T383-01 native 因果行为 | 32 个声明 ID 的最新结果全部通过，既无遗漏也无额外 ID：Check 7、Branch 5、Delivery 3、Completion 11、Delivery refresh 1、Closure 1、second Delivery 1、second Completion 1、Reactivate pending 1、Reactivate refresh 1。实际 native authoring 原样交给 original installed recorder/checker/wrapper。C11 同 scope reapprove_plan 的原投影缺陷修订后重跑通过；Branch 按正式 --expected-exit 重跑通过。 | 期待答案只在 host。保留 7 条历史失败及原始 trace；测试用 production observation 只证明 workflow cognition/transport，不证明业务生产效果。 |
| T383-02 objective runtime | root 8；Planning 23/10 subtests；Check 修订后 29/23；Branch 36/25；Delivery 18/9；Completion 27；Reconcile 44/44。Installer 定向 8 tests/6 subtests，93 deselected。源码/安装 validator、ownership inventory、drift、JSON/shell/Python、task context 与 diff check 已通过。 | 测试次数不替代语义审查。首次 managed pytest 缺依赖、合并 collection 同名冲突均不计 pass；使用临时 uv pytest/jsonschema、各包独立进程，没有修改 managed dependency 环境或无关 machinery。 |
| T383-03 distribution | source 36 packages/109 commands；22 declared platforms 在同一个 installed fixture 实际 apply 与 reapply 均 ok，选中集合与 live inventory 完全相同，installed validation 零 errors，common spec 与 canonical 字节一致。Claude/Codex/Cursor 与 shared dogfood 匹配。初次 60 managed backups 逐个核对并保留在 repo-external /tmp 后 reapply ok。局部修订的 16 sidecars 被后续 canonical reapply 正常退休，非人工保存。当前 dogfood/fixture 无未知 sidecar 或安装冲突。 | 仅使用一个代表性 clean owner fixture；没有 .trellis/.version，故未伪造版本执行官方 update，也不创建第二 clean target。官方源码确认 spec 排除和 custom workflow 保留；不声明实际完整 init/update 或 Release matrix。 |
| T383-04 semantic lifecycle | Planning wording pass，normal/solution 21 candidates classified；独立 Planning Architecture baseline_current；Planning approved；Activation activated。Native transport 使用实际 C20 Completion ResultRef 调用原 Closure，返回 no_mutation；C15 同 gen0 exact merge_result refresh；C21 本地第一次 fast-forward merge 后实际第二 Delivery ready、第二 merge 和同 task/gen0 Completion completed；C16 实际 gen1 pending 与相同 current reactivation anchor 的新证据 refresh completed。 | 所有 transport 都在隔离 fixture；source 为 reference_only，未修改 GitHub。源任务的 Phase2/TaskCommit、独立 committed review、promotion、正式 Delivery/Completion/Closure/Finish 由各 owner 在当前候选边界执行；不以 fixture pass 替代。 |

首次失败的归属与接续：C11 是受支持正常回程的局部 runtime correctness bug，已修订原 projector 并补 original-wrapper regression。Branch 首次调用使用不支持的 --allow-nonpass，改用既有 --expected-exit。Delivery batch 在原 600s 限时内未完成，改为逐例运行，没有提高 timeout；C04 首次缺 task source facts 导致真实 wrapper 拒绝 Refs，保留 native 原结果后补实际 source/Git facts 并 fresh 重跑。C15 首次 600s timeout 的 trace 显示读取完整大型 quality guideline 与历史矩阵；将辅助读取收敛到本阶段适用章节后 fresh 重入通过，不声称已证明唯一 timeout 根因。Native trace 现实时写入日志，partial trace 不因 timeout 丢失；未改 model、effort 或语义答案。

重现 native：用 managed interpreter 运行
trellis/skills/guru-team/packages/guru-review-task-completion/tests/run_native_causal_eval.py
--root <source> --output <repo-external-output>；记录实际 native authoring 与 wrapper stdout，不能预写语义 pass。
完整多平台 Release matrix、candidate 远端安装及任一业务生产效果未验证。
