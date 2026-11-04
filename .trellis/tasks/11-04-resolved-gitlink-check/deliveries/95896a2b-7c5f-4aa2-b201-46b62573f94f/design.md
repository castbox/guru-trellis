# D1 resolved gitlink Check 设计

## 1. 设计目标、需求承接与内容基线

承接本批PRD DR1—DR4、DS1—DS3与DAC1—DAC4。开发基线与固定内容B均为main `b78edbbdc32e77392bc3775366473971050ccb4b`，来源为本Task正式Sync/CreateTask审定基线；Planning H0等于B，PR目标为main。实际实施H由后续原candidate owner绑定，不把H0当最终提交。

独立Architecture已实际返回 `baseline_current`、`candidate_assessment`、`no_architecture_impact`。适用baseline为`guru-trellis-architecture`，constitution为`guru-trellis-design-constitution-v1`，change contract为`guru-trellis-architecture-change-contract-v1`。修复在既有Check/Reconcile职责内，不新增Architecture contribution或ADR；最终方案仍进入Wording→独立final_plan→Approval。

## 2. 当前系统、边界与目标差额

无前序Delivery。当前`common.py`的普通`gitlink_entries`要求stage-0与HEADtree一致；record/check捕获完整业务file_set，delivery invoke再核该身份，project把实际resolved结论投影给Reconcile。正常合并中HEAD未动而stage-0指针已更新，因此第一处capture就拒绝合法候选。

本批只为原专用resolved profile增加显式capture上下文，让stage-0成为这一路径的gitlink目标。普通算法、普通token、private schema6.0、公共输出DTO、Task/Delivery身份和原Reconcile精确提交职责保持。拒绝以typed_exit或发现MERGE_HEAD自动开启此语义。

## 3. 来源设计处置（唯一）

当前no_issue请求给出行为与兼容约束，没有规范性来源设计。整体PRD第1节所列历史仅用于保留真实child身份、普通绑定和exact Reconcile职责；本节不创建空处置矩阵。以下方案是本Author选择并接受独立candidate评估后的实施方案。

## 4. 模块、职责与设计取舍

- Check `record.py`、`check.py`读取可选`--skill-input`，加载已有公共输入。先核mode、Task、Delivery、当前Planning result与candidate，再判profile。只有`delivery_resolved_reconciliation`选择resolvedcapture；不提供参数的普通调用行为保持。
- `common.py`集中capture选择与Git内容事实。resolvedcapture绑定live HEAD、唯一MERGE_HEAD、完整stage-0条目的mode/OID语义、stage-0tree和完整业务file_set。条目从`git ls-files --stage -z`读取，不哈希raw index字节，避免正常Git index缓存刷新导致假变化。
- resolved gitlink按index OID绑定。复用child校验职责但区分父仓合法staged更新与child自身dirty：要求child是精确root、内部clean、HEAD匹配stage-0目标。无初始化child继续遵循现有已支持语义，不新增初始化或写入权限。
- `delivery.py`、`project.py`使用同一resolvedcapture规则核当前owner结果；普通candidate/finalCheck继续普通capture。若存在现成纯事实helper，可在原职责层提取复用，不复制一份与Reconcile竞争的规则。
- 原Reconcile继续验证resolved tree、integration_paths、HEAD/MERGE_HEAD和精确parents/message，独占提交。Check不commit、不修改公共candidate，不伪造新HEAD结果。

直接修改原capture比先commit、排除gitlink或放宽所有HEAD校验更贴近首个偏离。无需新开关、持久字段、第二ledger或兼容状态机。可选参数有当前record/check两个真实consumer；不是未来预留。

## 5. 接口与数据

`record-phase2-check`与`check-phase2-check`的commands和合同新增可选`--skill-input`，输入为原公共Check输入JSON。该参数不改变11字段semantic authoring结构；采用file或现有单次stdin规则，不能与另一stdin locator争用。给出的Task/mode/Delivery/Planning/candidate不匹配时返回原schema/stale诊断，不能只凭profile字符串放宽。

resolvedcapture生成独立的局部内容token，仍占原`reviewed_content_sha256`，只服务同owner相邻一致性，不作授权或跨阶段authority。完整stage0与file_set变化须改变token。普通token逐字保持现有算法，private6.0与publicDTO不加字段。

原invoke从其真实public_input取得profile，project从相同public输入和实际checked结果生成原resolved-candidate1.0。target原Reconcile继续消费该原格式，不从source加载替代target公共API。

## 6. 状态、顺序、正常与失败流程

1. 调用方正常merge并解决冲突；HEAD仍为原提交，唯一MERGE_HEAD为选定目标，index全为stage0。存在未解决项、其他sequencer、未暂存或untracked业务内容时保留原拒绝语义。
2. 原Check owner完成完整语义审查，record携原skill输入捕获resolved内容；checker以同输入重读全部当前事实并核token。
3. invoke与project按同resolved语义验证；正常Git刷新index缓存不改变语义身份。HEAD、MERGE_HEAD、stage0条目、业务内容或child状态改变则拒绝过期结果并回原owner重审。
4. project输出进入原Reconcile，后者独占exact commit。此时resolved token不被解释为提交后Check pass。
5. 实施owner绑定实际新HEAD candidate，原普通Check/fullReview重新审查。

## 7. 恢复、兼容、迁移与集成

没有新持久模型或数据迁移。旧普通record/check调用不携`--skill-input`时语义保持；新增参数只为当前专用入口提供上下文。旧owner checkpoint不转换成resolved pass，候选变化重新走原record/check。

工具调用路线使用clean且完整matching reviewed canonical source的原wrapper `--root target`，runtime来自完整source，公共Task/Delivery API仍从target安装读取。target原Reconcile包及resolved-candidate1.0格式保持，必须通过实际组合验证。先前dry-run到达原gitlink拒绝只证明入口加载，不能证明修复或下游可消费。若source和target API/consumer出现不兼容，停止该组合并回原安装owner；禁止手工copy、混合安装或扩大业务PR纳入无关工具资产。

canonical变更通过原工具升级/受管同步owner更新本工具仓dogfood，保留Task/session和并行修改。普通apply被旧Task阻断时不得手动覆盖managed副本。

## 8. 验证设计

- V1（DR1、DAC1）：真实正常Git merge fixture保留旧HEAD、新stage0 gitlink和cleanchild，使用正式wrapper实参执行record→check→invoke→project→原Reconcile；核tree、parents、message。单函数mock不替代此链。
- V2（DR2、DAC2）：同样本走普通入口仍拒绝；正常child dirty、child HEAD不匹配、unmerged和capture后候选变化各覆盖独立诊断。非恶意输入或并发压力。
- V3（DR1—DR3、DAC3）：无gitlink和原普通gitlink算法回归，正常index缓存刷新不制造失效；新增wrapper参数实际到达runtime。已验证且依赖未变的原测试事实可复用，新增/受影响分支补验证。
- V4（DR4、DAC4）：完整canonical source与target安装API/旧Reconcile schema、实际消费组合验证；canonical/dogfood和受管投影一致。工具source交付后由原业务owner在原真实候选复跑，不用fixture声称原业务恢复。

## 9. Canonical 引用、本轮差额与实际未决项

Check canonical package的`SKILL.md`、`references/contract.md`与`commands.json`维护新增参数、明确resolvedcapture边界及原consumer；必要当前RDT差额由原RDT维护owner处理，历史文档保持原观察。Architecture authority入口、constitution和change-contract按第1节读取，本轮无架构边界变化，不写shared导航或空贡献。

不存在待用户决定的方案问题。实际实现、兼容组合和真实候选复跑尚未执行；若测试暴露新的scope/机制变化，返回最早受影响owner，不用当前Planning覆盖新事实。
