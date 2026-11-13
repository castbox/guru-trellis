# D1 项目行为验证与 Agent 对照实验需求

## 1. 整体来源与术语

整体 authority 为 .trellis/tasks/11-13-826-verification-experiment-methods/prd.md，revision sha256:af3db2f6b64985ea1a9eb45f5522889c5ee640d25fb5ea42489116132556d9d1；Direct Source 为 https://github.com/castbox/guru-trellis/issues/826 全文。本批 scope_ref 选定 R1–R5、AC1–AC5，planning_root 为 deliveries/e74b8c49-7042-4896-a74f-61527e7050c0。术语沿整体PRD第1节，pstack只作方法参考。

## 2. 整体与本批目标、非目标

D1 交付两项方法的完整增量：项目验证入口的发现、建立、执行、维护；真实Agent对照实验的隔离、匿名评价和边界报告。复用R735通用方法与现有采集，消除只有规范没有可执行方法的缺口。全部整体非目标保持：不改生命周期、权限和现有公共API语义，不引入总控、固定实验门禁、设备/并发/故障注入/形式化或完整多平台矩阵，#747只关联。

## 3. 本批起点、前序结果、依赖与剩余责任

首次D1，无前序Delivery。起点Git f16bb562e4ea844939786cebd5c6c20e686914b2；现有共用方法与eval runner可用，但本批方法和实际运行尚未完成。依赖可运行去敏项目与原生Agent入口。D1覆盖全部当前要求；缺依赖和未验收责任仍属于本Task，不能以方法正文或单项通过宣称整体完成。整体Completion需AC1–AC5及原交付结果。

## 4. 本批调用方、场景与流程

S1：实施者读取真实项目入口和已有设施，复用或补方法，依次启动、确认就绪、操作、观察、清理并回读保留证据。S2：行为或入口变化，维护者定位、更新并重跑受影响路径。S3：方法维护者在相同任务材料上执行现行与候选方法，评价者先匿名判读，原owner综合原始输出。S4：依赖或执行失败时分别保留环境失败、未执行和目标行为失败，不记通过。

## 5. 完整行为、条件与约束

R1：方法明确启动、可用就绪、真实操作、可观察结果、证据位置和清理；只清理本轮资源，证据保留，权限沿目标项目。

R2：实际跑通一条正常旅程，区分直接方法/替身/真实入口层级；无UI按CLI/API/库调用方验证，不强制设备。入口或行为变化更新并重跑受影响路径，复用适用证据，不建重复功能账本。

R3：现行/候选采用相同材料和事前固定标准。执行者不见标准、答案或优劣标签；评价者先读匿名输出和真实工具记录，原owner判断结果。脚本不决定语义充分性。

R4：复用原runner/原生入口/采集。保留支持复核的最小材料、方法版本、环境差异及真实输出，不保留授权或敏感信息。环境、未执行、产品失败分开，失败不静默替换。新实验回答具体缺口；小样本不推断普遍质量或成本改善。

R5：原职责消费方法，canonical/preset/tools owner分发，保留定制及Task/session，无新增固定审核轮次或门禁。具体新增Skill的必要性及I/O由后续Architecture和方案阶段判断。

## 6. 本批验收、验证方式与未决项

AC1：可运行去敏项目执行完整启动至清理后证据回读，核对层级和实际入口。AC2：改变覆盖行为或入口后验证维护能更新并重跑受影响路径。AC3：本批执行一次现行/候选真实Agent匿名对照，事前标准与材料冻结，真实报告改善、退化、未证。AC4：原审核者核对原始输出和工具，拒绝自述替代证据。AC5：定向package/runtime、分发、reapply/drift、sidecar及实际投影检查。全部尚未执行，不推断Release或外部采用。无产品未决；候选方案仍待独立Architecture，未提前写设计和实施计划。

## 7. Canonical 引用与本轮差额

requirements/design/test current/behavior-validation-method.md 的R735、D735、T735为已有验证方法。本批补项目入口维护及匿名对照方法，原规则不复制。quality-guidelines Test And Validation Value提供测试边界。Architecture入口 docs/architecture/README.md、00-foundation与06-governance决定方法/工具职责；实际影响由独立Architecture判断，本PRD不预设无影响。后续需要的文档贡献由原知识owner准备和整合，不写共享导航登记。
