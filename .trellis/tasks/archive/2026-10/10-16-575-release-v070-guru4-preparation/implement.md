# #575 执行计划

本文件是稳定执行计划；勾选状态、运行结果、当前 HEAD、PR/tag/Release 进度不写入此文件。整体需求读 `prd.md`，机制及唯一 source-design matrix 读 `design.md`。

官方 context manifest 提供 spec 定位。执行者必须直接读取任务涉及的完整合同；超过 native injection 上限的文件，不能把截断正文当作完整规则。代码通过 design 中的真实 owner 路径读取，不作为 spec 注入。

## P1. 唯一 Delivery Policy

策略：`staged`。整体 scope 始终为 R575-01..07/A575-01..08。当前计划负责 S1；S2 在真实 native 转换和 Creation 后由同一 Author 对其实际 Delivery 重新规划，不用这里的未来步骤替代新流程的 Approval。

| 阶段 | 入口与交付范围 | 可观察出口 | 剩余责任 |
| --- | --- | --- | --- |
| S1 正式来源采用 | 当前完整旧 installed 图；本三份规划和门禁通过后，固定新 Fork 锁、当前公开来源/稳定版本说明、精确断言、S1 Docs 贡献。manifest 保持 `.3` | 真实可构建 source/CLI/Core/CI 与文档一致；完整审查和原 promotion 链通过；Refs-only PR 经原 Publish/Merge 交付，源码 clean committed 且远端可寻址 | M、S2、整体 Completion/Closure/Finish 均由同一 Task 保留 |
| M 原生维护边界 | S1 完成后，使用其实际 clean committed source，依次进入原 tools-only 和 selected-task maintenance | 各自实际结果与 recovery、目标 native 和下一实际 owner 通过；同 Task/source/义务与原文件保留 | 新 scope/Delivery identity 只能来自真实原 owner；未满足则停止，不推进 S2 |
| S2 完整准备交付 | M 返回的真实新 native scope/Creation，新的 Delivery Planning 与批准 | `.4` 与 matching maintenance assertion、完整投影、唯一 Test 和定向证明经新图完整交付 | 整体 Task 审查全部 R/A；Stage2 发布仍归 #575 |

S1 独立条件：其 source lock、可构建匹配 API、当前公开来源映射和最小贡献无需安装 M 或完成 S2 就能被独立检查、提交和消费。S1 不以 installed parity、`.4` clean install 或最终发布成功为自身已通过条件；不能以这些条件尚未完成删减整体 Task 的后续义务。首次 PR 明确列出 M/S2。

S1 Merge 后进入真实 Completion；有剩余工作不能进入 Closure/Finish。若其路由要求 next-independent-delivery planning，先由原 Author 说明 M 的既有维护前置，按 D5 取得真实 native/下一 owner，绝不预置 D1。M 若转换为 delivered/pending acceptance，遵守真实 Completion/evidence_pending，再消费实际 scope/Creation。

## P2. Docs SSOT Plan

策略：`delta_first`。长期 RDT 原 owner 为 `guru-maintain-requirements-design-test-ssot`；Architecture 原 owner 为 `guru-maintain-architecture-baseline`。Current authority 由四层 README 现场读取，不把 `.89/.90` usage projection 当作 current，也不批量重写历史。

| 切片 | RDT 唯一贡献根 | Architecture task-owned / durable 定位 | 直接 consumer |
| --- | --- | --- | --- |
| S1 | `docs/requirements-design-test-contributions/575-source-adoption/` | 当前 `architecture/source-adoption.md`；晋升到 `docs/architecture/contributions/575-source-adoption.md` | 原 RDT/Architecture task_impact_sync、原 promotion、Phase2、完整 BranchReview、S1 Publication |
| S2 | `docs/requirements-design-test-contributions/575-release-preparation/` | 在真实 S2 Planning 形成 `architecture/release-preparation.md`；durable `docs/architecture/contributions/575-release-preparation.md` | 新图原 owners，对该实际 Delivery 的新差额审查及晋升 |

每个 RDT 根使用现有 `manifest.yaml / requirements.md / design.md / test.md / traceability.md`。S1 只拥有来源采用、当前文本和其实际验证；S2 拥有最终版本、原生迁移/安装及投影差额。每切片唯一 `test.md` 拥有该切片真实结果与未验证边界，双向 trace 使用稳定 R575/BEH575、D575/CON575、T575 标识并链接具体归属；不在多处复制结果。

先在贡献根收敛 requirements→design→test 与 trace，在该切片最终 Phase2 前完成 delta reconciliation；不能第一次到 BranchReview 才补 Docs。首次 committed 全量独立 BranchReview 后，原 owners 基于真实 expected-current 串行 promotion。Promotion 新差额必须 fresh Phase2、原 TaskCommit 和完整独立 BranchReview。S2 不编辑已晋升 S1 的历史结果；维护各自定位和 predecessor/successor 引用。

## P3. S1 顺序

1. 原 Author 收敛整体 PRD/候选，消费 candidate Architecture，完成本设计/计划、task-owned Architecture 贡献和官方 context。原 Wording→final Architecture→Approval 后展示规划与首切片 activation 边界，取得当前对话确认，再由原 Activation 执行。
2. 在已批准 S1 范围中核对正式锁及构建；修改根、workflow、preset README 与 public-docs spec 的当前来源说明。稳定 `.3` provider 保持原 immutable tag；新的未发布源码来源与最终 `.4` 目标区分。不得先 bump `.4` manifest/TARGET_GURU。
3. 原 RDT owner 承接 P2 的 S1 contribution，落实 source/doc 双向 trace；完成 V1/V2 与变更文件检查。旧 installed graph 与 final target 差异在切片说明中列为 remaining，不作虚假 parity 结论。
4. 按 S1 完整范围执行原 Phase2、TaskCommit 精确预览与确认、全量独立 BranchReview。零开放 P0–P3 finding 后，按 P2 执行所需 Architecture/RDT promotion，再 fresh Phase2、TaskCommit、全量独立 Review；不能用 recorder pass 替代语义审查。
5. 原 publication Architecture→Delivery readiness；PR 为中文、Refs #575，列出 source proof、旧安装仍保留、M/S2 未执行及部署边界。原 Publish 只在其精确计划确认后 push/建 PR/Ready；原 Merge 只在独立 expected-head 确认后合并。
6. Merge 实际结果进入 Completion。保留完整 Stage1 与同 Task 身份；按 D5 单独展示 M 的真实 source、checkout、写集和命令，分别执行两个维护 owners。这里的规划不预先授权其写操作。

## P4. M 与 S2 承接

M 按 D5 的六步执行。Tools 只更新所选 checkout，原始 Task/规划/session/private controls 留给原维护 owners。公共 inspect/prepare 出错、未知 controls、source/build/版本不符或 sidecar 冲突，均保留原状态并回原 owner；不复制新 Skill 到旧 dispatcher，不借 full Plan2 改义兜底。

公共转换持久化原始快照并保留五规划，原 Publish/Merge 核验真实历史交付；历史 gate 不转为 current。只读 observe/finalize 必须运行目标自身 native 与下一实际 owner。记录层次限于唯一 Test：工具可用、数据转换、session/native、历史交付、业务 Completion 分别陈述。后续 Creation 返回什么 identity，就在其 public planning_root 写 S2 五规划，不重建 Task 或从路径猜 UUID。

S2 重新 Planning/Approval 后，同步 `.4` extension、原维护版本断言和精确 fixtures；由原 public tools 与 Guru installer 完成成套 tracked 投影。执行 V3..V7；需要 clean committed source 的正式调用安排在原任务提交/Review后。若结果需要改产品或 Test/贡献，再进入受影响的原 Check/Commit/完整 Review。对源码 revision 的每次维护预览绑定当前实际 source，不重用已变更 source 的旧 frozen plan。

S2 逐切片 RDT/Architecture 收敛、promotion 前后门禁与 S1 同构，由新图实际 owners 执行。最终 Whole Completion 覆盖全部 R/A 和真实 M/native；reference-only Closure 不关闭 #575，Finish 单独归档/bookkeeping。Stage2 发布不属于本任务执行步骤。

## P5. 验证计划与失败路由

命令从实际 checkout 运行；Python 验证使用该层 managed resolver，依赖与 fixture 条件不满足就是 blocked/SKIP，不能写 pass。

| 编号/层次 | 精确入口与观察 | 阶段和判断 |
| --- | --- | --- |
| V1 正式来源 | 既有 `verify_trellis_compatibility_matrix.py` 的 `validate_fork_source`，通过 canonical `resolve-python.sh` 运行；同时运行生产 maintenance `inspect_source`。核对 commit/tree/ordered parents、CI repo/head/success、CLI/Core、pnpm、构建 marker 和模板 bytes | S1 必需；固定值以 PRD 为准，失败回原 source/build owner，不写全局安装 |
| V2 当前公开映射 | `python -m unittest test_fork_preparation`，cwd 为 `trellis/presets/guru-team/scripts/python`；README/public-docs 人工核对四轴、当前/历史边界；JSON/diff check与精确变更文件 secret scan | S1；测试必须消费当前新 lock，历史 provider不被改成未来 tag；源/旧安装差异列 remaining |
| V3 公共维护 | canonical `guru-upgrade-tools/scripts/preview.sh`、`prepare.sh` 和确认后的 `invoke.sh`；`guru-maintain-legacy-task/scripts/preview.sh --action inspect/prepare` 及其实际 apply/observe/finalize | M/S2 正式 source_locked；必须目标 native与下一实际 consumer，不以JSON解析或local_candidate fixture替代 |
| V4 source/installed/platform | 各自实际 `check-skill-packages.sh --root . --mode source|installed --json`；source 平台根 `.agents/skills`、`.codex/skills`、`.claude/skills`、`.cursor/skills`；byte parity含私有release Skill四份 | 整体准备最终必需；S1只判断自己变更的source层，不宣称尚未切换的installed与target一致 |
| V5 upstream/dogfood/reapply | `verify_dogfood_upstream_projection.py --repo-root . --fork-source <exact-built-source> --json` 与既有定向测试；ownership check；canonical apply三平台；dogfood overlay drift；递归sidecar/权限/receipt与`.version`检查 | 成套切换后和最终准备；reapply不得产生未审查mutation，不patch全局包或静默覆盖用户修改 |
| V6 代表性安装/旧样本 | 既有 focused Codex clean verifier及`.3` predecessor定向维护样本；既有 tools/selected-task runtime tests；source_locked真实生产调用补足local_candidate测试边界 | S2；工具/Task/native/原consumer/恢复/不兼容回退分别观察。远端最终候选和tag-pinned证明归Stage2重跑 |
| V7 最终内容与卫生 | `git diff --check`、实际 secret scanner覆盖本次完整变更集、声明可执行权限、bytecode/.new/.bak residue；完整Review覆盖origin/main...HEAD | 每切片按自身完整内容；任何product/contribution变更刷新受影响门禁 |

不执行完整多平台/native-host矩阵，不迁移真实业务，不把CPU/环境失败或未执行结果包装成成功。不新增与实现镜像的测试；最终 `.4` target assertion只补充能检测实际同版本stale/source mismatch与合法新revision的既有维护用例。

## P6. 完成和确认边界

当前三份规划通过不代表 activation。Activation、TaskCommit、push/PR、merge、两次维护操作、Finish/bookkeeping与cleanup各由其原owner展示精确目标/refs/文件/命令，按当前对话中适用的确认执行。必要恢复沿原同操作ref继续，不用一次确认扩展source或写集。

整体完成条件：A575-01..08与S2唯一Test一致，M真实native/下一owner完成，tracked投影无漂移，全部准备交付与Docs晋升通过原门禁，无遗漏剩余工作；Closure no_mutation；Finish独立bookkeeping合并。Task归档不关闭#575，也不创建 `.4` tag/Release。
