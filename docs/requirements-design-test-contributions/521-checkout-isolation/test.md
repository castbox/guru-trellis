# #521 验收与实际结果

状态：reviewed_promoted，定向实现与真实 native 验收已完成（2026-10-11）；晋升前正式 Check 与独立完整 Branch Review 已通过，review commit 为 `5bcee456787cfb70bb6f26956a90af696083e73d`。RDT .85 / Architecture .84 晋升差额仍须 fresh Phase2、TaskCommit 和新的独立完整 Branch Review。此文件是 #521 定向验收结果的唯一长期 owner。测试只覆盖 honest 正常路径及当前合同要求的普通冲突/外部状态变化。

| Test identity | 执行入口与观察 | 当前结果 |
| --- | --- | --- |
| T521-01 | composition 26、checkout substrate 27、create package 23 个 unittest 通过。真实 Codex start 从 primary 获取 linked/non-base，仅在 linked 编辑，公共出口 completed；primary ref/HEAD保持 | PASS：客观 runtime 与真实 native 分别成立 |
| T521-02 | native 同聊天复用 linked；fresh新聊天只读检查零创建；首次 acquisition 被 workspace-write 沙箱拒绝后 blocked且零目标写入，在同聊天可写Git环境重试成功 | PASS：沙箱失败保留，不推定任意 host 可创建资源 |
| T521-03 | Codex CLI 0.160.1真实持久会话：start、同一session普通继续、fresh新聊天明确范围后编辑、显式trellis-continue均完成；实际读取原上游Skill，无binding的no_current_task由Guru caller承接；公共completed | PASS：未增Task/activation/binding；init预存未绑定bootstrap Task仅为inventory |
| T521-04 | bind package 12 unittest（指定锁定Fork后无SKIP）包含真实Git primary/linked及official schema-2 session port、generation/stale/冲突零写；native无binding不误选bootstrap inventory | PASS：绑定冲突为客观integration证据，不冒充全部native绑定分支 |
| T521-05 | native primary带无关dirty/untracked，linked中完成多轮文档修改；独立比较primary ref/HEAD/status与相关文件字节均未变；其他候选与工作树保留 | PASS：本地修改/保留；真实push与发布未执行 |
| T521-06 | 真实双目标native产生第一项partial diff后读取第二项consumer；自动返回reselect_mode并由selector返回standard_intake，显式返回explicit_choice_required并由原execution owner接回。两者后续范围收窄均真实completed，partial/unrelated完整且零Task。补充真实GitHub-backed既有安装fixture，同一native聊天自行完成第一项后实际接续reselect_mode → standard_intake → synced → context_ready → clear → pass；原Change Request recorder首次因standalone_request/workflow mode不兼容拒绝；最小输入修订安装后，同一原会话保持原source/transition，亲自Review record/check/invoke返回ready，再由原router/create owner运行record-task-plan返回status=ready，展示clean linked、Task和独立partial承接方案 | PASS：真实扩张、收窄和standard接管到独立副作用边界；实际创建/绑定/承接未执行，客观creation/acquisition回归单列 |
| T521-07 | 一个Codex代表性clean安装、current update --create-new及reapply exit0；core为5c760463680ffc10a3f26957b330c57a4b0c3ff8 / 0.7.0-castbox.3；使用当前本地未提交Guru candidate。source/installed closure、dogfood drift及183个upstream projections通过 | PASS：local候选安装层；非远端发布、完整矩阵或业务安装 |
| T521-08 | 新Task primary adoption零写拒绝、linked adoption/provision与旧primary created-result recovery通过；sync-base 15 unittest通过；旧current-checkout仅为pinned历史、current contracts/投影一致 | PASS：定向回归；旧业务安装尚未采用 |

## 执行层与首次失败

受影响 selector 16、execution 11 测试通过；233个Python文件内存编译、44个Bash语法检查、diff检查通过。没有配置独立lint/type-check，不把compile称为静态类型检查。正式task context校验通过；四个规范超过注入长度阈值，完整文件读取fallback仍适用，本任务未修改上游注入机制。

native证据来自真实`codex exec --json`与精确session-id resume，不用`--ephemeral`或host预写owner result。首轮存在locator schema拒绝、workspace-write的Git元数据权限拒绝；后者实际公共blocked且无写入。同scope重试使用可写Git执行环境，Agent自行创建linked并编辑。克隆扩张fixture缺少ignored runtime指针时，正式invocation报runtime_not_bootstrapped，未产生typed exit/目标写入；测试安装owner通过正式preset补齐，原聊天fresh重试。首组第二项仅检查的请求并不证明真正扩张回程，保留失败/不足样本而不标通过。后续明确双目标更名测试才产生实际reselect_mode/explicit_choice_required，两组独立收窄均完成原owner回程。

标准接管的首次Sync失败源于fixture的main比克隆remote多一个setup commit。补充同基线的本地bare remote后，原Sync正式返回synced，primary ref/HEAD与partial候选内容未变；旧失败样本保留。Discovery正式返回blocked：本地remote不能提供其合同需要的真实GitHub仓库身份。Agent读取真实inventory与create合同，确认两个dirty linked不能直接adopt，clean primary也被creation-only规则排除；没有选择目标、没有acquisition/Task invocation或搬运。

随后从真实GitHub main克隆既有安装fixture，在linked应用当前candidate并同步canonical workflow。29个backup均核对为HEAD preimage后保存在repo外；reapply exit0。真实native自行写入文档label候选并返回completed，同一聊天读取剩余稳定API token后停止写入，实际公共出口依次为reselect_mode、standard_intake、synced、context_ready、clear、pass。原`guru-review-change-request/scripts/record-change-request-review.sh --root . --invocation - --json`返回exit2、`schema_mismatch`、`public_input.mode`；这是调用校验错误，不是该Skill的正式blocked出口。该源package未被#521修改：`public-standalone-request-input.schema.json`限定`mode=standalone`，而`runtime/common.py`同时要求public与真实前序transition的mode一致；本轮transition为workflow。没有改写transition、放宽schema、换用真实Issue或伪造ready以继续。

独立核对标准接管前后的34个dirty/untracked文件hash一致，首项为preview，剩余JSON仍为draft；primary仍clean main且HEAD不变，worktree仍为原两个，没有新Task、session binding或承接。该首次失败定位原Phase0 Change Request owner的no_issue workflow输入兼容前置。随后经原规划/Architecture owners复核，直接将原输入mode扩为workflow与standalone，保留schema id、source/target身份、三方mode equality、router与clean acquisition。原package 26 unittest、现有真实production producer-chain测试类9 unittest无SKIP通过；新断言首次读取错误层级导致KeyError，修正后重跑通过，不作为生产缺陷。

最新真实 native 同一会话重入读取 live installed schema/contract，原 source 与 Wording public transition 完整可取且内容一致；由模型亲自完成十维Review并实际record/check/invoke，正式ready保留workflow与standalone_request。沿原guru-task-intake-router进入guru-create-task，原只读record-task-plan实际返回status=ready（中间回执，非created）。dirty当前linked不能adopt，clean primary也被create-only规则排除；原owner选择同级github-status-migration-clean、codex/native-status-versioned-migration、main@44a8b9c1...和10-11-native-status-versioned-migration TaskRef，展示原acquisition的精确Git/Task副作用。独立承接计划仅创建目标native-boundary-note.md的preview字节并保留来源；历史draft→preview差额与base无此文件的真实状态均明确，不搬安装差额、unrelated或status JSON。没有执行创建、激活、绑定或承接。

原模型核对2339项fixture/setup快照不变（包含此次Codex-only正式preset投影移除的未选平台tracked文件）；parent独立对仍存在的31个dirty/untracked文件hash、两个worktree、目标路径/branch缺失、common-dir零Task资源/绑定和primary clean main复核。两个真实仓库的primary亦为clean main。新mode修订的dogfood和native fixture apply产生11与7个backup；全部HEAD preimage核对后repo外保留。首次同步恰逢新测试断言修正，另一个test backup核对等于前次实际应用字节后外置；最终两处reapply exit0、source/installed closure和dogfood drift通过。未选平台移除属于测试安装选择，不认领业务安装或全平台矩阵。

dogfood首次apply产生29个`.bak`，逐一核对等于对应HEAD旧字节后保存到repo外可恢复证据目录；workflow旧字节先与HEAD核对，再按README的local sample方法同步canonical。reapply后installed closure通过，conflict/sidecar均0。代表性update保留Guru管理的codex dispatch配置，产生的一个upstream配置`.new`经diff核对后保存，当前配置未被覆盖。upstream start/continue/context/hook字节前后相同；当前candidate未提交，安装不能证明不可变远端provenance。

独立规划与implementation_discovery Architecture正式出口baseline_current / reviewed_candidate，current baseline `.83`、constitution-v1；RDT current `.84`未写。此前正式Task Check blocked与首次失败保留；当前完整native接管证据已补齐，fresh Phase2 Architecture/Check结果仍由原owners独立产生，不以测试文档代填。

客观 Python/runtime/schema pass 不证明 Agent 执行、完整调用链或业务安装。native traces 必须由实际模型调用生成，既有 post_owner host预写候选/结果只能证明 serializer消费，不能作为first-write/partial-edit行为证据。无法实际接续时保留原失败、依赖owner与未交付边界。

完整多平台 Release matrix、tag/Release、业务 #120 安装及 PHX验收、生产效应均未验证，且不由此定向测试推定。晋升前独立完整 committed review 已发生；本次知识晋升后的 fresh gates 尚未发生。


## 晋升前独立 committed review 的实际结果

原 Branch Review recorder/checker/public invoke 对 `origin/main@44a8b9c1...5bcee456` 实际返回正式 `passed`，无开放 P0–P3 finding；Architecture 同阶段正式 `baseline_current / reviewed_candidate`，不以 Phase2 结果代替。独立 composition26、bind12、Review单文件22、selector16、execution11、Stage0全套10通过；create23初跑一项因缺固定Fork跳过，核对 `5c760463...` 后补跑该项通过。41变化投影字节一致、dogfood drift通过，原生轨迹直接核对及31现存路径hash/topology保留。以上结果不证明晋升后候选已通过新Check或新Branch Review，也不认领实际Task创建/承接、发布或业务采用。
