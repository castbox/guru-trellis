# 验证记录

这是 #567 当前实现候选的验证记录。Package/runtime、真实 Git/公共 API、实际 AI owner 执行和本地 GitHub 模拟分层陈述；不代表真实 GitHub 发布、最终验收、共享知识 promotion 或 Release Gate 已完成。

## 定向验证

| CASE | 当前结果与证明范围 |
| --- | --- |
| T567-01 | real Git＋公共 Delivery API 的固定候选3项通过：registered peer fetch 不改变候选；实际 HEAD 演进保留旧 Check/full_review 历史但令其不适用；D2依据真实 D1 delivery_result 选增量并恢复自身范围。 |
| T567-02 | Reconcile runtime41项通过：ordinary、实施前 resolved baseline、实施后 resolved candidate、add/delete/mode、精确提交、同操作恢复及固定目标期间 ref 推进。原公开 transport 与原 Task/Delivery API 接续均有定向证据。 |
| T567-03 | TaskCommit42项通过，含 committed reentry9项：当前 Check 固定B、完整范围、dirty精确事务/hooks、已提交候选保留、结果丢失恢复及首次完整 Review 义务。 |
| T567-04 | Merge最终全套45项通过；补齐当前gate2.0 schema注册后 contract10项再次通过。覆盖仅behind/目标推进、实际blocker、私有1→2投影、historical migration与同操作恢复；fixture的server facts不冒充live策略。 |
| T567-05 | Finish contract60项及新增private2→3迁移1项通过：expected-head bookkeeping、Closure/source变化、固定事务与target推进后的可达性恢复。Completion21项pytest通过。 |
| T567-06 | 最终 canonical source validator通过：40 active packages、124 commands、111 package tests。受控 source＋installed 自身apply/reapply、installed/activation validator通过：Claude/Codex/Cursor＋shared、9420 managed files、0 conflicts/sidecars/private tests。最终drift通过；完整canonical字节/权限复核及native get_context continuation通过。采用README已声明的local workflow sample，不声称远端marketplace安装证明。 |
| T567-07 | 实际 AI 双Delivery owner链完成到原Finish success，详见下文。原真实Reconcile41和Merge45提供实际阻塞/恢复的确定性回归；不把fixture预写pass称作AI语义执行。 |
| T567-08 | Main fresh独立Phase2 Architecture正式baseline_current / architecture_impact / target_native / reviewed_candidate；原RDT正式ssot_current。贡献仍为task-owned candidate，未promotion。主Task的正式Check、真实工作提交和独立committed Review各以其原owner实际结果为准。 |

另有 BranchReview44、Readiness21、Publish26、active fixture composition2、scope revision3项通过。变更Python解析、package shell语法、task context和ownership validator通过；ownership覆盖22平台descriptor、43 managed claims、22 overlays。未执行完整多平台安装矩阵。

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

未验证真实GitHub mutation/服务端更新策略、远端marketplace exact candidate、业务仓采用、开发checkout迁移和完整多平台Release矩阵。以上只声明各实际观察层，不声明生产效果或Release Gate通过；真实主仓commit/push/PR/merge/tag/Release和共享Architecture/RDT promotion均未执行。
