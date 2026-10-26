# existing verifier 的 AGENTS custom 调用适配：设计

## 1. 设计目标、需求承接与内容基线

本批承接整体 AC7/AC8、本批 D2-R1–R5 与 D2-S1–S3。目标是在原稳定 existing 入口内修复 caller 的 AGENTS decision 遗漏，并保留原 tools owner 的全部执行职责。

开发基线 B 选择当前 Task checkout 的初始基线 `e70769fb3c48ea05b106809a99161995c8dfcdfa`。它来自本 generation 原 Reactivate 的 reviewed main；不是 gen0 业务交付 H，也不是最终 Release candidate。Planning H0 是写方案时的 checkout HEAD 观察，最终内容范围由同一 Delivery 的实际 B..H 承接。PR 目标为 `main`，目标分支后续变化不自行重选 B。

独立 Architecture `candidate_assessment` 已实际返回 `baseline_current/no_architecture_impact`，适用 authority 为 `guru-trellis-architecture`、`guru-trellis-design-constitution-v1` 和 `guru-trellis-architecture-change-contract-v1`。该结果只评估当前三项候选事实，不是 final_plan、实现、安装或发布通过。最终方案仍须 Wording、原 Architecture final_plan 和 Approval。

## 2. 当前系统、边界与目标差额

`_upgrade_native_bootstrap_tools` 在 preview 后，仅为 `status=conflict AND required=false` 的文件构造 preserve decision。真实 init fixture 已有 AGENTS.md；当其状态为 unchanged 时，输入中没有该文件。原 `compose_agents_input` 明确要求一个显式 custom decision，因此当前稳定 existing 入口在 prepare 前失败。

目标差额位于 verifier 的输入构造，涉及 `verify_trellis_compatibility_matrix.py` 与现有 `test_verify_trellis_upgrade_contract.py`。原 runtime、renderer、Fork public maintenance API、workflow、installer、manifest/source lock 和状态模型均没有本批实现差额。前序版本/文档准备保持其历史交付，不被本批重复或改判。

## 3. 来源设计处置（唯一）

| 来源及原承诺 | 处置 | 本批落点、理由、影响及上游处理 |
| --- | --- | --- |
| tools contract / Forward behavior4：实际 capability `AGENTS.md/custom` | retain | 第4–6节保留原 consumer 的 capability 检查；caller 不承担或放宽该检查 |
| 同节：唯一 custom、实际 source snapshot、已审查 base content | retain | caller 始终从真实 preview row 构造一条 custom，使用原 source 与解码正文；第5节字段及V1验证 |
| 同节：原 renderer 只更新 Guru block，public prepare 一次，冻结计划不改 | retain | 第4/6/7节保持原单写路径；不复制 updater、不把 preserve/replace 静默转换 |
| private release Stage1 / R5：整合前后两次完整独立审查，第二轮真实公共full_review | 保留两轮；本切片第一轮使用有界恢复载体 | 第9节规定early TaskCommit、完整existing和candidate Check之后，由原独立reviewer通过原early Review入口执行第一次完整恢复审查；零开放P0–P3才继续原整合。第二轮在实际候选重绑、final Check和原TaskCommit后执行真实公共完整Review；不伪造第一轮公共gate |
| private release Stage2 与内容有效性 | retain | 第7/8节区分准备 H 与最终候选，保留所有原失败、重新取得最终候选门禁；不以早期反馈代替正式结果 |
| 当前构建要求：新版 pnpm、本地 checkout | retain | 第7节只复用匹配的 F/P 本地构建；不锁定 pnpm 执行版本，不更改源码 packageManager 或锁文件 |

## 4. 模块、职责与设计取舍

verifier caller 读取 preview 的 `public_tools.files`，定位 AGENTS.md row，取得该固定 fixture 的实际 source。它构造一个 custom decision，并将 AGENTS.md 排除在原 optional-conflict preserve comprehension 之外；其它文件仍按原条件 preserve。直接修改受控 caller，无新 wrapper、兼容 adapter、fallback、重试或状态字段。

tools owner 继续检查 capability 和唯一 decision，对输入副本调用原 `render_agents_ai_first_principles`，再一次调用 Fork public prepare。Fork 保留 source freshness、最终 target、mode、guard 与冻结计划。后续原 invoke 和原恢复仍消费同一计划。

测试仍使用现有 caller 合同测试，分别输入 unchanged 和 conflict AGENTS row，同时提供另一路 optional conflict。测试执行实际 caller，捕获其 prepare 输入，再交原 compose consumer；外部调用可用 mock，但不能只比较 fixture 自身。真实 public prepare/幂等/回滚另由原 `test_agents_target.py` 覆盖。

替代方案是修改 tools runtime 接受 preserve，或手改已生成 tools input；这会掩盖已发布合同与 caller 的不一致，并绕开本批真实入口，因此不采用。固定 init fixture 必有 AGENTS.md，不为假设的缺失文件添加长期支持路径。

## 5. 接口与数据

没有新增公共 API、DTO、schema 或持久化数据。使用原 file decision：

```text
path = AGENTS.md
action = custom
source = 本次 preview row.source（原 content_base64、sha256、mode）
content = UTF-8 decode(base64 decode(source.content_base64))
```

source 逐字段保留；content 是实际 preview 字节的已审查 base，不从另一份模板替换。caller 不修改原 snapshot，不预先 render，也不更改 public prepare 返回的 plan。原 consumer 的能力/输入拒绝仍保持原错误与停点。

## 6. 状态、顺序、正常与失败流程

正常顺序为真实 preview → caller 构造唯一 custom 与其它 preserve → 原 compose/renderer → 一次 prepare → 保存原 frozen plan → 一次 invoke → 原输出/终态断言。unchanged 与 conflict 只影响原 preview 事实，不决定 AGENTS 是否进入 custom。

本批无新增状态转换。source 变化、capability 不符、原 prepare/invoke 或后续 existing 检查失败时，保留原具体错误与原失败样本，停止该验证链并回原 owner 判因。不能因 prepare 错误消失就声称完整 existing 成功。

## 7. 恢复、兼容、迁移与集成

没有数据迁移或新恢复协议。原 tools 同计划 recover/resume/rollback 保留，不由 verifier 重建输入接管旧计划。原失败 work root 保留；重跑 stable existing 使用新的仓外空 root。验证执行期间源码不并发修改。

完整 existing 要求执行源的 `trellis/**` clean、source_ref 等于 HEAD，并使用真实远端 `gh:castbox/guru-trellis/trellis#H`。因此工程安排为实施/定向自检后，经原 early TaskCommit 和 Draft Publish 提供 H，再跑完整 existing；不通过临时提交、本地 provider 或生成文件 patch 绕过。Draft 不构成最终 readiness，两个副作用仍分别由其原 owner 展示精确动作。

F/P 分别复用已存在且匹配 lock 的本地 checkout。确需重建时，使用新版 `pnpm with current` 并核实际来源和构建结果；不修改 Fork/锁文件，不另 clone。源码内的 packageManager 声明与实际 pnpm 执行版本分开核对。

## 8. 验证设计

| ID | 对应要求/AC | 测试层与入口 | 预期观察及限制 |
| --- | --- | --- | --- |
| V1 | D2-R1–R3 / AC7 | 原 caller unittest；unchanged/conflict、真实形状的 source、另一个 optional conflict；实际 compose consumer | 一条 custom、source/base正确、其它 preserve保留；原 prepare/invoke各一次、plan原样消费。不是完整维护链证明 |
| V2 | D2-R3 / AC8 | 原 `test_agents_target.py`；真实 F public API、受控临时 fixture | 原 prepare、renderer幂等与回滚行为满足现行合同；不是正式远端来源或 Release证明 |
| V3 | D2-R4 / AC8 | 原 stable existing，真实 .5、匹配 F/P、已发布 H、新空 work root | 完成原 maintenance/reapply/退休资产/sidecar/终态断言；记录实际失败层，不泛化为最终候选通过 |
| V4 | 实现与分发约束 | Guru范围内存语法检查、changed-file检查、source validator、ownership、实际managed/drift与residue检查 | 变更可被当前source/runtime消费；按实际inventory判断投影影响。历史旧archive preflight拒绝仍如实报告，不为此迁移数据 |
| V5 | D2-R5与第9节双轮恢复路径 | 原独立Architecture/RDT/Check和两次完整Review；工程事实按实际依赖判断复用 | 第一轮全范围恢复审查零开放P0–P3才进入整合；第二轮完整真实公共Review记录full_review。各原owner判断当前候选；不凭测试或旧pass制造formal gate，不做空commit |

没有实际 Agent 会话、真实业务安装或生产效果的新增验收。未执行的最终新 candidate、多平台/native-host、业务和生产链继续由原发布边界单独报告。

## 9. Canonical 引用、本轮差额与实际未决项

Requirement/design/test引用沿本批PRD第7节，tools具体输入由原contract拥有；本轮只补caller和回归，不改变这些完整定义。独立候选Architecture已确认无架构影响，因此不制造contribution、ADR或project-check负担；后续候选变化仍回原owner。

本generation1、Delivery `f3ea7321-289e-4c40-be0f-75b5c5d8c21d` 保留以下双轮恢复路径，不降低为一次Review，也不继承gen0的历史例外：

1. 原early TaskCommit形成真实H，原Draft Publish提供远端同H；执行完整existing及工程验证。早期反馈仍按原workflow返回implementation/Check协调者。
2. 原Architecture/RDT评估完整候选；原完整candidate Check返回candidate_checked并合法rework回implementing。
3. 原独立reviewer以固定B/H和已激活Planning，通过 `guru-review-branch:delivery_draft_content_review` 执行第一次完整恢复审查，覆盖全部差额、完整拟写内容或实际空写集、受影响未改consumers、验证结果及边界。必须独立确认零开放P0–P3；candidate Check不能替它作判断。
4. early Review仍只返回原协调者，不写final Check、committed或公共full_review。协调者核H与内容未变后，消费仍适用的原candidate_checked进入其原router，由原Architecture/RDT owners亲自完成no-change整合；不将early Review DTO改映射为promotion输入。
5. implementation重绑实际candidate，原final Architecture/公共Check检查真实after，原TaskCommit在必要dirty时提交、在clean且准入成立时committed reentry。随后原独立reviewer执行第二次完整正式Review并真实记录公共full_review；第一轮不能代替第二轮。

该承接只覆盖第一轮载体与整合前等待，不改变公共runtime、schema或唯一consumer。候选改变、未闭合finding或出现真实共享写入时，停止当前承接，回原受影响owner修正并刷新。当前实现目标仍是两文件caller修复；不存在必要未决产品问题或待选择的单轮替代方案。
