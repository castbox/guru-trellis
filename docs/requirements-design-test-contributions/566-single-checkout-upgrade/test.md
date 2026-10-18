# #566 Test 唯一增量证据

状态：本地实现与下述分层联合验证完成，整体Phase 2仍由原Check owner独立判断。上游 #40 的公共层候选只作为隔离开发依赖，不继承为本任务通过结果。

| Identity | 场景与可观测结果 | 当前结果 |
| --- | --- | --- |
| T566-01 / SCN566-01 | 真实Git refs/registered checkout：显式目标、配置和ordered fallback；缺失/歧义/prunable不给低优先级替代、不create/switch/fetch。 | 共享resolver与tools定向回归通过，见下文 |
| T566-02 / SCN566-02 | primary/linked pointer隔离、shared/peer bytes/modes与实际解释器解析，普通activation不回退。 | 实际双解释器与原fullupgrade回归通过，见下文 |
| T566-03 / SCN566-03 | 完整matching public pair＋Guru工具wrapper对代表旧安装真实apply/native/reapply，Task/session不变，conflict/sidecar不能输出成功。 | 旧writer样本与最终source实际tools链路、同ref恢复、native及reapply通过 |
| T566-04 / SCN566-04 | 旧parser拒绝仍从完整来源prepare/convert；目标native与下一owner真实续接；已交付待验收无新Delivery。 | 两类实际installed下一owner通过；历史待验收样本Completion=evidence_pending，维护正式task_resumed |
| T566-05 / SCN566-05 | 历史rawarchive/note可读后精确退役公共/私有control；旧工具不升级，旧正常context不再选择任务，历史义务与其他会话保留。 | 真实旧writer的history-only闭环通过，见下文 |
| T566-06 / SCN566-06 | 固定operation重试/丢结果/普通partialwrite，保留后续工作；install→convert→toolsrollback不兼容写前阻断。 | 局部恢复及最终matching-source的真实Guru组合兼容阻塞通过，见下文 |
| T566-07 / SCN566-07 | canonical/dogfood/installed完整graph、声明平台投影、sidecar/reapply/drift及原fullPlan2/current-only定向回归。 | source/installed及受控source-repo dogfood实际apply/reapply/drift/native全部通过；实际开发Task仍由旧完整安装拥有 |

验证上限：本普通Issue最多一个代表性真实安装拓扑，非完整Release矩阵。正式source lock采用、真实业务安装/迁移/会话恢复/外部验收、发布及清理均未执行。后续只在本文件记录实际命令、首次失败、修复后结果与边界，不把计划写成通过。

## 基础层定向结果

以下结果由实际 Trellis implement worker 执行，工作目录为本 Task checkout；仅证明各层列明对象，不替代 T566-03–07 的完整联合验收。

共同环境 `PYTHONPATH=trellis/skills/guru-team`，执行 `python3 -m unittest discover -s <目录> -p <模式> -q`：

| 目录 / 模式 | 实际结果 |
| --- | --- |
| `trellis/skills/guru-team/packages/guru-sync-base/tests` / 全部 | 15通过 |
| `trellis/skills/guru-team/runtime/tests` / `test_maintenance_foundation.py` | 3通过 |
| 同runtime tests / `test_python_update.py` | 7通过 |
| `trellis/presets/guru-team/scripts/python` / `test_verify_throwaway_python_routing.py` | 45通过 |
| `trellis/skills/guru-team/runtime/task_lifecycle/tests` / `test_identity.py` | 18通过；另以 `TRELLIS_FIXED_FORK_SOURCE` 指向 #40隔离来源 |
| `trellis/presets/guru-team/scripts/python` / `test_tools_only_installer.py` | 1通过；tools-only跳过全部language指导改写，普通apply原行为保持 |

实际packed公共contract/package digest与旧0.6.17 target inspection已核实，未修改全局CLI。shell syntax与基础Python编译通过。

首次集成未通过：普通transaction installer的16项测试先缺packed-assets环境，补入真实 `GURU_UPSTREAM_DELIVERY_SCRIPTS` 后仍被并行新package未完成注册的 `canonical_package_set_mismatch` 阻塞；该轮16 errors不计通过。source package检查也曾报告新增Finish command entrypoint schema错误，待原owner修复后完整重跑；未把结构检查当作semantic或安装通过。

## 真实旧 session 首次失败（上游 #40）

原0.6.17 writer生成带platform/last_seen_at/current_task/current_run的正常无版本local session，公共tools安装native postcheck返回 `unsupported_binding_schema`，预期为 `maintenance_required`。Guru资产尚未写入。Core carrier分类器和Python旧carrier诊断只识别singleton current_task，漏掉原writer的完整已知shape；不是用户篡改样本。修复归#40原owner，保留旧candidate和原失败operation；原candidate的rollback同样被已确认的旧carrier识别缺陷阻塞，原失败实例/ref/candidate保留。使用原source与相同writer生成的严格等价新实例，用新matching pair新建安装操作；原Task/planning/session bytes/modes一致，仅替换绝对root/common identity。不同candidate不能手改原plan假装同operation resume。回归须同真实writer/session输入经过原public安装/native路径，分别观察carrier识别、诊断分类及最终安装结果；Guru不能删session、放宽current parser或跳过真实native检查。


新增静态及局部回归：canonical source package graph已通过一次（40 active packages、125 commands，后续声明更新须复核），upstream ownership通过（22平台/43claims/22 overlays，无新增平台矩阵）。检查worker执行306个runtime/package/preset Python编译、44个shell语法、marketplace JSON、两套各12项Task context检查均通过；context仅报告既有大文件截断warnings。六个原owner维护入口定向20项、Sync15、foundation3、tools9、tools-only installer2通过。缺少新pair时native tests明确SKIP，不计native通过。ordinary preset transaction重跑仍进行中。


## 原生下一owner与runtime回归

独立Architecture实际复现：tools-only local pointer A之后，普通activation选择B仍写common/gitdir但读取A，返回fitness_regression。原runtime owner修复为已有local时读写同effective scope，并让原fullupgrade备份/restore覆盖不同effective路径；无override原行为保持。真实CPython3.12→3.14、primary/linked、目标shell resolver选择B、common/peer不变、原owner snapshot/restore恢复A bytes及0640模式已通过；原fullupgrade合同33项、foundation3项通过。

真实旧writer代表样本已经tools升级、同ref结果恢复和reapply通过，随后public selectedTask转换保留TaskKey/PRD、没有凭空Delivery/Completion/Closure；target自身task current/get_context continuation rc0、peer tree bytes/modes不变。但下一Guru branch owner仍返回unsupported_task_schema：它对registered checkout用HEAD旧Task记录判当前Task2，忽略正常尚未commit的转换结果。Identity已建立、checkout/session因缺Guru branch/resource绑定无法继续，R14不计完成。原C4应正确消费当前公共Task2及本次绑定事实，不能手写资源记录或强制额外commit绕过。

C4修复后原branch owner对已有公共绑定、live registered branch匹配的checkout，使用原Identity校验工作树canonical Task2与generation/active；不匹配时不回退HEAD。未绑定候选仍走原HEAD验证。37项branch/substrate回归通过；独立复制真实公共转换样本运行原C4建立ownership，HEAD和未提交Task2 bytes保持。该结果不是目标installed完整续接的替代。

随后在原真实安装目标通过普通preset reapply安装修复，逐一保留5个known managed更新.bak并归零sidecars后重应用成功。目标自身原Identity、C4 branch、C3 checkout与session依次返回identity_established、binding_established、checkout_resolved、session_resumed；原Author实际返回scope_requirements_ready。AI读取完整保留PRD及当前Task，确认未完成bootstrap义务仍保留、没有新Delivery或plan approval；维护observe/finalize重新执行实际native与Author后正式返回task_resumed（原TaskId/generation0）。peer同Task仍保留legacy HEAD，未强制提交或手写资源账本。

## 历史保留与验证边界

代表拓扑中独立选定仍为0.6.17的旧peer，使用其实际task.py writer生成history-only样本。真实source-loaded维护返回history_archived；raw archive/note可读、所选session退役，旧版本与scripts bytes/modes保持，primary已转换Task树不变。旧task.py current --source实际返回Current task: (none)、Source: none，正常退出码为1；另行get_context --json退出0证明旧入口仍执行。不能用JSON缺少current_task字段单独证明无选中，也不能把rc1记成rc0。

普通installer16项稳定性轮次实际14通过、2失败（current reapply和declared kernel），source并行修改期间出现conflict；最终冻结后只重跑这两项，尚未以中间轮次宣称16项全部通过。早期source变化后的tools rollback返回source-stale，不构成Guru兼容性门禁已执行；公共rollback独立实际返回incompatible_restore且Task/session/version/pointer不变。最终matching-source组合链路须单独记录。

本开发checkout仍承载旧Task及旧installed runtime；普通apply会被current-only guard写前阻塞。本轮不手改declaration、不放宽guard、不悄然迁移Task566。隔离样本可证明canonical安装投影，不等同本checkout dogfood整体切换。正式source lock仍缺维护API，local_candidate结果仅为隔离开发证明；业务安装、业务Task迁移、外部验收与Release矩阵均未执行。

最终冻结C4 source的严格等价样本已实际完成：Guru tools安装与同ref恢复 → 原维护wrapper执行8actions将原writer Task转换Task2 → 原Guru tools rollback调用公共owner，实际返回incompatible_restore。转换Task与rawsource、local/common session/binding、版本、本地Python pointer、原公共tools checkpoint与Guru原preimages/checkpoint的bytes/modes全部保持，未先恢复任何一半；没有重锚旧operation或将Task转换纳入工具备份。该次Task维护停在verification_required，仅用于回退顺序证明，不冒充A8或task_resumed。

最终两项ordinary installer定向重跑通过（2 tests，72.844s）：从仓库root设置PYTHONDONTWRITEBYTECODE=1、PYTHONPATH为preset scripts/python及canonical runtime、GURU_UPSTREAM_DELIVERY_SCRIPTS为匹配candidate的packed templates/scripts，经原resolve-python.sh启动unittest的test_current_reapply_remains_valid和test_installs_only_declared_runtime_kernel_files。此前从scripts子目录启动缺temporary lifecycle runtime、bare Python缺jsonschema的轮次均为环境失败，不计通过；没有改测试断言或生产代码消除失败。未受后续C4修改影响的其余14项原执行事实保持适用，不宣称重新执行了全部16项。

## 历史交付待验收的实际下一owner

以CMS #4的历史7406a45只读副本作为Task维护数据fixture，不改变原业务checkout或当前业务会话。原Publish与Merge独立只读核验真实PR15/head7406a45/merge53d8525/target dev，均返回verified_legacy_history。source-loaded tools独立安装后，原维护wrapper转换唯一Task/gen0，固定一个历史Delivery及其结果；5份原planning、历史planning副本和migration/source-task.json与原Git对象bytes/modes一致，当前candidate与四个gates均null，Completion/Closure为空。

目标自身原Identity/branch/checkout/session及task current/get_context continuation均成功。AI读完整原accepted scope、HOME-L01未执行的原test-plan及当前Issue4正式revision4责任，实际调用目标installed Completion返回evidence_pending：真实服务/素材、保存发布与产品44联合验收仍待原业务owner取得证据；不声明当前Architecture完成资格或任何业务通过。维护observe/finalize再次执行目标native与该实际owner，正式返回task_resumed。finalize前后Task全树bytes/modes不变，无新Delivery、Completion或Closure。这只证明历史快照可正确进入待验收路径，不替原业务会话作当前完成判断。

## 实际匹配依赖与最终门禁

修复后隔离CLI/Core仍同版本0.7.0-castbox.3，tar SHA-256分别为dd82a1dae0e2b325edcc9f310e2b7619a9f1dd88f94125f9b9aec2b2239904e1与036e895a4f088cc48e90f01cde0b8db91379ffb105f4dd3f135c909d39601496；实际执行CLI/Core digest分别为d51417e513d9f6f4469a0639d085e1a731a6672b4352977ab5be2708fa79e5e9与5e167afdc4c18809f7102e37af6737799d74e61096e3f6f8aa1d969b9093949f。源HEAD仍含未提交实现，不以HEAD或版本号代替这些实际包身份，也未改变正式source lock。

最终独立Architecture原owner返回baseline_current/task_impact_sync/phase2、architecture_impact、reviewed_candidate；未晋升shared CURRENT。RDT原owner完成task_impact_sync并返回ssot_current，协调task-owned差额与RDT96/Architecture90，不代替实现Check或文档晋升。真实业务采用、正式依赖采用、完整Release矩阵与本开发checkout旧dogfood整体切换仍未执行；声明平台和sidecar/reapply由隔离安装投影及原owner定向回归承担。

整体Phase 2不能据上述局部成功宣称passed：当前开发checkout只读diagnose_delivery_installation实际返回blocked/upstream_delivery_migration_required，检出224条旧Task记录，包含Task566本身；普通dogfood重应用未完成。A5的本checkout同步/漂移证据仍缺，不把隔离投影等同自托管切换。保持原安装及任务，不放宽guard、不扩大为全部历史Task迁移；此缺口作为当前Check的blocking verification，不赋予未复现代码问题severity，也不提交或发布。

上述首次Check实际返回blocked，但其将A5提升为“实际author checkout必须采用候选”的判断经fresh审查撤回：canonical workflow的Candidate migration boundary明确旧installed graph继续拥有开发Task，直到独立显式迁移；live A5没有要求本Task在采用候选后才能完成验证，既有#531受控source-repo dogfood验证也保留主旧runtime。原普通预检的224条结果是真实诊断，不是当前必须迁移这些记录的依据。原normal-scenario owner将该额外门禁判为rejected_no_authority；仍须补齐真实受控dogfood，不能据此直接判pass或声称主checkout升级。

同时确认一个真实当前缺口：本任务三个通用维护spec新段仅写在项目.trellis/spec/workflow，遗漏原canonical模板。原normal/solution owners均qualified_current，root owner判not_incident_applicable；现已在三个原canonical同名模板补入相同新段，不拷贝其他历史project/template差异，不改runtime或guard。由原installer与受控source-repo dogfood证明实际分发与漂移，源头修正后旧tools operation的source token不重锚；仍适用的runtime/owner行为证据按真实依赖复用。

## A5 受控 source-repository dogfood 最终结果

冻结完整当前canonical trellis树与既有carrierfix matching CLI/Core，在同一代表性受控source-repo中执行真实CLI三平台初始化：`init -y --claude --codex --cursor --workflow native-delivery-v1 --no-monorepo`。该CLI不解析本地marketplace路径，沿原安装验证器已有local_sample合同将冻结canonical Guru workflow放入目标，明确只验证未发布本地custom workflow，不声称远端marketplace下载或正式source采用。

从冻结author canonical运行原`apply.sh --repo <controlled>`首次安装，再从受控repo自身运行原`apply.sh --repo <controlled>`和`check-dogfood-overlay-drift.sh --repo <controlled>`；均实际退出0。受控repo同时包含完整canonical和installed图，非仅业务安装fixture。原installed模块validator返回passed：40 active package IDs、125 commands、9419 managed files、Claude/Codex/Cursor及shared投影正确，conflict/sidecar/private-package-test均0。目标自身managed Python解析且可import jsonschema，真实get_context及continuation均退出0；结束前author/受控canonical bytes与modes复核零差异，递归零.new/.bak。

保留原始失败：第一次使用旧native初始化成功但产生旧bootstrap，原apply正确返回migration_required；改用正式native-delivery-v1，未手改Task/.version/declaration。fresh source自身首装因无installed manifest在ownership写前失败，改由完整来源原installer生成manifest后再自有reapply。一次直接执行validate.py相对import错误，改用原installer使用的模块入口后通过，不是产品finding或通过证据。仅首个受控样本路径内重建正确初始化，不扩张Release矩阵。

因此A5的真实受控dogfood证据已补齐。当前开发Task及其旧installed graph、其他worktrees、224条旧记录和业务仓均未采用候选；该保留符合canonical Candidate migration boundary，不再被提升为当前Check阻塞。三份spec之外没有运行时代码变化：已有原生工具/任务/历史待验收/回退结果按未变的实际代码、工具链、匹配依赖和执行入口保持适用，不把旧operation重锚为新source，最终安装分发差额由本节的新冻结样本证明。

## 首次 committed Review 与文档晋升

原 Check 已完成真实 Phase2，exact commit `95bcf24334f9a4d25df3f9175af9d00b58d86915` 后工作树干净。独立 Architecture 对 `origin/main@3e8b281c93894cd3df4e704901bda63ca2885f23...95bcf24334f9a4d25df3f9175af9d00b58d86915` 实际返回 baseline_current / reviewed_candidate；同一合规 reviewer 随后完成独立完整 Branch Review，原 recorder、checker 与 public invocation 正式返回 passed，无实际候选或 P0–P3 finding。亲自运行 source/installed、matching legacy maintenance 5项、原 owner 23项、Sync15项、tools9项（另1共享写入 skip）、tools-only installer2项；实际历史归档、两类 task_resumed、CMS4 installed Completion=evidence_pending 和 incompatible_restore 原日志均已读取。未重放共享安装。

随后 post_branch_review pair guard 实际 unchanged；publication Architecture eligibility 实际返回 sync_required / promotion_required，未进入 Delivery readiness。原 owners 按 expected RDT `.96` / Architecture `.90` 维护 successor `.97` / `.91` 与 durable contribution / ADR-027。该晋升只承接已审查责任、trace 与实际证据，不改变代码、正式 source lock、旧 author runtime 或业务数据；新差额必须重新 Phase2、TaskCommit、独立完整 BranchReview，当前尚不宣称这些后续 gates 完成。
