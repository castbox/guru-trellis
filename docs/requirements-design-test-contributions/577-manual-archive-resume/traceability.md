# #577 双向追踪

| Requirement / Behavior | Design / Contract | Test / Scenario / Issue acceptance |
| --- | --- | --- |
| [R577-01 / BEH577-01](./requirements.md) | [D577-01/03/04](./design.md) | [T577-01/04 / AC1/4](./test.md) |
| [R577-02 / BEH577-02](./requirements.md) | [D577-02/04](./design.md) | [T577-01/05 / AC1/5](./test.md) |
| [R577-03 / BEH577-03](./requirements.md) | [D577-01/03](./design.md) | [T577-03 / AC3](./test.md) |
| [R577-04 / BEH577-04](./requirements.md) | [D577-02/03/06](./design.md) | [T577-03/04/06 / AC3/4/6](./test.md) |
| [R577-05 / BEH577-05](./requirements.md) | [D577-01/03/04](./design.md) | [T577-02 / AC2](./test.md) |
| [R577-06 / BEH577-06](./requirements.md) | [D577-02/05](./design.md) | [T577-04/05 / AC4/5](./test.md) |
| [R577-07 / BEH577-07](./requirements.md) | [D577-04/06](./design.md) | [T577-01/02/06 / AC1/2/6](./test.md) |

反向读取同表：每项设计责任和测试都有具名需求consumer，没有额外平台矩阵或攻击模型义务。Architecture继承 `.97/active`；实际结果读唯一Test，不从Task阶段或旧gate推断。
