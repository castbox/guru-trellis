# #503 需求贡献

修订候选，current authority仍为current-main-0.6.17-guru.75。来源：[#503职责修订](https://github.com/castbox/guru-trellis/issues/503#issuecomment-6053071122)，承接R495-08，历史证据不改写。

- R503-01：current正式create/ensure/bind/id-ref resolution在无关混合历史worktree共存时成功。
- R503-02：占用只读取合法id/ref；source/generation/status/未知非身份字段不改变占用。投影不认可current执行能力或migration分类。
- R503-03：exact/casefold id、ref/目录、branch/ledger占用仍拒绝；活动坏JSON/非object/缺失非法id具体拒绝。archive/branch缺损规则保持。
- R503-04：selected ref/id先身份定位与唯一性，后严格current schema/source/generation；旧混合/非法目标拒绝并准确定位与指向正式处置。新创建target仍严格校验。
- R503-05：只读保全bytes/modes与其它Git状态，失败无半创建，恢复无重复mutation。
- R503-06：正式Fork source-lock集成#29修复，canonical/dogfood/platform一致，source及实际clean installed正式入口验证；不冒充Backend恢复。

不含业务安装写入、Fork新修改、历史迁移、清理、发布部署。shared current由正式owner独立review后promotion。
