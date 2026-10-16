# #575 S1 双向 Traceability

| Requirement / Behavior | Design / Contract | Test | 内容源 |
| --- | --- | --- | --- |
| R575-S1-01 / BEH575-S1-01 | D575-S1-01 / CON575-S1-01 | T575-S1-01、02 | canonical source record、生产 source/build/API validators |
| R575-S1-02 / BEH575-S1-02 | D575-S1-02 / CON575-S1-02 | T575-S1-03 | 根/workflow/preset README、public-docs spec |
| R575-S1-03 / BEH575-S1-03 | D575-S1-01 / CON575-S1-01 | T575-S1-02、03 | 根 README 原构建入口、既有 fork preparation tests |
| R575-S1-04 / BEH575-S1-04 | D575-S1-03 / CON575-S1-03 | T575-S1-03、04 | 当前公开说明、原 maintenance/migration contracts |
| R575-S1-05 / BEH575-S1-05 | D575-S1-02、03 / CON575-S1-02、03 | T575-S1-04 | 本贡献与 task Architecture candidate、历史 Test 引用 |

测试反向覆盖：T575-S1-01→R01；T575-S1-02→R01/R03；T575-S1-03→R02/R03/R04；T575-S1-04→R04/R05。缩写 R01..R05 仅指本表的 R575-S1 identities。

整体 Task 的 R575-01..07 / A575-01..08 由本贡献和后续独立 `575-release-preparation` 差额共同承接；本 S1 不把未执行的 M/S2 验收标为通过。实际结果和未验证边界只由本目录 test.md 单写。Architecture 继承及本贡献状态见 manifest.yaml，不从 Task 生命周期或历史 release 推导当前完成。
