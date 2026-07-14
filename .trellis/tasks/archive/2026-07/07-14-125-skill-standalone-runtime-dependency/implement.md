# #125 实施计划：Skill standalone runtime dependency

## 1. 执行前提

- [ ] 用户完成 post-planning review 并明确批准 `prd.md`、`design.md`、`implement.md`。
- [ ] Main session 写入 schema 1.2 `planning-approval.json`，ambiguity review 通过，fixed scan scope 完整，`unchecked_normative_hits[]` 为空。
- [ ] `check-planning-approval.sh --json` 通过。
- [ ] `task.py start` 把 task 切换到 `in_progress`。
- [ ] 实现 sub-agent 在编辑前重新执行 workspace boundary 与 planning approval 校验。

## 2. 实施顺序

### Phase A. Durable SSOT first

- [ ] 更新 `.trellis/spec/workflow/skill-package-contract.md`，定义 routing independence、runtime dependency 与 non-portable package。
- [ ] 更新 `.trellis/spec/workflow/companion-scripts.md`，定义 shared dispatcher 的输入、客观校验与 fail-closed 边界。
- [ ] 更新 `.trellis/spec/preset/installer.md`，定义 runtime dispatcher managed asset、extension capability 与 upgrade 验证。
- [ ] 更新 `.trellis/spec/docs/public-docs.md`，要求三份 README 同步 standalone/runtime 语义。
- [ ] 更新 `docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md` 与 requirements index 追踪 #125。

### Phase B. Interface 与 source validation

- [ ] 升级 interface schema identity/version，并增加 mode routing、runtime dependency、validator runtime command 的闭集字段。
- [ ] 更新 production interface 与 representative fixture。
- [ ] 更新 source validator，校验 routing、dependency、API、dispatcher、distribution、portability、runtime command 与 mode parity。
- [ ] 更新 extension public API schema facts与版本号。

### Phase C. Shared runtime dispatcher

- [ ] 新增 canonical `run-skill-command.sh` thin wrapper 与 Python subcommand。
- [ ] 实现 repo/package/manifest/interface/installed inventory/runtime API/runtime command 的确定性校验。
- [ ] 只把固定 validator id 映射到 interface 声明的 shared companion command。
- [ ] 更新 `guru-create-task-commit` 两个 package wrapper，移除旧 runtime command 直连 fallback。
- [ ] 缺失或不兼容 runtime 时输出固定 preset install/upgrade remediation，并在业务副作用前退出。

### Phase D. Installer 与 generated copies

- [ ] 把 dispatcher 加入 `MANAGED_ASSET_PATHS`、executable handling、extension manifest companion scripts 与 preset README installed-file list。
- [ ] 更新 installer/unit/throwaway 的 managed asset count、manifest assertions 与 package inventory assertions。
- [ ] 运行 canonical preset apply，同步 `.trellis/guru-team/skills/`、shared root 与 Codex/Cursor/Claude roots。
- [ ] 检查并处理每个 `.new` / `.bak`。
- [ ] 运行 dogfood overlay drift 与 skill package installed drift 校验。

### Phase E. Public docs

- [ ] 更新 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- [ ] 更新 canonical workflow 与 dogfood workflow 中 global routing/standalone 边界，只保留调用与 route 语义，不复制 step-local 实现。
- [ ] 确认 selected platform copies 只来自 canonical package distribution。

### Phase F. Test matrix

- [ ] Package tests 覆盖 mode 语义、dependency metadata、non-portable contract、wrapper thin boundary。
- [ ] Source tests 覆盖 schema/semantic negative matrix。
- [ ] Runtime tests 覆盖 missing manifest、missing dispatcher、API mismatch、dependency mismatch、runtime command mismatch、managed drift。
- [ ] Standalone package-only fixture 验证 clear remediation 与 zero business side effect。
- [ ] Full preset throwaway 验证初次安装与 update/reapply 后的 standalone entry。
- [ ] 保留 existing task commit smoke，证明 shared parser 与 exact Git transaction 行为未回归。

## 3. 验证命令

### Targeted

```bash
python3 trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py
python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
```

### Static 与 contract

```bash
python3 -m json.tool trellis/skills/guru-team/schemas/skill-interface.schema.json
python3 -m json.tool trellis/skills/guru-team/packages/guru-create-task-commit/interface.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-14-125-skill-standalone-runtime-dependency
git diff --check
```

### Installer、dogfood 与 clean throwaway

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
```

### Official workflow 与 upgrade evidence

```bash
trellis --version
trellis workflow --marketplace gh:castbox/guru-trellis/trellis --template guru-team --create-new
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.4
```

远端 exact feature-ref marketplace validation 必须在 reviewed content push 后由 finish-work gate 执行；Phase 2 只运行本地 clean throwaway 与 canonical/installed 验证。

## 4. Phase 2 handoff 要求

实现 sub-agent 必须报告：

- changed files 与 canonical/generated 分类；
- requirement/design carryover；
- Docs SSOT strategy 执行结果；
- durable docs sync、task delta merge 与 task-history-only 内容；
- test/validation 结果；
- `.new` / `.bak` 状态；
- deployment/security 判断；
- stacked PR base limitation；
- remaining risks 与 check focus。

Check sub-agent 必须独立覆盖 requirements、design、source、schema、runtime、installer、platform copies、docs、tests、upgrade、security、deployment 与 Docs SSOT reconciliation。Main session 只能在完整 check report 完成后记录 `phase2-check.json`。

## 5. Commit 与 review gate

- [ ] Fresh Phase 2 pass 后 mandatory invoke `guru-create-task-commit`。
- [ ] Commit diff 只能包含 #125 task-reviewed paths；#122 base commits 不得重复计入 #125 diff。
- [ ] Work commit 使用 issue-bearing Chinese Conventional Commit，并只写 `Refs #125`。
- [ ] 独立 Branch Review sub-agent 审查 `origin/feat/122-guru-create-task-commit...HEAD` 全量 diff。
- [ ] 任意 P0/P1/P2/P3 finding 都必须修复并经过 fresh Phase 2、fresh commit 与 finding closure。
- [ ] Fresh final reviewer 必须为未参与前序 finding/closure 的新 technical agent id。
- [ ] `trellis-continue` 在 Branch Review Gate 后停止，不 push、不创建 PR、不 archive。

## 6. Rollback points

- Schema/source validation 失败：回到 Phase B，禁止同步 installed copies。
- Dispatcher/runtime tests 失败：回到 Phase C，禁止运行 preset apply。
- Installer 产生未决 sidecar：停止并逐个处理，禁止声称安装成功。
- Throwaway/update/reapply 失败：停止，记录未验证项，禁止通过 Phase 2。
- Durable docs 与 implementation 不一致：视为 current-scope blocker，禁止降级成 observation。
