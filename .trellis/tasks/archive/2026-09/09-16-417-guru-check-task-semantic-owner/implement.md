# #417 实施与验证计划

需求见 [prd.md](./prd.md)，设计见 [design.md](./design.md)，Docs SSOT Plan 仅见 PRD 第 4 节。

## 1. 执行顺序

- [x] 完成 wording、两项 qualification、Planning Architecture 和 plan approval；最终规划审阅阶段结束。
- [x] 原 start-task.sh 激活 exact task，仅在本 worktree 实现。
- [x] 修改 canonical Phase 2 Skill/contract：当前 AI ownership、六步顺序、authoring 字段和错误分类。
- [x] 增加两个 native case、事实 fixture 和最小 adapter 承接，host 不生成 Phase 2 语义结果。
- [x] 补结构测试并跑四类 deterministic routes、Architecture/post_owner 定向回归。
- [x] 更新 PRD 指定 Docs，经 preset reapply 同步投影并检查 drift。
- [x] 执行真实 native clean/finding cases，审查 transcript 和 wrapper 真实出口。
- [ ] Phase 2 Architecture 与 guru-check-task 完整重审后才提出 Task Commit 计划。

## 2. 验证

命令均在 task worktree 执行。Python 使用 managed interpreter 并设置 PYTHONDONTWRITEBYTECODE=1，不用 py_compile 向源码树写 bytecode。

| 检查 | 入口和通过条件 |
| --- | --- |
| Package | managed Python -m unittest discover -s trellis/skills/guru-team/packages/guru-check-task/tests，全部通过。 |
| Adapter | 既有 native/eval suite 加新增 fixture 测试；expected/actual case 集合完整，Architecture 与 omitted/post_owner 不回退。 |
| Deterministic | 原 run-skill-evals.sh 执行四个既有 case，逐个检查原出口。 |
| Native | 先读取原 runner --help，按当前参数执行 native-owner-clean/native-owner-finding；核验模型、installed 来源、recorder/checker/wrapper 和完整语义证据。 |
| Projection | trellis/presets/guru-team/scripts/bash/apply.sh --repo .；trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh；声明投影 byte/executable parity。 |
| Hygiene | git diff --check；task context 路径可读；受影响树无 .new/.bak/__pycache__/.pyc residue。 |

native 登录、模型、执行能力不足报告具体未验证项，不用 fake CLI 代替。不执行 Release 完整矩阵。

## 3. 风险与恢复

touched 非生成代码达到 3000 行时执行机械拆分或小幅解耦，不重构 untouched 历史文件。
模型语义结果不允许 host patch；上游 Architecture 证据与 Phase 2 authoring 分开。
reapply sidecar 逐个核对，不覆盖无关改动；scope/authority 扩张先重新规划。
提交、push、PR、merge、release、cleanup 各需独立后续确认。

## 4. 当前状态

任务保持 in_progress，未提交或发布。最新 candidate 验证摘要：

- package 27 tests、fixture/transport 5 tests、semantic_authoring 8 tests 通过。
- 两个正式 qualifier 的 clean/finding fixture roundtrip 已覆盖；错误 recorder 返回保持原样，不转为 pass。
- 四个旧 shared cases 的 actual exits 和 deterministic assertions 全部正确；旧 passed-initial 的 semantic grading 未提供，不宣称该旧聚合全绿。
- 最新 installed native 使用 gpt-5.6-sol：clean 返回 passed；finding 返回 implementation_required，真实上界/单点/负数上界测试失败支撑其 finding。两个运行均完成必读规范、Architecture、两个 qualifier 和原 recorder/checker/wrapper。
- 对已完成 transcript 的两项语义断言进行了事后 AI 审查并通过，独立 grading 按正式 schema 校验。raw runner 保留 evaluation_failed/external semantic grading missing；没有预填评分，也没有改写原报告。
- 早期 native 暴露的 qualifier transport、planning identity 和 installed fixture 缺失必读规范已修复并重跑；旧运行不作为最终通过证据。
- 全平台 reapply、installed package validator、dogfood drift 通过；本轮生成的 sidecar 经逐项 preimage/canonical 核对后清理。
- 完整 Release/跨平台 native 模型矩阵未执行，由 #410 负责。验收结论不代表 merge、Release 或 Issue closure。
