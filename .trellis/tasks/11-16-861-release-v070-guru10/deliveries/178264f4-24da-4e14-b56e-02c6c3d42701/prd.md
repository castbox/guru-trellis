# #861 后继 Delivery：发布消费者与当前清单修复需求

## 1. 整体来源与术语

Task `744a637b-a044-46cd-8cdd-77ddd85ded8e` / generation 1，当前 Delivery `178264f4-24da-4e14-b56e-02c6c3d42701`，planning_root 为本目录。整体 `../../prd.md` 为原 Clarify 已接受的 R1–R11/AC1–AC9；本批选中 R5、R8–R11、AC6–AC9。当前切片实现 source/consumer 修复；R11 的真实采用与 AC7 完整 existing 是第3节明确分配的后继责任。

| 来源及条款 | 角色 | 本批用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/861：执行范围、失败返回原owner及验收 | 要求 | 必要发布准备修复，无其他Issue状态依赖 |
| `.agents/skills/release-guru-trellis-version/references/contract.md`：Stage 1、Complete Source Before Actual Adoption、Stage 2 | 约定设计 | 完整source先交付，真实采用独立后继，正式发布仍在Task外 |
| `.trellis/spec/preset/installer.md`：AGENTS受管块、Codex shared discovery、Platform Overlay Selection | 约定设计 | 合法文本变换、用户块外保留、每root平台集合 |
| `.trellis/spec/workflow/data-contracts.md#public-skill-io-current-fields` | 约定设计 | current input/output清单精确来源；instruction-only不贡献JSON I/O |
| `trellis/presets/guru-team/MIGRATION-812.md`、`MIGRATION-813.md`、`MIGRATION-819.md`；Create Task、Root Cause、Sync Base当前Interface及原schema | 兼容约束及事实 | 当前selector与历史schema/固定provider恢复分离 |
| `docs/{requirements,design,test}/current/codex-skill-distribution.md`：R724-02/D724-01/03/T724-01/04；同层 `native-compatibility.md`：R630-04/05/D630-04/T630-05/07 | 当前知识 | 平台边界、正常文本维护及分层验证 |

current清单指canonical manifest向安装者声明的当前可调用结构化输入集合；磁盘上仍保留的历史schema不自动属于current支持。native检查是projection parity，不是实际客户端Agent行为。原正文是同cell首次preset前与Core template hash相符的AGENTS bytes。

## 2. 整体与本批目标、非目标

本批同批修复Wording退役消费者、AGENTS合法受管替换验证、native平台预期集合，以及原真实manifest验收发现的11项旧独立input登记差额。source修复必须独立可验证，不能依赖准备checkout已采用尚未交付的新源。

不恢复Wording，不改生产renderer、平台能力或registry，不修改历史schema/runtime selector/public Skill I/O，不升级Fork/CLI/source lock，不改template hash或弱化exact比较，不转换历史Task，不修改self-reapply guard。不实施其他开放Issue，不执行tag/smoke/Release、主目录tools安装、Issue closure或Cleanup；不扩张累计完整矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

gen0源准备、实际采用、终态簿记已分别经PR #865/#866/#867合main。固定B为 `b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec`；保其历史身份，不重复交付。同一固定B下保留已有三项修复增量，纳入本批完整内容及后继审核。

原受影响回归和manifest真实安装入口证实current input清单多11项、缺0项，typed outputs无差额。11项属Create Task旧2项、Root Cause旧aggregate与七类Delivery profile共8项、Sync Base旧current输入1项。Create Task与Root Cause旧schema仍留作历史验证/原provider恢复；当前Interface已改用新版输入。Sync当前Interface为scalar CLI，其call-local 3.0仍引用2.0原普通/资格确认分支：退出旧独立登记不取消该当前消费者，也不删除被引用schema。

本批从source-only调整为可分发source修复。**当前Delivery先独立交付完整canonical manifest、直接consumer/test与兼容说明。** 真实准备checkout采用依赖本批实际delivered的完整干净source；原Completion随后返回 `additional_delivery_required`，原Creation才分配同Task后继采用Delivery。不得提前创建、选择空Delivery或用未交付commit、手改installed/自引用provenance代替source_locked。

完整 `.9→.10` existing 原入口使用本批干净交付源，在后继采用及Whole Completion前完成；未执行的采用是业务工作，不是仅待证据。所有采用和existing满足后才Completion/no_mutation Closure/Finish，#861保持OPEN。Stage2再从届时最新main重冻结候选并负责发布与主目录收敛。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、条件与触发 | 行为及观察 |
| --- | --- | --- |
| S1 | 当前installer tests正常安装已退役Wording源 | 真实产物/manifest无旧资产，当前剩余合同成立 |
| S2 | existing验证器首次preset前，目标AGENTS含旧受管块且hash匹配 | 原renderer精确after被接受，块外bytes及原hash保持 |
| S3 | clean init及同候选update/reapply | 合法追加/幂等通过，未知正文变化仍失败 |
| S4 | native exact Claude/Cursor选择，registry含shared和Codex-only | 各root仅要求适用集合，真实missing/额外投影仍失败 |
| S5 | Codex原共享根 | Codex-only仍必需，旧 `.codex/skills/guru-*` 不恢复 |
| S6 | installer正常传播canonical manifest，Interface含JSON及instruction-only | current JSON input/output精确相等；历史文件保留但不宣告current支持 |
| S7 | 本批实际delivered，准备checkout仍为先前安装 | 原Completion/Creation建立并规划后继真实采用，全部责任完成后才整体收尾 |

## 5. 完整行为、条件与约束

- **D-R1 → R8/S1**：完整迁移Wording wrappers/artifact/commands/schema必选断言及仍调用退役helper的测试。检查真实安装结果，保用户修改保护；不恢复生产旧路径。
- **D-R2 → R9/S2–S3**：同cell首次preset前捕获并核hash绑定的实际preimage，沿原调用链由原renderer精确比对整个after；删除suffix猜测及AGENTS source-equality放行。只用调用期bytes，不新增持久状态或改hash。
- **D-R3 → R10/S4–S5**：按root descriptor selected flags与supported_platforms求expected，计数和后继catalog保持一致。保持missing/unexpected/private-test检查，不按包名建立排除表。
- **D-R4 → R5**：以直接回归、必要安装/平台/ownership/drift及完整bytes/mode/sidecar观察支持本source切片。采用仍适用的三平台focused事实；manifest改变后必须补实际after的安装与current inventory消费者验证，不声称旧b85证据覆盖新分发。
- **D-R5 → R11/S6**：核清11项真实生产者/消费者，只退出不再由当前Interface选择的独立input登记；保历史schema、Sync3.0仍引用的2.0分支及完整旧provider恢复。原manifest测试保exact集合，合法识别无JSON schema的instruction-only输出；可变schema版本从当前Interface/schema取得，不冻结旧常量。以明确兼容说明解释current、pending及old-operation边界，不新增旧输入双读或公共字段。
- **D-R6 → R11/S7**：本批source交付不省略后继真实source_locked采用；将未实施采用和完整existing分别保留到原Completion/后继owner，不在当前切片冒充完成。

来源设计唯一处置在 `design.md` 第3节。规划不预填实现或通过结果。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应 | 入口及预期观察 |
| --- | --- | --- |
| D-AC1 | D-R1/S1 | 原两installer tests及必要消费者：真实安装无退役资产，当前manifest合同成立 |
| D-AC2 | D-R2/S2 | 旧块替换真实hash gate回归，独立观察精确after、块外prefix/suffix、原hash不变；完整existing为后继Whole Task责任 |
| D-AC3 | D-R2/S3 | clean append、reapply及未知正常编辑回归保持作用，source相等不能单独放行 |
| D-AC4 | D-R3/S4–S5 | mixed registry真实native回归，三平台每root计算及真实missing/额外投影 |
| D-AC5 | D-R4 | 有效source/installed/ownership/drift、受影响target完整受管bytes/mode/lock/workflow/sidecar；不泛化Agent或最终Release通过 |
| D-AC6 | D-R5/S6 | 同一真实manifest安装入口的current JSON input/output exact比较通过；11项不再被当前Interface独立选择后才退出登记；保历史schema、Sync3.0对2.0的引用及原selector字节不变；能力projection读取新清单 |
| D-AC7 | D-R6/S7 | 原current切片独立source交付与后继采用顺序明确；本批delivered不等于whole Completion |

其余历史固定计数、文本布局或全Git历史断言的原失败保留。它们未因模块红而纳入本批，不放宽其断言、不将范围外历史断言失败改称通过；若出现影响本批可交付的真实supported consumer缺口，回原资格/范围owner判断。

## 7. Canonical 引用与本轮差额

RDT稳定入口为 `docs/{requirements,design,test}/README.md`，原R724/R630单元承接三项消费者；data-contracts current清单合同与MIGRATION-812承接新增差额。原RDT owner判断必要现行知识维护，实施前更新实际context，整合/readback后提交并独立审核。兼容迁移公开说明属于本批source，不将其误作新的runtime协议。

Architecture为 `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md`。分发边界已改变，原source-only no-impact/Approval不再覆盖新计划；本批重新取得独立candidate_assessment、final_plan及Approval，取得完整当前计划及原接受边界后，才进入新增范围实施。
