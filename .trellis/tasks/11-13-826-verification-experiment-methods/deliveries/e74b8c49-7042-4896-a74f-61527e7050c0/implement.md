# D1 实施与验证计划

## 1. 输入与引用

整体 .trellis/tasks/11-13-826-verification-experiment-methods/prd.md、本批prd.md与design.md第3节承接#826；设计第4/8节定义具体方法与验证。实际加载quality-guidelines Test And Validation Value、review-sufficiency、current-knowledge及受影响原owner合同。起点B=f16bb562e4ea844939786cebd5c6c20e686914b2，无前序Delivery。

## 2. 有依赖顺序的步骤与文件责任

I1 原RDT owner在隔离贡献内准备behavior-validation-method三个current完整拟写，保共享current不变。I2 trellis-implement负责canonical quality-guidelines方法正文，以及真实需要的Author planning-body §3/Review验证段引用；不改runtime/API或其他Task。I3 执行V1小CLI真实旅程和V2维护，定位装配缺口后修复。I4按事前冻结材料执行V3现行/候选对照，独立评价先匿名，保原失败。I5原tools owner同步本checkout dogfood并做V4，保用户/Task/session，逐个处理sidecar。I6 trellis-check核完整diff和实际证据，原RDT owner final integration/readback，后续TaskCommit及提交后完整Review沿原流程另行授权。

## 3. 验证入口、输入与预期观察

V1/V2使用受支持原生codex exec --ephemeral --json，以现有命令格式和当前可用模型/effort运行外部去敏CLI项目；输入不含host准则或缺陷答案。先记录实际codex版本及设置，再执行真实启动、CLI读写、证据回读和维护。V3现行方法从固定B提取，候选从当前canonical提取；使用同项目初始副本/请求/设置，冻结host准则和匿名标签，原审核者读完整输出与轨迹。采集复用现有方式，无新后台任务或通用工具平台。

V4定向运行 python3 -m unittest test_planning_body_distribution test_review_sufficiency_distribution（在canonical preset scripts/python目录，使用现有匹配测试环境）；受影响包合同检查按实际差额选择。原guru-upgrade-tools local_candidate同步本工作区后运行 check-dogfood-overlay-drift.sh、installed package验证、git diff --check，并读回实际三平台方法引用和原Task/session。若实际方法未触及某测试consumer，不为数量重跑。无完整多平台throwaway矩阵要求。

验证通过只能按实际执行记录；依赖失败、未执行与行为失败分别报告。现有分发测试不证明Agent读法，V1–V3不能证明外部项目采用或普遍成本改善。

## 4. 停止条件与适用回退点

真实产品/范围变化回Clarify；机制超出当前候选回Architecture。设施失败保原错误，重评可回答同问题的复现方式，推进独立工作但保验收缺口。证据足以回答当前问题即停止该实验，不惯例追加rollback/red。保并行改动；只回退本轮未接受的局部内容，不自动stash/clean。无DB迁移、部署或发布动作，故不造其回滚协议。Git/GitHub副作用另走原边界。

## 5. Delivery Policy（唯一）

full：D1覆盖当前Task R1–R5/AC1–AC5。独立交付条件为方法正文和必要consumer完整、真实项目执行及维护完成、真实匿名对照已判读并诚实报告、定向分发同步通过、原质量门禁通过。没有预分配后继；未验收责任仍归当前Task，不以单条样本或Delivery合并替代Completion。当前无额外临时能力限制，环境未证按实际证据缺口处理。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原guru-maintain-requirements-design-test-ssot写隔离贡献，目标为docs/requirements/current/behavior-validation-method.md、docs/design/current/behavior-validation-method.md、docs/test/current/behavior-validation-method.md三个原完整单元。需求记录项目验证与实验行为，设计记录原owner/单一方法正文与事实采集，测试记录V1–V4的层级和原结果位置。保留R735既有条件、identity及历史边界，不另建重复current或改根导航。实施及真实验证后、TaskCommit前由原owner重读目标、整合完整增量并回读；提交后同一次独立Review判断真实after。Architecture no impact不造贡献/ADR。canonical规范与consumer属于实施差额，dogfood经tools owner同步。
