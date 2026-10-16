# #578 跨独立审查者的工程执行事实适用性

## Authority 与边界
Direct Source：https://github.com/castbox/guru-trellis/issues/578，当前正文“范围”“验收”为 requirement authority。没有引入额外外部设计来源。开发基线和交付目标均为 main；固定起点为 404d3f4d7635b19fb2c9f0d6aa642e2f1bf925b4。不得修改既有 phase、mandatory owner、typed route 或 CI/CD。
本仓是 Guru Team extension source，不是业务后端；本次不新增业务 API，不引入后端分阶段接口交付或联合验收。

## 问题
Check 同 owner 的依赖级执行事实采用已经存在；Architecture 的 personally executes 与 BranchReview 的 independently reruns 要求没有区分完整语义审核和命令重跑。正常新 reviewer 或阶段切换因而无条件重复同依赖的业务命令。本次修复该合同原因，不把磁盘成本或历史命令次数推算为资源因果证明。

## 需求与验收
| ID | 必需行为 | 可观察验收 |
| --- | --- | --- |
| AC1 | 每名 owner 先独立判断当前完整候选、风险、消费者与检查集合，随后核查执行事实 | 文档只对齐已有实现、检查依赖不变，新 reviewer 完成当前完整审查，原无关业务检查执行计数不增加 |
| AC2 | 定义/版本、实际依赖、工具链、参数、环境、测试期望均仍适用，原始结果合法可定位且可核查时采用 | 现有 summary 区分本轮实跑与采用，包含来源及适用理由；不声称本 owner 亲自执行原命令 |
| AC3 | 条件改变、原始结果缺失或适用性未知时执行受影响检查；新风险/新义务纳入当前集合 | 变更行为合同、共享依赖、工具链/参数/环境/检查定义及缺失结果的正常 fixture，各自执行需要的消费者或检查，保留无关事实 |
| AC4 | reviewer/阶段/提交身份/promotion 变化不直接使工程事实失效；当前判断与结果绑定必须新鲜 | 当前 owner 正式结果绑定当前候选；旧 pass、旧 freshness token 和已退休 private checkpoint 不能替代 |
| AC5 | canonical 与 dogfood、声明平台、安装投影统一，采用遵循完整安装 | 定向 package/runtime、matching installed public invocation、apply/reapply/drift 与 sidecar/mode 验证；不热补丁活跃任务 |
| AC6 | 行为证明来自真实 Agent 的实际选择和调用 | 小型正常 fixture 的原始命令观察能区分采用、必要补跑、新增义务和当前绑定；文本断言或绿色 DTO 单独不算完成 |

## 非目标与依赖
复用 #464 依赖级复用/局部恢复、#567 固定候选/差额接续、#477 测试价值合同。不新增 Skill、phase、exit、公共 DTO、跨 Skill 验证账本、长期日志平台、缓存协议或审批链。
不改业务仓、全局 Go 参数、缓存容量、磁盘清理、CI/CD 或原部署/Release 门禁。不扩张为完整多平台 Release/Upgrade 矩阵。
ABTest #421 和 Roleplay Backend #607 拥有项目级选 module/package/入口与实际采用；本任务不等待其消费结果作为验收。
设计源约束处分由 design.md 唯一维护；implement.md 拥有 Delivery Policy 和具体验证执行计划。

