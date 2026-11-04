# D1 resolved gitlink Check 实施与验证

## 1. 输入与引用

读取整体`prd.md`第4—7节、本批`prd.md` DR1—DR4和DAC1—DAC4、`design.md`第3节来源设计判断及第4—8节方案。当前起点B/H0为main b78edbbdc32e77392bc3775366473971050ccb4b，无前序Delivery。

实施前加载Check canonical `runtime/{common,record,check,delivery,project}.py`、commands与合同，及Reconcile `runtime/{resolved,execute}.py`的精确tree/parents/message职责。原Architecture candidate实际no-impact结论确认此方案保持既有职责；该结论不代表实施已通过。

## 2. 有依赖顺序的步骤与文件责任

1. I1：Check实施者在canonical `common.py`建立显式resolvedcapture与共享纯事实逻辑，固定HEAD/MERGE_HEAD/stage0和完整业务file_set，保留普通算法与childroot/clean/OID。
2. I2：同实施者更新`record.py`、`check.py`与`commands.json`的可选`--skill-input`；按真实public身份绑定上下文。`delivery.py`、`project.py`消费同语义，保留publicDTO/private6.0和原Reconcile职责。
3. I3：canonical包tests增加正常Git fixture与正式wrapper整链，覆盖V1—V3；证明普通行为及候选变化诊断没有放宽。若纯事实helper提取触及Reconcile，补直接consumer适用验证。
4. I4：原文档owner落实第6节Docs Plan；原工具升级owner以合法受管入口同步dogfood，保留现有Task/session，执行定向drift/投影验证。禁止手改managed副本。
5. I5：原Check owner对完整工具候选检查，独立reviewer审完整提交范围，经原pull_request交付main。原业务Check/Reconcile owner使用clean完整工具source执行V4真实候选；新HEAD进入原普通Check/fullReview。整体完成由原Completion核全部责任。

## 3. 验证入口、输入与预期观察

使用本工具仓managed Python与matching Fork；从canonical package tests运行：`python -m unittest discover -s trellis/skills/guru-team/packages/guru-check-task/tests -p 'test_*.py'`。其中新增V1必须真实调用`record-phase2-check.sh`、`check-phase2-check.sh`、`invoke.sh`、`project-resolved-reconciliation.sh`及原Reconcile入口，不能仅比较fixture常量。

- V1：合法stage0新gitlink且cleanchild→专用整链完成→exact提交符合预期；绑定DAC1。
- V2：普通入口、正常childdirty/HEAD不匹配、unmerged与capture后drift→明确拒绝；绑定DAC2。
- V3：无gitlink、普通gitlink、正常index缓存刷新和wrapper实参→原普通token稳定、resolved语义稳定或如实失效；绑定DAC3。
- V4：clean完整source原wrapper `--root target`→target既有publicAPI→target原Reconcile消费组合通过；再由原业务owner执行真实候选并记录实际结果，绑定DAC4。dry-run和fixture只支持各自层次，不证明业务复跑。

同步后运行原`check-dogfood-overlay-drift.sh`及受影响package/声明平台定向检查；不执行无要求的完整Release矩阵。测试失败先界定本候选因果，不将无关失败擅自纳入修复。

## 4. 停止条件与适用回退点

新scope/公共格式/owner变化回Author与Architecture；需求变化回Clarify。候选变化回原Check重审。source/target公共API或旧consumer不兼容时停止V4组合，回原安装owner，不热补业务runtime。受管同步冲突由原升级owner处理，不恢复他人内容。

本批无产品数据迁移或release/tag副作用，故不新增数据回滚协议。任何Git副作用只处理本Task精确路径，提交前按会话变更安全合同隔离；其他Task和并行改动保留。

## 5. Delivery Policy（唯一）

policy=full。D1覆盖整体R1—R4和AC1—AC4，没有延期到新Delivery的代码责任。工具源码、合同、定向测试和支持入口组合验证经原质量/交付流程完成；source合并后原调用方真实候选复跑仍为整体Completion的必需事实，不能由Delivery merge代替。复跑由原业务Check/Reconcile owner执行，不创建另一工具identity掩盖未完成责任。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。实际差额是原Check专用resolvedcapture及两条命令可选参数；由原RDT维护owner评估并准备必要的完整当前定义差额，直接consumer为Check调用者、Reconcile和后续实现/检查者。canonical `guru-check-task/SKILL.md`、`references/contract.md`、`commands.json`及必要例子按原包职责同步；普通调用、private6.0/publicDTO和exact Reconcile边界写清。

涉及现有RDT current单元时，在本Task隔离贡献中准备完整拟写，由原RDT owner在完整candidate Check后final_integration整合并读回；再由implementation重新绑定全部after，完成最终Check/commit/独立Review。没有实际RDT差额时原owner返回no-change，不造空贡献。Architecture已判断no-impact，不建贡献/ADR或修改共享入口。受管dogfood只经原升级/同步owner写入，canonical/dogfood/目标实际执行的证据分别陈述。历史事实不改成当前通过。
