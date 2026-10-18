# #285 contribution traceability

| Requirement | Design | Test | Architecture |
| --- | --- | --- | --- |
| `REQ-021` | `DES-020`, `DES-021`, `DES-022` | `SCN-017`, `SCN-018` | `ARCH-DOM-002`, `ARCH-DOM-003` |
| `REQ-022` | `DES-022`, `DES-023` | `SCN-018`, `SCN-020` | `ARCH-DOM-002`, `ARCH-DOM-004` |
| `REQ-023` | `DES-024` | `SCN-019` | `ARCH-DOM-004` |
| `REQ-024` | `DES-023`, `DES-025` | `SCN-020`, `SCN-023` | `ARCH-DOM-002`, `ARCH-DOM-004` |
| `REQ-025` | `DES-020`, `DES-025` | `SCN-019`, `SCN-020` | `ARCH-CUR-007`, `ARCH-DOM-002` |
| `REQ-026` | `DES-021`, `DES-024` | `SCN-021`, `SCN-022`, `SCN-023` | `ARCH-DOM-005`, `ARCH-CUR-006` |

Architecture impact：`no_change`。本 contribution 不新增 Architecture identity，不修改
domain/component ownership，也不 promotion shared `current-main-0.6.5-guru.37` authority。
