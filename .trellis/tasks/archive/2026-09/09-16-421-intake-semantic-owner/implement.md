# #421 实施与验证计划

## 范围与状态

仅承接 live [Issue #421](https://github.com/castbox/guru-trellis/issues/421) 的四步 standard Intake。Task Commit 已暂停，旧提交候选和 Phase 2 checkpoint 已移除。当前修复 P1-421-full-aggregate-grading：完整 full/mixed run 保持完整 aggregate identity，只更新 Intake semantic rows，non-flow 行全部保持不变。a95a65a 的 Phase 2、native binding 和 Branch Review 不作为本轮通过依据。

本轮工作：
1. 撤出 guru-check-task 的 canonical、installed、Shared/Codex/Claude/Cursor 全部任务改动，保持其 HEAD 基线合同、criteria 和测试。
2. completed-run 两阶段补评分在 focused 或含 Intake 的 full/mixed run 中只更新声明 native_authoring_flow=standard_intake 的行。先验证完整 case/side identity，评分只接受 Intake assertions；non-flow 全部字段、顺序和原始证据不变，重算 aggregate。没有 Intake 的运行保留原行为。
3. 保留显式最小资产投影、封闭读取清单和 examples/evals/private runtime 不投影；保留真实拒绝额外读取的测试。
4. 修正后重新运行 source/installed tests、平台 parity、all-platform reapply、dogfood drift、secret/residue hygiene，以及全新 full Codex run-root、两条 Intake 的独立语义评分和同次正式评分消费；不得复用旧完整运行或拆换 case 集合。
5. 基于最终工作树执行 fresh Architecture phase2 与完整 guru-check-task，之后进入 Task Commit 的独立确认门禁，并对新的 exact HEAD 执行完整 Branch Review；fresh Branch Review 通过前禁止 Publication、push 或 PR。

## 文件边界

| 集合 | 责任 |
| --- | --- |
| 四个 Intake package SKILL.md、contract、tests | 当前 AI 亲自履行 owner 职责与生产公共输出承接 |
| Readiness eval corpus 与两份 source facts | 完整成功链与真实 scope conflict，无预填语义结果 |
| adapters/eval 下 Intake staging、projection、trace 及必要 caller | 事实与原命令转发，不生成判断 |
| runtime/eval_runner.py 与 Intake/评分定向测试 | flow 专属同次执行评分；未声明 flow 原行为保护 |
| eval corpus/request/trace schemas | eval-only closed flow，不改变生产 I/O |
| canonical specs/README 与受管副本 | 复用 prd.md 唯一 Docs SSOT Plan |
| 当前 task 六文件 | 范围、设计、实现与 check 上下文 |

## 验证矩阵

| 组 | 当前通过条件 |
| --- | --- |
| V1 | 四个 Intake package tests、Intake adapter/allowlist/semantic-grading tests、受影响 shared adapter/runner 定向回归全部通过 |
| V2 | 两条 fresh installed/native Intake 完成实际 owner authoring；首次缺评分不通过，独立审查后原同 run-root 正式补评分，无模型重跑 |
| V3 | 完整 Codex raw 缺 Intake 评分而失败；同 root 仅 Intake grading 后 aggregate 可 passed，non-flow rows 序列化 bytes/所有字段与原始文件不变；case/side/assertion 缺失、重复、未知及 non-flow grading 均拒绝；focused 与纯 non-flow 原路径保持 |
| V4 | source/installed packages、四个 owner 平台 bytes/mode 一致，guru-check-task 各投影与 HEAD 相同 |
| V5 | apply.sh --repo . --all-platforms 后 drift 为零；逐个核对本任务备份，无 .new/.bak/bytecode/credential residue |
| V6 | task.py validate、完整 dirty diff scope、whitespace、fresh Architecture/Phase 2 通过 |

使用 managed Python 和 PYTHONDONTWRITEBYTECODE=1。不以 transport/mock/schema 通过代替 native 语义审查。失败保留真实结果；未完成验证明确阻塞。完整多平台 clean/update/exact-candidate Release Gate 属于 #410，不在普通 Issue 内扩张。任何其它 owner 或通用 eval 生命周期问题需独立 Issue/task，本任务不创建这些资源。

## 当前结果

当前起点 HEAD 为 a95a65a94ad148b0c6b87223dcf0b68f0115dab6，base 为 origin/main@78651e2068184e9e52a778fe33eda8b2bd7c8e0b。独立复审 P1 已正式返回 implementation_required，Publication 停止。旧已提交版本与历史 native 结果保留，不将其作为当前修复通过证据。

本轮新增修改为 runner、对应评分测试、原规范/README 和任务设计说明，保留 Wording receipt 回归与最小 allowlist。为消除已观察的 Codex 默认模型不受账号支持这一运行前提，增加可选 --codex-model，仅选择 corpus 未固定模型的 Codex case；扩展 eval adapter request 的既有 model_id 适用条件及 native argv 和定向测试，不改变生产 I/O、固定模型、其它 adapter、评分或生命周期。

完整聚合修复首轮结果（早于可选模型选择，本轮不可复用为 native 通过依据）：
- runner 仅将评分集合及更新循环过滤为 Intake cases，保留完整 aggregate identity 校验并重算整体状态。non-flow 行不进入 completed validation 或更新循环；纯 non-flow 原 dispatch 不变。
- 16 项 semantic-grading tests 及 10 项既有 runner/qualification 定向回归通过，独立只读 checker 复跑 26 项通过。真实 transport/helper/validator 测试覆盖 full 7-case、comparison 14-row 的 raw 缺评分失败到 passed，并证明 non-flow row 序列化 bytes、顺序、字段及原始执行文件不变，non-flow 失败不被洗绿。
- 本轮 source 四包 88、installed 四包 88 项通过（两种布局重复覆盖，不相加）；Intake 13、projection 3 项通过。all-platform reapply、23 source/installed packages、dogfood drift、语法/JSON/diff check 通过。4 个安装备份经 preimage 核对处理，测试 bytecode 清理后无残留。
- 全新完整 Codex run-root：`/private/tmp/guru421-fullfix-native-eywxLe`，未预置 grading、未筛选 case，实际执行全部 7 个 case，raw aggregate 为 execution_error，不复用 a95a65a 的 native binding。
- success Intake 的真实 wrappers 已到 ready，但 native 最终回复多出右花括号成为非法 JSON；独立 native-four-owner-review 为 false，该行保持 execution_error。conflict Intake 独立 native-conflict-review 为 true，原同 full run-root 消费 grading 后从 missing-grade evaluation_failed 变为 passed。
- 同一 full selection/root 的 grading 只含两个 Intake assertions，原入口成功消费，无 mixed rejection；complete identity 和五条 non-flow row 字节一致，49,554 个原始执行文件均未改变。aggregate 继续 execution_error，没有通过评分覆盖失败。
- non-flow ready-route 与 refresh-context-route 因默认 gpt-4o-audio-preview 不支持当前 ChatGPT 账号而 execution_error；其它三条 non-flow 通过。原状态、输出、时序和诊断全部保留。未更改模型选择或其它 Skill 行为。
- 实际全链通过仍有验证阻塞，不能创建 Task Commit 或用旧 Branch Review 放行。先执行 fresh Architecture/Phase 2 如实收口；通过前不提交、push、PR 或 Publication。完整 Release Gate 仍归 #410。本轮临时 auth.json 已删除，旧提交/证据/stash 保留。

## 可选模型选择轮验证（历史）

- 新完整 installed Codex run-root 为 `/private/tmp/guru421-model-full-RII42R`，使用 `--codex-model gpt-5.6-sol`，无 case 筛选或预填 grading；全部 7 个 case 执行完成。五个 non-flow case 的实际 argv 均包含指定模型，全部通过，原默认模型不支持问题不再出现。
- success Intake 真实 wrappers 到 ready，但 native 最终 stdout 在零基位置 3249 多出 `}`，独立评分为 false；该行保持 execution_error，不清洗输出、不以 wrapper ready 或进程 rc0 替代验收。conflict 独立评分为 true，真实 Clarification blocked 后停止，未虚构用户答案或继续下游。
- 原入口在同一 full selection/root 正式消费仅两条 Intake 评分，结果为 6/7 passed、aggregate execution_error。前后逐项核对五条 non-flow 的序列化内容、完整 case 顺序、全部行的非评分/状态字段，以及 current 和模型可见目录的原始执行文件内容与 mode 均未改变。未再次调用模型。
- 当前模型选择 6 项、semantic-grading 16 项复跑通过；前序本轮 Intake 13 项、projection 3 项及固定模型回归保留。all-platform reapply 已完成，fresh dogfood drift、workspace boundary、diff check 与 task context validate 通过；context validate 提示既有大 spec 自动注入会截断，审查须直接读取适用正文。无 sidecar/bytecode 残留。
- fresh Architecture phase2 返回 baseline_current / no_architecture_impact。实际成功链最终 public output 仍不合格，完整 Phase 2 不能 passed，不进入 Task Commit、Publication、push 或 PR。完整多平台 clean/update/exact-candidate Release Gate 仍由 #410 承担。
- 本轮临时 auth.json 已删除；失败运行、原始回执、已有提交及 stash 保留，不以旧轮结果替代本轮验收。

## 终态传输修订后的当前验证

- 根因定位为 native 模型转写最终回复时追加括号，实际 wrapper stdout 合法。仅在 Intake context 增加三句模型侧 JSON 解析、缩进呈现及完整性核对指引，补三条原 context 测试断言；parser、validator、trace、grading、argv、schema、owner 与结果通道不变。设计同步说明既有 JSON 空白归一化边界，不新增 host 修复或代答。
- source 四包 88 项、installed 四包 88 项通过（相同覆盖的两种布局，不相加）；Intake 13、projection 3、semantic-grading 16、model-selection 6、qualification 固定模型 1 项通过。installed 首次测试启动缺 PYTHONPATH 导入失败，修正启动环境后通过，未修改代码规避失败。独立只读检查未发现本轮三句增量问题；静态断言不替代 native 证明。
- all-platform reapply 产生一个 native_adapter.py.bak，与捕获 preimage 一致后处理；第二次 apply source/installed 23 包通过，drift、diff check 和 sidecar/bytecode 扫描通过。guru-check-task canonical/installed/平台投影保持 base 原样。
- 全新完整 Codex run-root：`/private/tmp/guru421-terminal-full-5Q2bxf`。原始运行不带 grading、无 case 筛选，7 个 case 的 exit/schema/trace 全通过；两条 Intake 因缺独立评分使 raw aggregate 为 evaluation_failed，符合 fail-closed。
- success 的真实四步结果为 context_ready、clear、pass、ready；最终 70 行 JSON 与实际 Readiness invoke 输出对象完全一致。conflict 识别互斥范围并真实返回 Clarification blocked，未虚构问答，未运行 Wording/Readiness/workspace。两条完整 transcript 的独立语义评分均为 true；所有同次 authoring/命令错误及恢复保留在原始证据中。
- 原入口消费同一 full selection/root 的两条独立评分后，7/7 passed、aggregate passed。仅 Intake semantic_results/status 及 aggregate 更新；五条 non-flow 行序列化内容、case 顺序、非评分/状态字段和 49,721 个原始执行文件内容/mode 均保持不变，未重新调用模型。
- 审查观察到 Readiness 一处辅助 evidence_refs/affected_hashes 标注不精确；实际 source 已审查，recorder 派生标题/正文摘要与原始事实相符，真实公共身份未改变。按 Issue #421 及既定 native criterion 的范围审查，不将其扩大为继承合同全部证据元数据的全面合规测试或 validator 修改；原观察保留，不宣称该 native 评分证明所有字段细节，也不制造 required follow-up。
- fresh Architecture phase2 为 baseline_current / no_architecture_impact。本轮定向验收已具备进入 fresh guru-check-task 的证据；Task Commit 仍需独立门禁与确认，新 exact-HEAD Branch Review 之前不进入 Publication、push 或 PR。完整多平台 clean/update/exact-candidate Release Gate 仍属 #410。
- 本轮临时 auth.json 已删除，旧失败运行及原始回执、已有提交、stash 全部保留。
