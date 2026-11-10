# 正常续接与出口查询的 Architecture 贡献候选

本贡献属于 Task `resume-step-context` generation 0、Delivery `a2df31bc-2082-48ce-acba-545c8a6adb3b`。状态为 proposed，尚未独立审核或晋升。本次补齐批准实施计划 I3 要求的完整拟写，替代本文件先前的规划摘要；不改需求、方案、Planning 接受结果或共享 CURRENT。

## 固定来源、完整目标与替代范围

固定来源为 Git `26630149070e2988ad08102679931468b3535ef8`。同一 tree 的 `docs/architecture/README.md` 定位 `guru-trellis-architecture`；`docs/architecture/00-foundation/design-constitution.md` 定义 `guru-trellis-design-constitution-v1`；`docs/architecture/06-governance/change-contract.md` 定义本阶段适用的九 concerns、独立候选审核与 final-integration 合同。

唯一共享目标为 `docs/architecture/03-domains/ownership.md`。完整拟写位于同目录 [architecture-ownership-proposed.md](architecture-ownership-proposed.md)，逐一给出 ARCH-DOM-016、ARCH-DOM-019 两个完整表格行及 ARCH-DOM-038 完整段落的 resulting definition。其原文分别由固定来源中的同 identity 定位。晋升仅替换这三个原单元，不向 ownership 追加 Task 登记，也不改变任何其它单元或根入口。

这些单元的必要关系包括该文件原 #419、#443 说明，以及 ARCH-DOM-024/025/043/045/053/060。它们原有的 upstream 身份和公共状态 authority、C4 branch binding、C5 resource ownership、Bind/Selection writer、接收者恢复、阶段门禁和知识晋升职责保留。拟写将新增只读组合明确接入这些职责；不使旧说明失效或把查询变成恢复 writer。公开 I/O 字段与判断条件仍由原 Ensure Interface/Skill、discovery 及 canonical workflow 单写，不在 Architecture 重建 API。

## 原边界、实际差额与直接消费者

原 Ensure 需要 caller 明确组装 TaskId/generation；原 discovery 返回完整 Interface 合同索引。实施在原 package 内新增 current profile，复用 installed public current、原 context resolver 与 Ensure C4/C5/唯一 checkout 校验，输出白名单事实。实际无 key、无绑定和普通错误分别保留，不写 session、selection 或 Git。

discovery 在原入口增加实际 exit 查询，与 installed validation 共用原 marker parser，核 Interface 和唯一 workflow consumer，返回选定 output/input/projection 与原入口定位。动态 selector 保留为原合同；查询既不求值 profile，也不执行下一业务步骤。

直接消费者是原 current-checkout workflow router、原阶段 owner 的 continuation caller，以及取得实际 Skill/exit 后加载 consumer 合同的 caller。上游 start/default get_context 及 managed Python cache 的职责保持。旧显式 Ensure 和无 exit discovery 继续服务原已批准调用边界，不新增 adapter、resolver、Skill 或状态体系。

## 九 concerns 与五原则的本范围承接

| Concern | 适用性与本贡献的处理 |
| --- | --- |
| authority-binding | applicable；上述固定 tree、三个 authority locator、当前 D1 计划和唯一 ownership 目标限定本次改动。 |
| constitution-binding | applicable；采用原公共 current 和 parser 符合成熟扩展面；区分无 key、无绑定及错误保留完整语义；语义 owner、确定性查询和原 writer 分离；只增两项当前查询所需能力；沿 target_native 且不增加第二 authority。五原则正文仍只由 constitution 拥有。 |
| boundary-and-decision | applicable；target_native 在原职责内增加只读组合与定位。没有新的原则性架构取舍，现有 ADR-024、ADR-034、ADR-035 及知识 final-integration 决定继续适用；不新增 ADR。 |
| owner-and-single-writer | applicable；拟写明确 ARCH-DOM-016/019/038 与原 upstream、C4/C5、Bind/Selection、阶段 owner 的关系。查询不取得 writer 或语义 pass 权限；独立 Architecture 审本候选，原 maintenance owner 才晋升。 |
| compatibility-and-exit | applicable；旧显式 Ensure 和无 exit discovery 按原 accepted scope 保留。没有过渡 dual-read、兼容 adapter 或待删除的独立状态；后续改变其支持合同须回原需求/owner。 |
| gap-and-deviation | applicable；本次不关闭既有 GAP，也不迁移其 owner。候选主张无新增偏移，须由独立 before/after 判断，本文不预填通过。 |
| parallel-scope | applicable；当前只写本 D1 贡献和三个拟写单元；禁止提前修改共享 CURRENT、其它 Task、session、资源、源码或已冻结的原生结果。晋升前原 owner 重读目标并整合仍有效条件。 |
| evidence-and-freshness | applicable；实现及工程执行事实分别见原源码、package/runtime、安装与原生首次结果；原生正确性不证明产品缺陷下降。重新构造的完整 candidate 及 before_authority 由原公共入口绑定，本文不计算或复制其 token。 |
| review-and-promotion | applicable；当前 proposed，review 与 promotion 均 pending。实际独立 Architecture 和 candidate Check 之后，由原 final_integration owner 核 expected-current、写入并读回。实施重绑真实 after，再做最终 Architecture/Check。 |

## 验证证据与未验证范围

Ensure 的 managed Python 14 项定向测试实际通过，包含真实 wrapper、有/无 Delivery、无 key/无绑定、普通 stale/ownership/checkout、原诊断、最小投影和查询前后状态。discovery 的原 managed 定向测试覆盖 Skill/workflow/stop、动态 selector、正常声明错误和共享 parser；source gate、当前 Ensure contract graph、caller inventory、新旧安装 smoke 与 drift 分别已有实际结果。这些结果由正式审核 owner 判断当前适用性，不由本贡献替代其质量结论。

外部首次原生结果和限制见 `/Users/devSC/Documents/JobProject/guru-validation-evidence/fizz-filter-controlled-2026-11-10/host/resume-step-context-comparison-result.md` 及其原始 evidence。实验组两个场景均完成，绑定场景调用和墙钟减少、输出读取量未减少；生产会话身份自动提取、产品缺陷率及完整 Release 矩阵未由本次证明。原生测量前后 query 文件及 Task 字节相同；首次错误、预算中断与不利观察保留。

## 最终整合与恢复

拟写审查完成前，shared ownership 保持原文。原 maintenance owner 在合法 `candidate_checked` 后，固定实际目标，核三个完整单元仍与其受审 before 相同，只应用上述三个 reviewed resulting definitions；其它内容原样保留。出现真实并行差额时按原合同协调，并对受影响语义补独立审核。写后完整读取目标和必要关系，核无额外实现或义务变化，再交原 implementation 重绑候选。部分写入或输出丢失沿原同操作恢复，不重复已完成写入，也不新增账本。
