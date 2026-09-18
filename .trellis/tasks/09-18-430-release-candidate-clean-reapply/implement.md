# #430 实施计划

## 1. Durable contract

1. 在 installer spec 定义 complete-manifest no-op 比较与 provenance retention。
2. 在 canonical/dogfood data contracts 与 preset README 同步该行为。
3. 明确 raw apply 入口及其子进程不得写 Python bytecode。

## 2. Installer implementation

1. 为 installed manifest 增加局部 helper：只在完整 manifest 除 `installed_at`/`source` 外与
   previous 完全一致时复用 previous payload。
2. `install_assets()` 写 manifest 前调用该 helper；fresh install 和 changed install 保持现状。
3. `apply.sh` 导出 `PYTHONDONTWRITEBYTECODE=1` 后再启动 Python。

## 3. Regression tests

1. 覆盖 cross-HEAD byte-equivalent reapply 的 manifest byte identity。
2. 覆盖 managed content change 后 timestamp/source refresh。
3. 覆盖 raw entrypoint clean Git fixture 的 status、diff 和 recursive residue。

## 4. Projection synchronization

运行 canonical preset apply 同步 dogfood installed files，审查全部 diff；不得产生 `.new`、
`.bak` 或 bytecode。确认 Shared/Codex/Claude/Cursor 与 release Skill projection byte parity。

## 5. Validation

```bash
PYTHONDONTWRITEBYTECODE=1 python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
PYTHONDONTWRITEBYTECODE=1 python3 trellis/presets/guru-team/scripts/python/test_preset_transaction_installer.py
PYTHONDONTWRITEBYTECODE=1 python3 .agents/skills/release-guru-trellis-version/tests/test_contract.py
./trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
./trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
./.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json
python3 .trellis/scripts/task.py validate 430-release-candidate-clean-reapply
git diff --check
find . \( -type d -name '__pycache__' -o -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.new' -o -name '*.bak' \) \) -print
```

任何失败、SKIP、unexpected mutation 或 residue 都阻断 commit/PR。修复合并后，#410 从新
`origin/main` 创建全新 detached candidate 并从零执行完整 Stage 2。
