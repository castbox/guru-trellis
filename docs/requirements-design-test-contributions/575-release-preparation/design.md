# #575 S2/S3/S4/S5：来源、工具采用与完整准备设计

行为由 requirements.md 单写，实际结果由 test.md 单写。本设计继承 [S1](../575-source-adoption/design.md) 与 Architecture `.93/active`，不复制或改名历史证明。

## D575-S2-01 / CON575-S2-01：版本消费者与公开来源

canonical extension manifest 与原 maintenance owner 的 TARGET_GURU 推进 `.4`，生产 upgraded() 复用该 target；schema/example、tools example、两个 stop consumers 与目标 fixture 同步。TARGET_CORE、合法旧族、真实 predecessor、formal source 的 HEAD/clean/manifest 检查、Plan2/resume/rollback 保持；preset resume 仅补齐实际使用 sys 的模块 import。生产结果进入 manifest/schema 的实际消费测试避免常量自证。

当前 source README、workflow/preset README 和 public-docs spec 映射 `.4` 未发布、CLI/Core `0.7.0-castbox.3`、Fork `2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0`；真实 stable `.3` 仍使用自身 immutable tag/旧锁。试用未发布源码要求同一个真实可寻址完整 SHA，不预造未来 tag/SHA。

## D575-S2-02 / CON575-S2-02：基础图与所有权

public tools 拥有 upstream native/scripts/templates/receipt/.version；Guru installer 拥有 runtime/packages/registry/consumer/Shared/平台 overlay，workflow 仍走 marketplace。S2 审查 M 已采用的 `.3` 图及其全部受管差额，核实自身 receipt、固定 Fork native、workflow/平台入口、权限与 config/Task/session/common/peer 保持；generated 身份不能免于 Review。

canonical `.4` 与 installed `.3` 的版本差额明确由 S3 原 tools-only owner 消除。S2 不手抄 `.4` 生成副本、不普通 apply 绕过旧归档 guard、不转换无关归档。当前 `.3` 结构与 receipt 通过不证明最终 `.4` parity。私有 release Skill 不进入公共 inventory。

## D575-S2-03 / CON575-S2-03：先来源再正式消费

S2 先完成来源/模块和当前基础图验证、Check/TaskCommit/独立完整 Review，再产生可消费的真实 clean committed `.4` source。内容基线 B 与 PR target main 分离，来源不通过虚构提交或放宽原 source 检查取得。

后续完整安装 Delivery 从实际已提交修复 source 建立新的 `.4` tools-only operation，不重用 M 的 `.3` operation/备份；原 selected-task/public/private owners 各写其资产。四平台最终 parity、三平台 reapply/drift/权限/sidecar/退休资产、一个 Codex clean/local-workflow 和真实 stable `.3` predecessor 样本均在后续完整安装 Delivery 执行。目标自身 native/managed runtime、下一真实 owner、固定 identity 的同操作 resume 与不兼容单侧 tools rollback 是正式证明；fixture/外部 source runtime 不替代。Task/history/config 保持，旧 gate 不变成当前 pass；generic verifier 不匹配回原 owner。

## D575-S2-04 / CON575-S2-04：增量文档与整体完成

当前贡献保持 draft，S2 final Phase2 前 reconcile 当前来源责任和 S3 待办，不更改 shared current。后续完整安装 Delivery 补齐完整准备证据后，在首次完整 committed Review 之后由原 owner fresh expected-current 晋升；晋升差额重新 Check/TaskCommit/独立完整 Review。无 Architecture impact 不制造 ADR/contribution。

S2 仅 Refs #575；实际交付后由 Whole Completion/Creation 建立真实 S3 key，本文不预建未来 Delivery。全部准备责任完成才可 Closure no_mutation 与 Finish/bookkeeping。正式 Release Stage 2 从最终 main exact candidate 重跑全部适用发布证明，不从本地来源/安装样本推断发布成功。

## D575-S3-01 / CON575-S3-01：source-only 读取边界

在原 `_validate_repository` 内将 installed manifest 的 `read_json` 置于既有 `validate_installed` 条件内。False 不读取该 target 事实，canonical schema/inventory/extension/registry 校验保留；True 读取与错误收集、后续 installed 校验保持原样。直接修正唯一 validator，不新增 manifest writer、分支入口、fallback、API、状态或恢复框架。

原 tools-only rebuild 正常退休旧 manifest 后，preset 的 `run_upstream_ownership_validator` 以 False 校验同 checkout 的 canonical source。定向回归在等价正常样本同时观察该真实 wrapper 与 validator：原失败阶段、错误、source-only 结果及 default/True 对照分别判断，不能将另一阶段失败或总通过数当作完整安装成功。实际结果由 T575-S3-01 单写。

## D575-S3-02 / CON575-S3-02：修复来源先交付

继承 RDT `.101` 和 Architecture `.94`；当前无 Architecture impact，不新增 ADR 或共享 authority。现有 #578/#579 交付及终态归档保留来源，原 owner 各自独立判断工程事实的真实依赖与适用性，不读取他人 private checkpoint 或继承 pass/token。

原 tools 操作只由原 owner 在不变 source 下处理完毕；修复会改变 canonical token，不能用其恢复引用消费新 source。当前 S3 独立交付 code/回归/draft delta，经原 Check、TaskCommit、完整 committed Review 与 Refs-only 交付形成 source。原 Whole Completion 保留所有剩余安装义务，原 Creation 建立后续 Delivery，原 tools owner 从 clean committed 修复源预览/准备新的 source_locked 操作。

D575-S2-03/04 的完整投影、A/B 对象、真实 stable predecessor、目标 native/下一 owner、恢复/兼容回退和保留责任继续有效，由后续完整安装 Delivery 承接。当前贡献保持 draft；最终 reconciliation/promotion 及前后 fresh gates 留到证据完整的后继切片。Stage2 对最终 main candidate 重跑，不以当前 source 修复替代发布门禁。

## 工具采用、平台证据与正常捕获修复增量

### D575-S4-01 / CON575-S4-01：原 owners 的完整工具采用

复用 ADR-027 的单 checkout 工具维护分工。新 source_locked 操作只消费实际 clean committed 修复源；原 public maintenance 写其工具/workflow，原 Guru installer 临时退休精确旧受管资产、完整重装并生成 manifest，本 checkout managed Python override 与 peer/common 默认分开。旧已回滚 operation 不切换 source 或重新作为恢复。所有写集/保留项由本次原owner现场prepare并审查，历史数量不成为新操作授权。

当前Task2/session3、五规划与Delivery历史、raw source、未选archives和配置保留。目标自身resolver/installed validator/native/current与实际下一owner分别观察，不以source launcher或静态DTO替代。无新公共API、owner、状态、兼容reader或恢复框架。

### D575-S4-02 / CON575-S4-02：分离验证对象与层次

A含合法旧archives，保留普通current-only guard而使用tools-only。B为相同实际Guru/Fork来源、无旧archives的隔离样本，执行三平台apply/reapply/drift；四投影source graph和私有release Skill四份bytes独立验证。focused Codex clean/local-workflow只声明本地/隔离来源链，Stage2远端最终provider仍重新验证。

### D575-S4-03 / CON575-S4-03：真实 predecessor 联合维护

从真实stable `.3`及其原正式锁/构建创建正常旧活动Task样本。原tools owner先只更新工具，目标native对旧Task返回原maintenance诊断；原selected-task owner执行所选对象维护，再由目标自身native与下一consumer证明身份、规划/历史/配置保留和继续运行。原operation的正常resume与不兼容单侧toolsrollback分别观察，不伪造recovery、digest或状态、不添加故障注入。generic existing的update/workflow/apply链不作为联合证明；有前置gap先由原owner处理，不静默SKIP或放宽guard。

### D575-S4-04 / CON575-S4-04：当前独立交付与剩余准备

当前五文件draft在本切片final Phase2前reconcile；工具/平台证据与可独立消费的source helper修复经完整当前Check/TaskCommit/committed独立Review交付。WholeCompletion保留完整clean样本、真实predecessor最终证据适用性与完整最终RDT责任，仅其additional_delivery_required经原Creation建立后继，不预造key或把根验收删减。

完整准备候选首次committedReview后，原owners以现场expected-current串行晋升，晋升差额fresh Check/TaskCommit/完整Review。当前不提前晋升shared；无Architecture impact不制造贡献/ADR。Refs-only、reference-onlyClosure/Finish和软件Stage2保持独立。

### D575-S4-05 / CON575-S4-05：verifier捕获边界修复

在原matrix `_run` 中分别捕获stdout/stderr，各自strict UTF8解码；capture给Git/version/JSON直接消费者stdout数据，log/MatrixError保留完整双流诊断、实际returncode与timeout124分类/残留事实。不改CLI/警告/参数、超时预算或source检查，不增加API/owner/state/恢复框架，不以两流合并字节作为文本。

本helper和定向tests不进入安装managed projections；A4096工具/runtime和B平台事实按bytes/参数/依赖逐项判适用，保留实际来源，不改称新HEAD已安装。完整trellis source token仍随helper变化，因此新source不恢复旧operation。定向真实子进程success/nonzero/timeout和同Fork init分别检测数据/诊断/退出及原失败阶段；完整focused留待包含修复的真实clean committed source，dirty或fixture自建提交不作正式源。


## 完整 clean 与最终准备收敛增量

### D575-S5-01 / CON575-S5-01：真实来源的完整 focused

在仓库外取得包含修复的真实提交07884d05d746d398c290cd834a9a03192a0e7205的干净checkout，保留该Git身份和正式origin；不把verifier自建的fixture提交当成formal source。正式Fork2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0与匹配CLI/Core0.7.0-castbox.3由原source lock/validator消费。

复用原verify-throwaway-install.sh的focused/Codex，workflow provider固定同真实07884完整SHA、关闭local-sample，preset来源也为该HEAD；单次PATH选择原支持CPython3.12.8 seed，锁/阶段/预算保持，指定全新外部work directory保留样本/日志。现有direct分支让CLI按初始Guru contract生成Task，preset guard不变；不删除/转换bootstrap或修改代码。原profile执行init/preset、两轮update --skip-all/workflow preview与apply/preset reapply、source lock/template hashes/Docs保留/sidecar/版本、来源复核、native platform load与session binding；全部阶段及最终退出实际满足才证明完整cell。已交付helper分流捕获，警告、真实exit和timeout124保留，不修改预算、样本或过滤输出。新失败先保留再走原qualification/诊断，不用后阶段成功覆盖首失败。原local-sample/native-init首失败保留，不宣称修复；本准备source的direct远端结果不充当Stage2最终main candidate gate。

### D575-S5-02 / CON575-S5-02：依赖感知终审

先确定根A575-01..05完整定向检查集，再逐项核原工具/平台/predecessor来源、当前bytes/定义、输入/工具链/参数/期望及raw结果。未变且可核实事实注明实际执行来源采用；缺失、变化或无法判断补受影响检查。当前AI语义独立执行，不继承旧pass或跨owner private checkpoint。

predecessor保留真实stable tag/旧正式Fork构建、原tools与selected-task分离维护、Task/五规划/历史/config、目标自身native及下一实际consumer、同operation恢复和不兼容单侧tools rollback阻塞。旧build来源不足与后续完整来源补核分别记录；source4096安装不改称07884，改变source不恢复旧冻结operation。原73suite两计数FAIL和Bhelper对照只保持其因果层证据，不扩大为历史checkout全suite结论或新增断言维护义务。

### D575-S5-03 / CON575-S5-03：唯一贡献与最终晋升

当前根requirement/design/Test/trace由原RDT owner在本五文件delta_first收敛，最终Phase2前reconcile draft；S1独立已晋升source-adoption贡献与历史版本保持。第一次完整committed Review零开放finding后，原owners以写前expected-current串行晋升；Architecture无impact不制造贡献/ADR。实际shared差额回到fresh Phase2、TaskCommit与不同reviewer完整Review，post-promotion结果才进入publication/readiness。

本机制只有原owners与直接consumer，不新增状态、authority或恢复框架。Refs-only交付后WholeCompletion判断全部根义务；只有completed才进入reference_only Closure/no_mutation与Finish/bookkeeping。软件Stage2独立，不从准备样本、RDT晋升或PR合并推断发布/业务/生产效果。
