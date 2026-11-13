# #812 设计差额

完整 resulting definition 位于 proposed/docs/design/current/qualifier-applicability.md。保 DES-793 的三个 owner 与条件调用。新增 DES-812-01～05，承接同层明确的完整身份传递、原模型校验、调用期续接和输入直接演进。

原 DES-793-03 的“输入保持”仍描述 #793 的已交付差额；#812 的七类输入按新版本窄演进，旧字节保留为历史验证资产。不存在双 reader、第二选择 writer 或资格存储。精确接口由原 package 独占，迁移由 MIGRATION-812 独占。

Architecture 只引用公开 baseline guru-trellis-architecture / docs/architecture/README.md / active，与 ARCH-DOM-QUALIFIER-APPLICABILITY、ADR-EXPLICIT-TASK-QUALIFICATION 关联；不复制其内部判断。
