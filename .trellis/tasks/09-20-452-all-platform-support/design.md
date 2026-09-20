# #452 技术设计

## 1. 设计目标

先恢复可消费的共享 Architecture/RDT authority，再建立两层平台模型：pinned upstream `AI_TOOLS` 完整集合拥有“所有平台”语义，目标业务仓库 installed manifest 拥有该仓库升级时的 exact selection。Claude/Codex/Cursor 只是无参数新安装的缺省值，也是 guru-trellis 当前 dogfood selection；它们不构成第三层 capability inventory。

## 2. `.57` #443 promotion 与 `.58` #452 RDT promotion

当前共享 authority 存在两个前置缺口：`.trellis/spec` 仍指向 `.55`，而 Docs current 为 `.56`；同时 `.56` 只承接 #436 的 31/136/101 状态，未吸收已经完成并关闭的 #443 capability 与 live 32/142/102 registry。该状态无法支撑 #452 的 Phase 2 before/after 判断。

本任务在当前分支执行一次串行 promotion：

- 以 `.56` 为 immutable predecessor，新建 `current-main-0.6.17-guru.57` Requirements/Design/Test version；
- 将 #443 contribution 提升为 `reviewed_promoted`，补齐 task identity/session binding 的 current owner、integration、GAP/exit、evidence、ADR 和双向 RDT traceability；
- 更新 Architecture current/readme/evidence/governance 导航与 RDT README/manifest，使 32 packages / 142 exits / 102 commands 成为 `.57` current 事实；
- production workflow 继续为 22 mandatory invokes / 98 exits，#434 graph activation 保持独占且未执行；
- 同步 `.trellis/spec` 的 Architecture/RDT/public-doc projection 到 `.57`；
- promotion 后所有旧 Planning/Phase 2 结果 stale，必须重新进入 fresh gate。

在平台合同收敛后，#452 task-owned RDT contribution 以 `.57` 为 immutable predecessor
提升为 `.58/active`；Architecture shared current 保持 `.57/active`，对应 #452 Architecture
contribution 保持 `reviewed_candidate`，等待实现后 committed full-diff review 与 serialized promotion。

## 3. 平台能力模型

引入一个 preset-local inventory 与一个 target-local selection：

- `upstream_platforms`：pinned upstream registry 声明的全部 canonical `AITool` id、唯一 public `cliFlag`、template/root 与 native entry；当前共 22 个；
- `inventory_source`、`inventory_version` 与 digest：绑定固定 Trellis commit 和 `AI_TOOLS` 内容，防止“所有平台”随 ambient checkout 静默变化；
- `selected_platforms`：目标仓库 manifest 中以 registry `cliFlag` 表示的非空、排序、去重 exact installed selection；每个值必须唯一映射回一个 upstream `AITool` id，install、skill packages 与 overlays/projection records 必须对同一选择达成一致；
- `default_platforms`：仅用于两种 flag 都省略的新安装入口，固定为 Claude/Codex/Cursor，不参与 capability 分层。

重复 `--platform <cli-flag>` 形成显式 exact subset；未提供该参数时使用 `default_platforms`。公开 parser 不再声明 `--all-platforms`，installed manifest 和 installer JSON 也不再记录对应布尔状态。不存在 `guru_supported_platforms` 或 `deferred_platforms`。

升级 owner 必须从目标仓库 current installed manifest/provenance 读取 exact `cliFlag` selection，并始终投影成重复 `--platform <cli-flag>`。升级不得因为 selection 等于默认集合或完整 upstream 集合而改写其来源语义，也不得从 source checkout 当前安装了哪些平台推断目标仓库选择。

## 4. OpenCode projection

OpenCode 作为 upstream 22 平台之一加入完整 projection：

- canonical platform root 与 `.opencode` native discovery/command path；
- `platform_destinations`、registry/manifest、skill projection 和 ownership claim；
- executable mode、public contract、package-private `tests/` 排除；
- installer shrink/reapply/update 的 previous managed hash、`.new`/`.bak` 和 removal provenance；
- compatibility matrix 的 root/path parser/init/actual-load adapter；
- throwaway helper 的 explicit `--platform opencode` 路径和 clean/existing/reapply/update 断言；
- actual-load smoke，不以目录存在或静态内容匹配替代真实 native entry discovery。

其余 upstream 平台同样必须从 registry 解析 native destination 和 entry form，并可通过重复 `--platform` 显式选择。不同平台可以拥有不同 discovery/command surface；实现和 ownership cardinality 从显式 projection descriptor 计算，不能把“平台数”直接等同于 active dogfood overlay 数。OpenCode 的真实 actual-load 仍作为本 Issue 的代表性 native probe，不把静态目录存在冒充平台加载成功；其余 21 个客户端的 native compatibility 直接继承 pinned `castbox/Trellis` 测试权威，本仓不重复逐平台执行。

## 5. Dogfood 与升级保真

guru-trellis 的 dogfood manifest 固定选择 Claude/Codex/Cursor。仓库 reapply 使用三个重复 `--platform` 参数，drift checker 从 current dogfood manifest 读取 selected set，只比较 shared assets 与这三个平台的 installed projection；canonical inventory 中存在 OpenCode 或其他平台 projection 不要求它们出现在 dogfood checkout。

业务仓库升级使用同一保真机制：先验证 install、skill package 与 platform projection selection 一致，再将 exact ordered set 传给 preset。missing、空集合、重复、unknown、列表不一致或 provenance stale 均在写目标仓库前 fail closed。

## 6. 变更边界

Authority promotion 变更集中在 `docs/architecture/`、`docs/{requirements,design,test}/`、#443 contribution 和 `.trellis/spec/{architecture,docs}/`；平台实现集中在 `trellis/presets/guru-team/` 的 installer、ownership、compatibility/throwaway scripts、tests、README，以及 `.trellis/spec/preset` 和 `.trellis/spec/workflow/quality-guidelines.md`。canonical/installed/platform package projection 统一通过已有 preset apply/reapply 机制同步，不手工维护独立副本。

本任务会实质修改的 `apply_guru_team_trellis_preset.py`、`verify_trellis_compatibility_matrix.py` 与 `test_apply_guru_team_trellis_preset.py` 当前均接近 3000 行。实施在增加全平台逻辑或测试前，必须先做 AI 审查的机械拆分或小型解耦：inventory/selection 解析进入独立模块，compatibility descriptor/adapter 辅助逻辑从 matrix 主文件分离，新增平台选择测试进入独立 test module；所有 touched non-generated Python 文件在最终候选中保持不超过 3000 行。

不修改 `trellis/workflows/guru-team/` 的 Task Delivery Lifecycle，不触碰 #434 production graph，也不修改上游 Trellis 源码。`.57` promotion 只吸收 #443 已交付 capability；平台 projection 扩展不激活任何 deferred production package。

## 7. 失败与兼容策略

- `.57` 任一 Architecture/RDT locator、版本、trace、registry cardinality 或 #443 owner/exit/evidence 不闭合：promotion fail closed；
- `.57` 意外改变 production 22/98 graph、提前消费 #434 routes 或把 #443 binding 当作 tracked/public authority：阻止 promotion；
- upstream inventory 缺失、来源无法解析、digest 不一致、平台 projection descriptor 缺失或声明与实际 projection 不一致：fail closed；
- `--platform` 指向 upstream inventory 外的平台：argparse fail closed；任一 upstream 平台缺少 required projection 时，该平台显式安装失败，不得降级为 deferred success；
- 旧 `--all-platforms` 参数：argparse 作为未知参数失败且目标仓库零写入；
- 业务仓库升级 selection 缺失、非法或跨 manifest section 不一致：在 preset apply 前 fail closed；
- reapply 遇到未知本地修改：保留本地文件，生成 `.new`，记录 conflict，不静默覆盖；
- 无平台参数安装 Claude/Codex/Cursor；显式平台集合只能通过重复 `--platform` 表达；guru-trellis dogfood reapply 始终显式保留三平台。

## 8. 验证策略

按风险分层执行：

1. Architecture/RDT：Architecture `.57/active`、RDT `.58/active`、immutable predecessor、#443/#452 trace、ADR/evidence、32/142/102 registry 与 22/98 production boundary；
2. installer/ownership/unit：22 平台 inventory、重复 `--platform`、旧 `--all-platforms` 拒绝、三平台默认值、manifest selection、mode、private tests 排除和 unknown fail-close；
3. canonical/installed/platform：descriptor、完整 selection 与任意 exact subset 的 apply、reapply、update、sidecar/removal provenance 和 byte parity，不调用 22 个外部平台客户端；
4. OpenCode actual-load：真实 `.opencode` entry discovery/command invocation；
5. upgrade preservation：单平台、任意 subset、三平台 dogfood 与完整 22 平台 selection 均按 exact repeated `--platform` 保留；
6. dogfood：guru-trellis manifest 和 drift 只消费 Claude/Codex/Cursor，不要求 canonical 全平台全部安装到当前 checkout；
7. throwaway：一个代表性 clean install、三平台 dogfood与 OpenCode clean/existing/reapply/update 代表性 native probe；不提供全量安装模式，也不执行 22 平台 native matrix；
8. promotion 后 fresh Planning Architecture/RDT、Phase 2、Task Commit 与完整 Branch Review；
9. 仅在 Issue #452 contract 要求的范围内验证，不扩展为正式 Release/tag/GitHub Release。
