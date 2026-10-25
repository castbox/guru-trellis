# #637 测试策略与本轮实际结果

状态：正式 Delivery 与 Task Completion 已有原公开结果。以下 Test 对应 Task design V637-01..08；策略不是通过声明。原工程观察保留当时截止点，较晚正式结果见文末，不据此升级其它未证项目。

| ID | 实际入口/输入 | 必须观察 |
| --- | --- | --- |
| T637-01 | 原公共Task/Delivery及七owner wrappers首次链 | 首次完整独立；当前Check/Review/readiness/predecessor真实绑定 |
| T637-02 | matching installed实际Agent，文档冲突/finding修订及未改consumer | 审双方/组合/依赖，当前完整覆盖，闭合不无因换新全量 |
| T637-03 | 共享Runtime/事务正常实现错误，原命令缺失/环境变化 | 扩审未改consumer并检错，缺项补跑，无关事实保留 |
| T637-04 | 同树提交/无关target前进/公开结果恢复/退休checkpoint | 固定B与同Delivery，旧gate不冒充当前，缺覆盖补审，无私有跨读 |
| T637-05 | 同构旧新实际Agent样本 | 充分性/检错成立，语义/命令/正式记录/远端等待分别实测，不预设收益 |
| T637-06 | #636实际installed早期入口及本Task获准远端动作 | 同PR/key/HEAD接续，Draft不冒充full_review；#638未来接口未验证 |
| T637-07 | canonical/platform/installed、单clean、apply/reapply/drift/mode/sidecar/在途恢复 | 完整matching投影和真实installed行为；非完整Release矩阵 |

## 已执行工程事实

原test_candidate_reuse.py通过真实Git及公共Check/TaskCommit/BranchReview/Readiness wrappers执行2项，12.000s，exit0：原Review checkpoint退休后，实际文档候选变化保留原public覆盖但不适用旧gate，旧输入被拒，新Check/full_review绑定精确最终candidate和Check predecessor；实际同树amend后由当前Check和clean Commit reentry接续，不制造额外提交。fixture语义authoring不证明AI实际判断，文档修订测试也不冒充真实Git冲突。

| 命中检查 | 实际结果与边界 |
| --- | --- |
| TaskCommit `test_early_draft.py` | 2项，4.138s，exit0。原#636提交入口的fixture回归通过。 |
| Publication `test_early_draft.py` | 3项，14.003s，exit0。原#636发布入口的fixture回归通过，不证明真实远端PR。 |
| source package validator | `check-skill-packages.sh --root . --mode source --json`返回passed，40 active packages、124 commands、134 test assets；证明结构及分发机械条件，不证明Agent语义判断。 |
| diff、语法与平台格式 | `git diff --check`及新增测试AST解析通过；实现owner的JSON/TOML overlay解析通过。尚未据此声明installed投影或运行行为通过。 |
| Task上下文与checkout | 原`task.py validate`通过，且提示3份规范超过32768字节注入上限；Agent需显式完整读取，不以截断注入证明已读。当前registered checkout边界检查返回ok。 |

安装首次尝试：将固定B的完整source普通clone作为dogfood目标执行apply，因clone含历史legacy archives而返回`upstream_delivery_migration_required`。保留历史归档，不删除或迁移来绕过；该尝试不计成功。

随后在全新临时Git仓库，以Fixed Fork CLI的官方marketplace入口固定到B执行`init -y --codex --no-monorepo --workflow guru-team`，exit0；再从固定B完整source执行preset apply，status=ok，无skill/overlay conflicts。这只证明当时旧B clean安装准备成功；新候选与实际Agent样本的后续结果另列。原始命令日志保留在本轮临时验证位置，不提交原始日志或本机路径。

## 后续实际结果

原TaskCommit实际返回`draft_committed`，H=`fd16444370c3eceed68c02dc1fc344114bc2ae7e`，固定B保持。原Publication随后返回`draft_published`，真实PR为[castbox/guru-trellis#644](https://github.com/castbox/guru-trellis/pull/644)，读回OPEN/Draft、同Task/Delivery、main目标与该H一致。正文为Refs-only，未产生最终PublicationFact。三平台Targeted native CI均通过：Ubuntu 2m33s、macOS 5m26s、Windows 5m55s；这些是GitHub job duration，不当作本地语义或远端提速收益。

独立`trellis-check` reviewer实际读取完整59文件B..H及消费者，经原`delivery_draft_content_review`返回`draft_content_reviewed`，没有成立finding。一个短语候选经原normal/solution入口均为`rejected_not_reproduced`，未进入修订或阻塞。该call-local早期分析不写full_review，也不替代最终Check后正式Review。

| 定向检查 | 实际结果及限制 |
| --- | --- |
| 五个package `test_contract.py` | TaskCommit 5项、Branch Review 26项、Delivery Review 7项、Publication 6项、Merge 10项均通过。 |
| Check合同测试 | 12项中2项失败；固定B复跑出现相同两项：预期exit列表缺既有legacy出口，workflow精确短语断言在B已不满足。保留为基线限制，未扩改历史测试，不记整组通过。 |
| Architecture合同测试 | 首次32项均因缺显式upstream scripts依赖失败；补实际Fixed Fork依赖后，整组在archived只读前后全目录相等断言的difflib差异计算中持续占用CPU，人工中止，exit130，整组未完成。另选本项直接命中的AI执行顺序、独立committed范围、Planning/非Planning合同3项，3.426s，均通过。 |
| 平台库存 | 原`test_guru_platform_inventory` 11项，4.199s，均通过；证明声明投影机械条件，不证明所有平台实际Agent。 |
| preset定向 | 原clean/reapply managed spec、current reapply、kernel inventory 3项，93.630s，均通过。首次缺upstream路径、随后从子目录运行缺runtime定位的两次环境调用失败均未计通过；补依赖并从仓库root运行后才取得上述结果。 |
| 新候选clean安装 | 官方marketplace固定H的Codex init成功，再从干净完整H source应用preset，status=ok；该target自己的installed package validator返回passed/errors=[]。reapply/drift、其实际Agent运行与在途行为另行验证。 |
| Check公共Delivery流 | 原`test_delivery_flow.py` 16项，50.186s，均通过。覆盖当前候选重入、Check元数据不强制第二提交、固定范围与公开结果恢复；这些fixture不证明实际Agent语义审核。 |
| 固定候选 | 原`test_fixed_candidate.py` 3项，2.535s，均通过。覆盖无关fetch保持固定候选、真实HEAD变化不继承旧gate、后续Delivery独立base恢复。 |
| 晋升引用对齐 | 原`test_promotion_alignment.py` 4项，22.858s，均通过。覆盖原公开结果、清空slot后新Check到consumer，以及真实候选变化的阻塞；不代替本Task实际共享晋升。 |

实际Agent旧新样本已分别通过公开Task/Delivery创建、C4绑定、原Author requirements/plan入口、Wording、真实独立Architecture candidate/final_plan、Approval和Activation。两个Architecture正式出口均为`baseline_current/no_architecture_impact`，final均为`promotion_state=no_change`；两边Activation均实际返回`delivery_started`。初次实现、正式Check、提交和首次完整Branch Review均已完成，后继差额仍在验证。setup中的参数、设计locator和reviewer session前置错误经各原owner停止、读回并fresh re-entry，未通过改state或伪造结果跳过。该setup耗时不计入后继候选语义/命令/正式记录/远端等待的对照收益。

新样本在Planning成立后、业务实现前执行完整preset reapply。默认PATH的Python 3.12.8在3.4527s返回`dependency_install_failed/python-runtime`，未计成功；同source、同apply入口选择首次成功clean安装已确认的managed Python后，15.1829s实际成功。未修改lock或manifest。前后Task全部公共文件字节、selection、implementing阶段和当前session相同，`.new/.bak`均为0，installer的new_copies/managed_backups为空。该结果证明此样本的完整reapply保全；不扩张为所有解释器、开发Task matching切换或Release矩阵结论。

## 实际同构样本：首次覆盖

两边为相同的整数分运费policy和两个独立consumer（checkout/invoice），实际业务与测试候选相同。三独立测试入口分别为6/4/4项；原执行者另跑整体14项及diff hygiene，全部成功。两位独立审核者均先读Architecture权威、完整实现和consumers，确定当前检查集后才读取原执行事实，再完成真实Architecture和九维Check。均无实际缺陷候选，原Check正式出口为`passed`；这不是首次完整Branch Review的替代。

| 首次阶段 | 旧B完整安装 | 新H matching安装 |
| --- | --- | --- |
| Architecture实际读取/判断窗口 | 约111s，含一次输入token混用纠正；成功formal 0.592025s，失败调用0.621327s另列 | 约101s，含两个producer定义核验；formal 0.517593s |
| Check实际读取/判断/编写窗口 | 约105s；record/check/invoke合计2.558316s | 约116s；record/check/invoke合计2.512642s |
| 本轮工程事实 | 采用原5条命令（3独立tests、整体tests、diff-check），原耗时0.204480s；另补文本/JSON/hygiene 0.065900s | 采用同定义原5条命令，原耗时0.204490s；另补文本/AST/JSON/JSONL/hygiene 0.087709s |
| 原TaskCommit | prepare/invoke合计3.259746s，精确提交13文件 | prepare/invoke合计3.096980s，精确提交13文件 |
| 远端等待 | 0；本地样本无远端动作 | 0；本地样本无远端动作 |

上述窗口按实际clock读数记录，含接口核验与工具往返，不是精确模型计算耗时；formal与工程命令单列，不据此相减伪造纯语义时长或收益比例。Planning/setup不计入优化对照。原Architecture调用曾把Delivery的路径content_ref填入不同定义的整树content_identity，旧轮真实返回`stale_identity`并停止；读取各原producer后fresh reentry成功，未改public candidate或伪造通过。

提交改变HEAD后，两边均沿原Reviewing公开rework和implementation begin-check绑定实际committed候选，保留原key/Planning/B；旧Check在公共历史中明确不适用。两边当前Check随后均正式`passed`，原clean TaskCommit re-entry返回现有HEAD，没有为绑定再造第二提交或新Delivery。

首次完整committed Branch Review两边均实际`passed`，各自Architecture当前stage、recorder、checker和public wrapper真实执行。旧安装使用新的独立Architecture/Branch reviewer；新安装由原未参与实现的独立reviewer继续，先Architecture后Branch的完整当前判断仍真实完成。两位均未发现缺陷候选。新轮本stage实际读取/判断窗口为准备24s、Architecture约31s、Branch约45s；等待40s单列。新轮Architecture formal 0.476842s，Branch record/check/invoke合计2.221036s，没有重跑业务测试。旧轮active wall为236s，包含源码/规划读取、判断、编写、接口核验和enum修正，不能当作精确纯语义耗时；成功Architecture+Branch formal合计2.236775s。旧reviewer额外重跑三项入口，0.107862s，但没有发现原事实失效的具体依据；该额外执行及0.746721s的失败输入调用不计作旧合同必然成本或复用收益。以上窗口口径不同，不计算提速比例。

两边Review checkpoint均由各原wrapper实际退休；下一consumer从public Delivery结果和精确Git对象取得B/H、当前Check predecessor及full_review。新轮还实际通过原wrapper的public-result recovery取得同一最小`passed` DTO；没有读取或重建退休gate。

new后继同树amend实际将HEAD改为`c849cc3617886a6dcc0293fe88aba10dd310f539`，新旧tree均为`074edce6379f3bb84f7376ae5763109b18fc2e53`，完整Git diff为空。原API将旧Check/full_review明确标为不适用，原独立owner亲自核完整差额、13paths/两个consumer、scope/plan，以及同一路径Python 3.12.8、标准库、检查参数/定义/预期，再形成当前Architecture和Check。原clean TaskCommit re-entry保持新HEAD，无第二提交。该owner随后从原public full_review、Git对象与仍可核验的命令结果接续，亲自形成当前stage Architecture和完整当前Branch Review；两者正式结果均通过，public full_review精确绑定新HEAD和新Check predecessor，原wrapper再次实际退休其checkpoint。本轮业务测试和hygiene重跑均为0；没有新审核者、退休gate重建或新ledger。同树只提供内容绑定依据，工程事实仍经单独适用性判断。

同树当前Phase2 Architecture读取/判断窗口约54s，Check当前判断/编写约45s；其formal分别0.485494s/2.656666s。clean committed re-entry为0.794816s；当前Branch阶段Architecture约21s、Branch判断/编写约33s，成功formal合计2.481625s；远端等待0。窗口含绑定/接口核验与编写，不当作纯模型计算或固定收益比例。后继文档冲突与缺证据补跑的实际结果见下文。

## 实际共享 Runtime 与未改消费者

运费policy属于业务规则库，不能承担共享Runtime验收。V637-03另使用固定B/H的两个完整临时source，在既有`trellis/skills/guru-team/runtime/reviewed_content.py::_tree_entries`引入一处普通mode归一化错误：把实际Git `100755`错误记为`100644`。两份source的两个原公开消费者`guru-review-branch`与`guru-verify-extension-installation`的identity wrapper、原harness和tests均保持HEAD字节。

独立configured check Agent先从实际shared delta和依赖图确定两未改消费者的影响范围，再选择原`test_reviewed_content_identity_integration.py::ReviewedContentIdentityIntegrationTest.test_current_wrappers_share_one_identity_across_real_git_drift`。该test创建真实Git对象，包含合法路径、mode-only和blob变化；不写Task或正式gate。Agent还排除了另一个有界continuity oracle的无关mode测试，没有扩跑整组。

原baseline命中检查两侧各1项通过，原命令耗时3.255843s/3.292296s。Agent核相同Python 3.12.8、jsonschema 4.25.1、Git 2.54.0及原argv后，因shared依赖已变而拒绝把原绿事实用作当前pass，实际补跑同一命中test。两侧均在第228行`assertNotEqual(path_identity, mode_identity)`失败，两个未改入口不能区分mode-only变化；各1项、exit1，unittest报告2.904s/2.905s。实际负向原始stdout/stderr只在该Agent当轮工具输出中存在，没有事后补造日志；本Test保留直接消费者需要的具体原因、对象和结果。

原writer随后只恢复该shared文件至各自HEAD原blob`c3ef22ad4827e2df7a2ac52a25b6bb46d7e93ab4`，两个source恢复Git clean。原同命令实际新执行两侧各1项、exit0，命令耗时3.344478s/3.278055s。持有原检错理解的同一独立Agent亲自核修正、两个未改consumer、test与环境，采用这两条新执行事实并判定本Runtime样本闭合，未再重复命令。独立检错已计时复核段48s，前置读取未精确计时；独立闭合15s，远端等待0。该样本是实际Runtime依赖变化与闭合证据，最终main Check/Review仍须亲自消费和形成正式结论。

## 实际文档冲突：解决稿与整合提交

两侧target先只新增无关`target-notes.md`；feature只fetch到本地固定ref，公共Delivery、B/H及既有gate保持，未执行Reconcile或业务重测。随后feature通过原#636 `delivery_draft_commit`只提交`sample/design.md`的等义需求链接。target另在同段明示既有R1/R2净额、5000分免运费及600分费用。原`execute-base-candidate`两侧均真实返回`conflicted`，唯一冲突文件为该设计文档，live feature保持原HEAD且没有MERGE_HEAD。

原Reconcile owner实际完成normal→solution→eligible-root判断；前两者为`qualified_current`，root为`not_incident_applicable`。该结果只在进程内消费。真实merge产生同一文档冲突，解决稿保留双方完整含义及target无关文件。原public API绑定固定B/实际F/14paths；两独立owner读取双方正文、完整解决稿及两个未改consumer，确认新增说明没有改变业务行为。两侧原Architecture均实际返回`baseline_current/no_architecture_impact`，原resolved Check均返回`resolved_reconciliation_passed`；没有把旧Check当作当前结果。各Check owner只消费自己的私有结果，实际投影最小公开Reconcile输入。

| 解决稿阶段 | 旧B安装 | 新H matching安装 |
| --- | --- | --- |
| 实际判断窗口 | 稳定后228s，含读取、判断和正式执行；此前已计候选等待至少94s | Architecture约93s，Check约45s；不含此前idle |
| 原正式调用 | Architecture 0.428s；Check record/check/invoke及projection合计3.382s | Architecture 0.514442s；Check三步合计2.637762s，projection 1.472640s |
| 工程采用与补充 | 采用原6/4/4及整体14结果；核当前candidate/index hygiene和Git绑定，无unittest重跑 | 核原输入、依赖、Python环境、定义与预期后采用原14结果；新增文档/链接/staged diff检查0.028717s，无unittest重跑 |
| 原resolved executor | 1.120265s，实际M=`0705c48a62cfb4d9793ee0dcc2c67316f94d5d73` | 1.040807s，实际M=`890f3d105d79d86f161c121f869a2c0f0bc2300e` |

两个M的父序、tree、message均与原公开输入逐项一致，提交时Git clean且MERGE_HEAD退出。原executor返回的是`formal_exit=false/status=committed`中间结果，不冒充`reconciled`正式出口。窗口含接口核查和编写，不是纯模型计算。旧owner自选重复hygiene不计作旧合同必然成本；样本无远端写入或等待，不计算性能比例。

提交后，两侧均经原public rework和implementation候选绑定保留固定B/同Delivery，并取得当前Architecture、正式公开Check及完整committed Branch Review。两次原TaskCommit `delivery_committed_reentry`分别耗时0.841722s/0.797842s，均返回既有M，零额外提交；两次原`project-resolved-full-review`分别耗时0.385454s/0.386782s。没有把解决稿Check直接当作committed Check。old那次begin_check由Check worker执行父委托的精确API操作，原implementation owner随后只读复核并承接绑定事实，不伪称自己执行过该写入；new由Check owner rework后交原implementation owner实际begin_check。

| 最终当前结果 | 旧B安装 | 新H matching安装 |
| --- | --- | --- |
| Check | `check:93d19ebab910b1e9c6b2b4ce4a7607b45676d91310e4f42154abae0b19d89bca` | `check:b87d601270e68967030b9aca4dd1d2819d5612ea18c40898ce936457451371c2` |
| 完整Review | `full-review:1a586edf818bd7d4187f82ec5088cec41d74b4749da6317bab6d67994fc2ebd1` | `full-review:208addf409fa0005139cc8bdc8786686aa9454dd6ad65f58d1d89a7d806057ab` |
| 实际独立职责 | 按旧合同另用fresh Phase2 worker及fresh committed reviewer，完整范围16文件 | 原独立reviewer接续真实原完整覆盖、所有Hr..M差额、两侧语义和未改consumers，形成完整当前B..M结论 |
| 工程命令 | Phase2因原工具链适用依据不足，补跑6/4/4及discover14与hygiene，6命令约0.1643s；committed reviewer核当前环境/代码后采用这些新事实，未再重跑tests | 当前Phase2和Branch均核原定义、输入、依赖、Python路径/版本、参数和预期后采用原事实，业务测试重跑0；另核完整范围diff |
| 成功正式命令 | Phase2 Architecture 0.425s，Check record/check/invoke约2.505s；committed Architecture及Branch四步合计约2.319s | Phase2 Architecture 0.464211s，Check三步2.500378s；committed Architecture及Branch四步2.242986s |

old Phase2首个实采clock为00:01:01 UTC，Check于00:05:35.324完成；首标记前已有读取，不能将两者差值冒充完整语义耗时。old Branch于00:06:39开始，00:08:48完成首轮独立判断与检查集，Branch/工程输入于00:13:24到达、Architecture输入于00:15:04到达，00:16:18正式通过。输入转交包含父协调延迟，单列为协调等待，不算旧合同必然成本。

new post-M assignment于23:59:01 UTC开始核owner边界，Phase2 Architecture于次日00:02:17.442026完成、Check于00:03:06.207905完成；投影于00:04:42.432594完成、Branch Architecture于00:04:57.409321完成、正式Branch于00:05:14.031533完成。该轮没有单独采集各阶段语义起点，不能倒推纯语义时长；00:03:27只是Branch准备期间观察点。以上时间锚包括读序、编写、接口核查与协调，不用于旧新速度比例。旧Phase2两次schema authoring错误、新Phase2一次遗漏input字段及一次不存在的wrapper路径、builder一次本地缩进错误均属执行者错误，未计为合同必要成本或优化收益。

两侧最终Planning/Check/full_review均对各自M适用，Readiness仍missing。Branch wrapper均实际退休自己的checkpoint，未手删、跨读或重建；后续只读公开结果与精确Git对象。仅public API的Task元数据dirty，不产生证明提交。真实减少的动作是新侧无需另启reviewer重建已有理解、完整当前覆盖仍成立；不能把两侧因证据或执行者差异而产生的重跑/等待全部归因于合同变化。本样本未执行远端发布、Readiness或Task Completion。

## 实际工程证据缺项与补齐

另建独立普通临时clone，固定在new F，业务实现和R1..R5保持不变。开始前定义V1 policy、V2 checkout及新V3发票矩阵。独立owner先读完整要求、实现、两个consumer及检查定义，确认新矩阵只覆盖既有R1/R2/R5：15个service/net组合和9个discount/service组合，核两条发票明细与checkout总额。V3交接时确实尚未执行；旧invoice四项或旧Check不能代替这项新检查。

owner先实际补V3，2项/24组合、exit0、0.041989s。原V1/V2的输入、定义和预期可核；原执行者也从真实工具代码核实了cwd及继承环境的调用方式，但没有当时解释器解析/版本的单独记录。owner没有因为缺固定字段直接判错；在过去工具链适用性仍无法核实后，定向补V1/V2：6项/4项，均exit0，0.039555s/0.032784s。闭合时采用本轮已亲自执行且当前环境/对象可核的V3，没有重复V3。原历史成功结果与日志保持不变，未改成失败或补造过去环境。

本例实际新执行三条命令，合计0.114328s，不宣称只补一条。初始读取/判断窗口67s；后续来源核查含跨Agent等待，未单独精确计时，不包装成纯语义耗时。没有Task绑定或正式gate，不证明丢失日志恢复、旧合同必然重复成本或main Check通过。它证明当前工程证据不足时不能继承pass，并在补齐缺项时保留已适用的其它事实。

## 实际 Check finding、修复与完整当前 Review

新 matching 样本另经原公开 rework 回到 implementing。原 writer 在同一 policy 中将 `net_cents >= 5000` 改为 `net_cents > 5000`，构成受控的普通实现错误；requirements、design、既有 tests 和两个 adapters 均未改。原 API 绑定实际坏候选到 checking，固定 B、HEAD M、同 Delivery 和 Planning 保留。该错误没有提交。

同一独立 owner 读取实际差额、完整规则及两个未改 consumer，选择三个既有独立入口。policy 6 项中失败 2 项、checkout 4 项中失败 1 项、invoice 4 项中失败 2 项，实际耗时分别为 0.042613s、0.032284s、0.032140s。`quote(5000)` 以及两个 adapters 的 `(5500, 500)` 均错误收取 600 运费、总计 5600，违反 R2/AC1 的免运费和总计 5000 要求。原 normal/solution 正式 qualification 均为 `qualified_current`，eligible-root 为 `not_incident_applicable`；原 Check 正式返回 `implementation_required`，finding 为 `F-SHIPPING-5000-INCLUSIVE`，API 合法退回 implementing。当前 Architecture 的 `baseline_current/no_change` 只证明职责边界未变，没有遮盖功能失败。

原 writer 只恢复 `>= 5000`，policy 字节恢复为 M 原内容；没有修改 authority、tests 或 adapters。原 API 重新绑定 checking。同一独立 owner 亲自核修正与受影响的两个 consumer，并实际执行同输入、同断言的三个入口：6/4/4 项全部成功，耗时 0.035765s、0.032979s、0.033533s。原失败观察消失，没有转移或修改断言。owner 闭合 finding 后完成当前完整九维 Check，正式结果为 `check:52a6fa3e643cfe6f851c0f5ecd8c67ddb5adfdf9ed1ad03144e305dc168deff8`。当前无缺陷候选，按原合同记录空分类，不制造空 qualification。

原 TaskCommit 的 clean committed re-entry 实际返回 `committed`，耗时 0.767614s，绑定上述新 Check 与既有 M，零新增提交。原独立 owner 随后完成当前 committed Architecture 及完整 B..M Branch Review。正式结果为 `full-review:e86cdeae41390bdb996f2eb74849c4276fd99fd127c5654fde6baebe56d2235f`，predecessor 精确为上述新 Check；Planning、Check、full_review 均 applicable，Readiness missing。Branch 采用本人修复后实际正向事实，没有再跑业务测试。原 wrapper 自行退休 gate 与对应目录；没有手删、跨读或重建私有 checkpoint。

坏候选检查的观察窗口为 00:37:55–00:41:40.179467 UTC；修复复核窗口为 00:45:15–00:46:45.155867 UTC。坏候选 Architecture 正式调用 0.498195s，三项 qualification 分别 0.366673s、0.409119s、0.410603s，Check record/check/invoke 分别 1.104612s、0.598667s、0.539983s。修复后 Check 三步分别 1.212814s、0.592919s、1.239756s。Branch 准备观察点为 00:47:11 UTC，正式完成于 00:50:50.612347 UTC；其 Architecture 正式调用 0.472323s，Branch 三步分别 0.791537s、0.383274s、0.624441s。这些窗口包含读取、编写、接口核验和协调等待，不当作纯语义耗时；本例无远端等待，不计算旧新速度比例。

三入口的负向、正向命令事实均有实际 argv、时间、结果和输出，但当轮未单独采解释器解析/版本快照。后续该 Agent 环境实查解析到 Framework Python 3.12.8；不据此补写历史版本，也不把父 Agent 当前 PATH 推广到这些调用。实际检错与闭合由比较符、未改输入/断言/consumer 及真实负正执行支持。本例证明真实 Check finding → qualification → 原 writer 修复 → 当前完整 Check → 当前完整 Branch Review；finding 始于 Check，未伪称 Branch-origin finding，也未制造不存在的 finding/fix commit anchors。它不替代前述共享 Runtime 样本或 main 的最终门禁。

## 开发 Task 的 matching 切换与实际原生入口

原`guru-upgrade-tools`从干净完整H source消费原冻结plan，一次执行返回`tools_upgraded`，installed_version=`0.7.0-guru.5`。CLI/Core实际为0.7.0-castbox.5，使用`local_candidate`；正式输出明确`unverified=[formal_fork_source_lock]`，不称正式源锁或Release通过。原public/Guru installer生成受管结果，没有手填manifest、改Task或以源码读取冒充目标运行。

本次切换前后，当前Task所有公共文件、当前session目录、workspace、未提交贡献内容、用户`.trellis/config.yaml`、common Python pointer及HEAD均一致（38个实际文件/状态项）。目标自身installed package validator返回`passed/errors=[]`，40 packages/124 commands，Claude/Codex/Cursor选择一致，conflicts与sidecars均为0。原dogfood drift命令返回exit0，canonical workflow、受管spec与三平台实际投影匹配。

目标自身原生`get_context.py --json`实际返回当前session来源、准确TaskId/generation、唯一checkout、原DeliveryKey及`implementing`，Planning仍适用，Check/full_review/readiness尚未生成。原`--mode continuation`及Phase Index也已实际输出matching workflow合同。该结果证明在途原生入口保留，不是另造binding或将旧pass转成新pass。

另以同一完整H source及原managed Python3.12.8执行普通全仓库preset reapply，实际在写前返回`upstream_delivery_migration_required`，涉及228个历史legacy archive；与先前固定B完整source普通apply的既有边界一致。该次不计成功，不删除、转换或迁移归档来绕过；前后上述38项继续保持。新clean样本上的完整reapply/在途保全已有真实成功证据，但含这些legacy archives的普通全仓库reapply没有通过。原matching tools-only安装、目标native与dogfood drift已通过，不能用它们替代这个单独入口的失败结果，也不为本Issue扩入历史Task迁移。

## 原实施观察截止点与未验证边界

以下段落保留正式最终门禁及 PR #644 合并之前的原观察。“尚待／未完成”只描述当时状态；较晚正式结果由下一节承接。该后序引用不改变本段的原命令、失败、未知或其余未证边界。

canonical实现已形成早期候选，尚待main完整质量门禁。新候选clean安装及其reapply、本Task真实Draft反馈、两套样本首次完整审核、共享Runtime检错/闭合、文档冲突解决稿与实际整合提交及其最终正式当前Check/Review、真实Check finding至修复后完整当前Check/Branch Review、工程缺证据补齐、开发Task matching tools切换/目标native/三平台dogfood drift已经执行，实际计时与测量缺口如上。含legacy archives的普通全仓库reapply仍阻塞，formal_fork_source_lock未验证。main完整当前Check/独立committed Review与#636最终同PR组合仍未完成。本轮RDT/Architecture共享定义已分别晋升至current-main-0.7.0-guru.114/.105；原独立Phase2评估及原owner实际写入适用性由各自真实公开结果承接，本Test不替代它们或后续最终Check。#638未来接口、业务采用/生产效果、完整Release与多平台升级矩阵不由此证明。

## 后序正式结果引用（#649 有限核实）

2026-10-21 核实原 [归档公共 Task](../../../.trellis/tasks/archive/2026-10/10-20-637-candidate-review-reuse/task.json) 的 Delivery `5499bb2d-86d7-4a5c-9747-9b06e00f4ef9` 已为 delivered。其正式结果为 Check `check:50ac1fb9eea8a61e18bfd5b4f5052ebe2e764ec80ee92136e271ab77aadd5d6b`、full_review `full-review:81b66dcf3388ef2edca121d63c5cec22faa46fc7a514739bbdd827fae1e1c0a0`、readiness `readiness:b92f49efb49a6f513002df6530799a76099f8a91b255d5846968606e5c9ebeff`、Delivery `delivery:3a38020b456112fd329e9a6616e4222e589dea12`，以及 Task Completion `completion:3356b089-5f91-473d-8b39-12fbcdb45451`。这些引用说明后序正式门禁已发生，不声称本次重新执行。

live [PR #644](https://github.com/castbox/guru-trellis/pull/644) 为 MERGED，head 为 `0aae5dda625278948d646a6d2027eb7785de93b6`，merge 为 `3a38020b456112fd329e9a6616e4222e589dea12`，mergedAt 为 `2026-10-20T02:06:55Z`。实际祖先检查证明该 merge 可达 #649 固定 main 基线 `319202beab79c7666ecdb855291bf117e43d407e`。原“main 完整当前 Check／独立 committed Review 尚未完成”不再作为当前否定声明。

本次只修上述状态、截止点和引用。含 legacy archives 的普通全仓库 reapply 阻塞、formal_fork_source_lock、原观察时 #636 最终同 PR 组合、当时未来的 #638 接口、业务采用／生产效果以及完整 Release／多平台升级矩阵，均未由本次引用取得新的通过证明。
