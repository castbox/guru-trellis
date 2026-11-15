# D1：诊断实施与验证计划

## 1. 输入与引用

整体 accepted scope 为根 `prd.md` 的 R1–R8、AC1–AC4；本批 `prd.md` 承接全部范围。来源技术约束只在 `design.md` §3维护处置；本文件不另建矩阵。首次 D1，无前序交付。development B 为 `a72981db56d2070d8140b468cab3a97ae82effd3`，PR目标为 main，精确候选在实际实现后用原 constructor 形成。

实施前读取：本批三正文和整体 PRD；原 Author `references/planning-body.md` 及三份 Delivery 模板；`.trellis/workflow.md` §2.1 和 `workflow-contract.md` 的 Phase2／Candidate Applicability And Coverage；quality-guidelines 的 Test And Validation Value／Validation Scope Ownership；原 root 的 applicability／contract 与 causal-completion-semantics；R735／D735／T735 三个完整单元；design §1 的 Architecture authority。consumer连续性与Reconcile触发的完整条件沿根PRD S3–S5的唯一源，不在派工prompt另塞答案。

本 Task 的正式实现 worker 仍读取这些上下文。被测的隔离 Agent 只获得 design §5 的正常 fixture 工作上下文，两者不能混用；不能把本 Task正文作为被测输入。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、owner、文件和具体动作 | 可审核完成观察 |
| --- | --- | --- |
| I1 当前入口与证据适用性 | D1正式激活后，原实施协调owner在已验证checkout读Phase2原入口、必要共享方法与既有行为材料；实施worker受其边界约束 | 本D1 `validation/diagnosis.md` 只记原入口、消费线索、适用已有事实及真实缺口；不先宣称需修复 |
| I2 中性事实装配 | 当前行为证据不足时，配置的实现worker扩展 `trellis/skills/guru-team/packages/guru-qualify-root-cause/tests/run_behavior_validation.py` 的CASE/fixture分支，并在其 `tests/fixtures/shared_dependency/` 准备design§4的源码、调用、依赖与观察材料 | 复用既有provider/upstream fixture/native采集；被测工作区无#853叙述/host预期/evaluator代码，材料身份与实际文件一致；原cases保持 |
| I3 原入口行为观察 | I2装配可用，原实施owner通过匹配managed Python、真实upstream scripts运行 `shared-material` 和 `shared-ordinary`，外置输出，`--jobs 1` | 实际prompt、工具、读取、结果与失败事实齐全；不预写语义答复，不用脚本grader判pass |
| I4 诊断与最小处理选择 | 原实施owner亲读I1–I3事实，并由原审核owner判断覆盖；根据具体缺口调用原root资格和受影响Author／Architecture | 形成有依据的消费缺口、具体方法缺口、无需追加修复或仍需诊断结论。若要改规范内容，先保留同D1合法rework，补精确规划并重进受影响原门禁，未经该步骤不写方法 |
| I5 定向验证／知识职责 | 无修订时原owner核V1–V5与最小Task结果；真实修订则原内容owner执行受审差额，原tools/RDT/Architecture owner按修订后计划承担同步和整合/readback | 机械、行为和分发结论分开。当前方法未变不制造投影/贡献；真实变更不得漏必要consumer或共享知识 |
| I6 正式质量与交付 | 原实施协调owner在完整工程自检后准备TaskCommit；真实Git副作用另展示确认。随后固定完整B..H，原独立Review实际承担Check/full_review及适用Architecture before/after，原readiness再接Publication | 不以局部命令、规划或collector退出替代门禁；当前不授权commit/push/PR/merge。Delivery事实后仍由整体Completion／Closure／Finish判断，合并前等待协调器 |

I1的静态路径不能替代I3实际行为；已存在且适用的同等当前行为事实能回答时由原owner说明采用依据，不机械重跑。I4不是新增日常gate，是本Task接受范围要求的诊断与修复选择。没有已定后继Delivery，不因诊断未完创建新identity。

## 3. 验证入口、输入与预期观察

V1–V6的独立观察与边界由design§8唯一展开。当前先诊断，再决定是否修订。先核fixture与依赖，再做低成本机械检查和原生行为观察；不采用固定“红→修→绿→回退再红”。所有下列命令是计划，尚未执行。

匹配依赖：安装声明的Trellis commit为 `e3793251fad8bd261d0c370d408c7675b9f6a140`。本机可用干净源码的scripts目录是 `/Users/wumengye/Documents/GoProjects/Trellis/packages/cli/src/templates/trellis/scripts`；只读复用该路径，执行前核HEAD与声明一致，不改upstream或全局CLI。源码不可用时报告该具体设施缺口，不换成伪造Task/Delivery model。

collector命令在I2真实增加case后执行。临时输出目录由执行owner运行时创建；以下仅用于本地fixture，不创建本仓新worktree或正式Task，也不触及远端：

```bash
SHARED_DIFF_RUN=$(mktemp -d /private/tmp/guru-853-native.XXXXXX)
GURU_UPSTREAM_DELIVERY_SCRIPTS=/Users/wumengye/Documents/GoProjects/Trellis/packages/cli/src/templates/trellis/scripts \
PYTHONPATH=trellis/skills/guru-team \
bash trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime \
  -B trellis/skills/guru-team/packages/guru-qualify-root-cause/tests/run_behavior_validation.py \
  --source . --output "$SHARED_DIFF_RUN" --case shared-material --case shared-ordinary --jobs 1
```

原fixture在外置项目建立测试Git提交、schema2 Task／Delivery／Planning前置，仅服务声明边界；这些不属于本仓正式Task、业务提交或阶段通过。原生进程为既有 `codex exec --ephemeral --json --cd <fixture workspace>`，启动prompt只定位正常Phase2责任与中性事实，host预期不进入工作区。

host原owner读取每次实际 `prompt.txt`、`native.jsonl`、`native-final.txt`、facts及被读取源码，再写本D1最小 `validation/diagnosis.md`。V2应能从事实判断实现／增量／调用与证据范围及具体必要后继，V3应保留无影响变化与适用事实的正常承接。只返回预期词语、未读事实却碰巧答对、设施未启动、模型断流或缺必要消费依据均保留其实际证据缺口。

V5选择collector真实装配、命令传递、host/model隔离和失败传播的定向单测；复用实际helper而不复制其逻辑或固定产品文本自证。修改Python按quality-guidelines Python Syntax Check做内存AST；检查新/改文件的whitespace。官方context校验命令：

```bash
python3 .trellis/scripts/task.py validate .trellis/tasks/11-15-853-shared-dependency-diagnosis
git diff --check
```

不为fixture未运行的SDK组合或生产效果填成功。V6只在后续精确修订确有分发差额时执行原tools同步及package/installed/platform/reapply/drift/sidecar/mode检查；完整Release矩阵与外部业务采用不在本批验证范围。

## 4. 停止条件与适用回退点

每次实施写入前用原 `check-task-checkout-boundary.sh --json --task .trellis/tasks/11-15-853-shared-dependency-diagnosis` 验证身份；错误回原owner，不手工重建映射或覆盖其它工作。scope/source实质变化回Clarify；新诊断／修复机制或Architecture边界变化在写对应source前回原资格及最早受影响Planning。固定B不因远端推进重选，只有真实必要整合进入Reconcile。

fixture装配、依赖或原生启动失败保留原错误，不能当产品行为失败或通过。设施反复失败时只修能回答同一未决问题的装配，或选择更直接受支持入口并说明等效边界；仍不足保留验收缺口。追加诊断须指出现有证据不能回答、且影响结论的具体问题；已充分后停止，不为数量/阶段/换执行者重跑。

本次无生产数据或发布操作，不造回滚协议。临时fixture只保留直接评估需要的事实，原始日志不搬成长期转录。原结果输出丢失先恢复实际输出，不重放外部动作。存在真实受管改动时沿原tools处理`.new/.bak`，不手工覆盖副本。不得把加长prompt后的单次成功作为修复证据；修订后的验收必须从正常入口确认。

## 5. Delivery Policy（唯一）

`full`：D1覆盖全部根R1–R8、AC1–AC4，当前没有划给后继切片的未交付范围。独立交付条件是：定位当前消费/具体方法缺口并完成必要最小修复及适用行为证据，或者以足够当前依据确认已有能力满足目标无需追加修复；仍需诊断不满足交付／Completion条件。

当前可激活的是具体有界诊断、fixture和证据工作；未选定的规范性修复有明确前置：I4根据真实证据形成机制，经原资格和受影响Planning门禁及真实计划展示/接受后才实施。该限制只作用于未知修复，不冻结同D1已获支持的独立诊断工作，也不转移整体完成责任。

验证边界为Guru原入口的当前方法消费与共享差额判断、机械事实装配及实际受影响分发；不是原业务生产修复或完整多平台Release证明。原实施owner承担后续具体修复/补证，整体Completion负责所有接受范围，Delivery合并不替代Task完成。无修订分支仍需真实当前行为依据；无后继不等于验收已经通过。

## 6. Docs SSOT Plan（唯一）

`strategy=no_docs_update_needed`，适用于当前仅有界诊断和test-only事实／采集增量。原因是没有选定规范性方法、入口、API、Architecture决定或共享知识定义的变更；现有R735／D735／T735与canonical消费者连续性、Author、Reconcile方法仍是唯一完整来源。本D1最小validation正文记录实际诊断依据和边界，不复制这些方法为第二current，不改根导航或预建空contribution／ADR。

原RDT owner在I5核对实际结果是否仍符合此依据；Check／Review消费该真实判断而非Policy标签。若诊断确认需要规范性修复，I4先由原Author把Docs Plan改为精确命中单元与delta；原RDT writer准备真实task-owned完整proposed定义和关系，原Architecture owner判断自身差额。批准规划、实施和真实工程自检后，各原maintenance owner在TaskCommit前final_integration/readback；实际committed Review覆盖after。当前no_docs结论不授权跳过真实修订的知识整合，也不预写共享current。
