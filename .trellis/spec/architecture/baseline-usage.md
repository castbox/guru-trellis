# Architecture Baseline 使用规则

本页是项目读取投影，不保存第二套 current version、架构定义或历史增量。

## Authority

- Baseline locator：`docs/architecture/README.md`，版本及状态从该入口读取。
- Constitution：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1`。
- Project change contract：`docs/architecture/06-governance/change-contract.md`，包含真实 concern 和 project-check descriptor。
- 两层栈选择：`docs/architecture/00-foundation/stack-selection.md`，固定通用源/version，项目只拥有选择、范围和差异。
- 当前治理：`docs/architecture/06-governance/rules.md`，稳定 ARCH-GOV identity 可直接定位，历史原因进入其 ADR/Git 来源。

## 读取与维护

原 `guru-maintain-architecture-baseline` 先判断阶段适用 authority，从根入口取得职责目录和发现方法，再在该阶段的目录范围内按稳定 ID、alias 或概念限定检索。读取完整单元、原 owner 晋升状态/适用来源及必要 RDT 关系；目录名、文件存在或搜索命中不建立 current。根不枚举全部单元，普通独立主题不写根或另一共享登记文件。

完整知识读取方法由 `.trellis/guru-team/skills/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md` 唯一拥有；Architecture 专属 profiles/concerns/独立评估及晋升只读原 Architecture package。本项目采用/未迁移范围和旧写退出从 `trellis/presets/guru-team/MIGRATION-711.md` 及真实 authority 读取，不能把安装新规则当作项目文档已切换。

FOUNDATION、CURRENT、TARGET、GAP、PLAN、ADR、EVIDENCE 保持原角色；目标或接受的选择不等于实现证据。来源缺失、断链、冲突、迁移未完回原 repair/澄清，不能推定完整采用。

Task 隔离贡献，shared current 仅由原 promotion owner 写入。独立 Phase2 先比较旧 authority、完整候选及拟写内容，原 owner 按 expected-current 晋升并核对实际写入，随后最终 Check/commit/独立完整 Review。无关 CURRENT/ref 推进不强迫旧 Task 改选版本；真实 scope/依赖/方案变化回原 owner。具体合同及恢复只由原 Skill 定义。
