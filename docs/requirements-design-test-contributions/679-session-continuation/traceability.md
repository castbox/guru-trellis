# #679 追踪与窄补充边界

完整前驱：Git `e6c3b8276d62ac174ab42cba5bca4d5784be2ca3` 的 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`。三个 proposed 是受改单元的完整拟写定义，保留全部仍适用前驱与稳定 identity；共享 current 仅由原 RDT 在候选 Check 后最终整合，不增加全局版本。

| 来源 | requirement / behavior | design / contract | test |
| --- | --- | --- | --- |
| #679 R1、AC1/AC2 | R679-01 / BEH679-RECEIVE | D679-01 / CON679-RECEIVE | T679-01/02：真实接收/已有进度/状态 |
| #679 R2、AC2/AC4 | R679-02 / BEH679-FIRST-FAILURE | D679-02 / CON679-DIAGNOSTIC | T679-02/05：首失败及直接消费者 |
| #679 R3、AC3 | R679-03 / BEH679-STANDALONE | D679-03 / CON679-PROJECTION | T679-03：公开 recipe、两 mode 和原生重建 |
| #679 R4、AC4/AC5 | R679-04 / BEH679-ARTIFACTS | D679-04 / CON679-PRESENTATION | T679-04：实际文案调用/Task-only/archive |
| #679 AC4–AC6 | 全部本批行为 | 原 matching 分发与唯一 owners | T679-05/06：兼容、安装和分层证据 |

不替代 R531/R635/R657 的公共身份/状态/资源模型，不改现有 Planning phase 或原 Skill/typed exit，不新增 Architecture 决定、store、compatibility authority 或授权记录。只补明确接收者前置事实、首失败、standalone 投影和展示调用；历史材料继续作为历史，不成为当前 pass。实际结果仅由 test.md 维护。
