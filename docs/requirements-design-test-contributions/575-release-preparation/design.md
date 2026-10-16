# #575 S2/S3：来源准备与来源校验修复设计

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
