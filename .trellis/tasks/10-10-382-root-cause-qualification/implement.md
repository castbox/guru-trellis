# #382 实施与验证计划

## 顺序与边界

本task处于Planning；正式approved之后展示三份文档并等待当前方案acceptance，随后由 `guru-activate-task` 写状态进入Phase 2。此文件描述后续工作，不是任何副作用的授权。

每次task/source写之前通过 `check-task-checkout-boundary.sh --json --task .trellis/tasks/10-10-382-root-cause-qualification`；源头为本dedicated branch的canonical，保护其它checkout和无关dirty。Git commit/push/PR/merge及shared-authority promotion分别遵守现有workflow边界。任务内只交付#382，后继#383/#468不启动。

## 实施切片

| 顺序 | 内容 | 出口与依赖 |
| --- | --- | --- |
| I1 | 对照官方workflow/marketplace文档，fresh inventory current registry/profile/router/manifest/runtime与installed selection；形成RDT contribution requirement/design/test trace。 | 确认新增包与实际consumer，不改历史authority；发现实质设计变化回Planning/Architecture。 |
| I2 | canonical新增guru-qualify-root-cause semantic package，input分profile、output分exit、最小consumer maps、process-local semantic-result schema与wrapper。 | diagnosis目标未知根因可classified继续；root-fix不足diagnosis_required；symptom只机制修订。 |
| I3 | deterministic runtime闭合schema/identity/freshness/candidate coverage/aggregation/projection；无语义推断、无资格输出path或持久化。 | 真实wrapper分别执行四出口及普通stale，检查no-residue。 |
| I4 | 将root调用接到现有candidate callers和workflow显式marker/routers，保留normal→solution→root职责；阶段复用与实质变化条件写step-local。 | 全graph唯一consumer；不存在root对前两owner递归、重复completion或scope-confirmation误路由。 |
| I5 | 更新current registry/interface/manifests/spec/data/quality/usage与README；canonical preset/apply分发shared及exact selected native roots。 | 保持现有两qualification已发布API；新contract用新versioned assets；legacy immutable字节不变。 |
| I6 | focused native semantic eval与runtime/projection/安装验证；完成task RDT/Architecture contribution、独立review及owner promotion。 | 未具备真实环境不记pass；promotion-created diff重新正式Check/commit/完整独立Branch Review。 |
| I7 | 当前完整Phase 2 Architecture/check、Task Commit、独立完整Branch Review，随后Delivery review/readiness。 | 只形成concrete可审交付；任何publish/merge/closure/cleanup沿独立授权边界。 |

## 验证计划与证据层级

| Gate | 实际入口与观察 | 能检出的缺陷 | 证明边界 |
| --- | --- | --- | --- |
| V1 package/runtime | 新包真实invoke.sh、dispatcher与schema validators；四出口、七classification和profile/consumer映射 | 缺分类、错误诊断继续、nonpass折blocked、错误projection/consumer、普通stale继续 | 只证明确定性合同，不证明语义判断。 |
| V2 semantic eval | 当前native Adapter执行AI，输入真实事实/locators；expected结果留grader侧 | C01..C13中症状抑制误通过、未知诊断准入循环、合法缓解/保护误拒、framing影响 | 报actual native argv/context/output/trace；缺native execution记unsupported/blocked。 |
| V3 reuse | 实际caller完整新候选调用后进入下一stage；分别提供不变机制与实质变化机制 | caller变化重复同一资格、旧结论覆盖当前stage审查、变化机制未回owner | 当前stage资格承接，不证明#383完成声明新合同。 |
| V4 residue | 调用前后git status及ignored qualification namespace实际inventory | normal invoke遗留tracked/ignored artifact、checkpoint或输出文件 | 不把repo外eval报告或既有stage gate当资格residue。 |
| V5 distribution | canonical/installed/shared/exact selected native平台真实discovery和wrapper；registry/manifest graph checker | 新Skill缺分发、platform旧流程、marker未知出口/多consumer | dogfood selection与complete upstream inventory分开报告。 |
| V6 install/update | 一个clean throwaway安装workflow marketplace/preset；current manifest update、Trellis update后preset reapply；drift与递归sidecar检查 | 新装不可发现/调用、update丢失、reapply回退、未处理.new/.bak | 一个代表性当前版本链路；不证明完整多平台/旧版本Release矩阵。 |
| V7 business dogfood | 只读#354/#355/#357与可用实际代码/证据，native Agent回放真实候选并观测classification/route | 通用eval与真实业务first failure、mitigation、retry/fallback事实脱节 | 只证明资格判断；业务生产效果未验证。实际业务checkout若需写入，先展示精确范围再请求授权。 |
| V8 quality/docs | 当前task accepted scope完整AI Check；git diff --check；docs link/trace与真实consumer inventory | 文档漂移、无consumer字段、过宽scope、缺验证边界 | 不以字符串计数或coverage flags冒充semantic pass。 |

禁止测试自证明：不把implementation复制进expected，不只assert固定文案，不把当前配置值冻成业务硬范围，不以相同病例重复计数增加充分性。C01..C13采用事实反例/正例比较，V1..V8各证明独立缺陷。

## Docs SSOT Plan

策略 `ssot_first`。先在 `docs/requirements-design-test-contributions/382-root-cause-qualification/` 写 requirements.md、design.md、test.md与traceability.md；Test文件拥有实际验证结果唯一来源。Planning的Architecture候选保留在task-owned `architecture-contribution.md` 与 `architecture-adr-candidate.md`，独立owner判断后由后续实现贡献承接，shared accepted ADR只在原owner晋升时写。三个current入口通过各owner晋升，不在Planning直接写shared current。

准入唯一正文在新package `references/contract.md`；`.trellis/spec/workflow/skill-package-contract.md` 管package/public I/O规则；`data-contracts.md` 管确定性传输；RDT/Architecture usage引用owner边界；quality指南定义验证价值/范围；三份README只描述真实用户入口。canonical spec源位于 `trellis/presets/guru-team/spec/`，dogfood由apply同步，不能只改运行副本。

#383拥有 `causal-completion-semantics.md` 与完成判断；当前不存在时只用design指定最小qualification/completion边界，不造替代文件、stub或adapter。文件出现后的共同引用由其owner承接。

## 完整Delivery policy

task_scope与delivery_slice均为R382-01..09，remaining_work为空。完整交付须具备可执行新资格链、目标感知真实native证据、正确跨阶段消费、零residue和所声明安装/分发证据。业务repo native或外部环境不可用时保留明确证据缺口，Delivery Review沿其当前planning_revision_required / implementation_required / blocked出口处理，后续Completion在自身入口按当前合同判断evidence_pending；不宣称完成全部验收。#383/#468不是本task剩余工作；完整Release矩阵属专门owner，生产效果属业务owner。

## 风险与恢复

主要风险是root-fix证据门槛误套诊断/缓解、过大的public witness、资格复用变成持久缓存、#383边界重复及平台caller漏接。各风险分别由C08..C12、consumer字段审查、V3/V4、owner graph和V5捕获。正常schema遗漏或stale按同owner重入修正；真实workflow defect记录实际错误并走typed route，不伪造pass。任何改变accepted目标或authority的发现返回原Clarification/Planning；同scope机制remove/replace自动重审，无例行确认。
