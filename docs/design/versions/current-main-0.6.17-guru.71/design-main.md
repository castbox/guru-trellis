# Reference-only 创建设计

版本：`current-main-0.6.17-guru.71`；状态：`active`；predecessor：`current-main-0.6.17-guru.70`。本版以薄继承保留[不可变前驱的完整合同](../current-main-0.6.17-guru.70/design-main.md)；未由本版显式替换的 requirement/design/test、owner、边界、NFR 和 trace 全部继续有效。前驱版本身份、旧 source pin、历史计数与验证结果仅表示当时快照，当前版本事实以下文为准。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.71` / `active`。

## D490-01

既有 C6 `task-creation-input.schema.json` 直接采用两值 enum；现有 Guru creator 将 reviewed source 原值交给 official `task.py create --no-start`，恢复和 reader 按原 owner 校验同一 identity。保持单 writer、既有 public entry 和 lifecycle graph。

## D490-02

canonical source lock 固定 `9c36002a324c16a09a85b6aa5a380b74aabf801f`，tree `1eb0dc446bb8b8f122db771e00a7004b48eaf4d8`，ordered parents `64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac`、`505d853cbc90db050f135cf0cc8f81f36e434e18`，CI `37179218822`。实际 built Fork CLI 负责 official template/hash generation；preset 只同步 Guru-owned 投影。未改变官方文件 ownership。

## D490-03

Closure 从 current source disposition 判断关闭权限；reference-only/no_issue 不调用 close provider。fixture 使用 current official writer；旧 metadata 仍只读拒绝，不增加 normalization/legacy runtime。

## D490-04

Architecture 与 RDT 各自从 expected `.70` 串行晋升到 `.71`；完整前驱正文通过明确链接继承，当前增量归本版。promotion-created diff 必须 fresh Phase 2、Task Commit 与不同独立 reviewer 的完整 Branch Review，才可进入 Delivery。

[R490 -> D490 -> T490 双向 trace](./traceability.md)；source contribution 见[#490 design](../../../requirements-design-test-contributions/490-reference-only-adoption/design.md)。
