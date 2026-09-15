# #414 实现计划：semantic retrieval ownership 收敛

## 1. 实现前门禁

- [ ] 重读 live Issue #414/comments `5678843409`、`5679841798`、task 三份规划
  文件和当前 `origin/main` identity。
- [ ] 完成 planning wording review、Architecture task-impact sync 和
  `guru-approve-task-plan` semantic review。
- [ ] 在单独的 plan presentation 后取得 task activation 确认，再运行标准
  task start；本文件不代表 activation authority。
- [ ] 通过 `trellis-before-dev` 加载当前 task 与 `implement.jsonl` 中四份已列明
  spec；inline Phase 2 不伪造额外 context entries。

## 2. 有序实现步骤

### Step 1. Canonical owner wording

- [ ] 只编辑
  `trellis/presets/guru-team/spec/workflow/semantic-retrieval.md`。
- [ ] 将 owner 列表收敛为四个 Guru owners。
- [ ] 增加 Guru caller 消费 upstream worker/provider evidence 时的
  concept-family、coverage 与 sufficiency 责任。
- [ ] 保持现有 concept taxonomy、negative conclusion、AI/script 和 artifact
  边界不变，不新增 adapter、API、schema 或 owner。

Checkpoint：检查 diff 只表达 current authority replacement，没有恢复或改写
官方 `trellis-*` 文件。

### Step 2. Ownership-aware focused test

- [ ] 编辑
  `trellis/skills/guru-team/tests/test_semantic_retrieval_contract.py`。
- [ ] 保留四个 Guru owners 的 reference/eval/fixture 断言和现有 non-owner
  negative assertions。
- [ ] 以 upstream exclusion/managed-boundary assertion 替换 13-path positive
  assertion；不通过删除整个 test case 降低覆盖。
- [ ] 先运行 focused test，确认原 13 failures 消失且四项 test 全部通过。

### Step 3. Reconcile bounded-owner guidance

- [ ] 只编辑 `guru-reconcile-task-base` canonical `SKILL.md` 与
  `references/contract.md`，移除直接 semantic-retrieval SSOT consumption 与第五
  retrieval-owner 声明。
- [ ] 保留 exact caller input、old/new base pair、live authority/planning locators、
  candidate delta/validation facts 与 `base_impact_candidate_set` 的既有 bounded
  judgment；不改 interface、schema、runtime、typed exit 或 workflow route。
- [ ] 将 `guru-reconcile-task-base` 加入 focused test 的 non-owner assertion，并
  运行其 package contract/runtime tests，证明行为合同未发生非授权变化。
- [ ] 编辑 canonical
  `trellis/presets/guru-team/spec/workflow/skill-package-contract.md` 的现有
  `Task Base Reconciliation Owner` 段落，移除 reconcile 对 broad semantic
  retrieval SSOT 的 direct-consumer 要求；不改其它 package contract。
- [ ] 在 focused test 中增加 shared canonical contract 的最小 non-owner 回归
  断言，证明该声明不会再次产生第五个 retrieval owner。

### Step 4. Preset projection

- [ ] 运行
  `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms` 同步
  dogfood spec。
- [ ] 核对 apply 只更新预期 managed projection；逐项处理任何 `.new`/`.bak`。
- [ ] 验证 canonical 与 `.trellis/spec/workflow/semantic-retrieval.md` bytes 一致。
- [ ] 验证 canonical 与 `.trellis/spec/workflow/skill-package-contract.md` 对应
  managed projection bytes 一致。
- [ ] 运行 dogfood overlay drift 和 upstream ownership checks。

### Step 5. Source/installed 与 focused throwaway 验证

- [ ] 运行 semantic retrieval focused source test。
- [ ] 运行 source/installed `check-skill-packages.sh`、preset apply tests 与
  upstream ownership validator。
- [ ] 运行一个 clean standalone throwaway 的 fresh install、official update、
  preset reapply 和 current semantic owner contract 检查。
- [ ] 验证 fresh 与 reapply 后均无 upstream Guru patch、无 unresolved sidecar、
  无临时 cache/runtime residue。
- [ ] 保持该验证为 Issue #414 focused representative throwaway，不声明已完成
  #410 release matrix 或 tag-pinned proof。

### Step 6. Phase 2 与交付门禁

- [ ] 执行 secret scan、residue hygiene、`git diff --check`、task validation、
  workspace boundary 和完整 scoped diff review。
- [ ] 运行 `guru-check-task`，确认 AC1-AC8、Docs SSOT execution 和未验证边界。
- [ ] 取得单独 commit 确认后，由 `guru-create-task-commit` 精确 stage 本任务路径。
- [ ] 完整 Branch Review 覆盖 `origin/main...HEAD`，不得复用旧 review 结论。
- [ ] Publication/Finalizer 仅准备 #414 PR，正文使用 `Closes #414` 与
  `Refs #410`，明确不创建 tag/Release、不关闭 #410。
- [ ] push、PR、merge 分别展示 exact refs/HEAD/commands/scope，并在每一步
  取得确认后执行。
- [ ] merge 后回到 #410，从新的 `origin/main` 开始全新 exact candidate；旧
  candidate 和本轮 pre-merge release evidence 全部作废。

## 3. 预计修改文件

### Canonical 与 test

- `trellis/presets/guru-team/spec/workflow/semantic-retrieval.md`
- `trellis/presets/guru-team/spec/workflow/skill-package-contract.md`
- `trellis/skills/guru-team/tests/test_semantic_retrieval_contract.py`
- `trellis/skills/guru-team/packages/guru-reconcile-task-base/SKILL.md`
- `trellis/skills/guru-team/packages/guru-reconcile-task-base/references/contract.md`

### Preset-managed projection

- `.trellis/spec/workflow/semantic-retrieval.md`
- `.trellis/spec/workflow/skill-package-contract.md`

除上述五个 canonical implementation/test 文件及 installer 产生的 managed
projection 外，不得扩大到其它 workflow、Skill、agent、README、schema 或
Architecture/RDT 文件。

## 4. Validation commands

实现前复核实际 wrapper help；以下为当前已发现的最小必跑集合：

```bash
PYTHONDONTWRITEBYTECODE=1 \
./trellis/skills/guru-team/runtime/resolve-python.sh \
  "$PWD" "$PWD/trellis/skills/guru-team/runtime" \
  trellis/skills/guru-team/tests/test_semantic_retrieval_contract.py

trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh \
  --json --mode source

trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms

.trellis/guru-team/scripts/bash/check-skill-packages.sh \
  --json --mode installed

trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --json

PYTHONDONTWRITEBYTECODE=1 \
./trellis/skills/guru-team/runtime/resolve-python.sh \
  "$PWD" "$PWD/trellis/skills/guru-team/runtime" \
  -m unittest discover -s \
  trellis/skills/guru-team/packages/guru-reconcile-task-base/tests

trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

python3 ./.trellis/scripts/task.py validate \
  09-15-414-semantic-retrieval-projection

.trellis/guru-team/scripts/bash/check-workspace-boundary.sh \
  --json --task 09-15-414-semantic-retrieval-projection

git diff --check
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
```

Secret scan 使用仓库当前受支持的 scanner/命令并限定于本任务 diff；若没有统一
wrapper，则以精确 staged/branch diff 做 credential pattern scan，并在 Phase 2
证据中记录命令和结果。Throwaway 命令在运行前必须使用独立临时根，并在完成后
验证目标已清理且仓库状态只包含本任务文件。

## 5. Review gates

- Ownership gate：四个 Guru owners 保持完整，所有 upstream roles 不被 Guru claim。
- Scope gate：实现 diff 限于五个 canonical implementation/test 文件、必要
  managed projection 和 task artifacts。
- Distribution gate：canonical、dogfood、installed、throwaway current contract 一致。
- Upgrade gate：official update + preset reapply 后 contract 仍成立且零 sidecar。
- Semantic boundary gate：脚本/test 不产生 concept family 或 sufficiency judgment。
- Release gate：#414 交付不冒充 #410 release proof，#410 保持 OPEN。

## 6. 回退与重新规划条件

- Focused test、apply、installed 或 throwaway 出现超出五个 canonical 文件及
  必要 managed projection 的修改时，先判断是否为 current-scope direct
  consumer；不能证明则不修改。
- 发现必须新增 public contract、改变 upstream file bytes、修改 #408 行为或
  Architecture/RDT authority 时，停止 Phase 2 并返回 fresh clarification/planning。
- 任何验证失败只针对根因作最小修复；不得弱化 test、绕过 installer、手工覆盖
  managed projection 或扩大为 release-wide patch。
