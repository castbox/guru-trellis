# #872 Discovery 关联检索与草稿绑定整体需求

## 1. 来源与术语

| 来源 | 角色 | 用途 |
| --- | --- | --- |
| [Issue #872](https://github.com/castbox/guru-trellis/issues/872) 全文及本次需求审核评论 | Direct Source 要求 | 正常场景、交付范围、验收及边界 |
| main@e33ecf82d 的 Discovery contract、owner-result 4.0 schema、runtime/common.py、test_contract.py | 当前事实 | 核实现有组合条件、检索差异、恢复与兼容承诺 |
| 官方 custom-workflow / custom-spec-template-marketplace | 扩展约束 | Markdown 管理判断和流程，不修改上游或全局安装 |

关联引用仅用于背景或检索；真实绑定指草稿与已有开放 Issue 的同内容来源绑定。两者不能互相推导。

## 2. 背景与问题

业务仓库创建新草稿时把关联 #1689/#1269 填入 issue_refs，同时 issue_binding=null。现行 draft+非空 issue_refs 条件要求绑定对象，record 按合同拒绝。AI 误判为 runtime bug 并停止。合同的无绑定示例未在原位说明该条件及关联线索表达。将编号移入 terms 的局部通过不证明原链或检索等价；两类计分不同。

## 3. 目标与非目标

使正常调用方从 Discovery 公开指引构造保留关联检索用途的未绑定草稿输入，普通装配错误由原 owner 纠正后继续原链。完整承担 #872；保留真实绑定一致性检查。

不交付业务搜索、不创建业务后续 Issue、不重写通用 schema、不改变检索权重/排名或新算法、不要求下游 Clarify/Readiness/创建与完整多平台安装升级发布矩阵。

## 4. 真实调用方、场景与流程

| ID | 前置与动作 | 结果 |
| --- | --- | --- |
| S1 | Discovery owner 依据公开指引处理关联已有 Issue、但尚无外部绑定的新草稿 | 关联线索仍用于检索，正确输入经公开 record/check/invoke 得到 context_ready |
| S2 | 同一场景普通装配时将关联编号误放入会触发绑定约束的字段 | 明确条件及正确表达，原 owner 保留失败并纠正、重跑原链；不伪造绑定，不误报内部故障 |
| S3 | 草稿确有合法同内容 Issue 绑定 | 原来源和内容一致性规则继续适用 |

## 5. 行为要求

- R1：在原 Discovery 合同、入口和示例清楚区分关联线索与真实绑定，给出适用条件及可执行表达；不能删除线索来通过校验。
- R2：保留原 AI 判断、record/check/invoke 与真实绑定一致性门禁；本场景不普遍放宽 null。
- R3：普通装配错误沿原同范围恢复，准确定位条件并纠正，无需伪造绑定或把字段错误当内部故障。必要诊断改动须有实际缺口依据。
- R4：canonical 修改沿原 owner 同步受影响投影。若公共 I/O 改义，先遵循已有兼容迁移合同；不静默破坏。

## 6. 约束与依赖

Markdown 拥有语义判断；确定性脚本只负责事实与结构。优先复用既有 fields/terms 和恢复机制，具体方案由原 Author/Architecture 判断。source schema 与业务安装一致；不据此宣称修复后调用方已验证。普通 Issue 仅执行必要 package、投影、drift/sidecar 和实际调用验证；不扩大矩阵。无数据迁移、线上部署或凭证配置需求。

## 7. 可观察验收与验证方式

AC872-01（R1—R4/S1—S3）：调用方从修订指引为有真实关联线索的未绑定草稿构造输入，保留检索用途，并通过公开 record/check/invoke 返回实际 context_ready；普通字段装配错误可按准确指引纠正重跑；真实绑定保持原一致性合同。实际指引产生的调用与公开结果是行为证据，固定文本/局部 schema 不能独立证明；复用已有适用证据并仅补真实缺口。不要求下游创建、业务接入或生产效果。

## 8. 实际未决项

没有阻塞需求的用户选择。机制、测试与分发方案在 Delivery Planning 明确；不预填通过。完整安装升级发布矩阵明确不在本 Task，修复后的调用方行为尚待实施验证。
