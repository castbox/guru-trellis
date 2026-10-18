# #154 规划正文合同 Architecture contribution

Identity：`architecture-contribution-154-planning-body-contract-v1`。状态：`reviewed_promoted`，晋升至 `current-main-0.6.17-guru.99`。所属 Task：`154-planning-body-contract`，generation `0`；Delivery：`fcc749cc-2240-4fc3-a457-dc86ec962462`。前置基线：`current-main-0.6.17-guru.98`。来源：[Issue #154](https://github.com/castbox/guru-trellis/issues/154) R1/R2/R4/R5/R7 的规范性边界。

## 当前与目标边界

原 Author 已唯一拥有整体 PRD 与 Delivery 三正文的写作，但缺明确正文骨架。目标在同 canonical package 增加一个共享正文合同、四类薄模板及两组完整去敏过程示例；写作 profiles 显式加载，原 consumers 在各自职责读取同源合同和必要引用。原生 seed/生成器仅创建初始文件，既有 recursive preset 分发负责安装，官方 agents/hook 不承载新业务规则。

路径为 `target_native`，沿 [ADR-022](../adr/022-unique-planning-author.md) 和 [ADR-024](../adr/024-task-delivery-public-authority.md)。本轮不新增 ADR、公共 Skill、phase、DTO、持久化状态、第二写作 owner 或兼容 reader。真实方案由选定 Delivery design 第2–8节承载；本 contribution 仅拥有长期 Architecture 差额，不重复正文模板规则。

## 适用 concerns

| Concern | 适用性与本轮处理 |
| --- | --- |
| authority-binding | applicable：Planning3.0 candidate/final 两目的仍由原 Architecture；当前阶段绑定基线98与 change-contract-v1。本文不是 pass 或 promotion 结果。 |
| constitution-binding | applicable：引用唯一 constitution-v1；新增能力的必要性是四类正文及实际加载，不新增无 consumer 机制。正文骨架归原 Author，分发归原 preset。 |
| boundary-and-decision | applicable：现有 writer/模型不变；目标为原 package 内正文能力与 consumers 直接加载。ADR-022/024 足够，无新决策 authority。 |
| owner-and-single-writer | applicable：Author 写规划与本 task-owned contribution，Clarify/Architecture/Wording/Approval 保留原判断；RDT/Architecture 原 owners 才能晋升共享 authority。 |
| compatibility-and-exit | applicable：同步受控 consumers 与完整 matching package/preset；不留 dual-read、旧模板 authority 或长期 adapter。旧历史不重写，已有安装经原采用路径更新。 |
| gap-and-deviation | applicable：不修改既有 GAP lifecycle，不主张关闭或重开 GAP；若实际实施引出新增/恶化偏移，回原 Architecture owner，不靠模板说明覆盖。 |
| parallel-scope | applicable：只写本 Task 规划、隔离贡献和本次 canonical 变更；不竞争 shared-current、GAP 或其他任务的 ownership。共享晋升仍 expected-current 单写。 |
| evidence-and-freshness | applicable：候选与 Wording-current design 分别绑定原 freshness；真实 Agent、确定性、安装三类证据由唯一 Test 分列。工程、安装及真实 Agent 场景的当前结果和未完成边界统一定位唯一 Test；这里不复制分场景通过状态。 |
| review-and-promotion | applicable：final_plan 审本真实贡献及设计；实施阶段独立 Architecture 审完整候选后再由原 owner 晋升，最终 Check/commit/独立完整 Branch Review 覆盖实际写入。Planning 不晋升。 |

## 证据与晋升边界

项目检查沿 `guru-trellis-architecture-convergence:repository:1` / `guru-trellis-architecture-convergence@1` 与原 result2.0。独立 Phase 2 Architecture 评估完整实现及本次拟写内容后，原 Architecture owner 按 expected `.98` 晋升本贡献。正式项目检查与实际结果由原 owner 的当前调用产生，本文不替代该调用。

本轮实际验证由 `docs/requirements-design-test-contributions/154-planning-body-contract/test.md` 唯一承接。该 Test 已写实际定向结果和失败边界。V1–V7 与代表性安装的实际结果由该 Test 按证据更新；其他平台行为、完整 Release 矩阵及软件发布不由分发检查证明。本贡献与共享后继的实际写入仍由原 owner 核对适用性，并由最终 Check、TaskCommit 及 committed 独立 Architecture/完整 Branch Review 审查；本文不替代这些判断。
