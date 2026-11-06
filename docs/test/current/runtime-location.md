# Runtime与Git来源验证

导航别名：`R718/D718/T718`；`runtime与Git来源`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/test/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：`RDT-TST-RUNTIME-LOCATION`；状态：current。本单元定义[Requirement](../../requirements/current/runtime-location.md)与[Design](../../design/current/runtime-location.md)的验证责任；实际观察按明确候选与层次记录，不把知识接受或命令绿色当整体完成。

## 测试策略与可观察结果

| Test / Scenario | 需求→设计 | 实际入口、输入和预期观察 |
| --- | --- | --- |
| T718-01 / S718-ARBITRARY | R718-01/02/06→D718-01/02 | 原bootstrap形成隔离有效cache；普通Git/外部预建linked、无自动pointer、无Task，运行实际installed wrapper。观察目标代码成功、相同需求同物理venv、无新增venv/Task；位置删除后环境仍可复用。 |
| T718-02 / S718-STABLE | R718-02/04→D718-01/02 | 多合法cache、PATH改变、不同需求分支及切回、显式兼容类别；观察有效hint保持、显式失配拒绝、patch/path复用与不同类别并存；初始化默认PATH与显式--python分别执行。 |
| T718-03 / S718-RECOVERY | R718-03/05→D718-03 | 由原安装/维护路径在owned cache形成缺失/损坏/旧hint；公开check/repair及原wrapper重试。观察具体诊断和最终目标结果；缺seed/锁来源准确拒绝，失败保留此前可用环境/选择。 |
| T718-04 / S718-READ | R718-07/09/10→D718-04/05 | 外部worktree、无Task、有未提交/untracked草案，明确Git对象且base未检出或其位置dirty；经原read→Discovery→Clarify/Wording/Readiness公开链到声明结果。观察固定tree内容和候选分别绑定，无隐式ff/commit/push。底层git show或手写上游pass不能证明本链。 |
| T718-05 / S718-REJECT | R718-08/10→D718-04/05 | 原Sync对dirty/不可ff目标、错误base、普通候选漂移；正式阶段缺Task/提交/远端事实。观察必要拒绝、原入口纠正/刷新；只读通过不产生正式gate。 |
| T718-06 / S718-MAINTAIN | R718-03/11→D718-03/06 | 旧目标dispatcher不可运行，matching source-loaded维护和原rollback；运行目标自身resolver/installed/native。观察工具与选择兼容、Task/session/用户内容/非目标工具和选择bytes保持，peer实际解析值保持。 |
| T718-07 / S718-DISTRIBUTE | R718-01/11→D718-07 | 命中runtime/package/tests、代表性clean安装至多1个、同样本reapply、canonical/dogfood/installed/声明平台投影、mode、drift/sidecar。观察真实wrapper与机械一致性分别成立；不跑完整Release矩阵。 |
| T718-08 / S718-AGENT | R718-07/09/10→D718-05/07 | 实际Agent读取新workflow/公开合同，使用真实草案和固定来源调用原consumer到声明结果。记录实际决策、入口和终点；文本/schema/分发测试不代替此观察。 |

fixtures只建立受测边界之前的合法状态，外部GitHub provider可隔离；不得代生产者生成结果、补偿错误输出、手写Task/gate或发布产品Issue。逐项保留原失败和正确正向/必要拒绝，确认失败没有转移到下游。相同观察共享证据，不展开无独立缺陷检测价值的排列。

## 实际观察边界

修复前观察基线为main `610a810d45bb30173906d55c77709389adf1cf31`。隔离仓库包含该版本完整installed资产；原installed bootstrap以checkout-local方式成功构建隔离cache。普通git worktree add后，同一installed guru-select-workflow-mode wrapper返回runtime_not_bootstrapped/退出2，primary真实wrapper可运行。没有删改pointer/cache或复制venv。该观察支持原入口定位耦合，不能推断旧cache删除原因。

下列观察来自各次实际执行的本批未提交候选或其隔离安装，区分源码、目标安装与实际Agent行为。这些事实不能替代最终完整候选的正式Check/Review：

| 观察 | 实际入口与结果 | 边界 |
| --- | --- | --- |
| T718-01/02/03 | runtime/tests/test_runtime_selection.py及原更新/维护/有效pointer suites；真实3.12/3.14、普通linked、两类cache、分支需求切回、PATH/hint稳定、旧610a公开producer→新格式→原旧reader、公开check/repair和缺seed/lock均已运行通过 | 同一受管需求的物理复用、合法不同类别并存与patch/path identity分别核验；没有业务仓现场依赖 |
| T718-01/05 / 业务argv | 原manage-python seed扫描在--处停止；新增test_public_resolver_preserves_business_python_arguments单例通过。同一保留SOURCE/TARGET的原resolver均精确保留--python application-value和--python=another-application-value | 修复前新入口越过--误把业务参数当seed，旧入口同输入可保留；修复后仍验证分隔符前的环境owner显式--python生效，未弱化原显式选择 |
| T718-04/05 | 原Sync20、Discovery18、Clarify27、Wording32、Readiness26、CreateIssue16、CreateTask25，共164项通过；其中五个新真实read-chain场景走到Readiness ready及原Issue创建计划ready | 草案/两个checkout的dirty保留，无ff/commit/push；固定tree实际blob读取、Clarify回程、真实consumer schema与普通草案漂移拒绝已核；外部GitHub provider隔离，不发布产品Issue |
| T718-05 | 同一真实checkout的公开check→validate-active另一合法cache→check对照：修复前错误接受另一ID；修复后wrong-ID exit2/managed_runtime_missing、correct-ID通过，前后真实选择及新旧文件bytes不变 | 对应原公开expected-ID语义，未删除另一合法cache或取消正常发现 |
| T718-06 | 真实718 checkout新canonical resolve写selection-v3.json后，旧active.json bytes保持，原installed checkout guard status=ok；原tools rollback5项与upgrade-installation34项通过 | 这是单元与同位置新旧入口共存证据；实际维护与回滚见后两行 |
| T718-06 / A7维护 | 隔离linked旧目标入口不可运行；matching source-loaded原tools owner实际返回tools_upgraded。写后目标自身公开--check、installed validator（43 active packages/128 commands）与get_context均成功 | primary peer整树，以及目标Task/session/草案的bytes与mode保持；来源执行没有冒充目标自身成功 |
| T718-06 / A7回滚 | 在合法旧primary安装上，原tools owner实际返回tools_upgraded，再由同操作原rollback返回rolled_back。legacy原文与mode恢复，原不存在的selection-v3.json被移除，旧native smoke成功 | 已更新linked peer整树、其合法共享环境选择及Task/session保持；结果为local_candidate，formal_fork_source_lock仍unverified，不是Release |
| T718-07 | source package validator通过43 active packages/128 commands；命中Python内存compile、JSON、Bash语法和diff检查通过 | 实际维护、dogfood、focused与Agent观察见各自对应行 |
| T718-07 / A8 dogfood | 真实718 checkout经原source-loaded tools invoke返回tools_upgraded，最后runtime差额也通过同一owner更新。目标自身公开--check确认合法共享环境，installed resolver完整保留业务--python与--python=参数；installed validator通过43 active packages/128 commands，sidecars为0。get_context --json识别原TaskKey/DeliveryKey、implementing及适用Planning；check-dogfood-overlay-drift.sh退出0 | Task的13个文件bytes与mode保持；shared及Claude/Codex/Cursor投影、spec和workflow与canonical一致。未将这些安装事实表述为formal_fork_source_lock或Release通过 |
| T718-07 / A8代表安装 | 保留同一隔离TARGET，经原installer用当前完整source reapply返回ok，Python环境action=reused；source/installed validators通过，49个runtime文件和2747个skills文件逐字节一致 | 4个已知managed .bak经原manifest hash核对后消费；不是另起样本或完整多平台安装矩阵 |
| T718-07 / eval fixture | 原standalone clear/refresh public输入在recorder前形成Issue145、实际mode、standalone_review和guru-standalone-caller；定向test_clarity_six_exits_use_recorder_authoring通过六种recorder/check出口及两种standalone public invoke。同TARGET source与installed的clear-route报告均为passed，两个transcript的实际stdout均为exit_id=clear、resume_target=guru-standalone-caller | 修正原fixture producer，不改产品validator，不补偿已record结果；这是确定性fixture结果，实际Agent行为另见V8 |
| T718-07 / adapter入口 | source/installed与shared/Codex/Claude/Cursor组成的8个直接adapter入口，在PATH没有Python且清空PYTHONPATH时均到达预期请求诊断execution_error / adapter request-context invalid | 证明adapter从自身位置到达声明的协议边界；未调用真实模型，不把请求拒绝当作业务审核成功 |
| T718-07 / focused最终断言 | 复用同一SOURCE/TARGET和原最终断言体，结果status=ok；source、installed、target-wrapper-source三项validator按原顺序通过。SOURCE仅bootstrap时extension诊断为missing；TARGET installed状态ok，版本0.7.0-guru.7与canonical一致 | reapply为ok/reused，共享环境identity保持；49个runtime与2747个skills文件逐字节一致。该结果不表示从首次启动起脚本一次全绿，早期失败和恢复截止点见后文 |
| T718-08 / V8 | 实际Agent从目标安装的公共入口选择operation=read，依次取得baseline_ready、context_ready、clear、pass、ready；各阶段均先完成本人语义审核，再执行原record/check/invoke | 独立standalone草案审核；不声称workflow初始selector、正式Task/Branch Review、创建或发布通过。外部GitHub provider为合成替身 |

固定B的registry已有43 active packages，而原test_runtime.py仍断言38；本批实际同样报告该既存失败。原SharedRuntimeTests其余27项在matching upstream依赖下通过；该历史常量断言不作为本项通过证据，实际inventory由current registry/Interface与package validator完整核对。未将缺依赖或旧断言失败泛称绿色。

A7首次primary样本在调用上下文未带原隔离cache时执行旧native失败。该轮虽完成exact restore，formal结果先为resume_required，后为blocked，不能记作成功回滚。后续通过独立环境维护恢复合法旧安装，再建立上表的fresh回滚对照；新结果没有覆盖或改写原失败事实。

V8采用的固定树为fixture commit `b337e081722417acd6eb7410e6b5292ae366fd4a`，它由归档副本产生，不是上述修复前main提交。Agent通过目标安装的read-change-context-source读取该树的README、同步执行器和readiness runtime测试；从20个历史候选中选择并深读#184 PRD，只复用目标与工具来源分离的原则。未跟踪草案独立要求将来新增V8-READING.md的用途、来源、边界三章。Clarify没有编造提问或回答；Wording在完整title/body扫描后完成六项语义检查；Readiness独立完成十维审核。最终main与external-review refs未推进，草案原文保持，V8-READING.md仍不存在。没有执行Issue、Task、commit、push或发布动作。该实际Agent观察与确定性read-chain测试分开成立。

原qualification eval fixture把新环境选择文件误判为业务residue；同轮adapter还存在安装后kernel定位和standalone owner context不匹配。它们属于测试执行边界的普通缺陷，不说明产品门禁应放宽。原owner已直接修正residue分类、adapter自身位置解析与recorder前context构造；同TARGET reapply后的source/installed实际clear-route和入口复验见上表，原before报告保留。

Focused早期末段汇总脚本按平面对象读取现有公共diagnostic envelope，触发KeyError。该次SOURCE仅有bootstrap，extension status=missing是正确诊断。原owner改为消费diagnostic.result，分别核SOURCE missing、TARGET installed ok及canonical版本后，复用保留样本完成原最终断言，得到上表status=ok；没有重写早期报告或另起样本宣称首次全绿。

刷新时曾额外同时启动三项validator，其中installed与target-wrapper-source共用TARGET选择器；该次target-wrapper-source返回runtime_dependency_missing且runtime identity为null。随后独立重跑及原脚本顺序逐项均通过，原最终断言也通过。额外重叠执行的该次拒绝保留为观察，不表述为全部尝试通过；本项不扩展为并发竞态机制或额外required测试。

最后runtime差额后的真实718 dogfood原owner更新与目标自身读回已完成，观察见上表。下一阶段仍须对最终完整候选执行正式Check/Review；本单元不预写该阶段结论，也不代替Task Completion。完整Release矩阵与业务采用由其原owners另行验证。

## PR719首次CI后的观察修订

上述完整策略、早期失败和当时的阶段边界保留原六目标晋升提交`c65f2571f8269c04819cce42e3f0f20f8c64178d`的观察截止。以下为同一Delivery的后继Test观察，完整需求、设计条件和原覆盖边界继续适用。

| 观察 | 实际入口与结果 | 覆盖边界 |
| --- | --- | --- |
| T718-07 / 首次远端CI | PR719的[run 41468760261](https://github.com/castbox/guru-trellis/actions/runs/41468760261)在Ubuntu、macOS、Windows三端均failed，候选为c65提交；B=`610a810d45bb30173906d55c77709389adf1cf31`的[run 41401016503](https://github.com/castbox/guru-trellis/actions/runs/41401016503)三端均success | 原候选的首次失败保持。B结果只证明该固定B运行，不证明修复候选的三平台结果或Release |
| T718-07 / CI installed collector | Ubuntu/macOS的安装步骤已经成功，随后installed-wrapper collector在调用case前读取旧flat pointer字段runtime_id，产生KeyError；报告calls为空。Windows该轮没有installed-wrapper报告 | 安装成功与collector失败分别成立；不得把Windows缺报告同化为相同KeyError或相同case结果 |
| T718-07 / 公开resolver消费 | CI collector改用报告中的diagnostic Python调用目标实际bootstrap.py的公开--resolve-active --json，并薄投影runtime_identity到原active_runtime.runtime_id。真实旧B目标与当前installed目标均collector completed、fixture passed，原两case实际返回0/2；原报告保留 | 两目标均执行自己的installed wrapper，原预期和参数保持；没有读取新选择文件布局、fallback或新API。该本地对照不替代远端三平台重跑 |
| T718-07 / CI driver回归 | 当前修订的ci/test_targeted_ci.py全11项通过，包含公开resolver消费及原wrapper结果保留；原观察器4项定向检查也通过 | 证明driver及fixture消费者的命中行为，不能据此宣称全部runtime或原三平台CI已通过 |
| T718-01/07 / Linux locale对照 | 使用H archive，在真实python:3.12-bookworm Linux容器内按hash lock安装依赖，并以PYTHONUTF8=0运行原Unicode wrapper用例。仅删除manage-python.sh中的LC_ALL=C强制设置前，status=1、stdout为空且stderr为runtime_dependency_missing/jsonschema；同输入删除后status=0，原用例通过 | 原日志保留两次结果。该对照支持强制locale与此入口失败的因果关系；没有另行probe内部受管解释器，不能把外层jsonschema诊断写成实际缺包，也不等同Ubuntu CI通过 |
| T718-01/07 / Windows执行机制 | Windows分支由原exec替换改为等待受管子进程并传回其退出状态；macOS上的四项定向自检通过 | 这是分支、stdin/stdout及退出状态的机制验证，尚不是实际Windows runner通过；原Windows CI待修复候选重跑 |
| T718-07 / 本轮dogfood | 原source-loaded工具更新返回tools_upgraded 0.7.0-guru.7。目标自身公开--check为ok，get_context原native退出0并识别718；installed validator通过43 active packages/128 commands，sidecars=0、conflicts=0。原drift脚本退出0，shared及Claude/Codex/Cursor、spec/workflow与canonical一致，bootstrap/manage字节一致 | Task元数据bytes保持；这些是目标本次安装与读回结果，不是formal_fork_source_lock、三平台CI或Release通过 |

当前截止：修复后的原三平台CI尚待执行。原报告、Linux对照及本地机制结果保留各自对象和环境边界；后继完整候选的Check、晋升、Review、Publication与Task Completion继续由原owner消费实际结果，本单元不预写其结论。
