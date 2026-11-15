# #850 测试完整差额

状态：integrated_pending_review。固定前驱为Git `a72981db56d2070d8140b468cab3a97ae82effd3` 的同名current单元。原语义owner为guru-maintain-requirements-design-test-ssot；以下是已写入并读回的完整变更章节/稳定单元，其余正文及历史观察保持。关联来源及替代范围见traceability.md；精确API仍由canonical packages与MIGRATION-850单写。

# 完整整合目标：docs/test/current/issue-content.md

## T850-01 / SC850-CONTENT：实际有界语义审核

实际Agent经Clarify standalone_wording_review审核正常草稿与完整来源，指出义务弱化、条件/返回遗漏或验收不明，标位置/影响/原修订owner；预期不入被测上下文。原writer正常返修后再审，保首稿/首错；合法建议/default/quote/history/literal不因词面阻塞。必要来源缺失实际blocked。显式文件经review-change explicit_files/wording_only捕获并审核完整Markdown，含Git未变文件；核snapshot、正式invoke和无对象/Task/session写入，不以进程exit0代替判断。对应R850-01/D850-01。

## T850-04 / SC850-ADOPTION：匹配采用及退役

原tools owner安装/reapply后读回resolver、installed/native、三平台bytes/mode、退役资产、sidecar及Task/session/配置/peer。普通模式偏差保原观察及恢复，不手改manifest/checkpoint，不把准备当成功。源码、Agent、安装、外部层分开；formal_source_lock、完整Release矩阵与未执行外部效果保持未验证。对应R850-04/D850-04；实际观察由#850贡献test.md单写。

# 完整整合目标：docs/test/current/local-fix-intake.md

## T819-03 / SC819-ROUTE：实际分流与终点

从原已有Issue→Sync→Readiness入口，观察直接ready、事实/需求/措辞局部补审、必要完整链、真实阻塞/恢复及多缺口最早依赖。局部实际producer必须返回同次Readiness；事实不变不自动补Clarify，需求变化只刷新受影响内容判断；措辞问题由原Clarify wording_only真实producer处理，不保留独立Wording补审。另观察讨论/草稿/只创建/创建并开工及原no_issue边界。实际AI判断和完整答复单独验证，机械出口或文案存在不代替它。对应R819-02/03/04、D819-02/03/04。

## T850-02 / SC850-LOCAL：实际措辞局部往返

用原#819正常三来源及真实Sync/Readiness/Clarify wrappers，Agent自行判gap/focus，不预填supplement_requirements、wording_only或pass。仅实际出口要求该focus时进入Clarify，原owner修订沿source_actions/readback，真实supplemented以同Issue/base/continuation回Readiness，必要context往返保focus。受控GitHub fixture不证明live写入。旧helper预选exit/复制示例语义只证明装配，不算实际Agent。本轮live#850 ready未触发该分支，不证明已覆盖或不能另用fixture补验；本轮独立Sol/medium Agent已在受控本地三来源fixture经原Sync、Readiness、Clarify及同次Readiness实际往返；保单次PATCH/GET及首错，具体观察由原贡献test.md单写，不证明live GitHub写入、完整链或全部正常分支。对应R850-02/D850-02。

# 完整整合目标：docs/test/current/task-delivery-lifecycle.md

## T531-02 完整拟后表行

| 稳定scenario/test identity | 正常起点/动作 | 必须观察 |
| --- | --- | --- |
| T531-02 / R531-01/02 | 同Task建立D1、独立D2，分别写规划 | key/root/文档和历史分开；Task scope持续；唯一Author、独立Architecture candidate/final与Approval，Activation是真公共Planning writer；无独立Wording前置。 |

## T850-03 / SC850-PLANNING：实际内容与审核链

Agent读完整来源及整体/切片要求，由Author写规划，独立Architecture candidate/final和Approval各自判断。真实遗漏交原writer，修订后依实际出口刷新必要依赖，不重标旧pass。保切片边界、条件/例外、Policy/Docs Plan及提交后一次正式Review顺序。同切片content_revision及在途恢复区分wrapper和实际Agent；不手改hash/state，不把旧provider输出给当前reader。#657等历史截止保持；隔离Planning不是真实#850 Planning/Check/Completion结果。对应R850-03/D850-03。

# 本轮实际观察与不足

观察对象为#850 D1，真实checkout的固定B仍为a72981db56d2070d8140b468cab3a97ae82effd3；当前未形成TaskCommit或独立committed Review。

- 实际模型通过CLI参数或原生spawn参数绑定GPT-6.1-Sol/medium。首轮read-only CLI对草稿完成语义判断，但原公开入口报runtime_dependency_missing，无正式typed exit；文件CLI的capture/invoke同样未正式完成。原错误不改称通过，未为它修改collector或运行时。
- 后续原生独立Agent通过原Clarify standalone_wording_review实际发现草稿的联合条件、无选择保持状态、返回内容及行为验收缺失，报告位置/影响/原writer。原writer另建正常修订稿，原reviewer再审，实际reviewed且findings=[]。合法recommended建议与default_mode literal保持。必要来源缺失的另一请求实际blocked，未猜测来源。
- review-change explicit_files/wording_only实际完整审核README.md与MIGRATION-850.md，capture/invoke均成功并reviewed。README相对HEAD未变，捕获实现按选定完整bytes/mode绑定，不以diff代替正文。对象与已比较Task/规划/runtime无写入；不声称持有全部私有session文件的完整前像。
- live #850的Sync read及Readiness existing_issue_intake实际baseline_ready→record/check/invoke→ready。没有人为制造gap。该次未进入Clarify局部补审，不能算T850-02通过；原#819 fixture的预填helper只证明装配。该次仍不作为局部往返证明；后续实际fixture观察见下一项。
- 新独立原生Agent在spawn参数绑定GPT-6.1-Sol/medium，完整读取原要求、合成Issue和有效评论，自行发现AND验收被正文误写为OR；原Sync read实际baseline_ready，Readiness existing_issue_intake真实record/check/invoke返回supplement_requirements、review_focus=wording_only。原Clarify source_actions仅一次fixture gh PATCH替换验收句，再GET回读完整payload，原record/check/invoke实际supplemented；薄投影result_summary为requirements_result，原Readiness issue_review_return重读完整对象与固定B的README并真实record/check/invoke到ready。四个公开出口均保持example/repo#27、git_object及固定B、stage0-current、standalone；标题、评论与需求范围保持。派发前中止无PATCH回执后先GET确认状态；首个实际producer错误stale_identity/source_actions.preimage_sha256(exit3)，随后mutation_results(exit3)及invoke缺owner_context(exit2)均保原输出，在调用期内存重建正确authoring/摘要/envelope后恢复，无重复PATCH、无provider或仓库写入。该fixture来自原#819正常source_actions及fake-gh方式，只证明本地受控同次往返，不证明首次正确、live GitHub写入、完整Intake或全部正常分支。
- 一个隔离原Task/Delivery fixture实际执行独立Architecture candidate assessment、Author solution planning、final_plan、Approval。首次Approval发现切片PRD仍是整体来源副本，真实revision_required；main另指出实施计划把正式Check写在提交前的顺序问题。原Author正常返工七节PRD及顺序，沿requirements_ready→新candidate assessment→solution planning→final_plan→Approval revision_reentry，实际approved。角色各自读取完整来源/当前对象并通过原wrappers，不预填语义通过。原投影外读取路径和Bind引用路径首错保留，不能称首次正确；未执行Activation。隔离规划不是真实#850的Planning结果或Completion。
- 原tools完整匹配安装及独立reapply实际tools_upgraded。重应用曾因capture父进程umask077，使23普通文本从prepared0644变为0600；原输出和readback保留。后经独立原owner冻结操作、仅installer子进程umask022恢复，23文件均0644，9992受管投影bytes及原installer modes匹配。用户config按原owner逐字/模式保持，不以其非canonical内容制造冲突。installed42 active/123 commands、目标resolver/native/Phase2.1、dogfood drift通过，退役目录无残留、sidecar零，已比较Task/配置/peer保持；这些是实际目标事实，不改称源码测试或业务采用证明。
- 此前131定向工程检查、54AST/63JSON的原始日志和receipt编号未保留到当前可重开证据，本owner不将该组标为本轮直接复核通过；已有执行者摘要不能替代当前独立Review的验证责任。当前可直接核验的是实际安装、投影及本轮Agent公开出口。

结论限于以上实际覆盖。T850-02的受控本地实际Agent往返已覆盖；live GitHub写入、全部正常分支、formal_fork_source_lock、完整多平台Release矩阵、正式外部创建/发布及业务采用保持未验证。文档整合仅为integrated_pending_review；真实#850 scope/key/implementing与原适用Planning保持，没有Check/full_review/readiness/Completion结果。
