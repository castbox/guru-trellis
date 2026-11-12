# Runtime与Git来源验证

导航别名：`R718/D718/T718`；`R760/D760/T760`；`worktree配置路径`；`runtime与Git来源`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。`R718/D718/T718` 与 `runtime与Git来源` 别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/test/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：`RDT-TST-RUNTIME-LOCATION`；状态：current。本单元定义[Requirement](../../requirements/current/runtime-location.md)与[Design](../../design/current/runtime-location.md)的验证责任；实际观察按明确候选与层次记录，不把知识接受或命令绿色当整体完成。

本单元 RDT 定义修订：`fixed-git-task-creation-813`。来源为[Issue #813](https://github.com/castbox/guru-trellis/issues/813)，适用 before 为 Git `5c6a4591db7165ece045e6b0eb789c21d06d7d38`。本次细化原 R718 固定来源贯通 Creation 的定义，保留稳定身份、#760/#769 条件和历史观察截止。该标识不是软件版本或最终 Git HEAD；独立 committed Review、Delivery 和 Completion 由其原 owner 建立。

## 测试策略与可观察结果

| Test / Scenario | 需求→设计 | 实际入口、输入和预期观察 |
| --- | --- | --- |
| T718-01 / S718-ARBITRARY | R718-01/02/06→D718-01/02 | 原bootstrap形成隔离有效cache；普通Git/外部预建linked、无自动pointer、无Task，运行实际installed wrapper。观察目标代码成功、相同需求同物理venv、无新增venv/Task；位置删除后环境仍可复用。 |
| T718-02 / S718-STABLE | R718-02/04→D718-01/02 | 多合法cache、PATH改变、不同需求分支及切回、显式兼容类别；观察有效hint保持、显式失配拒绝、patch/path复用与不同类别并存；初始化默认PATH与显式--python分别执行。 |
| T718-03 / S718-RECOVERY | R718-03/05→D718-03 | 由原安装/维护路径在owned cache形成缺失/损坏/旧hint；公开check/repair及原wrapper重试。观察具体诊断和最终目标结果；缺seed/锁来源准确拒绝，失败保留此前可用环境/选择。 |
| T718-04 / S718-READ | R718-07/09/10→D718-04/05 | 外部 worktree、无 Task、有未提交草案；明确对象较 primary main 新且 primary 有 staged/unstaged 工作，经原 read→Discovery→Clarify→Wording→Readiness→Creation 公开链创建。核 exact HEAD、唯一 Task/generation/binding，前后比较 primary refs/index/workfiles；原 check/recover 返回同一结果且不增资源。底层 git show 或手写上游 pass 不能证明本链。 |
| T718-05 / S718-REJECT | R718-08/10/11→D718-04/05 | 原 Sync dirty/不可 ff 拒绝保持；Creation 错对象、非 commit、source/acquisition/common-dir 普通装配失配均给字段诊断。synced 新建 stale 拒绝、原结果在 branch 正常前进后仍恢复；采用既有 Task/generation/binding/session 冲突和缺 context 回归。当前入口拒旧输入，旧 provider 恢复旧成功结果；正式阶段仍核 Task/提交/远端事实。 |
| T718-06 / S718-MAINTAIN | R718-03/11→D718-03/06 | 旧目标dispatcher不可运行，matching source-loaded维护和原rollback；运行目标自身resolver/installed/native。观察工具与选择兼容、Task/session/用户内容/非目标工具和选择bytes保持，peer实际解析值保持。 |
| T718-07 / S718-DISTRIBUTE | R718-01/11→D718-07 | 命中 runtime/package/tests、代表性 clean 安装至多 1 个、原 owner 对已安装目标 reapply、canonical/dogfood/installed/声明平台、mode、drift/sidecar。分别核真实 wrapper、原 Task/session/config 保持与机械一致性；记录样本是否保留，不以新样本冒充同样本复验，不跑完整 Release 矩阵。 |
| T718-08 / S718-AGENT | R718-07/09/10→D718-05/07 | 实际 Agent 完整读取采用 provider 的公开合同，亲自完成原 owner 判断与 record/check/invoke，使用独立 draft 和固定来源走到 Creation 及原恢复结果。独立核 primary 保存、精确起点与身份/资源不重复；确定性 fixture、结构/分发与实际 Agent 观察分别报告。 |

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

## worktree 配置路径的验证责任（#760）

承接 R760-01—05 / D760-01—03；适用实现基线
`8c158381b5bdb61fd961cbb89e23c2d1f659c9aa`。原 T718 策略、全部失败及后继观察保持各自
截止点，不因本项新建修复扩大为已验证事实。

| Test / Scenario | 需求→设计 | 入口、输入及独立观察 |
| --- | --- | --- |
| T760-01 / S760-ROOT | R760-01→D760-01 | 真实Git fixture解析空/相对/绝对root，代表性primary、linked、detached调用得到同一项目root；外置gitdir可确证时正确锚定，不可确证时明确诊断。正常空模板与非空配置冲突分别观察，不做全组合矩阵。 |
| T760-02 / S760-TASK | R760-02/03→D760-02 | 正式create-task公开入口消费configured，真实Git创建后比较计划、实际目录、注册及原后继binding。正常错误计划在首副作用前拒绝，修正后成功；不得仅调用private helper证明创建链。 |
| T760-03 / S760-TASK-FREE | R760-02/03/04→D760-02/03 | 公开环境预检生成目标→原task-free普通Git创建→直接后继位置读回，观察无Task身份。复用仍适用显式新位置、外部采用、恢复回归，补配置变化不重定位差额，保留原clean/identity/位置资格检查。 |
| T760-04 / S760-DISTRIBUTE | R760-05→D760-03 | 命中runtime/package tests、source/installed validators；原tools owner同步canonical/dogfood/声明平台，drift、sidecar和JSON/Bash/内存compile/diff检查。源码、安装与Agent行为分别记录，不跑完整Release矩阵。 |

### 本次观察截止与未验证边界

以下为本次未提交实现候选的本地观察，由原 runtime owner 实际执行并报告。
命令使用本 checkout 的 `trellis/skills/guru-team/runtime/resolve-python.sh .
trellis/skills/guru-team/runtime` 选定受管 Python；需要 Fork 的 suite 通过
`GURU_UPSTREAM_DELIVERY_SCRIPTS` 指向本次固定 source-lock 对应的真实 Fork scripts。
本表保留 suite 与最终定向复验的先后边界，不把局部重跑写成全套再次执行。

| 观察 | 实际入口与结果 | 覆盖边界 |
| --- | --- | --- |
| T760-02/03 / 正式 Task | 受管 Python `-m unittest discover -s trellis/skills/guru-team/packages/guru-create-task/tests -p test_contract.py -v`：26项通过，73.742s。当时 `_plan` 集中调整后，新增场景单独复验1项通过，4.467s | 公开configured错计划拒绝且refs/worktrees不变，纠正后真实Git创建、Ensure读回原binding；修改配置后公开recover返回原结果且Task字节/位置保持。最终单例还观察record-task-plan在创建前拒错。原省略字段绝对路径、external adopt与恢复回归仍适用；外部GitHub provider隔离。 |
| T760-01/03 / 路径与 task-free | 受管 Python `-m unittest discover -s trellis/skills/guru-team/packages/guru-select-workflow-mode/tests -p 'test_*.py' -v`：21项通过，11.386s；该阶段 `test_worktree_paths.py` 单独3项通过，3.376s | 空/相对/绝对root、primary与detached linked一致，linked空模板和非空冲突，separate-git-dir primary可确证、linked缺core.worktree拒绝、有core时核真。公开check-env错计划拒绝且refs/worktrees保持，正确result目标经普通Git创建，再读实际toplevel/注册/无Task身份。只有GitHub外部facts使用stub，topology/config/Git真实；不声称实际Agent执行完整语义链。 |
| T760-04 / source机械检查 | `PYTHONPATH=trellis/skills/guru-team` 下受管 Python `-m runtime.validate --root . --mode source --json`通过，43 active packages / 128 commands；changed Python内存compile、JSON解析及 `git diff --check`通过 | 源码/声明/语法层证据。修复版目标工具、installed及drift观察见后续行，不以source通过代替安装成功。 |
| T760-01/02/03 / 最终定位范围与创建复验 | `_primary_root` 只读已确证primary、必要core.worktree或待核primary候选，不逐项探测无关peer。原受管入口执行 `test_worktree_paths.py` 4项通过（2.611s）；configured公开创建/Ensure/改配置恢复单例1项通过（3.946s） | 新增真实3个peers的读取范围断言；同一现场单次解析保持primary/root不变，inspect 2次、Git 8次、0.124s。耗时只说明该次样本。前述26/21 suite其余事实按未变consumer及合同继续适用，不能把最终4/1重跑写成全部suite再次执行。 |
| T760-04 / 修复版实际工具投影 | 原 `guru-upgrade-tools` 返回 `tools_upgraded`，installed_version=`0.7.0-guru.8`；目标自身installed validator通过43 active packages / 128 commands，conflicts=0、sidecars=0。`check-dogfood-overlay-drift.sh --repo .`退出0，所选Claude/Codex/Cursor投影一致；目标installed check-env读回正确primary_root、primary配置worktree_config_path、同级guru-trellis-worktrees根及760-validation目标 | 最后定位差额经原tools owner再次实际更新后验证；结果为local_candidate，formal_fork_source_lock仍unverified。首次并行drift调用返回runtime_dependency_missing，未进入drift判断；随后显式--repo .的实际成功独立成立。没有运行完整多平台升级/Release矩阵。 |

这些行为与分发观察不能替代其原owner的正式阶段结果，也不代表最终Check/Review或Task Completion通过。
后续按原owner实际结果承接，不把 #718 的历史通过替代 #760 的配置创建验证。

定向真实Git测试可证明其入口和后继观察，不能自动证明完整真实Agent业务链或生产效果。
不要求业务#1232重新复现、不触发Codex清理、不运行业务恢复或完整多平台安装/升级/Release。
本单元写回不代表Task Completion、Architecture晋升或发布；这些结果分别由原owner消费。

## T769 / peer增长与冻结源恢复验证

承接R769-01—03 / D769。T769-01用真实Git topology和原peer_pointers入口观察新增独立peer、原值保持及peer文件不被写入；原peer合法选择变化和实际不隔离继续拒绝。T769-02用原owner正常创建的schema1.0事务执行新公共profile，观察resume/rollback阶段、preset pending/complete不重复安装、retry保持action/ref及原source/plan/preimages不变；unit外部隔离只证明该层。T769-03实际#766原操作从交付修复源恢复，核同public operation及目标own resolver/installed/native。T769-04定向package/source/installed/drift/sidecar/mode验证，不承担完整多平台矩阵。

### #769 当前本地观察

| 观察 | 实际结果与层次 | 边界 |
| --- | --- | --- |
| T769-01 / peer | 最终test_peer_growth.py 3项通过，1.590s；真实Git新增peer、原pointer变化拒绝、parent alias下缺失leaf、leaf symlink及hardlink隔离均经原检查入口 | fixture建立reader边界前的pointer状态；不声称完整环境选择或并发压力证明。 |
| T769-02 / 冻结源 | test_frozen_recovery.py最终8项通过，12.576s；原完整Git资产源、原owner begin/checkpoint/preimages与阶段真实，覆盖pending preset、public pending、complete、resume/rollback retry及owned mismatch；真实公共wrapper拒绝普通原资产变化 | public SDK、preset writer/native在模块层隔离，不代替现场原操作成功。 |
| T769-04 / package | 整包31项中30通过、1个opt-in native fixture跳过（24.217s）。最后等义路径解析收敛后，contract 8项（0.659s）、peer 3项、frozen 8项复验通过 | 使用固定aa898d09真实Fork CLI；末轮定向复验不能写成整包再次执行。 |
| T769-04 / 源码 | 最终source validator通过43 active packages/128 commands；390个Guru Python内存compile、45个Bash语法及marketplace JSON通过 | 首次直接source验证未设置模块路径，未进入validator；纠正PYTHONPATH后实际通过。该设施错误不是产品缺陷。 |
| T769-04 / 真实目标同步 | 原source-loaded guru-upgrade-tools返回tools_upgraded，版本0.7.0-guru.8；同固定public operation完成。目标自身resolver执行installed validator通过，conflicts=0、sidecars=0；native continuation退出0，公开current仍为本Task/Delivery、implementing；Task/config/AGENTS共10路径bytes与mode保持；drift退出0，shared/Claude/Codex/Cursor与canonical一致 | local_candidate的formal_fork_source_lock仍未验证。源执行与目标自身结果分别成立；本项不承担完整多平台矩阵。 |

本观察截止为未提交候选、candidate Check前。实际#766原操作尚未恢复，T769-03由交付后的原tools owner与整体Completion继续核验。历史#718/#760结果保原观察，不能替代本项证据。知识晋升、最终Check/Review、Task/Delivery完成分别成立。

## T769-D2 / 正常退出位置的恢复验证

承接 R769-04—06 / D769-D2；before 为 D1 delivered head aaf7f939，历史观察保留各自截止。T769-D2-01：真实 Git peer 经原观测/begin 后正常移除，公开 frozen 入口携准确 roots 续接；独立核原 source/public operation/plan/preimages/snapshot 不变。T769-D2-02：省略/[]不建立例外，仍注册/仍存在/不关联原观测的普通选错拒绝；存续 peer/common 真实变化继续拒绝，保留 D1 和 #759 回归。T769-D2-03：真实 retry 生产结果有字段、无字段、显式空数组，经声明 presence-select 满足 consumer schema，action/ref/字段存在性和值保持。T769-D2-04：原 tools owner 更新本 Task 的 canonical/dogfood/声明平台，核目标自身 source/installed/native、drift/sidecar/mode 及 Task/config/AGENTS 保持。T769-D2-05：交付后的完整修复 source 实际恢复 #766 原 ref/action，核原固定 bundle/public operation/source 与目标自身入口；组件隔离不能代替此现场验收。

规划时观察：D1 PR776 已合并，三平台 Targeted native CI run 42619232369 成功。随后实际 #766 frozen resume 返回 blocked；只发现 #759 已退出位置五键缺枚举，无存续值变化。原 Cleanup 公共入口已恢复同一 cleaned 结果。以上不建立 D2 实现或整体恢复成功；该规划观察截止时 D2 尚未实现。后续观察由原实现/质量 owners 在合法边界追加。local_candidate 的 formal_fork_source_lock 和完整多平台 Release 矩阵仍未验证。

### D2 实现候选的后继观察

原实施 owner 在本次未提交 D2 canonical 上使用固定 aa898d09 真实 Fork CLI 运行 guru-upgrade-tools 完整 package：37 项中 36 通过，1 个 opt-in native fixture 跳过，61.668s。source validator 通过 43 active packages / 128 commands，JSON、内存 Python 编译和 diff 检查通过。

真实 Git 原 owner begin 冻结 peer 观测，peer 自身 resolver 建立 selection-v3；正常 Git remove 后，公开 frozen profile 携非空 roots 成功，省略/[]保持原 blocked。完整注册含 prunable、根路径残留/普通错位置、存续/common/原 gitdir 变化及未覆盖 runtime 缺失分别拒绝。真实 retry 生产者的 resume/rollback、有/无字段和显式[]经声明 projection 到 consumer schema；原固定 bundle 和 checkpoint 无 roots 字段均已观察。

以上恢复组件中的公共 SDK、preset writer 和目标 native 仍在模块边界隔离；不证明实际 #766 恢复或安装分发。后两项由原 tools owner 继续，后继 Check/Review 与整体 Completion 不由本表预写。早期 D1/现场失败保持各自截止。

### D2 实际目标同步与机械读回

原 source-loaded tools owner 的 operation `45de5159-45a3-4e1d-a43d-830c5e4cdc30` 返回 tools_upgraded，版本 0.7.0-guru.8，recovery_ref `d43a310b-0beb-4858-ad71-aab30a0248dd`。15 个 Task/config/AGENTS 路径的字节与模式保持。目标自身 installed validator passed，43 active packages、128 commands、9124 managed files，conflicts=0、sidecars=0；实际 get_context.py --json 退出0，仍为本 Task/generation0、D2 implementing、Planning applicable。原 drift 退出0，shared/Claude/Codex/Cursor、workflow/spec 与 canonical 一致。

主协调者本轮执行 canonical 三目录下 521 个 Python 文件内存 compile、两 scripts/bash 目录 45 个 Bash syntax 和 marketplace JSON 解析，均通过；分发后 git diff --check 退出0。采用实施 owner 的 source validator 原执行：43 active packages/128 commands passed，其后仅两处等义合同措辞修订，接口/runtime/schema未再改。

以上仍为 local_candidate，formal_fork_source_lock 未验证。实际 #766 原 ref/action 的恢复仍待 D2 交付后执行；本表不预写现场、最终 Check/Review 或整体 Completion 成功。完整多平台安装/升级/Release 矩阵不在本项。

## #813 固定来源创建的工程与实际 Agent 观察

适用 before 为 `5c6a4591db7165ece045e6b0eb789c21d06d7d38`；本节观察对象为 #813 D1 本地未提交候选。来源为 Issue #813 与已接受 D1 规划。原 #718/#760/#769 的测试数量、失败、CI、安装和未知状态保持各自历史截止，本节不改写它们。

| 观察 | 实际执行与独立结果 | 证据边界 |
| --- | --- | --- |
| T718-04/05 / 创建与恢复 | Creation `test_contract.py` 26/26（70.098s）、`test_delivery_chain.py` 2/2（24.583s）；shared `test_composition.py` 20/20（16.948s）；Sync `test_read_baseline_chain.py` 5/5（15.490s）；新增 `test_fixed_base.py` 最终 5/5（11.348s） | 共 58 项定向测试。完整 public producer 链到 Creation；primary 旧 main、staged/unstaged、refs/index/files 保持，原恢复不增 Task/branch/worktree。session 采用原同身份、缺 record attach、冲突/无效拒绝、缺 context 回归。外部 GitHub facts 隔离，不对生产写入。 |
| T718-05 / 来源和兼容 | 新旧合同分别验证及交叉代入拒绝；exact 不可用对象/非 commit、acquisition 起点与 foreign common-dir 的创建/恢复拒绝给字段诊断。synced 新建 stale 拒绝，正常后续 main 前进后原结果恢复 | 仅普通错误装配和真实 Git 状态。历史 `test_495_migration_lifecycle.py` 保持原字节，不把旧协议改成 current。 |
| T718-05 / 真实旧 provider | 从固定 B 的完整 trellis 资产提取旧 provider，原旧 wrapper 创建成功；当前 wrapper 拒绝该旧输入为 schema_mismatch；原旧 provider 恢复同一 created，Task bytes 保持 | 证明固定旧操作的原 owner 恢复边界，不在 current 增加旧 parser/fallback 或转换旧输入。 |
| T718-07 / source | source validator 通过 43 active packages / 126 commands / 159 package test files；524 个 canonical Guru Python 内存 compile、Creation JSON parse 与 git diff --check 通过 | 结构与语法事实；不替代行为、安装或正式 Check/Review。历史各节 128 command 是其当时观察。 |
| T718-07 / clean 安装 | Creation contract suite 中一个代表性 clean installer 样本通过 | 样本由原测试 cleanup 删除。没有再建第二个 clean installer 样本，也不能声称同一 clean 样本已 reapply。 |
| T718-07 / 本 App 工具同步 | 原完整 source-loaded guru-upgrade-tools 返回 tools_upgraded，版本 0.7.0-guru.8。目标自身 resolver/installed validator 通过，43 active packages / 126 commands / 9502 managed files，conflicts=0、sidecars=0；get_context 保留原 Task/generation/Delivery、implementing 和适用 Planning；drift 退出 0，shared/Claude/Codex/Cursor、workflow/spec 与 canonical 一致 | 原 10 个 Task/config/AGENTS 路径 bytes/mode 保持。只更新本 App 工具；不动 source primary main 或 #808 停放工作。local_candidate 的 formal_fork_source_lock 仍 unverified。 |
| T718-07 / 同目标 reapply | 在已更新 App checkout，通过原 tools-only install_assets 与实际已 applied public operation 的原 plan/ref 再应用；installed validator passed、conflict/sidecar=0，10 路径 bytes/mode 保持，drift 退出 0 | 这是同一已安装目标和同一 public operation 的 reapply 证据；与已删除的 clean 样本分开，不声称完整多平台 clean/update/Release 矩阵通过。 |
| T718-08 / 实际 Agent | 本 Agent 读取 repaired installed provider 的 Sync、Discovery、Clarify、Wording、Readiness、Creation 合同，先分别完成语义判断，再沿公开 wrappers 获得 baseline_ready→context_ready→clear→pass→ready→created。固定树 `c2ec2a09aba8ec05342adb9a7bce3804176e9357`，primary main 为 `57668f6488186906d3e1dc14eb479d5479931d8c`；独立 configured checkout 的 HEAD 等于固定树。原 check、recover 及正式恢复均返回同一 Task/generation | 独立隔离 Git 样本未执行 clean preset install，调用本 App 实际 installed provider，Task API 来自 matching Fork。外部重复查询为隔离空返回。sample 文档、来源常量和验收说明不冒充业务实现或测试通过。 |
| T718-08 / 保存和资源 | 实际 Agent 创建后与恢复后独立比较：Task bytes、C4 branch binding、C5 resources、官方隔离 session、refs、worktree 清单均不变；primary HEAD/main/index 及 staged notes、unstaged work 文件与原 capture 一致 | 同一 Task native-fixed-source / generation 0。没有重复 Task/branch/checkout，没有 GitHub 写入或 commit/push。实际 Agent 证据与自动 fixture 的门禁通过分开成立。 |

首次新增 full-chain 测试在 Creation 前调用了不存在的 component shell wrapper，未到产品断言；修正为原 runtime/launch.sh dispatcher 后完整链通过。一次同时运行共享 resolver 的验证在进入 composition 测试前返回 runtime_dependency_missing；随后顺序执行通过。本轮实际 Agent 的首个 recorder transport 命令因 Python argv 装配错误未调用产品入口，随后完整原序列成功；Readiness 首个显示捕获额度不足，未把截断文本当 receipt，通过同源原 recorder 重取完整结果。这些设施问题保留，不能列为产品修复前对照或声称所有尝试一次通过。

当前观察不预写正式 committed Check、Branch/Delivery Review、Publication、Merge、Completion 或 #813 Closure/Finish。完整多平台安装/升级/Release 与业务采用不在本项；本地安装仍有 formal_fork_source_lock 限制。后继结论消费原 owner 的真实公共结果，不追加第二完成台账。
