# #569 验证结果

本文件是本Task实际结果与未验证边界的唯一长期来源。下列实施验证已实际完成；不代表Phase2、独立完整committed Review、知识晋升或交付通过。

| 场景 | 需求/设计 | 当前证据与边界 |
| --- | --- | --- |
| T569-01 installed接续 | R569-01、02、09、10 / D569-01、CON569-02 | matching installed原Merge经当前AI检查完整7路径差额/Publication与真实本地two-parent merge后返回delivered；恢复副本local ref落后且缺merge对象，query2自动返回该事实。独立Architecture对代表性仓库实际评估并formal acceptance_finish；原Completion由当前AI读公开cutoff和完整scope/Delivery/evidence后正式返回completed。provider和前序gates为fixture，未将其说成native开发/远端live证明。 |
| T569-02 独立/恢复 | R569-02、08、10 / D569-01、CON569-01、02 | 真实Git组件证明完整本地对象在stale/missing base ref时不fetch。source query2恢复副本读取原public writer的字节，缺merge时scratch核验候选并返回，caller仍缺该对象。installed丢失查询stdout的consumer不读取该输出或private state，用原query身份重新调用原producer，实际得到明确新cutoff及当前两条真实public事实。 |
| T569-03 固定cutoff | R569-01、04、07、09、10 / D569-01、02、CON569-01、02 | 真实Git组件只读base一次；B1后source实际推进B2仍返回B1。installed公开query同样返回B1且caller全文件hash无差额。当前AI核对B2为无内容记账、scope与Delivery集合未变，直接消费B1，Completion返回completion:569-fixture-unrelated-b2，没有重查。另一正常恢复分支中原public writer创建并记录同Task第二Delivery，旧B1仍只有一条；当前AI明确判定须补事实，原query有界重入和输出丢失恢复后返回新cutoff/两条，原Architecture ownerfresh eligibility后原Completion返回completion:569-fixture-new-delivery-refresh。未重跑D1业务gate。source及installed query2先核验后排除真实后继，身份不符/非first-parent后继具体失败。 |
| T569-04 归属/空/混合历史 | R569-01、05、06、07 / D569-01、02 | 原6项history回归通过；新增真实Git混合schema1/2、多Delivery顺序与DeliveryKey、bookkeeping排除、完整无匹配合法空通过。public writer/query2的去重与manual事实语义原回归保持。 |
| T569-05 失败 | R569-03、05、07 / D569-01、02 | 实际本地transport不可达返回history.preparation且清理；获取后仍不完整具体失败。provider permission/network unit执行原准备逻辑，返回区分原因；PR/head与后继关系错误不伪装discovered或空数组。 |
| T569-06 隔离 | R569-03、11 / D569-01、CON569-02 | 真实Git caller和registered peer的全部文件（含Git数据、dirty work）bytes/modes不变；scratch成功/失败清理。installed恢复副本query前后全文件hash相同，HEAD/refs/Task事实保持。没有Task分支整合或业务gate重跑。 |
| T569-07 分发 | R569-08、10、11 / CON569-01、02 | matching CLI/Core tar SHA与MIGRATION-531一致，官方clean init后使用local canonical workflow及完整preset，Codex/Claude/Cursor/shared安装无冲突。source validator40 packages/124 commands通过；最终installed validator40 packages/124 commands通过且零conflict/sidecar/removal。独立source-repository matching dogfood最终drift检查证明workflow、selected native/shared投影及spec与canonical相同。四个本项临时样本最终apply/reapply全部ok/零conflict/sidecar。开发carrier普通apply按upstream_delivery_migration_required拒绝且保留旧安装；不半升级本Task。 |

工程回归：完整Merge suite首轮57项中56通过，唯一旧contract仍断言github_read；按本项真实写入修改为git_write后10项contract通过。最终完整Merge suite58项全部通过；新增fixed-cutoff组9项、source与matching installed public-query组各4项通过。产品package测试均由managed resolver运行。5个触及Python文件语法通过，最大538行；tracked/untracked共27路径文本hygiene与git diff --check通过。官方Task context validate通过，9+9引用中的大spec截断与code-ref为非阻塞提示，执行者直接读取相关正文。原manual-recovery/迁移/CI分支等组件结果不冒称实际远端操作。

首次环境/命令失败：managed runtime无pytest，采用原native unittest；首次source validator以-m调用缺module path，改用原check-skill-packages wrapper后通过。installed query首轮因样本落后源码产生.bak而停在apply；逐项检查6个备份仅为本次差额并删除后同版reapply，4项通过。普通installed目标直接跑source dogfood checker缺canonical脚本，改用含完整canonical的独立source-repository matching样本，drift通过。失败均未计为通过、未放宽验证或篡改产品scope。

native第二Delivery fixture准备首次import路径错误未mutation；修正后缺provider PATH导致只读PR核验失败，真实public记录保留planning/无Publication。检查已有Delivery与实际head后只恢复失败步骤，原writer最终记录新Publication与真实本地merge；未重复创建或伪造结果。这些是本地验证编排错误，不作为产品失败或live结果。

门禁边界：fresh独立Phase2 Architecture、原Check与后续完整committed Review由各原owner另行判断，上述测试结果不替代这些门禁。完整多平台Release矩阵、远端marketplace采用、旧安装/业务仓迁移、生产效果不属于本项证明；真实#569交付/知识晋升/收尾尚未发生。代表性仓库两次completed仅说明本次实际consumer判断与公开接续；它们不关闭Source #569，也不证明前序fixture开发gate已由native owner执行。
