# 能力 inventory 继承

版本：`current-main-0.6.17-guru.71`；状态：`active`；predecessor：`current-main-0.6.17-guru.70`。本版以薄继承保留[不可变前驱的完整合同](../current-main-0.6.17-guru.70/capability-inventory.md)；未由本版显式替换的 requirement/design/test、owner、边界、NFR 和 trace 全部继续有效。前驱版本身份、旧 source pin、历史计数与验证结果仅表示当时快照，当前版本事实以下文为准。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.71` / `active`。

registry 保持 34 active packages / 155 package exits / 104 commands，零 planned；production workflow 保持 33 mandatory invokes / 153 exits。现有 `guru-create-task` 增加 reference-only Issue creation，不新增 Skill、exit、command、source 概念或 owner。当前能力语义按本版 D490 与继承合同解释；旧 inventory 中的 historical/planned 状态不回到 current graph。
