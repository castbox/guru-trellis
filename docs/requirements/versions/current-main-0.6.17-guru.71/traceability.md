# 需求双向 trace

版本：`current-main-0.6.17-guru.71`；状态：`active`；predecessor：`current-main-0.6.17-guru.70`。本版以薄继承保留[不可变前驱的完整合同](../current-main-0.6.17-guru.70/traceability.md)；未由本版显式替换的 requirement/design/test、owner、边界、NFR 和 trace 全部继续有效。前驱版本身份、旧 source pin、历史计数与验证结果仅表示当时快照，当前版本事实以下文为准。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.71` / `active`。

| Requirement | Design responsibility | Test strategy/case | Architecture / evidence |
| --- | --- | --- | --- |
| [R490-01](./requirement-main.md#r490-01) | [D490-01](../../../design/versions/current-main-0.6.17-guru.71/design-main.md#d490-01) | [T490-01](../../../test/versions/current-main-0.6.17-guru.71/test-strategy.md#t490-01), [T490-02](../../../test/versions/current-main-0.6.17-guru.71/test-strategy.md#t490-02) | ARCH-CUR-048 / ARCH-DOM-033 |
| [R490-02](./requirement-main.md#r490-02) | [D490-02](../../../design/versions/current-main-0.6.17-guru.71/design-main.md#d490-02) | [T490-04](../../../test/versions/current-main-0.6.17-guru.71/test-strategy.md#t490-04), [T490-05](../../../test/versions/current-main-0.6.17-guru.71/test-strategy.md#t490-05) | ARCH-INT-036 / EVD-047 |
| [R490-03](./requirement-main.md#r490-03) | [D490-01](../../../design/versions/current-main-0.6.17-guru.71/design-main.md#d490-01), [D490-03](../../../design/versions/current-main-0.6.17-guru.71/design-main.md#d490-03) | [T490-01](../../../test/versions/current-main-0.6.17-guru.71/test-strategy.md#t490-01), [T490-02](../../../test/versions/current-main-0.6.17-guru.71/test-strategy.md#t490-02), [T490-03](../../../test/versions/current-main-0.6.17-guru.71/test-strategy.md#t490-03) | ARCH-DOM-033 |
| [R490-04](./requirement-main.md#r490-04) | [D490-02](../../../design/versions/current-main-0.6.17-guru.71/design-main.md#d490-02), [D490-04](../../../design/versions/current-main-0.6.17-guru.71/design-main.md#d490-04) | [T490-01..05](../../../test/versions/current-main-0.6.17-guru.71/test-strategy.md) | EVD-047 |

Design 和 Test 的本版 trace 均反向链接本表；前驱全部 trace 通过上面的不可变继承继续有效。
