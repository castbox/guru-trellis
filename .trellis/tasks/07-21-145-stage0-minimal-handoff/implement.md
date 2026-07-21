# #145 实施计划：Stage 0 最小 typed handoff 原子迁移

## 1. 实现前门禁

- [ ] `guru-review-contract-wording:planning_artifacts` 对当前 `prd.md`、`design.md`、
  `implement.md` 返回 checker-passed `pass`。
- [ ] 用户查看三份规划链接后给出独立、明确的实现确认；Phase 0 workspace确认不得复用。
- [ ] `guru-approve-task-plan` 对当前三份文档返回 checker-passed `approved`，且
  `check-planning-approval.sh --json` freshness通过。
- [ ] Scope-change re-entry 将旧 `planning-approval.json`、`contract-wording-review.json` 与
  `phase2-check.json` 判为 stale；完成新 wording/plan approval 后，由
  `guru-clarify-requirements` checker 验证 GitHub authority、刷新 context、规划、ledger
  decision trail与 re-entry owners，再恢复已暂停的 `in_progress` task。
- [ ] Workspace boundary仍指向
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/145-stage0-minimal-handoff`，
  branch为 `feat/145-stage0-minimal-handoff`，base为 `main`。
- [ ] 按 `trellis-before-dev` 加载其输出的 `.trellis/spec/` 清单。
- [ ] 当前 `codex.dispatch_mode=sub-agent` 下，由 `trellis-implement`/`implement` agent负责实现，由独立
  `trellis-check`/`check` agent负责 Phase 2检查；主会话只协调、运行 recorder/validator、
  修复整合与后续 commit/review。
- [ ] Docs strategy固定为 `ssot_first`，Middle-platform Knowledge Gate为“不适用”。

## 2. 有序实现步骤

### Step 1. Durable SSOT 与 migration manifest baseline

- [ ] 按 `design.md` 12.3先更新 workflow/preset/docs specs、requirements docs。
- [ ] 把 #145 comment 5037168364 的 D1 optional scalar与 D2 production semantic eval
  execution closure同步到 durable contracts；#144/#147 保持 closed authority refs。
- [ ] 新增 `guru-team-stage0-migration-manifest-1.0` closed schema与
  `migrations/stage0-minimal-handoff.json`。
- [ ] 在 manifest 中精确登记6 Skills、24 exits、4.1 input profiles/signature、per-exit
  output/consumer/projection ids、private artifacts、eval bindings与 #146 legacy allowlist。
- [ ] 增加 manifest set-equality tests，覆盖 missing/extra/duplicate/renamed/unknown/mixed
  version负例。

Checkpoint：durable contract与 manifest先通过 JSON/schema测试；任何 stable id、semantic
owner、consumer或范围变化都暂停实现并重新 planning approval。

### Step 2. Consumer-owned input contracts

- [ ] 为六个 package实现 `design.md` 4.1 的 structured profiles或 scalar signature。
- [ ] `guru-sync-base`只声明 scalar CLI arguments/examples，不新增 input JSON schema。
- [ ] 将 Interface 1.3 `scalarArgument.required`改为必填 boolean；现有 scalar arguments
  显式保留 `required:true`，`guru-sync-base.base_branch`声明 `required:false`。
- [ ] 为 `guru-sync-base` 增加携带与省略 `--base-branch` 的 executable examples、public
  invocation probes与 schema/dispatch负例；省略路径必须走同一 owner resolver order。
- [ ] 为 Skill consumers把 input schema放在目标 package；为 workflow routers/transitions在
  `trellis/workflows/guru-team/consumers/stage0/`新增 closed schemas；stop使用
  `zero_payload`。
- [ ] 确认 input只含 caller-owned值和必要 locator；live facts、digest与file metadata由
  runtime派生。
- [ ] 为每个 profile/signature增加完整 input example和 schema/argv负例。

Checkpoint：每个 consumer input都有唯一 owner与真实 caller；无 optional/null mega object、
无人消费 schema或 private artifact body。

### Step 3. 六包 Interface 1.3 与 24 output contracts

- [ ] 将六个 canonical `interface.json`切换到
  `skill-interface-1.3.schema.json`与 `schema_version=1.3`。
- [ ] 为24 exits分别新增 closed output schema和完整 example。
- [ ] 声明每个 exact consumer input与 direct/select/rename/normalize projection。
- [ ] 为每个 output property登记 `consumer_use_ids`和目标 consumer pointer；增加
  unconsumed field、private field、unknown operation、wrong consumer负例。
- [ ] 把现有 artifact登记为 `runtime_checkpoint|gate_evidence`及正确 persistence；不改变
  published private schema id/body。
- [ ] 更新 package `SKILL.md`、`references/contract.md`与 contract tests，保持 judgment
  mode、stage order、confirmation与副作用边界。

Checkpoint：`discover-skill-contract` source mode对六包返回 `minimal_handoff`，24 examples
全部通过对应 output schema；#146三包仍返回 `legacy`。

### Step 4. Public wrappers 与 runtime projection

- [ ] 为六包新增 thin public invocation wrapper并登记 executable mode。
- [ ] Shared runtime读取 public input、live Git/GitHub/Trellis facts与owner private locator，
  调用现有 recorder/checker/executor，最终只序列化一个 typed-exit DTO。
- [ ] 实现/复用 declarative projection执行，不新增 operation或semantic routing。
- [ ] Runtime负责 digest、hash/size/mtime、absolute path与freshness重算；Agent-facing input
  不要求这些字段。
- [ ] Stable errors只含 `code`、`field_path`、`remediation`。
- [ ] 增加静态/trace测试证明 wrappers、normal Agent与consumer不读取/import
  `guru_team_trellis.py`，普通 invocation不加载 `evals/`。
- [ ] `guru-sync-base` wrapper在 flag省略时向正式 owner resolver传递未指定状态；`synced`
  output只能投影 checker-passed owner result中的 selected base。
- [ ] Semantic wrappers只接受 repo-local owner result locator，并在序列化 DTO 前执行对应
  checker；实际 route必须来自 checker-passed result，不得接受 caller-selected exit。

Checkpoint：每个 input profile/signature执行一次或多次真实 wrapper invocation；每次stdout只有
一个 declared exit并通过对应 schema。

### Step 5. Registry、extension 与 atomic activation

- [ ] 同时把六个 registry entries切换到1.3 + `minimal_handoff`；active总数仍为9。
- [ ] Extension `legacy_skill_ids`精确保留
  `guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit`。
- [ ] 更新 public/private schema exact inventories、migration manifest locator、managed
  paths、release version/note与source/installed facts。
- [ ] 更新 source/installed validator，强制 registry/interface/workflow/extension/manifest
  6×24双向 set equality和 mixed-graph rejection。
- [ ] 在 preset installer使用完整 staging transaction；只有客观证明一次 transaction
  不可行时才实现 design 8.3 versioned public DTO adapter，并同时实现 removal test。
- [ ] 增加 pre-#145 installed fixture，验证旧完整1.2 graph升级为完整1.3 Stage 0 graph，
  不出现1.2/1.3混合激活。

Checkpoint：source tree与staged install均为“六包全部minimal + 三包legacy”，任何中间状态
在validator中失败关闭。

### Step 6. 六份 production eval corpora 与 runner/adapter closure

- [ ] 为六包各新增唯一 canonical `evals/evals.json`及必要 `evals/files/`。
- [ ] 每个24 exit与每个 input profile/signature绑定一个或多个 current case；case ids在package
  内唯一，manifest binding非空且无重复。
- [ ] 覆盖 normal、refresh/re-entry、blocked/stop、retarget、content-changed、issue-only
  initial/recovery、workspace/task initial/recovery。
- [ ] Cases只exact-ref Interface/profile/exit/schema/projection，不复制 public/private合同。
- [ ] 用 `discover-skill-evals`/`run-skill-evals`执行 shared adapter完整corpus；runner实际
  调用 wrapper，semantic cases提供 checker-passed repo-local owner result，semantic
  assertions只消费外部 grading/human input。
- [ ] Runner先读取 actual exit并按 actual exit校验 output schema，再比较
  `expected_exit`；测试证明所有24个 cases均未把 `expected_exit`传给 wrapper、owner result
  builder或 route selector。
- [ ] 执行 Codex trusted Git context、Claude input protocol、Cursor unavailable/unsupported
  与 shared parse/execute tests，比较同一 corpus bytes；Cursor native能力缺失时精确记录
  `unsupported`，不得合成 pass。
- [ ] 限定 #147 基础设施修改面为 D2 所需的 runner、adapter、public dispatch、validator、
  fixtures、tests与文档；eval schema、grader policy、run evidence和semantic owner保持不变。

Checkpoint：coverage manifest对6×24与全部profiles闭合，runner实际执行public wrapper；
actual exit来自checker-passed owner result，`expected_exit`只执行事后断言；四平台协议结果
与同一 corpus bytes绑定。

### Step 7. Preset、dogfood 与四平台同步

- [ ] 更新 preset managed assets、mode、installed manifest、installer tests与throwaway
  inventory。
- [ ] 更新 canonical workflow/preset README与root README中的1.3 production状态、discovery/
  eval命令、#146 legacy边界和upgrade说明。
- [ ] 运行 canonical preset apply同步 `.trellis/guru-team/`、`.agents/skills/`、
  `.codex/skills/`、`.cursor/skills/`、`.claude/skills/`。
- [ ] 逐项处理 `.new`/`.bak`，不得静默覆盖用户文件；运行dogfood overlay drift与upstream
  ownership检查。
- [ ] 比较六包 Interface/schemas/examples/wrappers/evals在canonical、installed与四平台
  roots的bytes和executable mode。

Checkpoint：dogfood source/installed validation均通过，overlay drift为零，递归sidecar扫描
为空。

### Step 8. Clean throwaway、update/reapply 与 existing-state验证

- [ ] 在干净临时repo运行workflow marketplace init与guru-team id/path/type检查。
- [ ] 验证已有项目workflow `--create-new` preview与正式switch。
- [ ] 安装preset并运行六包contract discovery、6×24 set equality、完整Stage 0 normal route。
- [ ] 在 clean install 与 pre-#145 upgrade 两条路径分别验证 `guru-sync-base` 显式 base和
  optional fallback，并验证 shared/Codex/Claude/Cursor production eval兼容矩阵。
- [ ] 执行refresh/re-entry/stop/retarget/content-changed/issue/workspace recovery fixtures。
- [ ] 从pre-#145 fixture升级，运行 `trellis update`、preset reapply并重复上述验证。
- [ ] 验证existing active task通过owner re-entry进入1.3，archive仍按旧schema只读。
- [ ] 最终扫描throwaway与dogfood无 `.new`/`.bak`、无mixed graph、无private runtime import。

### Step 9. Docs reconciliation 与 Phase 2 handoff

- [ ] 更新 `docs/requirements/README.md`、`requirement-main.md`、
  `guru-team-trellis-flow.md`与三份public README。
- [ ] 对照Docs SSOT Plan记录实际更新、task delta merge、task-history-only内容、无update或
  follow-up/PR限制。
- [ ] Implementation handoff列出所有修改路径、R/AC承接、validation、existing-state与
  deployment/safety影响。
- [ ] 独立 `trellis-check` agent检查durable docs/task artifacts/code/API/schema/config/test/
  install/update一致性；主会话只在完整AI报告后record/check `phase2-check.json`。

## 3. 预计修改面

### Canonical contracts/packages/runtime

- `.trellis/spec/workflow/{index,skill-package-contract,data-contracts,companion-scripts,quality-guidelines}.md`
- `.trellis/spec/preset/{installer,overlay-guidelines,upstream-ownership}.md`
- `.trellis/spec/docs/public-docs.md`
- `trellis/skills/guru-team/migrations/stage0-minimal-handoff.json`
- `trellis/skills/guru-team/schemas/stage0-migration-manifest.schema.json`
- `trellis/skills/guru-team/packages/{guru-sync-base,guru-discover-change-context,guru-clarify-requirements,guru-review-contract-wording,guru-review-change-request,guru-create-task-workspace}/**`
- `trellis/skills/guru-team/registry.json`
- `trellis/workflows/guru-team/consumers/stage0/**`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`及其tests
- `trellis/skills/guru-team/schemas/skill-interface-1.3.schema.json`、eval runner/adapter
  public contracts与 `trellis/skills/guru-team/tests/test_skill_packages.py`
- `trellis/guru-team-extension.json`

### Distribution/docs

- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`及tests
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- 必要的canonical overlay inventory/source；不把dogfood copy当source
- `.trellis/guru-team/**`与shared/Codex/Cursor/Claude installed copies
- `docs/requirements/{README,requirement-main,guru-team-trellis-flow}.md`
- `README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`

若实现证明某个“预计修改面”无需修改，Phase 2 handoff必须给出基于当前diff与consumer的
明确 no-update reason；不得使用泛化的条件占位语替代判断。

## 4. Validation commands

路径和新增test selector在实现时按实际文件名精确化；以下命令族全部必跑，任一子集通过
不能替代完整门禁。

```bash
python3 -m json.tool trellis/skills/guru-team/migrations/stage0-minimal-handoff.json
python3 -m json.tool trellis/skills/guru-team/schemas/stage0-migration-manifest.schema.json
python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
python3 -m py_compile \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh \
  trellis/presets/guru-team/scripts/bash/*.sh
trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode source
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode installed
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 ./.trellis/scripts/task.py validate 07-21-145-stage0-minimal-handoff
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json \
  --task .trellis/tasks/07-21-145-stage0-minimal-handoff
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
git diff --check
```

必须额外执行并记录：

```bash
# 六包 source/installed contract discovery
# 六包 shared adapter 的 canonical eval corpora full run
# guru-sync-base explicit base + omitted base fixed resolver probes
# actual-exit schema validation + expected_exit non-oracle negative tests
# Codex trusted Git context、Claude input protocol、Cursor unavailable/unsupported与corpus byte identity
# checker-passed repo-local semantic owner-result cases
# 6 Skills/24 exits/profile/case/consumer/projection set equality
# normal Agent transcript: public_invocation_only + private_runtime_not_read_by_agent
# clean throwaway pre-#145 upgrade + update + preset reapply + full Stage 0 rerun
# existing active re-entry + archive read-only fixtures
```

## 5. Review gates

- Contract gate：6×24 exact set、profiles、schema ids、consumer/projection与manifest一致。
- Minimality gate：每个public output field有直接consumer pointer；private/audit字段未泄漏。
- Semantic boundary gate：AI仍做scope/review/confirmation/route判断，脚本只执行确定性事实。
- Invocation gate：每个profile/signature与24 exits均由真实public wrapper执行验证。
- Compatibility gate：stable ids/owners/confirmations/private schema/archive读取不回归，#146
  三包仍legacy。
- Activation gate：source/staged/installed出现mixed Stage 0 graph时必须失败。
- Eval gate：六份canonical corpus通过production runner；actual exit决定schema，
  `expected_exit`只做事后断言；checker-passed owner result与四平台协议均有证据，且不fork
  corpus/grader policy。
- Distribution gate：canonical/installed/dogfood/四平台byte/mode一致。
- Upgrade gate：fresh install、pre-#145 upgrade、update/reapply后同样通过且零sidecar。
- Docs gate：Docs SSOT Plan已执行，无current-scope durable docs不一致。

## 6. Rollback points

| Point | Trigger | Action |
| --- | --- | --- |
| RP1 | Consumer无法以最小DTO完成下一步 | 暂停并修订consumer schema/field proof；不得暴露完整private artifact |
| RP2 | Interface/schema需要stable id或semantic owner变化 | 停止实现，更新三份规划并重新planning approval |
| RP3 | Source validation出现mixed graph | 不执行preset apply，修复完整六包activation后重跑 |
| RP4 | Preset staging/install产生冲突或sidecar | 保留原完整安装，处理canonical/provenance后整包reapply |
| RP5 | D2 之外仍要求修改 eval schema、grader policy、semantic ownership 或 run evidence | 停止实现并回到 scope clarification；不得借 production closure 扩张 #147 基础合同 |
| RP6 | Existing active/archive兼容失败 | 保留旧schema读取，修复owner re-entry/adapter；不得回写archive |
| RP7 | Native platform能力缺失 | 返回`unsupported`并明确未验证风险，不生成平台专用corpus |

## 7. Docs SSOT checkpoint

- Strategy：`ssot_first`。
- 实现前：先更新design 12.3列出的durable contracts。
- 实现中：task artifact只保留delta、取舍与证据，不成为平行长期规范。
- Phase 2前：逐项核对docs、Interface、runtime、manifest、registry、extension、installer、
  evals、help与tests一致。
- Commit前：记录实际docs文件、已合并task delta、task-history-only内容、existing-state
  兼容、throwaway/update/reapply与无sidecar证据。

## 8. 完成清单

- [ ] R1-R9均有代码、schema、测试或文档证据。
- [ ] AC1-AC15全部通过。
- [ ] Implementation与check sub-agent liveness/handoff完整。
- [ ] `guru-check-task` checker-passed，零未解决finding。
- [ ] `guru-create-task-commit`完成reviewed task commit。
- [ ] 独立Branch Review覆盖`origin/main...HEAD`并通过。
- [ ] `trellis-continue`停在Branch Review Gate；只有用户后续明确调用
  `trellis-finish-work`才执行push、draft PR、archive与ready closeout。
