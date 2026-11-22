# #819 Test 策略与观察

状态：integrated_pending_review。Task=819-issue-review-intake/gen0，D1=f108d161-d60d-4c89-91bf-d96004ef86a6，固定B=4f2adef1f7b099f78bb8429e8b8facd66dce3bfc。本文件单写本轮真实工程与验收观察，完整拟current策略在proposed/docs/test/current/local-fix-intake.md和issue-content.md。

## 所需证据

- T819-01/02：原Create/Clarify最小评论内容、发布/更新/只读及同对象恢复，确定性executor与live GitHub结果分开。
- T819-03：原已有Issue入口的六类分叉、三类局部返回、多缺口/阻塞及讨论/草稿/仅创建/no_issue终点；实际AI判断不由schema替代。
- T819-04：生产Sync结果经新入口/局部/刷新/完整链到当前Creation2.0/3.0，保来源三字段、独立集成目标及acquisition和原同步/恢复条件，不造被测producer结果。
- T819-05：原matching tools更新/installed/reapply、声明平台、drift、mode、sidecar与Task/session/用户内容保持；不执行完整Release矩阵。

## 当前实际观察

原Activation已实际返回delivery_started，公共readback为同D1 implementing，planning_accepted_result_id=planning-accepted:e8412d31-e550-4b5d-aee1-06d54cdb8e24。这是生命周期事实，不是工程或验收通过。

Canonical 实施已完成。配置的 `trellis-implement` 执行原生产 wrappers 与定向回归；配置的 `trellis-check` 以 quality profile 检查完整差额、必要未改消费者及完整知识拟后，并在修后补查全部差额。两者均已停写；quality 未写正式 Check/full_review/readiness 或生命周期结果。

| 实际入口 | 已取得结果与证明边界 |
| --- | --- |
| source `check-skill-packages.sh --mode source` | 43 packages、126 commands 通过；证明源码 package/command 合同，不证明 Agent 或外部动作。 |
| `test_issue_review_intake.py` | 初始完整 wrapper 集 10/10 通过；真实 Sync、三类补审/事实往返、六类分流、固定来源刷新、当前 Creation 2.0/3.0、评论及恢复均由生产入口执行。gh 替身隔离外部依赖，不算 live 写入。 |
| `test_intake*.py`、`test_discovery_exits.py`、Create Issue `test_contract.py` | 分别 16/16、13/13、16/16 通过；采用已核适用的原完整链和当前消费者证据。 |
| matching installed profile/必要完整链 | 四个局部与评论子场景、必要完整链通过；后者消费原真实 Sync transition。临时 installed fixture 与本 Task checkout 的正式 tools 采用分开。 |
| `test_issue_content_distribution.py`、`test_public_skill_examples.py`、`test_public_example_installation.py` | 共享正文真实安装/reapply 与投影通过；公开示例 3/3、安装示例通过。此层证明分发，不证明平台 Agent 实际判断。 |
| 编译与机械检查 | 407 个 Python 文件内存编译、80 个变更 JSON、canonical Bash 语法与 `git diff --check` 通过。没有独立静态类型检查命令。 |

源码自检曾发现 Sync projection 缺少 successor 所引用的原 profile schema，以及受控 transport 输入遗漏原 required `source_exit`；本批沿真实 consumer 适配。Intake 旧目录断言也曾把合法 Python `selection-v3.json` 当作业务结果残留；改用原 `runtime_residue`，继续拒绝预置业务结果，未删除环境选择或放宽生产。局部 Clarify 初版完整 3.0 载荷要求无关 duplicate 前置，实施方将其收敛为独立局部形状；修后 source 与 installed 回归通过。

质量检查实际复现了正常“正文 A 修订为 B，再发布评论 C”在公开 record 返回 `stale_identity/mutation_results`；最终 GET 校验也会误拒合法 B。原因是逐动作 preimage 与最终正文均误绑初始正文。原实施 owner 按已有动作顺序推进正文依据，最终读回最后成功 postimage；原 confirmation consumer 共用该验证，draft 原条件保留。正文成功、评论结果未定可保真实成功事实并 blocked，查回同一评论后恢复，不重复 POST。受影响 source 6/6 通过（17.030s），matching installed 两组合子场景通过（27.546s）；新增断言到达原生产 record/check/invoke，质量 owner 已检查修复全部差额。首次失败采用原公开复现，没有虚报另跑红例。

两组旧 fixture 边界保留：`test_intake_profile_integration.py` 的旧两测试有四处错误，仍提交 fixed B 已拒绝的 Task-status 或旧 confirmation 输入；未放宽 runtime 或扩成旧测试清理。额外 `test_fixed_base.py` 为四项通过、一项在 matching build 的 `.version` carrier 读取阶段出错，未到达本项行为。819 的新 ready→真实 Creation→精确 commit/同对象恢复桥接已独立通过；这些旧失败没有被改称通过，也不形成本项新增兼容或 follow-up 义务。

原 `guru-upgrade-tools` 使用本 checkout 的完整 canonical local_candidate、实际 HEAD B，以及已核定 CLI/Core `0.7.0-castbox.6`，经 read-only preview、唯一 prepare 和 invoke 返回 `tools_upgraded`，安装版本 `0.7.0-guru.8`。同一恢复引用的终态为 complete。原 installer 以 `tools_only=true`、同一 frozen public plan/recovery_ref 实际 reapply，Skills/overlays 为 ok、installed validator 通过，new_copies/managed_backups/conflicts/sidecars 为空。首次手动 reapply 调用因缺 provider runtime 导入路径在写前退出；补完整 provider 路径并使用目标已选解释器后完成，没有重新 prepare 或修改 checkpoint。随后同一原 owner 再验证返回 tools_upgraded。

目标自身 resolver 为 ok；实际 `get_context.py --mode continuation` 返回0，dogfood drift 通过，workflow、三个声明平台 Claude/Codex/Cursor 及 spec copies 与 canonical 一致。原 owner 校验 peer/common runtime 观察及物理写隔离；本 owner 另比较 3,231 个 Task/session/AGENTS/配置文件，differences=[]。公共 Delivery 仍为同一 key、implementing、原 planning accepted；check/full_review/readiness 仍为空。`formal_fork_source_lock` 明确未验证，不把本地候选采用描述为正式发布。

目标安装上的实际只读 Agent 观察为：原 Sync 固定读取 B→baseline_ready，原 Readiness existing_issue_intake 亲自复核刚回读的完整 live #819，record/check/invoke 均返回0，正式出口 ready。该 Issue 正文未变、没有评论；本次完整材料足够，没有为取得前序 receipts 重跑 Discovery/Clarify/Wording。未调用 Task router、未创建资源或写 GitHub。该观察只证明此实际直接 ready 路径，不证明所有局部分流、完整 start/selector、历史评论消费或其他平台 Agent 效果；其余分支在该观察截止时仅有生产 wrapper/installed fixture 证据；本轮新增实际 Agent 结果见下节。

前轮观察截止时，外部验收仅准备了准确评论草案，未执行；该截止保留。本轮新增实际结果见下节。当前工程与知识整合不能建立完整 AC、独立 committed Review 或 Task Completion。

## 本轮补验收：Clarify live 评论

原执行 Agent 从本 checkout 的 matching installed 公开入口，以固定 B 取得实际 `baseline_ready`。初始 standalone Clarify 因缺当前 Discovery，亲自判断并经 record/check/invoke 返回 `needs_context`；原 Discovery 读取完整 live #819、固定树 Docs、原 workflow Intake 与测试策略，完成实际重复检索、历史 preview/选择及 Gate，再经原 record/check/invoke 返回 `context_ready`。

同一原 Clarify 亲自审查完整标题、正文、原来源与精确评论。结论是需求范围、支持的正常路径、各终点及验收明确；评论只表达该需求审查，不证明实现、Task 创建或 Completion。执行前再次 GET Issue/全部评论：标题正文与已读来源一致，评论数为0，没有相同成功对象。随后唯一一次 `POST repos/castbox/guru-trellis/issues/819/comments` 成功，评论为 [6863818636](https://github.com/castbox/guru-trellis/issues/819#issuecomment-6863818636)。GET comment 及 GET Issue 均成功，评论正文逐字一致，comment id 和所属 Issue 正确；Issue 标题和正文未变。没有 PATCH。

原 Clarify 的真实 source_action/mutation_results 经生产 record/check/invoke 返回 `refresh_context`。原 Sync 再 read 同一 B，原 Discovery 重读完整 Issue 与唯一评论、刷新 duplicate/history 并采用仍适用的固定树证据，实际返回新的 `context_ready`；原 Clarify 再完成当前语义判断和 record/check/invoke，返回 `clear` 到同一 standalone caller。整个序列均退出0，没有调用 Task router或重复 POST。此结果证明本次原入口的评论发布、live 读回、同成功对象再读取和正常刷新接续；未发生响应未知或中断，不把该读回称为未知结果恢复测试。

随后补了真实评论消费观察：原 Sync 再读取固定 B，原 Readiness 的 `existing_issue_intake` 亲自重读完整 live #819 和评论6863818636，核正文未变、评论范围及结论仍适用，并完成十维判断。生产 record/check/invoke 均退出0，正式返回 `ready`，保留真实来源三字段及 Issue 身份。未为前置 receipts 重跑完整链，未执行 Task router或资源创建。此项证明当前实际评论可作为 Readiness 的材料；不把 `ready` 当创建授权、Create 新建完成或实现验收结果。

本轮曾在调用 source reader 时选择固定 B 不存在的 `trellis/skills/guru-team/runtime/tests/test_public_skill_sources.py`，原 wrapper 返回 `git_failed/path`；随后从固定树清单选择实际存在的完整 Test 策略，原入口成功。首次 Node 捕获因不可用的 `process` 对象在命令发出前失败，改用默认继承环境的标准 spawn 后继续。长 workflow/history 工具显示曾截断；完整字节仍在调用期内存，随后读取 Intake 段落、全部20个候选的问题/结果/行为和选定 #55 的完整 PRD，未以截断作为空结果。没有改写 producer 输出。

父 Agent 为核对旧独立 Clarify 的 authoring字段和 refresh分支，实际只读过 installed private runtime；没有 import 私有模块、调用测试结果构造器或伪造前序结果。因此本轮是实际语义 owner 和生产公开 wrapper 的执行证据，不能声称全程未读 private source 的独立入口隔离观察。

## 本轮补验收：实际 Agent 与隔离事实 fixture

配置的 `trellis-check` Agent 在 matching installed 原入口亲自读取材料、判断实际缺口并完成生产 record/check/invoke。临时 provider/Git/source fixture 只建立外部依赖和固定源码事实；没有用 `readiness_owner`、`local_clarification` 等测试结果构造器代替 AI 判断，没有手写 producer 通过、修改 producer 输出或重建其 transition。下表中的 Issue145、正文更正和依赖事实均为隔离 fixture；不是真实 GitHub Issue 的修改、真实用户回答或 live 外部效果。

| 实际材料及原入口 | 已完成的正式序列与语义观察 |
| --- | --- |
| A：仅补 guide 中 Ada→Hello,Ada 示例，代码/API不改；缺当前实现与测试事实 | 实际 Sync → Readiness `supplement_context` → Discovery fixed reader/duplicate/history、record/check/invoke `supplemented` → 同 Issue/source/continuation 的 Readiness `issue_review_return` → `ready`。事实证明原行为未变后，没有调用 Clarify/Wording。无评论本身没有被当作阻塞。 |
| B：同一完整正文既要求 only docs/Hello，又要求改代码为 Welcome；当前 requirements 无获采纳的输出变化 | Readiness `supplement_requirements` → 原局部 Clarify `blocked`。事实可回答，剩余是未知真实选择；`clarification_rounds=[]`，没有虚构答复。其后只更正边界外 source fixture 为完整 guide-only 正文，再实际重读同145并重新审查：Clarify `supplemented` → Readiness return `ready`。原固定 commit 和 continuation 保留，没有 Sync 刷新。这证明来源更正后的正常阻塞恢复；不是用户选择或 live Issue 修订证据。 |
| C：两处“相关”都明确只指 docs/guide.md；需求/上下文已充分 | Readiness `supplement_wording` → Wording 完整 title/body scan、实际分类与语义审查、record/check/invoke `supplemented` → Readiness return `ready`。scanner 同一行两处命中具有相同 hit_id，原合同按该 id 一条 deterministic_reference 分类即可通过；未改/删/重编号输出，未形成缺陷或修复义务。 |
| C 的同一局部调用遇到来源正常变为互斥正文 | 完整 scan 零命中，AI 仍识别真实需求冲突并 gate blocked，原 invoke 返回 `requirements_gap` → Readiness return `supplement_requirements` → Clarify `blocked`。零命中不构成语义通过。 |
| D：既有 config/调用方事实缺口，也有真实需求冲突 | Readiness `supplement_context` → Discovery 实际读 config 并 `supplemented` → Readiness 回判 `supplement_requirements` → Clarify `needs_context` → 原 Discovery 用固定树检索/reader 读取 src/client.py 并返回 `context_ready` → 同局部 Clarify 重判 `blocked`。多缺口逐次回 Readiness，事实补齐不自动关闭未知产品选择；该选择仍未回答。 |
| F：新公共可选 prefix 与 legacy consumer 承诺，使旧局部覆盖不足 | Readiness `full_intake_required` → 使用缓存的原真实完整 Sync stdout 进入 Discovery pre_task，新 duplicate/history 及完整 API/config/client/docs/tests 调查后 `context_ready` → Clarify standard_intake `clear`（真实 duplicate_snapshot）→ Wording 完整 scan/record/check/invoke `pass` → Readiness current_issue `ready`。最终为同145的 existing_issue 与固定来源；没有从最小三字段反拼 transition，也没有把旧 scope 的结果换标签。 |
| N：原请求为准备 reviewed standalone request，明确本观察不发布 Issue、不建 Task | 实际 Sync → Discovery pre_task（本地 candidate_file、duplicate/history）`context_ready` → Clarify standard_intake `clear` → Wording 完整 scan/record/check/invoke `pass` → Readiness standalone_request `ready`。无 Issue/评论字段前置；在原 Task router/创建门前停止，未创建资源。只证明原 no_issue 准备链及停止边界，不改称 proposed_draft、仅创建或创建并开工。 |
| T：原请求明确只讨论准确输出和最低验收，不发布草稿、不建资源 | 实际 Sync → Discovery pre_task `context_ready` → Clarify standard_intake `clear`，给出 Ada→Hello,Ada、仅补 guide、保代码/API，以及例子与现有测试的最低验收。caller 依原只讨论意图在 clear-router 结束；未调用 Wording/Readiness/Create。 |

上述完成序列的生产命令均退出0，实际 producer stdout 通过公开薄投影交给 consumer。A 初次 history query 装配误用 issue_number/keywords/limit，原 wrapper 返回 `schema_mismatch/query`；执行者重读公开 change_input 形状，同源重建并重试成功，没有修 producer。旧 staging facts 仅为旧输入来源；F 的判断采用当前 fixture gh source，未用旧快照覆盖新来源。

该 Agent 另有一次运输层输出预算不足造成 JSON 解析失败；扩大捕获后重新取得完整数据，未消费截断内容。B 早期两份局部 Clarify authoring 的 generated_at 使用固定时值，不能作为实际墙钟或 freshness 证据；真实次序与结果以工具调用和原 checker/current source 回读为据，后续新结果使用实际 UTC。自建临时 staging 树已清理，三个事实仓库均无 Task 条目，正式 checkout/installed/Task/shared docs 未被该 Agent 写入。

该 Agent 曾为核原完整链读取 installed private runtime/invoke.py；未 import 私有运行时或用其生成 producer 字段。与父观察相同，不能据本轮声称全程仅靠 public projection 的严格 native 隔离，也不证明其他平台 Agent。完整实际判断与生产调用、事实 fixture、matching 安装和 live GitHub 效果分别成立。

本轮没有新增实现修复或机械测试矩阵。新证据补足局部返回、多缺口、阻塞/正常来源更正恢复、必要完整链、讨论及 no_issue 准备终点。该观察截止时，正式 Issue 草稿创建、仅创建的 created 终点、创建再开工及其未知结果恢复仍需合法 live 对象，不能由这些 fixture 填成完成；随后的一次性工件 live 结果见下节。完整 start/selector 与原 Task 资源创建没有在这些观察中执行。

## Create live 对象调查（原截止）

原 implementation Agent 只读核对 D1 implement、MIGRATION-819、当前 Issue 内容 Test、#153 历史计划/Test及 repo-bound GitHub GET。#153→#619 是当次明确安排的一次性验证；#619 当前已关闭，不能用作本轮新 Create 完成语义证据。#818 摘要草稿被当前 Test 明确限定为示例，不能提升为待创建产品需求。限定范围内未取得当前真实未创建请求或专用验证对象的用途、范围和结束处置。

该调查截止时未调用 Create 或 recover；recover 本身可能补发评论，不能当只读探测。合法后续需要真实待创建请求，或有明确来源的专用验收安排，再经原完整草稿链准备完整 repo/title/body/labels、评论、结束处置与原入口计划。历史对象或本地 fixture 不能替代这项缺口，也没有新建测试 Issue。

## 本轮补验收：Create live 工件 #836

在明确一次性工件用途、范围及结束处置后，原 owners 对完整草稿实际执行 matching installed 公开链：Sync `baseline_ready` → Discovery `context_ready` → Clarify `clear` → Wording `pass` → Readiness `ready`，最终 `target.kind=proposed_draft`。每阶段 record/check/invoke 均退出0；完整正文保真实工件用途、原顺序及不建 Task 边界，不把它伪装为待实施产品需求。Wording 完整 title/body scan 零命中，仍独立检查完整语义。原 Create 复制真实 ready target、核空 labels 和准确评论，公开 `record_plan` 返回 ready；该 receipt 未被当作创建结果。

后续执行前，原 Create 重新读取真实 repo、labels、全部状态的同用途候选及 #819 来源，完整读回获审标题、正文和评论，确认仍适用；没有既有成功对象，不改旧审查结果或仅改时间伪装复核。原新建输入使用该次真实复核时刻，公开 record_plan 与唯一一次 invoke 均退出0，正式返回 [#836](https://github.com/castbox/guru-trellis/issues/836) `created`。原 executor 完成创建、正式内容 GET、评论 POST 和评论 GET，随后 Issue-only 终点结束。只有一条审核评论 [6869393432](https://github.com/castbox/guru-trellis/issues/836#issuecomment-6869393432)；标题/正文/空 labels 与获审输入一致，Issue/comment 原生 attempt marker 保留，comment id、正文和所属 Issue 均经实际 GET 核对。

关闭前，原公开 dispatcher 的 `check_result` 使用同次原始完整 Create 输入及原 reviewed_at，退出0并在中间 receipt.result 查回同一 `created/836`。核验前后 title/body/comments/updatedAt 一致，没有重发 Issue 或评论。该入口只读；本轮未调用可能补发评论的 recover_result，也没有响应未知、输出丢失、故意中断或故障注入。因此证明的是已成功对象能被原只读查回，不把它写成真实未知结果/缺失评论补发已验证。

随后从实际 Sync read 同一 B 进入独立 `existing_issue_intake`，原 Readiness 读取完整正式 #836 和实际评论，亲自完成十维 record/check/invoke，均退出0，正式出口为 `blocked`。原因是工件没有可供新 Task 实施的独立工作范围；创建与只读核验已完成，剩余本次观察和关闭沿工件处置，不虚构产品差额。没有将草稿 receipts 改写为正式 Issue pass，也没有因评论存在放行 Task。该停止只针对836的Task入口，不将其转成819实施阻塞。

观察整理后仅关闭 #836，不追加关闭评论。北京时间2026-11-14 09:32:07，GET核实 `CLOSED / COMPLETED`；title/body/labels/评论及其所属 Issue 全部保持原样。#819仍为OPEN且正文未变，Task/gen0/D1仍implementing；没有新Task、branch、worktree、stage、commit、push、PR或merge。关闭仅表示工件观察结束，不是819实现、交付或Task Completion结果。

本轮未改生产机制、接口或验证义务，未重复已有足够机械测试。原 RDT 只维护本 Test 的当前结果与证据截止；六个完整current/proposed目标及Architecture决定/关系保持，仍为 integrated_pending_review。Architecture单元此前对Clarify评论的限定仍只描述那次观察，不能改读为本次Create未发生；新工件结果由本节单写。

### 创建后开工的剩余边界

本次836证明完整获审草稿→真实创建/评论读回→Issue-only终点、同成功对象只读查回及正式Issue的独立Readiness判断。它没有真实待实施产品工作，因此不能承接创建后 `ready` → 原Task router → 原Create Task写前语义/精确计划的live正向观察，更不能为补证创建无意义Task。

该正向入口仍需要明确请求开工、尚未交付、范围清楚且有实际消费者与可观察验收的真实工作对象。原Create Task另需判断来源disposition、固定来源commit与acquisition、独立集成branch/delivery_target、日期/TaskId、checkout/资源身份和副作用边界。评论或ready均不能代替这些条件。既有fixture的当前Creation桥接继续按其层级采用，不升级为live全链；本项AC不因工件完成而默减或宣称全通过。

## 未验证边界

Create的本次live创建/评论和同对象只读查回已取得上述结果，真实未知响应、输出丢失或缺失评论补发仍未发生；Clarify的live PATCH和未知响应恢复也未发生。实际分流与终点按上节观察分别记录，不以机械覆盖替代。完整多平台 Throwaway、官方 upgrade/update/Release、formal_fork_source_lock、其他业务仓采用、生产效果、TaskCommit、独立 committed Review 和 Task Completion 均未验证。

