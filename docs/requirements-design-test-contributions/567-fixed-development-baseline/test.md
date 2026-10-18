# 验证记录

这是 #567 当前实现候选的验证记录。Package/runtime、真实 Git/公共 API、实际 AI owner 执行和本地 GitHub 模拟分层陈述；不代表真实 GitHub 发布、最终验收或 Release Gate 已完成。共享知识晋升文档差额另须 fresh gates。

## 定向验证

| CASE | 当前结果与证明范围 |
| --- | --- |
| T567-01 | real Git＋公共 Delivery API 的固定候选3项通过：registered peer fetch 不改变候选；实际 HEAD 演进保留旧 Check/full_review 历史但令其不适用；D2依据真实 D1 delivery_result 选增量并恢复自身范围。 |
| T567-02 | Reconcile runtime41项通过：ordinary、实施前 resolved baseline、实施后 resolved candidate、add/delete/mode、精确提交、同操作恢复及固定目标期间 ref 推进。原公开 transport 与原 Task/Delivery API 接续均有定向证据。后续完整package检查检出BR567-F2，修复后完整49项通过，详见下文。 |
| T567-03 | TaskCommit42项通过，含 committed reentry9项：当前 Check 固定B、完整范围、dirty精确事务/hooks、已提交候选保留、结果丢失恢复及首次完整 Review 义务。 |
| T567-04 | Merge最终全套45项通过；补齐当前gate2.0 schema注册后 contract10项再次通过。覆盖仅behind/目标推进、实际blocker、私有1→2投影、historical migration与同操作恢复；fixture的server facts不冒充live策略。 |
| T567-05 | Finish contract60项及新增private2→3迁移1项通过：expected-head bookkeeping、Closure/source变化、固定事务与target推进后的可达性恢复。Completion21项pytest通过。 |
| T567-06 | 最终 canonical source validator通过：40 active packages、124 commands、当时111个test目录文件（非测试执行数）。受控 source＋installed 自身apply/reapply、installed/activation validator通过：Claude/Codex/Cursor＋shared、9420 managed files、0 conflicts/sidecars/private tests。最终drift通过；完整canonical字节/权限复核及native get_context continuation通过。采用README已声明的local workflow sample，不声称远端marketplace安装证明。 |
| T567-07 | 实际 AI 双Delivery owner链完成到原Finish success，详见下文。原真实Reconcile41和Merge45提供实际阻塞/恢复的确定性回归；不把fixture预写pass称作AI语义执行。 |
| T567-08 | Main fresh独立Phase2 Architecture正式baseline_current / architecture_impact / target_native / reviewed_candidate；原RDT正式ssot_current。该记录描述实现时的task-owned候选。修复后完整独立committed Review及本次共享知识晋升差额见下文；后续门禁以各原owner实际结果为准。 |

另有 Readiness21、Publish26、active fixture composition2、scope revision3项通过。BranchReview最终44项通过，首次独立审查检出的中间失败与修复见下文。变更Python解析、package shell语法、task context和ownership validator通过；ownership覆盖22平台descriptor、43 managed claims、22 overlays。未执行完整多平台安装矩阵。

## 主 Task 提交与 BR567-F1 修复

原 installed Check 正式通过后，原 TaskCommit 已创建本地实现提交 `62e7ef1baf3af263af0922b3e8baf0d89d862ae9`，完整范围为 `3b165daef0001bd9816c0bf3bbe928bcb59de390..62e7ef1baf3af263af0922b3e8baf0d89d862ae9`，共111路径。fresh独立 reviewer 先完成该完整范围的 Architecture，正式返回 `baseline_current / architecture_impact / target_native / reviewed_candidate`；随后实际 BranchReview 返回 `implementation_required`，唯一 finding 为 `BR567-F1 / P2`，没有把前序 Check 或 Architecture 当作完整 Review 通过。

该 reviewer 重跑 BranchReview 全套时为43通过、1失败：`test_workflow_closes_delivery_completion_finish_and_promotion_architecture_routes` 仍逐字要求本轮已移除的无条件 stale/sync 政策及旧 promotion 原句。此前44项绿色日志不覆盖这次最终文案，不能作为当前全套通过证明。normal/mechanism资格均实际返回 `qualified_current`，root为 `not_incident_applicable`，属本轮测试消费者迁移遗漏。修复仅删除这两条废弃逐字断言，保留现有阶段、owner、promoted与执行顺序检查；没有冻结另一组新文案或改产品行为。修复后亲自重跑同一完整套件44/44通过，随后实际完成fresh Phase2 Architecture、原Check和原TaskCommit，本地两文件修复提交为 `bc5bb42677140b326a6f6ac59751fd68b26b1b55`。原finding owner瞬时核验F1关闭；不同fresh reviewer执行的后续完整Review仍检出下述F2/F3，未把F1关闭等同完整Review通过。

首次 canonical source validator记录40 active packages/124 commands/111 package test files；独立复跑时计数197，差异来自validator统计本地编译缓存文件。该计数不是测试执行数或语义充分性；两次source验证均通过，未把缓存计数差异列为产品finding或扩大修复。

## 完整package检查与 BR567-F2/F3 修复

第二次独立完整committed Review覆盖 `3b165daef0001bd9816c0bf3bbe928bcb59de390..bc5bb42677140b326a6f6ac59751fd68b26b1b55` 的111路径。reviewer先独立评估完整差额/consumers，再实际调用原Architecture，取得 `.91` 的 `baseline_current / architecture_impact / target_native / reviewed_candidate`；原BranchReview recorder、checker、public invoke随后正式返回 `implementation_required`，F1为resolved，当前open为F2/F3。

- `BR567-F2 / P2`：Reconcile完整套件48通过、1失败，`test_interface_commands_errors_and_examples_close` 仍断言8条命令，本轮guard退役后实际为7。修复删除这项旧数量冻结，保留既有command/schema/example、launcher与help闭合检查，不恢复guard，也不冻结另一个chosen count。修复后以同一无bytecode环境亲自重跑完整package：49通过、51 subtests。
- `BR567-F3 / P2`：补跑Approval contract套件时为18通过、3失败，其中ordering测试查找已退役的 `resume_target=delivery_activation` 而产生 `ValueError`。base中该marker存在、current退出；修复只在实际Delivery activation节内核验展示先于直接调用原 `guru-activate-delivery`，保留展示、语义结论、选择与对话要求。修复后contract为19通过、2项下述已归因边界；本次ordering用例已通过。

F2/F3均由原normal/mechanism/root公开入口实际取得 `qualified_current` / `qualified_current` / `not_incident_applicable` 后才进入finding和修复；没有借测试失败恢复旧政策或扩张产品机制。修复差额仍按原Check、TaskCommit、不同fresh reviewer完整Review接续，不把测试绿色当formal BranchReview通过。

完整套件也暴露了正常fixture环境差别：首次Check/TaskCommit执行时，fixture在base之后导入上游Python而生成并提交 `.trellis/scripts/common/__pycache__/*.pyc`；新完整候选正确包含这些额外已提交路径，但旧fixture owner只审 `app.txt`，故不能通过。实际重建Git候选确认额外路径均为bytecode；仅增加 `PYTHONDONTWRITEBYTECODE=1`，原失败消费者不改代码即通过。没有为此修改产品路径过滤、放宽Check覆盖或增加测试实现。

| 当前完整/扩展检查 | 实际结果与边界 |
| --- | --- |
| DeliveryProjection / Merge / Finish / BranchReview | 独立reviewer实际16 / 45 / 64 / 44项通过；相应subtests另列，不冒充新case数。 |
| TaskCommit无bytecode全套 | 42通过、14 subtests；覆盖未改的实际消费者，首次bytecode污染执行不记绿。 |
| Check无bytecode全套 | 53通过、54 subtests；1项 `legacy_controls_retired` exit-list旧断言失败。该test和interface均与base字节相同，属继承边界，未修复、未称全绿。 |
| doc-only受影响contract | Activation6、Author2、Architecture32、RDT9通过。Approval修复后19通过/2失败：旧installed eval runner拒绝base已存在的kernel文件，以及与base相同的legacy extra-exit旧断言。实际test/interface/kernel文件均与base相同；不扩范围调整旧运行图或历史断言。 |

此前runtime子集未覆盖F2/F3的contract消费者，本轮因真实失败补齐相关完整/contract检查。当前修复只有package-private测试与唯一Test，不改变managed安装payload；既有matching安装/reapply/drift证据只承接其未变依赖，不声称本轮重新安装或所有canonical测试字节重新比对。该轮实现检查时共享Architecture/RDT尚未晋升；本次晋升差额见下文。

## 修复后的完整 Review 与知识晋升差额

F2/F3修复已通过fresh Phase2 Architecture、原Check与原TaskCommit，本地三文件提交为 `f2538d822dbede7ea34dc29bdad9a0f828130dad`。原finding owner瞬时核验F2/F3关闭，保留原introduced `62e7ef1` 与真实 `62e7ef1→bc5bb426→f2538d8` 祖先链；F1先前已关闭。不同fresh reviewer独立审查完整 `3b165daef0001bd9816c0bf3bbe928bcb59de390..f2538d822dbede7ea34dc29bdad9a0f828130dad` 的113路径，先取得原Architecture正式current，再经原BranchReview recorder、checker与public invoke取得 `passed`；没有把原失败、Check或closure换标签作为完整Review通过。本轮reviewer还亲自重跑source validator、controlled installed validator和drift，核对87个变更managed依赖及2669个完整非测试产品文件的字节/权限一致；未把package-private测试文件称作已重装。

本次原owners按expected Architecture `.91` / RDT `.97` 晋升到 `.92` / `.98`，ADR-028只承接已审贡献。当前晋升新文档差额仍须fresh Phase2、TaskCommit和不同reviewer独立完整Review；本节不将promotion前的结果当作后续gates通过，也不证明Delivery、Completion或Release。

## 实际 AI owner链与真实 Git

受控 checkout包含完整 canonical source、matching CLI/Core/Guru安装，远端为本地bare；registered peer工作树在Planning、Check、Review、两次Delivery之后及Finish期间真实commit/push/fetch共享origin/main。根AI及fresh独立reviewer亲自读候选、形成判断，再调用原wrapper；未以host预写结果代替这些判断。

D1实际完成 Task2原writer、branch绑定、整体scope、Delivery创建、Author requirements、fresh独立Architecture candidate、Author solution、Wording record/check/invoke、独立final_plan、Approval、Activation、implementation begin_check、fresh独立Phase2 Architecture/RDT、原Check、必要TaskCommit、原rework/begin_check及提交封装差额Check、clean committed reentry、fresh独立committed Architecture/full BranchReview、Readiness、Publish、Merge。D1未单独调用publication阶段Architecture，故不把该轮称作每项mandatory invocation均完整的workflow证明；D2补齐该项。

D2按同一原owner链完成，并实际执行publication阶段Architecture。固定B为真实D1 reviewed head `92c74c1d2b535044d251778692798fc78b4badb3`，实际H为`be2ce7be3b4071759ef52c6f83f854891a52fa6d`，产品paths只有`verification/d2.txt`，没有重复D1。提交前Check同输入重试返回相同result；必要提交后原owner审封装差额并产生新Check，clean reentry保留同一H。fresh独立Review完整覆盖七文件B..H及metadata dirty，正式full_review为`full-review:a75f19fa9de40df3d49b982e87dd4b7d2c634db9fce580b19a9cb4732c6f6651`。

模拟PR1/2均仅BEHIND、MERGEABLE、checks成功且无服务器更新要求；原Merge实际创建并核验Git merge commits：D1 `e52fcdda8d925c8f6525b823b17884e3d9519bd3`，D2 `8b4155bde96726ea6c6ce6226423396bf570d9b7`。D2同一Merge调用结果恢复一致，无第二次mutation。实际target读回d1=`first\n`、d2=`second\n`。

旧D1 Completion截点在D2后由原wrapper拒绝，错误为`stale_identity/semantic_result`，没有冒称当前完整。当前AI保留D1事实、补实际D2事实，结合整体PRD、两次Review与whole-task acceptance_finish Architecture重新判断后，原Completion返回`completed`，原Closure返回`no_mutation`。未执行 #569 查询准备或历史遍历新机制。

原Finish依次执行本地archive、bookkeeping commit/push/模拟PR3、expected-head merge，返回`success`。Task branch不含最新target；target在bookkeeping发布后前进仍可合并，成功后再次前进仍恢复同一`finish:v1:2671ade13fd0941b`。归档保留D1/D2及Completion/Closure事实。Task branch只有scope定义、D1、D2和bookkeeping四个提交；自动Reconcile、同步提交、base触发回退、空提交均为0。未执行Cleanup或删除这些隔离资源。

## 验收映射与边界

| 验收 | 当前证据 |
| --- | --- |
| A567-01/02/10 | 上述实际AI链、registered peer共享ref推进、D2固定范围与同操作恢复、整体Completion/Finish；零Reconcile路径有真实Git和原public owner结果。 |
| A567-03 | 当前stage-applicable Architecture/RDT与工程合同审查、原owner输入/validator消费者检查及无关peer内容推进。没有另造CURRENT promotion来证明无关版本；不把目录白名单当适用性。 |
| A567-04 | D1实际merge、D2增量、旧截点拒绝/补缺Completion、Finish目标推进恢复；没有为ancestry补提交。 |
| A567-05/06/07 | 原Reconcile ordinary/resolved/committed/continuity公共transport与真实Git回归、Merge实际blocker回归；固定target期间再次ref推进仍完成原操作。冲突/检查差额由当前AI审阅原owner合同和实际测试；这部分是确定性fixture证据，并非另一轮完整AI冲突后PR发布或live GitHub。 |
| A567-08 | scope revision3项实际公共API回归、原Reconcile planning-authority变化/explicit integration路径，以及当前语义owner责任审查；真实scope变化不靠旧gate放行。 |
| A567-09 | 各原owner同操作恢复、Merge私有1→2、Finish私有2→3、MIGRATION-567与保留#566边界；开发checkout本身未迁移。 |
| A567-11 | 实际AI样本的仅behind无更新要求对照＋Merge具体checks/BLOCKED/policy回归。服务器要求由fixture模拟；未触真实GitHub Ruleset或服务器强制更新配置，不声明live服务端证明。 |
| A567-12 | T567-01..08、最终完整matching source/installed、三平台shared、reapply/drift/native continuation。完整Release/Upgrade矩阵由专门Issue拥有。 |

## 首次失败、恢复与未解决的基线验证

已修复并重跑：旧source checker不识别新版inventory改用canonical同版模块；固定候选测试重复发现导入用例改模块别名；Reconcile漏import/陈旧moving-ref断言；TaskCommit reviewed_paths遗漏完整candidate；BranchReview陈旧文案/interface索引/profile断言；Merge删去无用参数后遗漏caller。最终结果分别如上，失败日志不计通过。pytest依赖通过managed Python＋uv隔离依赖提供；缺显式upstream目录的执行是环境失败，补真实目录后重跑。

最终apply首次由PATH选择无锁定wheel的Python而失败；改为显式managed Python后完成managed更新，quality-guidelines产生的已知bak在成功reapply后未残留。初次final drift指出workflow仍为前freeze；确认它与freeze Git blob完全一致、无本地定制后，按README local sample机制复制最终canonical，随后drift通过。preset apply不管理workflow，未掩盖这项差别。

phase2_authoring在author旧安装下原9项中8项通过，1项source/installed identity失败；在最终matching source＋installed单独重跑该identity项通过。额外matching全套9项有7个staging errors：继承的fixture_io只复制scripts/workflow，没有在已有Delivery API时复制`.trellis/.version`，child apply报`unsupported_delivery_api / installed_core=null`。fixture_io与HEAD完全相同；这不是#567运行时回归，未扩范围修复，亦不把该次全套记绿。实际matching安装与AI owner链不使用该缺失version的子fixture，均已独立验证。

扩大的preset定向6项中3通过、3失败，未称全绿：manifest测试仍期待既有旧Merge aggregate schema1，而HEAD/current interface已为aggregate2；Finish退出数断言期待5，而HEAD/current均为6；managed-Python测试期待fixture_io旧exact string，而该生产文件与HEAD相同。两个完整测试函数、第三项失败断言及对应生产事实均能从HEAD确认继承。manifest测试本轮只移除retired guard声明并新增当前gate2.0安装清单断言；没有顺带修改历史aggregate断言。

曾检查“旧constructor符号base在恢复时漂移”候选。实际运行HEAD旧constructor与当前公共begin_check时，原store先拒绝`candidate_mismatch: base must be an exact commit`，未写入该候选；原normal-scenario正式返回`rejected_not_reproduced`。没有据此增加防御实现、负例测试或finding。

未验证真实GitHub mutation/服务端更新策略、远端marketplace exact candidate、业务仓采用、开发checkout迁移和完整多平台Release矩阵。以上只声明各实际观察层，不声明生产效果或Release Gate通过；本地实现及修复commit已完成；本次Architecture `.91→.92` / RDT `.97→.98` 晋升只承接已审贡献，其新增文档差额尚须fresh Phase2、TaskCommit和不同reviewer完整BranchReview。真实主仓push/PR/merge/tag/Release未执行。
