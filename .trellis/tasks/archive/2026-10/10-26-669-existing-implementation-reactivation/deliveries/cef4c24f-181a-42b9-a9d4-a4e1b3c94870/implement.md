# D1 实施与验证计划

## 1. 输入与引用

整体 Task 根 PRD R1–R7/AC1–AC5、本批 PRD、design 第3节来源处置及第4–8节实际机制为本批输入。固定 B=`83512901506409f59016121aebc2d0b0bbe98059`，首批无前序 Delivery。读取 `.trellis/spec/workflow/{workflow-contract,companion-scripts,data-contracts,skill-package-contract,quality-guidelines,subtraction-first-compatibility}.md` 适用完整条件；清晰写作正文和 guides 进入 implement/check context。

架构原候选结论是 `architecture_impact / target_native`；最终规划仍须 Wording、独立 Architecture final_plan 与 Approval。后续步骤不得把本计划或文件存在当 gate pass。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与原 owner | 文件 / 行为 | 完成观察 |
| --- | --- | --- | --- |
| I1 | 当前规划批准及 Activation；implementation worker | Reactivate 独立 public/semantic/必要 transaction schema、interface/commands/examples、MIGRATION-669、SKILL 和薄 workflow/README定位 | 新入口明确定义，旧合同保留原义 |
| I2 | I1；原 Git facts/C3及Reactivate实现 | 逻辑index/文件内容/类型/执行位 snapshot、精确既有checkout承接、repo-bound PR只读观察、原增代/后继/同操作恢复 | 原公共 writer 被复用，无通用 allow_dirty、无远端写/清理 |
| I3 | I2；同 implementation worker | Reactivate/C3源码与真实Git回归测试 | V1–V4验证真实行为与保留/拒绝结果；失败归因明确 |
| I4 | I1–3；主会话原分发及RDT writer | preset apply同步dogfood/installed/声明平台；RDT隔离完整拟写与Architecture contribution | V5和无漂移证据；共享current尚未提前写入 |
| I5 | 完整候选；原独立Architecture与Check owners | 旧authority、所有代码/测试/隔离拟写 | 实际 candidate_checked；不产生最终Check通过 |
| I6 | I5；原Architecture/RDT promotion owners | final_integration实际更新合适完整current单元并回读 | 对真实after判断适用性，不遗漏原条件 |
| I7 | I6；原implementation/Check/独立Review | 重新candidate/begin_check、最终Check、精确提交、完整B..H Review | 原当前公共gates和真实提交完整对应 |
| I8 | 代码与安装可用；实际原生Agent/主会话 | 单个受控安装Git案例执行V6；Delivery Review/Publish/Merge后整体Completion/Closure/Finish | 分层结果、真实PR与终态事实，不把合并视作整体完成 |

Worker仅编辑分配的canonical源码、schema/例子与测试；主会话拥有规划、架构贡献和RDT正文、分发、提交与发布收尾。保留其他工作区与并行改动。

## 3. 验证入口、输入与预期观察

- V1/V3/V4：`python3 -B -m unittest discover -s trellis/skills/guru-team/packages/guru-reactivate-task/tests`，并运行改动实际影响的 lifecycle checkout/branch substrate suites。输入和观察按 design 第8节；不得只断言新字段存在。
- V2：逻辑 snapshot 的真实Git回归，覆盖正常index刷新不误报、staged/unstaged/untracked与文件模式/类型变化可检测、旧capture/rebind语义保持。新增测试限本AC直接需要。
- V5：按 quality-guidelines 的内存Python syntax检查；package source/installed checks；`trellis/presets/guru-team/scripts/bash/apply.sh --repo .`；`check-dogfood-overlay-drift.sh`；定向schema、shell语法、task validate、`git diff --check`。检查 `.new/.bak`，逐项处理本批source变更引起的备份，不碰既有未知资产。
- V6：在独立临时repo完整安装匹配版本，driver通过公共Task操作建立准确前驱并形成真实Git归档/实现提交；受控gh提供原Draft PR和bookkeeping事实。实际Agent读取原生入口、核语义并调用installed wrapper，观察同TaskId增代、工作区/原PR保留和输出丢失后的同后继。记录其真实命令、结果和外部边界；不声称真实GitHub/backend恢复。
- 最终检查只覆盖本Delivery完整候选及已晋升正文。完整多平台Throwaway、发行升级矩阵、生产/业务实际恢复未验证，由原对应工作承接。

## 4. 停止条件与适用回退点

source/TaskKey/DeliveryKey或当前authority失配回原owner；本批实现发现新职责/范围变化先qualification及Architecture重入，不静默实现。普通authoring、stale或mapped re-entry在原owner自动修复，不制造用户确认。

真实内容/HEAD/PR/ownership失配必须保留现场并给具体诊断。公共reopen已发生后不删除后继或回退提交；沿原结果和transaction补本机接线。未完成的本机操作保持真实失败结果，缺环境标为未验证，不写pass。

## 5. Delivery Policy（唯一）

策略为 full。D1承担整体R1–R7/AC1–AC5；没有延期功能或第二业务切片。完成条件是代码、合同、定向回归、分发与安装后原生恢复证据均满足，完整候选获当前门禁并合入main后再由Completion判断整体scope。Delivery合并不替代Completion、Closure或Finish。

临时限制仅是验证环境：受控provider证据不证明真实GitHub/backend/生产效果。本批不要求这些外部效果，不能把该限制扩大为整个新能力不可用。

## 6. Docs SSOT Plan（唯一）

strategy=`delta_first`。原Author创建实际Architecture contribution；主会话作为原RDT writer维护 `docs/requirements-design-test-contributions/669-existing-implementation-reactivation/` 的requirement/design/test/traceability及完整拟写。直接consumers是原独立Architecture、candidate Check、原RDT/Architecture final_integration与最终Review。

拟晋升目标是 `docs/{requirements,design,test}/current/completion-closure.md` 的实际Reactivate与验证单元，以及 `docs/architecture/03-domains/ownership.md` 的原ARCH-DOM-060/shared lifecycle完整职责。原owners在candidate Check之后、最终Phase2之前按真实expected-current整合并回读。原历史定义和贡献保留为provenance；不增加全局版本、重复导航摘要或无consumer账本。现有ADR-PORTABLE-SHARED-LIFECYCLE继续适用，无新ADR/GAP。
