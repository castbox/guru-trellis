# #657 追踪与替代边界

固定前驱为 Git `319202beab79c7666ecdb855291bf117e43d407e` 的 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`。保留 RDT-REQ/DES/TST-LIFECYCLE identity 和全部仍适用前驱条件；三个 proposed files 是完整拟写定义。共享 current 只在完整 candidate Check 后由原 RDT owner 最终整合，不递增全局版本或新增无关导航。

| 来源 | requirement / behavior | design / contract | test |
| --- | --- | --- | --- |
| #657 R1–R3/F1 | R657-01 / BEH657-ADMISSION | D657-01 / CON657-ADMISSION | T657-01/02/03：V1–V6 |
| #657 R6/F5 | R657-02 / BEH657-SELECTION | D657-02 / CON657-SELECTION | T657-04：V11 |
| #657 R3/R7/F6 | R657-03 / BEH657-SCOPE | D657-03 / CON657-SCOPE | T657-05：V3/V12 |
| #657 R4/R5/F2–F4 | R657-04 / BEH657-CONTRACT | D657-04 / CON657-DISTRIBUTION | T657-06/07：V7–V10 |

只修订初始 created 普遍准入、Selection 无条件 initial Author 和退役 scope/身份/恢复指令。R531/R635 的公共模型、唯一 owner、共享事实及本机资源边界、R636/637/638 的 Draft、适用性、实际晋升及最终质量职责保持。历史 schema/ADR 通过 immutable Git 和窄替代保留，不成为 current fallback。实际执行只由 test.md 单写。
