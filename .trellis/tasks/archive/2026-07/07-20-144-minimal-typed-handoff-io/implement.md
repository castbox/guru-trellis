# #144 实施计划：最小 typed handoff I/O 基础设施

## 1. 实现前门禁

- [ ] `guru-approve-task-plan` 对 current `prd.md`、`design.md`、`implement.md` 返回
  checker-passed `approved`。
- [ ] Task workspace boundary 指向
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/144-minimal-typed-handoff-io`。
- [ ] Branch 为 `codex/144-minimal-typed-handoff-io`，base 为 `main`。
- [ ] Implementation/check agents 只在 task worktree 工作，不修改 main checkout。
- [ ] 按 `trellis-before-dev` 加载其输出的 `.trellis/spec/` 文件清单。
- [ ] Docs SSOT Plan 固定为 `design.md` 第 12 节，策略 `ssot_first`。

## 2. 实施顺序

### Step 1. Durable SSOT

- [ ] 更新 `.trellis/spec/workflow/skill-package-contract.md`，写入 1.2/1.3 version、
  registry migration、public invocation/discovery、consumer/projection 和 private artifact
  精确合同。
- [ ] 更新 `.trellis/spec/workflow/data-contracts.md`、`companion-scripts.md`、
  `quality-guidelines.md`、`index.md`。
- [ ] 更新 `docs/requirements/requirement-main.md`、
  `docs/requirements/guru-team-trellis-flow.md`、`docs/requirements/README.md`。

Checkpoint：durable docs 与 `design.md` P1-P15 一致后才修改 schema/runtime。

### Step 2. Versioned schemas

- [ ] 保持 `trellis/skills/guru-team/schemas/skill-interface.schema.json` 的 1.2 identity
  与 semantics 不变。
- [ ] 新增 `skill-interface-1.3.schema.json`，实现 closed `public_contracts`。
- [ ] 升级 `skill-registry.schema.json` 为 1.1，active entry 必填
  `interface_schema_id`、`io_contract_state`。
- [ ] 补充 schema tests：unknown fields、wrong version/state、structured/scalar union、
  output/consumer/private declarations。

Checkpoint：1.2 legacy fixture 与纯 schema 1.3 examples 同时通过。

### Step 3. Representative mixed fixture

- [ ] 将现有 fixture 拆为 `guru-example-legacy`、`guru-example-action`、
  `guru-example-sync`。
- [ ] 为 semantic initial/reentry profiles、四个 exits、三类 consumer、direct/select/
  rename/normalize projection 创建独立 schemas/examples。
- [ ] 将 workflow/stop consumer schemas 放在 fixture consumer-owned roots；producer
  interface 只记录 locator，Skill consumer 绑定目标 package input。
- [ ] 为 deterministic scalar CLI 创建 exact wrapper/help/example，不创建 input JSON
  schema。
- [ ] 添加 private checkpoint/gate evidence schemas 与 stdout-only/task-local persistence。
- [ ] 添加 stable invocation error schema/example。
- [ ] 确保 fixture extension/registry/workflow 自洽且不进入 production inventory。

Checkpoint：fixture wrappers 实际执行两个 structurally distinct exits，stdout 通过
per-exit schema。

### Step 4. Runtime validator 与 discovery

- [ ] 在 `guru_team_trellis.py` 增加 interface version table 与 registry 1.1 relation
  validation。
- [ ] 增加 1.3 package-local path、schema id/dialect、example、exit/consumer/projection、
  direct-use 和 public/private互斥验证。
- [ ] 增加 declarative projection validator/executor，operation 只含 design 第 4.5 节闭集。
- [ ] 增加 representative public invocation execution probe 与 stable errors。
- [ ] 增加 `discover-skill-contract` parser/handler，输出 closed legacy/minimal variants。
- [ ] 新增 thin executable wrapper
  `trellis/workflows/guru-team/scripts/bash/discover-skill-contract.sh`。
- [ ] 保持 `run-skill-command` 和九个 legacy command paths 不变。

Checkpoint：所有 negative fixtures 返回预期稳定 code，且没有 semantic judgment 进入
runtime。

### Step 5. Production registry 与 extension API

- [ ] 为九个 active registry entries 添加 1.2 + `legacy`。
- [ ] Extension 添加 supported/current/scalar migration fields、legacy allowlist 与三个
  production schema inventory 空数组。
- [ ] `companion_scripts` 添加 `discover-skill-contract`。
- [ ] 更新 runtime manifest validation、ownership validation 与 facts output。
- [ ] 断言 production registry/manifest 不包含 test fixture ids 或 schemas。

Checkpoint：source validator准确报告九个 legacy、零 minimal production package，mixed
fixture validator同时报告1.2/1.3。

### Step 6. Installer 与 public docs

- [ ] Preset installer managed assets 增加 1.3 schema 与 discovery wrapper，保持 executable
  mode。
- [ ] 更新 installer tests、throwaway inventory counts 与 installed manifest assertions。
- [ ] 更新 `README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`，给出 exact discovery 命令、migration timeline 和
  verification commands。
- [ ] 不修改 upstream-owned overlay payload；ownership inventory变化只包含 Guru-owned
  assets。

### Step 7. Dogfood 同步

- [ ] 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`。
- [ ] 检查并处理所有 `.new` / `.bak`；不得静默覆盖未知修改。
- [ ] 确认 `.trellis/guru-team/skills/`、`.agents/skills/`、`.codex/skills/`、
  `.cursor/skills/`、`.claude/skills/` 与 canonical active packages一致。
- [ ] 运行 dogfood overlay drift 与 source/installed validators。

### Step 8. 全量验证与收敛

- [ ] 运行 unit/contract/installer tests。
- [ ] 运行 source、installed、selected-platform 和 ownership checks。
- [ ] 运行 clean throwaway install、workflow preview/switch、update、preset reapply。
- [ ] 复验 discovery legacy/minimal outputs、代表性 invocation 和 final zero sidecars。
- [ ] 使用 `guru-check-task` 对 R1-R12、AC1-AC15 与 Docs SSOT Plan 做完整 semantic
  check，并修复 findings 后全量重跑。

## 3. 计划修改面

### Canonical contracts and runtime

- `.trellis/spec/workflow/*.md` 中第 1 步列出的 durable files。
- `docs/requirements/*.md` 中第 1 步列出的 requirements files。
- `trellis/skills/guru-team/schemas/*.json`。
- `trellis/skills/guru-team/registry.json`。
- `trellis/skills/guru-team/tests/**` 与 test-only fixtures。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- `trellis/workflows/guru-team/scripts/bash/discover-skill-contract.sh`。
- `trellis/guru-team-extension.json`。

### Distribution and docs

- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 及其 tests。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`。
- `README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`。
- Preset apply 生成的 `.trellis/guru-team/**` 与 active selected-platform copies。

工作流 phase/route 与九个 production package business payload 不在计划修改面；
schema/manifest 适配产生的机械 installed copy变化是唯一进入 diff 的 package变化。

## 4. 验证命令

### Focused contracts

```bash
python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
```

### Source、installed 与 dogfood

```bash
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode installed
.trellis/guru-team/scripts/bash/discover-skill-contract.sh --root . --mode installed --skill guru-sync-base --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
```

### Full install/update

```bash
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

Throwaway 输出必须证明首轮与 update/reapply 后：新 wrapper可执行、legacy discovery
正确、source/installed validation通过、mixed fixture invocation通过、selected platform
copies完整、无 unresolved `.new/.bak`。

## 5. Phase 2 semantic check

`guru-check-task` 必须逐项确认：

- 1.2 bytes/identity 与九个 production typed exits/runtime behavior 未被 reinterpret；
- production registry 与 extension inventories真实，不包含 fixture；
- 1.3 schemas/examples/invocation/consumer/projection/private classification完整；
- 每个 output field均有 direct consumer use；
- public invocation实际执行，不是静态 fixture-only assertion；
- projection与调用方无需读取/import runtime source；
- docs、code、tests、installed copies、README命令与 throwaway evidence一致；
- #145/#146 migration、unusual hardening 和其它 related issues 未进入实现。

## 6. Rollback points

| Point | Trigger | Action |
| --- | --- | --- |
| RP1 | 1.3 schema无法表达closed contracts | 回退未提交1.3 delta，修订design后重新planning approval；不改1.2 |
| RP2 | Runtime影响legacy behavior | 回退version dispatch delta，先补legacy regression fixture再实现 |
| RP3 | Installer产生未知覆盖或sidecar | 停止同步，保留用户文件，修复canonical/provenance后重新apply |
| RP4 | Throwaway update/reapply失败 | 阻止commit/publish，修复并完整重跑，不跳过门禁 |
| RP5 | 实现发现scope或authority变化 | 停止实现，更新三份planning文档并重新执行clarification/wording/approval |

## 7. 完成清单

- [ ] P1-P15 均有代码、测试或文档证据。
- [ ] AC1-AC15 全部通过。
- [ ] `guru-check-task` checker-passed，零未解决 finding。
- [ ] Docs SSOT merge checkpoint 完成。
- [ ] Branch Review 覆盖 `origin/main...HEAD`。
- [ ] PR readiness 只使用 `Closes #144`，#145/#146 保持 follow-up。
