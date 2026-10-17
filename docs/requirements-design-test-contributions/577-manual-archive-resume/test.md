# #577 Test：策略与实际结果

状态：本Issue定向验证完成；以下结果不表示正式Fork采用或真实业务恢复。此文件是本增量实际工程验证、联合行为和未验证边界的唯一长期记录；Task规划与Architecture只引用它。

| Identity / Source acceptance | 策略与可观察结果 | 当前结果 |
| --- | --- | --- |
| T577-01 / SCN577-01 / AC1 | 一个代表性隔离旧安装含人工旧归档、规划与历史；source-loaded维护后目标installed原生与下一真实Guru owner消费同一公共key，archive/source仍可读且current唯一。 | 通过；实际层次和未验证边界见下文。 |
| T577-02 / SCN577-02 / AC2 | 原历史owner核验实际PR/commit与归属；当前scope补差/验收由实际owner承接，旧gate不通过，无空Delivery/替代Task。 | 通过；实际层次和未验证边界见下文。 |
| T577-03 / SCN577-03 / AC3 | 定向回归正式Reactivate/合法人工Cleanup、旧活动转换、history_closeout、完整Plan2以及未完成closeout回原事务。 | 通过；实际层次和未验证边界见下文。 |
| T577-04 / SCN577-04 / AC4 | 支持入口的普通缺证据/不支持格式/歧义/stale/mismatch/依赖缺失有具体诊断；选定外资源不变，只读不依赖预修旧绑定。 | 通过；实际层次和未验证边界见下文。 |
| T577-05 / SCN577-05 / AC5 | 公共同operation重试/丢输出/前缀恢复及原controls回退；保留generation、一次历史和原写集，后续工作阻止覆盖。 | 通过；实际层次和未验证边界见下文。 |
| T577-06 / SCN577-06 / AC6 | actual source/build/API、canonical/dogfood/installed、声明平台、apply/reapply/drift/sidecar及目标native联合证据分层报告。 | 通过；实际层次和未验证边界见下文。 |

已观察依赖事实：上游PR #52的最终HEAD为 `28fcf4c611d197903b64b818fe9bd4fea7040b3e`，merge为 `7bcbeaad31380e7a29c97898cb947c6120a61775`，CI run `39043118700` success。matching CLI/Core为0.7.0-castbox.4；源码dist与安装内容一致，CLI两个Python模板模式0755→0644，故不声称严格source_locked匹配。现有正式Fork pin不改，local_candidate只证明隔离开发。


未验证且不属于本Issue交付声明：真实CMS/业务数据恢复、正式source-locked采用、软件发布、完整多平台Release矩阵。上游测试和CI不代替Guru私有owner或目标native联合验证。

## 代表性旧安装：历史检查

只在隔离副本使用 CMS PR #17 已合并快照 `9b5b03696fd66fbefd841f8309524c9d87e6f12d`，分支为 `codex/577-isolated-resume`。真实CMS没有安装、恢复或数据写入。选定原归档 `10-13-1-normal-price-promotion`，TaskId `1-normal-price-promotion/generation 0`。原manual-closeout明确保留原scope/规划和PR历史，且没有当前Closure/Finish/Cleanup/seal；源Issue保持OPEN，历史后端联调与联合验收缺口保留。

执行AI读取原Task和manual-closeout，随后通过原source-loaded Publish→Merge的 `legacy_history_verification` 两次正式invoke，均返回 `verified_legacy_history`。实际核验 PR #10/#12/#13/#16 的reviewed head、base/head branch与合并提交，且各merge是该固定快照祖先。此证据证明历史归属/合并，不证明当前业务完成。原维护已完成公共恢复和正式 finalize：`task_resumed`。目标自身 Identity、C4、C3、Bind 均正式通过；原生 task current 读取同一 active Task、generation0、PR16 delivered历史且 `no_current_delivery`。目标自身 get_context continuation 返回 Guru 当前无Delivery路由；目标 Clarify 实际返回 `scope_ready/scope_action=revised`，指向 Issue1 当前 PROMO11。未执行Author或创建新切片。


## 定向回归

产品 wrapper与最终 unittest 使用原 managed resolver：Python 3.12 venv（cache identity `f0b89dabd24ef812b1244b8b`）。lifecycle 161、Delivery projection 16、maintenance 9、Bind 13、六原owner legacy 23、完整 Plan2 原合同34项与新增dirty来源3项均通过。source package验证40 packages/124 commands、ownership22 descriptors/43 claims/22 overlays和 diff --check通过。Reactivate25项由独立工程解释器 Python3.12/pytest8.3.5通过；该工程测试环境不是产品runtime fallback。

真实CLI/Core回归含 packed维护6项，首次C4绑定、保留同ID归档后current唯一、真实active占用冲突、同operation丢输出/前缀恢复/rollback和后续工作保护。生命周期旧错误文案断言因官方resolver更早给出 `current_task_checkout_unresolved` 而失败；修正断言后全161通过。两项installed测试最初硬编码core.3，真实pair.4被正确拒绝；fixture改读选定包实际version后16项通过，产品version/capability gate未放宽。

完整 Plan2真实旧安装20项因缺 `GURU_UPSTREAM_LEGACY_CLI` / `GURU_UPSTREAM_DELIVERY_CLI` 记为SKIP。本Issue未修改Plan2转换行为，不将原合同34项通过表述为20项安装矩阵通过。本次代表样本覆盖tools-only安装及archive-resume，完整矩阵由专门owner承担。

## 同一隔离样本：工具与数据

原tools owner实际安装matching pair与三平台投影，正式返回 `tools_upgraded`，`unverified=[formal_fork_source_lock]`。安装前后34个原Task/归档文件bytes/modes全部一致；无workspace journal文件。原archive恢复operation为 `a9355dfd-e141-47fe-b10c-e31293e1a509`；恢复目录沿原active locator，同一TaskId/generation0，不修改原archive。

PR16历史Delivery只导入已核验的reviewed head与真实merge结果；原commit是受审head，按source_snapshot保留，不冒充merge。原completedAt只保留source_snapshot。PR10/12/13及全部原始规划仍在原archive；当前Completion/Closure及所有历史gate slots为空。原归档没有可迁移旧session或Guru私有controls，不制造空owner；C4将样本分支登记为caller-owned，Bind为样本session重新绑定，不称其为旧指针恢复。

当前source变化是CMS Issue1 PROMO11明确移除映射编辑及新版要求、保留既有数据；原PROMO8规划仍要求映射。目标Clarify根据实际源修订判定当前scope补差。恢复结果只证明工具、数据、历史、native/session及下一owner可用；未证明CMS业务、真实服务联调或产品#59联合验收完成。

## Dogfood 首个失败与修复边界

普通preset apply按旧归档预检在写前停止。转原tools owner预检时，既有receipt记录dirty来源与core.4；其provenance commit的manifest为core.3。39个缺历史hash的实际工具文件与原commit canonical bytes全部一致，但原owner在逐路径核验前按整体metadata拒绝，尚未prepare写入。首个失败位于原历史来源筛选，尚未进入目标写入；修复与相同输入重跑分别观察。限定在原owner恢复已记录dirty provenance commit的逐路径候选资格；不改receipt、正式pin、source_locked或Task数据，未知preimage仍由显式preserve/replace处理。原owner最小修复与3项managed真实Git回归通过：dirty原commit提供逐路径bytes且不使用后续HEAD；clean metadata不匹配和缺原对象仍阻塞。同一dogfood原preview→prepare已成功，固定dogfood tools操作已成功；真实原owner工具写入和分发结果见下节。

原恢复finalize与同operation丢输出resume均正式返回相同 `task_resumed`。恢复后重新比较原34个文件bytes/modes，差异0；当前一项PR16历史、所有gate=null、Completion/Closure=[]，没有当前Delivery。


## 最终分发与工具恢复结果

Dogfood 原tools operation `7d3ec616-96df-43a9-a1d6-1f321d202edb` 正式返回 `tools_upgraded`；同operation resume恢复相同结果。原installer实际同步package/runtime/spec，installed checker通过40 active packages/124 commands、Claude/Codex/Cursor与shared投影；conflict/sidecar/removal均0。workflow/spec canonical parity和dogfood drift通过。2609个既有Task/archive/public-session/private-control文件bytes/modes不变；305个peer/common Python pointer保持。只新增本工具操作public recovery和计划内checkout-local managed Python pointer。

同一CMS隔离样本用新operation `06bb86ae-406b-4c1f-9fd8-7198cfcc4fde` 经原tools owner重应用最终canonical；公共212项均零内容变化，config/.gitignore/AGENTS保留。实际返回 `tools_upgraded`，同operation resume返回相同结果。installed40/124、三平台和target managed resolver通过；无conflict/sidecar/removal。60个既有data/control/customization文件bytes/modes不变。最终目标native continuation exit0；Delivery current仍为同TaskId/generation0的 `no_current_delivery`，schema3 session身份保持。源package checker、dogfood drift和diff --check再次通过。

普通 `apply.sh` 对dogfood与样本仍在原whole-inventory前置因旧归档停止，未绕过预检。实际reapply由原tools owner调用既有 `install_assets/tools_maintenance` 完成，不是手工拷贝，也不声称普通apply已能解析全部旧归档。canonical与实际installed受管投影一致，官方template hash/用户编辑和sidecar语义保持；没有执行官方update完整矩阵。

语法检查：当前20个canonical Python模块AST/内存compile、32个JSON parse、相关bash -n、diff --check通过；触及非生成源码均不超过3000行。仓库无适用的专用ruff/mypy/TypeScript等lint/typecheck配置，不把语法检查称为独立类型检查。

两处工具操作均明确 `unverified=[formal_fork_source_lock]`。正式pin、source_locked mode校验、全局CLI和node_modules未修改。真实CMS恢复、正式Fork采用、软件发布、完整官方update及多平台Release矩阵均未验证，分别保留原业务/来源/发布owner边界；这些不属于本Issueaccepted交付范围。
