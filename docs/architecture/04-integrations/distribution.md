# INTEGRATION

- `ARCH-INT-001`：canonical registry/interface/schema/runtime 经 preset inventory 投影到 dogfood 与平台 Skills；version/mode/bytes 必须一致。
- `ARCH-INT-002`：Trellis marketplace 通过 `trellis/index.json` 与 workflow id `guru-team` 暴露；preset 在 workflow 安装后补齐 runtime/platform assets。
- `ARCH-INT-003`：Git/GitHub 是 base、Issue、PR、merge、release live facts provider；Task archive 仅保留 closeout history，不替代 live provider。
- `ARCH-INT-004`：RDT 只消费 Architecture public locator/version/status；Bootstrap 只消费两个 child owner 的 minimal schema-validated result。
- `ARCH-INT-005`：`get_context.py` 从 `.trellis/spec/**/index.md` 提供 Agent 读取入口，但 projection 不复制 authority 正文。
- `ARCH-INT-006`：每个 declared platform cell 同时安装 shared `.agents` public projection 与唯一 selected platform projection；package-private validator scripts 不分发到平台 roots。
