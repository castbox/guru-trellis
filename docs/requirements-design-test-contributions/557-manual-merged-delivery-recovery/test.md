# #557 唯一 Test 结果

状态：implementation candidate；本文件单写实际验证与未验证边界。

| Test identity | Actual observation |
| --- | --- |
| T557-01 formal chain | 完整matching Codex组合实际完成Creation、Delivery Planning、Activation、Check、TaskCommit、独立完整Review、Readiness与Publish。真实PR castbox/guru-trellis#563已普通two-parent合并为f1a010051207b1786953c3312b4257ea1cd7480c，无Guru trailers或Merge gate。原Merge正式返回delivered，exact同输入重入只读返回同结果且task.json字节不变；query2实际读回唯一事实。原Completion完整审查整体scope、actual content、真实CI与所需证据，正式返回completed（completion:e990ed15-ff05-4d4c-ae46-42d1709daa06）。实际JSON、8项完整PR差额及各原owner结果有真实观测，未使用provider或judgment fixture。 |
| T557-02 CI truth | 九项手动恢复组件回归通过，其中全绿/pending/cancelled/missing/failed均得到可靠 delivered；原 gates/Publication 保持。Completion fixture分别保留 evidence_pending/remaining_work 或 completed，无伪造统一 pass。 |
| T557-03 identity | 错误 PR 选择、公开 Publication 重复关联、未合并、base mismatch 均留原 Merge且不写假结果。测试通过正常公开操作构建重复关联，没有手改 store/hash/state。 |
| T557-04 actual candidate | actual head 新增原 candidate.paths 之外路径，实际 DeliveryFact/head 与原 Publication/head 分离；旧 gate 未改。完整差额由实际 Git读取。 |
| T557-05 recovery/history | 基线推进、head branch删除、当前HEAD不同、record后projection失败和stdout重入、query2只读恢复通过。query1仍无此无trailers事实；原schema1/2/bookkeeping回归另列。 |
| T557-06 old paths | 最终 Merge package 39 tests全部通过、无skip：新增9项及原 expected-head/trailers、schema1/2 history、私有历史迁移与原正式输出恢复。 |
| T557-07 installed/distribution | matching clean完整安装与两项 installed公开wrapper组件回归通过（query2历史/Completion不同CI出口）；当前canonical reapply完成，触及bytes一致。installed validator通过：38 packages/114 commands，Claude/Codex/Cursor选定投影、0 conflict/sidecar/removal。这些仍是组件与分发证据，前序语义/provider为fixture。 |
| T557-08 static/docs | source validator38 packages/114 commands通过；官方context validate通过（大spec截断告警已直接读）；5个触及Python文件语法通过、全部低于3000行，最大495行；git diff --check通过。RDT调和与正式Check另由原owner执行；知识晋升与软件交付是独立事实，须遵从各原owner。 |

## 首次失败与证据层

原 base ccf67ff157dc006f236870049dda9cba0fafa73f 的实际 Merge public wrapper，
面对真实本地 two-parent merge、公开 Publication 与 provider fixture，返回exit2：
schema_mismatch / field_path=profile，要求使用既有 Delivery profiles。
当前新增 profile 已从相同公开调用边界输出 delivered；这证明组件入口缺口，
不证明实际 GitHub、installed AI owner审查或原业务事故修复。

测试开发曾出现 provider fixture遗漏body/格式不匹配和dirty task metadata
阻止fixture checkout；已修正fixture和真实Git构造，未把这些错误称为产品缺陷。
clean install首次从target cwd启动，遇到 Guru temporary lifecycle runtime is
unavailable；原preset要求从source执行，改为source cwd后同一样本安装成功。
未改installer、公共模块或node_modules绕过。

后续文案更新首次reapply报告conflict；再次完整原apply得到ok，实核两处触及
installed合同与canonical bytes一致，样本无.new/.bak。此前manual_recovery.py
受管.bak经preimage与新canonical核对后处理；未强制覆盖用户修改。
原source旧dogfood普通apply实际拒绝：delivery_upgrade需要reviewed Plan2及
original-owner私有迁移；drift实际报旧模型finish-work入口不匹配。未半升级，
该项是迁移前置未满足，不是PASS。

本轮原RDT的task_delta_reconciliation正式返回ssot_current；fresh独立
Architecture phase2正式返回baseline_current / reviewed_candidate。
此前原Check完整九维审查正式返回blocked，唯一缺口为T557-01真实公开全链；
没有代码finding，非passed checkpoint已由原owner消费后删除。当前T557-01真实
观测已取得，原Check须按更新后的完整候选与依赖证据重新判断，不把旧blocked
或验证Task的completed直接改称Source #557通过。

真实验证资源：castbox/guru-trellis 的 codex/557-validation-base，root commit
a426a6e3e814d6d3be43cc1ba33102c069796fbe（仅README/.gitignore）；本地
codex/557-validation-head位于同一Git common-dir的独立linked checkout。
正式Task 557-manual-merge-validation / generation0 / source=no_issue，由原
Task Creator创建并由其check_result读回；原Clarify接受实际Author root PRD，
原Delivery Creator分配aaac7ead-8b99-4674-aff0-a463fe2280cf并返回planning_root。
所有前序语义判断由当前执行AI依据实际事实完成；此链没有provider或owner
judgment fixture。原Author正式返回plan_ready，完整三文档Wording返回pass；
fresh独立final_plan Architecture实际返回baseline_current / no_architecture_impact /
no_change，原Approval完整八维审查并经record/check/invoke返回approved，其private
checkpoint已由原owner退休。原Activation实际返回delivery_started并写公共Planning；
真实夹具已写入且接受字节保持。原implementation begin_check绑定精确candidate后，
完整Check实际record/check/invoke返回passed，Delivery进入reviewing。Check第一次
public调用因传入recorder的artifact_path/dry_run元数据被schema拒绝；原owner重新
核对当前候选并以纯semantic checkpoint完成正式调用，未改实现或弱化schema。
Activation前曾读base facts但漏调用原post_plan guard，随后实际补核为unchanged；
post_check guard亦为unchanged。上述纠正是本次操作事实，不当作产品缺陷或早先执行。
原TaskCommit已提交精确8项文件，commit为30c7ccd1322c5c0c2de397b2120ea31c4b9fbf05。
其HEAD变化由原Reviewing rework、implementation begin_check与fresh完整Check承接，
只读TaskCommit重入沿用同一commit，未产生第二提交。精确a426a6e3...30c7ccd完整
Branch Architecture与Review均实际invoke通过，无P0–P3 findings；Review checkpoint
由原consumer退休。原Architecture新的publication调用返回current/no_change，原
十维Readiness返回ready。post_check/post_commit/post_review/prepublication guards
均为unchanged。原Publish实际preview确认远端head与candidate PR均不存在，计划
首次push/create及Ready接续；随后原Publish已实际执行并返回ready_for_merge，PR#563
为OPEN/non-Draft，head30c7ccd、base codex/557-validation-base/a426a6e3，完整8项
PR差额与已审查提交一致。实际正文摘要5fa00432保持，唯一公共Publication关联已
由原writer写入；Planning/Check/full_review/readiness仍applicable。实际CI rollup与
reviews均为空，状态按missing保留。

实际普通two-parent merge为f1a010051207b1786953c3312b4257ea1cd7480c，parents精确为
a426a6e3e814d6d3be43cc1ba33102c069796fbe及30c7ccd1322c5c0c2de397b2120ea31c4b9fbf05；
merge tree与已审查head tree相同，完整8项PR路径与candidate字节/mode均已核验。
merge message不含Guru trailers，没有Guru Merge gate。原Merge基于existing
Publication与authenticated live GitHub/Git事实正式记录唯一
delivery:f1a010051207b1786953c3312b4257ea1cd7480c；原Publication、Planning、Check、
full_review与readiness保持。exact同输入重入返回同delivered DTO，公共task.json
字节不变，没有再次merge。query2首次因本地remote-tracking base仍为a426a6e3返回
stale_identity/history.base_ref；正常fetch唯一远端base ref后，query2返回discovered
及同一Task/Delivery/PR563/actual merge/head事实。query1返回空列表，保持trailer-only合同。
原独立Architecture新的acceptance_finish正式返回baseline_current/no_architecture_impact；
原Completion重读whole accepted scope、全部Delivery事实、实际合入JSON、完整差额与CI，
正式记录completion:e990ed15-ff05-4d4c-ae46-42d1709daa06并返回completed。CI/reviews
仍按missing保留；本验证Task没有新增CI要求，也没有将其称为green。
本结论完成V557-01..03的公开软件链观测；不承担Source #557 Closure。

matching候选当前实核：CLI tar
5aeeb81ca72508081b7dd94ddb7a19f69444714f78b3a38858d908196cc77916，
Core tar45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967；
713/270个installed文件bytes/modes全部匹配。clean样本经固定base marketplace init，
再按官方 workflow customization使用当前local canonical候选；这不是未提交候选的
远端marketplace采用证明，也不是正式released source-lock。

旧source dogfood采用、原backend #149/PR #526恢复、业务验收、完整多平台/Release矩阵
均未由上述证据证明。验证资源Finish/归档及cleanup未执行；Source #557 的知识晋升新增
差额必须重进当前完整Check、committed Review，正式交付/Completion/Closure仍由各原
owner判断，不能由验证Task的completed或知识晋升代替。
