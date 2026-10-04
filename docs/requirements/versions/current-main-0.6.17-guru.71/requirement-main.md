# Guru Team 当前需求：reference-only 创建

版本：`current-main-0.6.17-guru.71`；状态：`active`；predecessor：`current-main-0.6.17-guru.70`。本版以薄继承保留[不可变前驱的完整合同](../current-main-0.6.17-guru.70/requirement-main.md)；未由本版显式替换的 requirement/design/test、owner、边界、NFR 和 trace 全部继续有效。前驱版本身份、旧 source pin、历史计数与验证结果仅表示当时快照，当前版本事实以下文为准。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.71` / `active`。

当前 source：`castbox/Trellis@9c36002a324c16a09a85b6aa5a380b74aabf801f`，main CI `37179218822`，CLI/core `0.7.0-castbox.1`，extension `0.7.0-guru.1`。知识版本不是软件版本；历史 repository 目标 `v0.6.17-guru.2` 未在本次发布，后续发布范围归 #489。

## R490-01

Guru 正式创建入口必须支持 Issue 的 `exact_source` 和 `reference_only`；创建、结果恢复和 source identity 返回同一 repo、number、disposition、TaskId、generation 与 TaskRef。不得另造 source writer。

## R490-02

安装和当前 source projection 使用上述已合并 Fork；正常官方生成和 canonical preset 管理的副本必须同步，同一安装不可混用旧来源。

## R490-03

保持 `no_issue`、`exact_source`、session、branch/checkout/resource ownership 和 Closure 合同。引用来源不授予关闭来源 Issue 的权限；`follow_up`、`parent` 不进入新任务创建能力，历史任务不迁移。

## R490-04

通过正式 wrapper/writer/recovery、当前 lifecycle 与 Closure 回归、source/installed/platform projection、一个代表性 clean/current-update/reapply 和零 sidecar 验证本范围。远端 marketplace、native-host 全矩阵、前驱拒绝无写证明和 release proof 由 #489 独立承担。

设计与测试双向引用见[本版 trace](./traceability.md)。来源是已独立审查的[#490 contribution](../../../requirements-design-test-contributions/490-reference-only-adoption/requirements.md)；本版取代其 current authority 角色，贡献作为历史来源保留。
