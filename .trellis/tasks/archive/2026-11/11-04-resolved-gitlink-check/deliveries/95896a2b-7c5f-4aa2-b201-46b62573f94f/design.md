# D1 父仓 gitlink 原子内容设计

## 1. 设计目标、需求承接与内容基线

承接本批 PRD DR1—DR4、DS1—DS4 和 DAC1—DAC4。父仓只管理自己的 path/mode/OID；child 内部状态不参与父仓捕获、准入或提交。开发/内容基线 B=b78edbbdc32e77392bc3775366473971050ccb4b，来自原 Delivery 固定 candidate；接续观察 H0=4bf6f551a19b313ee3ac1ccc277388e0c888dc2f，PR 目标 main。B..H 包含原两个待完善提交，没有已交付前序切片。

适用 authority 为 docs/architecture/00-foundation/baseline.md、design-constitution.md 及 06-governance/change-contract.md。原独立 Architecture 已正式返回 candidate_assessment / baseline_current，impact=architecture_impact、path=target_native。本轮fresh candidate_assessment已按修订Issue确认同机制target_native，完成范围仅Guru侧；当前方案消费该判断；它不替代 Wording 后的 final_plan、Approval 或实施质量结果。

## 2. 当前系统、边界与目标差额

Check common.py 普通路径要求 index=HEAD，resolved 路径仍读取 child HEAD/clean/root；全局 unstaged diff 还拒绝 begin_check 正常更新的当前 task.json。shared reviewed_content.py 对 child 和 gitlink deletion/replacement 另有准入。TaskCommit capture_snapshot 读取 child，execute.py 的 git add 又会从 child HEAD 取指针。Review/Reconcile/snapshot 的工作区枚举会将 child 内部变化当成父仓变化。原第二提交的 Reconcile canonical 与 dogfood 不一致。

本轮替代上述同责任规则。既有 committed-tree identity 与 Reconcile index_tree_digest 已能表示原子条目，保留其算法。明确选定 child root 是独立仓库操作；清理、数据保留、hook 隔离和提交发布职责保持原 owner。

## 3. 来源设计处置（唯一）

Issue739 和整体 PRD 是行为要求。原分支与历史 #186/#309/#397 是实现及历史证据，其 child root/HEAD/clean 前置已由本轮需求明确替代，不作为新方案的规范性设计。现行 data-contracts.md 中 Check/Commit 的 child 准入属于受影响旧合同，本轮同步更新。无外部规范性来源设计，故不创建空处置矩阵。

## 4. 模块、职责与设计取舍

共享 Git 事实层在现有 runtime 内提供最小父仓状态投影：worktree 状态忽略 child；cached diff 显式使用 --ignore-submodules=none 保留父 index 变化，再合并为现有 status consumer 所需结果。不能仅把 status 全部改成 --ignore-submodules=all，因为它也隐藏 staged gitlink。路径仍按 NUL 分隔和 literal pathspec 读取；unmerged 由父 index 检出。共享函数以root和精确父仓path集合为输入，返回每个path的head_entry与index_entry（分别为mode/OID或absence）、父index状态及非gitlink的worktree状态/bytes/mode；rename_from保持独立来源路径。head_entry只用于识别旧gitlink类型与删除，不用于约束新OID。index_entry=160000时不读worktree；head为gitlink而index缺失表示父staged删除，即使child目录仍在；index为普通blob的replacement按新普通文件worktree事实处理。删除不得由path.exists或单个合并mode推断。已为 gitlink 的条目不 lstat/scandir 或进入 child，也不递归其目录。

Check 的普通/resolved 捕获都以父 stage-0 gitlink mode/OID为内容；不再要求 index=HEAD。删除取父 index absence，即使 child 目录仍在；replacement 按新父条目类型捕获。其它普通文件保持 worktree bytes/mode 语义。resolved 仍固定 HEAD、唯一 MERGE_HEAD、全部 stage-0 entries/tree 和原 public candidate。

TaskCommit 捕获父 index entry 与必要的父 HEAD 类型，区分 staged deletion 和 replacement。隔离 index 先 read-tree pre_commit_head；普通路径沿原 git add/hook 流程；gitlink 更新/新增用捕获的父 OID update-index --cacheinfo，staged 删除移除隔离条目。rename 的 source 按原精确 stage 集承接。执行前重读父 entry，改变即 stale；不读取 child HEAD 来重新决定指针。原 hook 后精确 tree/commit 检验继续。

Review/Reconcile 和实际 verification/snapshot consumer 复用同一父仓事实边界。先查调用链再删除重复 child 检测；不凭文件名扩大改动。Review-change cached/committed diff 保留父指针，unstaged snapshot 忽略 child 内部状态。已有 upgrade snapshot 过滤仅在实际存在差额时修改。

不排除 gitlink、不新增状态 authority 或双读兼容层。最小共享事实函数用于现有多个真实 consumer，避免各包再次拼凑不同语义；AI 仍负责 scope 和充分性。

## 5. 接口与数据

公共 Skill id、typed exits、Task/Delivery identity 与 resolved projection DTO 不增加字段。Check 原 --skill-input 继续验证真实 profile/key/Planning/candidate 后选择 resolved 上下文，不能只凭 MERGE_HEAD放宽。

Commit private candidate 采用新的 delivery-3.0 语义及匹配 schema，去掉 gitlink_head/gitlink_initialized/gitlink_dirty。现有 index_blob 表示父 index OID，mode=160000 表示原子 gitlink，staged deletion 为父 entry absence；父 HEAD 类型由当前捕获事实明确表示，仅用于区分gitlink staged删除与replacement，不新增公共DTO。旧 private delivery-2.0 的未执行候选明确要求重新 prepare，不转换或双读。若原操作已经生成commit或recovery receipt，先由原Commit owner核真实commit并恢复同一结果，不能重新prepare重复提交；语义未变的result receipt不随candidate升级。同步 schema、builder、validator、executor、真实 snapshot consumer 与包合同；不改公共输出DTO。Check 捕获语义变更也需更新局部算法标识，使旧 checkpoint重新执行原record/check。

上游 castbox/Trellis _candidate_content_ref、verify_candidate、_verify_commit、GitCandidateContent 当前仅接受普通 blob；本仓 adapter 直接消费它们。显式 gitlink 正式 candidate、Check/Review predecessor及Merge/history需要上游支持；本Issue不承担上游改造或正式采用。禁止过滤路径、伪造content_ref、切manual profile或热改生成的 .trellis/scripts。

## 6. 状态、顺序、正常与失败流程

1. 原实现 owner捕获父仓状态及内容。child 未初始化、dirty、检出不同提交或本地没有目标对象时，同一父 index产生同一结果。
2. 当前公开 Task/Delivery已校验后，resolved Check仅豁免精确 task_ref/task.json 的自然 unstaged metadata。其它Task文件及业务未暂存仍拒绝；当前metadata原bytes/index保留。
3. record→check→invoke→projection 使用同一捕获。HEAD/MERGE_HEAD/父index或被审业务内容变化返回原 stale，不把正常index cache刷新当内容变化。
4. 原Reconcile校验integration_paths和精确tree/parents/message并独占提交；同样保留当前Task metadata。后继新HEAD必须进入真实candidate/Check/Review，resolved结果不能充当最终pass。
5. 正式上游候选能力不足时停在相应consumer并明确依赖；本仓独立源码和局部行为验证继续。后继上游改造、工具采用和业务复跑由其原owner承担，不作为本Task完成阶段。

## 7. 恢复、兼容、迁移与集成

本轮直接替代错误的 child准入与重复实现，不保留旧新并行分支。旧未执行private候选/checkpoint重新prepare/record；已执行commit/receipt按第5节由原owner恢复，历史事实不重写。无产品数据迁移。完整source runtime与target publicAPI各自来自匹配安装，单独 source --root target不证明下游兼容。

本仓受管副本经 guru-upgrade-tools完整源合同更新，保留Task/session、用户AGENTS及无关改动。sidecar由原owner逐个处理，不能手拷贝managed副本。上游能力完成后由其原采用owner成套更新；本轮不修改上游。完整矩阵由专门Release owner承担。

## 8. 验证设计

- V1（DAC1/DR3）：真实父子仓resolved fixture保留begin_check自然metadata，正式wrappers执行record/check/invoke/project/Reconcile，独立核tree、parents、message及Taskbytes/index。去掉现有测试额外stage task.json；新HEAD正式candidate/Review的上游能力边界如实报告，受影响后继consumer只补定向回归。
- V2（DAC2/DR1/DR2）：同一父index依次处于未初始化、dirty、其它child HEAD和缺对象，shared/Check/Commit snapshot结果一致；只观察父内容，不依赖child探测。新增、更新、删除（保留child目录）、mode replacement/rename及父index后续变化分别核原子捕获/精确隔离tree/stale。
- V3（DAC3）：普通文件捕获与hook/精确提交回归；业务unstaged、其他Taskmetadata、unmerged仍拒绝。Review/Reconcile及实际verification快照覆盖受影响入口。shared身份所需跨包正式wrappers接受按quality-guidelines既有合同执行；上游相关失败不能mock后声称全链通过。
- V4（DAC4）：受管更新后检查canonical/dogfood/平台字节、mode、sidecar及drift，定向采用组合验证。本轮不要求完整工具采用或业务现场复跑；只有实际触及安装行为才补必要定向安装验证。

测试使用真实Git状态和生产边界，fixture只建立被测边界前置，不替被测producer修输出。已知archive artifact_origin既有失败先归因；不扩大为无关修复。完成必要定向检查后停止重复广扫，不跑完整多平台矩阵。

## 9. Canonical 引用、本轮差额与实际未决项

canonical为 trellis/skills/guru-team/runtime/reviewed_content.py、原Check/TaskCommit/Review/Reconcile及实际verification/upgrade snapshot包；合同包括其schemas、references和trellis/presets/guru-team/spec/workflow/data-contracts.md。Docs Plan由implement第6节单写。Architecture贡献为docs/architecture/contributions/739-parent-git-content.md及739-parent-git-content/proposed下完整领域单元和ADR，目标为03-domains/parent-git-content.md及adr/parent-git-content.md，不改共享导航，说明父仓/child职责、上游API边界与采用退出，原Architecture owner经candidate Check后final_integration晋升/readback。RDT原owner维护完整当前行为/设计/验证差额，不能靠历史追加摘要代替现行定义。

当前没有需求选择缺口。实际实现和验证尚未执行。上游API实现和采用是外部能力边界，不属于本Issue交付。Guru侧源码/合同/受管投影和最小验收完成即可满足本Task；不得声称上游或业务已恢复，也不绕过真实缺口。
