# 父仓 gitlink 原子内容与自然 resolved 流程需求

## 1. 来源与术语

TaskId=resolved-gitlink-check，generation=0，保留原no_issue身份及已有Delivery。当前选定要求来自https://github.com/castbox/guru-trellis/issues/739 的行为要求、最小验收、上游依赖与交付边界（2026-11-05修订），不重建Direct Source。用户要求以main为基线，在已有工作树/分支完成该Issue。

gitlink是父仓mode=160000的path/mode/OID条目；child内部状态不属于父仓内容。resolved指HEAD未移动、唯一MERGE_HEAD存在且index冲突已解决的候选。历史#186/#309/#397及原两个提交仅为问题证据，不提供当前完成结论。

## 2. 背景与问题

Check的gitlink_entries将合法stage0指针与旧HEAD差异拒为stale；原补丁后resolved_content_identity仍拒绝begin_check正常写入的当前task.json。fixture额外stage元数据掩盖该缺陷。shared identity和Commit仍检查child HEAD/root/clean，隔离index的git add可重新从child取pointer；部分Reconcile canonical尚未完整同步受管副本。

## 3. 目标与非目标

交付Guru侧统一父仓原子内容、自然resolved修复及必要合同/受管投影。父仓不进入child，显式父index变化保持可审查、精确提交和stale检测。只收敛真实同责任consumer，不扩展无关Git工具或未用代码。

不含castbox/Trellis上游API改造、业务仓库升级采用/现场复跑/发布、完整安装升级Release矩阵、恶意输入、并发压力、额外锁或crash加固、业务代码或child修复。不承诺消除未来所有Git缺陷。显式破坏性清理边界保持。

## 4. 真实调用方、场景与流程

S1：原Check/Reconcile owner处理正常resolved merge；保留自然begin_check metadata，经record/check/invoke/projection/Reconcile核精确提交，不额外stage task.json。
S2：父仓准备显式gitlink新增/更新/删除/类型变化；捕获父index并精确提交。删除时child目录仍在也按父index absence处理；父条目后续改变仍stale。
S3：同父index下child未初始化、dirty、不同HEAD或无目标对象，父仓身份及结果不变，不递归、不获取child。
S4：用户明确选择child为独立root时执行它自己的流程；父仓不自动取得child操作权限。

## 5. 行为要求

R1（S1/S2）：gitlink以父index/tree path/mode/OID原子处理，显式新增/更新/删除/类型变化进入捕获、差异、审查与精确提交。提交使用被审父OID，不重采child HEAD，不排除路径。父条目变化继续stale。
R2（S2/S3/S4）：Check/Commit/Review/Reconcile、共享身份和真实验证/工具快照consumer不读取child root/HEAD/clean/初始化/内部文件或对象，不init/update/fetch。保留普通文件、父unmerged和业务unstaged的原正确行为，删除同责任重复child准入。
R3（S1）：resolved保持唯一MERGE_HEAD、stage0 tree和原Reconcile精确parents/message。仅公开校验的当前task_ref/task.json具有自然metadata例外，保留bytes/index；不豁免其它Task或业务修改，不用额外stage掩盖producer缺陷。
R4：canonical、dogfood、声明平台、schema和合同一致，沿原受管owner更新。旧未执行private候选重新准备；已有commit/receipt由原owner恢复，防止重复提交。不热改业务安装或上游生成脚本。

## 6. 约束与依赖

上游Delivery candidate/commit验证/GitCandidateContent当前regular-only，显式gitlink正式Delivery/新HEAD链需要上游配套；由castbox/Trellis owner承担。本Task不绕过、不伪造另一authority，报告实际阻断及其能力边界；不把上游改造或业务恢复增加为本Issue验收。局部机制通过不代表完整链路已恢复。

复用原Task/Delivery、原Git事实owner和受管升级入口。无产品数据迁移。必要RDT/Architecture差额由原owner完整拟写并在candidate Check后晋升，不能只追加历史摘要替代当前定义。

## 7. 可观察验收与验证方式

AC1（R1/R3）：一个真实Git resolved fixture通过生产wrappers执行record→check→invoke→projection→Reconcile，保留begin_check自然metadata，独立核tree/parents/message及Taskbytes/index。后继consumer仅补受影响定向回归，不重复完整流程。
AC2（R1/R2）：代表性真实Git用例证明child状态不影响父身份，父指针被捕获/精确提交；新增/删除/类型变化和父index后续变化有能暴露遗漏的回归。按逻辑分支取用例，不做child状态×Skill×平台矩阵。
AC3（R1—R4）：通过直接受影响runtime/package回归和canonical/dogfood/声明平台一致性检查；复用仍适用测试，不新增重复验收、独立证明artifact或审批。AC4沿用为本验收的受管投影/工具来源一致性定位，不再承担业务采用或现场复跑。

## 8. 实际未决项

没有待用户决定的需求问题。上游缺口如第6节，是外部能力边界，不冻结本仓独立修复，也不声称已解决。Issue/Task完成仅表示Guru侧交付和上述最小验收完成，不表示业务已恢复。实现和验证尚未执行。
