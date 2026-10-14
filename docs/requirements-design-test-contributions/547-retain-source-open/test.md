# #547 Test 证据与界限

测试语义结果是 fixture判断，验证确定性 owner/API投影，不冒充实际 AI语义门禁或 GitHub/CMS生产成功。

| Strategy / scenario | 入口与观察 | 当前证据 |
| --- | --- | --- |
| T547-01 / SCN547-RETAIN | canonical Closure public wrapper，workflow/standalone；OPEN、no_mutation ref、共享 snapshot；同入口恢复 | 新 retain regression 通过，provider close=0；Task2 source_result=null且唯一 public Closure |
| T547-02 / SCN547-FINISH | 固定上游正式 Task writer、scope owner、真实 local_commit Delivery API历史；匹配 preset installed Completion/Closure/Finish wrappers；真实 Git bare remote bookkeeping | 同 Task/gen/source scope修订；evidence_pending不写Completion；fresh completed后源OPEN；archive保存scope/历史/未验证文本；重复调用无第二archive/PR/merge；远端唯一archive且active副本不存在 |
| T547-03 / SCN547-MIXED | retained exact source + 另一 Issue close，及 source close control | aggregate closed不等于source_closed；源retain仍OPEN、public no_mutation/null；源close控制组CLOSED；provider计数逐项正确 |
| T547-04 / SCN547-BLOCKED | 有效identity的 semantic blocked / 原 reference/no_issue/close paths | 原reason返回，无provider、无新transaction；原close/recovery行为回归 |
| T547-05 / SCN547-DRIFT | provider普通关闭retained Issue、reopen关闭动作、source/scope正常变更 | Closure conflict、Finish closure_refresh_required；原owner re-entry，无擅自close/reopen/archive；Completion剩余scope不完成 |
| T547-06 / SCN547-INSTALL | source graph、受控matching clean preset、reapply、Shared/Claude/Codex/Cursor、managed bytes/modes与sidecar | source 38 packages/114 commands通过；受控再次apply及dogfood drift通过；8个声明.bak逐项确认原字节后仅在受控副本处理，无.new/conflict残留 |

2026-10-14 定向运行：Closure/Finish、DeliveryFlow、scope_revision、finish_family、delivery_contract_graph 合计 **110 passed**。使用managed resolver、外部pytest和固定已安装upstream scripts；未使用PATH Python作为产品fallback。source package graph另行通过。

固定内容身份：CLI tar SHA256 `5aeeb81ca72508081b7dd94ddb7a19f69444714f78b3a38858d908196cc77916`；Core tar SHA256 `45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967`，当前产品commit `1e40014023de53ddfd9368b3fb4d0a7a31e92293`。字节核验不是正式远端source-lock/Release证明。

受控安装测试使用真实preset和从固定CLI复制的官方scripts，不是官方CLI init远端marketplace安装或原旧安装真实upgrade证明。local_commit是upstream API的受控声明profile，生产Guru仍pull_request；不会伪造business PR Delivery。匹配installed/public API结果与实际Git远端post-state分别观察；fake gh不证明真实GitHub调用。

未验证：当前app完整旧安装采用新模型、原CMS Task恢复、业务联调/产品#59联合验收、完整多平台throwaway/Release、真实远端marketplace init与发布。它们是范围外边界；不借110通过宣布这些完成。正式Phase2/committed Review与Architecture promotion保留原门禁。
