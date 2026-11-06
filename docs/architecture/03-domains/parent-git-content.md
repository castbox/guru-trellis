# 父仓 Git 内容边界

Identity：guru-parent-git-content。Owner：Guru Git事实runtime及各Skill原语义owner。Status：current。本文拥有父仓Git内容职责边界；源码行为、工具采用与业务效果分别判断。

## 职责

父仓流程以父仓index/tree的path、mode、OID为Git内容事实。mode=160000是一个原子条目，父仓不读取child root、HEAD、clean、初始化、内部文件或对象，不init/update/fetch。child内部变化不改变父仓内容身份，也不单独阻断父仓。用户明确选择child作为独立root时，对该仓执行自己的流程；父仓不由此取得对子仓的操作权限。显式破坏性清理的数据保留和确认边界保持。

父index显式gitlink新增、更新、删除和类型变化进入候选、审查、精确提交及stale检测。cached/committed差异必须保留父指针；忽略child的worktree状态不能隐藏cached父变化。删除由父index absence决定，不能因child目录存在而恢复条目；提交从被审父OID写隔离index，不能用child HEAD替代。普通文件的worktree内容及原hook/exact-commit职责保持。

## 现有owner与合同

共享事实和身份由trellis/skills/guru-team/runtime拥有；Check、TaskCommit、Review、Reconcile及真实verification/snapshot consumer各自消费同一父仓边界。算法、payload及private候选格式由这些canonical包和trellis/presets/guru-team/spec/workflow/data-contracts.md单写，本单元不复制算法。旧child准入及重复实现随直接consumer同步退出，不建立并行authority。

resolved Check仍固定HEAD、唯一MERGE_HEAD、stage0 index/tree。仅公开验证的当前Task task.json自然metadata例外由原Check/Reconcile承接，保留bytes/index；其它Task及业务unstaged、unmerged和过期父内容继续阻断。原Reconcile独占精确tree/parents/message提交，随后新HEAD进入独立正式candidate/Check/Review。

## 上游与采用边界

正式Delivery candidate、commit验证和GitCandidateContent归castbox/Trellis公共API。17015调查时这些接口仅支持regular blob，显式gitlink正式Delivery及新HEAD/history链当时存在上游缺口；这是历史观察，不再是当前上游能力结论。castbox/Trellis #62已由[PR63](https://github.com/castbox/Trellis/pull/63)合并，固定merge为3c37c75897f530c3ae8c5c4d85f6c1f3455b2e5f（head0336f397e1c38194d6d853149e0c1e9db14200cf）。同签名API在candidate capture/verify、local commit验证及GitCandidateContent中采用父index/tree原子条目；gitlink行是[path,57344,OID]，普通文件摘要表示保持。此处仅说明上游公开合同，不复制其实现算法。

当前工作树r4完整匹配采用已由原guru-upgrade-tools owner完成，实际出口tools_upgraded、installed_version=0.7.0-guru.7，固定上游merge3c37c75897f530c3ae8c5c4d85f6c1f3455b2e5f。原输出仍列formal_fork_source_lock为unverified，不宣称该项已验证。采用保持原API与职责边界，不新增Guru内容authority。Guru不得通过过滤路径、伪造content_ref、manual profile或手改生成脚本绕过consumer。原owner依据实际采用结果更新本单元的当前状态；源交付、当前工具采用和业务效果分别判断。

业务仓库工具采用、正式候选现场复跑及业务恢复仍未验证，由其原owner承担，不属于本Task完成条件。不新增验收流水线或完整安装矩阵。历史Guru侧修复证据保留原观察范围；本Issue仍须满足既有Guru侧最小行为验收，源码或投影一致不能单独替代它。

## 来源与证据限制

要求来自Issue739行为要求/边界、resolved-gitlink-check整体PRD R1—R4及本批设计。选择依据见adr/parent-git-content.md。本单元及完整领域决定由739隔离贡献经原Architecture和完整candidate Check审查后，在原final_integration写入并读回；实现owner随后重绑实际after，最终Check/committed Review覆盖真实内容。本文不声明业务root_cause_fixed；RDT原owner维护自己的完整行为/设计/测试定义。

本Issue完成边界按2026-11-05修订Issue739：只交付Guru侧修复及最小验收；上游改造、工具采用、业务复跑非本Task后继阶段或额外完成条件，不以局部测试声明其成功。
