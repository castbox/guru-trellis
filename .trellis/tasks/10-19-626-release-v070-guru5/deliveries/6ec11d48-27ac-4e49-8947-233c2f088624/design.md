# D1 发布准备设计

## 1. 设计目标、需求承接与内容基线

本批覆盖 DR1–DR5 / DAC1–DAC5。development baseline B 为 Creation 所用 main commit `33f18a768c9c8d901f34b899934ac40c3d97cc5b`，来源为 Sync 的 selected main 与 D1 首批无前序的开发基线。Planning H0 同为该 commit；内容范围为 B 至最终 D1 HEAD，PR target 独立为 main，不能把 H0 当作最终实现候选。

阶段适用 Architecture 为 `current-main-0.6.17-guru.101`，constitution 为 `guru-trellis-design-constitution-v1`，change contract 为 `guru-trellis-architecture-change-contract-v1`。独立 candidate_assessment 的正式出口为 baseline_current / no_architecture_impact：发行目标与知识 identity 后继不改变架构决策、职责、GAP、兼容退出或 public I/O。因此不新增 Architecture contribution/ADR；内部知识 identity 仍由原维护方写入，不将 no-impact 解释为可跳过版本一致性。

## 2. 当前系统、边界与目标差额

首次 D1，无前序 Delivery。当前 manifest .4；guru-upgrade-installation 的 TARGET_GURU、output const schema、consumer schema、示例/测试也使用 .4。三个 README/public-docs 仍把 .3 标稳定、.4 标候选。当前 RDT .6.17-guru.110 与 Architecture .6.17-guru.101 通过 current 完整单元和原历史定位规则提供知识。

目标为软件 .5 和内部 RDT .7.0-guru.111 / Architecture .7.0-guru.102。Fork lock/CLI .4、公共 Skill id/exit/schema id/字段、既有 runtime 算法与安装流程不变。历史 tag、版本目录、Task archive 和原证据不重写。

## 3. 来源设计处置（唯一）

| 来源条款 | 原承诺 | 处置 | 本方案落点、理由与影响 | 上游处置 |
| --- | --- | --- | --- | --- |
| Issue #626 / 版本与来源 | tag .5、extension .5、Fork .4 三轴独立 | retain | 第4/5节同步 canonical 目标和全部维护 consumer，Fork lock 保留 | 无偏离 |
| Issue #626 / 内部版本 | RDT .110→.7.0.111、Architecture .101→.7.0.102，保留历史 | retain | 第4/7节由原 owners 只建立新 identity/导航关系，完整正文和旧来源保留 | 无偏离 |
| release contract / Stage1 | 准备 Task reference_only、Refs PR、Completion/Finish 与 Stage2 分开 | retain | 第6节执行原 owners；#626 不随准备合并关闭 | 无偏离 |
| release contract / reviewed promotion | 真实 shared promotion 发生时不得复用前后 bytes 的同一审查 | retain | 无新增架构行为 contribution；知识 owner 判断 identity-only 的窄 direct sync。若实际变成 contribution/promotion，回独立 Phase2 assessment，按原 release contract 执行晋升前后 fresh check/commit/review | 不以版本更新构造虚假 promotion |
| current Architecture / ADR-030、R331-04 | full candidate/proposed targets 先独立 Phase2评估；实际写入后核对，再最终 Check/commit/committed Review | retain | 第6/8节保留；身份后继写入不替代独立 assessment，所有最终 bytes 纳入最终 Check 与 Review | 无偏离 |
| release contract / Stage2 | 准备和 Finish 合并后 fresh main exact-candidate gates、tag、smoke、Release、closure | retain | 本 Task 不执行 Stage2，不记录动态发布状态；由同一 release caller 后续继续 | 无偏离 |

PRD 与 implement 只引用本节，不另建来源设计处置。

## 4. 模块、职责与设计取舍

- 版本配置 owner：修改 `trellis/guru-team-extension.json.version` 为 .5；`target_trellis_cli` 与 source lock 保留原值。
- maintenance package：在 `trellis/skills/guru-team/packages/guru-upgrade-installation/` 原 runtime/schema/example/test 及其 canonical consumer 同步 target .5。保留原 predecessor parsing/upgrade 行为，不新增 alias、fallback 或 .4/.5 双 target。`guru-upgrade-tools` 的当前输出示例随源版本对齐。
- 公开文档 owner：根 README、workflow/preset README 和 `.trellis/spec/docs/public-docs.md` 使用真实 stable .4 peeled `855f236850714edc4b78169218c09568c823f336` 与现有 Fork lock，明确 .5 仍为准备。清除已失去当前 consumer 的旧 S2/S3 待办叙事，历史能力与证据保留其身份。
- 原 Architecture maintenance owner：将 README current identity 建立为 .7.0-guru.102、predecessor .6.17-guru.101；不变更架构正文或制造 ADR。原 RDT owner随后建立三层 .7.0-guru.111 版本入口并切换三层 README/current 导航关系，继承 .102；旧 .110 版本页不改。
- preset installer：按现有 apply 管理 canonical→installed/platform，逐个处理实际 sidecar，不直接补丁生成副本。并行实施者只写各自声明的 canonical 范围；apply 由主会话串行执行。

使用原单写 owner 与直接版本演进即可满足本次目标；不增加 release-state writer、后台任务或新公共机制。

## 5. 接口与数据

`extension manifest.version` 与 maintenance 的 `target_guru_revision` 从 .4 演进 .5；output const schema 和实际消费者同步。它们描述所选发行，不改变 public output 字段或路由。原 upgrade 输入继续按真实 receipt、source lock 与版本 family 解析，不以旧发行号创建第二维护实现。

内部 knowledge identity 是文档 authority/version 关系，不是软件版本或 Task API 字段。三层 RDT 必须使用同一新版本并继承 Architecture .102；旧 .110/.101 可从原版本/Git读取历史含义。没有新 DB 字段、业务数据迁移、额外 runtime artifact 或授权字段。

## 6. 状态、顺序、正常与失败流程

1. 当前 Planning、Wording、final_plan Architecture、Approval 与展示后由 Activation 接受 D1。
2. 实施者更新 canonical 软件版本/maintenance/docs；原知识维护方先审查完整目标及旧 current，建立 identity 后继。共享 current 写入仍由原维护方负责。
3. 串行 apply 三平台，检查实际 byte/mode/ownership、sidecar 和 drift。未知本地改动保留并回原 installer conflict 路径，不静默覆盖。
4. fresh 独立 Phase2 Architecture 评估完整 tracked/untracked 候选及实际知识目标；确认已写 identity-only 适用性，必要真实晋升走原 owner。最终 Check 覆盖全部最终 bytes。
5. TaskCommit、fresh committed Architecture/full Branch Review、Delivery Review、Refs-only Publish/Merge；然后准备整体 Completion、no_mutation Closure、Finish bookkeeping 与资源收尾。
6. 同一 release caller 取得 fresh main 执行 Stage2，旧准备 branch HEAD/gate 不作为最终发布证明。

任一身份/版本、source lock、test 或 managed projection 不一致时，停在原负责 owner 修复；不把 FAIL/SKIP 变成通过。实际范围或机制改变时回最早 Planning/Clarify/Architecture，保留同一 Task/D1。

## 7. 恢复、兼容、迁移与集成

新版本 target 使用原直接演进；保留前驱真实安装验证，不引入持久兼容分支。旧知识版本/Git历史是历史读取来源，不作为第二 current 写入面。新内部版本页保留未迁移 .109 的精确入口和 #331 完整知识单元关系；版本切换不宣称迁移范围扩大。

没有业务数据或部署迁移，故无需数据库/服务回滚协议。普通 owner 输出丢失通过原 read-only recovery 获取同一身份；不重复 create/commit/push/merge。知识 identity 写入发生冲突时回原 maintenance owner，用写前 live expected-current 判定，不能覆盖另一个任务。

## 8. 验证设计

| 验证 | 要求/AC | 入口与输入 | 预期观察与边界 |
| --- | --- | --- | --- |
| V1 | DR1/DAC1 | maintenance package 与 tools package 现有 unittest，真实 canonical target .5 | 原入口/const/consumer一致，旧输入边界不被新 target 固定值破坏；不是发布安装证明 |
| V2 | DR2/DAC2 | 三 README/public-docs 全文 review；live tag/source CI 读取 | .4 stable 与 .5 candidate 清楚，Fork来源匹配；不复用旧性能或 live模型结论 |
| V3 | DR3/DAC3 | 原知识 owner对三层新版本页、README、current导航和 Architecture关系的语义/链接检查；旧 .110与非必要正文 diff | 前后继一致、历史不改、完整单元/未迁移入口保持；identity更名不冒充新功能验收 |
| V4 | DR4/DAC4 | check-skill-packages source/installed 和四个 platform-root；check-upstream-ownership；apply三平台；check-dogfood-overlay-drift | 版本与实际受管 byte/mode一致，无未解决 sidecar或意外变更 |
| V5 | DR4/DAC4 | test_issue_content_distribution、test_planning_body_distribution、test_bytecode_hygiene；本批触及 package 的定向 tests | 已合入 release内容与发行投影没有受本批破坏；不跑累计平台矩阵 |
| V6 | DR5/DAC5 | 独立 Architecture、完整 Check/committed Review、Delivery及Completion/Finish各原入口 | 最终准备内容无开放P0–P3，Refs-only与归档事实真实；Stage2仍未执行 |

准备阶段不重复最终 candidate focused/existing 安装；Stage2 必须绑定其新的 exact commit/tree，完成 release contract 的全部定向入口及真实 scanner。未覆盖完整多平台/native-host、真实业务与生产。

## 9. Canonical 引用、本轮差额与实际未决项

必要依据为 RDT 三层 current `knowledge-maintenance.md` / R331-02/04、D331-02/04、T331-05/06，以及 Architecture FOUNDATION、change-contract 的阶段适用性和实际写入规则。当前 no-impact 结论意味着无架构行为 contribution/ADR 责任；RDT 原 writer 对 identity-only successor 执行窄直接同步并给正式结果。若原 owner 判断需要真实 contribution/promotion，则回相同 D1 的最早受影响 owner，不预建空贡献。

本批没有必要未决项。安装、真实模型、业务部署和累计矩阵的边界保持；后续 Stage2 不因本批规划而成为已通过。
