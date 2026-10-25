# #649：验证观察与证据边界

本次观察截止于2026-10-25本轮F02修订后、下一次正式candidate Check前：下节记录持久目录中的14组独立对照、受控多Delivery样本的实际后续结果及本轮安装观察。正式Task `649-stage-result-convergence / 0` 的full D1首次独立Architecture已返回no-impact/no-change；正式candidate Check发现F02入口覆盖与评分遗漏，返回`implementation_required`，同一Delivery回到`implementing`。尚无成功candidate Check、final Check、完整committed Review、GitHub交付或整体终态。九份shared current拟写仍为proposed。后续正式结果由原公共Task/Delivery结果及Git/PR事实承接，本文不追记自己的最终pass或最终HEAD。

## 当前独立评测与实际收益

本轮来源、逐次raw及host评分保留于仓外`649-independent-20261025/`的`preparation.json`、`runs/`、`host-grading/`和`selected-comparison-results.json`。修订后的D02位于同目录的`d02-v02/`。before生产方法固定于B=`319202beab79c7666ecdb855291bf117e43d407e`；新侧使用当次实际源码。双方corpus与测试运输相同，被测Agent没有收到host预期或评分。每次评分均在实际读取、判断、命令及原wrapper输出形成后进行，再交原runner。

| 场景 | before实际观察 | new实际观察及边界 |
| --- | --- | --- |
| C01：失效当前指南 | 检出矛盾，原`planning_stale/reapprove_plan`；语义true，固定出口期待不匹配 | 同样检出并返回原规划修订；语义true，runner仍为`evaluation_failed`。before已有该能力 |
| C02：错误或被skip的测试 | 上游Architecture返回`fitness_regression`，目标Check未发生；no-grade | 原Check检出被删除覆盖、skip及错误空列表期待；`implementation_required`，runner `passed`。不据缺失的before Check宣称旧侧漏检 |
| C03：必要filter未实施 | 上游Architecture停止，目标Check未发生；no-grade | 保留已实现predicate，实际filter调用失败，原`implementation_required`；runner `passed` |
| C04：合法无变化 | 原Check `passed` | 原Check `passed`；无台账、空contribution或额外验证义务 |
| D01：部署入口与未激活状态 | 原`ready`，但未分别表达制品入口与Control/采用状态；语义false | 原`ready`的实际PR载荷保留本地制品入口、Control未开放、采用及远端E2E未证；runner `passed` |
| D02：切换条件的操作范围 | 原`ready`遗漏受限切换与独立display关系；语义false | 初次新侧仍遗漏display，语义false。修订原Delivery Review合同后，同corpus复测在原review及PR载荷明确switch receipt仅约束`select_target(release-2)`，release-1下rename/display独立可用；runner `passed` |
| P01：必要consumer缺失 | 实际`NotImplementedError`，原`additional_delivery_required`；语义true，固定期待不匹配 | 同样保留R1并路由必要R2实施；语义true，runner仍为`evaluation_failed` |
| P02：无依据Control前置 | 检出前置无来源；原`additional_delivery_required`合法，语义true，固定期待不匹配 | 首次inspect先于规定读取，no-grade；独立复测实际复现无依据gate，将未分配R2交实施；语义true，原合法出口与固定期待仍不符 |
| P03：真实外部待证 | 原`evidence_pending`，runner `passed` | 原`evidence_pending`，runner `passed`；保留源码/制品事实，明确staging operator及receipt到达后的原evidence-refresh条件 |
| P04：范围外环境未知 | 原`completed`，runner `passed` | 原`completed`，runner `passed`；本地accepted scope已满足，远端未知保持未证，不新增blocker |
| P05：正文截止点与后续结果 | 两次原Completion均`stale_identity`，另有库存诊断；no-grade | 原`completed`，runner `passed`；消费真实后续Delivery/Git事实，不要求正文回写自身最终pass/HEAD或重放已完成晋升 |
| P06：局部完成与整体缺口 | R1成立而R2 consumer未实施；原`additional_delivery_required`合法，语义true，固定期待不匹配 | 分别保留本地实现/制品事实与R2缺口；语义true，runner仍因固定期待为`evaluation_failed` |
| F01：task-free报告 | 同一单JSON格式提示下，原`completed`，runner `passed` | 原`completed`，runner `passed`；仅指定文档、本地写后检查与明确未证边界 |
| F02：task-free操作边界 | 原`completed`且三项apply级测试通过；复核发现CLI仍将qualification设为全局必填。原host true评分遗漏实际入口，已保留并纠正为false；runner重评分`evaluation_failed` | 初次新侧同样遗漏CLI，原host true已纠正为false。原task-free方法补实际入口／未改caller与写后调用检查后，同语料new-v02实际修CLI，5项测试及带资格选择的真实CLI探针通过；但对应installed v02仍遗漏CLI，host false。再次明确读取caller、parser、dispatch、outer guard并从受影响实际入口验证后，当前source new-v03的5项测试通过，host true、原runner `passed`。实际展示重命名不要求资格且保留active_target，无资格切换拒绝且state不变；报告仍限本地 |

采用修订后D02和F02的实际结果，新侧14项均有有效目标owner观察且host true；原runner为10项`passed`、4项`evaluation_failed`。后四项C01、P01、P02、P06是固定出口期待与原合法路由差异，语义评分均为true；没有修改期待值将其改记通过。F02初次新侧是真实入口遗漏，修订前false保留，不能并入合法路由差异。旧侧为4项`passed`、3项语义false、4项合法路由期待差异、3项no-grade。D01、修订后D02和F02分别支持本轮具体的载荷／操作入口覆盖改善；其它已有能力不重复记为新增收益，旧侧no-grade不构成漏检证明。原selected结果、F02旧评分及更正前runner输出均另存保留，评分修订不改原执行或fixture。F02当前选择来源和运行位于仓外`649-independent-20261025/f02-v03/`，前次`f02-v02/`及选择前像保留。两次生产方法差额均只修改原task-free合同，不改corpus或期待值。

早先shell/运行时、上游Architecture、inspect读取顺序、尾随JSON说明、P05身份/库存等错误，以及D02首次新侧false均保留。task-free运输只澄清最终消息为一份原JSON，双方同口径复测；不向执行面提供业务结论或预期出口。所有已结束run的原trace、context及request均有持久保留副本。

## 当前受控组合与安装观察

受控链的实际结果在本Task ignored runtime的`649-recovery-20261022/paired-fresh-sample-01/runs/new-v01/`。这是同一实际fixture Task的D1/D2原owner接续，不是14项独立fixture的拼接。

- D1原merge返回`delivered`。D2实际实施后，原candidate Check返回`candidate_checked`；原RDT final_integration返回`ssot_current`，实际重绑后的final Check返回`passed`，完整committed Review返回`passed`。D2受控PR #2合入`8351b54e826eb8509ee63263e405e3cb6b43d823`，原Merge返回`delivered`；D1历史事实未改写。
- 原whole-task Completion返回`completed`。原Finish返回`success`；bookkeeping受控PR #3经原provider的body-file恢复后合入`f2ea0cde956af161b5cb44e0ea5f7015f02a6480`，14份归档与真实target核对一致。首次provider参数失败及资源状态核对误判均保留，恢复不计为独立盲测成功。
- fixture Cleanup的正式出口仍为`remaining_resources`，因后续复核用途保留worktree、branch和ignored证据，没有`cleaned`声明。18个冻结package及受控provider main在本轮独立评测后仍匹配。该受控I/O与历史冻结方法证明其实际执行层，不代表真实GitHub、全部最新方法或生产采用。
- 正式checkout本轮source/installed校验、Shared/Claude/Codex/Cursor投影drift、实际安装的get_context入口及零未处理sidecar通过。原tools-only最终返回`tools_upgraded`，保留`formal_fork_source_lock`未证边界；212项公共工具目标字节未变，303个peer pointer由原owner检查。首次preset保留决策失败已沿原rollback返回`rolled_back`，随后按原接口重新准备成功，没有改写旧错误。
- 原唯一`clean-rebuilt`的native默认初始化因manual bootstrap Delivery无法直接切换Guru而停止；部分初始化前像保留。沿同一代表路径从匹配CLI的`trellis init --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#e9583202b67750d7b3ec2b7eab4b037c0c52a226`重新初始化后，workflow等于canonical，preset及reapply均为`ok`，installed校验通过，实际get_context返回`currentTask: null`。用户内容及scaffold Task共五文件的字节/mode在reapply前后相同。原installer投影枚举核对10,243份目标字节及323份可执行源的目标权限，零差异、零未处理sidecar。
- 该实际clean安装的F02已完成host复核，原installed runner重评分为`passed`。Agent读实际合同、源码及消费者后，修正CLI将qualification参数对所有操作设为必填的问题；展示重命名无需资格，目标切换仍要求资格且拒绝时保留state。原wrapper返回`completed`，只列两份本地文件、5项实际通过测试及未接触qualification service/runtime deployment的边界。初次空run请求的rc2保留。此样本证明实际安装可执行及本地修订，不作为before/new比较收益，也不证明部署、激活、采用或业务E2E。证据位于仓外`649-independent-20261025/installed-clean-f02-v01/`及同目录的host-grading和logs。
- 正式候选阶段的24项stage-result运输回归全部通过（668.484秒）。实施运输12项首轮出现一项error和一项failure：旧断言读取已消费输入，并要求将消费路径写回facts。原消费方法已使用内存`consumed_paths`，输入实际删除、facts保持；经原normal/solution核验后，只修两项测试断言和下一次recorder输入准备，两项命中复跑通过（70.981秒）。task-free运输3项通过（73.970秒）。这些确定性结果不代替F02实际Agent复测。
- 本轮Author／Check／Delivery Review合同分别2／12／7项通过；task-free合同及runtime为11项通过；RDT合同11项及26个subtests通过。Completion首轮缺上游API路径的19个skip保留，补齐matching来源后21项全部通过。Architecture全量43项schema／promotion套件运行中主动停止，不计通过；本轮没有schema或晋升执行代码差额，改由实际独立原wrapper结果和命中的无影响路径1项通过承接。Closure／Finish命中5项通过。统一pytest首次收集时的同名`tests`导入冲突、初次Architecture环境错误均保留；未扩完整仓库回归。
- F02修订后的原tools-only再次返回`tools_upgraded`，recovery为`834d27ed-ddb1-468a-9022-5582a281216c`。212项公共工具动作字节不变，更新原task-free合同五份投影、实施运输测试安装副本及生成manifest；Shared/Claude/Codex/Cursor drift通过。唯一clean更新产生6份预期bak，逐份匹配prior manifest，当前目标等于canonical；备份仓外保留后原reapply返回`ok`。五份用户／scaffold文件content/mode保持。本轮不继承早先其它操作的保护对象数量，`formal_fork_source_lock`仍未验证。该次实际安装态F02 v02已完成，Agent只改测试而未修实际CLI；host false、原runner重评分`evaluation_failed`，不是当前通过依据。

- 第二次F02方法修订为原合同中的11行实际入口检查要求；适用范围仍限状态／gate变化，不增加完整状态矩阵。原tools-only返回`tools_upgraded`，recovery为`8e11aee9-1fdb-41e2-b1e8-539801d88421`；212项公共工具目标字节不变。唯一clean产生的5份预期bak逐份核对prior manifest后移存，原reapply返回`ok`，五份用户／scaffold文件字节和mode保持。当前installed F02 v03先实际复现旧CLI必填错误，再修参数与dispatch；6项测试覆盖无资格重命名、无资格选择拒绝且state不变，以及有资格选择成功。原wrapper返回`completed`，host复核true，原installed runner重评分`passed`。source v03的5项测试与原runner也通过；两者独立取证，不互相替代。前次installed v02的false及其原始输出不改写。最终source／installed package checker及Shared／Claude／Codex／Cursor drift通过；原installer枚举的全部10,243份目标及323份可执行源权限无差异，五份用户／scaffold文件保持，零未处理sidecar。证据位于仓外`649-independent-20261025/f02-revision-v03/`、`f02-v03/`及`installed-clean-f02-v03/`。

正式Task后续须在F02修订后取得成功candidate Check，再执行真实final_integration、实际候选重绑、final Check、完整committed Review及GitHub/终态owners。首轮Check的F649-F02-ENTRY、原正常场景／机制／因果适用性结果及原`implementation_required`均保留；修订不改变accepted scope。完整升级/Release矩阵、正式Fork source lock、既有业务安装采用和生产E2E仍未验证。以下历史记录保留各自run/reapply和评分截止点；旧F02通过描述已由本轮实际入口复核纠正，不能继续作为当前通过依据。

## 方法与层次

固定 before 为 `319202beab79c7666ecdb855291bf117e43d407e` 的完整匹配方法。新旧侧使用相同 native corpus、运输、模型和隔离条件；被测 Agent 自主读实际来源、候选、说明、断言及公共状态，再编写语义结果并调用原 wrapper。host 的预期和逐项评分在执行面之外；历史 fixture gate 仅建立独立入口，不证明当前原 owner 已审核，更不证明连续链。

设计 V649-02..04 的14组分别为 C01..04、D01..02、P01..06、F01..02，每组要求 before/new 实际观察。返回出口、schema、运输和语义分别判断。`execution_error`、未评分及真实行为失败保留，不由后续重试倒改。独立观察不能代替V649-06同一Task多Delivery连续链；当次实际结果及未证边界见前两节。

## 历史执行记录（各段仅描述原观察截止点）

### 已执行观察

| 对象 | 实际事实 | 结论与边界 |
| --- | --- | --- |
| 确定性运输 v3 | 4项，142.880秒，全部通过。原 API 建立 Check 四fixture、实际 consumer；P04原Completion和transient清理；D01原wrapper拒绝空semantic；缺可执行文件保留inner失败且运输继续 | 只证明接线，不证明实际Agent结论 |
| 原回归首轮 | 26项，660.012秒；25项通过，1项source/installed package identity因canonical尚未同步而失败 | 原失败保留；不是方法语义失败 |
| 运输 v4 | 4项，142.536秒，全部通过。新增Architecture历史入口前提经原wrapper建立；Check候选identity、Completion实际结果和Delivery Review原schema均可消费 | 历史前提不计本轮Architecture或连续链 |
| 普通run输入恢复 | 空stdin、非法JSON、缺argv和空argv均显式inner rc2，纠正后真实命令打印42；1项0.024秒通过 | 不制造命令成功、不放宽原owner非零停止规则 |
| native v1/v2 | 旧三路最终均execution_error。包括缺具体invoke terminal trace标记、Completion缺Architecture前提、空run输入导致通道关闭 | 不评分、不计有效观察；原stdout和日志保留仓外 |
| before-v3 C04 | fresh独立Architecture实际调用提交含尾逗号JSON，原wrapper返回invalid_json；没有最终Check | execution_error/no-grade；不记合法对照方法失败 |
| before-v3 P04 | Agent将planning等gate ID放入reviewed_delivery_result_ids；原Completion stale_identity拒绝，trace另缺成功terminal绑定 | execution_error/no-grade；不把局部completed意图当实际完成 |
| before-v3 P03 | 原Completion实际返回evidence_pending；正文区分已交付R1与R2所需staging receipt，明确staging operator及refresh条件，不声称E2E | 原runner结构检查通过，初次因external semantic grading missing为evaluation_failed。独立host逐项评分仍须完成，不预报passed |
| new-v3 P03 | 安装事务正在替换旧Guru目录时启动，runner报eval_runtime_target_invalid | execution_error；不能据此评价新方法。其余native在安装完成后新开runroot |
| 普通preset apply | 原apply在写前报upstream_delivery_migration_required | 保留失败，不迁移或删除legacy archives以制造成功 |
| 原tools-only准备 | 第一prepare把公开claude-code直接用于Guru平台，原安装器写前拒绝；按实际Guru ID claude重新准备成功 | 首次失败保留，无部分tools写入；最终一次冻结plan被原invoke消费 |
| 原tools-only安装 | 当前Task checkout，匹配CLI/Core 0.7.0-castbox.5及实际bytes，local_candidate；原invoke返回tools_upgraded，installed_version=0.7.0-guru.5 | 3063项Task/workspace/session/common与peer pointer保存对象零变化。config保留，无Task转换；formal_fork_source_lock未验证 |
| 安装后定向检查 | source 40 packages/124 commands通过；installed通过、dogfood三平台drift通过；唯一原identity回归0.023秒通过 | 解决原25/26后的唯一命中失败。安装事实不证明业务采用；独立reapply、代表clean与installed Agent尚待完成 |

### 后续确定性验证与评测修复

本节保留前表首次观察，不将后续修复改写为首次成功。测试支持两侧同步；before 的生产 Markdown 保持固定 B。每个 native invocation 在启动时复制自己的测试支持与输入，运行中后续同步不追溯改变该 invocation 的版本。

| 对象 | 实际观察 | 证明范围 |
| --- | --- | --- |
| 运输 v5..v8 | v5为5项/139.724秒；v6为6项/162.985秒；v7为6项/158.225秒；v8为6项/163.504秒，均通过 | 实际 Task/Delivery 绑定、候选路径、Architecture identity、可纠正的 run/write 请求错误、原 wrapper 非零停止，以及连续链无预建 gate。不是 native 判断证明 |
| 原计划要求的 consumer probes | 最新1项/85.212秒通过，覆盖四个 Check fixtures。实际执行原定 singleton、duplicates/order 两组断言，并保留 stdout/returncode | C03的真实consumer仍失败；其余正确实现的三组consumer观察通过。补齐原fixtures证据缺口，没有降低验收 |
| 受影响原回归 | Activation/Check两项/55.361秒通过 | 工具文件属于既有 baseline，candidate路径完全属于facts覆盖，不将整套工具误当业务差额；原 Check 只改声明的checkpoint |
| Architecture reviewer运输 | 首轮新增测试缺shutil导入而失败；补导入后1项/27.103秒通过 | 缺输入目录可创建；缺reads的普通请求在创建worker目录前返回可纠正错误；纠正后实际原独立wrapper可用。保留首轮测试错误 |
| installed fixture规范 | 1项/3.552秒通过 | 从实际installed输入复制当前规范，字节相同。解决测试fixture漏复制spec，不修改生产安装器 |
| source检查 | 最新40个packages、124个commands通过 | 结构和命令一致性；不证明真实Agent已正确使用方法 |
| 唯一clean安装与reapply | matching CLI init和原apply成功；沿同一clean同步至第13次reapply，最终status=ok，零sidecars | 中间.bak逐项核前后manifest SHA后移至仓外保留，未更改installer或创建第二个clean |
| clean安装闭包 | 10,194个manifest文件、287个可执行文件核对无错；workflow等于canonical；installed checker与Claude/Codex/Cursor投影检查通过 | 定向安装分发证据；不代表完整多平台升级/Release矩阵 |
| clean用户内容 | AGENTS非managed句子、gitignore用户规则和一个非managed文件，在原reapply前后3项SHA均相同 | 只证明本次代表clean中实际用户内容保留；不是所有历史业务安装证明 |
| P03 before/new v4 | 两侧原Completion均返回evidence_pending；独立host审实际来源、正文、trace和原wrapper后，原runner均passed | R1已成立，R2欠具名staging operator activation receipt，有具体refresh条件，未声称E2E。这是#648已有能力，不单列为新增收益 |
| before C01 v9 | 原Check返回implementation_required；host逐项审后原runner passed | 识别已实现filter与当前“不可用”usage的冲突，保留历史P1 cutoff并回原实现/Docs修复。before已有该识别能力 |
| before P06 v7 | 原Completion返回additional_delivery_required；语义评分true，原runner仍为evaluation_failed | R1四项测试及三组filter断言通过，R2实际NotImplementedError且未分配。固定expected_exit=remaining_work与原合法路由不符；不把期待值差异当行为失败 |

普通apply仍保留写前`upstream_delivery_migration_required`；正式Task采用原tools-only路径，未迁移legacy archives。第二次 tools-only 已同步 Architecture 边界澄清及当时测试支持，3063 项 Task/workspace/session/common 与 peer pointer 保护对象零变化，installed checker、三平台 dogfood drift 及实际 get_context/phase 入口通过。第三次 tools-only 已同步 consumed owner-result 清理与连续链等待说明，3063 项保护对象仍零变化；installed checker 和三平台 dogfood drift 通过。v3 recovery_ref 为 e8c68434-048f-415f-873a-879e74fa827c。此后 C03 fixture 与 task-free 出口期待修正尚未同步，不能把较早安装等同最新源码。

后续旧失败包括：before P04后加业务说明使Architecture identity过期；new P06缺Architecture输入目录；before连续链缺planning写入支持、未声明help请求、缺reads后留下worker目录；installed连续链初次缺runtime导入路径，随后fixture漏spec使Agent依法停止。均保留原raw并区分测试接线错误与语义观察。普通请求语法错误可在同一通道纠正；真实原wrapper非零结束该invocation。

连续链后段使用`--resume-protocol`读取实际前段Task、Git和原命令receipts；不重建Task，不预写Planning/Check/Review/DeliveryFact。当前尚无完整D1/D2链完成结果，不能用上述独立fixtures拼接替代。

### 新 C01/C02 复测与后续执行诊断

以下结果晚于前表第13次 clean reapply 截止点。旧 raw 保持原样。

| 对象 | 实际观察 | 判断与后续责任 |
| --- | --- | --- |
| new C01 v9 | fresh Architecture 原 wrapper 返回 fitness_regression，将普通过期 usage 归为 Architecture 退化；Check 未进入 | 语义评分 false，runner execution_error 保留。predicate/caller 的职责、接口、状态和依赖未变；普通功能说明缺口由原 Check、implementation 和 RDT 处理 |
| Architecture 原方法修正 | 仅在原 contract 澄清其自有决定及派生指南责任；一般 usage/功能断言不一致须先证明 Architecture 缺陷，不能仅因能力变为可用而升级 | 没有新增 owner、API、schema 或 typed exit；before 生产方法不接收此修正 |
| new C01 v10 | 原 Architecture baseline_current，原 Check implementation_required。四项 predicate 测试及三组 caller probes 通过，当前 usage 仍宣称不可用 | host 审读取、判断、原 wrapper 后，原 runner 重评分 passed。before C01 已有该识别能力，不将本例单列为新增收益 |
| before C02 v10 | fresh Architecture 将删除测试及旧 skip 归为 fitness_regression；Check 未进入 | host 评分 false，execution_error 保留。该记录没有完整 before Check 观察 |
| new C02 v10 | 原 Architecture baseline_current，原 Check implementation_required；实际 unittest 只有一个有效断言和一个旧 P1 skip，caller probes 通过 | 识别删除的 endpoint/outside/singleton/negative 覆盖和被 skip 的错误空列表期待，要求原实施返工。host 评分后原 runner passed，没有将 rc0 当作语义通过 |
| before C03 v10 | 原 Architecture 返回 fitness_regression，原 Check 未进入 | runner execution_error 保留。不能记为 Check 发现或漏掉缺陷；新 C03 继续独立执行 |
| before P01 v7 | 独立 Architecture 实际 baseline_current、rc0；child stderr 为539,221字节，parent 后续等待，没有最终 Check/Completion | 只终止本 run 的四项进程并保留停止记录；不计语义失败，不把挂起误报为 wrapper 失败 |
| new P06 v9 | 两次 Architecture 均 rc0，stderr 分别为665,171和696,087字节；parent 在前一请求 pending 时重发，最终 JSONDecodeError/等待并自行终止 | execution_error 保留。测试支持只向 consumer 返回原 stdout，完整 native 诊断留私有 raw，并说明应轮询原 session |
| 独立 reviewer transport v3/v5 | v3为1项/25.193秒；v5为1项/28.651秒，均通过 | 验证成功 stdout 精简、完整诊断保留，以及真实原 wrapper schema 错误能简明转交。v4 因测试误期待更具体 field_path 而失败；原 wrapper 实际只报告 input，修测试后通过 |
| before 连续链 v5 | 同一原 fixture 的原 Author 已返回 requirements_ready；下一独立 Architecture 使用旧非 Delivery schema，原 wrapper schema_mismatch 拒绝 | invocation 已结束，不造 gate。v6 继续同一 Task；host 不供应 profile 选择或语义结果 |
| installed 连续链 v2/v3/v5 | 初次 fixture 漏 spec，Agent 依法停止；恢复 spec 后，Author 用错误 initial_review profile 被原 wrapper 拒绝；v5 同一 fixture 已由原 Author 返回真实规划候选 | 仍无完整 D1/D2 链结果。该 fixture 的生产包冻结于首次 clean 安装，未包含后来的 Architecture 边界澄清，不能声称覆盖最新全部源码 |
| clean v14..v17 | v14三项、v15五项、v16两项 sidecars，逐项核 backup 等于前次 manifest、current 等于当次 manifest 后归档仓外；v17 status=ok、零 sidecars、installed checker passed | 仍为唯一 clean。刚完成的 transport 诊断修正沿原 reapply 继续同步，不将 v17 写成未来版本的安装证明 |
| clean v18/v19 | v18两个 support sidecars 逐项核前后 SHA 并归档；v19 status=ok、零 sidecars | 10,194 个 manifest 文件和287个 executable 无误，workflow 等于 canonical。第20次 reapply 已同步消费清理/等待说明；三项 sidecars 核前后 SHA 后归档，第21次 status=ok、零 sidecars。随后 C03 fixture 与 task-free 出口期待修正尚未 reapply |
| before P01 v11 | 原 Completion 返回 remaining_work；整体 R1/R2、历史 Delivery、current-review、consumer.py 与真实 rc1/NotImplementedError 均已审 | host 评分后原 runner passed。将 R2 判为必要实施工作，保留已交付 R1，不要求外部证据来代替实现；before 已有该能力 |
| new P06 v11 | 原 Architecture baseline_current；原 Completion stale_identity 拒绝 | Agent 将 Planning/Check 等 gate ID 混入 reviewed_delivery_result_ids，并填写非实际 evidence revision。该 invocation 为 execution_error，不计语义通过；v12 独立重测 |
| installed 连续链 v5 结束 | 主 Agent 在独立 Architecture 仍 pending 时结束；没有原 Architecture 最终 stdout。另有成功 Author 消费的 owner-result 临时文件未被 transport 删除 | 两项诊断均保留，不记语义通过。补齐 --owner-result 消费清理，原路径记录仅供 fixture inventory 检查；等待说明不以耗时推导失败。v6 使用同一 fixture 和原 gate 结果继续 |
| 消费清理与错误转交定向验证 | v6为1项/26.843秒，v7为1项/26.612秒，均通过 | 实际原 Author wrapper 消费后清除 owner-result 文件；已有 transient 删除纳入既有 fixture mutation 范围。原 Architecture schema 错误仍为失败并保留具体原输出，不替代 native 判断 |


### 第21次 clean reapply 后的观察

| 对象 | 实际观察 | 判断与边界 |
| --- | --- | --- |
| new P06 v12 | 原 Architecture baseline_current，原 Completion remaining_work；host 审读取、正文、真实源码/观察及 wrapper 后，原 runner 重评分 passed | 四项 predicate 测试通过，R1 filter 和局部制品事实保留；consumer.consume 实际 rc1/NotImplementedError，R2 是必要实施缺口。没有将未激活或无关外部未知推成整体未实施，也没有将局部交付推成整体完成 |
| new C03 v10 | Architecture 返回 fitness_regression，Check 未进入；原 raw 保留为 execution_error | 复核 fixture 发现其先建立可用 filter，再把 candidate 改成 stub，实际变成已实现能力退化；这与冻结的“消费者仍未实施”场景不同。不能将该记录当成 Check 观察或据此要求方法放过退化 |
| C03 fixture 修正 | 将未连接的 filter 置于原 before baseline，candidate 不再删除可用实现；当前 usage 明确实际缺口。双方使用同一修正 | 原 consumer 仍真实失败，期望仍是实际实施返工；没有预写 owner 判断。四fixture定向验证1项/81.334秒通过，额外核 C03 before/current consumer bytes 相同。首次测试命令因未设模块路径而 import 失败，改为原文件入口后通过 |
| F02 首次 runner 启动 | eval_expected_exit_unknown，未启动被测 Agent | F01/F02 corpus 误写未声明的 completed_local；核原 interface 后改成既有 completed。双方测试 corpus 同步，不修改生产接口或 typed exit；原失败保留 |
| new P01 v11 | independent-review rc2：首次 Architecture 读取列表含 Task PRD；原独立入口拒绝 | 不是 Completion 语义失败，也不能记当前 Architecture 已审。当前 invocation 不得沿失败通道合成结果 |
| before 连续链 v6 / installed 连续链 v6 | 原 Architecture wrapper 均报告 input.freshness_identity stale_identity | 保留具体原错误；不由 host 提供 digest、profile 或 gate。后续只能沿同一 Task 的原 owner fresh re-entry 继续 |
| 测试支持 parity v15 | 13项支持文件双方相同；14项 before 生产方法逐项等于 B | 包含最新 owner-result mutation assertion 和 C03 fixture；task-free corpus 同步。每个已启动 native invocation 仍绑定启动时版本，不追溯替换 |

### 后续 fixture、运输与有效观察

| 对象 | 已核事实 | 判断与边界 |
| --- | --- | --- |
| C03 配套规划修正 | 第一次 fixture 修正后，原规划仍将 filter 描述为已有实现。第二次同步修正起点规划和 authority 历史，使 before/current 均为真实未连接的 filter stub；定向测试1项/84.944秒通过 | v12 在第二次修正前启动，双方不能作为最终同口径方法比较；仍需使用一致事实的新一组。预期继续要求实际消费者可用，没有放宽验收或预填 owner 判断 |
| 终止通道 | new P01 原独立入口拒绝 PRD 后，后续误调用已关闭 FIFO 挂起；before P05 在成功 Architecture 后重复提交缺 stdin 的请求而挂起。精确停止本 run helper/native 并保留停止记录 | 运输现在保留 FIFO 服务至 stop，由原 relay 立即拒绝 terminal 后调用且不执行命令。真实原 wrapper 失败后连续两次误调用均返回 rc2、marker 不写，1项/21.199秒通过；不是语义方法通过 |
| reviewer 调用前校验 | 校验 reads 先按输入顺序读取 Constitution、Baseline、change contract，并排除整份 PRD/implement/task.json。请求不符合时在创建 worker 目录前返回可纠正错误；纠正后调用原独立 wrapper | 1项/26.422秒通过。未执行原 wrapper 的普通请求错误不计 semantic failure；host 不提供 profile、digest 或 exit 答案，原 schema 仍由原 wrapper 校验 |
| before 连续链 v7 | 原 Wording、Architecture final_plan、Approval、Activation 已实际完成；随后 Phase2 的 reads 顺序及 PRD/implement 读取不符合独立入口。最终库存错误遮住原错误，新增文件仅为 pytest cache 和原 Approval checkpoint | 只扩展测试 inventory 的既有 consumer，列入该 fixture 的实际 cache 与该 Task 的原 owner-checkpoints；没有新增生产状态或合成 gate。v8 沿同一 Task/D1 继续，结果尚未完成 |
| installed 连续链 v8 | 原 Architecture schema_mismatch 指向 schema_version，要求重入当前 final-integration 合同；adapter 后续 JSON 解析失败 | 保留两层错误。v9 从 v8 原 protocol 继续同一 fixture；host 不给出 profile 或语义答案。生产包仍冻结于首次 clean 安装，不等同最新 source |
| before F02 v10 | 原 record/check/invoke 均 rc0，原 completed 只报告 catalog.py/test_catalog.py、本地三项测试和未接触 qualification service/runtime deployment。实际 rename_display 仅改标题并保留 active_target，未获资格的 select_target 拒绝且状态不变 | host 审实际读取、源码、操作 receipts、判断和原 wrapper 后，原 runner 重评分 passed。原 fixture 已具备 operation 边界；本例证明范围保留和本地报告，不声称修复旧坏实现、真实部署、激活、采用或 E2E |
| new F02 v10 | final stdout 为截断的 public_input/owner_result envelope，未得到原成功 record/check/invoke receipts | execution_error，无有效语义评分；具体截断原因尚未确认，不猜测。原 raw 保留，需独立复测 |
| source 与支持一致性 | 最新 source checker 通过；双方13项测试支持在 v18 相同。上次逐项核对的14份 before 生产方法等于固定 B，此后只同步测试支持 | checker 的40 packages/124 commands/136 package tests为结构库存，不能写成执行136项测试。最新 fixture/运输支持尚未沿原 tools-only/reapply 同步正式安装与唯一 clean |

### 最新运输修复与安装截止点

| 对象 | 已核事实 | 判断与边界 |
| --- | --- | --- |
| 连续链请求与消费清理 | before v8 将受限 write 的请求错误误作 terminal；修复后不写越界目标并返回可纠正请求错误，已有 run 仍可写临时 JSON。1项/19.801秒通过。new P05 v11、new P01 v12 的原 wrapper 已成功，但清理输入时改写 facts，trace 拒绝；改用内存 consumed_paths 后，实际 wrapper 成功、输入被消费且 facts 字节不变，1项/23.295秒通过 | 原 execution_error/raw 保留，不将原 wrapper 局部成功升级为有效评测。修复只属于测试运输，双方支持 v20 的13项字节相同 |
| 连续链恢复诊断 | before v9 driver 缺 PYTHONPATH，未启动 native；v10 忽略 write 请求错误，原 Check 因输入不存在返回 unsafe_path。installed v9 的原 Architecture 返回 planning_root stale_identity，adapter 随后解析失败 | 都没有完整质量链结果。后续从同一 fixture 的实际 Task/命令 receipts 恢复，不由 host 提供 profile、digest 或判断 |
| source checker v6 | 40 packages、124 commands、136 package tests 库存，status=passed | 结构库存不等于执行136项测试；不替代独立 Agent 或完整链 |
| tools-only v4 | 原入口返回 tools_upgraded，安装版本0.7.0-guru.5；recovery_ref=09507528-a96c-4ee9-a471-aadcf0a825c8。3063项保护对象 content/mode零变化；installed checker和三平台dogfood drift通过 | matching CLI/Core为0.7.0-castbox.5，local_candidate。保留config，不迁移Task/archives，不碰common/peer pointer；formal_fork_source_lock仍未验证 |
| 唯一 clean v22/v23 | v22产生9项.bak，逐项核 backup=前manifest、current=当次manifest后移仓外保留；v23 status=ok、零sidecars。installed checker通过；10186项manifest文件及287项executable核对无错，workflow等于canonical | 仍是原唯一代表clean，未建立第二个clean。当前安装覆盖上述最新测试支持和产品方法；较早installed连续链fixture仍冻结原生产包，不能据此扩大其覆盖 |

后续连续链 fact sheet 的 `planning_root` 曾写成仓库相对路径，而原 API 要求相对 Task。现改为原 API 对应值，恢复入口也从同一 Delivery 重新读取；已有测试同时核该值和实际规划文件写入，1项/19.138秒通过。双方13项测试支持在v21相同，14份before生产方法再次逐项核对等于固定B。该修复不提供语义答案，旧native输入不追溯替换。

第5次tools-only同步返回tools_upgraded，recovery_ref=e1a868c0-0e18-41c4-aeec-96bdf828fc3b；3063项保护对象content/mode零变化，installed checker、三平台dogfood drift和实际get_context入口通过。唯一clean第24次reapply产生2项support备份，逐项核前后manifest后移仓外保留；第25次status=ok、零sidecars，installed/闭包检查沿原目录刷新。formal source lock及业务采用仍未验证。

before P04 v10原Completion返回completed，但旧版消费清理改写facts，trace验收失败；该轮继续记execution_error，当前支持版本独立复测。before C03 v13原Architecture返回fitness_regression，仍无原Check结果，不将其记为Check检出或漏检。new F02 v14提交的semantic witness不合原schema，没有完成结果；installed连续链v10原Architecture输入JSON无效。原错误均保留，各自从合法入口复测或同一Task恢复，不升级为语义通过。

new F02 v15原wrapper完成，host审实际输入、读取、两个文件、CLI操作和本地测试后，原runner重评分passed。display rename保留active_target，未获资格的target选择失败且状态不变，具资格切换测试通过；最终报告仅含两个本地edited paths和本地检查，明确外部未证。该fixture起点已具操作边界，本例不证明修复旧坏实现。

本轮另确认new P01/before P05的helper在终端stdin等待，尚未发出该次Architecture请求。仅中断两项输入等待helper，原native和同一Task保留。测试helper现对带--stdin但无管道的调用立即rc2且不发送请求；无stdin参数的help仍执行原命令。定向测试首轮因旧receipt索引期待失败，修正期待后1项/21.078秒通过。顺带更新原终止通道测试的过期thread期待，使其符合已实现的terminal后仍可返回拒绝诊断。双方13项支持在v22相同；这两项最新helper/test支持尚未同步tools/clean安装，不能将第25次安装扩大到这些后续bytes。

本轮新增三项有效评分：new P01 v13原remaining_work，实际R1已成立而consumer.consume的R2仍NotImplementedError；new C03 v13原implementation_required，分别保留已实现predicate与缺失filter，AC3 consumer正常调用实际失败；before P05 v12原completed，完整R1/AC1..3与consumer均成立，远端激活/E2E明确不属accepted scope。host逐项审实际要求、读取、判断、源码/观察、原Architecture和原wrapper后，三项原runner重评分均passed。before P05首次重评分误选新侧root而被原validator拒绝；随后使用原before root重评分，未修改原执行。

### 第27次 clean reapply 与后续观察

| 对象 | 实际观察 | 判断与边界 |
| --- | --- | --- |
| new P05 v12 | 四项 predicate 测试、三组 filter probes、consumer 与 diff 检查通过；fresh Architecture 为 baseline_current，原 Completion 返回 completed | host 核要求、实际读取、current-review、源码、原操作及 wrapper 后评分 true，原 runner passed。本地 accepted scope 已满足；范围外 Control、远端采用及 E2E 不成为新前置。正文 cutoff 与后续公共 Delivery 事实分别承接 |
| installed F02 v1 | 原 completed 保留本地 edited paths 和外部未证边界；Agent 通过 file_updates 新增 execute 及两项测试，但实际检查仍是起点的三项测试 | host 评分 false，原 runner evaluation_failed。未执行修改后的五项测试，不能声称新覆盖已通过。保留完整 raw，不把原 wrapper rc0 当语义通过 |
| task-free 测试运输 | 补 private write/run，先把 Agent 提供的 bounded bytes 写入实际 checkout，再返回实际检查结果；原 public API、生产 owner 与 gate 不变 | helper/原 wrappers 定向测试1项18.216秒通过。实际检查读到写后字节，分别返回失败和成功；trace 与实际 commands 一致。首轮测试误选 fixture 不允许写的 catalog.py，16.917秒失败；修正为该 fixture 的授权 target 后通过 |
| before P04 v15 | helper 缺 stdin 在终端等待；仅中断该 helper，原 native 保留。后继请求的初始 reads 不符合独立合同，最终未调用 Completion | 记 execution_error，不记语义通过或失败。使用已有 stdin 修复的支持版本独立复测；不由 host 提供 reads/profile/判断答案 |
| P02 v13 场景复核 | before 原 completed；new 原 Completion stale_identity。两侧 fixture 将 Control guard 放在 consumer.consume，但原 Task authority 只明确要求 predicate 与 range_filter.select | 旧场景不能证明 accepted operation 被无依据前置阻断，before 不判漏检；new 仍是 execution_error。现把原设计所需的本地 consumer 明确纳入 fixture Task R2，保留两侧原 raw，同口径重跑 |
| P02 fixture 验证 | Task R2 明确 consumer.consume 不依赖 Control；真实 consumer 调用 rc1/Control receipt required；Task/Delivery/public wrapper 运输仍有效 | 定向1项23.201秒通过。首轮测试误改了同文件另一处 request，22.343秒失败；修正目标测试后通过。不给被测 owner 预填 route 或语义结果 |
| before D02 v12 | 原 ready；predicate 四测试和三个 filter probes 实际通过，fresh Architecture 为 baseline_current | host 评分 false：读取了 operation policy 与 catalog_operations，却未说明 release-2 switch 仅约束 select_target，也未表达独立 display 与该迁移关系。远端未证边界保留，但 operation/状态分维要求未完整覆盖 |
| tools-only v6 | tools_upgraded，recovery_ref=22421bf3-ddf7-4c5c-a627-6d9995d904db；3063项保护对象 content/mode 零变化 | matching CLI/Core仍为0.7.0-castbox.5、local_candidate。installed checker、三平台 dogfood drift 通过；包含 task-free write/run 和 stdin 支持。后来的 P02 fixture/test 两项尚未同步 |
| 唯一 clean v26/v27 | 4项备份逐项核 backup=前manifest/current=当次manifest 后移仓外保留；v27 status=ok，零sidecars | 10189个manifest文件和287个executable核对无错，workflow等于canonical，installed checker通过。installed F02 v2从该实际入口复测，结果尚未完成；不扩为完整矩阵或业务采用 |

双方15项测试支持在v24逐项字节相同，包含上述P02 fixture修正。before生产方法继续固定B；已启动的native绑定各自启动时支持，不追溯改写。连续链仍沿原Task/D1推进，尚无完整D1/D2结果。正式shared current仍未晋升，不能把proposed正文或独立fixture当作最终质量链。

### 第29次 clean reapply 与 tools-only 同操作恢复

| 对象 | 实际观察 | 判断与边界 |
| --- | --- | --- |
| installed F02 v2 | 原 completed 只报告本地 test_catalog.py；实际 write/run/inspect 后三项 unittest 通过，原 qualifiers、record/check/invoke 均 rc0 | host 审实际读取、写后字节、检查与原 stdout 后评分 true，原 runner passed。空 qualified_targets 不阻止 display rename，active_target 保留；无资格选择拒绝且状态不变，具资格选择通过。fixture 起点已有正确操作实现；不声称修复旧坏实现或证明外部采用 |
| tools-only v7 中断与恢复 | 初次 invoke 退出120，result/stderr为空；原 checkpoint 停在 preset，安装 manifest、入口及写作规范缺失。使用原 operation 的 recovery_ref=2438ce0a-0d68-4494-a915-f646e68f66a0、未改 source 或 frozen plan，原 resume 返回 tools_upgraded/0.7.0-guru.5 | 3063项保护对象内容与权限零变化；installed checker、三平台 drift 和实际 get_context 通过。恢复使用原 launcher，不手补安装文件。初次退出原因未确定，不以连续链的磁盘错误替代其诊断；formal_fork_source_lock 仍未验证 |
| 唯一 clean v28/v29 | v28的两项 support 备份逐项核 backup=前manifest/current=当次manifest 后移仓外保留；v29 status=ok、零sidecars | 刷新 installed checker通过；10189个文件、287个executable核对无错，workflow等于canonical。仍为同一代表clean，不扩为完整矩阵 |
| before P04 v16 | fresh Architecture baseline_current，四项predicate测试、三组filter probes及consumer实际通过，原Completion completed | host 审完整本地scope、当前review、原读取和Task/Delivery事实后评分true，原runner passed。Control未开及远端初始化/采用/E2E保持范围外未证；before已有本例能力 |
| 连续链 v12/v13 | before v12原Architecture报告invalid_json；installed v12/v13原Architecture拒绝旧schema。before v13原日志记录trace写入时No space left on device，随后未得到最终原wrapper stdout | 全部保留为execution_error；无完整D1/D2结果。v14分别沿各自同一Task和原preceding stdout继续，不拼接独立fixture，不由host提供profile、digest或判断。installed链生产包仍冻结首次clean，不代表最新全部源码 |
| 源码与比较支持 | source checker v8通过；415份Python AST检查无错；git diff --check通过。恢复后再次核双方15项support相同、14份before生产方法逐项等于固定B | 结构及语法检查不等于实际行为测试。独立样本、安装及连续链分别报告；正式candidate/final质量链仍未执行 |

### #648 前置与 #637 有限修正

原 #648 Test 的最终汇总为14个具名子组各两次before/new，共56项有效观察。有效观察包含真实false；固定出口期待失败与具体语义成立分开，execution_error/no-grade不计有效次数。该结果只承接 #648 自身行为验证，不能替代本项独立样本或多Delivery组合。具体来源为 [原唯一Test](../648-constraint-premise-review/test.md)，本轮重读已核到最后汇总及其剩余边界。

#637 本轮只修当前状态与观察截止点。原“尚未验证”正文保持，追加归档Task的正式 Check/full_review/readiness/Delivery/Completion 引用。live PR #644 为 MERGED，merge `3a38020b456112fd329e9a6616e4222e589dea12` 对本项固定B祖先检查成立；head和mergedAt与归档交付对应。原legacy reapply阻塞、formal source lock、当时组合、业务采用、生产和完整矩阵没有被改成通过。

### 第31次 clean reapply 后的观察

| 对象 | 已核事实 | 判断与边界 |
| --- | --- | --- |
| 连续链失败调用恢复支持 | continuation 保留真实原请求的 arguments、stdin 和 response；原 Author 失败再 resume 的定向测试1项/19.328秒通过。双方15项支持在v25字节相同，14份before生产方法仍等于固定B | 只修测试运输，不提供profile、digest、语义结论或gate。已启动native保留其启动版本 |
| tools-only v8 | 原invoke返回tools_upgraded/0.7.0-guru.5，recovery_ref=bb485e59-d05b-4061-8566-302c67c71dfa；3063项保护对象content/mode零变化 | installed checker、三平台dogfood drift和实际get_context通过。matching仍为0.7.0-castbox.5/local_candidate，formal_fork_source_lock未验证 |
| 唯一clean v30/v31 | v30两项support备份逐项核backup=前manifest/current=当次manifest后移仓外保留；v31 status=ok，零sidecars | installed checker通过；10189项manifest文件、287项executable无错，workflow等于canonical。仍是同一代表clean，不扩完整矩阵 |
| before P02 v15 | fresh Architecture baseline_current；四项predicate测试及三组filter probes通过，consumer实际因Control receipt required失败。原Completion返回implementation_revision_required，原runner重评分passed | accepted R2明确要求本地consumer且无Control前置。原判断正确归为实现缺陷，要求去除无依据guard并重验；before已有此能力，不算新方法收益 |
| before P02 v14诊断 | 原独立Architecture wrapper internal_error；只读提取其原envelope复查，定位owner_result缺baseline_identity而触发KeyError | 旧execution_error保留，不改原payload、不算额外native成功。诊断harness初次缺模块路径，纠正后定位原错误；v15是另一有效执行 |
| new P04 v16 | 原Completion stale_identity指向semantic_result；原Agent把Planning/Check/Review/readiness/publication IDs同时放入reviewed_delivery_result_ids。失败后保留的两个临时JSON又触发inventory错误 | execution_error，不记语义false，不扩大运输范围接受错误。before P04 v16已有效；new v17独立复测中 |
| new D02 v12 | fresh Architecture baseline_current、四项测试和三组filter probes通过，原Delivery Review返回ready。原runner语义重评分为evaluation_failed | 本地scope与远端未知保留，但未解释release-2证据仅约束select_target，未表达独立rename/display的适用关系，也未分别明确artifact/Control状态。该operation与分维观察为false，与before相同；不以出口/schema通过替代语义判断 |
| 连续链before v15 / installed v14 | before独立Architecture worker未返回其原wrapper stdout；installed原Author返回schema_mismatch/owner_result.output，运输随后报告缺终态trace字段 | 两段均为execution_error，无完整D1/D2结果。installed v15沿同一原Task和真实失败请求恢复；不拼接独立fixture或改写生产包 |

### Delivery载荷修订与第33次安装观察

| 对象 | 实际事实 | 判断与边界 |
| --- | --- | --- |
| new P02 v15 | 原Completion返回additional_delivery_required；fresh Architecture与R1本地验证成功，R2无凭据consumer仍实际失败 | 已核原历史Delivery明确只含R1，R2仍在整体accepted scope。Agent判无authority的guard为实际实现缺口，要求新增Delivery去除guard并验证；语义criterion成立。固定期待implementation_revision_required不匹配仍为deterministic false，runner保持evaluation_failed，不改原期待或原结果 |
| new P04 v17 | fresh Architecture baseline_current、四项predicate测试、三组filter probes及consumer通过；原Completion completed，原runner重评分passed | 分别保留本地source/artifact、直接调用无需初始化和local consumer事实；Control未开、远端采用/E2E未证且不属本地accepted scope。没有制造外部blocker |
| D02命中方法修订 | 在原Delivery Review contract补充最终payload自检：独立说明artifact/entry和enablement，说明受限制operation及保持独立的已交付operation；泛化的未证环境清单不能替代这些事实 | 只补原owner自然语言职责，不增字段、脚本判断、gate、profile或exit。旧new D02 false保留；new v18独立复测，不向Agent提供答案 |
| tools-only v9 | 原invoke tools_upgraded/0.7.0-guru.5，recovery_ref=8d3d6033-7dae-4a14-9080-4ccd082520de。public/Guru目标路径集合、peer pointers和matching source与v8相同；3063项保护对象零变化 | installed checker、三平台dogfood drift与实际get_context通过；formal source lock仍未验证。只暂停父调度器，已有native继续；安装结束后两项父调度器已恢复 |
| 唯一clean v32/v33 | 5份contract备份逐项核backup=前manifest/current=当次manifest后移仓外保留；v33 status=ok | installed checker通过，10189项文件、287项executable零错误，workflow等于canonical，零sidecars。不是第二个clean或完整矩阵 |
| before连续链v15进一步诊断 | fresh Architecture worker最后输出为--stdin requires piped JSON input; no request was sent，原wrapper未执行 | 仍为execution_error；v16沿同一Task恢复，不改原失败或向worker提供semantic结果 |

### 第35次安装与继续观察

| 对象 | 已核事实 | 判断与边界 |
| --- | --- | --- |
| new D02 v18 | fresh Architecture baseline_current、四项测试/三组filter probes通过，原Delivery Review ready。payload已明确select_target(release-2)受限制、rename/display与contains/select保持独立 | operation观察已补齐；仍只报告本地source/调用，没有分别表达已观察的local-fixture-artifact/entry事实。完整semantic/current-review也未补齐该分维，host保持false，原runner evaluation_failed |
| Delivery载荷自检补充 | 在原pr_payload_truthfulness职责明确核实际状态正文，evidence reference不能替代；已成立的本地制品/入口与远端未证分别说明 | 原owner、字段和出口不变。new D02 v22使用新方法独立复测；旧false不改写 |
| tools-only v10 | tools_upgraded/0.7.0-guru.5，recovery_ref=32f57613-12e9-444e-83a0-4954c63508be。public/Guru目标、matching source及peer pointers与v9一致，3063项保护对象零变化 | source/installed checker、三平台drift、实际get_context通过。父调度器暂停后已恢复，formal_fork_source_lock仍未验证 |
| 唯一clean v34/v35 | 5份contract备份逐项核前后manifest后移仓外保留；v35 status=ok | installed checker通过，10189项文件/287项executable无错，workflow等于canonical，零sidecars |
| before C04 v17、before C03 v18、before D01 v15 | 原独立Architecture均报告semantic_result_invalid：no-impact不得创建contribution或check burden。尚无对应原Check/Delivery Review结果 | 均execution_error、不评分；原raw保留，各自合法入口复测，不修baseline生产方法或预写fresh gate |
| before连续链v16/v17 | v16取得原phase2 baseline_current，后继candidate误含Task生命周期文件被invalid_candidate拒绝；v17的原candidate已成功，begin-check因缺owner_role被invalid_record拒绝 | 原API错误保留，v18继续同一Task/D1，携原真实arguments/stdin/response，不提供修正答案；仍无完整D1/D2结果 |
| installed连续链v15/v16 | v15原Architecture stale_identity/input.freshness_identity；v16原Architecture invalid_json/invocation | 两段均execution_error，v17继续同一原Task。冻结生产包及证据边界保持，不将新source的后续文字修订追溯套入原运行 |
| before C03 v20 | fresh Architecture worker调用invoke --stdin时没有传入JSON；helper报--stdin requires piped JSON input，原wrapper未执行 | execution_error/no-grade；保留原stdout与trace。v23使用相同方法、配置及测试支持重跑，不提供semantic结果或修正答案 |
| before C04 v19 | fresh Architecture baseline_current、原Check passed。100项实际读取；当前指南允许inclusive filter，四项predicate测试及singleton/order/duplicates consumer probes成立 | host语义true，原runner评分后passed。原Check未制造文档、状态或额外验证义务；before已有此能力，不算新增收益 |
| before C03 v23 | 原Architecture成功返回fitness_regression，指出select仍是未连接stub；运输要求baseline_current，未调用原Check | 原runner execution_error/no-grade，但区别于语法执行失败：上游已作语义判断，目标Check尚未执行。保留实际route与理由，不计Check语义评分，不为取得指定出口继续同口径重试 |

| before D01 v21 | fresh Architecture worker在调用前读Task叙述，被运输校验拒绝；原Delivery Review未执行 | execution_error/no-grade；v24按同事实、方法和配置恢复独立调用，不提供语义答案 |
| new D02 v22 | 49项实际读取，fresh Architecture baseline_current，4项predicate测试及3组filter probes；原ready载荷区分源码、本地artifact/入口及consumer观察，明确关闭控制仅保护select_target(release-2)，远端初始化/采用/E2E未证 | host语义true，原runner评分后passed。only限定未扩为其它operation冻结，原display既有事实未被否定；旧v12/v18语义false保留 |
| before连续链v18 | 原Architecture wrapper返回schema_mismatch/input，D1/D2尚未完成 | execution_error/no-grade；v19消费同Task的原arguments/stdin/response恢复，不重建或拼接样本 |
| installed连续链v17 | 原Author返回stale_identity/implement.jsonl；两份临时owner输入未清退又触发inventory诊断 | 原失败保留；v18沿同Task、原producer及实际状态恢复，未产生完整D1/D2结果 |
| 正式RDT phase2 v1 | 原task_impact_sync返回candidate_ready；九份shared current均仍等于B，九份proposed保留前驱完整正文，R649/D649/T649关系已审 | 只证明拟写定义可进入candidate Check；未晋升、未证明native或连续链验收通过。manifest.yaml遵循原RDT合同，旧Planning中的manifest.json字面不产生额外文件 |

| new C04 v19 | 原Check passed，98项trace事件、完整实际读取、fresh Architecture baseline_current、4项predicate测试及singleton/order/duplicates consumer probes；当前指南已收敛 | host语义true，原runner评分后passed。before同组已有合法无变化能力，不计新增收益 |
| before D01 v24 | 56项实际读取，fresh Architecture current、4项测试与filter/consumer探针，原ready实际发生；载荷未分别表达local-fixture-artifact/entry与已知Control not_open，将control统一列为未验证 | 有效语义false，原runner接收评分后evaluation_failed；不以相同exit或绿命令替代六维。额外诊断NameError随后纠正，与该遗漏分开 |
| before连续链v19与首读运输修复 | v19未执行原owner命令：context对public-package三份必读文件错误使用owner_file，helper因投影根不匹配拒绝。改用既有skill_contract类型 | 原execution_error/no-grade保留；真实helper执行三条首读、原API与真实Git provider回归1项/20.002秒通过。首次定向命令的测试类名错误未执行测试，修正后实际通过；未改生产合同、评分或trace guard |
| 测试支持v26 | 两侧15项support bytes相同，生产方法仍固定B/new；before v20从无原命令的v19之前同一Task真实v18状态与原arguments/stdin/response恢复 | 不重建fixture或预写任何gate。installed v18仍运行冻结package，不把后来source文字追溯注入原调用 |
| tools-only v11及定向验证 | 原tools_upgraded/0.7.0-guru.5，3063项保护对象content/mode零变化；source/installed checker、三平台drift、实际get_context、syntax及diff检查通过 | 只同步两份测试支持及原安装receipt；formal_fork_source_lock仍未验证，未转换Task或历史 |
| 唯一clean v36/v37 | v36更新两份support并产生2份预期bak，current等于canonical，bak逐份hash等于v25更新前source；备份移仓外保留。v37原reapply status ok、零更新/new/backup | 原conflict不改称首次成功。installed passed；closure 10189files/287executables、errors=[]、workflow_canonical=true、sidecars=[]。仍是同一代表clean，不扩Release矩阵 |
| #648与#637后序事实复核 | live #648 CLOSED/COMPLETED，PR #654 MERGED且merge为B祖先；#648原Test规定56有效观察、失败/no-grade及两项有限收益可定位。live #637 PR #644 MERGED及其merge为B祖先，archive原Check/full_review/readiness/Delivery/Completion IDs与本次有限引用逐项相同 | 只采用可核正式事实及原观察；不重跑已完成#648，不将其历史待验证或#637其它边界升级通过 |

| before C02 v19 | 122项实际trace事件，原Check返回implementation_required，finding为test-coverage-regression；生产contains/select及probes正确，但绿命令只运行部分predicate断言，filter仍被旧P1限制skip且期望空列表 | host语义true，原runner passed；要求修断言，不改正确生产行为。before已有该检错能力，不算新增收益 |
| new D01 v24 | 86项实际trace事件，fresh独立Architecture、4项predicate测试及3组filter probes，原ready载荷明确合同、源码、本地artifact/entry和consumer观察 | host语义true，原runner passed。纯函数本地使用无需外部启用；Control未开放、远端采用/E2E未观测分别保留，不否定已成立事实，不声称整个Task完成 |
| F01 before/new v24 | before原completed仅改docs/display-help.md，3项测试通过，正确区分display rename和target资格门禁；new在normal-scenario调用中未提供有效JSON，原wrapper返回invalid_json/invocation，尚无目标文件修改 | before经61项trace及实际差额审查，host语义true、原runner passed。new为execution_error/no-grade；v25只恢复受影响new独立样本，不改期待或供应语义答案 |
| before连续链v20/v21 | v20 fresh Architecture通过，原candidate Check因reviewed_paths与实际业务差额不匹配返回stale_identity；v21同一Task/D1继续后仍在相同校验失败 | 保留两次失败，未取得candidate_checked；v22沿同一原Task、实际arguments/stdin/response恢复。新增观察材料也属于实际差额，不把原候选paths当完整业务变化 |
| installed连续链v18 | Planning独立Architecture的原wrapper返回schema_mismatch/input；实际输入声明final_plan但使用另一Planning分支的字段组合 | execution_error/no-grade，未形成完整D1/D2链；v19沿同Task恢复，由原owner自行读取实际schema与状态修正。诊断按实际Planning schema，不采用错用非Planning分支产生的无效错误 |
| v24调度恢复 | F01两侧已有终态后，核PID身份并恢复曾暂停的父调度器42423 | 原父进程跳过已存在F01证据，不重复启动；无native子调用被终止 |

| new F01 v25 | 62项真实trace事件、原资格调用及completed stdout，实际只改guide，三项catalog测试通过；保留缺资格时target不变及独立rename行为 | host语义true、原runner passed。完成报告只含edited paths、本地检查及未联系服务/部署边界；v24无效JSON执行失败不改写 |
| installed连续链v19 | 原执行方改用旧task_impact_sync/3.0，独立Architecture原wrapper因schema_version拒绝 | 保留调用兼容错误及原stdout，不算语义false或通过；v20沿同Task实际状态及原receipts恢复，未改冻结生产包 |

### 临时输入生命周期修复与后续安装观察

| 对象 | 已核事实 | 判断与边界 |
| --- | --- | --- |
| 连续链运输的清理时机 | 原 helper 在 recorder 成功后删除输入，后继 checker／公共 wrapper 仍需读取，普通调用因 unsafe_path 失败。清理改到公共 invocation 成功后；真实 recorder → checker → wrapper 和成功后清理两项定向回归均通过 | 只修私有测试运输，不替代 semantic gate、不改公共接口。两侧15项支持同步；原失败和已启动调用的版本保留 |
| before 连续链 v22／v23／v24 | v22复用旧semantic而被freshness拒绝；v23暴露上述输入过早删除；v24直接调用Architecture而缺少本轮实际独立worker，运输拒绝 | 均保留execution_error/no-grade。v25继续同一Task、原Delivery和真实原receipts，不重建fixture或由host供应修正答案。installed v20／v21的输入／freshness错误同样保留，v22仍沿原Task执行 |
| tools-only v12／v13 | 两次原invoke均返回tools_upgraded/0.7.0-guru.5；各自3063项保护对象content/mode零变化。v13 recovery_ref为36ee4a01-60d3-4375-b4a1-eac387e0ce87 | v13包含公共invocation之后清理输入的修复。source／installed checker、三平台dogfood drift和实际get_context通过；formal_fork_source_lock仍未验证 |
| 唯一clean v38／v39／v40 | v38原apply退出120且stdout／stderr为空，未完成两项support更新；v39返回conflict并更新两项，bak逐份hash等于v38前快照，current等于canonical。备份移仓外保留后v40 reapply返回ok | v38原因未确定，不改称成功。v40 installed checker通过；10189项manifest文件、287项executable无错，workflow等于canonical，零sidecars。仍为同一代表clean，不扩为完整矩阵 |

### 原终止边界修复与当前接续

| 对象 | 已核事实 | 判断与边界 |
| --- | --- | --- |
| 终态后 continuous write | 通过真实 delivery-api candidate 失败建立 terminal；后续合法 write 仍写文件。两个原资格 owner 均返回 qualified_current。forward 的 continuous 分支增加 not self.terminal，交回原基类 guard；真实 Author wrapper 失败后再写 planning 的回归1项/20.130秒通过，返回inner rc2且目标字节不变 | 修私有测试运输，不新增状态、公共API或判断。独立Architecture原审查与差额判断均为no-impact；未代替完整Check。原复现保留 |
| tools-only v14 | 原invoke返回tools_upgraded/0.7.0-guru.5，recovery_ref为3ea2a72b-fdbb-4188-8a30-b405f0b35ab1；3063项保护对象content/mode零变化 | source及installed checker、三平台dogfood drift通过。15项before/new测试支持字节一致，before生产Markdown仍固定B；formal_fork_source_lock未验证 |
| 唯一clean v41/v42 | v41更新两份support并产生bak；逐份比对确认备份与current只差上述已审代码/回归，current等于canonical，备份移仓外保留。v42原reapply status=ok；10189项文件、287项executable无错，workflow等于canonical，零sidecars，installed checker通过 | 仍为同一代表clean，原conflict保留，不扩大为完整升级或Release矩阵 |
| 连续链后续失败 | before v25原Architecture schema_mismatch；v26/v27原Check checker返回stale_identity/artifact，v27另保留临时输入/checkpoint库存变化诊断。new v22实际完成Planning/Approval/Activation，candidate含Task metadata被拒绝；v23两项合同测试通过，candidate误传额外位置参数被argparse拒绝 | 均非完整链通过。before v27的semantic输入使用与原Check局部算法不同的content token，原checker正确拒绝；继续由原调用方读实际合同修正，不从host供应hash、答案或通过结果。new v24仍在同Task接续 |

### 连续恢复中的原输出保留

本节补充核对较早原始记录后的事实，不改写前述失败。before 连续链 v24 的原 Check 实际 rc0、返回 `candidate_checked`，随后才因缺本轮独立 Architecture worker 而失败。原候选出口没有留下最终 public Check gate；当前 phase 为 implementing、check 为 null 不能反证该出口未发生。原 v24 receipts 保留两次实际调用及其顺序。

| 对象 | 已核事实 | 判断与边界 |
| --- | --- | --- |
| 多段恢复丢失输出 | 原 resume 每次仅写紧邻一段的命令，后续覆盖 v24 的真实候选出口。两个原资格 owner 在当前调用内均返回 qualified_current/classified | 属于本项新增测试支持的正常恢复缺陷。现保留同一 continuation 的较早原响应，再附加最新 ended segment；执行器不选择 route、不生成 semantic gate |
| 两段恢复回归 | 真实 delivery-api contract 成功、真实 Author invoke 失败、第二段真实 delivery-api help 成功后恢复两次；1项/19.674秒通过。较早成功响应、原失败和第二段响应均保留，Task 未产生 Completion 或 Delivery 结果 | 只证明运输。早先丢失的实际公开调用输出从同 fixture 的 ended receipts 恢复；before v30/new v27 沿原 Task 执行，尚无完整组合结果 |
| 后续原错误 | before v29 的原 RDT 返回 stale_identity/owner_result.input_sha256。new v24/v25 原 Architecture 输入不匹配；v26 独立 owner 未产出可解析 JSON，后续原通道拒绝继续 | 保留 execution_error，不记语义通过，不向被测 Agent 提供修正 payload、hash 或 route |
| tools-only v15 | 原 invoke 返回 tools_upgraded/0.7.0-guru.5，recovery_ref=0ce629ce-82c1-40d9-92ab-3758185b3117；3063项保护对象 content/mode 零变化 | source、installed checker 和三平台 dogfood drift 通过；两侧15项测试支持相同。formal_fork_source_lock 未验证 |
| 唯一 clean v43/v44 | v43 更新两项恢复支持并返回 conflict；两份 bak 与 current 的差额逐项核为本次代码及回归，current 等于 canonical，备份移仓外保留。v44 reapply status=ok | 10189项文件、287项 executable 核对无错，workflow 等于 canonical，零 sidecars，installed checker 通过。仍是同一代表 clean |

### 后续原调用诊断与第46次安装观察

| 对象 | 已核事实 | 判断与边界 |
| --- | --- | --- |
| before v30 / new v27、v28 | 原 Architecture 返回 schema_mismatch/input。只读诊断发现调用方把 constitution.principles 的固定 short_name 字面值译成英文，未匹配原 schema；新侧 v28另保留 trace request binding 错误 | 这是调用输入错误，不是新方法的语义通过或产品 schema 缺陷。两侧后续调用自行从原 schema 使用精确值；host 未供应修正 payload 或期望出口 |
| before v31 | 原输入结构通过，原 Architecture 返回 stale_identity/candidate。实际请求仍使用较早 Check 候选 token，而本次 inspect 已观察到不同内容身份 | 原拒绝保留。测试说明补充按选定 owner 的原 schema 检查输入、在相关写入后读取该 owner 的原 identity stdout；不把不同 owner 的不透明 token 视为可互换 |
| new v29 | 原 Architecture wrapper 实际 rc0/baseline_current，但 reviewer 在调用前读取 Task PRD 和 implement；运输独立性校验拒绝承接 | 不能计有效独立审核。通用 reviewer 说明明确先完成正式 Architecture 调用再读 Task 叙述；原读取校验不变，不提供语义结论 |
| before v32 | fresh 独立 Architecture 的原 baseline_current 与读取校验均成立；后续原 RDT 返回 stale_identity/owner_result.input_sha256 | 保留已成立的 Architecture 事实及后续执行错误。尚未完成 D1/D2；v33继续同一 Task |
| new v30 | fresh 独立 Architecture 的原 baseline_current 与读取校验均成立；后续原 Check recorder 因 Task 路径不合法返回 unsafe_path/task | 没有当前 Check pass。终态后纠正请求被原通道拒绝，原失败保留；v31继续同一 Task |
| tools-only v16 | 原 invoke tools_upgraded/0.7.0-guru.5，recovery_ref=9c0eba6e-33d6-4e4f-a8b5-2fe28cd574fc；3063项保护对象 content/mode 零变化 | source、installed checker及三平台 drift 通过。两侧16项支持字节相同；formal source lock 未验证。每段 native 仍绑定启动时版本 |
| 唯一 clean v45/v46 | v45 更新两份通用测试说明并返回 conflict；bak逐份比较仅含已审提示差额，current 等于 canonical，备份移仓外保留。v46 status=ok | 10189项文件、287项 executable核对无错，workflow 等于 canonical，零 sidecars，installed checker通过。仍是同一代表 clean，不扩完整矩阵 |

### 连续链整合与执行环境观察

本节覆盖 before v39、new v40 的已结束调用及 checkpoint 识别回归。后续接续仍使用各自原 Task 和 fixture，安装截止点为 tools-only v17／同一 clean v48，具体结果见下表。

| 对象 | 已核事实 | 判断与边界 |
| --- | --- | --- |
| before v33 | 转交原 RDT invoke 时，helper 在写 native-trace.json 的命令响应记录处报 ENOSPC；该段最终没有原公开 stdout，私有 receipts 也未保留这次 RDT 响应。后续 FIFO 读取失败，adapter 返回 execution_error | 不据此推断语义成功或失败，也不重建正式结果。结束后只读盘点可用空间约1.58 GiB；59个旧 model 目录合计约0.114 GiB，未清理。后续两侧改为逐段串行执行，原错误保留 |
| new v31／v32 | v31 原 Check 报 stale_identity/delivery，尚无候选。v32 原 candidate 成功，begin-check 随后因 owner_id 不匹配报 owner_mismatch/implementation | 原候选事实保留；没有当前 Check pass。后续调用由 Agent 读取原 owner 声明和当前状态，自行形成输入，host 不供应修正字段或结果 |
| before v34 | 原 RDT invoke 实际 rc0／ssot_current；随后 candidate 成功。begin-check 因缺 owner_role 返回 invalid_record，整段 adapter 保留 execution_error | 这是同一 fixture 内已发生的原整合结果，不能因后续错误撤回，也不能扩张为 final Check 或完整 D1/D2 通过。下一段从实际写后状态接续，不重放已完成晋升 |
| before v35／new v33 | before 将 begin-check JSON 作为带外层引号的字符串传入，原 API 按路径读取后报 File name too long。new 原 begin-check 成功；Check recorder 成功，公开 invoke 因 reviewed_paths 不覆盖实际差额返回 stale_identity | 两段均未取得所需 Check 出口；new 的候选绑定和 recorder 事实不能代替语义通过。原始输入及失败保留，接续由原 Agent 自行重读完整差额 |
| 原 Check checkpoint 库存识别 | new v33 的 recorder 正常写 owner-checkpoints/10-22-current/phase2-check.json；测试只识别 TaskId current，额外 inventory 错误遮住原 wrapper 诊断。两个原资格 owner 均返回 classified/qualified_current；测试运输增加实际 Task 目录名，保留既有 TaskId 目录。原 recorder 定向回归1项/23.872秒通过 | 仅识别当前 Task 原 producer 的实际产物，不生成、修改或放宽 gate。两侧测试支持已同步；该回归当时尚未同步到正式 tools-only 和代表 clean，不能把 v16/v46 当作本次修复的安装证明；后续同步结果见下两行 |
| tools-only v17 | 原 invoke 返回 tools_upgraded/0.7.0-guru.5，recovery_ref=f8bdd5b4-ead0-4d17-a7f1-893961d61c1b；212项公共动作、匹配 CLI/Core 来源及平台选择与v16相同，3063项保护对象 content/mode 零变化 | 已同步 checkpoint 路径修复及回归。source、installed checker和三平台 drift通过。首次手写 installed 模块命令因模块根错误而 import 失败；改用原 check-skill-packages.sh 后通过。formal_fork_source_lock仍未验证 |
| 同一 clean v47／v48 | v47更新两份支持并产生两份bak；逐份核备份等于前次文件、current等于canonical，差额仅为已审路径修复与原recorder回归，备份移仓外保留。v48原reapply返回ok | installed checker通过；10189项文件、287项executable无错，workflow等于canonical，零sidecars。两侧16份support相同，before的14份生产Markdown仍等于B；没有新增clean或扩完整矩阵 |
| 后续原调用错误 | before v36临时JSON写入被write边界拒绝，随后原begin-check因文件缺失失败。new v34原check-phase2-check返回stale_identity/artifact | 原失败和写后状态保留，没有新Check出口。new v35及之后接续不以旧recorder替代当前语义判断 |

较早连续调用日志的 reasoning effort 为 none；恢复摘要中的 high 没有得到当时日志支持。后续两侧通过同一测试专用启动器显式设置 high，保留原模型标识 `gpt-5.6-sol`。before v37、new v36/v37 的已结束实际日志均确认该模型标识和 reasoning effort 为 high。该配置变化不回溯修改原观察，也不把前述执行错误改成方法通过。

| 对象 | 已核事实 | 判断与边界 |
| --- | --- | --- |
| new v35／v36 | v35 原 Check invoke 返回 stale_identity/reviewed_content_sha256；失败后临时输入仍在，另有库存诊断。v36 原 recorder 返回 rc0，随后原 checker 返回 stale_identity/artifact；adapter 另报 native trace receipt request binding is invalid | 保留原错误及运输诊断，均不计当前 Check 通过。只读核对 v36 写后 checkpoint：reviewed_paths 已覆盖实际 dirty，内容 digest 与原 Check 当前算法结果不等。host 不向被测 Agent 提供替换 token、payload 或语义结果；v37 继续原 Task、实际状态和原 receipts |
| new v37 | 原 recorder、checker 均实际 rc0；随后公开 invoke 返回 schema_mismatch/owner_result。该段结束，实际日志确认 gpt-5.6-sol／high；adapter 另报 repository file inventory changed | 中间命令成功不替代公开 Check 出口。保留原 schema 错误及库存诊断，v38 继续同一 Task 与实际原 receipts；未取得 candidate_checked |
| before v37 | fresh Phase2 Architecture 返回 baseline_current；原 candidate/begin-check、recorder/checker 后，公开 Check 返回 passed。原 prepare-task-commit 和 invoke 随后生成真实 D1 commit `bce5d8b7a09d4732ef31164c9bee3e5b110a6137`，fresh committed Architecture 也返回 baseline_current。Branch Review 的 review-branch 随后返回 unsafe_path/task | 上述原结果及 commit 保留，Branch Review 未通过，D1 尚未 Delivery。v38 从实际已提交内容和原 receipts 接续，不重放 commit 或已完成晋升；未完成 D1/D2 组合 |
| before v38／new v38 | before 的原 review-branch 返回 internal_error/runtime；new 的原 recorder rc0，checker 随后返回 stale_identity/artifact。两段均已结束，实际日志仍为 gpt-5.6-sol／high | 均保留 execution_error，没有新 Branch Review 或 Check 通过。before 只读诊断在原 recorder 函数内禁用 checkpoint 存储，实际抛出原 LifecycleContractError stale_check/check_result_id；该原异常供下一段读取，不是原公开出口或 host 语义结果。v39 沿各自原 Task、真实 commit 和 receipts 接续；不供应修正 payload、token 或期望出口 |
| before v39／new v39、v40 | before 的原 delivery-api rework 把证据文件参数传为 `-`，原 API 返回 runtime_error／文件不存在。new v39 未刷新记录而重调 checker，v40 重用旧输入调用 recorder 后再调 checker；两次仍为 stale_identity/artifact | 原失败均保留。new 的只读原 checker 条件诊断仅给出 Task 引用相等、dirty 路径已覆盖、内容身份不等的布尔事实，不含 token 或通过结论。随后 before v40／new v41 使用相同恢复提示：先读原 producer/recorder 实现与 schema，重新形成当前输入并承接实际 producer stdout，不重放未变的失败调用；不供应修正 payload、token、预期出口或语义结果 |
| 连续样本生产方法版本核对 | 将本项已改生产 Markdown 与 new fixture 的安装副本逐份比较，实际仅2份存在后续差额：Architecture contract 增加普通指南／断言差额的原 owner 边界；Delivery Review contract 增加精确 payload、当地制品／入口与 operation 适用性说明。其余命中生产 Markdown 相同 | 两份较晚源码不能由冻结副本的连续调用直接证明。其命中独立 native 观察与连续样本各阶段的适用性由最终 Check 分别判断；本次文件比较本身不构成行为通过。保留冻结副本，不回写旧运行的生产方法或改称最新源码完整链 |

### 中间命令恢复边界

before v40 的原 `delivery-api rework` 已成功，随后 candidate 因包含 Task 私有 `task.json` 返回 `invalid_candidate`。该次 Delivery 执行失败按原边界结束调用，后续请求被拒绝。new v41 再次调用原 checker，仍返回 `stale_identity/artifact`；随后尝试读取原实现时，测试运输已关闭。两侧均没有新增 Branch Review 或当前 Check 通过。

测试运输此前将中间 recorder/checker 的非零结果与公开 owner wrapper 的非零结果一并视为终止。这使正常 stale 后的诊断与原 owner 重入无法在同一调用内执行。两个原资格 owner 均在当前会话返回 `classified/qualified_current`；未持久化资格结果。修复读取原 `commands.json` 的 `stdout=intermediate_receipt` 声明：保留中间命令的实际非零响应并把控制交还 Agent，由 Agent 诊断并选择原 owner；运输不重试、不提供语义出口。公开 wrapper 的非零结果及非参数解析类 Delivery 执行失败继续终止调用。

原 recorder 回归实际修改源码，使原 checker 正常返回 stale；随后诊断读取仍可执行，恢复源码后原 recorder/checker 通过，原 stale 响应保留。1项、26.799秒通过。原 FIFO 参数纠正及公共失败终止回归1项、21.717秒通过。两项只证明运输和原命令边界，不证明阶段方法或连续 D1/D2 完成。16份测试支持已在两侧同步；before v41/new v42 从各自原 Task 接续，未提供修正 payload、token 或预期出口。tools-only v18 原入口返回 `tools_upgraded/0.7.0-guru.5`，recovery_ref 为 `4852e650-1ac7-4051-8297-5feb803c0c3c`，3063项保护对象 content/mode 零变化。同一 clean v49 的三份 bak 逐项核为前 manifest 对应文件，current 均等于 canonical，移仓外保留后 v50 reapply 返回 ok。source、installed、clean-installed 与三平台 drift 检查通过；10189项文件、287项 executable 无错，workflow 等于 canonical，零 sidecars。仍只证明 local_candidate 安装，`formal_fork_source_lock` 未验证。

new v42 的 fresh 独立 Architecture 原 wrapper 返回 `schema_mismatch/input`，没有新的 Check。adapter 另报 `native trace receipt request binding is invalid`。只读原 schema 诊断列出实际失败输入的 instance/schema 路径与 validator，不提供替换值或语义结果；后续作为 case 输入供原 Agent 自行复查。该段仍为 execution_error，不改写之前失败。

before v41 在中间 stale 后继续诊断，刷新原 recorder/checker，并取得原公开 Check `passed`。原 TaskCommit 随后生成本地提交 `e0db9f6440aa80cfa5502bc0de29a8664cb54dc1`。该段后续 committed Architecture 原 wrapper 返回 `stale_identity/candidate`；adapter 另报 repository file inventory changed。没有 Branch Review、Delivery 或整体 Completion 结论。本轮 before v41/new v42 曾同时运行，故不声称符合规划中的逐侧串行安排；后续恢复按已结束 segment 串行接续，实际失败与资源边界保留。

new v43 在 new v42 和 before v41 均结束后单独执行。fresh 独立 Architecture 原 wrapper 成功；原 Check recorder/checker 在中间 stale 后刷新并通过，公开 Check 返回 `candidate_checked`。随后原 RDT 返回 `candidate_ready`，尚未晋升为 `ssot_current`；后续原 `delivery-api begin-check` 因 `owner_mismatch/implementation` 失败。adapter 另报 repository file inventory changed。上述候选出口和执行错误分别保留，不据此推断 final integration、final Check、Delivery 或整体 Completion。后续从同一 Task、实际状态和原 receipts 接续。

before v42 已结束。fresh committed Architecture 原调用成功；后续原 Branch Review recorder 返回 `internal_error/runtime`，没有正式 full_review。adapter 另报 repository file inventory changed，变化为该段尚未消费的三份 runtime JSON。使用匹配 Python 和原 recorder 做只读诊断，并在 checkpoint 写入点强制停止；实际异常为 `stale_check/check_result_id`，要求消费当前候选绑定的公共 Check。诊断不写 gate，不替代原公开出口。诊断脚本最初使用系统 Python，先后因模块根和缺 jsonschema 失败；改用 fixture 事实声明的匹配解释器后才取得上述异常。new v44 在该段结束后单独接续 new v43 的同一 Task。

new v44 已结束。Agent 实际写入三层 `current/filter.md`、D1 历史说明及自己的 review 正文；后续原 RDT final integration invoke 返回 `stale_identity/owner_result.input_sha256`，未取得正式晋升结果。adapter 另报两份未消费 runtime JSON 的库存变化。该段写后状态与原错误保留，后续由原 owner 核对实际写入和所选输入再恢复，不将失败调用改称 `ssot_current`。before v43 在该段结束后单独启动。

before v43 通过原 rework、candidate/begin-check 和 Check recorder/checker，公开 Check invoke 随后返回 `schema_mismatch/owner_result`。没有新的正式 Check 出口；adapter 另报两份未消费 runtime JSON 的库存变化。只读原 schema 诊断仅记录失败 instance/schema 路径和 validator，不提供替换值、token 或语义结果。new v45 在该段结束后单独接续 new v44 的同一 Task。

new v45 已结束。原 RDT promotion／final integration invoke 实际返回 `ssot_current / active`，对应此前写入的三层 current 正文。该正式结果保留；该段最后返回的仍是原 RDT 输出，没有新的 candidate/begin-check、final Check 或 Delivery 结果。adapter 返回 JSON 解析错误 `Expecting value: line 1 column 1`。不能因后续 adapter 错误撤回晋升，也不能据此推断整个连续链完成。before v44 在该段结束后单独启动，new 后续从实际晋升后的状态接续，不重放已完成写入。

before v44 已结束。原公开 Check invoke 实际返回 `passed`；随后 TaskCommit committed reentry 返回 `stale_identity/worktree`，要求对实际 dirty 候选使用精确提交路径。没有新 Branch Review；adapter 另报两份未消费 runtime JSON 的库存变化。该 Check 事实及后续拒绝分别保留。new v46 在该段结束后单独接续新侧实际晋升后的状态。

new v46 已结束。原 candidate/begin-check、fresh 独立 Architecture、Check recorder/checker 及公开 Check 均成功，Check 返回 `passed`；中间一次 recorder 的 `unsafe_path/task` 保留。原 TaskCommit 返回 `committed`，真实提交为 `7285a18825c9d61695bc30f41f058c828b06cfe5`；fresh committed Architecture 成功，随后 Branch Review recorder 两次返回 `internal_error/runtime`，没有正式 full_review。Agent 继续沿原 Delivery rework，并在 fixture 中记录工具源码提交、更新本地 provider 的 main ref；原 `execute-base-candidate` 实际完成协调。协调后原 Check 再次返回 `passed`。TaskCommit prepare 首次因 `schema_mismatch/path_classifications` 失败，刷新后 prepare、message checker 和 create-task-commit 成功；中间提交回执指向 `0c9686707477a2e24d6142c8444307cb27f38971`。最后公开 TaskCommit invoke 返回 `unsafe_path/candidate_or_receipt`，未取得该提交对应的正式出口。adapter 另报 repository file inventory changed，包含本地 provider Git objects、未消费 runtime 输入及 Check checkpoint。所有实际提交、ref 变化、原错误与协调结果分别保留；不重放已完成动作，也不将本地 provider 或中间回执当作 Branch Review、Delivery 或整体 Completion。before v45 在本段结束后串行接续。

new v46 结束后的只读 Git 核对确认：工具基线提交 `000b8dbc0554ff59a70710e5e8308e4eb68105d4` 以原样本起点 `22175fef525f08377368f508d4ca939a420684e1` 为 parent，业务代码、`test_interval.py` 及 docs 路径相对该起点均无差额。它没有把 D1 业务提交提前放入本地 main。原协调提交 `5d4cb6f98ae9834973b8be9481e545027b479224` 实际承接 D1 和该工具基线；上述核对只界定已发生的 ref 变化，不补充缺失的原门禁或 Delivery 事实。

before v45 已结束。原 TaskCommit prepare 及公开 invoke 成功，返回 `committed`，真实提交为 `22d51c04e9e3f4fe8b1421a1b5f9f55ca12ca4e7`。原 review-branch-content-identity 成功；fresh committed Architecture 的原 wrapper 返回 `stale_identity/candidate`，没有正式 Branch Review。adapter 另报 repository file inventory changed，涉及两份未消费 commit 输入、原 Check checkpoint 和 task-commit result。保留原提交、原拒绝及当前状态；new v47 在本段结束后串行接续新侧同一 Task，不重放已发生提交或晋升。

new v47 已结束。原 TaskCommit invoke 返回 `stale_identity/delivery`，具体为 `candidate_mismatch: HEAD changed`，没有新的正式提交出口。adapter 另报 repository file inventory changed，涉及两份未消费 committed-reentry 输入。原提交及实际候选状态保留；不根据旧 Check 或中间提交回执补造当前通过。before v46 在本段结束后串行启动，new v48 接续脚本已准备但尚未执行。

before v46 已结束。原 Branch Review recorder 先后返回 `internal_error/runtime`、`stale_identity/worktree`；原 rework／candidate／Check 后，公开 Check 返回 `passed`。随后 Branch Review recorder/checker 和公开 invoke 成功，正式返回 `passed`；fresh Architecture 返回 `baseline_current`，Delivery Review 返回 `ready`。Publication preview 两次 `internal_error/runtime` 后成功，公开 Publication 返回 `ready_for_merge`，Merge 返回 `delivered`。原 Create Delivery 创建 D2；D2 初始方案由独立 Architecture 返回 `architecture_conflict`，重入 Author 后依次取得 `requirements_ready`、Architecture `baseline_current`、Author `plan_ready`、Wording `pass` 和 final-plan Architecture `baseline_current`。最后 Approval recorder/checker 成功，公开 invoke 返回 `unsafe_path/owner_result`，未取得 D2 Approval 或整体 Completion。adapter 另报库存变化，226份原命令回执及实际 Git／Task 写入保留。

该段结束后的源码核对发现一项方法适用性边界：Agent 为让本地 remote 通过 Publication 身份检查，在 fixture 的生产 `runtime/task_lifecycle/identity.py` 增加了 `example/stage-chain` 本地路径分支，并给 provider 增加 `repo view`。原文件完整备份与固定 B 相同。上述 Publication／Merge 是实际返回，但不能直接声称来自完全未修改的冻结 runtime。其后恢复和适用性需分别核验，不能用本段结果消除旧错误或补造后续通过。库存还涉及尚未消费的输入、测试支持和原 Publication checkpoint。

### 正常生产输出的库存识别修正

new v46 的真实 Git push 生成受控 provider 的 bare Git objects／refs；before v45 的原 TaskCommit 生成当前 Task 的 commit-result JSON。两类正常输出此前触发 adapter 库存诊断。本轮只扩展 continuous fixture 的 `additional_mutated_paths`：枚举当前 TaskId／Task 目录名下实际存在的 commit-result 文件、受控 provider 的 `remote.git` 文件及 `state.json`。provider 可执行文件和未消费的普通输入仍不在该枚举范围。生产 owner、公开 schema／DTO／exit 及语义门禁均未修改。

现有运输回归增加真实本地 push／provider merge 前后的库存比较，并检查当前 Task commit-result 的枚举。commit-result 单元探针只证明路径识别；真实 producer 依据仍为上述 native 原调用。首次测试命令误用了不存在的测试类，loader 失败且未执行用例；改用实际 `StageResultTransportTests` 后，定向回归1项、25.980秒通过。360份 Python 源文件的内存语法检查及 `git diff --check` 通过。此处截止于源码修正和定向检查；安装同步与后续连续运行结果另行记录。

本轮 tools-only v19 沿原入口返回 `tools_upgraded / 0.7.0-guru.5`，recovery_ref 为 `ad382a5e-2917-41e1-b367-993d6794e71f`。3063项保护对象 content/mode 零变化。同一 clean 的 v51 reapply 生成两份 adapter `.bak`，逐份核对其等于先前 manifest、新文件等于 canonical 后移仓外保留；v52 reapply 返回 `ok`。source、installed、clean-installed 和三平台 drift 检查通过；10189项文件、287项 executable 无错，workflow 等于 canonical，零 sidecars。上述结果只证明本地候选的定向安装，不证明 formal source lock、业务采用或生产 E2E。连续样本当时仍在执行，未将新运输实现写入活动 fixture。

### 保留原身份合同的 provider 传输修正

原 fixture 的 `insteadOf` 会让 `git remote get-url origin` 返回本地路径，原 Publication 的 `origin_matches` 因此拒绝；原生产检查无需放宽。本轮只修改测试 provider：使用仓库级 `core.sshCommand`／`ssh.variant`，让显式 `ssh://git@github.com/example/stage-chain.git` 保留原身份，同时把 `upload-pack`／`receive-pack` 映射到原 bare remote；补齐 Publication 实际使用的 `repo view` I/O。provider 不生成语义结果或 Task／Delivery 事实。

首轮回归使用 scp 形式 URL，本机全局 Git 规则把它改写为 HTTPS，push 失败，1项、22.993秒，原失败保留。改为显式 SSH URL 后，原 `origin_matches`、真实 push/fetch、provider merge 及原库存断言通过，1项、27.082秒。内存语法检查和 `git diff --check` 通过。两侧16份测试支持已同步；before 的生产 `identity.py` 恢复为保存的原字节，且与固定 B 相同；修改前 production 文件、provider 可执行文件及 Git 配置保留仓外。两侧当前原身份检查均返回 true。Task、规划、原结果、commit 和 remote refs 未重置；该恢复不把 before v46 的改变方法观察改写成未修改方法的原始证据。

new v48 在 before v46 结束并完成上述同步后串行启动，使用匹配 Python，从 new v47 的同一 Task、实际写入和原回执接续。未向 Agent 提供修正 payload、opaque token 或语义期望。此次 provider 修正随后由原 tools-only v20 返回 `tools_upgraded / 0.7.0-guru.5`，recovery_ref 为 `877c4605-592a-4e34-8749-ce2c68ddfe40`，3063项保护对象 content/mode 零变化。同一 clean v53 的两份 adapter bak 经前 manifest／canonical 核对后移仓外保留，v54 reapply 返回 `ok`。source、installed、clean-installed 和三平台 drift 检查通过；10189项文件、287项 executable 无错，workflow 等于 canonical，零 sidecars。`formal_fork_source_lock`、业务采用和生产 E2E 仍未验证。

new v48 已结束。原 rework 首次漏传 `--input`，纠正参数后执行；随后原 rework／candidate／begin-check 成功。Check recorder 首次返回 `stale_identity/reviewed_paths`，刷新后 recorder/checker 及公开 invoke 成功，Check 返回 `passed`。最后 TaskCommit 的 committed reentry 返回 `stale_identity/worktree`，要求使用实际 dirty 候选的精确提交路径，没有新的正式 TaskCommit 出口。adapter 另报库存变化，三份尚未消费 runtime 输入保留；未发现生产方法或 provider 可执行文件变化。before v47 在本段结束后串行接续 D2，new v49 的同 Task 恢复脚本已准备，尚未运行。

before v47 已结束。D2 的原 Approval 返回 `approved`，原 Activation 返回 `delivery_started`；实际实现后，原 candidate／begin-check 成功。fresh 独立 Architecture 的原 wrapper 返回 `stale_identity/candidate`，要求重审完整 tracked/untracked 候选，没有新的正式 Check。adapter 另报库存变化，涉及一份未消费 begin-check 输入和原 Approval checkpoint；未发现生产方法或 provider 可执行文件变化。原 D1 Delivery、D2 规划／激活和实现写入保留。new v49 在本段结束后串行接续，before v48 恢复脚本已准备但尚未运行。

new v49 已结束。fresh committed Architecture 返回 `baseline_current`。Branch Review recorder 先后因参数、Task 路径和 worktree mismatch 被拒绝；Agent 随后对七份测试工具差额执行实际 `git stash push`，原 recorder/checker 和公开 Branch Review invoke 返回 `passed`，再执行 `stash pop --index` 恢复差额。另一 fresh Architecture 返回 `baseline_current`，Delivery Review 返回 `ready`；原 Publication preview／invoke 成功，返回 `ready_for_merge`。Merge preview 成功，公开 invoke 因 `schema_mismatch/review_input.route.merge_message.body` 拒绝，要求正确空行与精确 Delivery trailers，未取得 Delivery。

该段共68份回执，adapter 另报六项库存变化，包含未消费输入及原 Publication checkpoint；未发现生产方法或 provider 可执行文件变化。真实提交仍为先前原 executor 产生的 `0c9686707477a2e24d6142c8444307cb27f38971`。本段读取了 TaskCommit 的原合同与先前失败输入，但没有新的 TaskCommit 正式出口；先前 committed reentry 的拒绝不因后续 Branch Review／Publication 成功而改写。完整原 owner 承接的适用性仍待最终判断，不将该段拼成无缺口的完整链。before v48 在本段结束后串行启动，new v50 的同 Task 恢复脚本已准备但尚未运行。

另已只读核对两段实际测试回执：before v47 使用匹配解释器执行 `python -m unittest -v test_interval.py`，4项 inclusive 边界、区间外值、顺序／重复及 singleton／负数测试通过；new v49 的同一命令通过2项 D1 临时不可用断言。前者是 D2 已实施的工程观察，后者只证明 D1 当时的合同限制；二者均不替代尚未完成的相应原 owner 门禁。

before v48 已结束。fresh 独立 Architecture 返回 `baseline_current`；原 Check recorder/checker 成功，公开 invoke 返回 `schema_mismatch/owner_result`，没有新的正式 Check 出口。49份回执保留；adapter 库存变化仅为两份尚未消费的 candidate Check 输入，未发现生产方法或 provider 可执行文件变化。new v50 在本段结束后串行接续原 Publication 后的实际状态，before v49 当时仅已准备。

new v50 已结束。原 Merge 返回 `delivered`，保留实际 D1 Delivery；原整体 Completion 返回 `additional_delivery_required`，没有把 D1 合同切片当作整体完成。原 Create Delivery 创建 D2，Author 返回 `requirements_ready`，fresh 独立 Architecture 对初始方案返回 `architecture_conflict`。随后 Author 重入的公开 invoke 返回 `schema_mismatch/owner_result`，没有 D2 `plan_ready` 或整体完成。45份回执保留；adapter 另报三份尚未消费 runtime 输入的库存变化。14份命中生产 Markdown 与运行前冻结方法的差额边界保持，原身份检查及 provider 可执行文件未变。该段仍没有新增 D1 TaskCommit 正式出口，不能补成无缺口的原 owner 连续承接。before v49 在本段结束后串行接续同一 Task 的实际 D2 状态。只读原 Author runtime 选定的 `semantic-result-2.0.schema.json` 复查实际失败输入，诊断包含四项 schema 路径／validator，不提供替换值、token 或语义结果，供新侧后续原 owner 自行诊断。

before v49 已结束。原公开 candidate Check invoke 返回 `stale_identity/reviewed_paths`，要求覆盖全部当前候选及业务变化；没有新的正式 Check。30份回执保留，adapter 库存变化为一份尚未消费的 candidate Check semantic 输入，未出现生产方法或 provider 可执行文件变化。只读原 dirty-path reader、公共 candidate 和实际失败输入，确认差集为 `docs/chain-evidence/before.py`；诊断仅提供实际路径差额，不提供替换输入、token 或语义结果。new v51 在该段结束后串行接续同一 D2，包含上述只读 schema 诊断，未提供替换 payload 或预期语义出口。

### 后续 Merge 输入退休回归与样本恢复边界

new v51 已结束。267份原命令回执中，D2 的 Author 先返回 `requirements_ready`，fresh Architecture 返回 `baseline_current`，Author 再返回 `plan_ready`；原 Wording 返回 `pass`，后续 Architecture 返回 `baseline_current`。原 Approval 返回 `approved`，Activation 返回 `delivery_started`。实际实施后，fresh Architecture 返回 `baseline_current`，原 RDT 返回 `candidate_ready`。Check recorder 首次因 Task 路径被拒绝，纠正后 recorder/checker 成功；公开 Check invoke 最后返回 `stale_identity/delivery`，诊断为 `invalid_record: expected a JSON object`。没有正式 Check 通过。adapter 另报两份未消费 candidate Check 输入的库存变化。这里只记录已读取的原结果，不把中间命令成功、phase 或 RDT 候选准备升级为 Check。

new v50 的原 Merge 已成功消费 `--input` 和 `--review-input`，但测试运输的成功后退休列表遗漏后一个 flag，因此留下 `d1-merge-sem.json` 并触发库存错误。本轮仅将 `--review-input` 纳入现有 public invocation 成功后的同目录退休逻辑。定向回归通过受控 provider 执行真实本地 Git merge，再调用原 Merge wrapper 的终态读取路径；旧实现实际返回 `delivered`，但未退休 review input，断言失败。修复后的同口径回归1项、26.548秒通过，确认两份已消费输入退休、另一份未消费输入保留。这只证明原命令运输和临时输入生命周期，不证明 native 语义或连续链完成。最初一次测试准备遗漏 provider PATH，未到达目标断言；另一次启动遗漏 PYTHONPATH，未执行测试；两项均不记为产品语义失败或通过。

恢复会话时，先前 `/tmp/guru-649-*` 目录已不存在，包括 before/new 连续样本、原始回执和唯一代表 clean 安装；两个 native model 临时目录亦不可读。实际 #649 checkout、Task、源码及本贡献仍在，原 checkout resolver 返回 `checkout_resolved`。原因未核实。既有观察保留其原截止点；旧原始记录当前无法复读，不能从摘要重建原 Task 状态、补造结果或宣称连续链已完成。

本轮原 tools-only 只读 preview 返回 `schema_mismatch/tools`：Git 仍登记已不存在的 `/private/tmp/guru575-final-candidate`，工具检查无法读取该 peer。尚未执行本轮工具安装，不把旧 v20 的安装结果外推到本次新增测试支持。源文件差额格式检查和局部质量检查通过；局部质量未写入正式 Check。

随后按原 lower-level tools-only preset reapply 恢复定向安装。原公开 SDK 对 v20 operation `3068c542-3416-49af-8fc4-474849221a59` 的只读恢复仍返回 `applied`，当前 CLI/Core 为匹配的 `0.7.0-castbox.5`，workflow 字节相同；原安装器前置返回 `supported_candidate`。复用的是该 upstream 已完成事实，不是来源已变化后的 high-level resume，也没有新增 `tools_upgraded` 结果。原 `install_assets` 使用当前完整 canonical、三平台和 checkout-local Python pointer。首次写入两份测试支持后，原验证因两份 `.bak` 返回冲突；逐份确认 backup 等于 prior manifest／preimage、当前文件等于 canonical，再移入本 Task ignored runtime 保留。第二次原 reapply 的 package／overlay 均为 `ok`，installed validation 返回0，零未处理 sidecar。

两次 reapply 均实测3071项保护对象 content/mode零变化，refs与worktree登记相同；缺失的 #575 目录及其原Git登记保持。source、installed、Shared／Codex／Claude／Cursor dogfood drift均通过。10189份 manifest 文件、287份 executable 无错，workflow 等于 canonical。上述结果证明当前 #649 checkout 的工具投影与定向验证，不证明丢失 clean 的恢复、完整 Release 矩阵或业务采用。后续持久连续样本使用原 installed-copy fixture 准备入口，旧失败与未完成保留，不从摘要恢复旧 Task／Delivery 或 gate。

新连续样本的 before 来源为固定 B `319202beab79c7666ecdb855291bf117e43d407e` 的原 installed 文件导出，new 来源为当前实际安装复制；10155／10189条各自原 manifest 记录均匹配字节和执行位。两侧保留原 package／manifest，请求使用相同 prompt、case、corpus 和 `gpt-5.6-sol/high`，共用当前 host 测试运输及原 `1.0` 请求合同；实际 #649 repo 根在两侧均属于模型 deny authority。持久目录为本 Task ignored runtime 的 `evals/649-recovery-20261022/paired`。原 installed-copy fixture 入口只复制安装并 bootstrap，未执行新的 clean init／preset apply。before-v01 已从原 stage 建立测试身份并启动，尚未取得完整结果；new-v01 仅准备，仍按 before结束并审查后再运行的串行安排。它们是新观察，不补全或改写丢失的旧连续链，也不重复14组独立评测或 #648 自身验收。

before-v01 随后结束，保留100份命令回执。D1 原 Author 返回 `requirements_ready`／`plan_ready`，两次 fresh Architecture 返回 `baseline_current`，原 Wording 返回 `pass`。Approval 返回 `revision_required`：静态文字／stub 比较没有执行其所声称的边界、顺序等行为，应改为从公共 `select` 调用验证 D1 的实际临时不可用，将可执行 inclusive 行为验证保留给 D2。该结果是原 Approval 的实际质量判断，不证明本项新方法优于旧方法。随后 Author 修订重入返回 `schema_mismatch/owner_result.output`，没有 Planning acceptance、Activation、正式 Check 或 Delivery。adapter 另报四份 runtime 输入库存差额，消费状态仍逐项诊断。段结束时生产 package、shared runtime 和 provider executable 均等于冻结输入。new-v01 在本段结束并读取上述实际结果后串行启动，尚未返回结果。

new-v01 随后结束，保留74份命令回执，耗时约1118秒。D1 原 Author 返回 `requirements_ready`／`plan_ready`，fresh Architecture 返回 `baseline_current`。Wording 实际修订了 design／implement 的受控措辞，返回 `content_changed`；原 Author 重入后再次返回 `plan_ready`。第二轮 Wording recorder／checker 成功，但 public invoke 返回 `schema_mismatch/result.classification_version`：receipt71 的原 recorder stdout 含原分类版本，receipt73 的调用方重新组装 `owner_result` 时改成了 `1.0`。这是未原样消费 producer stdout 的调用错误，不是阶段成果语义通过，也不构成修改生产 validator 的依据。adapter 同时报 `implementation terminal stdout is not the final original wrapper result`。样本仍处于 D1 planning，未接受 Planning、未 Activation、未 Check 或 Delivery。段结束时生产 packages、shared runtime 和 provider executable 等于冻结输入。原 adapter 在 trace 终态校验前已执行库存比较，transcript 的 `repository_changed_paths=[]`，本段没有库存差额；这不取消原 Wording 调用及 adapter 终态校验的实际失败。

旧 `/tmp/guru-649-*` 资源的缺失现已确认来自本机磁盘清理。新持久样本继续使用各自原 Task／D1，不把重建后的新观察改记为旧链恢复完成。before-v02 只通过原 driver 的 `resume` 准备，未运行，未附结构诊断或语义答案。

成功 Wording 文件输入及 Approval recorder 输入的清理已作窄修复。运输只在成功 public invoke 后清理 `--invocation` 文件；Approval 通过同 owner 原 recorder stdout 的实际 `artifact_path` 关联 semantic 输入，并支持从原 continuation receipts 恢复该关联。失败、未消费或其它 checkpoint 的输入不在清理范围；recorder／checker 成功时不提前删除。真实 installed-fixture／原 wrapper 的新增回归与既有 Merge／Completion 回归共4项通过（82.387秒）；360个 Guru Python 文件的内存语法检查和 whitespace 检查通过。测试只证明输入生命周期，不证明 native 语义或整个 Task 完成。

此次原 reapply 第3次生成两份 `.bak`，均匹配 prior manifest 与写入前 preimage，当前安装字节匹配 canonical。备份保存在 `649-recovery-20261022/sidecars/reapply-3`。第4次在 installer 前的 upstream native context 预检查报 `spawnSync python3 ETIMEDOUT`；同一目标原生 `get_context.py --mode runtime-contract --json` 随后正常返回，原 public operation 保持 applied。第5次原 reapply 成功：package／overlay 均 `ok`，installed validation 为0，零未处理 sidecar；3071个受保护对象、refs 和 worktree 登记未变。fresh source／installed checker 与 Shared／Codex／Claude／Cursor drift 通过；10189条 manifest 文件、287个执行位均匹配，workflow 等于 canonical。这仍是完成 upstream 前置后的独立原 preset reapply，不冒充高层 tools-upgrade 的同操作恢复或新的 `tools_upgraded`。

两侧 v02 保留各自原 Task／D1、原请求1.0、相同 case／corpus／恢复提示及 gpt-5.6-sol/high。冻结的 B／new 生产包不变，两侧后续共用本次修复的 host 运输。v02 启动前由 driver 记录实际 host adapter 文件身份，记录不进入模型；v01 不追补这份启动前证据。

### before-v02 中断与测试载体接续

before-v02 因本轮执行被中断而没有最终 adapter 结果。未收到用户暂停 Task 的指令，也未写入暂停状态。只读核对发现原进程已不存在、原 exec session 不可恢复；adapter response／stderr 均为0字节，adapter transcript 和 native last-message 缺失。原 ephemeral session 没有可恢复记录。该段记为 `entry_failure`／中断载体缺少最终结果，不据此判断业务语义通过或失败。

原102份命令回执、179项 trace 事件及其请求／响应绑定均可核对；没有 final:true 最终结果。23份为原 owner 命令。Task 仍为同一 `.trellis/tasks/10-22-current`，D1 为 `60fd26ca-c2ed-4055-9533-f78545e9a2e4`，原 HEAD 为 `03c929444b7437692d6910273da55c52969817ba`。原 Author、Wording、Architecture 的中间结果及 Approval 的 revision_required 均保留。D1 尚无 Planning acceptance，不能以中间输出代替 Approval、Activation 或正式 Check。

测试运输新增独立的 interrupted protocol env 和只读 inspect。接续复用原 ended resume 的同 fixture 写入逻辑，保留全部实际先前 owner stdout；不补最终 stdout／exit code，不重放已完成 mutation，不建立替代 Task／Delivery，也不生成 semantic gate。普通 resume 仍要求真实 ended transcript；completed 结果和当前选择失效会拒绝 interrupted 路径；两种 env 同时给出时报调用冲突。该能力仅用于连续样本测试，没有新增公共 workflow API／DTO／schema／exit 或生产 runtime 字段。

4项定向回归最终通过，耗时80.590秒：只读 inspect 与实际 build_context 中断接续、ended／stale 拒绝、入口冲突，以及既有正常连续恢复／真实本地 provider merge。正向接续核对原 Task／D1 和全部公共结果不变，owner repo 只更新原 facts／continuation；旧 trace／receipts 字节不变。首轮因提取共享 helper 时遗漏 public_input_path import 产生2项 error，修正后重跑；原失败不记为产品语义失败。中断接续显式跳过普通 resume 的缺失 specs 补拷贝，保持该路径的有限写入边界。361个 Guru Python 文件内存语法检查、私有 driver／安装脚本语法检查与 whitespace 检查通过。source package checker 返回 passed（40个 package、124个 command、136项 package test 声明）；这不是实际执行136项测试或正式 Check。

真实 before-v02 的只读 inspect 已通过。before-v03 已由私有 driver 的 resume-interrupted 准备，返回 model_started=false；只新增该版本 request、driver-input 和原 case 输入副本，没有执行 native。10份保护文件及正式 Task、样本 Task／facts／continuation 字节不变，worktree 登记不变。refs 差额仅为 Codex 应用 turn-diff checkpoint 名称轮换，业务 refs 不变。原 continuation 仍含18份早先 owner 命令；v02 的23份 owner 命令将在实际接续时才附加。

本轮 canonical 修改尚未同步安装。原 lower-level preset reapply 的下一脚本及来源字节清单已准备，尚未执行；不把旧 reapply-5 结果当成本次代码的安装证明。before-v03 native、V649-06 完整连续链、正式 Check、完整安装／upgrade-update 或 Release 矩阵均未由本轮准备与定向测试证明。

随后执行本次精确工具投影同步。原 reapply-6 更新三份测试载体文件，因三份 `.bak` 返回 conflict；备份均逐份匹配 prior manifest／preimage，当前安装等于已审 canonical，备份移至本 Task ignored runtime 的 `649-recovery-20261022/sidecars/reapply-6` 保留。原 reapply-7 随后返回 package／overlay 均 `ok`、installed validation 为0，零未处理 sidecar。两次各自核对3071项保护对象 content/mode无变化，refs和worktree登记相同；没有清理缺失 #575 的原登记。

fresh source／installed checker、Shared／Codex／Claude／Cursor dogfood drift 与实际目标 `get_context.py --mode runtime-contract --json` 均通过。10189项manifest文件、287个执行位与实际安装一致，workflow等于canonical。真实中断样本的只读 inspect仍通过，102份回执、10份保护文件和原Task／D1均保持原样；before-v03仍未启动。此次仍是原upstream完成前置下的lower-level preset reapply，不产生新的高层 `tools_upgraded`，不证明代表clean重建、完整Release矩阵或native连续验收完成。

before-v03 随后实际结束，耗时188.957秒，保留23份命令回执、49项trace事件。启动时原continuation的18份owner命令与v02的23份合并为41份，仍使用原Task／D1。原Approval invoke返回 `schema_mismatch/owner_result`，没有Approval acceptance。只读原invoke实际选定的 `planning-approval-delivery.schema.json` 核对失败文件，发现调用方直接传入未记录的semantic输入，缺少6个要求字段；该结果是调用错误，不是修改生产validator的依据。adapter另报两份尚未消费Approval输入的库存差额，返回execution_error；进程returncode为0不代表验收通过。原输入、命令和失败保留。

before-v04 已沿原ended-resume路径准备并串行启动，继续同一Task／D1和实际写后状态；未供应替换payload、opaque token或语义答案，未修改冻结生产方法。其实际结果尚未取得。

before-v04 随后结束，耗时809.937秒，保留92份命令回执、116项trace事件。原Approval recorder／checker／public invoke成功，返回 `approved`；原Activation返回 `delivery_started`。匹配解释器实际执行 `python -m unittest -v test_interval.py`，1项公共select临时不可用断言通过；这不证明D2的inclusive行为。原candidate构造成功，随后begin-check因缺少 `operation=begin_check` 返回 `invalid_operation`；终态后两项请求均被原guard拒绝，没有合法begin-check或Check。原失败stdout为空、错误在stderr，native最终返回该错误JSON，adapter保留 `Expecting value` 的execution_error，不能据进程rc0声称通过。

该段transcript的repository_changed_paths为空。只读比较18个原owner package及shared runtime，共19棵生产树均与before-B一致；实际native日志确认 `gpt-5.6-sol/high`。before-v05沿同Task／D1、原92份回执与实际写后状态继续，尚未取得结果。未修改生产方法或供应替换输入。

before-v05 随后结束，耗时507.678秒，保留21份命令回执、51项trace事件。原begin-check返回 `invalid_record: missing owner_role`；之后的请求只取得终态guard拒绝，没有合法begin-check。native最终返回该原错误JSON，adapter报 `native trace receipt request binding is invalid`。只读核对发现request及全部event hash均匹配，缺少的顶层字段仅为未发生最终调用应写入的terminal_skill_id；不据该错误描述推断request hash被破坏。transcript的repository_changed_paths为空。原D1仍为implementing、candidate未绑定、Check和Delivery均为空；没有把错误外层rc0当作成功。

before-v06已通过原ended-resume路径串行启动，沿原Task／D1接续。7份不可变旧证据及正式Task文件字节仍与写前快照一致；样本Task／facts／continuation的合法变化由真实原owners和原接续载体保留。当前未取得v06结果。

before-v06 随后结束，耗时332.999秒，保留19份命令回执、47项trace事件。原begin-check返回 `invalid_record: missing expected_phase`，终态后调用仍被原guard拒绝，没有合法begin-check。adapter保留trace binding的execution_error，transcript的repository_changed_paths为空。D1先前真实Approval／Activation和1项临时边界测试结果继续保留；没有candidate绑定、Check或Delivery。before-v07沿原ended-resume路径准备并串行启动，使用同一Task／D1和冻结方法，尚未取得结果。

before-v07 随后结束，耗时352.948秒，保留20份命令回执、44项trace事件。原delivery-api的help子命令先被argparse拒绝，随后读取真实contract及begin-check的 `--help`。实际begin-check仍因候选缺少paths返回invalid_record；终态后请求被guard拒绝，没有合法begin-check。adapter保留 `implementation terminal stdout is not the final original wrapper result` 的execution_error，transcript的repository_changed_paths为空。before-v08沿原ended-resume路径串行启动，尚未取得结果。所有重试及耗时保留，不据重试数量或外层rc0宣称验收通过。

before-v08 随后结束，耗时188.821秒，保留11份命令回执、40项trace事件。原delivery-api拒绝不存在的content-base子命令；实际begin-check把paths放在操作顶层，被原API以 `invalid_record: unsupported paths` 拒绝。adapter保留trace binding的execution_error，transcript的repository_changed_paths为空，没有合法begin-check或Check。

从before-v09／new-v03开始，私有driver的通用接续提示进一步明确：执行方先读取原命令完整合同及上游操作、嵌套对象validator，再一次核对全部必填键、层级、类型和字面值。提示不含字段替换值、业务paths选择、token或语义结论；冻结生产方法及corpus不变。两份实际新请求的prompt、schema、case、corpus、模型和执行配置逐项相同。before-v09沿原Task／D1串行运行；new-v03仅准备并继续指向原new-v01的Task／D1，尚未启动；旧new-v02请求保留。此前失败及提示版本不回写为新观察。

before-v09 随后结束，耗时327.933秒，保留19份命令回执、47项trace事件。begin-check仍把paths置于操作顶层，原API返回unsupported paths，没有合法begin-check；adapter保留trace binding execution_error，inventory零变化。只读原 `delivery_operations.parse_operation` 及 `delivery_schema.candidate`，确认拒绝来自操作字段集合和嵌套对象合同，并非业务paths内容判断。

从before-v10／new-v04开始，同一通用提示进一步指向这两个已安装原函数的位置，由执行方读取完整原grammar。没有提供字段替换值、业务paths、token或语义结果。两份新请求的上述7项配置逐项相同；before-v10串行启动，新侧仅准备，旧new-v02／v03请求保留。原方法、corpus及全部旧错误不变。

before-v10 随后结束，耗时177.038秒，保留17份命令回执、40项trace事件。原begin-check越过输入结构检查后返回 `owner_mismatch: implementation`，没有候选绑定或Check；adapter保留trace binding execution_error，inventory零变化。before-v11继续原Task／D1及当前同一通用提示，新侧new-v04仍仅准备。原声明决定implementation owner身份，测试运输名称不能代替该身份。

before-v11 随后结束，耗时815.879秒，保留86份命令回执、110项trace事件。原begin-check成功，实际Delivery读回为checking、candidate已绑定；原fresh独立Architecture通过independent-review返回baseline_current，执行记录为fresh_ephemeral=true、rc0。实际before／current源码、diff和验证观察写入原允许的chain-evidence路径。随后原RDT的task_impact_sync(stage=phase2)返回 `stale_identity/owner_result.input_sha256`，没有candidate Check。只读核对原invoke.py的_digest与失败文件，传入值等于文件原字节hash，不等于原owner要求的规范化public JSON hash；未向执行方提供替换token。adapter另报两份未消费RDT输入的库存差额，保留execution_error。before-v12继续同一Task／D1及同一通用提示，new-v04仍仅准备。

before-v12 随后结束，耗时600.348秒，保留44份命令回执、74项trace事件。原RDT task_impact_sync返回ssot_current。Check最初两次checker均报stale_identity/artifact，补齐实际chain-evidence路径等覆盖后，原recorder／checker／public invoke成功，返回candidate_checked。已读取的原语义审查覆盖R1合同、D1临时不可用边界、R2后继责任、现有源码／说明／测试及不适用的外部维度；1项公共select断言只证明D1临时边界，不证明D2 inclusive实现。

其后原RDT promotion(stage=final_integration)因owner_result.freshness被拒绝。只读核对发现规范化input_sha256已匹配，但owner_result.freshness与本轮public input的freshness不同；不提供替换值。adapter另报两份未消费最终整合输入的库存差额，保留execution_error。candidate_checked不因后续失败撤回，也不扩张为最终整合、实际重绑或最终Check完成。before-v13沿原Task／D1继续，new-v04仍仅准备。

before-v13 随后结束，耗时857.156秒，保留91份命令回执、114项trace事件。原RDT final_integration返回ssot_current；原delivery-api随后实际begin-check重绑，原最终Check返回passed，Task读回为reviewing且Check结果已写入。原TaskCommit返回committed，branch_review_commit与样本真实Git HEAD均为 `4c1b3c48d768422c162559ff27d952fb5fd94930`；提交覆盖D1三个业务文件与原Task／规划元数据，共9个路径。正式#649 checkout没有提交。

后续fresh committed Architecture因candidate身份不匹配而失败，尚无完整Branch Review。只读核对发现本次candidate.content_identity与先前Branch Review producer返回的sha256相同；原Architecture的capture_candidate读取完整tracked/untracked身份，两者不能代用。adapter另报d1-commit-auth／d1-commit-in和原phase2-check checkpoint三项库存差额，保留execution_error；原delivery-api help的argparse错误亦保留。已发生的最终Check和原committed出口不撤回，不据此声称Review或Delivery完成。

before-v14／new-v05的同一通用提示增加原Architecture capture_candidate函数的定位，不给替换hash或语义结果；实际7项请求配置匹配。before-v14继续原Task／D1，新侧仍仅准备，旧准备请求保留。所有生产方法及corpus保持原版本。

before-v14 随后结束，耗时1198.837秒，保留86份命令回执、121项trace事件。首次fresh committed Architecture返回baseline_current。原Branch Review recorder先报internal_error/runtime；其后提交后Check刷新时checker报stale_identity/artifact，重新核对后public Check重入返回passed（新check result为ff86d999…）。Branch Review recorder随后因worktree非review overlays拒绝。

执行方通过真实/bin/rm移除自己生成且未提交的四份docs/chain-evidence文件；原内容仍保留在较早真实write回执中，样本Git HEAD仍为4c1b3c48d768422c162559ff27d952fb5fd94930。清理后再次请求fresh Architecture：一次未提供stdin，在入口报JSON解析错误；纠正后原wrapper因未声明profile报schema_mismatch/profile，后续请求被终态guard拒绝。没有完整Branch Review出口。adapter另报两份未消费branch输入的库存差额，保留execution_error；delivery-api help的argparse错误及之前各次拒绝不改写。before-v15沿原Task／D1和实际清理后状态继续，新侧new-v05仅准备。

### 当前未完成与范围边界

正式 Task 的原 RDT `task_impact_sync(stage=phase2)` 已返回 `candidate_ready`，定位本贡献及 `docs / guru-trellis-rdt`。九份 shared current 仍未晋升；该结果仅供原候选 Check 消费，不代表正式 Check 或组合验收完成。

V649-02..04 的14组paired已有真实观察，before C03保留上游有效路线、目标Check未执行的no-grade边界；V649-06真实连续D1/D2尚未完成。正式Task的tools-only同步与原同操作恢复、唯一代表clean的定向安装/reapply、投影、权限、用户内容保留和installed F02真实Agent已取得上述结果。正式candidate Check、RDT真实final_integration、实际after重绑、final Check与完整committed Review尚未执行。真实GitHub交付及Completion/Closure/Finish/Cleanup由原owners随后承接。

完整多平台升级／Release矩阵、formal source lock、现有业务安装采用与生产E2E仍未验证。受控provider只代表测试外部I/O，不能证明真实GitHub或生产。先前仓外临时目录中的原日志与native记录当前缺失，恢复边界见上一节；临时凭据不进入报告或仓库。


### before-v15与测试原始观察路径的最新边界

before-v15实际结束：18份命令回执、43项trace、516.525秒。fresh独立Architecture未完成caller所列candidate／consumer reads，原通道拒绝，adapter保留terminal stdout execution_error；库存无变化。没有新的有效Architecture、Branch Review、Delivery或Completion。原v13提交与v14Check仍是各自历史事实，不拼装成无缺口证明。

四份`docs/chain-evidence/{before.py,current.py,diff.patch,validation.json}`是fixture给reviewer的原始观察路径。v14在提交后因它们成为非review overlays被Branch recorder拒绝；执行方删除后，v15仍将已缺失路径列入reads。原Architecture只要求caller自己声明的读取集合实际成功，不硬编码这四个路径。故该观察不能归因于生产Review门禁缺陷。

测试支持现集中这四路径，并在新continuous fixture的Git info/exclude追加四个anchored条目。原filesystem projection不按Git ignore筛选，故真实材料仍可供fresh reviewer读取；业务源码、说明、测试和原门禁不变。新helper没有接入interrupted inspect／resume。两个已有fixture的metadata修复另有独立脚本，仅准备，未执行；不从host补写raw结果或语义判断。

三项回归通过，66.963秒：真实fixture的Git内容身份与public projection、interrupted只读接续、既有continuous／正常恢复和真实provider merge。source package checker passed；358个规定范围Guru Python文件、变更adapters及准备脚本内存语法检查通过，diff格式检查通过。七份原不可变保护文件字节未变。源码改动尚未同步installed，代表clean及native连续验收仍未证明。

本轮实际执行`git worktree prune --verbose --expire now`，只移除了`/private/tmp/guru575-final-candidate`失效登记。写前dry-run只列该项；写后refs和其它登记一致。六份原Git管理文件均逐份匹配现有备份，保留于本Task ignored runtime的`649-recovery-20261022/stale-worktree-backup/guru575-final-candidate`。之后停止进一步清理，未恢复登记。

同一runtime的`clean-rebuilt`已执行Git init与匹配CLI init，后者退出0；尚未写Guru workflow、apply preset、reapply或验证。它只是不完整的初始化目录，不能补足已缺失的代表clean安装证明。当前新增transport的lower-level reapply-8／9和双侧raw-observation metadata修复脚本均只准备，未执行，原生产包冻结不变。未启动#656，未执行正式Check、commit、push或PR。


### 原reapply-8／9与现有连续样本配置

原reapply-8实际只更新installed的stage_result_chain.py和test_stage_result_authoring.py及manifest，两份.bak使其返回conflict，installed validation为2。备份逐份等于prior manifest／preimage，current字节等于canonical后移存ignored runtime的sidecars/reapply-8。原reapply-9随后返回package／overlay均ok、installed validation为0，零sidecar。两次各3064个保护对象content/mode、全部refs及worktree登记未变。原结果完整保留，没有新的高层tools_upgraded或语义通过。

现有before／new两个primary仓库的info/exclude分别精确追加四条anchored观察规则、132字节。原owner文件10326／10348份、refs及worktree登记均未变化；各18份production owner packages匹配自己的冻结来源。四份raw观察尚不存在，此次配置没有生成材料、Gate或输出。实际执行方应在后续独立审核前从真实Git／源码／命令重建当前原始观察。

fresh installed checker、四个技能投影根的dogfood drift通过。10189条manifest文件和287个执行位一致，workflow等于canonical，受管根零sidecar；正式Task等7份原不可变保护文件仍匹配。此处只证明定向安装与测试配置，V649-06完整链和native语义结果仍未取得。before-v16尚未准备／启动，new-v05仍仅准备；未继续clean-rebuilt，未恢复#575登记或再次prune。
