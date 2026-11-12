# #811 资格确认 context 接续迁移

本合同适用于 normal 和 solution 两种 scope_confirmation_required 的真实context获取、刷新与原caller返回。
原Skill/exit ID保持，三qualifier的分类语义不变。Markdown拥有判断和路由，runtime只执行当前事实校验与薄投影。
具体step-local行为分别由五个原package的SKILL.md/references/contract.md拥有，本文件只拥有版本采用与退出边界。

## 1. Current支持集合

| 边界 | 原公开版本 | 当前版本 |
| --- | --- | --- |
| normal/solution scope_confirmation_required output | 2.0 | 3.0；Task-bound携task_ref/delivery_key，非Task不携；其余output不变 |
| Clarify 两确认 input | 1.0 | 各自2.0；input delivery-index aggregate3.0 |
| Clarify确认私有owner | 原普通3.0 | requirements-clarification-confirmation-5.0.schema.json；普通3.0保持，旧active4.0仍为pinned边界 |
| Clarify needs_context / refresh_context | 3.0 / 2.0 | 4.0 / 3.0 |
| Clarify确认 clear | 原generic4.0 | 两个独立confirmation clear1.0；clear delivery-index aggregate3.0；generic4.0保原分支 |
| Discovery context_request / input aggregate | 2.0 / 4.0 | 3.0 / 5.0；原pre_task4.0保持 |
| Discovery context_ready / shared context-current | 5.0 / 3.0 | 6.0 / 4.0 |
| Sync确认refresh read input | 无 | public-confirmation-refresh-read-input-1.0.schema.json |
| Sync deterministic envelope / baseline_ready | 原envelope1.0 / output1.0 | envelope2.0路径 / output2.0；envelope字段schema_version仍1.0 |
| clear router consumer | 原selected consumer | stage0/clarify-requirements-clear-3.0.schema.json，封闭generic与两确认分支 |
| 普通Interface | 1.8 | Clarify/Discovery/Sync选择1.10；两qualifier未用新metadata时保1.8；1.9仍仅Codex instruction-only |
| registry / production manifest | 1.4 / 5.0 | registry1.5、manifest6.0和production-current-6.0.json；current alias及extension public_api切匹配引用 |
| ordinary eval receipt | run2.0 | run5.0只增加普通Interface1.10支持；ordinary runner/receipt reader切5；qualification专用run3/4保持 |

原已发布schema/example的path、id和字节保留为验证资产。Current Interface、runtime selector、新示例、共享consumer、projection、
workflow routing reference和声明平台投影成套切换。Current不双读旧确认形状，不给旧结果补字段冒充新出口。
原四类context返回保各自current或pinned-old支持边界；本迁移不恢复退休active Task-status Clarify入口。
没有Task/Delivery数据格式迁移、第二状态机、qualification store或授权持久化。

## 2. 当前返回合同

真实normal/solution qualifier输出3.0进入对应Clarify确认input2.0。Task-bound对象保原task_ref、完整DeliveryKey、
candidates、target、mode、continuation和resume consumer；非Task是独立合法分支，不能从inventory猜对象。
Task target与当前Task.source指向的Issue authority分开；合法no_issue沿原accepted_scope/draft/source读取，不发明Issue。
no_issue的accepted_scope locator用于实际authority定位；原draft producer的live identity仍按原body identity合同生成。
context transition和authority snapshot分别承接正式authority locator，不用它替换旧draft live identity。

缺失或正常过期context经原Sync真实read base_current和Clarify正式needs_context进入Discovery context_request3.0。
Discovery正式context_ready6.0保确认对象，并公开原duplicate_search的最小authority_duplicate_snapshot。
该snapshot绑定真实Issue/draft authority，供Clarify原AI disposition与action校验；不能把Task当snapshot target，不能跨读private结果。
缺失或stale snapshot回原producer，不在Clarify重复Discovery搜索。

原source_actions中的真实Issue comment/body mutation仍返回refresh_context。新输出保return_identity，交Sync专用read输入：
source_exit=refresh_context、route=repo_change、operation=read、base_ref=原选定commit。Sync实际baseline_ready进入
Discovery context_request，保持原identity，不退回pre_task/stage0-current。旧snapshot不经Sync运输。
Discovery重读已变authority并生成新context/snapshot；Clarify核已生效选择，不重复mutation，再正式clear回原caller。
普通Sync read仍为pre_task/stage0-current；实际sync的clean/fetch/ff-only合同保持。

### 2.1 Consumer自有输入与AI补写

普通Interface1.10保留普通执行职责，并声明context-current4、consumer自有call-local输入和
profile-selected authoring seed。Interface1.8和instruction-only1.9的原字节保持。

Sync的 `public_contracts.invocation.call_local.public_input` 声明本包的 `{schema,example}`，
schema选择 `schemas/public-input-current-2.0.schema.json` aggregate。
Clarify refresh的consumer合同使用 `kind=skill_call_local_input`、目标interface_path和
`input_kind=structured_json`。原discovery从目标Interface读取其声明，不让producer另指定schema。
Sync普通scalar CLI继续支持原标量输入；确认return_identity只由结构化call-local入口承接。
普通调用保原public_input envelope或bare public object、字段默认及原诊断；新确认envelope校验
不得收紧这些既有普通调用。携return_identity的确认分支使用当前封闭envelope及专用read输入。

Sync baseline_ready保 `kind=skill_input_authoring_seed`，以
`profile_selector={source:producer_output,field:handoff_profile}` 唯一选中 `authoring_profiles`：

| profile_id | 从真实输出投影的seed | 原AI补写 |
| --- | --- | --- |
| pre_task | source_exit、profile、mode、continuation_id | change_input、clarify_profile；reviewed-plan alternate另保source_locators |
| context_request | 前四字段及真实return_identity | change_input |

原synced固定pre_task的seed/alternate保持。seed和AI字段不交叠，完整输入由Discovery schema校验。
缺失、未知或重复profile不得改选；普通pre_task不制造return_identity，确认identity不由AI重建。
base_current transition仍独立承接。Sync不判断检索线索、scope或source selection。

### 2.2 直接读取者切换

matching source同时迁移registry、extension public_api、production current alias、runtime discovery/validate、
installed公开投影、installer shared schema inventory，以及ordinary eval runner和直接receipt消费者。
原discovery解析目标call-local声明，validator校唯一profile和seed/AI字段关系；installed公开投影包含
call-local示例及authoring_profiles/alternate示例。原graph/projection tests执行字段补写和consumer输入校验。
不新增独立resolver、任意schema通道、投影表达式或业务状态。

已发布registry1.4、manifest5、run2/3/4及其他旧schema/example保原字节。
extension的 `skill_evals.run_schema_ids` 保原发布schema资产目录并新增run5；该目录不选择ordinary执行或reader。
ordinary当前运行/receipt消费绑定run5，保留旧schema资产目录不产生run2双读。
仅有固定旧schema不代表current reader已采用新合同；新package与旧reader混装保原版本诊断。
不能删除descriptor、把context4标成3或补造producer字段取得通过。

正式出口必须来自各原public invoke。record/check只证明其声明事实和结构，不替代语义判断、context_ready或clear。
Caller仍负责当前stage和受影响资格刷新；需要改变Task accepted_scope时走原whole-scope writer/acceptance及Delivery rework。

## 3. 待调用输入与在途操作

- 尚未调用的旧确认输入由原caller从真实已知对象重新装配；缺失身份回原Identity/Ensure/Bind/Selection，不从目录盘点选Task或Delivery。
- 丢失context或snapshot从原producer重取；不能改旧transition的target/continuation，也不能复制示例制造匹配。
- 已完成事实保持原含义；结论只按原applicability采用，不改写成当前阶段pass。
- 原完整旧provider中已开始的operation，用同一固定完整provider、原输入和原recovery ref恢复。
  不把旧owner私有状态转成新DTO，不重复已经执行的Issue mutation。
- 新调用采用完整matching current图。旧调用或操作未完成时，先由其原owner处置实际重叠，再更换涉及的工具写集。

## 4. 完整采用

已有checkout仅更新tools/workflow/Skills时使用原 `guru-upgrade-tools` 完整源合同，保Task/session；
需要完整安装迁移时仍由原 `guru-upgrade-installation` 选择其实际支持profile。
普通apply的旧Task inventory诊断不授权转换历史或手工覆盖受管副本。

采用source必须是实际选定的完整Guru source及其匹配CLI/Core来源。Preview/prepare取得精确目标、source ref、平台、
工具/workflow写删集与冲突，由该原owner审查并展示具体动作后执行。用户授权仅存在于当前对话，不进入计划、checkpoint或DTO。
本地local_candidate保formal_fork_source_lock未验证边界，不能因版本号相同而宣称正式配对来源通过。

Installer沿既有MANAGED_SOURCE_PATHS将本文件安装到 `.trellis/guru-team/MIGRATION-811.md`。
Matching采用同时覆盖workflow、routing reference、packages/runtime/shared consumers、实际命中的managed spec及平台投影。
同时采用本迁移的registry/manifest/shared schemas、公开authoring示例和ordinary receipt readers；
更新单个package或Interface白名单不构成完整采用。
Codex沿共享 `.agents/skills/`，其余平台沿实际descriptor和精确platform selection；不创建旧Guru专属路径。
只更新marketplace workflow或源码不能证明完整preset已采用。

## 5. 目标验证与普通恢复

原tools owner核目标自己的resolver、installed package/consumer/graph、实际native入口、mode、投影和sidecar。
Canonical/dogfood drift检查以及目标实际public chain分别报告；源runtime执行不证明目标可执行。
保Task/generation/Delivery、用户业务dirty、peer tools和common/peer pointers；工具更新不选择、激活或完成Task。
实际 `.new`/`.bak` 由其原owner逐个处置，未解决冲突不报告采用成功。

普通tools部分操作用同operation/ref/frozen plan恢复，不重新prepare、不改checkpoint、不刷新backup。
Rollback使用原owner审查的精确原preimage与public compatibility检查；保后来业务工作，不reset Git或回退Task数据。
工具恢复成功不证明业务接续成功；业务须回原caller实际执行同对象context循环。

## 6. 验证边界与退出

必要定向回归实际运行两个qualifier、Sync/Discovery/Clarify producers及原caller消费；fixture只建立声明boundary前状态，
不能预填这些producer应生成的输出或snapshot。覆盖当前/缺失/普通stale、mutation刷新、原四类及合法no_issue/非Task分支。
受控gh替身证明其测试边界，真实Agent与原Task/Delivery外部接续单独观察。
共享metadata定向回归实际解析context4和Sync自有call-local schema；从真实baseline_ready选择两类seed，
补AI字段后验证Discovery输入，reviewed-plan保source_locators。ordinary eval smoke须执行一个1.10包的原wrapper，
并由run5 schema/reader消费实际receipt；只检查版本字符串不能替代这些行为。

本迁移的源码、公共链、安装、真实业务接续和Release矩阵各自只建立实际证据层。
普通Issue不扩为完整多平台Throwaway/upgrade/update/Release矩阵；未执行的层保持未验证。
Shared RDT/Architecture由原maintenance owners在实施与工程事实齐全后提交前final_integration整合/readback，
随后TaskCommit和一次独立committed Review审核真实after。安装或结构通过不建立semantic pass、reviewed_promoted或Task完成。
