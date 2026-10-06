# 迁移能力 inventory

版本：`current-main-0.6.17-guru.72`；状态：`active`；predecessor：`current-main-0.6.17-guru.71`。完整继承[不可变前驱合同](../current-main-0.6.17-guru.71/capability-inventory.md)；除下文明确修订的独立迁移边界外，既有 requirement/design/test、无人员模型、source disposition、owner、历史拒绝边界、NFR 与 trace 继续有效。前驱 source、计数和证据只表示历史快照。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.72` / `active`。知识版本不是软件发布。

registry：35 active packages / 159 package exits / 106 commands，零 planned。新增 `guru-upgrade-installation` 为 standalone-only，不加入 business graph；production 仍为 33 mandatory invokes / 153 exits。当前 extension `0.7.0-guru.2`、CLI/core `0.7.0-castbox.2` 为未发布候选，源 lock 见 [canonical source](../../../../trellis/presets/guru-team/source/trellis-source.json)。旧 inventory 计数只属历史。
