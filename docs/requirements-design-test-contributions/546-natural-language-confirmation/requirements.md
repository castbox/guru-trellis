# #546 交互合同增量

来源：[Issue正文](https://github.com/castbox/guru-trellis/issues/546)及[分发验收修订](https://github.com/castbox/guru-trellis/issues/546#issuecomment-6159835923)。本贡献继承 `current-main-0.6.17-guru.90/active`，不更改 #531 Task/Delivery 或独立副作用合同。

| 增量身份 | 来源承诺 | owning design / test |
| --- | --- | --- |
| R546-01 / BEH546-CONFIRM | 正文目标1、4：自然语言及当前精确动作一次承接 | D546-01 → T546-CONTRACT/S546-01,02 |
| R546-02 / BEH546-CHANNEL | 正文目标2：聊天默认、渠道偏好和工具用途 | D546-01 → T546-CONTRACT/S546-04 |
| R546-03 / BEH546-ANSWER | 正文目标3：原问题对应、迟到重复答案 | D546-01 → T546-CONTRACT/S546-03 |
| R546-04 / BEH546-CONTINUE | 正文目标4：原授权边界及mapped自动接续 | D546-01/02 → T546-CONTRACT/S546-02,05 |
| R546-05 / BEH546-PLATFORM | 正文目标5：平台强制审批独立解释 | D546-01 → T546-CONTRACT/S546-05 |
| R546-06 / BEH546-DISTRIBUTION | 正文目标6及修订评论：公共SSOT、平台源、旧dogfood延后 | D546-02/03 → T546-SOURCE/S546-06 |

公共行为正文只由 design.md 指向的 Interaction Budget 拥有，不在本贡献复制。完整矩阵、软件发布、实际客户端行为与旧安装迁移均不得由静态合同或平台源检查推定完成。
