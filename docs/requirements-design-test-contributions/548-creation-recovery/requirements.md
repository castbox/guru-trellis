# #548 创建与原对象接续增量

来源：[当前 Issue #548](https://github.com/castbox/guru-trellis/issues/548)。前驱 R531 / ADR-024，Task整体scope与全部Delivery独立Planning保持。

| Requirement / behavior | 当前目标 |
| --- | --- |
| R548-01 / BEH548-EXPLICIT | 正式创建后有context解析同Task，无context通过明确校验的explicit-task进入D1 Planning/Activation |
| R548-02 / BEH548-RECOVERY | 原创建/attach/输出丢失恢复同Task/gen/D1，不增加Issue/Task/Git资源或空Delivery |
| R548-03 / BEH548-CONFLICT | 真实新session可rebind同Task；已有不同current、stale/mismatch保持原内容并明确停止 |
| R548-04 / BEH548-LEGACY | 旧untracked nonterminal缺已提交identity时，原公开owner逐记录转换或明确defer/manual；保留原规划及资源，不把停止当恢复成功 |
| R548-05 / BEH548-EVIDENCE | 定向package、代表installed/native、projection/reapply/drift和migration分层；恢复不产生Planning/Activation/Completion批准 |

不恢复已退役workspace-mapping/start模型、不改上游/provider、不升级清理业务仓、不扩完整Release矩阵。原CMS失败只是来源，不是本次current根因证明。
