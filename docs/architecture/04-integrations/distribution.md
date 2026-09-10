# INTEGRATION

- `ARCH-INT-001`：canonical registry/interface/schema/runtime 经 preset inventory 投影到 dogfood 与平台 Skills；version/mode/bytes 必须一致。
- `ARCH-INT-002`：Trellis marketplace 通过 `trellis/index.json` 与 workflow id `guru-team` 暴露；preset 在 workflow 安装后补齐 runtime/platform assets。
- `ARCH-INT-003`：Git/GitHub 是 base、Issue、PR、merge、release live facts provider；Task archive 仅保留 closeout history，不替代 live provider。
- `ARCH-INT-004`：RDT 只消费 Architecture public locator/version/status；Bootstrap 只消费两个 child owner 的 minimal schema-validated result。
- `ARCH-INT-005`：`get_context.py` 从 `.trellis/spec/**/index.md` 提供 Agent 读取入口，但 projection 不复制 authority 正文。
- `ARCH-INT-006`：每个 declared platform cell 同时安装 shared `.agents` public projection 与唯一 selected platform projection；package-private validator scripts 不分发到平台 roots。
- `ARCH-INT-007`：项目 Architecture check 通过 current descriptor/result identity、applicability、rule/decision/GAP refs、before/after、evidence/unavailable reason 与 freshness 接入 semantic owner；公共 runtime 只校验一一绑定和 route consistency，不执行或解释项目语义。
- `ARCH-INT-008`：installed manifest 的 immutable `repo/ref/commit` 只定位 extension source；canonical
  apply 以 `--repo target_reviewed_checkout` 写 target，postimage 分别验证 target lineage 与 extension
  provenance。不得解析 mutable main、PATH/global package、hidden checkout 或 legacy fallback，也不
  引入 verifier lifecycle edge。
- `ARCH-INT-009`：仓库私有正式发布入口通过既有 owner 的 declared typed result 串行连接 preparation
  与 post-merge exact candidate；PR/Release payload 从 live Issue、exact diff、当前验证与 candidate
  identity 即时生成。owner-private lifecycle metadata、授权和阶段状态不进入 tracked handoff，任何
  delivery、durable docs、配置、schema、script 或 test 变化仍使对应 owner evidence stale。
- `ARCH-INT-010`：normal-scenario 与 solution-mechanism qualification 在同一 caller candidate boundary
  分别执行；机制 owner 的 `mechanism_revision_required` 只返回原 owner remove/replace，不能变成 scope
  confirmation。canonical/installed/platform projections 保持同一 package identity。
- `ARCH-INT-011`：Merge 的 `phase2_reentry_required` 只投影最小 PR/task/archive/finding identity 到
  `guru-restore-archived-task`；恢复 owner 不创建替代对象，不复用旧 check/review/publication/finalization
  authority，并只把 `restored_to_phase2` 交给 Phase 2 consumer。
- `ARCH-INT-012`：installer、source/installed validator、compatibility matrix、throwaway、runtime/eval 与
  platform projection 从每个 package Interface 读取唯一 public wrapper path，验证 exact bytes/mode/launcher
  与 private-script leak；`restore-archived-task.sh` 证明该合同不依赖 `invoke.sh` 文件名。
- `ARCH-INT-013`：Finalizer `base_reconciliation_required` output 通过声明的 consumer seed/projection 把
  prior `branch_review_commit` 与 exact task/base identity 投影到 Reconcile；确认后的 package-private executor
  只创建 expected-head local reconciliation commit。Review Branch bounded continuity 分离验证 prior/current
  anchors、base ancestry、candidate tree 与 affected paths，再把 current HEAD 投影给未放宽的 Publication
  reviewed-content gate；task content、scope 或 authority 变化仍回到 Phase 2 与完整 Branch Review。

## Capability 与 installation consistency 边界

- `ARCH-INT-014`：框架与扩展来源分离：`trellis/presets/guru-team/source/trellis-source.json`
  是唯一框架来源记录，preset 仅投影到 `.trellis/guru-team/trellis-source.json`。
  README 准备链与 verifier 使用显式 checkout、固定 SHA 和 Fork 自身构建/Node bin；
  失败不回退到原 npm 包或全局 CLI，不复制 dist、不新增 launcher 或打包分发系统。
  full 历史验证需独立 predecessor checkout/SHA；focused 只证明当前 candidate 场景。

- Capability-loss gate 只比较 `workflow`、`task_data`、`docs_authority`，用于判断升级前后
  用户可观察 workflow capability 是否丢失。
- `skill_api` 与 interface/schema/command projection、distribution、managed/installed file
  inventory、mode、template hash、sidecar、声明平台 parity 及 extension identity/version
  binding 属于独立 consistency/installation gate。任一不一致仍 fail closed 并阻塞 release，
  但其变化本身不构成 capability loss。
