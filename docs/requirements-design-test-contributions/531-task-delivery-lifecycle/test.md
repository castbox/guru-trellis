# #531 验证与未验证边界

状态：本地实施候选的 draft；未通过完整 Phase 2，未完成联合验收。
本文件独占实际结果，规划文件保留当时准入快照。
首轮历史 candidate：ce36314b1ef5b44230883af9c1139a6244c13155 / API 1.0 / schema 2.0。
下表至“安装与恢复证据边界”均保留首轮实际结果，不重标为当前 077 验证。
B05 为 ce363 真实历史失败；当前候选及已观察结果见本文最后的新候选段落。
PR #32 当前 MERGED，merge 6e3ccc8d6d9e71dbcd77fbe6d945599e5f4f9b7f；
首轮读取时上游 #31 OPEN（历史）。Guru candidate 尚未提交，结果只适用于当轮工作树快照。

| Test | 已观察结果 | 剩余边界 |
| --- | --- | --- |
| T531-01 canonical | 最终 source package validator 37 active / 110 commands / 117 package-test 资产盘点 PASS；正式输出→唯一 consumer、reason relay、相对 schema refs 共 3 项 PASS；生产 manifest v5 schema PASS | 117 是资产数，不是 117 项测试执行通过；不是完整 semantic Phase 2 或所有 suite PASS |
| T531-02 多 Delivery | 显式 reviewed installed upstream projection 9 项 PASS；D1/D2 独立 identity/plan、明确 selection、Task identity 和 session 保留 | 两次 Guru 实际 GitHub 全链与联合 exact candidate 未完成 |
| T531-03 返工/退出 | 公共合法 planning rework 保留 candidate；实施 owner withdrawal/release/retry PASS；Activation 4 项含 planning withdrawal PASS；installed 整合 15 项包含 Check 与后续原 stage owners 的 withdrawal、stop/release 和输出丢失恢复 | Check stop/resolved 两个 production eval 的真实出口与确定性断言通过，仍缺 external semantic grading，整体 run 为 evaluation_failed；完整旧数据 scope 迁移未验证 |
| T531-04 clean/dirty | 正式本地 wrappers 证明 clean 同 HEAD 首次完整 Review、dirty 精确提交及 lost stdout、无重复提交，公开结果适用性改变时 stale | #444 旧 Task 形态 installed 接续依赖 D2，不等于原会话恢复 |
| T531-05 历史/事务 | 本地 provider 只读响应样本验证：Merge 已成功而投影失败后恢复零 merge；Publication 历史成功且当前 gate 缺失时先记录历史、返回 review_stale；first-parent/history 5 项 PASS | 实际远端 Publish/Merge 未执行；样本不能证明 GitHub 成功 |
| T531-06 整体收尾 | TaskLifecycle 152/152、Reconcile 39 runtime+7 contract PASS；Closure 16、Finish 56、Reactivate sealed Finish/adopt/provision/output loss 2 项 PASS；无 currentDelivery Completion/Closure 本地样本 PASS | 整体 accepted scope 未完成，无本 Task 正式 Completion/Closure/Finish |
| T531-07 installed/platform | 一份受控 clean target：真实固定 CLI `init --workflow native-delivery-v1 --codex --yes` 后使用未发布 canonical Guru workflow/preset；最终 installed validator 37 active / 110 commands / 8005 package managed files PASS，0 conflict/sidecar；installed 整合 flows 15 项 PASS；声明平台 inventory/native-load 静态 16 项 PASS；installed 入口路径 2 项 PASS；真实 hook 的 no-currentDelivery 与 planning→implementing 2 项 PASS；最终 reapply ok，8019 unique managed paths 的 installed/source hash 与字节 drift PASS | 未发布 Guru marketplace immutable SHA；平台静态/路径测试不是 host 原生 AI 全流程证明；native continuation extractor 失败（B05）；dogfood/旧安装因 D2 阻断 |
| T531-08 旧断点 | 当前 workflow 保留同 Task replan、clean candidate 和局部依赖原 owner；#149/#444/#155 的旧 installed 数据没有迁移成功证据 | 全部旧形态受控接续及原会话恢复未完成 |

## Consumer 与 eval 定向结果

Architecture shared eval 17 个 case 全部通过；真实 Delivery Architecture production
case 与 clean committed reentry production case 均为 passed。后者通过正式公共入口
确认 fresh Check 绑定同一已提交 HEAD 后不产生第二次 commit。

Phase2 authoring 的 8 项在分批修复复测中分别通过（7 项及最后 context/trace 项）；
Architecture authoring 的 8 项也分别通过。Architecture 全组那次记录仍是
7 PASS / 1 FAIL：失败发生在 TemporaryDirectory cleanup 的 Directory not empty，
该测试断言已通过，随后单项复测通过。最后 context/trace 与 no-candidate 合并复测
2 PASS。没有将这些结果写作一次完整 suite 全绿，也没有跳过失败或容忍失败。
实际 fixture 由固定 installed Task/Delivery API 创建，schema relative refs 和
selected Delivery Planning locator 由正式 Interface/公共 projection 消费；这些
测试证明 fixture transport，不等于 native AI semantic gate。

完整 shared runtime 131 项曾有 5 FAIL / 1 ERROR；本轮修复受影响的迁移 consumer
并定向复测，没有重跑并通过完整 131 项。`runtime.discovery.CURRENT_INTERFACE_SCHEMA_IDS`
缺 1.8，而原 HEAD 的 guru-sync-base 已使用 1.8；已核对属于继承基线，未扩张
本任务去修复。该项相关 discovery/skill-package 测试边界保留。
source/installed package identity 排除 private tests 的测试未运行：本工作树的
dogfood 仍是旧完整包，不能用它证明新候选字节相等。最终 git diff --check PASS。

## B05：已复现的上游 continuation 公共缺口

固定 installed `common/continuation_contract.py` 的 extractor 在扫描任何
`[trellis-*]` 独立行时返回 `mismatched_marker`；公共 runtime parser 又要求
`[trellis-runtime-contract]` 独立行。两种合同在同一真实 workflow 中不可同时被
该候选 extractor 消费。无需改动任何 artifact 或上游包即可复现：

1. 用固定 CLI 初始化 `--workflow native-delivery-v1`；运行目标
   `python3 .trellis/scripts/get_context.py --mode continuation`。
2. 用相同 installed extractor 分别读取其原生 `workflow-delivery-v1.md` 和本候选
   canonical `trellis/workflows/guru-team/workflow.md`。
3. 两份 workflow 都报 `mismatched_marker`；native package 3 项为 2 PASS / 1 ERROR，
   实际 installed get_context exit 2。本任务对应定向测试保留失败，未改为假 PASS。

原生 prompt hook 可以产生 planning/implementing breadcrumb，并不能推出
continuation 可提取。B05 由上游 owner 修复并审查新的明确 candidate/API；Guru
不修改上游源、node_modules、hook 或发明替代 extractor。重新绑定候选后重跑
受影响 installed/native 入口与联合验证，不等待 Issue CLOSED。
B05 是 D1 正常入口的实际阻塞，不归入 D2 deferred。独立 Architecture 最终正式
出口由该 owner 另行产生；本文件不代填 semantic pass。

## 安装与恢复证据边界

默认 native clean init 实际产生 legacy bootstrap Task，随后新 Guru installer
返回 `upstream_delivery_migration_required`，尚未应用；这是 D2 默认切换边界。
受控 opt-in clean target 使用上游原生 schema2 bootstrap，未伪造 Task aggregate。
尚未发布的 Guru workflow 通过 canonical source 显式投影到该临时 target；它不是
GitHub marketplace 下载成功证据。业务/dogfood 当前仍运行完整旧安装，没有提前切换。

最终 reapply 返回 ok；8019 个 unique managed paths（11 个 install managed hashes、
8005 个 package managed files、3 个 overlay）逐项比较 installed hash 与当前
canonical source hash，missing/different/source-unavailable/source-different 均为 0，
workflow 字节一致，当前 sidecar 为 0。raw apply clean fixture 1 项 PASS。
早期 8024 是旧检查口径，不作为最终候选计数。

增量 reapply 生成的 sidecar 均先逐项记录 hash/原 path，再移到临时 target 旁保留，
未删除用户文件；本轮四份 consumer inventory 分别记录 61、1、1、2 个 .bak，
无 .new，前轮 inventories 同样保留。该证据不是全部用户修改 .new/upgrade/update
组合的验证，更不是完整 Release 矩阵。

上游原生 Core/CLI 证据属于其 owner，复用而不双跑，不证明 Guru joint。
受控副本不证明原业务会话恢复；原树本任务未修改。
完整 Release 矩阵、业务部署、provider交付、工作 Task commit/push/PR/merge
均未执行。


## 077 新候选的定向 installed 结果（2026-10-13）

本轮上游完整 source fingerprint 为
`077bb02966156b10f5d7477fedd9d6f8c2953dcd113434cf2ff48393307f2c25`，
HEAD a85ce75 加 manifest 明确增量，API 1.0 / Task schema 2.0。
CLI tar SHA `d09b905a539a0f695d2d2d603eeb20fdd925e98d81f710f04af754fed013e20d`；
Core tar SHA `45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967`。
同版本号/HEAD本身不识别这个完整候选。1144 source files/hash/modes 与 manifest一致；
installed CLI713/Core270共983文件与 tar bytes一致。

Guru 当前产品候选内容身份为
`guru-product-sha256:d052372af73088870adc4c03255cb41ed1e599397b384bddb48030cca6a39c3a`；
该检查的2428 canonical paths前后snapshot一致，未产出Task工作commit。
以下是受控副本的 scoped compatibility 观察，不是整体Phase2或joint readiness。

| 检查 | 实际结果 | 证据界限 |
| --- | --- | --- |
| projection + native continuation | 最终10+3=13项 PASS，含显式git_free kind的0600/0640同输入回归 | 初始12项绑定旧419c… snapshot，保留原记录，不重新标记 |
| installed entries | 2项 PASS | 是实际安装路径consumer检查，不是全平台原生AI完整执行 |
| actual get_context | 正式 installed `--mode continuation` exit0，current为 `no_current_delivery` | bootstrap Task身份保留；退出不能推导Completion |
| official update + custom ownership | 077 `update --force` exit0；custom workflow bytes未变，receipt无native workflow claim | 通过真实candidate CLI执行，不patch node_modules；未从immutable marketplace下载 |
| canonical reapply | exit0 / ok；37 active、110 commands、8005 package assets validator PASS | 资产数不是测试数；本Task dogfood仍旧完整安装，未提前切换 |
| installed/source drift | 8019 Guru unique managed paths、34 upstream scripts逐bytes/hash零drift；workflow source一致，当前sidecar0 | 早期生成的2个sidecar逐项旁置保留，未删除；不是全Release矩阵 |
| syntax | 4文件 ast.parse PASS | 子检查没有产品修改，未执行lint/typecheck完整suite |

保留首次失败：原opt-in副本bootstrap为active manual，Guru只声明pull_request；
077官方update最初返回 `unsupported_delivery_profile`。原native intake owner核对
其boilerplate准备scope全撤回，记录stop/release，保留身份/files，无Completion。
副本最初unborn，C4因无HEAD/已提交metadata拒绝；仅在该受控副本提交既有bootstrap
PRD/task.json作为fixture seed，修正后正式C4 binding_established。
fixture seed是测试前序，不是本Task或业务候选commit；该bootstrap准备不证明旧断点迁移。

## 1e400140 / 185e 候选实施中定向预检

上游产品提交 `1e40014023de53ddfd9368b3fb4d0a7a31e92293`、CLI tar
`185ed1db6865b72138bb10b6d799225721bf50fddfb370f84d8ec330558f472d`、Core tar
`45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967`，API1/schema2/Plan2。
PR #36 MERGED、build CI `38339653228` SUCCESS；这是上游交付事实，不是 Guru joint。
本轮 RDT 贡献承接 .89、Architecture .86；旧 .88/.85、ce363/077/5181 结果仍保持
各自身份。下列检查发生在 TaskCommit/Upgrade 实施期间的原工作树 canonical 源码，
尚未冻结完整 Guru candidate，不声称最终 installed/source 同源复测或 Phase2 通过。

| 预检 | 实际结果 | 范围 |
| --- | --- | --- |
| 明确新 installed upstream assets | projection 10、Author 11、Check 50、Delivery graph 8 PASS | 正式本地 wrapper/公共 API；fixture 判断不是原生 AI 门禁 |
| Review/事务 owners | Branch Review 40、Delivery Review 21、Publish 22、Merge 30 PASS | 历史/当前适用性、事务与丢输出的本地回归，不是 GitHub 成功 |
| 整体收尾 owners | Completion 21、Closure 16、Finish 56、Reactivate 27 PASS | 无空 Delivery、各 owner 本地合同；不是本 Task 正式收尾 |
| Source package validator | 38 active / 114 commands / 130 package-test assets，PASS | 资产盘点不是测试执行计数；worker 退出旧资产后须 fresh 重核 |

首轮 Check 未设置 `TRELLIS_DELIVERY_API_COMMON`，20 项 SKIP，保留原日志；补上同一
185e installed common 后完整 50 项零 skip。收尾测试首轮通过 unittest 导入时缺
pytest，明确 ERROR；managed interpreter 未改动依赖锁或 cache inventory，pytest
8.4.2 仅置于外部测试目录，经同一 managed resolver 的临时测试 launcher 重跑上述
四包成功。产品 wrapper 不使用该测试依赖目录作 runtime fallback。

本轮完整旧 #149/#444/#155 受控迁移、冻结 candidate 的 canonical/dogfood/installed/
平台/update/reapply/drift、Phase2 Architecture/Check 与真实联合验证仍待执行。
#531 原 Task execution_resumed 是实际身份恢复结果；原业务安装/会话未改动，未恢复。

实际命令由managed Python3.12执行projection/native/installedentry unittest；
使用明确077 installed public scripts，真实CLI `update --force`、installed
get_context和canonical preset apply。临时复核 locator：
`/tmp/guru531-077-installed-check-result.json`、
`/tmp/guru531-077-projection-native-final.log`、
`/tmp/guru531-077-installed-entry-tests-final.log`、
`/tmp/guru531-077-installed-get-context-final.log`、
`/tmp/guru531-077-installed-drift.json`。
这些临时日志只是本段实际观察的复核线索，不是公共DTO或持久workflow authority。

新Planning Wording正式pass、独立Architecture正式baseline_current及Planning
Approval正式approved已完成；它们不批准尚未执行的migration或joint结果。
当前仍未完成：Plan2/Guru私有迁移实现与验收、#149/#444/#155真实旧形态接续、
真实远端Publish/Merge、整体Phase2/joint/P4 matching readiness、原业务会话恢复。
上游默认 SDK/API/init 退休由上游owner判断；完整Release矩阵、部署、provider业务
均保持独立边界。ce363 B05不再声称077当前阻塞，但旧失败记录保留。


## 最终5181来源接续与 #530 实际交付差额（2026-10-13）

上方所有 ce363/077 当时 Issue OPEN、pass/fail 和未验证项保留其原候选身份。
当前上游 #31 已 CLOSED/COMPLETED，PR #34/35 均已合入；固定最终来源为
5181ab6671cc2ed441feaa33e080f830e57c4f8266d927355cf69d272b85d77f，
CLI tar 6763278a436c754e9d97e85d9ae953983541b97041e0f0d167a9b8cde0434c16，
Core tar 45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967。
#530 产品 d7cde2f06 经 PR #540 合入并由 PR #541 归档；本 Task base 尚未整合
新的 main@bebf1993/.86/.89，当前正式入口仍是树内 .85/.88。

| 当前定向观察 | 实际结果 | 适用界限 |
| --- | --- | --- |
| shared runtime 恢复批次 | 实际命令发现并执行64项，1 FAIL；失败只在完整shared Architecture的三份owner输出 | 不写作131全绿；原日志 /tmp/531-shared-runtime-final518-afterfix.log 保留 |
| 受影响shared三个case，fresh fixture | no-impact / next-task-consumption / delivery-task-impact-sync-identity 全部正式 baseline_current/passed | 最小eval运输去掉candidate_assessment的future promotion；production gate未放宽，不是正式本Task Architecture/Check |
| TaskCommit当前显式base候选 | 29项回归 PASS；原nullbase默认main机制已按已交付来源删除 | 单元/正式wrapper回归，不等于本Task clean或原业务已恢复 |
| Phase2 authoring fixture staging | 三个actual installed/public current Delivery 均进入checking，当前key与public key相同 | 只验证真实staging，未执行host AI semantic Check；前次harness把current dict与key比较的失败保留 |
| 正常候选/source差额资格 | 原normal/solution/root正式stdin调用完成；属于对象合同迁移与运输修订，无事故机制 | 资格不授Planning Approval、Check或Review |
| final_plan来源差额 | 独立review实际contract_incomplete，指出#530来源和实际clean接口处置缺口；原Author已requirements_ready | fresh candidate assessment、solution、Wording、final_plan、Approval仍需当前结果 |

最终包上的受控installed c600671b/e7cb快照已运行clean init、Plan2/common-local
session/registered workspace/occupied archive、完整preset、平台投影/reapply与8652
managed bytes/modes核验；这些是各自非最终Guru候选的历史定向证据，后续变更不能
套用其identity。完整drift继承缺 bootstrap-repository-ssot.md，保留该失败；
本次定向drift单列，不扩张为修复无关历史债务。

真实旧receipt升级首先产生tracked安装增量，clean入口被阻塞；这是保留的真实失败。
仅/tmp由原安装写集单独提交产品增量并保持原业务commit为祖先、未来五规划未预提交后，
明确base的468eefc7样本 fresh Check→TaskCommit committed→首次完整Review已达；
semantic输入为受控fixture，不冒充独立host Check/Review。原nullbase默认通过的
e7cb结果已被当前显式base合同替换，必须保留为 superseded/historical_only；
最终应观测stale_identity/base_branch，由原base owner恢复。完整旧形态149/155、
matching最终freeze、正式整体Check/joint以及原业务会话恢复仍未据此完成。

原业务工作树只读；#531未commit/push/PR/merge/发布，当前Task安装未apply新runtime，
共享RDT/Architecture未promotion。上游交付、Guru样本、联合验证及原会话恢复分开报告。


## 真实注册旧工作树副本的 Plan2 阻塞（2026-10-13）

对应AC09旧安装迁移、AC02/#149活动重规划、AC04/#444clean接续、AC10/#155局部依赖；
设计责任为task design §15的原Upgrade完整inventory与上游Plan2公共处置前置。
最终上游5181/CLI6763/Core45bb和Guru受控snapshot138d332d绑定本次观察；
非最终freeze，不沿用其identity声称整个Guru/联合验收通过。

| 实际场景 | 结果 | 证据边界 |
| --- | --- | --- |
| 两registered workspaces均保留实际149/155 Task1.0副本，全convert preview | FAIL：Task identity collision149 | source rawbytes/modes和common binding来自真实旧安装；初次harness错标legacy的失败独立保留，纠正Task1.0后才属此产品观察 |
| 每Task仅当前checkout convert、其余副本defer，defer无未来artifact write | FAIL：同collision149，在public写入/private迁移前 | actual installed Plan2；完整13347 files bytes/modes无变，原owner fresh只读回查无变 |
| 独立Architecture owner重入实际dryRun | final_plan contract_incomplete，三个具体missing refs | 原Author已按§15修订真实candidate并requirements_ready；不是最终Approval或当前Architecture pass |
| #149真实owner五规划对HEAD | 五份一致，HEAD e27bfb7e… | 可作规划来源形态，仍未执行该拓扑迁移或fresh业务门禁 |
| #155真实owner五规划对HEAD | 当前三docs不一致；两JSONL一致，HEAD150f743e… | dirty/fresh Planning，不冒充clean五blob；原新规划与业务成果保留 |
| 当前业务规划事实 | 149 D3a/PR461已交付、D2b候选；155 D1/PR454已交付/remaining_work；P406-1/2局部限制奖励恢复/ELIGIBLE | 历史事实与scope，不推导当前新Check/Review；独立查询工作不因provider缺口停摆 |

复核线索为 /private/tmp/531-exact149155-7r03xsrr 中的
private-plan2-defer-current-only.json、defer-current-only-preview-result.json、
installed-plan2-defer-current-only-preview.stderr、original-copy-comparison.json、
original-owner-committed-planning-shape.json、original-owner-fresh-readback.json；
原独立assessment为/tmp/531-worktree-gap-finalplan-output.json。
仅临时定位实际执行，不新增公共DTO/state或把资格结果写成本测试authority。

接口缺口归上游原Plan2 owner；Guru不去重、省略workspace、删副本、改身份或
patch上游。修订candidate实际交付后fresh受影响Planning与installed同序列验证，
预览及执行均须保留原身份/每分支规划/完整inventory、唯一合法执行checkout与
正确session结果。未完成公共支持前不切原安装，旧失败不能改标为通过。
当前整体Phase2 Check、matching joint、原业务会话恢复均未完成；来源Issue
已结束、受控bootstrap成功、#530明确base样本和本次零写入均不能替代这几项。


## 当前 canonical runtime 完整回归（2026-10-13）

修复shared Architecture candidate_assessment运输后，以最终5181 installed公共
scripts/API common为依赖，从canonical runtime/tests完整discover执行：
`python -m unittest discover -s trellis/skills/guru-team/runtime/tests -p 'test_*.py'`。
实际managed Python3.12、PYTHONDONTWRITEBYTECODE=1；结果131项、567.811秒、OK，
命令exit0；日志/tmp/531-shared-runtime-current-complete.log。并行仅独立读/写规划
与task-local evidence，production runtime源码未改；验证完整set不只替代三个case。

此结果取代当前shared runtime失败状态，不重写此前64项/1FAIL及其运输修复事实。
TaskCommit29项、installed staging三个case仍各保留自己的scope；本131项结果
不授本Task语义Check、独立Phase2 Architecture、固定pair joint、原业务迁移/恢复
或Release矩阵。§15的正常Plan2副本接口缺口仍按实际installed失败报告。
当前git diff --check通过，实际HEAD/index/staged集合保持；没有#531 commit。

## #530 base 整合后的 TaskCommit 定向回归（2026-10-13）

实际 HEAD 为独立本地 base merge f03e8a04c487e64722e90697543ec7398de2b338，
包含 main@bebf1993、Architecture .86 / RDT .89；#531 pending 候选未提交，
当前 Task 安装仍为 legacy 完整运行合同。前节 131 项仅绑定整合前快照，
不能替代新 base 下完整 Check。

以同一最终5181 installed scripts/API、managed Python、禁止 pycache 写入的环境，
实际执行 canonical TaskCommit tests 目录完整 unittest discover：36 项、42.264 秒，
29 项通过、6 FAIL、1 ERROR，命令 exit 1；日志 /tmp/531-taskcommit-after-base530.log。
新 base 带入的 test_committed_reentry.py 六项在旧 Task Check 输入调用处返回
schema_mismatch，尚未到 clean 执行入口；另一项引用已退出的
production_committed_reentry_invocation，返回 ImportError。其余 29 项通过，
包括公共 Delivery clean 规划来源桥的两个用例。

这是实际候选迁移不完整的检查结果，不将 legacy 用例失败改标为通过，也不借此
恢复第二活动 Task writer。后续原 TaskCommit/eval owner 按 task design §14
核验每个旧 asset 的直接 consumer，迁移仍必要的正常 clean/Reconcile/首次完整
Review 行为，退出无人消费的旧入口资产，再运行适用的定向 suite。
当前记录不授 Planning、Phase 2 semantic pass、matching joint、原业务恢复或发布。

## 新 base 的投影与规划来源定向检查（2026-10-13）

在同一 f03e8a04 base 与最终5181 installed 公共API下，实际执行
`test_installed_projection`：10项/7.515秒/OK；`test_delivery_migration`：
2项/8.851秒/OK。日志分别为 /tmp/531-mechanism-first-projection-check.log 与
/tmp/531-mechanism-first-clean-migration-check.log。覆盖受控投影中的多Delivery、
返工/退出、整体完成重开，以及旧五规划路径来源保持与正常规划变更拒绝。
这些定向结果不覆盖完整TaskCommit36项、完整旧安装副本迁移、平台host、
reapply/drift、真实远端或联合验收；前节6 FAIL/1 ERROR仍未收敛。

## 1e400140 / 185e 当前候选的实际结果（2026-10-13）

本节更新当前结果；前述 5181、副本 collision、旧 source、旧 TaskCommit 失败均保留
为原对象的历史，不改写为通过。上游产品为
`1e40014023de53ddfd9368b3fb4d0a7a31e92293`（PR36 MERGED、CI38339653228 SUCCESS），
CLI tar `185ed1db6865b72138bb10b6d799225721bf50fddfb370f84d8ec330558f472d`，
Core tar `45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967`；
API1/schema2/Plan2。Guru 是未提交的完整本地候选，HEAD f03e8a04 仅识别 base 历史，
不是承载候选的提交，也不是正式 source lock。当前 managed bytes/modes 身份为
`538a969ddb98d1a9a0246adedca85e115304c992f1d2fbbd19339fe80dd3100c`；
它相对已运行的 b8e23019 只删除 eval authoring 一行末尾空格，实际逻辑等价。
完整包含本节的 source snapshot 另由当前冻结结果绑定，不在本文产生自引用 hash。

### 当前验证与依赖适用性

| Trace / validation | 实际结果 | 直接证明和边界 |
| --- | --- | --- |
| T531-01/02、V01 当前 canonical | 独立 Architecture reviewer 亲自执行 68 项 PASS | graph3、projection10、Creation3、Activation6、Checkflows16、TaskCommitmigration2、Publishmigration2、Mergehistory5、Reactivate2、Upgrade18、rawapply1；客观测试不授整体 semantic Check |
| T531-04、V07 TaskCommit | 完整迁移后 38 项 PASS，显式 base 的原29项 PASS | 原36项失败在其真实迁移后被取代；缺base保持诊断、不默认main。日志 /tmp/531-taskcommit-final.log、/tmp/531-taskcommit-explicit-base-suite.log；当前未改变其真实依赖 |
| T531-07、V03/V14 Upgrade | 18 项实际 installed tests PASS | /tmp/531-upgrade-after-qualified-removal-installed.log；首次未提供 env 的18 SKIP不计PASS。版本、完整副本/session/binding、原诊断、恢复与私有owner适用性受测 |
| T531-02/03/04/05/06、V04/05/09/12/13 | installed owner flows14 + 公共 projection10 PASS | 同代表性安装的真实wrapper/API；semantic/provider输入为受控fixture。覆盖多Delivery、同Delivery replan、另一计划保留、各阶段退出/loststdout、dirty精准提交、clean完整Review、stale/context、readiness、无Delivery整体/收尾及remaining scope；不冒充独立host或真实GitHub效果 |
| T531-07、V02/03/14 | 一个代表性 clean 的实际 apply、resolved/stable reapply、installed inventory、native context/continuation PASS | 首apply exit2为声明managed `.bak`待处置；逐项copy2保留后处置，再两次reapply。原#531 runtime未切换；真实CLI update→canonical reapply与Codex/Claude/Cursor入口投影已有适用证据 |
| T531-07、V02/14 完整 drift | FAIL：只缺既有 bootstrap-repository-ssot.md；changed=0，无其它missing | 继承缺项与本候选定向一致性分别评价。不修无关历史债务，不称完整drift PASS；sidecar处置结果逐项保留 |

本轮从完整候选和真实consumer判断测试价值：各组观察公开关系、实际阶段、候选/
HEAD/index、恢复出口和远端调用次数，而非仅镜像函数实现。只消费实际依赖仍适用的
执行事实；旧内容 token 不投成当前 gate。source validator 的38/114/130项是 inventory，
不是另计的测试数。上表不授Release完整矩阵、正式远端门禁或整体完成。

### 忠实旧形态与首次失败保留

T531-07/08、V06/08 使用受控旧安装副本的完整 Plan2 + 原 C4 binding、unique convert
authority + inherited defer：两 root 完整preset与同Plan2输出丢失恢复实际 PASS。
13,405原输入与91规划/关联docs的受保护 bytes/modes无差额，`.new=0`。
#149 TaskId `149-normal-price-promotion-current`、generation0、公共Delivery
`f00bb27c-d71f-4143-8630-126522fa0b60`；#155 TaskId
`155-home-subscription-v180`、generation0、公共Delivery
`82b8d774-6bd8-4754-95b2-ddbc4cc083c9` 保留。原D3a/PR461、D1/PR454及remaining
保留为历史交付，四gate/publication/delivery结果为空；不补造当前pass。

原认为#155有40个receipt外`.new`的观察已撤回：它们来自第二root叠加第一root的
fixture污染，真实原#155这40个路径均不存在。忠实exact-copy的`decisions=[]`完整迁移
通过；原Normal owner实际重新分类为 rejected_not_reproduced。只撤除本轮 union
consumer/合同段落/3tests，保留此前合法session/common.resolve/retained诊断修正及
并行成果。不得把该污染样本列为产品finding、必需负例或迁移支持范围。

两旧scope由原Selection合法选择后，root亲自完成完整三规划Wording七维、逐hit
分类、真实record/check/invoke，均PASS。随后fresh独立Architecture `final_plan`
均实际返回 `contract_incomplete`，purpose/key/planning_root准确保留，唯一consumer
为原planning-router：缺当前Task内真实task-local contribution。外部长期贡献与历史
晋升不替代当前输入；Positive Planning/Approval/Activation仍PENDING，不代填token。
首次reviewer context不匹配的stale_identity保留为无typed exit，原Selection在相同
context fresh重入后才取得当前正式回程。

为正确解释该样本的检查边界，仅从指定原HEAD补缺非敏感源码/Architecture及固定
schema/contracts；既有bytes/modes未覆盖。两scope实际ci-code在固定包补齐后仍失败，
归因为snapshot缺嵌入素材、部署/OpenAPI等资料；不是业务回归或Guru finding，不继续
追全绿或复制业务部署配置。#149三规划中迁移相对引用与#155原task状态历史文案仍需
由实际业务Author fresh处理。本Task不代写业务规划来产生批准，更不接管#406。
P406-1/2仅阻塞奖励恢复/真实ELIGIBLE，独立查询义务及完整AC保留。

T531-04、V07 #444最新 source 的 Plan2恢复与安装前序后实际链已PASS：
Creation→Activation→freshCheck→cleanCommitted→同DTO重试→post_commit pair guard→
Architecture→首次完整Review。原fixture业务commit f4bf0f0b保留为祖先，真实安装增量
独立前序HEAD 4db887f6；clean链前后HEAD/index/commit count不变，clean receipt为零，
未来Delivery五规划未预提交。原jsonschema缺失、source未bootstrap与owner失败保留，
同plan/source/rollback anchors下补隔离source runtime后恢复成功。该driver使用受控
semantic/Architecture输入，并直接计算Activation token，未执行真实Approval前序；
因此只证明客观installed接续，不冒充host语义批准、完整联合门禁或原会话恢复。

复核线索：/private/tmp/531-managed-decision-final-candidate-grza75nc/upgrade-proof.json、
exact-copy-provenance.json、task149/155-architecture-final-plan-round2-output.json、
fixed-contract-snapshot-enrichment.json、fixed-contract-ci-code-results.json；
/private/tmp/531-current-pair-elkukqgp/final-installed-result.json、
/private/tmp/531-current-pair-8_mufwk5/final-directed-result.json；
/private/tmp/531-copycandidate444-final-managedpy/{resume-result,continued-result,owner-chain}.json。
这些是临时执行定位，不成为新的公共DTO或状态authority。

### 当前剩余门禁

V06/08实际旧形态的正向Planning接受/实施仍缺当前业务owner合同，不能从成功迁移
或通用replan tests推定通过。V10/11真实远端Publish/Merge及其成功后投影恢复未执行；
当前controlled wrappers只证明自身层次。正式固定两仓candidate的联合核验、正式
source-lock与独立host语义证据尚未取得。原#531执行恢复已实际完成；它不等于原业务
会话恢复。原业务树只读、从未apply/迁移或实际接续。没有#531工作commit、push、PR、
merge、发布或cleanup，shared RDT/Architecture未promotion。

设计已接受、实现候选、单仓定向验证、完整联合验收和原会话恢复分别报告。
本Task full policy未改为partial；最终整体Check须按上述真实缺口决定，不能为了
进入提交而把required PENDING写为PASS。完整Release矩阵保持明确的非本Task边界。

## 当前只读复核与两项局部修复（2026-10-13）

本节是上述记录之后的增量，不改写旧轮失败或候选身份。当前开发树仍为
f03e8a04 base 上的未提交候选；原 installed Task/runtime 未切换。
上方 538a969d managed 身份和 931y5q82 source snapshot 不识别本节之后的修复。
本轮仅修改 #531 专用开发树；业务原树、既有验证对象和 Issue 未写入。

| 当前检查 | 实际结果 | 范围与边界 |
| --- | --- | --- |
| C01 global Planning router | 三条 canonical 回程修正；现有 Delivery graph 3项 PASS，实际 producer DTO 到六个 consumer input 的 schema 组合验证 PASS | policy 返工保留同 DeliveryKey并用当前 Author profile；下一切片先 Creation；整体需求修订先 Clarify/root scope-only Author/scope acceptance。未新增 runtime router或状态authority，未将 schema 验证当作 native AI 全链 |
| C531-UPGRADE-RESUME-TOPOLOGY | 两条真实正常复现修复前 FAIL；修复后完整 DeliveryUpgradeTests 20项 PASS、零skip，52.899秒 | 真实185e CLI/Core迁移，preset mock暂停后正常新增工作树注册或同HEAD切换分支；现有私有 business_before 绑定routing，resume/rollback停止且保留checkpoint、anchors、新资源和session；不刷新恢复快照、不重复Core/preset。不等于完整preset/joint验证 |
| 未改变拓扑的恢复 | 上述20项同时覆盖原same-plan/output-loss、monorepo、inherited peer与原私有owner路径 | 实际使用全新 TemporaryDirectory夹具；未修改既有受控样本来追绿 |
| 候选卫生 | 当前 git diff --check PASS；所改Python ast.parse与局部空白检查 PASS | 原index的唯一staged路径仍为trellis/guru-team-extension.json；未stage/commit |

只读复核已取得 #149/#155 后续原 Author 的 `plan_ready`、Wording `pass` 与独立
Architecture `final_plan/baseline_current/no_change`，分别绑定 v43/v35及原
DeliveryKey。它们是修订公开供给事实后的隔离 Planning 结果，不将前轮
contract_incomplete改标为通过。两者仍未Approval/Activation/实施，旧断点的
完整正向验收与原会话恢复均未因此完成。复核线索为
`/private/tmp/531-oldpath-{149,155}-current-facts-{plan-ready,wording-output,architecture-final-output}.json`；
仅用作实际输出定位，不是新authority或公共handoff。

本轮修复不改变上游1e400140/CLI185e/Core45bb/API1/schema2/Plan2依赖。
原已安装完整drift缺 bootstrap-repository-ssot.md 的失败保持；既有快照不重apply。
正式当前 Phase2 Architecture 已实际返回 `baseline_current`，独立判断为
`legacy_boundary_convergence`，没有 Architecture 阻塞。随后同一独立 reviewer
才加载完整 Task 并执行原 installed `guru-check-task` 九维审查；当前 defect
candidate set 为空、无新 findings，但 full 范围的必需证据缺口使其实际返回
`blocked`。原 recorder、checker、public wrapper 均 rc0；checker 的结构校验
成功不等于整体 Check passed。非 passed checkpoint 由原 wrapper 退役，本次
临时输入已删除，未进入 TaskCommit。

本轮独立 reviewer 实际掌握的定向测试共60项全部 PASS、零skip：先完成
graph3、projection10、Upgrade20、Creation3、Activation6共42项，再执行
Check flows16与source TaskCommit migration2共18项。42项按本轮未变化的
实际依赖适用性复用，不把 Upgrade20或其它重复执行再累加为新增覆盖。

正式 Check 的 required PENDING 是 #149/#155 实际 Approval→Activation→实施、
修后 matching installed、固定两仓联合与独立host语义证据，以及 V10/V11
真实远端 Publish/Merge 成功后的投影及输出丢失恢复。原业务会话仍从未迁移或
实际接续。设计已完成并接受；实现是未提交候选，整体 Check blocked；联合验收
与原业务恢复均未完成。本节追加只记录该轮已发生结果，不将其内容 token 用作
追加后的候选 pass；未来重入由原 owner fresh 判断实际依赖与适用性。

## 当前隔离 installed 与旧断点 Activation 补证据（2026-10-13）

本轮验证对象为新隔离 source、installed-copy、legacy-primary、legacy-secondary；
业务原树、此前样本、上游安装包和 Issue 均保持只读。冻结 source 的 base HEAD
仍为 `f03e8a04c487e64722e90697543ec7398de2b338`，它不是承载 #531 候选的提交。
上游固定产品 `1e40014023de53ddfd9368b3fb4d0a7a31e92293`、CLI tar185e、Core tar45bb、
API1/Task schema2/Plan2不变。Guru被验证的managed内容身份为
`1a5e01afa61a4ac36fb8c82817ca1be6f63ba151e9ff819ce88371ea15880746`；
完整冻结source身份为 `9f6d63abb6b79090cb616bf517a17672f14475d19cf3984f663ddceac28c2f92`。
本节追加会改变主开发树的完整内容，以上身份只识别实际被验证的冻结副本；
后续 owner 必须重新判断追加后的候选与这些执行事实的适用性。

### T531-07：matching local installed 定向结果

原安装inventory、get_context和continuation均rc0。8,652项managed投影无缺失或
内容差异，权限符合实际安装合同；Codex/Claude/Cursor各1,579项投影一致。
raw权限差额为一项Guru invoke-stage0及34项上游脚本的644→755，分别由原
ensure_companion_modes及官方update脚本权限合同解释；不将raw字节模式事实改写。
source的3,701项冻结路径bytes/modes前后相同。

最终五组共50项不同测试PASS、零skip：installed owner flows14、projection10、
current graph3、native continuation3、Upgrade20。实际执行53次，不与前轮60项
累加成新的覆盖数。首轮五组因临时driver将runtime错定位为skills子目录而未运行
用例；第二轮continuation执行3项其中1项因子进程同类locator错误失败；仅修新
driver后第三轮3项PASS。这些失败保留，不声称第一次执行全部通过。

关键projection/schema/Upgrade模块的实际加载路径均在新installed-copy下。
projection中的两项installer诊断仍加载冻结canonical installer；Upgrade20使用
真实Core与preset mock。受控semantic/provider输入、installed模块执行、host原生
AI门禁和真实GitHub行为分别报告，不以这些测试授予后两者通过。

首次reapply rc2，只有六个声明的.bak、无内容conflict；逐项copy2保留并读回后，
原resolved及stable reapply均rc0，installed checker rc0，最终sidecar为0。
本批次未执行official update --force，也没有修改主Task的运行安装。
完整drift仍rc1：缺 `.trellis/spec/workflow/bootstrap-repository-ssot.md`、changed0。
只读诊断证明基线canonical已有该spec，但原MANAGED_SPEC_PATHS遗漏它，drift却
枚举全部canonical workflow spec；该问题非#531引入。本Task保持继承FAIL边界，
未补验证target文件或自动修无关安装债务。实际汇总线索为
`/private/tmp/531-next-local-validation-20261013/installed-quality-summary.json`，
它是执行结果定位，不是公共gate或新的状态authority。

### T531-08：#149/#155 原 Approval → Activation → 实施入口

两个新root保留原TaskId/gen0/DeliveryKey、五规划和来源关系：#149 exact_source，
Delivery `f00bb27c-d71f-4143-8630-126522fa0b60`；#155 reference_only，Delivery
`82b8d774-6bd8-4754-95b2-ddbc4cc083c9`。原owner对完整当前三规划执行八维审查，
核验Author/Wording/独立final_plan与live来源的适用性；两个原record/check/invoke
均rc0、实际返回approved。不生成空qualifier或从文件自行制造approved。

之后两个原pair guard均rc0/unchanged，local dev和Task HEAD均为
`5bebc04514f9d77caa83b1a550f90f47f644aee8`。两个原Activation公共入口均rc0，
实际返回delivery_started。公共Planning结果分别为
`planning-accepted:1da90cba-a4de-40ac-a328-5b0dae945918`和
`planning-accepted:41303516-6fa1-42d1-a1fe-f06be6df191e`。
公共current与get_context读回同Task/gen/key/session，phase为implementing，
Planning applicable；Check/FullReview/Readiness仍missing。原continuation rc0，
唯一delivery-started consumer与实施owner路由可读；没有执行业务实施或Check。

Approval没有修改公共Delivery slot；新index的stat-cache刷新经逐字段只读比较
证明blob/mode/stage/path及扩展不变，未回写恢复index。Activation批次的工作文件
差额各仅task.json的本Delivery phase、plan_ref、planning result；其它工作文件、
HEAD、index及三规划不变。原Approval/Activation恢复checkpoint和本次临时输入
均由原consumer完成后退役。展示计划曾误写guard wrapper路径；更正为原installed
package声明的同一guard入口，未修改安装文件或产品routing。

本结果补齐旧形态受控Planning→Activation→实施入口；不证明业务回归、完整
奖励能力、部署或原业务会话实际恢复。#149保留D3b/D3c/D4与整体P149责任；#155
保留额度、原奖励/逆向/revision、ELIGIBLE及采用责任。provider公开供给与本快照
实际消费分开，未采用后继field9或猜测订单定位。#444 clean候选的前轮证据保持
其原范围，本批次没有重复提交或重跑其原样本。

### 当前整体门禁边界

设计已接受；实现仍为未提交候选。本批次没有TaskCommit、push、PR、merge、
Issue写入、cleanup或主runtime切换。最新正式Check仍是前节blocked；这些新
执行事实不是新Check pass。接续时由原owner重新执行当前Architecture及完整
Check，分别判断local matching、固定两仓joint/独立host语义和V10/V11真实远端
成功后投影/输出恢复。原#531开发会话已恢复，原业务会话仍未实际迁移或接续。


### T531-09：2026-10-14 当前链接候选、installed 与远端收尾增量

当前冻结 Guru managed fingerprint 为 d6536ffedb6c0779aca918ddf5aa5a1d7690a3fc9a8f0c58a90ca68df250ae8e；完整 source fingerprint 298a23260e4d924cf4b7bc54a2cfe5ab4926e32f381f85390709f0fbd7f2c774（本节回写前快照）。上游 CLI tar 为5aeeb81c、Core45bb，API1/Task2/Plan2。源HEAD f03只识别base，本地候选并非formal source-lock；PR38仍OPEN/CI FAILURE。

原installer漏bootstrap spec已在canonical受管清单修复，不手补target；真实clean/reapply闭合测试PASS，旧drift失败保留为旧候选事实。当前完整代表clean init后按官方本地custom workflow装入Guru，原apply/reapply及原drift实际rc0、Claude/Codex/Cursor与shared投影一致；没有执行gh marketplace发布候选或完整Release矩阵。主旧runtime仍未成套迁移，不以该copy替代主dogfood。

TaskCommit显式markdown_relative_links_v1六项迁移回归PASS，完整TaskCommit 42项PASS；保留原严格模式、直接HEAD字节校验、旧association不自动升级、真正内容变化dirty、代码/query/fragment及其它bytes不变。真实#149新执行副本保留e27候选与Task/gen0、85原Task和9binding；当前转换只投影1binding，8deferred原字节保留。首次误投全部binding被公共preview拒绝，Upgrade同样blocked无迁移；修正后新Plan2preview、Upgrade及same-result恢复实际成功。三规划11个destination指向原真实文件，其中10个是前轮失效引用；两context不变。正式Author已requirements_ready；Planning后续门禁仍待执行。本结果尚不授V07全链通过。

独立真实远端样本：candidate ade5e89、D1 50166a7c、Task531-remote-next-validation/gen0/no_issue；原完整Planning/Check/clean/首次完整独立Review/Readiness后，PR542真实合入专用base（b183e366）。原Publish same-plan与Merge terminal重入返回同结果；原history发现唯一同key/PR/merge。原整体Completion completed、Closure no_mutation，不写Issue。原Finish投影保留Task2 aggregate与scope/五规划字节，bookkeeping PR543合入专用base（3d2e8b96），重入返回同finish:v1:991d5fbe924ba275。原Cleanup盘点无Guru-owned pending资源，保留2caller-owned资源，正常与lost-output重入返回同cleanup-result:329f284b1a9f2189a704e29a；未删除样本或原业务资源。零删除路径不冒充实际资源删除验证。

远端正常成功后输出丢失已真实执行；公共投影暂缺没有在真实远端自然发生，仍由最终Check结合既有installed包级正常恢复回归判断充分性，不篡改slot制造。主#531工作未提交，完整Check/joint/交付仍待完成；原业务会话未恢复。

### T531-10：旧 clean 规划的合法空 context 与真实贡献定位

#149 e27 原 implement.jsonl/check.jsonl 均为空；Plan2保留同字节后，Author solution正式入口错误返回stale_identity/implement.jsonl。canonical修复将存在的regular空JSONL视为合法空选择，仍要求两文件存在、每个真实entry有file/reason，三Markdown仍非空；充分性归Author语义判断。原Author完整12项tests PASS，覆盖空context保持、不新增entry、缺文件仍blocked。执行副本经完整preset reapply安装该修复，六份真实旧受管bak逐项与冻结旧source相同比对后保存在owner临时备份，稳定reapply rc0。实际Author plan_ready与Wording pass，业务代码、三规划和两context不变；此链仍未获得最终Planning/Check/Review通过。

独立Architecture final-plan发现既有docs/architecture/contributions任务专属贡献存在、expected_current v40，但validator强制物理位置位于Task目录；实际正式调用stale_identity/contribution_locator，未冒充pass。canonical去掉该位置断言，保留safe repo-relative locator、regular file和当前content identity校验，由独立Architecture判断真实任务归属。完整32项Architecture tests PASS，覆盖既有durable locator不复制、正常内容变化stale。修复保持同public API、无新贡献镜像或第二authority。

主仓库完整只读preview盘点148注册workspace、15082份Task副本。当前上游Plan2与Guru升级要求每root的prospective模板及成套安装，不能仅靠Task defer保护并行root的受管文件。因此没有执行主切换；主保留原完整legacy流程。V02继续以获准受控dogfood验证为证据，自身原安装成套切换尚未执行，不能说成主已迁移。原业务树与旧样本继续只读。

### T531-11：当前候选的正式旧 clean 接续与最终定向安装

#149 新执行副本保留原 e27 业务候选，完整安装增量独立本地前序提交后 HEAD 为
8b9145e5；业务 app/proto/docs/Makefile/app_makefile 与 e27 无差额。原身份/gen0/D2b
经当前 Planning 全链、独立 Architecture 和完整九维 Check，实际返回 passed。
原 TaskCommit 首次与 lost-output 重入均 committed，HEAD/index 字节不变、无 stage、
hook 或重复业务 commit。post_commit pair guard 实际 unchanged；首次完整独立
Branch Review 已实际 passed，范围 origin/dev...8b9145e5；其独立Architecture及五项
Make重新通过，不由 clean 接续推定。#149 剩余业务
Delivery 与部署、原业务会话恢复仍未执行；#155 的局部 provider 界限保持 T531-08。

当前 canonical 修正 Delivery Architecture impact/maintenance 的同key/root回程，
Task-only Completion/Finish仍消费原Task profile，不让两类结果互冒。上游 bundled
meta 的旧激活名称由既有 workflow-contract 明确优先级；不覆盖 provider 参考文件，
不新增模型或wrapper。22平台 descriptor与ownership validator通过。

本轮冻结源码在新隔离环境使用已审查 CLI5aeeb81c/Core45bb，实际完成代表clean init、
canonical preset apply/reapply、受控dogfood fresh init/apply/reapply、完整drift、
installed package inventory、Claude/Codex/Cursor投影及native context/continuation，
全部最终rc0。首次dogfood apply的声明bak逐项保留后再apply；ordinary update拒绝
旧/current混合runtime保持为真实诊断，不称旧安装已成功升级。原主148注册root
和全部旧业务/验收样本不修改。actual installed原owner链14项和公共projection10项
均PASS，覆盖多Delivery、返工、退出、clean首次完整审查、历史事实/当前readiness
区分、输出恢复、整体遗漏与无Delivery收尾。受控semantic/provider输入不冒充真实
远端动作；PR542/543的真实远端事实仍仅按T531-09原candidate适用。

完整kernel当前轮93PASS/2FAIL/11SKIP；两失败分别是旧测试错误要求portable安装
项目自有index、以及错误把专用source-lock绑定复制到通用合同文档。迁移仅测试的
locator/version选择，保留实际安装合同、current owner与历史#454锁定断言。修正后
#434 activation 14PASS/1SKIP、workflow prose18PASS，合计32PASS/1SKIP；不将本轮
失败抹掉。SKIP对应需专门source或
native工具链的现有测试入口，非本Issue完整Release矩阵证明。
