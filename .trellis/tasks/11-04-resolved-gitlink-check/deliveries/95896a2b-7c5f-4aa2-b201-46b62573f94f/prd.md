# D1 父仓 gitlink 原子内容与自然 resolved 修复

## 1. 整体来源与术语

承接根PRD accepted_scope R1—R4/AC1—AC4；来源为Issue739的行为要求、最小验收和交付边界（2026-11-05修订）。gitlink是父仓path/mode=160000/OID，不等于child检出内容。保留原no_issue Task身份与当前Delivery UUID。

## 2. 整体与本批目标、非目标

本批交付完整Guru侧修复：共享父仓事实、Check/Commit/Review/Reconcile及真实verification/snapshot consumer统一忽略child内部状态，同时保留父index变化、精确提交和stale。修复自然begin_check metadata及受管副本差异。不含上游API改造、业务采用/现场复跑、发布或完整安装Release矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

固定内容/开发基线B=b78edbbdc32e77392bc3775366473971050ccb4b，来自原Delivery；原两个待完善提交的接续H0=4bf6f551a19b313ee3ac1ccc277388e0c888dc2f，无已交付前序Delivery。当前PR目标main，观察main=8989f38b481f7a48caeb210ee7753bdbe29577a6；内容B与整合目标分开处理，不重置分支。

上游castbox/Trellis candidate/commit验证/GitCandidateContent目前regular-only，显式gitlink正式Delivery及新HEAD链需要其配套。本批不修改上游、不排除路径或伪造content_ref；如实报告实际阻断，局部测试不声称全链恢复。上游改造、业务采用及恢复由原owner承担，不再是本Task额外完成阶段。本批Policy=full，完整范围是Guru侧交付。

## 4. 本批调用方、场景与流程

DS1：相同父index下child未初始化、dirty、不同HEAD或无目标对象，不影响父仓身份/准入，不进入child。
DS2：父index显式gitlink新增/更新/删除/类型变化进入捕获及精确提交；child目录仍在的staged删除按父absence处理，后续父条目变化仍stale。
DS3：正常resolved merge保留旧HEAD、唯一MERGE_HEAD和stage0；自然begin_check metadata经record/check/invoke/project/Reconcile保留bytes/index，精确tree/parents/message。
DS4：真实业务unstaged、其它Task metadata和unmerged不获得当前Task例外；明确选择child root则独立执行，破坏性清理边界保持。

## 5. 完整行为、条件与约束

DR1（R1）：所有真实父仓内容consumer以index/tree path/mode/OID捕获gitlink，不重采child HEAD；新增/删除/类型变化与父条目stale均保留。
DR2（R2）：删除child root/HEAD/clean/初始化准入及同责任重复实现，保留普通文件事实与正确原门禁；不扫描无关Git工具。
DR3（R3）：resolved绑定真实merge/index及原Reconcile精确提交；只豁免公开校验当前task_ref/task.json自然metadata，保留原bytes/index，fixture不额外stage修补输出。
DR4（R4）：canonical、schema/合同、dogfood和声明平台经原受管owner同步；旧未执行private重新prepare，已执行commit/receipt先恢复，防止重复提交。不热改target或上游生成文件。

## 6. 本批验收、验证方式与未决项

DAC1：一个真实Git fixture经生产wrappers完成resolved record/check/invoke/project/Reconcile，核tree/parents/message和自然metadata；后继consumer仅补命中定向回归。
DAC2：代表性真实Git用例核child无关性、父新增/更新/删除/类型变化及父index drift；不做child状态×Skill×平台矩阵。
DAC3/DAC4：直接受影响runtime/package回归与canonical/dogfood/平台一致性。复用现有有效测试，不新建验收artifact、审批或流水线。只有实际安装行为变化才加定向安装检查。

没有需求选择缺口；上游能力按第3节报告，不将业务恢复或全安装采用写成通过或本Issue门槛。

## 7. Canonical 引用与本轮差额

canonical为shared reviewed_content/Git事实、原Check/TaskCommit/Review/Reconcile及实际verification/snapshot包，data-contracts及这些包的合同/schema同步替代旧child准入。当前为target_native行为演进，原Architecture owner审核真实隔离贡献；RDT/Architecture由原owner经candidate Check后final_integration晋升/readback。历史正文保留原观察。
