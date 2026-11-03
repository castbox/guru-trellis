# Codex Guru Skill 发现与迁移

Identity：RDT-REQ-CODEX-DISCOVERY；来源：https://github.com/castbox/guru-trellis/issues/724。
设计关系：RDT-DES-CODEX-DISCOVERY；测试关系：RDT-TST-CODEX-DISCOVERY。

## R724-01 / BEH724-DISCOVER：单一项目发现根

Codex 的项目级 Guru 公共 Skill 从 .agents/skills/<id>/ 发现。新安装和正常 reapply 不生成受管 .codex/skills/guru-*/。公共文件集合、内容和可执行位保持原分发合同，私有 runtime、执行器、tests 和运行证据沿原 owner 管理。

## R724-02 / BEH724-SELECT：平台适用性

目标安装的 exact platform selection 包含 codex 时，共享根安装 Codex 专属编排包及 agents/openai.yaml；未包含时不新增这些包。共享根去重不改变 platform_destinations、显式调用策略和 Codex 原生能力前置。移除 codex 时按原受管规则退出专属公共文件，保留其它所选平台需要的共享包、平台副本和用户内容。升级不从 source checkout 推断目标选择。

## R724-03 / BEH724-MIGRATE：已有安装退出旧根

正式维护 owner 核对目标公共投影的完整集合、内容、mode 和无未解决冲突后，才按旧 previous managed provenance 移除未修改旧文件及其派生空目录。旧路径不作为 current 分发根、claim 或必要 inventory；重试/reapply 不恢复退役投影。

## R724-04 / BEH724-CONFLICT：两端内容保护与恢复

旧根和目标共享根的用户修改、未知来源文件都保留并沿原冲突处置。不能用 canonical 或旧副本直接覆盖目标。目标冲突解决前保留仍需迁移的旧受管副本。残留副本造成重复发现或冲突未解决时不能报告迁移成功；原恢复操作处理具体冲突并重试。

## R724-05 / BEH724-NATIVE：真实发现与公开调用

依据当前声明和官方文档确定客户端、版本与发现机制分组。相同机制的入口说明代表性依据；不同机制的受支持入口补定向 native 证据。在目标 Skill 无旧副本条件下，以原公开入口实际调用公共 Skill 和专属编排包并观察合法出口，记录宿主/版本/入口和结果。目录扫描、聊天 Skill 清单或模拟加载不能代替。专属包原生能力前置保留；合法能力不足出口不等于真实业务编排成功。

若发现受支持宿主仍依赖旧根，记录具体依赖并解决承接后再移除其旧投影。缺必需 native 证据时保留对应验收未验证，不宣告本需求完整完成。

## R724-06：范围和兼容边界

保持公共 Skill id、行为和出口；保留 .codex 的 config、agents、hooks 和 prompts 职责及 Claude/Cursor 平台根。不清理用户级、第三方或上游文件。只覆盖正常安装、升级、平台选择、冲突及恢复；一个代表性 clean 安装属于本项，完整多平台 Throwaway/Release Gate 另有 owner。

完整公共资产与维护细则读 canonical spec/workflow/skill-package-contract.md 的 Distribution And Managed Hashes、项目 .trellis/spec/preset/installer.md 和 trellis/presets/guru-team/MIGRATION-724.md。这里定义本能力的行为和条件，不复制脚本执行协议。知识晋升不证明安装、native 调用、软件发布或业务采用已完成。
