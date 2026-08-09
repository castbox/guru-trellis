# #179 Implementation Plan

## 1. Ordered Checklist

- [x] I1. 建立完整 current owner/consumer/asset inventory：Publication、Finalizer、Task Commit、Branch Review、finish-summary history reader、shared runtime、schema/interface/example/eval/test、workflow/README/manifest/ownership/installed copies；历史 archive从修改集排除。
- [x] I2. 先修订 Docs SSOT Plan列出的 durable specs，固化 ready/input 4.0、exact PR payload、summary单次派生、commit-message去权威化与旧shape fail-closed合同。
- [x] I3. 修改 canonical `guru-review-task-publication`：AI owner直接生成title/body，更新十维gate、private readiness schema、ready 4.0 output、Finalizer authoring-seed consumer、examples/evals/tests；删除两个task-local文件输入与metadata artifact revision路径。
- [x] I4. 修改 canonical `guru-finalize-task`：publication_ready 4.0直接消费payload；closeout plan绑定exact title/body；preview/recovery/PR create-update/remote validation不再读取`pr-body.md`或summary-index文件；六出口状态机保持不变。
- [x] I5. 修改 finish-summary current builder与schema/history reader：从reviewed PR payload和live facts一次生成archive summary；覆盖新summary检索与历史schema读取；删除独立index recorder/loader/validator/CLI flag/fixture/inventory依赖。
- [x] I6. 收敛 commit identity：保留Task Commit首次authoring gate，删除Branch Review/Publication/Finalizer对subject/body/`Refs`的跨Skill freshness依赖和metadata-only revision路径；更新接口prerequisite、runtime与回归测试。
- [x] I7. 删除固定human artifact表与重复Docs SSOT填表要求，保留Phase 1 Docs SSOT Plan、owner docs reconciliation和PR body文档同步结论。
- [x] I8. 更新 canonical workflow、三份public README、extension manifest、registry/consumer contracts、managed asset/ownership inventory与throwaway verifier；stable Skill/exit/target/command id保持不变。
- [x] I9. 运行preset installer同步`.trellis/guru-team/**`、`.trellis/workflow.md`、`.agents/**`、`.codex/**`、`.claude/**`、`.cursor/**`及manifest声明的平台副本；逐个处理`.new`/`.bak`。
- [x] I10. 执行targeted runtime/package/integration tests，覆盖payload bytes、schema migration、projection、preflight、same-plan recovery、summary generation/history retrieval、message-independent downstream freshness和retired-path zero-hit。
- [x] I11. 执行完整source/installed/preset/dogfood/throwaway/update-reapply门禁，记录exact remote marketplace source在push前的未验证边界。
- [x] I12. 在base evolution与durable docs finding修复后执行首次fresh current-only Phase 2 semantic check；修复全部P0-P3 finding并重跑受影响证据。commit、Branch Review、push、PR、Finalizer副作用不在本计划自动执行。
- [x] I13. 真实Finalizer恢复暴露recorder覆盖legacy gate后，按用户授权的finding-fix例外保留legacy gate并引入同owner ignored transition gate，补`record -> check -> execute`真实回归，重新执行current Phase 2、Task Commit、current-HEAD Branch Review与Publication；provenance tail只刷新Finalizer metadata，不重复这些上游门禁。

## 2. Primary Files and Rollback Points

- Shared runtime：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、`test_guru_team_trellis.py`、finish-summary schema。风险最高，先以targeted tests固定current behavior再删除reader。
- Publication package：`trellis/skills/guru-team/packages/guru-review-task-publication/**`。interface/schema/example/eval/test与private gate必须同批闭合。
- Finalizer package：`trellis/skills/guru-team/packages/guru-finalize-task/**`。只改变publication input与payload来源，不改六出口transaction state machine。
- Commit/Branch edge：`guru-create-task-commit/**`、`guru-review-branch/**`及finish-family integration tests。工作提交authoring与下游freshness必须分离。
- Distribution：`trellis/guru-team-extension.json`、preset scripts/README/ownership、canonical workflow/README与installed copies。同步只从canonical流向安装副本。
- Durable docs：Docs SSOT Plan列出的`.trellis/spec/**`。

## 3. Validation Commands

Targeted first：

```bash
python3 -m unittest trellis/skills/guru-team/packages/guru-review-task-publication/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-review-branch/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/tests/test_finish_family_integration.py
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
```

Distribution and complete gates：

```bash
python3 -m unittest trellis/skills/guru-team/tests/test_skill_packages.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-08-179-remove-publication-handoff
git diff --check
```

Static current-contract scans：

```bash
rg -n "finish-summary-index\.json|pr-body\.md" trellis .trellis .agents .codex .claude .cursor README.md
rg -n "commit_handoff|subject/body|Refs #|metadata-only commit" trellis .trellis .agents .codex .claude .cursor README.md
find . -name '*.new' -o -name '*.bak'
```

扫描结果必须逐项分类：active canonical/installed/runtime/package/test/docs命中清零；只读历史archive、Issue/task planning引用和明确的退役断言不计为active dependency。

## 4. Required Regression Matrix

| Case | Expected result |
| --- | --- |
| Publication normal ready | ready 4.0 exact输出title/body，checkpoint在projection后删除 |
| Publication metadata revision | 只重审payload依赖维度，不修改tracked task artifact |
| Publication content drift | `return_to_task_work`，不产生ready |
| Finalizer first preview | DTO + live facts生成同一immutable plan，不读取退役文件 |
| Finalizer same-plan resume | 从plan恢复exact payload，已有Draft metadata按同一PR收敛 |
| PR payload UTF-8 edge | 中文、换行、Markdown-sensitive spaces经projection/plan/GitHub保持exact equality |
| Finish summary current | 从reviewed body/live facts生成schema-valid summary与可检索index |
| Finish summary historical | 既有archive schema继续被history discovery读取 |
| Commit message deviation | 下游不要求metadata commit；content identity不变时继续审查 |
| Reviewed-content descendant | Publication/Finalizer仍返回task-work stale route |
| Clean install/update | source/installed字节一致、无retired asset、无sidecar、全平台入口一致 |

## 5. Acceptance Mapping

- A1-A2：I1、I3-I5、I7-I9，current-path扫描与throwaway fresh task。
- A3-A4：I3，Interface projection、ready/private gate与semantic package tests。
- A5-A6：I4-I5，Finalizer preflight/recovery与new/old summary history integration。
- A7：I6，commit/Branch/Publication/Finalizer回归矩阵。
- A8：I2、I7-I8，Docs SSOT review与workflow/README一致性。
- A9：I3-I4、I8-I10，schema id、consumer graph、old-shape rejection与installed closure。
- A10：I9-I11，完整分发、语法、格式、ownership、dogfood、throwaway/update门禁。
- A11：I12及后续独立Branch Review；remote marketplace证据保持独立状态。

## 6. Pre-Start Gates

- `guru-review-contract-wording:planning_artifacts` 必须覆盖三份current planning文件，七个planning semantic dimensions全部为true。
- `guru-approve-task-plan` 必须审查live Issue #179、scope ledger、Docs SSOT Plan、public schema迁移、Finalizer边界、测试矩阵与out-of-scope #180。
- approved exit可自动执行`task.py start`；该状态写入不授权commit、push、PR、Finalizer transaction或cleanup。

## 7. Base Evolution Recovery

- 2026-08-09：远端 `main` 的 `2e38ae0ea68de46842d5a4ca60492874e4c47525` 已通过 PR #192 合并 #191；当前已发布 #179 分支以 `--no-ff` merge 吸收该前置修复，不 rebase、不 force-push。
- 合并解析保留 #179 的 Publication payload/退役 handoff 合同，并将 #191 的 `reviewed_content_head`、`publication_head`、`provenance_tail_required` 与版本化 verification DTO 作为 current runtime；Finalizer aggregate current schema 为 5.0，旧 3.0/4.0 保持兼容资产。
- 合并恢复实现验证通过：Publication/Finalizer、Task Commit、Branch Review 与 finish-family owner 合同 60 项、共享 runtime 414 项、preset installer 45 项、Skill package closure 180 项，共 699 项；Python compile、Bash syntax、task validation、ownership、dogfood drift、JSON、diff hygiene 和零 sidecar 检查通过。
- throwaway fresh install、official update、workflow switch、preset reapply 与 no-developer fixture 已通过。因分支尚未push，public main + local unpublished workflow sample 仅证明本地安装闭环；current exact-ref marketplace source仍由push后的Finalizer gate验证。
- 唯一未完成证据是 push 后 exact remote marketplace ref verification；该检查仍由 Finalizer 的既有 publication transaction gate 拥有，不冒充本地通过。

## 8. Finalizer Gate Supersession Finding Fix

- 2026-08-09：首次checked recovery证明标准`record-finalization-gate -> check-finalization-gate`不可达，因为recorder把current `reprepare_required` marker写回唯一gate路径，覆盖了同一次checker必须复核的pre-#191 legacy `verification_required` gate。
- 修复保持public Skill I/O、schema id、exit、transaction order不变：仅base-evolution window把current marker写入`task-finalization-transition-gate.json`，legacy gate保持byte-identical；checker限制两者只在该window共存，executor成功后同时退休两者、旧plan与匹配request。
- 新fixture真实调用recorder、checker与executor，并在每轮preview执行base-evolution preflight；另覆盖transition gate缺少legacy predecessor时fail closed。该finding改变runtime与durable contract，因此按用户明确例外重新生成current Phase 2、Branch Review与Publication证据。
- finding-fix current验证：共享runtime 416/416、Publication/Finalizer/Task Commit/Branch Review/finish-family与Skill package closure 240/240、preset installer 45/45均通过；clean throwaway完成public marketplace discovery、本地未发布workflow sample、fresh install、official update、workflow switch、二次preset reapply、两轮installed finish-family与no-developer fixture，最终零sidecar。current exact-ref marketplace source仍只由push后的Finalizer gate验证。

## 9. Publication Public Schema Migration Finding Fix

- 2026-08-09：current-HEAD Branch Review 发现已发布的 Publication `public-ready-output.schema.json` 3.0 被原路径升级为4.0，旧 `$id`、bytes与interface inventory未保留；该正常升级路径违反public schema兼容合同，属于#179 R6/A9范围内P2 finding。
- 修复恢复原3.0 schema path与bytes，SHA-256为`57d984c5ef50b9ab2f4fa5e15fbde58c59ad76e563e1690d7cc4c6ceafc6062c`；新增`public-ready-output-4.0.schema.json`作为current output，并由Interface显式保留legacy inventory、选择current 4.0 output及既有Finalizer projection。
- 回归测试分别验证legacy/current payload、双向cross-version rejection、legacy byte digest和current Publication到Finalizer projection；canonical、shared installed及Claude/Codex/Cursor副本经`apply.sh --all-platforms`两轮幂等同步，最终零`.new/.bak/.rej/.orig`与零sidecar。
- finding-fix current验证：共享runtime 416/416、Publication/Finalizer/Task Commit/Branch Review/finish-family与Skill package closure 241/241、preset installer 45/45均通过；Python/Bash syntax、task validation、ownership、dogfood drift、`git diff --check`通过。clean throwaway完成public marketplace discovery、本地未发布workflow sample、fresh install、official update、workflow switch、preset reapply与installed checks；push前current exact-ref marketplace source仍保持未验证。
