# D1：v0.7.0-guru.10 完整可分发源实施与验证计划

## 1. 输入与引用

TaskId 为 `744a637b-a044-46cd-8cdd-77ddd85ded8e` / generation 0；DeliveryId 为 `60d7e5c9-e62e-4a92-bc33-ef7228202be0`。选择整体 R1、R2、R5、AC1。整体范围见 [Task PRD](../../prd.md)，本批行为/AC 见 [PRD](prd.md)，唯一来源设计处置见 [design §3](design.md#3-来源设计处置唯一)。无前序 Delivery；B 和 main PR 目标见 design §1。

实施前实际加载必要完整条件：design §1～9；私有 release contract 的 Stage 1/2、完整源与真实采用、独立副作用和禁止持久化；current workflow Phase 1～3；原 Author shared planning-body 和本批模板；quality-guidelines 的 Test And Validation Value/Validation Scope Ownership；public-docs 的 README 分工。design §9 的 RDT/Architecture 单元、constitution 和 change-contract 提供知识判断依据。涉及扩展实现前加载 trellis-meta，并对照 Trellis 官方 index/custom-workflow/custom-spec-template-marketplace；不改上游或全局包。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置和 owner | 实际文件、动作、完成观察与后继 |
| --- | --- | --- |
| S1 完成规划 | actual candidate_assessment；原 Author | 完成当前三正文、官方 implement/check JSONL；原 plan_ready → 独立 final_plan → Approval。展示完整计划后停在接受/Activation 边界 |
| S2 完整版本 | actual Activation；实施 owner | 改 design §4.1 六文件当前目标为 .10；shape、来源家族、CLI/lock 保持；V1 实际 producer→consumer 成立 |
| S3 私有及公开说明 | S2；原私有/docs writer | 四份私有合同对齐 current owners、取消默认 Wording；必要 tests 调整。三个 README 更新当前版本、前驱和真实安装条件；保留历史，V2/V5 核对 |
| S4 来源自身验证 | S2/S3 完整 after；实施 owner | V3 source；V4 一个 focused Codex 样本及同项目三平台、完整映射/installed/drift 观察。不得普通 apply 真实 Task checkout |
| S5 知识收敛 | 真实实现和工程结果；原 RDT/Architecture owners | 按 §6 判断必要差额；若确需，原 owner 完整整合/readback，TaskCommit 前完成并补受影响检查。不改共享导航，不造空贡献 |
| S6 提交与完整独立 Review | 完整本批 after/工程/知识；原 TaskCommit、implementation、Review | 展示精确本地提交文件和命令后停报。后续 TaskCommit → constructor/begin_check 固定 B..H；新独立 reviewer 同次完成 Architecture/Check/full Review，真实两槽；修复仍走原 writer、提交和受影响复审 |
| S7 D1 交付 | 完整 Review 和 publication Architecture eligibility；原 Delivery Review/Publish/Merge | 中文 Refs #861 payload，每项 push/PR/merge 先展示精确动作。实际 delivered 后才交 Completion；不关闭 Issue，不创建 D2 |

S7 后原 Completion 对未实施真实采用返回 additional_delivery_required，原 Creation 才建 D2。D2 独立规划/接受、tools source_locked 和 installed after 完整质量交付；全部准备满足才 Completion、no_mutation Closure、Finish。Stage 2 最新 main 与正式发布不由本批执行。

## 3. 验证入口、输入与预期观察

以下为未来执行计划，不预填结果。V1/V2 是长期回归，V4 完整比对是临时观察，不新增 tracked helper/report。先实现直接差额，再跑便宜定向回归，最后一个来源样本；复用仍适用覆盖，没有惯例红绿/回退重复要求。

### V1：upgraded 生产者和消费者

从 Task checkout 用 canonical resolver 执行三个现有用例：

```bash
for test_name in \
  test_delivery_upgraded_result_matches_source_and_public_consumer \
  test_formal_source_requires_committed_clean_canonical_candidate \
  test_formal_source_rejects_untracked_only_migration_package
do
  bash trellis/skills/guru-team/runtime/resolve-python.sh \
    "$PWD" "$PWD/trellis/skills/guru-team/runtime" \
    -m unittest discover \
    -s trellis/skills/guru-team/packages/guru-upgrade-installation/tests \
    -p test_contract.py -k "$test_name" || exit "$?"
done
```

预期实际 producer 输出与 manifest 目标一致，三消费者和 active example 合法；普通 dirty/untracked 正式源仍拒绝。现有用例已经沿 manifest 读取目标，不加固定 .10 自证断言。fixture 必须触及被测入口，不种 producer 应产生的结果。这是模块合同，不是完整业务升级。

### V2：私有 current chain 与副本

```bash
TRELLIS_DELIVERY_API_COMMON="$PWD/.trellis/scripts/common" \
  bash .trellis/guru-team/runtime/resolve-python.sh \
  "$PWD" "$PWD/.trellis/guru-team/runtime" \
  -m unittest discover \
  -s .agents/skills/release-guru-trellis-version/tests -p test_contract.py
```

预期当前公开包装链仍按原边界执行，私有合同不恢复默认 Wording；D1 delivered 后才接原 Completion/Creation。四份私有定义一致且不进入公共分发。只修实际失配回归；fixture semantic 判断和远端替身不证明真实独立 AI、GitHub 或本次 D1 已 delivered。

### V3：source 和声明根

```bash
bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh \
  --root . --mode source --json
```

V4 三平台样本形成后：

```bash
for skill_root in .agents/skills .claude/skills .cursor/skills
do
  bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh \
    --root "$GURU_D1_SOURCE_ROOT" --mode source \
    --platform-root "$GURU_D1_PROBE_TARGET/$skill_root" --json || exit "$?"
done
```

这里仅证明 declared root/support/public structure；完整 bytes/mode 由 V4 核。Codex 共享 .agents，无受管旧 .codex/skills/guru-*。

### V4：单项目来源样本和完整投影

执行前核 canonical lock 和复用 Fork `/Users/wumengye/Documents/GoProjects/Trellis` 的 clean HEAD、build marker、CLI/Core 相符。只有确需构建才按原 recipe 使用当前 pnpm；不改 source lock/package-manager 声明。

```bash
export GURU_D1_SOURCE_ROOT="$PWD"
export GURU_D1_PROBE_WORK="$(mktemp -d "${TMPDIR:-/tmp}/guru861-d1-source.XXXXXX")"
TRELLIS_FORK_SOURCE=/Users/wumengye/Documents/GoProjects/Trellis \
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

原 verifier 完成 focused 安装/update/reapply、CLI/lock/hash/native-load/session 检查，保留 local_workflow_sample。bootstrap main 不代表 .10 正式来源；原本地 canonical copy 才是本次被测 after。核 helper 真实输出的项目路径；若实现已改变，消费其实际输出，不能另建第二项目规避失败。

全平台 apply 后，以本 source 的 `apply_guru_team_trellis_preset.managed_source_projections(target, target/'.trellis/guru-team', {'claude','codex','cursor'})` 获得完整映射。通过原 canonical resolver 执行一次临时只读 Python：逐项核目标存在、bytes 等于原 canonical_bytes；按原 installed 规则核公共执行位和 companion executable 归一。再读回：

- installed extension 等于 canonical manifest，source 等于原 source_provenance(source)，不改 dirty/local source 观察。
- workflow bytes 等于 source canonical workflow；lock bytes 等于 canonical lock；CLI 记录等于 manifest target_trellis_cli。
- install/skill_packages/overlays 的 selected_platforms 为三平台；完整 expected managed 集合与实际 inventory 相符。
- 公共三 root 的完整集合/bytes/mode，无 private runtime/tests；私有 release Skill 不分发。
- manifest new_copies/managed_backups/conflicts/sidecars 无未处理项，实际目录无 .new/.bak。

完整源映射和 target own installed validator 联合证明本样本的实际 drift/parity；不只比较部分文件或信 exit0。`check-dogfood-overlay-drift.sh` 要求目标本身含 canonical source tree，不把它错误指向普通样本，也不为运行它往样本手补源码。真实 Task checkout 的该脚本在 D1 可能观察旧 installed 差额，结果按真实含义保留；D2 原 tools 采用后才验证真实 target drift。若本批改 overlays，仍按原 owner 分配相应同步及 checker 责任，不绕过要求。

V4 预期本来源 .10 能完整安装及 reapply。它不是 immutable 远端 .10、正式 source_locked、真实 Task 安装、前驱升级、完整矩阵或客户端真实业务使用的证明。任一必需源验证失败留在 D1。

### V5/V6：说明与完整交付

人工读三 README 改变后的完整相关章节，同 ref 命令/链接/anchors、版本历史身份、前驱 peeled commit、Release 条件及私有四份 bytes。运行 git diff --check，并检查改动 shell blocks 语法和必要链接。文字不新增固定值自证测试。

D1-AC4 由真实 TaskCommit、完整独立 Review 和交付结果证明；工程命令不替代语义审核。准备 Review 不替代 Stage 2 exact-candidate gate。

## 4. 停止条件与适用回退点

Task/key/phase/scope/root 不符时停在原 Identity/Ensure/Bind/Selection 或 scope owner；每次 Task 文件写前运行 boundary checker。版本消费者、必要来源检查或样本失败保留输出并回本批实施，不能手修样本/manifest 或留给 D2。

真实需求/来源变化回 Clarify；机制变化回 candidate_assessment；正文和执行缺口回原 Author 并刷新受影响 final_plan/Approval。没有数据迁移或正式发布动作，不新增 rollback 协议。本地编辑仅处理本批文件，保留并行改动；已完成外部操作由原 producer 恢复同一结果。

必需回归和完整来源观察充分后停止追加实验。设施反复失败时重评实际入口/环境，或保留具体证据缺口，不预填验收通过。真实采用与正式发布由后继合法边界承接。

## 5. Delivery Policy（唯一）

策略为 **staged**。当前 D1 覆盖完整可分发源、版本直接消费者、私有 current 消费者、公开说明和全部必要来源验证。进入条件是规划经原 gates/Activation；退出条件是完整实现、工程/知识差额、精确提交、一次独立完整 Review、readiness 和实际 delivered。

局部限制对象是准备 Task checkout 的 .10 installed/discovery 采用；原因是正式 tools 需要先有已交付完整干净源。解除条件为 D1 delivered；直接后继为原 Completion additional_delivery_required → Creation D2 → 独立 Planning/Activation → tools source_locked。D2 读取真实 D1 结果，维护实际安装 after、适用当前说明/断言，走完整质量交付；历史 D1 观察保持。D2 未提前创建。

整体准备完成还要求真实采用、全部 Delivery 责任、whole Task Completion、reference-only Closure no_mutation、Finish 簿记入 main。Stage 2 再取最新 main，独立 gate 后分别 tag、smoke、Release、唯一主目录安装、Issue close。本批合并不表示这些已完成。

## 6. Docs SSOT Plan（唯一）

strategy 为 **no_docs_update_needed**，限共享 RDT/Architecture authority。本批没有新增公共能力、语义、字段或架构职责。现行 R153-04/R850-01、D850-01/04、T850-01/04 已定义原内容 owner 和退役；R724/D724/T724 已定义共享发现根、维护及证据分层；ARCH-INT-006/014/015、ARCH-GOV-008/009 已定义来源、真实采用及完整交付。candidate 未要求贡献或 ADR，版本提升不追加知识根登记/release ledger。

三个公开 README 和私有发布合同仍是本批实际内容，由原 writer 更新，提交后完整独立 Review；不被此策略排除。共享 root/index/manifest 和历史 Test 不因版本提升机械改写。

S5 的原 `guru-maintain-requirements-design-test-ssot` 判断真实实现是否出现必要规范差额，其直接 consumer 是 TaskCommit/独立 Review 前的完整知识 after。确有新差额则先回 Author 刷新本唯一 Docs Plan，选合适策略；原维护 owner 在 TaskCommit 前完整整合/readback，随后独立 committed Review 审真实 after。Architecture 同理由原 owner 处理，不预建空贡献或自行晋升。D2 的实际采用指南/断言和 Stage 2 真实发布结果仍属后继责任。
