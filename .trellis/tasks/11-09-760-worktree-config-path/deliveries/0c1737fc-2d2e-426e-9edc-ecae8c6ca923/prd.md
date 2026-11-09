# #760 D1 配置驱动 worktree 路径修复

## 1. 整体来源与术语

整体权威：`.trellis/tasks/11-09-760-worktree-config-path/prd.md`，accepted_scope `sha256:529a525ba2852f44c16cb504941926153f35a7cf4c4bc4b19b49b4fe261bb97d`；Direct Source：https://github.com/castbox/guru-trellis/issues/760 完整正文。D1 scope_ref 选择整体第5节行为与第7节验收，planning_root 为 `.trellis/tasks/11-09-760-worktree-config-path/deliveries/0c1737fc-2d2e-426e-9edc-ecae8c6ca923`。primary/生成root定义使用整体第1节。

## 2. 整体与本批目标、非目标

全量D1恢复两个新建入口的项目配置路径承接。环境查询、计划、创建和直接后继一致；显式新位置和既有采用/恢复合法。排除Codex清理设置、业务恢复、暖池、prunable维护和完整Release矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

无前序Delivery。固定开发基线B=8c158381b5bdb61fd961cbb89e23c2d1f659c9aa，目标main；当前create-task直接消费checkout_root，environment回退调用root.parent，task-free沿普通Git。原Task acquisition、绑定、资源归属与恢复能力复用。D1承担全部实现和验收；合并后原Completion审核整体范围，Closure与Finish独立执行。

## 4. 本批调用方、场景与流程

S1：从primary/linked/detached调用，读取同一项目primary配置；空root采用primary父目录/repo-name-worktrees，相对root对primary解析，绝对root直接采用。
S2：AI选择配置生成新位置并审命名，经同一解析事实得到计划，正式Task原acquisition或task-free普通Git执行；实际目录、注册和后继读取一致。
S3：正常计划路径与配置解析不符时，创建任何branch/worktree/Task前诊断，原owner修正后继续。
S4：真实显式新位置仍合法；已有外部checkout采用与原Task恢复保持位置、身份、generation、绑定及资源归属。

## 5. 完整行为、条件与约束

- 配置驱动的新建位置以同一 Git common-dir 下、由 live Git topology 确认的主仓库为项目锚点，读取该项目的 .trellis/guru-team/config.yml。空 worktree_root 使用 <主仓库父目录>/<主仓库名>-worktrees；绝对配置直接采用；相对配置相对主仓库根解析。未改变项目配置或显式位置选择时，从 primary、linked 或 detached checkout 调用得到同一生成 root。不能仅取调用 cwd.parent，也不能假设 common-dir 的父目录必然是主仓库。配置来源、项目锚点或位置选择有真实冲突时，给出原 owner 可处理的准确诊断，不自动覆盖各 checkout 的配置。
- AI 先读取该项目配置和 live Git topology，再在原 Skill 内判断新建或采用、命名、范围、冲突处置及副作用计划。脚本只负责确定性路径解析、创建前一致性验证与 Git 动作，不新增脚本语义规划器。
- 配置驱动的新建路径由生成 root 与本次已审命名形成。环境查询、计划中的路径、实际 Git 创建和后继 consumer 使用同一解析事实。正式 Task 继续通过原 acquisition/checker/binding；task-free 继续由自身 owner 使用普通 Git 并复核位置适用性，不创建 TaskId、TaskBranchBinding、Task session、task.json 或新位置映射。不得把 Codex 当前工作目录、相邻已有目录或示例路径当作配置替代。
- 区分三种位置来源：按配置生成新位置、调用方显式选择新位置、采用或恢复已有 checkout。worktree_root 是生成位置合同，不是所有 checkout 的目录 allowlist。现有 public input 允许显式绝对 checkout_root，不能仅因它在生成 root 外就悄然改成非法。Planning 必须说明生成策略、显式位置选择与路径参数的可机器验证合同及旧调用迁移；AI 负责读取实际意图、选择策略和展示精确副作用，脚本不判断或记录用户授权。
- 在配置驱动的新建路径中，普通调用方计划与解析结果不一致时，须在创建 branch/worktree/Task 前准确诊断并回到原 owner 修正计划，不能静默换路径。真实显式新位置沿原兼容合同处理，不能从 AI 自行填入绝对路径反推用户要求该位置；显式项目配置也不能被通用“更安全目录”规则覆盖。采用已有 checkout、原 Task 恢复不受生成 root 限制，仍检查各自真实身份、绑定和位置适用性。
- 新配置解析不得改变已存在 TaskId、generation、branch binding、Delivery、session 或资源归属。恢复已有 Task 时按已验证绑定找原位置，不因默认目录变化搬移或重新创建。
- 复用现有 Skill 和 runtime ownership；确定性配置解析应有真实 consumer，不能只新增查询而不接入两个创建入口。公开参数或输出若需收敛，须在本项规划中明确兼容/迁移与受影响调用方，不静默改变既有语义，也不为 task-free 强加 Task-specific validator。workspace_mode: current 的历史存在不授权恢复现已退役的 primary 写入路径。不新增映射台账、审批链、平台专用清理进程或长期路径证明 artifact。


## 6. 本批验收、验证方式与未决项

- AC1：定向解析空、相对、绝对root；代表性primary及linked/detached得到相同生成root。
- AC2：正式Task公开创建入口和task-free原普通Git入口消费解析结果；真实Git创建观察计划、目录、注册、直接后继一致。配置生成路径不一致在首副作用前拒绝，纠正后可继续。
- AC3：保留显式新位置、已有外部checkout采用和原Task恢复；task-free无Task身份。采用适用旧回归证据补实际差额。
- AC4：命中package/runtime验证、canonical/dogfood投影同步、drift与sidecar核验。报告入口、观察和未验证边界。
没有需求未决项。配置策略与公开参数兼容细化进入设计，不以产品澄清阻塞。

## 7. Canonical 引用与本轮差额

RDT：docs/requirements/current/runtime-location.md、docs/design/current/runtime-location.md、docs/test/current/runtime-location.md 的独立身份与操作边界；本轮补新建路径配置承接。Architecture：docs/architecture/README.md、00-foundation/design-constitution.md、06-governance/change-contract.md；本轮设计须由独立owner评估。配置模板为trellis/workflows/guru-team/config-template.yml。原入口责任保留；公开参数迁移与原新建consumer细化于design第3节。
