# #237 实施计划

## 1. 实施原则

- 从 `origin/main@60a2e962b68a02d08061795cfe9fafcdff206e80` 的当前 task branch
  实施。
- 先 canonical、后生成/安装副本；不得手工让 dogfood 成为唯一源头。
- AI 负责 qualification、finding、scope、severity 与 route；新 Skill runtime 只通过
  stdin/stdout/内存序列化并校验确定性事实，不写 qualification state。
- 每次出现 planning 外新行为场景，先作为 candidate，经
  `implementation_discovery` fresh qualification 后才继续编辑或补测试。
- 不触碰 #236、#220、#127 的 worktree/task/runtime，不创建 tag/Release 或业务仓升级。

## 2. Phase A：建立新 public Skill package

1. 从最接近的 semantic closed-loop package 复制结构，不复制其业务语义。
2. 创建 `guru-qualify-normal-scenario` 的 SKILL、contract、additive Interface 1.6、
   commands、wrappers、runtime、schemas、examples、evals 与 tests；aggregate public
   input 通过 `profile_selector.field=profile` 选择十个 closed profiles，既有 Interface
   1.4/1.5 字节和语义保持不变。
3. 实现十个 closed input profiles、十一 candidate decisions、四 exits、固定 consumers
   和 projections。
4. 实现 scope-first AI forward behavior、安全反向举证、severity quarantine、
   mechanism revision 和 invocation-local freshness。
5. Process-local recorder/checker 只从 stdin 读取并在内存中校验 shape、identity、
   freshness、enum、candidate completeness 与 consumer binding，再写 stdout；不接受
   output/result/checkpoint locator，不写 tracked、ignored runtime 或临时跨进程结果。
   测试禁止关键词分类和 runtime semantic route。
6. 为 unknown/extra/null field、caller/profile mismatch、empty/duplicate candidate、
   multiple/no decision、stale target、consumer mismatch 和 private-field projection 添加
   fail-closed tests。

## 3. Phase B：Registry、workflow 与 routing

1. 在 registry 中添加 active Skill 与四平台 destinations。
2. 更新 current `production-current-v4` contract/eval bindings，使新 Skill 的十
   profiles 和四 exits 进入真实 production corpus；`production-current.json` 与
   extension 只选择这一 current activation manifest，v2/v3 保留为 immutable legacy
   assets。
3. 在 canonical workflow 添加 stable invocation marker、十 profile 触发/返回点、两个
   routers 和 blocked stop。
4. 同步 dogfood `.trellis/workflow.md`，运行 workflow marker/consumer/projection closure
   tests；由 validator 计算并更新图数量断言，不手写不一致 totals。
5. 验证 unknown/multiple/unmapped/profile mismatch 路由全部 fail closed。

## 4. Phase C：十个 caller 与 worker 边界

1. `guru-execute-task-free-change`：接入 `task_free_pre_write` 和
   `task_free_evolution`。
2. `guru-clarify-requirements`：接入 `requirements_scope_set`，已排除场景不得提问。
3. `guru-review-change-request`：接入 `change_request_candidate_set`。
4. `guru-approve-task-plan`：接入 `planning_scenario_set`，acceptance/negative test/新增
   行为约束先资格化。
5. Phase 2 coordinator 的每次 worker dispatch prompt 接入
   `implementation_discovery` 边界：只授权 approved-plan work；planning-external
   observation 仅返回 candidate ref、观察、locator 与最小复现线索，fresh qualification
   前不得 edit、补 test 或 self-fix。
6. `guru-reconcile-task-base`：接入 `base_impact_candidate_set`。
7. `guru-check-task`：接入 `phase2_candidate_set`，资格完成前禁止 scope decision、
   severity 和 `implementation_required|planning_stale`。
8. `guru-review-branch`：接入 `branch_review_candidate_set`，完整 range 的所有 candidate
   fresh 判断。
9. `guru-review-task-publication`：接入 `publication_candidate_set`，未要求加固不得返回
   task work 或 blocked。
10. 保持 upstream-owned research/implement/check、channel runtime 和平台 agent bytes
    不变；在 Guru-owned workflow/caller invocation 与 consumer contracts 中强制上述
    candidate-only 投影，并增加 ownership negative tests，拒绝 preset claim/patch
    官方 agent 路径。

## 5. Phase D：Existing owner gate witness 与 schema migration

1. 盘点 Phase 2、Branch Review、Publication 当前 owner-private gate 与 direct
   consumers。
2. 为发生 shape 变化的既有 owner gate 发布新 schema version，加入 direct consumer
   使用的最小 candidate classification 和 witness refs；由各阶段 Owner 在当前 round
   直接写入，不读取或引用新 Skill artifact/result/checkpoint。
3. 移除“`normal_path_reproduction` 非空即可充分”的 validator 假设。
4. 旧 owner gate checkpoint 明确 stale 并要求对应阶段 Owner 完整重跑；不增加 public
   DTO 字段、shared qualification locator 或长期迁移 artifact。
5. 增加 schema/current-identity/re-entry/consumer tests。
6. 增加 zero-residue tests：对 clean throwaway repository 的调用前后完整 file inventory
   做完全一致比较，并扫描 tracked、ignored `.trellis/.runtime/**` 与 repository 临时文件；
   任一 qualification result/report/checkpoint、candidate/rejection ledger、跨进程 result
   locator 或 sidecar 均阻断。

## 6. Phase E：Semantic eval matrix

1. 建立 profile × scenario × pressure framing × paired legitimate 的 canonical matrix；
   case ids 稳定、去重且可机器枚举。
2. 每个 case 通过 clean installed public package 和 real wrapper 执行，不向 native
   context 暴露 expected decision/route 或 canonical eval corpus。
3. Host-only `input_profile_id` 只用于模型返回后的 grading；adapter/native/model/public
   invocation 不携带 `profile_id` 或 `input_profile_id`。模型生成的完整 stdin 原样交给
   installed wrapper，adapter 仅从同一 stdin envelope 记录最小 public `profile`
   binding receipt。
4. 保留 GPT-5.6 Sol matrix 的配置与 fail-fast runner contract，但本 Issue 不执行 live
   model invocation；以 deterministic/no-model fake production path 验证 request、dispatch、
   wrapper、trace、grading boundary 与 failure propagation。
5. 覆盖 #113 F-001、#236 alias/wrapper/`shell=True`/`sh -c` 及所有 pressure framing。
6. 覆盖 paired legitimate digest/payload、real runtime caller、redaction、permission/
   destructive confirmation、stale/mismatch、executor/maintenance errors。
7. 增加模型/prompt/package/matrix identity invalidation 和不同 Owner 独立 eval review。
8. 确认任何脚本均未通过关键词匹配生成 semantic decision。

## 7. Phase F：Docs SSOT 与安装投影

Docs SSOT strategy：`ssot_first`。

1. 更新 canonical workflow 与五份 durable workflow specs：
   `workflow-contract.md`、`skill-package-contract.md`、`data-contracts.md`、
   `companion-scripts.md`、`quality-guidelines.md`。
2. 更新 preset installer/upstream ownership/docs contracts 与 workflow/preset README；
   只描述分层、公共 I/O、consumer mapping、安装与验证保证。
3. 更新 canonical package/registry/extension manifest，运行 preset apply 生成 shared、
   Codex、Claude、Cursor 和 dogfood copies。
4. 检查所有 platform copies byte/mode 一致；显式 overlay 集合仍只有三个
   `guru-finish-work` entries。
5. 运行 dogfood drift 与 recursive `.new`/`.bak`/unknown sidecar 检查。

## 8. Validation Matrix

### 8.1 Static 与 package

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
for root in (Path("trellis/skills/guru-team/runtime"), Path("trellis/skills/guru-team/packages")):
    for path in root.rglob("*.py"):
        compile(path.read_bytes(), str(path), "exec")
PY
python3 ./.trellis/scripts/task.py validate 08-15-237-normal-scenario-qualification
git diff --check
```

运行新 package、八个 caller packages、registry/interface/projection、workflow route、
existing owner gate migration、zero-residue、worker boundary 和 eval adapter 的 targeted
tests。

### 8.2 Canonical 与 dogfood

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

处理并记录所有 `.new`/`.bak`；最终数量必须为零。

### 8.3 Clean install、CLI upgrade、project update 与 reapply

官方 live 文档明确：`trellis upgrade` 把全局 CLI 升到发布版本，`trellis update` 再把
项目同步到本地 CLI 版本；二者是完整升级的连续两步。验证在 disposable directory 中
按以下顺序执行，环境变量只指向 disposable npm prefix，不修改开发机 global npm：

```bash
upgrade_root="$(mktemp -d "${TMPDIR:-/tmp}/guru-trellis-upgrade.XXXXXX")"
upgrade_prefix="$upgrade_root/npm-global"
npm_config_prefix="$upgrade_prefix" npm install -g @mindfoldhq/trellis@0.6.5
PATH="$upgrade_prefix/bin:$PATH" npm_config_prefix="$upgrade_prefix" trellis --version
PATH="$upgrade_prefix/bin:$PATH" npm_config_prefix="$upgrade_prefix" trellis upgrade --tag latest
PATH="$upgrade_prefix/bin:$PATH" npm_config_prefix="$upgrade_prefix" trellis --version
```

在同一隔离 CLI 下创建 clean throwaway repo，并使用当前 source ref 完成 marketplace
workflow initial install 与 canonical preset apply。验证 `trellis/index.json`、workflow
id/path/type、public Skill discovery、executable modes，并从 installed public entry 执行
全部十 profiles。随后在 existing-project 状态执行：

```bash
PATH="$upgrade_prefix/bin:$PATH" trellis update --dry-run
# dry-run/live output 含 MIGRATION REQUIRED 时执行下一行；否则执行 update --skip-all
PATH="$upgrade_prefix/bin:$PATH" trellis update --migrate --skip-all
PATH="$upgrade_prefix/bin:$PATH" trellis workflow \
  --marketplace "gh:castbox/guru-trellis/trellis#<reviewed-source-ref>" \
  --template guru-team --create-new
PATH="$upgrade_prefix/bin:$PATH" trellis workflow \
  --marketplace "gh:castbox/guru-trellis/trellis#<reviewed-source-ref>" \
  --template guru-team
<source-checkout>/trellis/presets/guru-team/scripts/bash/apply.sh --repo <throwaway-repo>
```

`<reviewed-source-ref>` 在执行时解析为包含当前 reviewed commit 的 existing branch/tag；
若该 ref 尚未存在，current-branch marketplace 结论保持 blocked。`<source-checkout>` 与
`<throwaway-repo>` 在执行时替换为本轮 exact disposable absolute paths。Project update
分支只有两个合法命令：输出 `MIGRATION REQUIRED` 时运行
`trellis update --migrate --skip-all`，其它输出运行 `trellis update --skip-all`；
`--skip-all` 保留已有修改并非交互继续，禁止使用 `--force` 或两者都运行后挑选结果。

完成 update、workflow preview/switch 与 preset reapply 后，重新验证 package、registry、
workflow、十 profiles、platform parity、ownership、dogfood、executable modes、零
`.new`/`.bak` 和零 qualification residue。最后运行 README 原始 throwaway verifier，
确认使用 #236 修复后的受管 Python 路径。

### 8.4 Production eval asset gate

- 不执行 GPT-5.6 Sol 或其它 live production model matrix。
- Deterministic/no-model tests 覆盖 production entry、十 profile contracts、pressure corpus、
  paired expected classification、真实 wrapper/trace、fail-fast 与零泄漏边界。
- 不同 Owner 检查未把 deterministic/no-model pass 写成模型通过，并明确没有 pressure
  matrix 或模型稳定性证据。

### 8.5 Complete Phase 2

- `guru-check-task` 对当前完整 task scope 运行，不用 targeted command 代替完整 check。
- 检查 Docs SSOT 已合入 canonical docs，existing owner gate witness 有 direct consumer，
  新 Skill 没有 tracked/ignored/temp qualification artifact、result locator 或 residue。
- Findings 修复后完整 rerun，而不是局部复用旧 qualification。

## 9. Phase 3 Gates

1. 在 commit 前展示 exact staging paths/commands 并取得单独授权。
2. 使用 `guru-create-task-commit` 创建 reviewed work commit。
3. 由不同 Owner 对 `origin/main...HEAD` 完整 current diff 执行 fresh Branch Review；不得
   使用 Phase 2 或旧 review 作为证明。
4. Branch Review findings 必须先通过 `branch_review_candidate_set` fresh qualification。
5. Publication readiness 检查中文 title/body、`Closes #237`、#113/#236 related-only、
   安全与部署影响、Docs SSOT、完整验证和真实模型结论。
6. Push/PR/Ready 各自展示 exact side effects，取得对应授权后执行。
7. 只有总编排发送“合并PR”且 live merge gate 全部满足后才执行 merge。

## 10. Stop Conditions

- Live #237 authority、base、task scope 或 caller graph 发生 material drift。
- 新候选无法通过 `implementation_discovery` 资格判断。
- Public package graph、consumer mapping 或 installed projection 不闭合。
- 任一 production eval invocation 误分类。
- Clean install/update/upgrade、ownership、dogfood 或零 sidecar 未通过。
- 独立 Branch Review 或 publication readiness 未通过。

上述情况均 fail closed；不创建 tag/Release，不升级业务仓。
