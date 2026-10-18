# #331 D1 实施与验证计划

## 1. 输入与引用

整体范围是 Task root PRD / accepted_scope；本批 PRD 第4–6节定义9场景和AC331-01..10。`design.md` 第3节是唯一来源设计处置；第4–7节定义原 owners、完整单元、迁移与兼容；第8节在首次实施前固定24次 native 对照及成本判据。候选 Architecture baseline_current 是 `.100`、constitution-v1、legacy_boundary_convergence；它不是 final_plan 或实施通过。

实施前完整加载原两维护 Skill、通用 current-knowledge 合同、实际变更 specs、官方 Trellis 扩展文档。共享正文合同及适用 planning templates 由官方 add-context 加入 implement/check manifest。版本 authority、ADR-028/030、change-contract 约束实施与晋升；公共 Skill I/O 保持原样。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、owner 与实际文件 | 行为、产物与完成观察 |
| --- | --- | --- |
| I331-01 | 本计划批准/Activation；主会话协调 Test 方法 | 固定 design 第8节问题/必答表；从 B 建立原始对照语料和临时独立会话工作区，先运行旧侧；原始 trace 只暂存 repo 外。 |
| I331-02 | I01；Trellis implement worker，canonical 两 package/workflow/spec/preset 文案 | 建立唯一 reusable current-knowledge 合同；日常 profiles 实际接入；补迁移指引；不新增 runtime API/解析器。 |
| I331-03 | I01；文档实施 worker，三层 current/ 与隔离 RDT contribution | 逐条读取真实前驱，写至少三个完整 R/D/T 单元、薄导航和迁移对应；保留 stable ID、关联、来源和未迁移 legacy 清单。暂不晋升共享 README。 |
| I331-04 | I01；Architecture 实施 worker，generic baseline/project stack selection/governance proposed targets | 写实际版本化通用源及项目投影；按既有 owner 修订晋升治理的完整 current；提供真实 proposed delta，不改旧快照。 |
| I331-05 | I02–04；主会话与实际 Test owner | 原 Apply 同步 dogfood，定向 tests、漂移和 installed clean/update/reapply；运行新侧全部样本，与旧侧同口径审查；记录首次失败和修复。 |
| I331-06 | I05；fresh Architecture reviewer，原 RDT/Architecture owners | 独立 Phase2 读完整 tracked/untracked candidate/proposed promotion targets；晋升 `.110/.101`，核对写入适用性；完整最终 Check。 |
| I331-07 | I06；原 Commit/Review/Delivery owners | exact staging commit、fresh committed Architecture/full Branch Review、Delivery readiness、publish、merge；任何返工回最早受影响 owner。 |
| I331-08 | 已验证 delivered；原 Completion/Closure/Finish/Cleanup | 对整体10项AC逐项审查，完成源 Issue disposition、归档与已授权资源收尾，live 验证远端结果。 |

Workers 按文件归属隔离，不撤回他人改动。主会话负责 planning/spec、整合、提交及最终收尾。每个写批次先执行 task checkout boundary check。文件责任可以在同一原 owner 内细分，不产生第二生效 authority。

## 3. 验证入口、输入与预期观察

V331-A..D 的问题、必答事实、3次 old/new 重复及每组判据唯一见 design 第8节。入口是原 `codex exec --ephemeral` 日常读取/修订任务，query 使用 read-only，revision 使用 workspace-write；固定相同模型/配置、工具权限和起点。每个会话只看本侧材料。Test owner 从原始 events 读取 actual usage/工具内容/实际文件改动，逐次做语义判断，不以脚本评分替代。

V331-E：按实际源 inventory 执行两维护 package 的 contract/runtime focused tests、现有 package/source validator、workflow 分发检查、变更 Markdown 引用和旧版本字节检查。AI 核对完整定义、9场景及迁移清单；命令成功只证明其客观范围。

V331-F：`bash trellis/presets/guru-team/scripts/bash/apply.sh --repo .`，随后 `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。一个代表性临时 clean repo 通过同一匹配源的完整 installer 安装，再以旧匹配安装为起点更新/reapply，核对 package references 可读、workflow/skills/spec 一致、用户指令保留、逐个 sidecar 处理和零漂移。具体受支持 argv 先读当前 apply --help/README。不用修改上游/global node_modules，不执行完整 Release 平台矩阵。

唯一长期 Test 结果包含全部24次样本结果、实际加载字节/步数/总input及cached tokens/maintenance paths、首次失败修复、迁移核对、tests/安装证据和未验证边界。分组中位和每次正确性同时报告；错误/漏条件不以成本抵消。首次迁移及维护导航成本另报，不将其隐藏在自动注入。

## 4. 停止条件与适用回退点

真实需求/来源角色改变回 Clarify；候选机制改变回 Author candidate/独立 Architecture，执行修复留在原 Phase2 owner。缺少必要源或实验环境时停止对应依赖并明确未验证，继续独立可做的工作；不得报告通过。旧侧不足以取得完整答案则保留失败，修复双方起点/必要来源后同口径重跑，不能只给新侧答案。

迁移冲突保留旧 authority 和未完成标记，由原 repair 判断；未切换候选可在本 Task 范围内修订。晋升后修正通过原维护/新 successor，不改历史。Git/GitHub 副作用继续由其原 owner 处理。保留无关 worktree/dirty。无生产配置或业务数据，故无生产回滚步骤。

## 5. Delivery Policy（唯一）

`full`：本批覆盖 Task accepted_scope 的全部 AC331-01..10，无延期功能或验收。完成条件为完整单元/两层基线实际采用、9场景多次真实对照、migration/installed/reapply 证据、原 gate 和远端交付均满足。任一缺口仍是本批未完，不能转为无依据 follow-up 宣称全量交付。Delivery 合并后由原 Completion 对整体范围另作结论，再 Closure/Finish。

## 6. Docs SSOT Plan（唯一）

`delta_first`：先在 `docs/requirements-design-test-contributions/331-current-effective-knowledge/` 写 R331/BEH331→D331/CON331→T331 完整差额及 Test 结果，由原 RDT writer 在最终 Phase2 前 reconciliation/promotion，consumer 是完整当前单元/三层 successor。Architecture 同期写实际 contribution 和必要 ADR-031，原 owner 在独立 Phase2 后、最终 Check 前按 `.100` expected-current 晋升 `.101`，consumer 为最终 Check/committed Review/Publication。RDT proposed `.110` 引用实际 Architecture public identity。无在 Planning 直接晋升共享导航。

命中来源与差额见 design 第9节：三层 `.109`/historical contributions、Architecture `.100`/ARCH-GOV-008/009/ADR-028/030、canonical maintenance Skills/workflow/spec。新 reusable 合同由唯一 source 分发；dogfood 不是长期源。完整历史语料不会在此轮全部迁移，未迁移的范围及旧 Task 适用边界须在新导航清楚列出；这不削减本批代表性实际采用和全部验收责任。
