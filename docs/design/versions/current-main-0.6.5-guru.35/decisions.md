# Design 决策

- `DDEC-001`（accepted）：文档只索引 registry/interface，不复制 schema 字段，避免 drift。
- `DDEC-002`（accepted）：current as-built 与 released tag 分开建模；manifest revision 不等于 release。
- `DDEC-003`（accepted）：Bootstrap 不合并 RDT 与 Architecture owner，只编排 minimal typed outputs。
- `DDEC-004`（accepted）：`.trellis/spec` 是 locator/usage projection，不是第三 authority。
- `DDEC-005`（inferred, not current）：未来 Phase owner 解耦可能改变 orchestration；在独立 Issue 接受前只列 GAP/TARGET。
