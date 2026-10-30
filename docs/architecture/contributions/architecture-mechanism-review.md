# 架构机制审核与存量收敛 Architecture contribution

Identity：`architecture-contribution-mechanism-review-v1`。状态：`proposed`。所属 Task：`architecture-mechanism-review`，generation `0`；Delivery：`2a0bdf40-feb7-4d21-b232-a9071b986820`。适用基线为 Git `2f70796103406683a2f63adfb6b54d247a7433a5` 的 `guru-trellis-architecture`。本文是本任务真实隔离架构差额，不是 pass、授权记录或已晋升声明。

## 当前、目标与变更路径

现行项目 change-contract 的 Constitution applicability consumption 明确落在新增能力与 minimum-necessary-complexity。目标是让该项目投影承接完整宪法下的本次采用机制审查，包含无实现 diff 的复用、保护提出方责任，以及纠正旧决策后的实际存量与完成义务。

路径为 `target_native`。公共方法仍由原 Architecture、Protection 与 current-knowledge 正文拥有；本项目只消费其方法并承接本项目既有 concerns、owner 和路由。RDT 只写自身三层 authority，不能代写本项目 Architecture。没有新 workflow 阶段、公共 API/DTO、状态库、writer、锁、双轨 reader 或兼容框架。

本贡献关联现有 `ARCH-GOV-007/008/012`、`ARCH-DOM-008`、`ADR-034`。不新增技术栈选择、原则例外/排名、owner/single-writer 或 compatibility exit；因此当前无需独立 ADR。实际实现若改变这些事实，由原 Architecture owner 重新判断，不能以此处预期免审。

## 完整拟写与责任

唯一当前 Architecture target 是 `docs/architecture/06-governance/change-contract.md`。完整 proposed 内容见 [拟写正文](architecture-mechanism-review/proposed/docs/architecture/06-governance/change-contract.md)，仅修订原 Constitution applicability consumption 方法投影，保留其余完整前驱和路由。

Author 按独立 candidate_assessment 编写本 Task 隔离贡献；独立 Architecture 对 Wording-current design 和本贡献作 final_plan。implementation 准备完整实现及拟写；原候选 Check 通过并合法回 implementation 后，原 Architecture owner 在 final_integration 固定真实目标、比较适用前驱/完整拟写/current、补审实际组合差额，写入并逐一读回。然后 implementation 重绑全部 after，完成最终 Check、commit 与独立 committed Review。Planning 不写 shared current。

RDT 的 knowledge/completion 六个完整目标由原 RDT owner 在自己的隔离贡献中维护；两方各自单写，不以 RDT contribution 取得 Architecture 写权。本任务不迁移后端业务实现或升级业务安装。

## 九 concerns

| Concern | 适用判断与本轮落点 |
| --- | --- |
| authority-binding | applicable：Planning3.0/Delivery1.0，candidate_assessment 与 final_plan 各自正式执行；原 baseline/change-contract identity 保持，精确前驱使用上述 Git。 |
| constitution-binding | applicable：读取唯一 constitution-v1，按实际命中取舍，不复制正文、排名或逐原则评分。 |
| boundary-and-decision | applicable：project 方法投影是实际 authority 差额；采用 target_native，保留既有 decision refs，不把旧技术选择自证为必要约束。 |
| owner-and-single-writer | applicable：原 Architecture 独占其拟写和最终写入；RDT 独占自身三层；Author、Check、Review、Completion 保持原职责。 |
| compatibility-and-exit | applicable：同一方法直接修订并经原受管分发；没有第二 runtime 路径。历史任务按真实阶段适用性承接，不重写历史或扩张旧模式。 |
| gap-and-deviation | applicable：不声称关闭、重开或迁移既有 GAP lifecycle。当前方法缺口由真实变更与验证证明；未验证收益保持未知。 |
| parallel-scope | applicable：本 Task 仅写自身贡献/proposed 和命中 canonical 文件；不写其他 Task，不竞争 shared-current，写前核真实 target。 |
| evidence-and-freshness | applicable：候选事实和最终设计各有原调用期 freshness；工程、安装、真实 Agent、外部采用分别报告，不建长期 digest/审核链。 |
| review-and-promotion | applicable：完整实际实现与所有拟写先独立 Architecture/候选 Check，再原 owner final_integration/readback、after 重绑、最终质量链。 |

## 项目检查与证据边界

沿用 `guru-trellis-architecture-convergence:repository:1`、`guru-trellis-architecture-convergence@1`，原 entrypoint 为目标 change-contract，result contract 为 `guru-project-architecture-check-result-2.0`。实际语义检查由原独立 Architecture 对当轮完整候选执行；本文不预填未来 pass 或新增 descriptor。

本段记录贡献初次拟写时的观察：当时工程、分发和四组原/新 Agent 对照尚未执行。后续实际结果唯一由 `docs/requirements-design-test-contributions/architecture-mechanism-review/test.md` 承接，分别记录实际来源、条件、观察、首次失败/修复与未验证边界。规则改动不证明业务安装已采用，也不证明后端密钥或旧实现已迁完。

## 兼容与删除边界

没有新增需要长期保留的旧 parser、writer 或配置；受管安装副本由原 preset 更新。历史 ADR、贡献和不可变版本是来源，不是第二活动 authority。普通 helper 不逐个建审查单元；被纠正决策的存量分析不得反向授权本任务跨仓修改或线上删除。旧资源退出仍要求真实消费者和支持窗口已退出，再按对应合同处理。
