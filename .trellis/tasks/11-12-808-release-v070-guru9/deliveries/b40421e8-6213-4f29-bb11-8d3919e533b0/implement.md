# D1：v0.7.0-guru.9 完整来源实施与验证计划

## 1. 输入与引用

Task 为 `808-release-v070-guru9` / generation `0`，Delivery 为 `b40421e8-6213-4f29-bb11-8d3919e533b0`，profile 为 `pull_request`，PR 目标为 `main`。本批选择 AC-01、AC-02、AC-03、AC-05、AC-06。范围、完整条件和剩余责任见[本批 PRD](prd.md)及[整体 PRD](../../prd.md)第3.3、5.4、5.5、7节。规范性来源的唯一处置见 [design 第3节](design.md#3-来源设计处置唯一)，不在此重建矩阵。

本批没有前序 Delivery。固定开发基线 B、其来源及 Planning H0 见 design 第1节；未来实际候选保持完整 B..H，不随 fetch 改写 B。六项发布输入保持不变，CLI/Core 为 0.7.0-castbox.6，Fork 来源从 canonical lock 派生。

本次实际 requirements_ready 后，原独立 Architecture 的新 candidate_assessment 返回 baseline_current / architecture_impact / target_native。design 第4.4节的真实隔离贡献维护 ARCH-DOM-010/ARCH-INT-015，保持既有 D1完整来源→真实 delivered→原 Completion/Creation→D2实际采用机制，不新增 ADR。该结果不替代 Wording-current final_plan、Approval 或 Activation。原单 Delivery 的 GAP-SOURCE-01/blocked 仍是历史失败观察，不能改记 pass；新的顺序尚须实际执行证明。

实施前必须完整加载下列适用引用及关联条件：

- 本批 design 第1～9节：模块、版本五面、真实回归、来源样本及未验证边界。
- MIGRATION-794 第1～5节：当前原 owners、TaskCommit 唯一 consumer、两槽 Review、旧入口退出及在途恢复。
- 私有 release 合同的 Stage 1、Stage 2、恢复、独立副作用和禁止持久化边界：本批迁移对象及保留责任。
- 原 TaskCommit、Review、Delivery Review、Completion、Creation 和 tools 的 SKILL、Interface 与命中合同：真实调用及后继责任，不复制第二公共协议。
- `.trellis/spec/workflow/quality-guidelines.md` 的 Test And Validation Value、Validation Scope Ownership；`.trellis/spec/docs/public-docs.md`：断言与证据层次、最小定向验证和三个 README 分工。
- design 第9节的 R794/D794/T794、Architecture authority/constitution/change-contract：知识差额和原整合边界。

## 2. 有依赖顺序的步骤与文件责任

下表是未来执行计划。本次只刷新规划，不实施、不安装、不生成候选或后继 Delivery。

| 步骤 | 前置与原 owner | 实际文件、动作及可审核产物 | 完成观察与后继 |
| --- | --- | --- | --- |
| S-01 收敛当前 Planning | 当前 requirements_ready 和新的 candidate_assessment；原 Author | 完成同 planning_root 三份正文和官方 implement/check JSONL，自检 scope、来源处置、staged Policy、Docs Plan 和可执行验证 | 实际 plan_ready 后交 Wording；后续 fresh final_plan、Approval、完整展示/接受和原 Activation 均须真实发生。本段停在这些后续 gate 前 |
| S-02 对齐版本直接消费者 | 当前计划已接受且原 Activation 成功；实施 owner | 修改 design §4.1 六处：canonical manifest、guru-upgrade-installation TARGET_GURU、该包 output schema、该包及 shared stop consumer schema、active public-upgraded-output.json。将当前目标对齐 .9；CLI/Core、选定来源自身 lock、公共 shape、历史版本不改 | 实际 formal source/installed_version→三 consumer 及 active example 的原 source validation 成立，不只比较版本字面；未来 D2 可使用完整来源 |
| S-03 迁移私有编排与回归 | S-02 及当前原接口；私有实施 owner | 改 Shared release contract 并同步 Codex/Claude/Cursor 三份合同。实际入口变化才同步四份 SKILL.md。迁移 Shared tests/test_contract.py 的旧 Task/status、initial_commit、branch_review/Check fixture，触达当前公开 producer/consumer | 逐 Delivery 原完整链成立；D1 delivered 后才接原 Completion additional_delivery_required→Creation→D2；没有 early commit/tools 插入、固定第二轮或 planned failed Review。Stage 2 和私有排除分发保持 |
| S-04 来源入口、公开文档与工程验证 | S-02/03 的实际 after；实施/docs owner | _install_workflow 统一复用原公开 Guru custom init 参数，local_sample 其后仍原 copy 本地 canonical workflow。移除本批 local_workflow_template 参数、known native hash 例外及失去 consumer 的测试增量；原未知漂移、非 local 路径、guard 和 bootstrap 保持。补真实 custom-init/样本字节行为回归，按第3节完整运行 focused+同项目全平台投影验证。更新三个 README 的受影响完整章节；当前 Fork 表改为 canonical lock/build recipe 引用 | 来源自身版本、接口、依赖、完整安装/平台投影可用性有实际结果；.9未发布与.8稳定事实分明，不以样本证明 eafc 已采用 |
| S-05 必要知识整合/readback | S-02～04 的真实差额与工程结果；原 RDT/Architecture owners | 原 RDT owner 核现行 R794/D794/T794 的实际适用性。原 Architecture 对本批真实贡献及 ownership/distribution 两完整 proposed targets 执行 delivery_promotion(final_integration)、expected-current 核验、实际写入/readback；不改 root/index 或 proposed ADR 状态 | 全部 D1 after 与必要关系完整进入待审内容；Architecture 仅 integrated_pending_review，之后由固定 committed Review 判断 reviewed_promoted。整合改变内容时补受影响工程验证 |
| S-06 完整本地提交与独立 Review | 本 slice 完整实施、必要工程验证及知识整合/readback；原 TaskCommit、implementation、Review | 原 TaskCommit 精确 prepare/invoke 或合法 clean reentry，实际 pre_review_committed 只交唯一 router；原 constructor/begin_check 固定完整 B/H/paths。新开且未参与实施的 reviewer 同次完成 Architecture before/after、九维与 full Review | 真实 check/full_review 两槽和当前 passed 齐全；修复回原 writer 后继提交，保 B 并审全部差额/组合影响。零开放 P0～P3 后才接 readiness |
| S-07 D1 发布与合并 | 当前完整 Review、publication Architecture eligibility；原 Delivery Review/Publication/Merge | 审完整 D1、剩余采用责任、真实旧安装/drift观察及中文 Refs #808 payload。仅当前 ready 才执行已审 push/PR/Ready；每次 Merge 前向 coordinator 展示精确 expected head 并停止 | 原实际 delivered 形成后继可消费来源；不关闭 #808，不声明实际采用、Task Completion 或 Stage 2 通过 |

S-06 的两个原 pre_review profiles 均保留完整前置；不为取得来源提交增加特例。D1 自身所有必需验证必须在完整候选中成立，不能将失败挪给 D2。

S-07 之后，原 Completion 对剩余实际采用返回 additional_delivery_required，原 Creation 才建 D2。D2 读取真实 D1 delivered、完整干净匹配来源及自身 lock，完成新 slice Planning/Activation 后，由原 tools 执行 source_locked。D2 承接全部受管 package/platform/workflow、installed/native、preservation、ownership、mode、sidecar、parity/drift，以及全部安装 after 的完整提交/审核/交付。本段不创建、选择、规划或执行 D2。

## 3. 验证入口、输入与预期观察

### 3.1 定向长期回归

以下命令均供未来实施后执行，本次规划未运行。先由原 resolver 核实当前 managed runtime；缺失回原 owner，不用全局依赖替代。私有回归在临时 Git fixture 中执行当前公开链，不操作真实业务仓或远端发布：

```bash
TRELLIS_DELIVERY_API_COMMON="$PWD/.trellis/scripts/common" \
  bash .trellis/guru-team/runtime/resolve-python.sh \
  "$PWD" "$PWD/.trellis/guru-team/runtime" \
  -m unittest discover \
  -s .agents/skills/release-guru-trellis-version/tests -p test_contract.py
```

fixture 只建立测试声明边界前已合法成立的前置状态，包括 Planning。被测 TaskCommit 必须真实 prepare/invoke 产生提交，constructor/begin_check 真实固定 Candidate，Review record/check/invoke 真实生成两槽，下游实际消费当前结果。不能在 fixture 中直接种被测 producer 应产生的结果。显式 fixture semantic 判断及远端替身只证明组件合同，不证明真实独立 AI 或 GitHub 成功。

本节三个版本回归使用 canonical 测试，installed package 不含 tests。先将两个 formal-source fixture 改为随真实当前目标构造，保留普通 canonical dirty/untracked 来源拒绝语义，不全仓替换历史 .8。实际执行三个适用用例：

```bash
bash trellis/skills/guru-team/runtime/resolve-python.sh \
  "$PWD" "$PWD/trellis/skills/guru-team/runtime" \
  -m unittest discover \
  -s trellis/skills/guru-team/packages/guru-upgrade-installation/tests \
  -p test_contract.py -k test_delivery_upgraded_result_matches_source_and_public_consumer

bash trellis/skills/guru-team/runtime/resolve-python.sh \
  "$PWD" "$PWD/trellis/skills/guru-team/runtime" \
  -m unittest discover \
  -s trellis/skills/guru-team/packages/guru-upgrade-installation/tests \
  -p test_contract.py -k test_formal_source_requires_committed_clean_canonical_candidate

bash trellis/skills/guru-team/runtime/resolve-python.sh \
  "$PWD" "$PWD/trellis/skills/guru-team/runtime" \
  -m unittest discover \
  -s trellis/skills/guru-team/packages/guru-upgrade-installation/tests \
  -p test_contract.py -k test_formal_source_rejects_untracked_only_migration_package

bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh \
  --root . --mode source --json
```

三个版本用例属于 MigrationContractTests；它们不是整套历史安装迁移验收。TaskCommit/Review/Completion/Creation 原覆盖先按实际输入、代码、工具和环境判断适用性，补私有迁移的真实调用与来源→后继消费缺口；不惯例重跑所有历史用例。

### 3.2 一个来源样本与完整平台补充

原验证 owner 在执行时解析 canonical lock 对应的完整干净 Fork build，将实际路径仅放当次环境变量 TRELLIS_FORK_SOURCE，不写持久 workspace 映射。以下命令从 Task checkout 执行，显式保留临时项目供同一次完整比对：

```bash
export GURU_D1_SOURCE_ROOT="$PWD"
export GURU_D1_PROBE_WORK="$(mktemp -d "${TMPDIR:-/tmp}/guru-d1-source.XXXXXX")"
TRELLIS_FORK_SOURCE="${TRELLIS_FORK_SOURCE:?先按canonical lock解析匹配Fork build}" \
  TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#main \
  TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 \
  bash trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh \
  "$GURU_D1_PROBE_WORK" --mode focused --platform codex

export GURU_D1_PROBE_TARGET="$GURU_D1_PROBE_WORK/matrix/codex/project"
bash trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo "$GURU_D1_PROBE_TARGET" \
  --platform claude --platform codex --platform cursor --json

bash "$GURU_D1_PROBE_TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" \
  --root "$GURU_D1_PROBE_TARGET" --mode installed --json
```

本未发布分支须经原 verifier 的公开 Guru custom init，再原 copy 当前本地 canonical workflow/preset，完整运行 focused 的两次 update/reapply、CLI/lock/hash/native-load/session 检查，并保留 local_workflow_sample。核 init-owned bootstrap 仍为 schema2、空 deliveries 且未被修改或转换；custom workflow 不登记官方 template hash，原其余 hash/未知漂移检查仍执行。原 native 初始化和临时 hash 修复的失败观察保持，不作为新路径通过。长期回归执行真实 _install_workflow 并观察实际参数和样本字节；已有 caller 回归按受影响差额采用，不冻结可变模板 hash 或增加无 consumer 的参数。

Codex focused 结果仅覆盖它实际执行的路径。完整 focused 通过后，在同一项目增加全部三平台，核实际完整 Shared/Claude/Cursor 公共投影及选定受管集合；Codex 的 public root 是 Shared .agents，不恢复旧 public .codex 根。公开 marketplace 只供 bootstrap 样本，本地 candidate workflow 与 preset 始终来自当前来源。该样本不证明 immutable 远端 .9、正式 source_locked 或真实 eafc .9 安装。

实施者在全平台 apply 后，使用原 installer 的完整源映射作一次只读比对，不新增 tracked helper/report。以下代码只验证确定性事实；充分性仍由原 AI owner 判断：

```bash
bash trellis/skills/guru-team/runtime/resolve-python.sh \
  "$GURU_D1_SOURCE_ROOT" "$GURU_D1_SOURCE_ROOT/trellis/skills/guru-team/runtime" - <<'PY'
import json
import os
import sys
from pathlib import Path

source = Path(os.environ["GURU_D1_SOURCE_ROOT"]).resolve()
target = Path(os.environ["GURU_D1_PROBE_TARGET"]).resolve()
sys.path.insert(0, str(source / "trellis/presets/guru-team/scripts/python"))
import apply_guru_team_trellis_preset as preset

mapping = preset.managed_source_projections(
    target, target / ".trellis/guru-team", {"claude", "codex", "cursor"}
)
for relative, canonical in mapping.items():
    actual = target / relative
    assert actual.is_file(), relative
    assert actual.read_bytes() == preset.canonical_bytes(canonical), relative

manifest = json.loads((source / "trellis/guru-team-extension.json").read_text())
installed = json.loads((target / ".trellis/guru-team/extension.json").read_text())
assert installed["extension"] == manifest
assert installed["source"] == preset.source_provenance(source)
assert (target / ".trellis/.version").read_text().strip() == manifest["target_trellis_cli"]
assert (target / ".trellis/workflow.md").read_bytes() == (
    source / "trellis/workflows/guru-team/workflow.md"
).read_bytes()
assert (target / ".trellis/guru-team/trellis-source.json").read_bytes() == (
    source / "trellis/presets/guru-team/source/trellis-source.json"
).read_bytes()
for section in ("install", "skill_packages", "overlays"):
    assert set(installed[section]["selected_platforms"]) == {"claude", "codex", "cursor"}
assert not installed["install"]["new_copies"]
assert not installed["install"]["managed_backups"]
for section in ("skill_packages", "overlays"):
    for field in ("conflicts", "sidecars"):
        assert not installed[section][field], (section, field)
for relative in preset.MANAGED_ASSET_PATHS:
    if relative.parts[:2] == ("scripts", "bash"):
        assert os.access(target / ".trellis/guru-team" / relative, os.X_OK), relative
print("Complete managed source bytes, version, workflow, lock and observed provenance match.")
PY
```

同时读回原 installed validator 的完整 inventory、package/platform bytes、执行位及 manifest/overlay 结果，并核实际未处理 .new/.bak 为零。installer 对 companion executable 有归一规则，不要求所有目标 mode 与源码逐位相同。public projection 的文件集合、内容和执行位由原 installed validator 检查。来源 provenance 如实保留当时 dirty source observation；不能称该 HEAD 已含全部未提交 .9 内容。不得修补临时产物或改写 manifest 来使比对通过。

这是一个代表性临时项目的来源自身验证，加同项目完整平台投影检查。它不是完整多平台矩阵、真实前驱 upgrade 或 Stage 2 candidate gate。若原入口正常前置不满足，保留实际失败并回原 owner；不能换 flag、借旧 provider 或把该失败转给 D2。

### 3.3 结果与验收对应

| ID（design / AC） | 输入、实际观察与断言 | 证明边界 |
| --- | --- | --- |
| V-01（01/03） | fresh-read #808/#794、实际 PR/归档 lineage、tags/Releases、版本五面、三个 README 的 changed links/command blocks；git diff --check | 六项输入、当前/前驱各自 lock、.9目标与.8稳定事实明确。不把未发布版本当 latest/stable |
| V-02（02/05） | §3.1 私有真实 public TaskCommit→Candidate→Review双槽→下游 consumer；未审与当前已审场景 | 实际 producer 成功且其当前结果可消费；未审不调用远端 executor。fixture 不证明实际 Agent/远端成功 |
| V-03（02/05） | 私有迁移实际命中的真实后继、普通 stale、同提交输出丢失、双槽缺步及旧 Draft/provider 恢复 | 同 key/B/PR 与原操作、无重复效果；缺语义覆盖回原 owner。不新增对抗、压力、fault injection 或无关历史转换 |
| V-04（02/05） | §3.1 canonical source validator、三个版本用例、私有四份 byte/inventory 及排除分发回归 | formal source 和 installed_version 真实输出通过三 consumer；来源分发完整。静态一致不替代行为验证 |
| V-05（01/03/05） | §3.2 一个 focused local sample、同项目全平台 apply、目标 own installed validator、全量 managed_source_projections 和实际 mode/provenance/sidecar 读回 | 来源自身完整可用；单平台结果不独立证明全部平台，不证明真实 eafc 采用或正式 source_locked |
| V-06（05/06） | 完整工程/整合结果、原 TaskCommit、固定完整 committed Review、publication Architecture eligibility、Delivery Review/readiness、Publication/Merge | 全部 D1 after 已审且当前中文 Refs-only payload真实。各原 owner 判断充分性，实际交付不从 fixture 推导 |

真实 checkout 的 installed/native/preservation、完整 source_locked、ownership、parity/drift 属 D2 AC-04。D1 若运行诊断，旧安装/公开 schema差额和失败须原样报告，不计通过。来源自身验证失败仍阻塞 D1，不能以 D2 待办替代。

V-02/03 为长期行为回归；V-05 的一次全量比对是临时诊断，不成为新长期 helper。按依赖执行并采用仍适用结果；必要覆盖完成、证据足够支持当前阶段后，停止追加实验。Stage 2 的完整前驱 diff、focused/existing、真实.8 upgrade、secret scanner、普通 self-reapply及限定 historical-Task observation、同源 candidate 和 smoke 门禁仍由原发布 owner另行执行，本批不预记通过。

## 4. 停止条件与适用回退点

| 条件 | 停点与原 owner |
| --- | --- |
| scope、#808来源、版本占用或 accepted authority 实质变化 | 原 Clarify/Planning 刷新受影响范围；不私改 anchors、根 PRD 或预建 D2 |
| 真实方案改变公共 owner/API/consumer/phase/责任 | 回原独立 candidate assessment；不能以本次 target_native 结论代替新机制评估 或在私有文案自授新路线 |
| D1 自身操作须先实际采用.9，或来源自身必需验证失败 | 停受该失败影响的 D1 接受、实施或交付步骤，回原分配/Planning或工程 owner。不豁免 TaskCommit、不插 tools、不安排失败审核，也不移交自身缺陷给 D2 |
| managed runtime、匹配 Fork build、原来源样本或生产安装入口前置缺失 | 写前停在原 runtime/验证/安装 owner；保真实证据缺口，不用 dirty 来源冒充正式 source_locked |
| 临时目标冲突、未处理 sidecar、模式/完整字节不符 | 在原安装/验证 owner 诊断，保留原观察；不手修产物取得绿色，不扩完整矩阵 |
| 工程失败、fixture绕过被测producer、Review finding或current gate stale | 回最早受影响实施/Planning owner；保 B、历史事实及仍适用覆盖，实际修复和受影响审核均补足 |
| 后继 D2 的 source/事务/目标状态异常 | D2 原 tools 按自身 source pair、冻结计划和恢复合同处置；D1不提前 prepare、换源或覆盖旧操作 |
| 已发生 commit/PR/Merge 但输出丢失 | 原 owner核同 operation、parent/HEAD/PR并恢复，不重复提交、push、建PR或merge，不提前关#808 |

局部修正只处理本批授权路径，保留用户并行改动。没有业务数据库或生产部署变化，不造数据/生产回滚协议。Git/GitHub、安装、bookkeeping、Cleanup和Stage 2各项副作用保原独立边界，授权仅存在于当前对话。

设施反复失败时重评测试入口、修复设施或明确保留证据缺口。未解决缺口不能记 pass；证据已足够支持当前阶段时停止追加实验，不制造无关验收。

## 5. Delivery Policy（唯一）

选择 **staged**。顺序来自已接受整体分配与本 D1 scope_ref，不由 Policy 标签改范围。当前阶段为 **D1完整来源交付**，本批完整覆盖 AC-01/02/03/05/06 的来源、私有消费者、文档及逐 Delivery质量/交付责任。

| 阶段 | 进入与本阶段责任 | 退出及直接后继 |
| --- | --- | --- |
| 当前 D1 完整来源 | 当前 scope及新候选assessment，经完整Planning、Wording/final_plan/Approval和Activation后才实施；完成来源自身、直接消费者、真实回归、必要知识及全部必需验证 | 原 TaskCommit→固定完整独立Review→readiness→Publication/Merge真实 delivered。未完成自身验证不得退出；未审本地提交不供D2采用 |
| 后继 D2 实际采用 | 仅真实D1 delivered后，原Completion additional_delivery_required→原Creation建立新slice，再独立Planning/Activation。读取真实前序和完整干净匹配来源 | 原tools source_locked实际采用；全部managed/package/platform/workflow、installed/native、preservation、ownership、mode、sidecar、parity/drift及自身完整提交/审核/交付成立 |
| 全Task准备完成及终态 | 原Completion读取所有真实Delivery/证据，判AC-07无剩余准备业务 | Closure no_mutation；acceptance-finish Architecture、Finish唯一归档及必要bookkeeping、Cleanup履行AC-08。caller-owned资源保留，不关闭#808 |

当前旧安装与来源差额的临时边界只限定真实 checkout 的.9采用。原因是正式source_locked须先有完整干净且实际delivered的D1来源；解除条件为D2完成原tools实际更新及完整匹配验证。后继owner必须核实际前序与解除条件，并按真实after更新当前说明/断言。历史安装、drift失败和原单Delivery blocked观察不改写。

本边界不限制D1的来源自身可用性，不免除同步义务，也不冻结整个Task。若D1实际修改扩大到必须同时采用的workflow/overlay或执行机制，回原owners重新判断。未实施的D2责任不是evidence_pending；D1合并不触发Finish。所有准备业务和终态完成后，Stage 2仍须fresh唯一candidate、完整验收、tag/smoke/Release、两个选定本地目标及独立最终关闭，各项不由本Policy预授权。

## 6. Docs SSOT Plan（唯一）

选择 **delta_first**。本次规划只写当前D1正文及官方context，不写共享authority。未来实施按真实before/after由原owners整合必要完整单元并readback；全部业务after在TaskCommit前完成，提交后一次独立完整Review审查。

| canonical目标 | 实际差额、原writer与直接consumer | 整合和验证边界 |
| --- | --- | --- |
| README.md、trellis/workflows/guru-team/README.md、trellis/presets/guru-team/README.md；public-docs规则 | 原实施/docs owner说明.9未发布来源准备与.8稳定状态；保公开anchor，当前Fork只指canonical lock/build recipe。consumer为安装/升级用户和原release reviewer | 更新受影响完整章节及必要关系，核命令/链接/版本语义。规则本身未变不改spec；不设第二当前版本表 |
| Shared release references/contract.md及Codex/Claude/Cursor私有副本，实际入口变化才改SKILL.md | 原私有owner迁移逐Delivery当前完整链与D1→原Completion/Creation→D2采用，保持完整Stage 2。consumer为原调用AI和实际回归 | 四份发现正文一致且排除公共分发；原TaskCommit成功consumer不变，不能只删过期引用而遗漏真实采用 |
| docs/requirements/current/task-delivery-lifecycle.md、docs/design/current/task-delivery-lifecycle.md、docs/test/current/task-delivery-lifecycle.md的R794/D794/T794及既有scope/stage事实 | 原RDT owner按实际差额判断。现有定义已承载本机制，本次不追加通用定义、全局版本或通过登记；只有发现真实正文缺口时，才由原writer完整整合，consumer为实施/审核/后继规划 | no_change不造空贡献；必要真实delta由原final_integration写入/readback，提交后独立审actual after，不预填测试结果 |
| docs/architecture/03-domains/ownership.md、04-integrations/distribution.md，以及隔离贡献 docs/architecture/contributions/808-release-v070-guru9.md 的两个完整 proposed targets | 独立candidate assessment选择target_native。原Author准备完整提案，原Architecture在实施/工程后按expected-current整合/readback，consumer为私有release调用方、committed reviewer和后继Planning | 只维护ARCH-DOM-010/ARCH-INT-015的现行完整关系及#392历史边界，无新ADR或root/index写入；整合pending与独立reviewed_promoted区分 |
| canonical extension manifest、TARGET_GURU、三份upgraded schema与active output example；local sample selector归原compatibility verifier；installed manifest/projections归原installer/tools | 实施owner对齐.9版本直接消费者，原source/安装/输出consumer读取真实当前目标。D1临时目标由原生产apply验证，D2原tools独占真实checkout受管采用 | 不手工同步受管副本或伪造manifest，不改source lock；来源、样本、正式source_locked和实际installed/native分别报告 |
| 后继D2实际采用涉及的当前说明与断言 | D2实施及原RDT/Architecture owners读取真实D1结果、解除条件和安装after；直接consumer为目标调用方、独立reviewer与整体Completion | 按真实差额维护必要当前单元，不重写历史观察，不在D1提前写D2计划或结果 |

不新增task-local release notes、PR/Release body handoff、动态checkbox、状态提交、授权记录、审查账本或共享逐主题索引。本计划不把未来安装、交付、终态或发布结果写成已完成事实。
