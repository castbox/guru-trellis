# #669 Design 差额

状态：promoted；固定 B 与 manifest 相同。完整正文已整合到 `docs/design/current/completion-closure.md`，本次拟写来源保留在 `proposed/docs/design/current/completion-closure.md`，新增 D669-01..04 / CON669-ENTRY/CONTENT/RECOVERY/VALIDATION。原 public Task/C3/C4/C5/Bind 和终态 owners 保持单写；独立 profile/schema 扩充既有实现状态，不增加第二生命周期或通用 allow_dirty。

Architecture 继承 [#669 contribution](../../architecture/contributions/669-existing-implementation-reactivation.md)、ARCH-DOM-060 和 ADR-PORTABLE-SHARED-LIFECYCLE。原 Architecture/RDT owners 在独立 candidate Check 后 final_integration 写完整 current，并检查实际 after 适用性。
