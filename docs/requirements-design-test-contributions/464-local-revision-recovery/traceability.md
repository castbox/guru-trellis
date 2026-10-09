# #464 Traceability

| requirement / behavior | design responsibility | scenario / case |
| --- | --- | --- |
| REQ-464-LOCAL / BEH-464-CHECK | DES-464-CHECK | SC-464-DELTA：AC03/04/06/12，A-only、B dependency/version/toolchain/environment、新C、fact不可用、当前绑定 |
| REQ-464-LOCAL / BEH-464-RECOVERY | DES-464-RECOVERY | SC-464-RECOVERY：AC08/10/11，同HEAD anchor可用/缺失，原transaction恢复 |
| REQ-464-LOCAL / existing identity-authority | current identity/Architecture/Planning owners | SC-464-AUTHORITY：AC01/05/06，无影响更新/实质变化 |
| REQ-464-LOCAL / existing revision | Check/TaskCommit/BranchReview owners | SC-464-REVISION：AC07/11，文档/projection/promotion/finding-fix |
| REQ-464-LOCAL / existing continuation | Reconcile/Completion/continuation owners | SC-464-CONTINUE：AC02/09/10，unchanged/evolved，后续Delivery/补证 |
| REQ-464-LOCAL / distribution | canonical preset projection | SC-464-DISTRIBUTION：AC13，apply/reapply/installed/platform/drift/sidecar |

前述 existing responsibility 引用当前 baseline，不复制已有合同，不创建第二 owner。每组实际结果、层级和未验证边界见 Test。
