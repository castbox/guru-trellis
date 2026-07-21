# #147 实现计划：Guru Skill 行为评测基础设施

## 1. 实现前知识核对

- [ ] 读取 `prd.md`、`design.md` 与 planning approval，确认 Close 仅 #147，#145/#146 仍是 follow-up。
- [ ] 通过 `trellis-before-dev` 加载 `implement.jsonl` 的 spec/research 上下文。
- [ ] 确认 #144 Interface 1.3、registry 1.1、`discover-skill-contract`、representative wrappers 与 public/private SSOT 是复用基线。
- [ ] 确认 `middle_platform_knowledge` 不适用：本任务不接入业务中台 SDK/framework。
- [ ] 确认 Docs SSOT strategy 为 `ssot_first`，实现阶段必须先更新 durable contract 再收敛代码/测试。
- [ ] 确认只覆盖 honest-but-fallible 正常路径，不新增 hostile-input、锁、TOCTOU、压力或 fault-injection 机制。

## 2. 有序实现步骤

### Step 1. Durable contract 与 schema 基线

- [ ] 按 `design.md` 更新 `skill-package-contract.md`、`companion-scripts.md`、`data-contracts.md`、`quality-guidelines.md` 与 preset/docs specs。
- [ ] 新增 `guru-team-skill-evals-1.0` closed schema，固定 `evals/evals.json`、string id、required/optional non-empty fields、profile/files/assertions 结构。
- [ ] 定义 deterministic/semantic assertion、semantic grading、human feedback、adapter request/response 与 run evidence closed schemas；只创建真实消费边界需要的 schema。
- [ ] 为 stable errors 定义并复用 `code`、`field_path`、`remediation` 形状。

Checkpoint：先运行 schema JSON parsing 与 focused schema tests；任何 public id/path/field 调整都回写三份规划文档并重新进入 planning approval。

### Step 2. Representative corpus 与 legacy migration fixture

- [ ] 为 `guru-example-action` 增加 normal、repeat/re-entry、blocked cases。
- [ ] 为 `guru-example-sync` 增加 normal 与非成功 family cases；若现有 fixture runtime 无法产生设计要求的 declared exit，则只扩展 test-only fixture runtime，不改变 production Skills。
- [ ] 增加 `evals/files/` fixture、profile/exit refs 和 deterministic/semantic assertions。
- [ ] 增加 factory-style legacy `expectations` 单向 migration fixture；canonical writer/output 只含 `assertions`。
- [ ] 增加 PRD 5.2 的 corpus/path/ref/assertion negative mutations。

Checkpoint：同一 mixed fixture 验证 legacy Interface 1.2、Interface 1.3 public I/O 与新 eval corpus；fixture ids 不进入 production registry/manifest。

### Step 3. Discovery 与 validation runtime

- [ ] 在 shared runtime 实现 eval schema/ref/path/assertion validator，复用现有 registry/Interface/public contract discovery 和 safe path helpers。
- [ ] 新增 `discover-skill-evals` parser/handler 与 executable wrapper；返回 closed discovery DTO 或 stable error。
- [ ] 验证 source/installed roots、legacy/no-corpus、unknown Skill、version mismatch、missing asset 与 installed drift。
- [ ] 静态测试证明 validator 不生成 semantic judgment，不读取 task/private runtime 来补齐 corpus。

### Step 4. Runner、grader 与 evidence

- [ ] 新增 `run-skill-evals` parser/handler 与 executable wrapper。
- [ ] 实现 repo/package 外 `--run-root` boundary、case selection、file staging、actual exit、per-exit schema validation 与 trace collection。
- [ ] 实现 deterministic grader closed operations；禁止 arbitrary expression/script 和 semantic reconstruction。
- [ ] 实现外部 semantic grading/human feedback schema binding与机械汇总；缺失或失败进入 `evaluation_failed`，脚本不生成 semantic pass。
- [ ] 实现 `passed|evaluation_failed|execution_error|unsupported` 闭集和 expected non-success exit 正确分类。
- [ ] 实现 exact comparison pair；拒绝单边参数和浮动 ref 解释。
- [ ] 写入 closed temporary evidence；验证无 package/task/repo tracked output、gate/checkpoint/audit/release/provenance 字段。

Checkpoint：focused runner tests 必须证明每个 case 执行真实 public wrapper，不以 static shape 代替；normal invocation 不读取 evals。

### Step 5. 四 Adapter

- [ ] 在 canonical adapter root 实现 shared/Codex/Claude/Cursor descriptor/wrapper 和统一 request/response protocol。
- [ ] Adapter 只组装 native context/argv、加载 exact Skill、传 prompt/files、收集 public output/trace/timing。
- [ ] Native CLI/能力缺失统一返回 `unsupported`；不得修改 corpus 或降低 assertion。
- [ ] 用 injected fake executables 覆盖四 adapter 的 success、behavior failure、execution error、unsupported 与 corpus byte mismatch。
- [ ] 静态测试拒绝 adapter 内复制 schema、grader policy、semantic judgment 或 platform-specific corpus。

### Step 6. Extension、preset 与平台分发

- [ ] 更新 `trellis/guru-team-extension.json` 的 companion commands、eval schemas/adapters/inventory 和版本/release notes。
- [ ] 更新 preset managed assets、executable modes、installed manifest 与 source/installed validators。
- [ ] 将含 eval corpus 的 representative packages/测试资产限制在 test-only fixture；生产 registry 保持九个 legacy Skill ids。
- [ ] 验证 shared、Codex、Claude、Cursor selected-platform package copies 的 `evals/evals.json` 与 files byte-identical。
- [ ] 运行 preset apply 同步 dogfood；逐项处理任何 `.new`/`.bak` 并运行 overlay drift。

### Step 7. Durable docs 与 public instructions

- [ ] 更新 `docs/requirements/README.md`、`requirement-main.md`、`guru-team-trellis-flow.md`。
- [ ] 更新根 README、workflow README、preset README 的可执行 discovery/run、adapter/status/evidence 示例和 #145/#146 timeline。
- [ ] 更新 public docs spec，确认命令、schema id、inventory 与实际 help 一致。
- [ ] 完成 Docs SSOT reconciliation，记录 task delta 已合并与 task-history-only 内容。

### Step 8. 全量验证与 Phase 2 handoff

- [ ] 执行 focused schema/runtime/fixture/adapter/negative tests。
- [ ] 执行 package contract tests、shared runtime tests、preset installer tests、ownership tests。
- [ ] 执行 source/installed package validation和 eval discovery/run smoke。
- [ ] 执行 preset apply、dogfood drift、selected-platform byte/mode validation。
- [ ] 执行 clean throwaway init/workflow preview-switch/preset install/commands，然后 `trellis update` + preset reapply + 同样验证。
- [ ] 递归扫描 throwaway 与 dogfood 无 `.new`/`.bak`，运行 `git diff --check` 与 task validation。
- [ ] Implementation handoff 列出文件、R/AC 承接、验证、Docs SSOT 执行结果、风险和 `trellis-check` 关注点。

## 3. 预计修改面

### Canonical source

- `trellis/skills/guru-team/schemas/`：eval/grading/adapter/evidence schemas。
- `trellis/skills/guru-team/tests/fixtures/representative-active/`：semantic/deterministic corpora、files、adapter fixtures。
- `trellis/skills/guru-team/tests/test_skill_packages.py`：schema、migration、negative、byte identity tests。
- `trellis/skills/guru-team/adapters/eval/`：四个薄 adapter descriptors/wrappers。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`：deterministic discovery/run/grader aggregation。
- `trellis/workflows/guru-team/scripts/bash/`：两个 public wrappers。
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：runtime behavior/error tests。
- `trellis/guru-team-extension.json`：public API/inventory/version。

### Distribution/dogfood

- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 与 tests。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`。
- `.trellis/guru-team/`、selected platform package copies 和必要 overlay source。

### Durable docs

- `design.md` Docs SSOT Plan 13.3 列出的 workflow/preset/docs specs、requirements docs 与三份 public README。

## 4. Validation commands

路径和 test selectors 在实现后按实际文件名精确化；以下命令集合全部必跑，任一命令子集通过均不能替代完整门禁。

```bash
python3 -m json.tool trellis/skills/guru-team/schemas/skill-evals.schema.json
python3 -m unittest trellis/skills/guru-team/tests/test_skill_packages.py
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
python3 -m py_compile \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --json
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 ./.trellis/scripts/task.py validate 07-21-147-skill-eval-runner-adapters
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task 07-21-147-skill-eval-runner-adapters
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
git diff --check
```

额外 smoke 必须覆盖：

```bash
trellis/workflows/guru-team/scripts/bash/discover-skill-evals.sh --help
trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh --help
# source/installed representative discovery + run
# shared/codex/claude/cursor adapter with injected executables
# normal public invocation trace proving evals are not loaded
# clean throwaway before and after trellis update + preset reapply
```

## 5. Review gates

- Schema/API gate：所有新增 id、field、command、status、error code 与 consumer 都有直接使用者和 test。
- AI/script boundary gate：Python/shell 不生成 semantic pass、scope、finding、route 或 product judgment。
- Invocation gate：每个 behavior case 真实执行 public wrapper，并按 actual exit 选择独立 output schema。
- Adapter gate：四 adapter 消费相同 corpus bytes，平台能力缺失只能 `unsupported`。
- Evidence gate：所有 run output 在 repo/package 外，且不是 handoff/gate/checkpoint/audit/release proof。
- Compatibility gate：Interface 1.2、九个 legacy production Skills、Interface 1.3 public I/O 与 normal invocation 不回归。
- Distribution gate：canonical/installed/dogfood/shared/Codex/Claude/Cursor byte/mode 一致。
- Upgrade gate：fresh install、update、reapply 后同样通过且零 sidecar。
- Docs gate：Docs SSOT Plan 已执行，不留 current-scope durable docs inconsistency。

## 6. Rollback points

- Step 1-2 未发布阶段：可移除独立 eval schema/fixture，不触碰 #144 Interface 1.3。
- Step 3-5 runtime 失败：撤回新增 public command/adapter inventory，不改变 production Skill behavior。
- Step 6 分发失败：停止在 canonical branch，修复 installer/provenance/sidecar 后重新完整 apply；不得手工把 dogfood 当 source。
- Adapter compatibility 问题：保留 `unsupported`，不得创建平台专用 corpus 或跳过断言。
- 任何发现改变 R1-R12、public ids、comparison/status/semantic 边界的情况：暂停实现，更新 planning artifacts 并重新执行 `guru-approve-task-plan`。

## 7. Docs SSOT checkpoint

- Strategy：`ssot_first`。
- 实现前：更新 design 13.3 的 durable contracts，使 schema/command/adapter/evidence 语义先成为 SSOT。
- 实现中：task artifact 只保留 delta、取舍与证据，不成为平行长期规范。
- Phase 2 check 前：逐项核对代码/schema/help/manifest/installer/tests 与 durable docs 一致。
- Commit 前：记录实际 docs 文件、已合并 task delta、task-history-only 内容和无 sidecar 证据。
