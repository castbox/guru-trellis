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

## Capability 与 installation consistency 边界

- Capability-loss gate 只比较 `workflow`、`task_data`、`docs_authority`，用于判断升级前后
  用户可观察 workflow capability 是否丢失。
- `skill_api` 与 interface/schema/command projection、distribution、managed/installed file
  inventory、mode、template hash、sidecar、声明平台 parity 及 extension identity/version
  binding 属于独立 consistency/installation gate。任一不一致仍 fail closed 并阻塞 release，
  但其变化本身不构成 capability loss。
