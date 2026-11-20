# D1 实施与验证计划

## 1. 输入与引用

使用本 Delivery PRD、design 第 3–8 节、整体 PRD 和独立 Architecture 候选结论。起点为从 origin/main 固定的 B。本 Delivery 没有前序。加载写作、Skill Interface、companion stdout、测试价值和当前知识安装规范。

## 2. 有依赖顺序的步骤与文件责任

1. Workflow owner 更新 canonical 的入口和路由指针。只读完成退出对应用户响应，明确请求开工时消费正式 Issue。
2. Clarify/Readiness owners 实作独立 profile、客观 stdout 校验及最小可读调用样例。共同方法说明证据采用、增量复审和实际缺口。保留旧完整链及按缺口补查。
3. Create Issue owner 添加直接路径和预备命令，复用原写入及同对象恢复。明确查重时限与用户等待的关系并给出可直接调用的示例。
4. 运行 source 及各受影响 functional tests 后，通过原 tools owner 同步 dogfood。运行已安装包和相同材料的真实 Agent 对照。
5. 原 RDT owner 集成受影响的 Requirements、Design、Test。原 Architecture owner 集成完整职责与必要决定。逐份读回后准备 TaskCommit。

## 3. 验证入口、输入与预期观察

运行受影响的包测试和 `check-skill-packages.sh --mode source|installed`。用只读正常及已变化的 live snapshot 驱动真实包装器，检查结果和零写入。复用现有 Create 测试的状态化 gh 替身，新增预备 stdout 接入点；检验 stale 的零创建、恢复的同对象，以及开工路由和老消费者。运行定向 `check-dogfood-overlay-drift.sh` 并检查 sidecar。真实 Codex Agent V1–V2 对照和应用运行输出分开保留，失败如实列入记录。

## 4. 停止条件与适用回退点

如发现正文义务、既有消费者或已确认 payload 被改动，按最早影响的 owner 修正，再执行针对性验证。安装冲突按原 tools owner 恢复。同对象建单输出丢失按原事务恢复。源或设计差额超出现有范围时进入原规划回程。足以证明验收后结束当前检查。

## 5. Delivery Policy

full。D1 覆盖 AC01–AC03 的完整交付。完成条件为三个入口、复审与变更分流均有相应工程和 Agent 观察，建单 writer 复用及原开工相容通过，精确证据录入现有配对 Test。Task Completion 仍按整个 Issue 的实际记录独立判断。

## 6. Docs SSOT Plan

delta_first。更新 `docs/{requirements,design,test}/current/issue-content.md` 命中的入口与验证定义。更新原 Architecture domain 和决定关系。规划使用隔离候选，实际工作和工程验证后分别由原 RDT 和 Architecture owners 集成并读回。独立 committed Review 以真实 before/after 为判断范围。配置、发布和其他职责沿用现有直接消费者。
