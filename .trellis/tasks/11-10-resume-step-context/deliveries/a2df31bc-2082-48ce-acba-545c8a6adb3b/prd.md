# D1 正常续接与实际出口查询需求

## 1. 整体来源与术语

整体 authority 为 Task 根 `prd.md`，accepted_scope 由公共 Task record 绑定。本 D1 的 scope_ref 选择 AC1–AC7，planning_root 为 `deliveries/a2df31bc-2082-48ce-acba-545c8a6adb3b`，无前序 Delivery。

直接来源、术语与非目标引用整体 PRD 第1、3节；冻结外部请求全文和实施约束已读取。当前会话的最小 current 输出约束是要求；#736 第2、5、6项只是参考。外部 comparison protocol 只作验证参考，不能成为产品 authority。

实施基线与新对照条件采用冻结补充 `/Users/devSC/Documents/JobProject/guru-validation-evidence/fizz-filter-controlled-2026-11-10/host/resume-step-context-baseline-adjustment.md` 的「新基线与保留内容」「对照含义调整」「当前证明边界」。它调整实施输入和取证边界，不改变整体 R1–R9/AC1–AC7。整体 PRD 的 `43d8f713` 保留为原调查历史，root 正文及 accepted_scope token 不变。

## 2. 整体与本批目标、非目标

本 D1 全量实现两处公开入口差额：原 ensure 增 current 组合 profile；原 discovery 增实际 exit 投影。共同目标是让正常 caller 取得足够而精简的身份及唯一 consumer 定位。

不转发完整上游 Delivery/results/candidate paths，不新增 resolver、平行 wrapper 或 profile help。整体 PRD 的 upstream/start、launcher 重构、整 #736、旧旅程 Task、业务功能和发布非目标全部适用。

## 3. 本批起点、前序结果、依赖与剩余责任

实施起点为整合提交 `26630149070e2988ad08102679931468b3535ef8`，父提交为 main `43d8f713865a7d621d838cf851bc358c34d29f29` 和 journey `f4a3da407bae582088c80213ddbf721e9b38a537`，交付目标仍为 main。它继承完整旅程方法及 main 更新；本 D1 尚无查询实现或验收结果。复用 `task.py current --json`、原 ensure 校验、`runtime/installed.py` marker/parser 和现有 Interface discovery。

一个 D1 覆盖整体 R1–R9、AC1–AC7；不预留空 D2。剩余责任是实施、定向验证、一次代表性安装投影与短原生对照，以及原流程的整体 Completion；规划通过不完成这些责任。

## 4. 本批调用方、场景与流程

- D1-S1：caller 自己已有合法 Task；current profile 消费原 current，校验 Guru 归属，返回最小 Task/checkout 和可用 Delivery 定位，不写 selection。
- D1-S2：无 Task、无 Delivery 或普通 mismatch；区分无对象与读取错误，保留原 owner 和诊断，不从 inventory 选对象。
- D1-S3：caller 已有真实 Skill/exit；discovery 查唯一 marker/Interface consumer，返回原 input/projection 与入口定位，动态 selector 不被提前求值。
- D1-S4：未知出口、多重/未映射开发声明；明确非通过，不挑一个 consumer。生产安装不写损坏数据。
- D1-S5：需要 profile authoring 的 caller 使用已有 help，完整读适用合同，不新增另一套导航。

## 5. 完整行为、条件与约束

整体 R1–R9 的完整条件适用于本批：保留旧显式 ensure profile；新 current profile 只含必要 identity/checkout/key/phase/planning，校验缺失交原 owner；discovery --exit 复用原解析及 consumer 合同；只读不改变 Task/Delivery/session/Git/业务状态；原 launcher ignored cache 刷新单列。

实现必须修改 Guru canonical，再由原安装 owner 同步。新字段、输出与相邻 consumer 需完整公开合同和兼容说明。design 第3节拥有唯一来源设计处置；本 PRD 不另设设计矩阵。查询不能推断业务下一步或阶段通过，不能绕过当前 owner 的完整合同。

## 6. 本批验收、验证方式与未决项

| ID | 入口和输入 | 预期观察 |
| --- | --- | --- |
| D1-AC1（整体 AC1、2） | 原 ensure 新 current profile：合法 Task/有无 Delivery、无绑定、正常 stale/mismatch | 最小事实正确、原校验生效、无状态变更；大 results/candidate 树不泄入公共输出 |
| D1-AC2（整体 AC3、4） | 原 discovery --exit：Skill/workflow/stop、动态 selector、未知及局部歧义 fixture | 唯一路由及原 contract 定位正确，动态选择不猜值，错误明确 |
| D1-AC3（整体 AC5、6） | 旧显式 profile、help；受管安装投影与定向 tests/reapply/drift | 旧接口兼容，原入口消费与完整合同读取一致，无并行内容丢失 |
| D1-AC4（整体 AC7） | 外部冻结 bound/unbound 原生 prompt，同模型/输入/环境；两组共用 `26630149` 旅程方法 | 新取控制组首次结果并另存，实验组只增加两项查询差额；历史 `43d8/unbound` 不用于新组节省比例；准备查询与待测查询、cache 刷新分列 |

均为待执行。无待用户决定问题。原生设施缺失保留具体缺证，不以机械通过替代。

## 7. Canonical 引用与本轮差额

`docs/requirements/current/task-delivery-lifecycle.md` 和 `docs/architecture/03-domains/ownership.md` 保有身份职责；`docs/design/README.md`、`docs/test/README.md` 按原完整单元发现合同定位必要正文。实际两项查询差额仅由原 RDT/Architecture owner 在实施中维护命中的完整单元。

当前公开合同为 `trellis/skills/guru-team/packages/guru-ensure-task-checkout/`、`trellis/skills/guru-team/runtime/discovery.py`、`runtime/installed.py` 与 `trellis/workflows/guru-team/workflow.md`。测试方法沿 `.trellis/spec/workflow/quality-guidelines.md` 的 Test And Validation Value，不另造质量门禁。Architecture 先读取项目 constitution/baseline/change-contract，再独立评估真实候选；本 PRD 不提供其结论。
