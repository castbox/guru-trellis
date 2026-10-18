# #331 唯一 Test 结果与边界

状态：`executed`。本文件拥有本轮行为、工程和安装验证结果；它不代表后续正式 Check、Review、Delivery 或 Task Completion 已通过。测试策略和稳定关系见 [当前 Test 单元](../../test/current/knowledge-maintenance.md)。内容比较基线为 `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`（B）。

## 方法、数据集合与测量边界

实施前由所选 Delivery design 第8节固定 V331-A..D、必答事实、必要条件、3次 old/new 及成本判据。实际使用 native `codex exec --ephemeral --json`，CLI `0.162.1`，同一默认 `gpt-6.1-sol` / high 配置。A 为 read-only，B/C/D 为 workspace-write；每次独立语料副本，不预载另一侧答案或评分表。AI 逐次读取答案、命令轨迹和实际文件差额作语义判断；采集脚本只统计 events、usage、输出量和 paths。

最终24次集合为第二轮完整语料的 old A/B，以及修复后的最终语料 old C/D、new A/B/C/D。old 侧来自 B 的完整文档及必要 canonical 执行源；新侧为本轮完整候选和已审拟晋升正文。D 双方使用来自同一真实 `trellis-extension-stack@1.0` 的等义两层 fixture，旧侧采用旧组织；不能据此声称 B 已有该通用源或外部业务已经采用。

C 双方 host 均在完整初始语料建立真实 Git commit。old=`dd00703652c021c5f48ab27ef164201ecee1f6cd`，new=`2800949f6f488ef0b546915a8deabd2383a0bc81`；它们是各自完整初始 tree，不能冒充远端 B。受测 Agent 不 commit。旧 Task 的入口、正文和必要引用在同一固定 tree 解析；更早不可取得的对象明确保留缺口。A/B 起点不因 C 增加 Git 而改变，D 使用独立 fixture。

表中 total input 是 native 实际 usage，包含公共注入、读取指令、重复上下文和工具结果；cached 单列，不从总量扣减。raw tool-output bytes 是 CLI events 捕获的 stdout 字节，工具命令数是实际 command_execution 数。raw 字节不能精称平台内部裁剪后模型可见的文档字节；混合输出也无法准确拆成导航、正文、重复、无关历史四个互斥字节数。下文按轨迹说明这些类别，并用实际总输入和可观察读取量共同判断。文档 paths 排除 Git index/cache 等内部变化，包含实际正文、关系、贡献和本地验证记录。

## 全部24次实际数值

| Run | Total input tokens | Cached input tokens | Raw tool-output bytes | 工具命令数 | 实际文档 paths |
| --- | ---: | ---: | ---: | ---: | ---: |
| old-A-1 | 1354292 | 1229440 | 553934 | 18 | 0 |
| old-A-2 | 1646764 | 1523584 | 464110 | 24 | 0 |
| old-A-3 | 925019 | 811648 | 436903 | 27 | 0 |
| new-A-1 | 859356 | 762496 | 365028 | 23 | 0 |
| new-A-2 | 529398 | 445952 | 255677 | 14 | 0 |
| new-A-3 | 713948 | 619904 | 295861 | 19 | 0 |
| old-B-1 | 1321387 | 1207040 | 1133348 | 18 | 8 |
| old-B-2 | 2020398 | 1888000 | 605256 | 24 | 8 |
| old-B-3 | 1403954 | 1280896 | 536289 | 22 | 8 |
| new-B-1 | 1524095 | 1401984 | 1800118 | 23 | 7 |
| new-B-2 | 1612735 | 1520384 | 365573 | 21 | 10 |
| new-B-3 | 1880515 | 1771008 | 1843959 | 25 | 8 |
| old-C-1 | 2332468 | 2230016 | 476357 | 30 | 20 |
| old-C-2 | 2777502 | 2638208 | 608758 | 26 | 26 |
| old-C-3 | 2300872 | 2157312 | 694946 | 23 | 20 |
| new-C-1 | 1374271 | 1267968 | 390360 | 17 | 15 |
| new-C-2 | 2117712 | 1993856 | 420040 | 25 | 27 |
| new-C-3 | 1616196 | 1512192 | 397591 | 22 | 15 |
| old-D-1 | 819626 | 759808 | 208982 | 15 | 3 |
| old-D-2 | 784328 | 698624 | 306074 | 17 | 3 |
| old-D-3 | 637409 | 557440 | 308933 | 17 | 2 |
| new-D-1 | 668566 | 603392 | 242833 | 13 | 1 |
| new-D-2 | 744733 | 676992 | 266506 | 11 | 1 |
| new-D-3 | 631198 | 548224 | 959675 | 11 | 1 |

## 正确性、读取与维护判断

**V331-A / T331-01：六次核心答案完整，零文件修改。** Task whole scope 与 Delivery slice、D1/D2 独立 Planning、唯一 Author、Activation、Check/Commit/独立 Review、Delivery facts、Completion→Closure→Finish/Cleanup 均明确。后继治理直接给出独立 Phase2→原 owner 晋升→实际写入适用性→最终 Check→commit→独立 committed Review，保留 expected-current、独立性、ADR-028 阶段适用性和 ADR-030 窄替代范围，并能追溯原因。没有以 merge、目录或旧 pass 冒充完成。

A 的 total input 中位数为 1,354,292→713,948（下降47.28%）；raw 输出为464,110→295,861（下降36.25%）；命令数24→19。必要正文包括 writing/Skill/contracts、生命周期/终态 R/D/T、workflow 和本题要求的 ADR 原因。旧入口夹有多轮历史正文，普通查询需进一步读旧版本/贡献链；新侧直接读完整 current 单元。因问题要求追溯的 ADR 历史属于必要来源，不能算无关。宽泛搜索、重复读取和机械输出全额计入；未把正文挪到免费注入。此组满足保持完整性的实质读取改善。

**V331-B / T331-02：六次均完成相关 R/D/T 一致修订与稳定身份映射。** 补证条目保留无新证据等待、获取条件、fresh whole-scope 判断、真实实施工作分流和原证据层次。拆分明确 Closure 与 Finish/Cleanup 的责任，保留 retain_open、普通状态漂移与恢复条件。Architecture/API/运行代码没有变化，实际无影响依据可核对；旧版本未改。

old 每次新增五份隔离贡献并修改三层导航，共8 paths；new 分别7/10/8 paths。new-B2独立拆出三层 evidence 正文，因此不能宣称每次或整体维护文件数下降，中位数仍为8。旧侧为重建当前 Completion 规则读取531/547及旧版本链；新侧从完整 current、迁移关系与 canonical 规格读取，不回放旧版本贡献链，满足预定的“历史拼接减少”判据。

B 总成本上升：total input 中位数1,403,954→1,612,735（+14.87%），raw 输出605,256→1,800,118（+197.41%），命令数22→23。new-B1/B3各两次输出约697 KB全目录 SHA 清单；old-B1一次约689 KB，其余没有此大输出。这是 Agent 实际选择的机械核对，全部保留计量，不能扣除后宣称全面节省。

**V331-C / T331-03：六次贡献隔离、依次晋升、完整定义和旧读取保持正确。** alpha/beta各自拥有贡献；第二次晋升保留第一项及原有条件。新侧查询直接读取最终完整定义，旧侧仍从版本前驱与贡献取得定义；旧 Task 用真实初始 Git tree，原版本/Architecture 正文不被回填改写，无关推进不要求旧 Task 重写。测试只是知识维护，不声称真实 Task provider/gate 已执行。old-C1实际从Git读Architecture入口和`.109`需求页，C2/C3读三层入口；原历史字节另经初始blob比较证明保留。new三次实际从固定tree读取必要完整Completion正文及入口。不能声称每次逐字展开了全部历史闭包。

old 实际20/26/20 paths，new为15/27/15，中位20→15。new-C2选择建立两个本地版本入口和 Test 全文快照，并更新相应 RDT/Architecture 关系，R/D正文不变；这是可解释的额外维护，非本场景必要步骤，不能据此声称每次减少维护。new-C1/C3仅修改 Test 当前正文/导航并保留隔离来源。total input 中位2,332,468→1,616,196（下降30.71%），raw输出608,758→397,591（下降34.69%），命令数26→22；晋升后当前查询不再拼接两项贡献补出定义。兼容子项只判断正确，不要求节省。

**V331-D / T331-04：六次两层来源与缺口处理正确。** 双方固定真实通用源/version，源 owner 与项目 owner 分开。中文 PR 差异仅写项目投影及必要导航/说明；通用源字节不变。缺失外部源只报告受影响结论并回原 repair/澄清；未迁移范围继续指向 `.109` 和完整继承源，不能报告全 corpus 完成。new每次仅改1个项目文件，old为3/3/2 paths。total input 中位784,328→668,566，raw306,074→266,506，命令数17→11；此组只按兼容正确性验收，不以成本降低替代判断。

## 历史拼接的独立计数

AI逐条按命令轨迹分类：读取旧版本页/旧贡献以重建现行定义时，一条命令计一步。混合命令不拆字节；当前正文、canonical规格、题设要求的ADR原因/既有测试证据，以及固定tree兼容核验不计为历史拼接，但仍全部计入总成本。

| 组 | old三次历史拼接steps | new三次 | 中位 |
| --- | --- | --- | --- |
| A | 4 / 4 / 6 | 0 / 0 / 0 | 4→0 |
| B | 6 / 6 / 7 | 0 / 0 / 0 | 6→0 |
| C | 5 / 5 / 4 | 0 / 0 / 0 | 5→0 |

A旧侧主要读取531与109→108等前驱以重建生命周期；B旧侧读取436/531/547、90/70等前驱确定终态；C旧侧读取436/531/547/567与90前驱确定原约束。新侧直接从current取得现行定义，再按必要关系读取来源。这个方法指标不等同固定token量，尤其不能覆盖B的总成本上升。

## 首次失败、普通执行偏差与修复

1. 首版实验语料只含 docs 与两个维护 package，缺必要执行源，不是完整正常起点。保留首次记录，停止该 runner，完整补齐后重做；首版不计收益。
2. 第二轮新侧发现拟晋升贡献 metadata 仍是无时间限定 proposed，与新导航矛盾。原 owner补齐贡献状态和固定 revision 同 tree 读取说明后，新侧全部重跑；该轮原新侧结果不计最终收益。
3. D旧fixture移动项目文件后残留一处相对位置说明；修正为双方一致的可读起点后，D双方同口径重跑。C旧试次没有真实Git，不能证明固定revision读取；C双方建立真实Git初始tree后重跑，原无Git C不计验收。
4. 最终各组仍有普通错猜路径、缺 `.agents` 或无Git时调用Git等非零工具返回。Agent沿真实入口修正或明确限制后完成核心行为。old-A错猜 ADR/Architecture versions路径、new-A2错猜ADR名、old-B2初写错误ADR链接后修复，均保留首次错误。new-B2还有一处无consumer的许可性措辞，记为写作执行偏差，不形成或供下游消费任何生命周期结果，不把它加入产品机制。
5. old-D3曾把当前run自生SHA清单临时写出工作目录，随后移回、仅读自生清单核对并删除，最终披露。没有读取其他试次答案或外部知识；核心源不变。不得描述为零路径执行偏差。
6. C旧侧两次因三/四列表差异发生局部晋升断言，随后读回并完成同一次晋升；另一次先校验尚未写出的本轮报告，补写后重核。旧历史7个断链被明确保留，未冒称全历史链接通过。new-C3遇更早B对象在fixture不可得，实际使用可验证初始tree并明确限制。C2的额外快照及 B 的巨大机械 stdout均保留实际维护/读取成本，没有挑选更好的一次代替三次中位数。退役试次、setup错误及修复均不覆盖成最后成功。最终核心语义判断和上述执行偏差分别报告。

## V331-E / T331-05：真实迁移与工程验证

原 owners逐条核对[迁移追踪](./traceability.md)的21组前驱/后继，包含 `.53` 原稳定身份与531/154/292/530/535/567/600/436/454/434/547/383/557/569/578等有效后继。三个主题的九份正文保留完整行为、条件、否定、例外、顺序和必要关系；canonical公共接口继续单写。Architecture治理直接收敛ADR-028/030当前要求，generic源与项目选择分开；其余主题明确为 legacy_unmigrated，不谎称全历史已迁移。

| 检查 | 实际结果与层次 |
| --- | --- |
| RDT focused contract/runtime | managed Python执行 `python -m unittest discover -s trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/tests -p 'test_*.py'`，9项通过。证明原输入/出口/普通stale投影仍可调用，不证明AI语义。 |
| Architecture focused contract/promotion | 同managed Python，`GURU_UPSTREAM_DELIVERY_SCRIPTS`指向匹配Fork的dist模板，执行该package `tests/test_*.py`，39项通过；含原候选/晋升/实际写入绑定。 |
| Source package validator | `check-skill-packages.sh --json --mode source`通过，实际40 packages/124 commands；接口、profiles、schema及typed graph未变。 |
| Dogfood drift | `check-dogfood-overlay-drift.sh`通过；canonical workflow、shared、Claude/Codex/Cursor和managed spec一致。 |
| 基础检查 | 340份Python内存compile、marketplace JSON、Bash语法及 `git diff --check`通过；变更相对链接/markers可解析；旧versions/历史贡献未改。 |
| Task/context | 官方task validate、phase2.1/3.5提取通过；两份大规格有injection size warning，实际owners自行完整读取，不以截断注入代替加载。 |
| 未触及旧文案suite | `test_434_workflow_prose.py`共18项有3项失败；在B与候选同managed环境复现相同失败，分别为installed workflow graph计数、project index graph计数、quality旧计数。原因是旧38/187/114与现40/206/124数量文案，不在本轮改动语义。记录为pre-existing，不宣称全suite绿色，也未扩改为计数清理。 |

首次迁移不是零成本：人工读取前驱、合并九份正文、维护三层导航/来源映射、通用源和项目选择，并修复候选metadata/历史读取说明。没有生成索引服务、重复自动视图或长期遥测；未来只由原owner修改受影响正文及必要关系。旧入口历史正文从当前默认路径退出，旧版本和Git追溯保留。

## V331-F / T331-06：安装、更新与dogfood

代表性 clean/init实际采用 clean `castbox/Trellis@7bcbeaad31380e7a29c97898cb947c6120a61775`，CLI/Core `0.7.0-castbox.4`，从该Fork CLI运行，未用全局旧 `0.6.17`。两个临时目标分别为clean与已有B完整preset更新，均选择Codex/shared；候选workflow为明确的local source projection，完整preset来自同一execution source，含dirty候选，不冒称远端exact source-lock。

clean完整apply、B→candidate更新、reapply、同Fork官方 `update --dry-run`→`update --skip-all`、update后reapply均最终成功。更新首轮正常产生13个`.bak`且无`.new`；逐个核对备份等于旧文件、当前文件等于候选后，仅删除这13个已验证备份再reapply，最终sidecar=0。每目标6161份Guru/平台/workflow/AGENTS文件bytes/mode在官方update前后不变，用户AGENTS行保留。两维护package及共享正文installed/shared/Codex一致、invoke可执行、managed spec一致；installed validator通过，4次实际public discovery成功。

首轮默认PATH Python安装锁定依赖失败，改用已有managed interpreter后恢复，未改lock或上游。dogfood普通apply在旧历史Task preflight前置拒绝 `upstream_delivery_migration_required`，没有搬移/转换历史Task来绕过。随后原 `guru-upgrade-tools`用同checkout完整local_candidate source，按preview→prepare→invoke完成tools-only同步，真实出口 `tools_upgraded` / `0.7.0-guru.4`，保留 `formal_fork_source_lock` 未验证边界。

dogfood212个public targets最终bytes/mode与原计划一致，2656个Task/archive/runtime-session/common-control文件未改，307项peer/common bindings保留；仅建立checkout-local runtime选择。五份installed/shared/Claude/Codex/Cursor新正文与canonical一致，installed validator/drift/boundary通过、sidecar=0，主会话public Delivery仍为同key/implementing，原Planning result保持。

## 验证结论与未覆盖范围

V331-A..F按各自预定判据成立：完整查询有实质读取改善；B/C修订减少历史拼接，成本和额外维护如实报告；D与旧Task/缺口兼容行为正确；本仓库代表性正文、canonical/dogfood/installed及匹配更新路径已实际验证。此结论不等同原维护owner已晋升、正式Check/Review或整个Task已完成。

本轮没有证明完整跨版本升级、完整多平台Release矩阵、远端exact-candidate/source-lock、外部业务仓采用或生产效果。官方update是同版本Fork的维护，不是跨版本升级。normal-scenario知识实验不是正式Task/Issue provider事务。CLI可观察raw输出无法细分平台内部可见文档字节；真实总input包含其全部成本，不用缓存扣减。原始traces只在repo外短期留给当前review consumers，消费后退休；长期只保留本文的结果、失败和边界。
