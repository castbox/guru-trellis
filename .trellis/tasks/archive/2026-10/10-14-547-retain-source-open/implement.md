# #547 实施与交付计划

## 唯一 Delivery Policy

选择 full：本次 Delivery覆盖 PRD R547-01..08/AC1..7 和 design D547-01..05，没有隐藏后继切片或本Task剩余工作。完成条件为闭环路径、现有行为回归、匹配投影/API迁移和RDT/Architecture承接全部满足，Phase2与committed完整diff独立Review通过后正式Delivery。Completion仍在Delivery后审查whole-task。原CMS现场采用、业务联调/产品#59联合验收、完整Release矩阵是本Task范围外且明确未验证的边界，不能被本次Delivery或Finish宣称完成。#548不启动。

## 实施顺序与文件

1. 在 canonical `trellis/skills/guru-team/packages/guru-complete-task-closure/` 的 contract、runtime/invoke.py、输入/semantic schema和实例增补retain_open；identity/uniqueness后返回blocked；按所需状态执行/恢复；aggregate terminal与Task2 source projection分开。只调整真实消费新枚举的contract，不增加DTO字段或状态库。
2. 在 `guru-finish-task/` 的contract、runtime/invoke.py与closure-result-snapshot.schema.json增补OPEN条件和真正关闭动作的terminal谓词；使用现有共享reader，保持archive/bookkeeping与Cleanup行为。检查共享runtime/task_lifecycle/closure_result.py是否已经完整透传，无需修改时保留。
3. 按下表补充语义owner调用、public-wrapper与真实upstream测试。阅读现有72测试、Completion scope owner和Finish fixture后复用其正常构造器，不手工篡改artifact模拟缺陷。
4. 更新迁移支持合同、isolated RDT delta、Task Architecture贡献与ADR候选。按官方marketplace/preset机制在受控候选checkout执行apply和drift检查；检查Shared/Codex/Claude/Cursor当前声明平台，保留用户sidecar处理记录。当前工程安装仍为完整旧Task运行包，不以新Task2 writer替换它。
5. 原RDT owner执行delta reconciliation，再完成Phase2全scope检查；精确TaskCommit和首轮独立`origin/main...HEAD` Review；原Architecture owner按live expected-current正式promotion后fresh Phase2/commit/独立全diffReview；正式Delivery Review/Publish/Merge各守自身边界。后续Completion、Closure、Finish和Cleanup分别执行原owner，报告调用方资源保留事实。

任何实际实现改变本设计机制、scope或owner时，返回Author/qualification/Architecture原入口，不能在实现中静默扩张。

## 验证合同

| 场景 | 入口、观察和缺陷检测 |
| --- | --- |
| 正常scope修订并retain | 正式scope owner保持TaskId/generation/exact_source，当前scope收敛；正式Completion/Closure/Finish串联；观察completed、no_mutation ref、OPEN、无close日志、归档和bookkeeping唯一远端结果；旧代码在exact_source eligibility处失败 |
| 未完成/证据缺口 | Completion原owner读取当前scope与未满足证据，得到原remaining/evidence/revision/blocked outcome；不得产生可用completed或Finish success |
| semantic blocked | 有效identity和唯一source action，执行正式Closure blocked；原reason保留，provider无close，且无新的Closure transaction |
| 原路径回归 | close、already_closed恢复、reference_only/no_issue；保留原typed exits、required状态和provider调用数；现有72测试作为基线而非本需求证明 |
| 已支持多Issue | 源retain_open/另一Issue close；aggregate closed，源仍OPEN，Task2 no_mutation/source_result=null；源close时source_closed/CLOSED；不把另一Issue关闭误投影到源 |
| 正常stale/state变化 | 通过scope/source原owner变更或fake provider正常改变OPEN/CLOSED；Closure conflict/Finish closure_refresh_required回原owner；保持原identity/evidence检查 |
| stdout丢失 | 首次真实执行后丢弃返回输出，再通过同owner原re-entry恢复；Closure与Finish对close、archive、bookkeeping mutation计数不增加，result identity保持 |
| 新装/API consumer | 验证固定Core/CLI内容身份与matching candidate；完整managed resolver调用输入schema、语义动作、共享snapshot、public close_task/archive，检查无新输出字段或替代Task store |
| projection/reapply | 受控canonical/dogfood/installed和声明平台contract/interface/mode一致；同候选reapply、drift检查、用户改动.new/.bak按官方合同保留/处置；不对本app旧模型整套应用新writer |

测试入口使用managed resolver和现有外部pytest测试依赖；联合pytest采用`--import-mode=importlib`避免同名tests包冲突。上游固定产品commit及Core/CLI tar内容身份以`trellis/presets/guru-team/spec/workflow/task-delivery-migration.md`为准，不能用版本字符串替代。按本Issue范围执行定向source/installed检查；干净新安装证明使用一个代表性受控throwaway，不执行完整平台/Release矩阵。

## 唯一 Docs SSOT Plan

选择 `delta_first`。原writer为`guru-maintain-requirements-design-test-ssot`，isolated contribution root为`docs/requirements-design-test-contributions/547-retain-source-open/`，文件为manifest.yaml、requirements.md、design.md、test.md、traceability.md。当前Requirements/Design/Test authority为`.90/active`，继承Architecture `.87`；每次门禁重读live authority，漂移回原owner。

贡献将R547-01..08映射D547-01..05及上表场景，不复制source prose；引用#436前驱决策并保留历史界限。实现与证据齐备后原RDT owner在final Phase2之前reconciliation；不把BranchReview当首次文档补齐入口。共享current变化依照原promotion single-writer合同和live identity，不能覆盖并行current。ADR-013/024增量仅由Architecture原promotion owner转为shared决定，Planning不晋升current。

## 门禁和诚实边界

Approval只判断本规划足够，Activation另行接受当前三文档内容并由已安装guru-activate-task更新本工程Task。实现之前没有代码变化或retain_open验证结论。之后报告实现、静态、受控集成、新安装、实际旧采用/原业务恢复分别证据；缺环境记unverified，不能借72测试或fake provider声称生产已恢复。Source-design处置由design唯一矩阵拥有。授权不写入任何文件。
