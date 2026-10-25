# 部分与后续 Delivery 的完整正文（教学替代安排）

这是与本目录 full D1 互斥的合成教学安排。P1/P2 不是实际 Delivery 标识；下面的前序快照也不是实际 delivered 结果或测试证据。实际流程须用原 Creation/Delivery producer 的真实身份和结果，不能把这些段落写入公共状态作为验收。本文件演示两批各自三正文如何完整成文；整体需求仍是 [task-prd.md](task-prd.md)，来源仍是 [source.md](source.md)。

# P1 Delivery PRD：先交纯引擎

## 1. 整体来源与术语

整体范围为 Task PRD 的 R1–R4/AC1–AC5；本批读取 source §1–4，要求、约定设计、建议和历史角色保持。引擎是 validate_manifest，adapter 是后续 CLI。

## 2. 整体与本批目标、非目标

整体交付可供 CI 使用的 check 命令。本批独立提供可调用、可测试的纯引擎，覆盖 R1/R2 及 R4 的纯计算/标准库约束。排除 CLI 命令、JSON 标准流和 exit 映射；整体非目标仍是缓存、网络、修复、内容检查、写报告、文本输出。

## 3. 本批起点、前序结果、依赖与剩余责任

首次交付，无前序；source §2 只有 version。P1 依赖标准库和现有 unittest。P2 仍承担 R3、R1 的 CLI 读取、R4 的入口只读/保留 version，以及所有 CLI 集成验收。P1 的 CheckResult/ManifestError 是 P2 的输入；P1 合并不能触发整体 Completion。

## 4. 本批调用方、场景与流程

| 场景 | 调用方/前置 | 触发 | 行为 | 可观察结果 |
| --- | --- | --- | --- | --- |
| P1-S1 | 未来 CLI adapter/单测，合法文档 | 调引擎 | 校验完整文档再按序检查 | CheckResult 有序，空文档 ok=true。 |
| P1-S2 | 单测，混合启用/禁用/缺失 | 调引擎 | 禁用不访问，缺失后继续 | skipped/missing_file 和后项结果都保留。 |
| P1-S3 | 单测，坏字段或重复 id | 调引擎 | 停止于结构阶段 | ManifestError，零 is_file 调用。 |

## 5. 完整行为、条件与约束

R1 的文档部分：version 必须为整数值1、entries 数组，每项非空字符串 id/path、布尔 enabled，id 唯一。path 相对传入 base_dir，完整验证失败不访问文件。R2：合法输入按序；禁用项直接 skipped，启用普通文件 ok，缺失/目录 missing_file 且继续；空列表合法。引擎返回 version/results/ok，results 每项 id/status；没有 missing_file 时 ok=true。引擎不打印、退出或写盘，使用标准库和注入 is_file；CLI 输出仍留给 P2。来源设计处置仅见本批 design 第3节。

## 6. 本批验收、验证方式与未决项

P1-AC1 对应整体 AC1：引擎合法/空/相对路径得到正确结果。P1-AC2 对应 AC2/AC3：记录 is_file，禁用不调用、缺失后继续、顺序不变。P1-AC3 对应 AC4 的引擎部分：先合法后坏项/重复 id 得 ManifestError 且零调用。P1-AC4 对应 AC5 的引擎部分：捕获标准流为空，输入对象和文件不修改。入口为 test_checker 的实际模块测试；CLI 验收明确未覆盖。教学产品输入无未决项，实际前提不符时回原 owner。

## 7. Canonical 引用与本轮差额

读 source §3.1–3.4：新增纯引擎及模块测试；CLI 和整体命令验收未交付。原 RDT/Architecture owners 承接真实差额，不由模板写共享导航。

# P1 Delivery design：纯引擎

## 1. 设计目标、需求承接与内容基线

承接上述 P1 PRD。B 为 source §2 的教学快照，实际项目另经原 content_base 取得真实 B/来源、H0 和 PR 目标。Architecture 沿 source §3.4 纯计算边界；本例无实际候选评估结论。

## 2. 当前系统、边界与目标差额

没有前序，无 checker；新增 checker.py，不修改 cli.py 的 version 或增加 check。目标向 P2 提供稳定纯函数结果和格式异常。

## 3. 来源设计处置（唯一）

| 来源/承诺 | 处置 | 落点 | 理由 | 影响 | 上游处置 |
| --- | --- | --- | --- | --- | --- |
| source §1 D-A 纯 validate_manifest/CheckResult/ManifestError | retain | §4/5 引擎接口 | 本批独立能力。 | 新增纯模块。 | 无偏离。 |
| source §1 D-A adapter 负责输出/exit | retain | §2 排除、§7 对 P2 的边界 | 不能在引擎混入标准流。 | P2 负责集成。 | 分批承接而非取消。 |
| source §1 D-B 完整校验先行、禁用先分支、缺失普通结果/标准库 | retain | §5/6 | 保持输入和顺序语义。 | 两阶段纯计算。 | 无偏离。 |

## 4. 模块、职责与设计取舍

checker.py 校验输入并构建结果；test_checker.py 调实际引擎。分离输入验证与文件存在判断，不选边读边检查。is_file 注入有当前不访问验收 consumer，不引入插件或异步框架。

## 5. 接口与数据

函数 `validate_manifest(document, base_dir, is_file)` 返回 CheckResult 或抛 ManifestError。先检查 document/object、version整数1、entries数组及每项字段/重复id。结果字段为 version=1、results=[{id,status}]、ok；status 为 ok/missing_file/skipped；无 missing_file 则 ok=true。is_file 接收 base_dir/path，只对启用项调用。该接口是 P2 明确输入，不是 CLI 公共 DTO。

## 6. 状态、顺序、正常与失败流程

无持久状态。完整校验→失败则 ManifestError/零文件检查→成功则逐项先判禁用→启用项调 is_file→有序结果。缺失或目录记 missing_file，继续后项。禁用字段仍校验。空 entries 返回空结果/ok=true。引擎不处理 argv、文件读取或 JSON 解析。

## 7. 恢复、兼容、迁移与集成

输入修正后可重新调用，无进度存储。没有数据迁移、旧引擎 consumer 或发布回滚协议。现有 CLI 不变。P2 必须读取 P1 实际结果和生产接口，再把 ManifestError 映射 exit 2，不能重写另一套校验。

## 8. 验证设计

P1-V1：模块测试合法/空/相对路径→P1-AC1。P1-V2：记录 is_file 并混合禁用/缺失/后项→P1-AC2。P1-V3：后续坏字段/重复 id→ManifestError/零检查，覆盖 P1-AC3。P1-V4：捕获标准流并比较输入/文件→P1-AC4。只证明引擎，CLI/整体验收仍待 P2；未执行。

## 9. Canonical 引用、本轮差额与未决项

source §3 的四类 authority 均实际读取；本轮增加引擎和模块验证，整体命令仍缺。由原 owners 维护真实 contribution 和晋升，没有必要未决产品问题。

# P1 Delivery implement：纯引擎

## 1. 输入与引用

读 Task PRD、source 全文和本文件 P1 PRD/design，尤其 design 第3节唯一处置及第5/6节条件。起点无前序、无 checker；真实身份不能用 P1 标记代替。

## 2. 有依赖顺序的步骤与文件责任

P1-I1：实施在 checker.py 写完整验证、结果/异常和禁用分支，产出可审生产接口。P1-I2 依赖 I1，在 test_checker.py 写合法/空/相对路径、禁用/缺失继续、格式先行和无输出测试。P1-I3 依赖实际结果，原 RDT/Architecture owners 维护真实引擎差额并按原路径审查晋升，再进入原 Check。cli.py 不改，剩余集成明确交 P2。

## 3. 验证入口、输入与预期观察

计划在真实示例对应仓库运行 `python -m unittest discover -s tests -p test_checker.py`，执行 design P1-V1–V4，观察返回结构、零/顺序调用、错误和无副作用，分别对应 P1-AC1–4。没有运行声明；原完整检查仍需保留已有 version 回归。模块测试不证明 check 命令已可用。

## 4. 停止条件与适用回退点

来源、候选或接口依据缺失时停相关步骤回原 owner；正常测试失败修复再验证。产品变化回 Clarify，机制变化回候选评估。只撤销本批错误，保留并行改动。无 DB/服务部署或写盘结果，无数据回滚。

## 5. Delivery Policy（唯一）

选择 partial。独立切片为纯引擎；remaining work 是 CLI 读取、JSON/标准流/exit、入口只读和 version 回归，以及全部真实集成验收。临时限制的对象是 CLI check 入口；原因是本批仅交引擎。解除条件是 P2 实现并验证既有引擎的 CLI adapter；P2 实施 owner 负责解除，原 RDT owner 负责更新当前使用指南。引擎可调用不等于命令可用；version 仍可用，不受该局部限制影响。P2 消费引擎而非复刻。整体 Completion 需 R1–R4/AC1–AC5 全覆盖；本批交付不能关闭整体责任。

## 6. Docs SSOT Plan（唯一）

选择 delta_first。原 RDT writer 写引擎行为/设计/唯一模块测试差额，consumer 为原 reconciliation/promotion 和 Check/Review；Architecture contribution 由原 Author 写、原 Architecture owner 审。最终 Phase 2 前完成所需晋升。source §3 是教学 authority；不得为本示例创建空 ledger 或修改共享导航。

# P2 Delivery PRD：接入 CLI

## 1. 整体来源与术语

读取 Task PRD、source 全文、P1 正文及真实前序结果。教学前提是：P1 原 owner 已交付 §5 的引擎，且 P1-V1–V4 有可核对结果；这只是示例前提，不是实际 delivered/pass。实际缺结果须回原 producer，不能靠本段继续。

## 2. 整体与本批目标、非目标

整体交付清单 check。本批独立交付可由 CI 执行的命令，覆盖 R3、R1 的读取、R4 的入口只读/version，并集成验证既有 R1/R2。排除重写引擎和整体非目标缓存/网络/修复/内容校验/写报告/文本模式。

## 3. 本批起点、前序结果、依赖与剩余责任

起点为前序已提供 validate_manifest/CheckResult/ManifestError，CLI 仍只有 version。本批依赖实际引擎及其结果；不能把 P1 的旧测试当本批 CLI 验收。P2 后无计划延期功能，但整体 Completion 仍需所有当前验收、原审核和跨批责任核对。

## 4. 本批调用方、场景与流程

| 场景 | 调用方/前置 | 触发 | 行为 | 可观察结果 |
| --- | --- | --- | --- | --- |
| P2-S1 | CI，合法含空清单 | check manifest | 读JSON、调既有引擎、输出 | stdout JSON/exit 0。 |
| P2-S2 | 操作员，缺失/目录/禁用混合 | check manifest | 复用顺序和跳过，缺失后继续 | 完整结果/ok=false/exit 1。 |
| P2-S3 | CI，不可读/坏JSON/字段 | check manifest | 读取失败或引擎异常转诊断 | stdout 空/stderr具体原因/exit 2。 |

## 5. 完整行为、条件与约束

读 UTF-8 JSON，清单父目录作为 base_dir 传入 P1 引擎。其 R1 格式/重复 id 先校验、R2 禁用不访问及缺失继续约束在集成中保持。正常只输出一个 `{version:1,results:[{id,status}],ok}` 对象，status 仅 ok/missing_file/skipped；无 missing_file（含空/全skipped）时 ok=true/exit0，否则 false/exit1。输入不可读、JSON/字段错误时 stdout空、stderr原因/exit2。命令不写盘/改输入，version 保持。唯一来源设计处置在 P2 design 第3节。

## 6. 本批验收、验证方式与未决项

P2-AC1 对应整体 AC1/AC3：真实 CLI 合法/空/相对路径及缺失/目录/后项，核对有序 JSON 与0/1。P2-AC2 对应 AC2：引擎的实际禁用调用证据加本批禁用集成，不用“路径不存在”单独证明零访问。P2-AC3 对应 AC4：不可读、坏JSON、字段错误/重复 id，stdout空/具体stderr/exit2，保留引擎零访问验证。P2-AC4 对应 AC5：输入/目录前后及 version 回归。实际前序缺失是阻塞依赖；教学产品本身无未决选择。

## 7. Canonical 引用与本轮差额

source §3 requirement 增 CLI 可用性，design 增 adapter 但不改纯引擎，test 增子进程集成，Architecture 沿原分层。剩余责任完成与否由原 Completion 核对真实证据。

# P2 Delivery design：CLI adapter

## 1. 设计目标、需求承接与内容基线

承接 P2 PRD，整体 R1–R4 不变。教学基线为上述 P1 接口前提，不是 Git SHA；实际 B 优先从原 projection 的合法前序 delivered head 解析，内容范围不重复 P1，再分别列 H0 与 PR目标。source §3.4 是架构边界，不伪造 candidate/final result。

## 2. 当前系统、边界与目标差额

已有纯引擎，CLI 只有 version。只在 cli.py 增 check 分支和 test_cli.py 增真实集成。checker.py 保持；若实际集成发现引擎缺陷，先由原 owner 判断修订范围，而非复制算法。

## 3. 来源设计处置（唯一）

| 来源/承诺 | 处置 | 落点 | 理由 | 影响 | 上游处置 |
| --- | --- | --- | --- | --- | --- |
| source §1 D-A 纯引擎与adapter分工 | retain | §4/5 直接调用既有引擎 | P1能力可复用。 | CLI新增，纯函数不改。 | 无偏离，先核前序事实。 |
| source §1 D-B 格式先行/禁用跳过/缺失普通结果 | retain | §5/6 错误和输出映射，§8回归 | 集成不改变语义。 | 异常exit2/缺失exit1。 | 无偏离。 |
| source §1 D-B 标准库 | retain | §4 JSON/Path处理 | 无新依赖。 | 保留安装边界。 | 无偏离。 |

## 4. 模块、职责与设计取舍

cli.py 处理参数、读取、JSON和标准流/exit；引擎负责计算。不把异常统一成missing_file，因为坏输入与缺文件不同。test_cli 调真实模块入口；没有新服务或持久化层。

## 5. 接口与数据

`report check <manifest>` 读取JSON，以清单父目录为base_dir，将Path.is_file传P1的函数。CheckResult字段原样输出version/results/ok，不泄漏内部Path对象。读取/JSON/ManifestError→stderr原因、stdout空、exit2；正常ok true→0，否则1。version仍走既有分支。

## 6. 状态、顺序、正常与失败流程

无持久状态。参数选择→读取UTF-8→JSON解析→调引擎（完整验证后才检查）→序列化一个对象→返回0/1。读取/解析/格式错误提前返回2；缺失为正常JSON结果，不走异常分支。禁用仍由引擎先分支，全skipped/空数组成功。

## 7. 恢复、兼容、迁移与集成

CLI只读，修正输入后重跑，无写入恢复。保留version，无旧check消费者或迁移。以真实P1结果/接口为集成前置；未取得则停止P2依赖。无需DB、远程服务或发布回滚。

## 8. 验证设计

P2-V1：真实CLI合法/空/相对路径与混合缺失/目录/后项，观察JSON/0/1→AC1。P2-V2：保留并复查P1禁用调用测试，再跑混合CLI→AC2。P2-V3：CLI不可读/坏JSON/字段及引擎零调用回归→AC3。P2-V4：前后字节/目录比较与version→AC4。测试未运行；P1事实不能替代本批集成证据。

## 9. Canonical 引用、本轮差额与未决项

读source §3四类authority，本轮只补adapter与集成，纯引擎能力是前序事实。原RDT/Architecture owners维护真实差额与晋升；无产品未决项，前序身份/结果不可读时停对应owner。

# P2 Delivery implement：CLI 集成

## 1. 输入与引用

先读Task PRD、source全文、P1实际生产接口及结果、本文件P2 PRD/design，尤其design第3节唯一矩阵和第5–8节。只使用当前合法P2身份/范围；教学标记不能进入公共状态。

## 2. 有依赖顺序的步骤与文件责任

P2-I1：实施先核对P1实际接口和验证，缺失回producer。P2-I2依赖I1，在cli.py写读取/JSON/引擎调用/标准流和exit，保留version。P2-I3依赖I2，在test_cli.py执行真实子进程的P2-V1–V4，同时保留引擎边界测试。P2-I4依赖实际实现/结果，由原docs owners维护差额并在最终Phase2前完成必要晋升，原Check/Review覆盖本批和集成。P2-I4 实际核对 P1 的 CLI 限制解除条件：实施 owner 将当前“check 尚不可调用”说明和只接受 version 的断言更新为真实 check 行为；原 RDT owner 在合法晋升时更新当前 usage 与派生指南。P1 正文和当时模块测试结果保留历史身份。原 Check 比较当前要求、命令行为、指南和断言，不能因旧断言仍绿保留已失效限制。

## 3. 验证入口、输入与预期观察

计划运行`python -m unittest discover -s tests`。P2-V1–V4的数据与观察见本批design第8节：合法/空/相对与缺失/目录混合、禁用调用、输入错误分流、只读及version。它们映射P2-AC1–4并共同支撑整体AC1–5。实际运行结果与前序模块结果分列；这里没有通过声明。

## 4. 停止条件与适用回退点

前序结果/接口/当前scope不可读则停止对应依赖，回原producer；格式或输出回归修复本批并重验。发现整体要求变化回Clarify，机制变化回候选评估。保留并行工作；只读CLI无DB或服务回滚，不创建额外恢复协议。

## 5. Delivery Policy（唯一）

选择partial：当前切片是整体中剩余的CLI集成；P1是历史已交付部分。本批成功后没有计划未交付功能，但整体责任仍由Completion汇总两批真实实现/验收和当前scope，不能仅因remaining work为空推定完成。缺任何整体验收保持缺口，不覆盖P1历史。

## 6. Docs SSOT Plan（唯一）

选择delta_first。原RDT writer基于source §3记录本批CLI与唯一集成测试差额，直接consumer为原reconciliation/promotion和Check/Review/Completion。原Author写真实Architecture差额，原Architecture owner审查；最终Phase2前完成必要晋升。本文件不改共享导航，不预建空贡献。
