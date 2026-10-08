# #503 身份占用与生命周期职责边界

## 来源与目标
来源：[Guru #503](https://github.com/castbox/guru-trellis/issues/503) 与[职责修订](https://github.com/castbox/guru-trellis/issues/503#issuecomment-6053071122)。current RDT/Architecture 为 current-main-0.6.17-guru.75；本文为 task 范围。

全新身份正式创建不应要求无关历史任务具备当前生命周期能力。根因是唯一性 consumer 在比较身份前越界读取完整 schema；原 legacy 白名单候选作废。

## 范围与合同
- R503-01：registered 历史 worktree 混合 header 共存时，正式 create/ensure/bind/ref-id resolution 成功创建和解析唯一全新 planning task。
- R503-02：占用只消费合法 TaskId、canonical locator 与冲突。无关 source/generation/status/未知非身份字段改变不改变占用结论；不生成 current DTO 或迁移数据。
- R503-03：目标 TaskRef/目录、exact/casefold id、branch history 与 unresolved ledger 占用继续拒绝。活动坏 JSON、非 object、缺失/非法 id 具体拒绝；archive/branch-history 既有缺损行为保持。
- R503-04：selected ref/id 先身份定位与唯一性，再严格校验选中目标完整 current schema/source/generation。旧混合和非法目标拒绝，提供具体 locator 与正式升级/逐案处置入口。新创建目标仍严格检查 gen0/planning/source/base。
- R503-05：成功/拒绝扫描均保留历史 bytes/modes 与其它 checkout Git 状态；拒绝无半创建，恢复无重复 mutation。
- R503-06：canonical/dogfood/平台/schema/consumer 一致；正式 Fork source-lock 集成已合并修复后，source 与 clean installed 同一正式入口验证。

升级 inventory/disposition 保留完整 schema 分类，不消费 reservation 作为 migration authority。Fork writer 已由独立 #29/PR #30交付，本 task 集成正式来源。不包含 Fork新修改、Backend安装patch、历史迁移、清理、发布部署；#378/#379仍独立。

## 验收
- S503-CREATE：真实脱敏混合 header 与 current checkout，正式创建、ensure/bind、ref-id resolution 成功。
- S503-RESERVE：同id/casefold/目标目录/branch/ledger冲突拒绝，资源数量不变。
- S503-REJECT：无关非身份字段不阻塞；同一无效记录被直接选择时严格拒绝。坏JSON/非object/缺失非法id拒绝并具体定位。
- S503-PRESERVE：历史bytes/modes及其它Git状态不变；恢复不重复创建。
- S503-INSTALLED：正式source-lock、clean安装、上述入口与投影/drift/reapply通过。定向证据不等于完整Release矩阵或Backend恢复。

## Docs SSOT Plan
ssot_first：修订task-owned RDT/Architecture贡献及spec投影；shared current在独立完整committed Branch Review后由各owner绑定expected-current串行promotion。#495及SHA绑定历史证据不改写。
