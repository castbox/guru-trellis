# #575 S2：v0.7.0-guru.4 来源准备

## 来源与整体责任

唯一整体 accepted scope 为 Task 根 `prd.md` 的 R575-01..07/A575-01..08。直接来源是 [#575](https://github.com/castbox/guru-trellis/issues/575) 的 Stage 1、正式依赖前置和发布边界；私有 `release-guru-trellis-version/references/contract.md` 是设计约束。唯一 source-design disposition matrix 位于本 Delivery `design.md`。

整体准备按 S1 来源采用、M 独立工具与任务维护、S2 来源准备、S3 完整投影与验证推进。S2 产生可经独立审查并交付的 `.4` canonical 来源及已采用的基础工具；S3 才消费实际 clean committed `.4` source 完成对应投影与安装验证。完整准备责任没有缩减，Whole Completion 必须覆盖 S3。

保持原 TaskId、generation、source disposition、当前 DeliveryKey 与 planning_root。S2 只使用 `Refs #575`。S3 经原 Completion/Creation owner 取得新的真实 Delivery，本文不预建其 UUID 或 planning_root。软件发布 Stage 2、tag、Release、Issue closure 不属于准备 Task 的实现。

## 当前切片要求

| 标识 | S2 来源准备的行为承诺 | 整体承接 |
| --- | --- | --- |
| R575-S2-01 | canonical extension revision、原 maintenance target、生产结果、public schema/example 和 stop consumers 一致使用 `0.7.0-guru.4`。保留真实 predecessor 值、合法旧版本族及原 HEAD/clean/source 检查；原 preset resume 正确使用 managed interpreter。 | R575-01、02、03 |
| R575-S2-02 | 保留并交付 M 已由原 owners 生成的 `.3` 基础工具图、固定 Fork 原生 Task2/session3 投影及同 Task 的历史转换；当前 installed `.3` 必须与自身 receipt 对应。`.4` canonical 与 installed 的剩余版本差额明确归 S3，S2 不声明最终 `.4` parity。 | R575-03、04 |
| R575-S2-03 | 根 README、workflow README、preset README 与 public-docs spec 的当前源码映射准确表达 `.4` 尚未发布、CLI/Core `0.7.0-castbox.3` 与固定 Fork `2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0`。已发布 `.3` 的 immutable tag、旧锁、稳定安装来源和历史证据保持原归属。 | R575-01、02、03 |
| R575-S2-04 | 完成当前来源切片所需的 source/graph、现存 `.3` installed、固定 Fork native、版本消费者与 Plan2/resume/rollback 模块检查，以及 ownership、平台入口、卫生和真实 secret scan；结果区分 source、installed、fixture/native 与外部层次。 | R575-04 |
| R575-S2-05 | 原 RDT owner 在独立贡献根承接当前来源结果和后续 S3 义务，完成双向 trace 与本切片 reconciliation。shared current 晋升由 S3 在完整准备证据齐备且首次完整 committed Review 后串行完成；S2 不把 draft contribution 当 current authority。 | R575-05、07 |
| R575-S2-06 | S2 经本切片 Check、TaskCommit、完整独立 Review 与 Refs-only Delivery 后，实际 clean committed 来源由 S3 消费。Whole Completion 只有在全部准备切片和必要证据满足后才进入 Closure/Finish；S2 合并不能代替该判断。 | R575-06 |

## S2 验收

- A575-S2-01：生产版本消费者及上述四份当前源码文档一致表达 `.4` 准备源码；合法旧安装和真实 `.3` 历史未被改写。
- A575-S2-02：当前基础工具的 installed/receipt、固定 Fork native、workflow 和平台入口与各自实际来源一致；Task2、历史 Delivery、session3 和配置定制保持。S3 的 `.4` 全投影差额明确列出，不以结构通过声称版本 parity。
- A575-S2-03：source 与原迁移/恢复定向检查、ownership、差额卫生和 secret scan 有实际结果；模块测试中的 preset 替身与缺少 formal predecessor marker 的边界公开保留。
- A575-S2-04：RDT 当前切片 trace 与剩余 S3 责任明确；本切片独立检查和完整 committed Review 无开放 finding 后才交付。

## S3 保留义务与整体完成

S3 使用 S2 的实际 clean committed `.4` source，经原 tools-only owner 完成独立 `.4` 操作，不复用 M 的 `.3` operation。原 public tools 与 Guru installer 完成 `.4` packages/runtime/schema、Shared/Codex/Claude/Cursor 投影、三平台 reapply/drift、权限、sidecar 和退休资产检查。

S3 执行一个代表性 Codex focused clean/local-workflow 样本、真实 stable `.3` predecessor 的正式维护样本；实际验证工具、所选任务转换、历史交付、目标 native continuation、下一真实 consumer、同操作 resume 和不兼容单侧 tools rollback。source_locked/clean-source 依赖在真实来源形成后消费，不能由 S2 fixture 代替。

S3 原 RDT/Architecture owners 收敛完整准备责任；需要 shared promotion 时执行晋升前后各自 Check/TaskCommit/完整独立 Review。随后 Whole Completion、reference-only Closure、Finish archive/bookkeeping 各走原 owner。正式发布 Stage 2 对最终 main candidate 重新冻结与验证，不继承 S2/S3 安装结果作为 final Release 证明。

## 非目标

不新增公共 Skill、schema id、typed exit、owner、compatibility reader 或恢复框架；不修改上游/global npm/node_modules，不安装真实业务仓，不处理 #577/#46 的产品能力，不发布软件、不清理资源。累计多平台/native-host、远端最终 provider、tag smoke 和生产验证不在当前来源切片。
