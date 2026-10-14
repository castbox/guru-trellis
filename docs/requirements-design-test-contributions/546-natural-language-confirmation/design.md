# #546 设计责任

继承 `current-main-0.6.17-guru.90/active` 和 Architecture `.87/active`。

| 身份 | 唯一落点及consumer | requirement / test |
| --- | --- | --- |
| D546-01 / CON546-INTERACTION | `trellis/presets/guru-team/spec/workflow/workflow-contract.md#interaction-budget`，当前执行AI读取唯一公共语义 | R546-01..05 → T546-CONTRACT |
| D546-02 / CON546-LOAD | canonical workflow、交互owner的Skill入口、既有finish平台overlay薄加载上列installed locator；各owner保留其原动作边界与typed exits | R546-01,04,06 → T546-CONTRACT/T546-SOURCE |
| D546-03 / CON546-DISTRIBUTION | #546评论6159835923及preset/workflow README；旧完整dogfood由原迁移owner同步，source不冒充installed或native | R546-06 → T546-SOURCE |

无 runtime、schema、公共API、授权存储、兼容adapter或局部安装器变更。来源设计矩阵在本任务规划中完成；长期行为责任及双向trace由本贡献持有，任务归档不改变上述canonical落点。
