# #417 修复 guru-check-task semantic owner 自阻塞

## 1. 目标与来源

修复 Phase 2 当前 AI semantic owner 自阻塞，并补充真实 native semantic-authoring 回归与安装投影验证。

来源：https://github.com/castbox/guru-trellis/issues/417 当前正文。评论中的人工纠偏 Prompt 是历史诊断材料，不复制为产品合同。

## 2. 需求与验收

| ID | 需求 | 验收结果 |
| --- | --- | --- |
| R1 | 当前 AI 加载完整 contract，读取 task、approved planning、live diff/dirty paths、Architecture result、实现、测试、Docs 和验证证据，完成九维审查，编写语义内容，再调用原 recorder/checker/wrapper，消费唯一出口。 | native transcript 显示读取、审查、authoring 和正式调用顺序；host 不预填 Phase 2 owner result。 |
| R2 | worker 未派遣、不可用或无 agent ID 不阻塞 owner；owner_not_yet_executed 是继续审查的内部状态。 | 两个 native case 均无 worker 前置，不要求用户重复解释 ownership。 |
| R3 | 真实 authority/Architecture/mandatory validation 缺失不通过；schema/identity/freshness/path 错误保留原诊断并由当前 AI fresh re-entry。 | 定向缺失证据用例不能产生 passed；平台能力缺失须有实际失败证据。 |
| R4 | 增加真实 installed/native clean 和 finding cases，expected exit 不进入模型输入。 | clean 实际返回 passed；finding case 根据实际需求违背返回 implementation_required；语义内容由 AI 完成。 |
| R5 | 保持四个 deterministic exits、schema 和 consumer。 | passed、implementation_required、planning_stale、blocked 原路由测试通过；Architecture authoring 和 post_owner 不回退。 |
| R6 | 同步 canonical、installed、dogfood、Shared/Codex/Claude/Cursor。 | reapply 后 byte/executable parity 与 drift 检查通过，受影响树无 .new/.bak/bytecode residue。 |

## 3. 证据与非目标

当前 guru-check-task contract 已声明 sole semantic owner；同包 eval facts 使用 owner_staging。
owner_staging.py 与 native_adapter.py 的 semantic_authoring 分支仅支持 Architecture；#415 不能证明 Phase 2 已修复。
不改业务仓 #323，不扩展 #415，不提前实现 #404/#292/#383/#398，不新增生产 wrapper、owner、授权 artifact 或长期 handoff。
不引入攻击模型、竞态压力、锁或 crash-consistency 加固。完整 release matrix 属于 #410；修复合并后由其重新冻结 candidate。
native 登录、模型或执行能力不足必须报告未验证，不使用 fake-native、关键词或 deterministic 成功代替真实语义回归。

## 4. Docs SSOT Plan

decision=update。本节是唯一文档更新清单。

| 路径 | 决策和 consumer |
| --- | --- |
| trellis/skills/guru-team/packages/guru-check-task/SKILL.md、references/contract.md | update：Phase 2 当前 AI 消费 owner 顺序、authoring 与错误分类。 |
| .trellis/spec/workflow/skill-package-contract.md | update：eval owner 消费 Phase 2 authoring 与 post_owner 证据区别。 |
| .trellis/spec/workflow/quality-guidelines.md | update：checker/reviewer 消费真实 native 和投影验证边界。 |
| trellis/workflows/guru-team/README.md、trellis/presets/guru-team/README.md | update：验证调用者消费回归入口，不复制 Skill 内部步骤。 |
| docs/requirements/、docs/design/、docs/test/ shared current | no_update：维持既有 sole-owner 与四出口合同，不晋升演进目标。 |
| docs/architecture/ shared current | no_update：current-conforming，理由见 design 第 4 节。 |

## 5. 状态

无待决定的产品范围问题。规划编写不代表正式 Planning Gate、实现或发布通过。
