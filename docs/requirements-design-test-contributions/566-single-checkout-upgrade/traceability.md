# #566 双向承接

| Requirement / Behavior | Design / Contract | Test / Scenario |
| --- | --- | --- |
| [R566-01 / BEH566-01](./requirements.md) | [D566-01 / CON566-01](./design.md) | [T566-01 / SCN566-01](./test.md) |
| [R566-02 / BEH566-02](./requirements.md) | [D566-01/02/03](./design.md) | [T566-02/03](./test.md) |
| [R566-03 / BEH566-03](./requirements.md) | [D566-03/04](./design.md) | [T566-04/05](./test.md) |
| [R566-04 / BEH566-04](./requirements.md) | [D566-04/05](./design.md) | [T566-04/05](./test.md) |
| [R566-05 / BEH566-05](./requirements.md) | [D566-06 / CON566-06](./design.md) | [T566-06 / SCN566-06](./test.md) |
| [R566-06 / BEH566-06](./requirements.md) | [D566-01/02/06](./design.md) | [T566-03/07](./test.md) |

反向读取同表：每个D/CON和T/SCN均回指其唯一当前Requirement；实现点由canonical package/runtime实际位置承接，test.md拥有结果。Architecture继承 `docs/architecture/README.md` / `.90/active`，本Task贡献与ADR尚未晋升shared-current。
