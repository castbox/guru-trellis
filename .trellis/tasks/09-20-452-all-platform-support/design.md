# #452 技术设计

## 1. 设计目标

先恢复可消费的共享 Architecture/RDT authority，再把“上游支持什么”“Guru Team 能交付什么”和“dogfood 无参数安装什么”从一个集合拆成三个有名字、有消费者、有验证边界的集合。平台集合的事实来源固定绑定上游 Trellis 当前 `AI_TOOLS` registry；Guru projection 由本仓库 canonical projection 的实际文件和能力校验产生；dogfood 只代表本仓库无参数 reapply 选择。

## 2. `.57` Architecture/RDT promotion

当前共享 authority 存在两个前置缺口：`.trellis/spec` 仍指向 `.55`，而 Docs current 为 `.56`；同时 `.56` 只承接 #436 的 31/136/101 状态，未吸收已经完成并关闭的 #443 capability 与 live 32/142/102 registry。该状态无法支撑 #452 的 Phase 2 before/after 判断。

本任务在当前分支执行一次串行 promotion：

- 以 `.56` 为 immutable predecessor，新建 `current-main-0.6.17-guru.57` Requirements/Design/Test version；
- 将 #443 contribution 提升为 `reviewed_promoted`，补齐 task identity/session binding 的 current owner、integration、GAP/exit、evidence、ADR 和双向 RDT traceability；
- 更新 Architecture current/readme/evidence/governance 导航与 RDT README/manifest，使 32 packages / 142 exits / 102 commands 成为 `.57` current 事实；
- production workflow 继续为 22 mandatory invokes / 98 exits，#434 graph activation 保持独占且未执行；
- 同步 `.trellis/spec` 的 Architecture/RDT/public-doc projection 到 `.57`；
- promotion 后所有旧 Planning/Phase 2 结果 stale，必须重新进入 fresh gate。

## 3. 平台能力模型

引入一个 preset-local capability inventory，字段固定为：

- `upstream_platforms`：上游声明的平台 id、template/root、native init/actual-load 入口；
- `guru_supported_platforms`：已具备完整 public projection、ownership、manifest、reapply/update、actual-load 和 throwaway 验证的平台；
- `default_dogfood_platforms`：无平台参数时 apply 选择的平台；
- `deferred_platforms`：上游已声明但 Guru projection 尚未完成的平台，包含稳定原因和后续入口；
- `inventory_source`：固定为 `castbox/Trellis@upstream/main:packages/cli/src/types/ai-tools.ts` 的 `AI_TOOLS` registry；
- `inventory_version` 与 digest：绑定验证输入，避免静默漂移。

`--all-platforms` 消费 `guru_supported_platforms`，无平台参数消费 `default_dogfood_platforms`，`--platform` 只接受 `guru_supported_platforms`。三者不能再共享 `ALL_PLATFORMS` 这个含义不清的别名。

## 4. OpenCode projection

OpenCode 作为完整支持平台加入：

- canonical platform root 与 `.opencode` native discovery/command path；
- `platform_destinations`、registry/manifest、skill projection 和 ownership claim；
- executable mode、public contract、package-private `tests/` 排除；
- installer shrink/reapply/update 的 previous managed hash、`.new`/`.bak` 和 removal provenance；
- compatibility matrix 的 root/path parser/init/actual-load adapter；
- throwaway helper 的 explicit `--platform opencode` 路径和 clean/existing/reapply/update 断言；
- actual-load smoke，不以目录存在或静态内容匹配替代真实 native entry discovery。

如果上游 registry 还有其他平台但当前无法提供上述完整链路，inventory 将其列为 `deferred`，测试其稳定拒绝/报告结果，而不是把它们加入 `--all-platforms`。

## 5. 变更边界

Authority promotion 变更集中在 `docs/architecture/`、`docs/{requirements,design,test}/`、#443 contribution 和 `.trellis/spec/{architecture,docs}/`；平台实现集中在 `trellis/presets/guru-team/` 的 installer、ownership、compatibility/throwaway scripts、tests、README，以及 `.trellis/spec/preset` 和 `.trellis/spec/workflow/quality-guidelines.md`。canonical/installed/platform package projection 统一通过已有 preset apply/reapply 机制同步，不手工维护独立副本。

不修改 `trellis/workflows/guru-team/` 的 Task Delivery Lifecycle，不触碰 #434 production graph，也不修改上游 Trellis 源码。`.57` promotion 只吸收 #443 已交付 capability，不把 deferred package 接入 production consumers。

## 6. 失败与兼容策略

- `.57` 任一 Architecture/RDT locator、版本、trace、registry cardinality 或 #443 owner/exit/evidence 不闭合：promotion fail closed；
- `.57` 意外改变 production 22/98 graph、提前消费 #434 routes 或把 #443 binding 当作 tracked/public authority：阻止 promotion；
- capability inventory 缺失、来源无法解析、digest 不一致或声明与实际 projection 不一致：fail closed；
- `--platform` 指向 upstream-only/deferred 平台：稳定返回 unsupported/deferred，非 argparse unknown；
- `--platform opencode` 但 projection/actual-load 不完整：阻止 staged activation；
- reapply 遇到未知本地修改：保留本地文件，生成 `.new`，记录 conflict，不静默覆盖；
- 无平台参数仍只安装 Codex/Cursor；显式 `--all-platforms` 不改变无参数行为。

## 7. 验证策略

按风险分层执行：

1. Architecture/RDT：版本、immutable predecessor、#443 trace、ADR/evidence、32/142/102 registry 与 22/98 production boundary；
2. installer/ownership/unit：集合、flag、manifest、mode、private tests 排除、unknown/deferred fail-close；
3. canonical/installed/platform：apply、reapply、update、drift、sidecar/removal provenance 和 byte parity；
4. OpenCode actual-load：真实 `.opencode` entry discovery/command invocation；
5. throwaway：clean/existing/reapply/update 的 OpenCode 代表性矩阵；
6. promotion 后 fresh Planning Architecture/RDT、Phase 2、Task Commit 与完整 Branch Review；
7. 仅在 Issue #452 contract 要求的范围内验证，不扩展为正式 Release 或全量升级矩阵。
