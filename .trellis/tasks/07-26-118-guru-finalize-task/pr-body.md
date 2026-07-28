## 变更摘要

- 新增公共 semantic closed-loop Skill `guru-finalize-task`，统一拥有 immutable closeout plan、精确人类 digest 确认、content push、verification routing、唯一 Draft PR identity、final projection、单次 archive metadata transaction、三方 HEAD equality、draft-to-ready 与封闭 recovery state machine。
- 建立 Interface 1.3 的七个 distinct public input profiles 与六个使用 `exit_id` 的最小 outputs；`reprepare_required` 通过 target-owned `skill_input_authoring_seed` 分离 producer seed 与 fresh AI intent/context authoring fields。
- closeout plan、readiness、verification、PR/archive/recovery facts 和内部 transaction states 全部保持 owner-private；跨 Skill 只投影 named consumer 直接消费的最小 identity。
- 复用既有 #105 closeout transaction engine，增加 exact one-time、same-month、plan-bound legacy partial-plan takeover，同时保持既有事务顺序、generic recovery 与 cross-month reprepare 语义不变。
- Production eval 执行真实 public wrapper，先由 owner result 选择 actual exit 的独立 schema，再在返回后断言 `expected_exit`；Shared、Codex、Claude、Cursor corpus byte-identical。
- 同步 canonical package、dogfood runtime、registry、extension manifest、preset additive distribution、schemas、examples、tests 与 durable Docs SSOT；不修改 global workflow route、preset overlays 或 upstream `trellis-finish-work` family。

## 影响范围

本变更影响 Guru Team finalization Skill package、deterministic runtime、private gate/plan schemas、consumer projections、production eval adapter、extension registry、preset additive distribution、四个平台副本和相关 Docs SSOT。AI 继续独占 plan、scope、readiness、recovery route 与 confirmation 判断；脚本只执行、校验和记录客观事实。

现有 task publication 与 extension verification Skill 仅通过各自最小 DTO 接入 finalizer。Content push 后，finalizer 先调用 #117 owner checker；只有 current plan/ref/HEAD 绑定通过且 actual exit 为 `verified|not_required` 时，才向默认关闭的 publication augmentation 精确放行当前 task 的 `marketplace-verification.json`。Prepared state 在无 plan 时只允许 exact finalizer-owned gate metadata 合法重入，arbitrary metadata 继续 fail closed。

Codex production eval 只向 argv 精确授权 repo-external native execution root；workspace-enforcing regression 证明真实 `guru-finalize-task/scripts/invoke.sh` 执行并写入 trace。全局 Finish family workflow/platform routing 仍由 #119 负责，upstream overlay 清理由 #132 负责；本 PR 不修改 upstream Trellis Skill、Command、Prompt、官方 archive 脚本、全局 npm 包或 `node_modules`。

## 验证结果

- Phase 2：P0/P1/P2/P3=`0/0/0/0`；runtime 627 passed、13 skipped；#105 transaction 105；Skill/package/eval 180；finalizer 5；focused Namespace 5；preset 45、ownership 9；72 条 command/144 个 exact stream evidence 全部重算匹配；source/installed shared wrapper eval 与 clean throwaway current-candidate install/update/reapply/`.new`/`.bak`/platform/OOTB chain rc=0。
- Public-wrapper Namespace closure：content-pushed re-entry 不再因缺少 checker-private fields 抛出 `AttributeError`；private args 仅从 validated task-local immutable plan 重建，initial no-plan 与 stale gate 继续 fail closed，public CLI/DTO/schema/exit 未扩大。
- Finalization gate re-entry closure：prepared gate recorder-to-checker 正向 1 项与 arbitrary metadata 负向 1 项通过；只放行 exact finalizer-owned gate path。
- Codex trace write closure：repo-external workspace-enforcing regression 通过，trace 最后事件为真实 public `invoke.sh`，wrapper rc=0；canonical/dogfood adapter SHA-256=`e519f1babbf5b90999f9cc3f64b431d7fc544a2e9fe2f640be482d4372a8fc35`。
- Verification re-entry：workflow `verified` 与 task-bearing standalone `not_required` 两条真实 recorder-to-finalizer public wrapper 路径通过；arbitrary metadata 与 missing explicit owner binding 继续 fail closed。
- Stale-checkpoint cleanup：task commit 009=`d7308d4aeaa3228d7650b93821ac7b4269ec5b38` 只删除 predecessor plan 绑定的 `closeout-plan.json` 与 `task-finalization-gate.json` active copies；旧 bytes 保留在 parent history，随后 Phase 2、Branch Review、publication review 与 finalization preview 均重新建立 current identity。
- Final Branch Review Round 17 覆盖完整 `origin/main...d7308d4aeaa3228d7650b93821ac7b4269ec5b38` 的 554-path/9-commit range，并 fresh 运行 runtime 627/13、package/eval 185、preset/ownership 54、parity/overlay/protected-surface checks；P0/P1/P2/P3 与 scope proposals 均为 0。
- Clean throwaway 覆盖 workflow marketplace discovery、preset initial install/reapply、official update、managed hashes、`.new/.bak` recovery、四平台分发、真实 wrappers/evals、installed recovery、ownership 与 overlay drift。
- Claude installed native 调用因外部 `401 Invalid API key` 未取得 semantic success；协议、adapter parsing、controlled tests 与 corpus parity 通过，但不把外部 401 描述为 live pass。Cursor 当前环境稳定返回 declared `unsupported`，同样不冒充 semantic pass。
- 当前通过的是 exact local committed source；feature ref 尚未 push。真实 pushed feature-ref marketplace verification 仍是 `guru-finalize-task` content push 后、Draft PR/archive 前的 mandatory #117 owner gate，不能用 local/main 验证替代。
- 完整 `git diff --check origin/main...d7308d4a` 仅命中 assignment-bound immutable Round 9 raw report line 203；Round 13/17 将其保留为 `rejected_candidate/out_of_scope` nonblocking observation。Current last-commit 与 metadata tail whitespace check 通过。

## Review Gate

Round 17 使用未参与 implementation、Phase 2、finding discovery/closure 或旧 Round 16 final-release 的全新 reviewer，对 current 554-path/9-commit range 执行 qualification-first fresh final review。它重新验证 stale-checkpoint cleanup、全部历史 finding closure、Interface 1.3/private-state/recovery/distribution contracts、Docs SSOT、安装升级和安全部署边界；Round 17 raw report SHA-256=`56784821f7bc46f9ae679d9ec2344450a50258244e0127319ac0b4eb2abce1cc`。

Current P0/P1/P2/P3=`0/0/0/0`，scope proposals=`0`。正式 Branch Review recorder、checker 与 public wrapper 均返回 `passed`；gate artifact SHA-256 为 `70452a5858e0787d6502e7a82db998e83c897d3517c8c50e093c0b8d18971d77`。

## Issue 关闭范围

Closes #118

Related #81, #115

Follow-up #119, #132

#118 的 Skill、runtime、schemas、examples、tests、eval、distribution 与 durable contracts 已由完整 diff、Phase 2 和 Branch Review 覆盖。#115 是 umbrella，由 #119 的 combined acceptance 负责关闭；#119 继续拥有 Finish family integration，#132 继续拥有 upstream overlay 清理。本 PR 不关闭或改写这些独立范围，也不改变或重新关闭已完成 #105 的事务语义。

## 安全说明

Public DTO 不携带 closeout plan、readiness、verification、PR/archive/recovery facts 或内部 transaction state。Task-local 与 runtime evidence 只记录去敏 repository identity、digest、HEAD、path/blob/mode 与状态事实；未发现 token、credential、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感原始记录进入候选变更。

本变更不新增恶意 actor、伪造 artifact、攻击模型、并发 finalizer、锁、TOCTOU、额外 fault injection、偶发 crash consistency 或跨 OS 原子性范围。

没有 dependency、CI/CD、container、Compose、Kubernetes、Helm/Kustomize、DB migration、Makefile、Terraform、服务部署或 production data write 变化；无需数据库迁移、配置变更、服务重启或生产回滚。存在预期的 Guru Team additive extension install/update surface，已由 clean throwaway install/reapply/update 与平台分发门禁覆盖。

## Docs SSOT

- Strategy：`ssot_first`。
- Durable docs：finalizer step-local contract、Skill I/O、workflow ownership、companion scripts、quality、preset installer/upstream ownership、public docs 与 repository/workflow/preset README 已同步。
- Merged delta：semantic owner、single transaction engine、七个 distinct profiles、六个 `exit_id` outputs、owner-private state、verification/PR/archive/recovery ordering、production eval、distribution 和 update/reapply 规则均已写入对应 durable owners。
- Current corrections：prepared finalizer gate re-entry、owner-check-first verification re-entry、Codex repo-external execution-root grant 与 public-wrapper private Namespace reconstruction 均恢复 code/test 与既有 durable contract 一致；stale predecessor plan/gate active copies 已在 task commit 009 删除，无新的 durable semantic delta。
- Task history：planning provenance、实现轮次、Phase 2 command evidence、historical finding lifecycle 与 raw Branch Review reports 仅保留在 task-local artifacts，不承担长期流程定义。
- Follow-up / limitation：global Finish family activation 与 combined acceptance 由 #119 负责，upstream overlay cleanup 由 #132 负责；exact pushed feature-ref verification 与真实 GitHub/archive side effects 仍是后续 finalization mandatory gates。
