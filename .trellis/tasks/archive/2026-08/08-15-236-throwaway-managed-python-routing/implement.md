# Issue #236 实施计划

## 1. 固化 durable 合同

- [x] 在 preset installer spec 中定义 verifier seed/source/installed runner 边界。
- [x] 在 companion scripts spec 中定义 caller inventory、checkpoint 与 fail-closed 路由。
- [x] 在 quality guidelines 中加入双环境与 Branch Review 五项负向保证。
- [x] 更新 preset README，保持原始命令不变并说明 verifier 自动解析 managed runtime。
- [x] 通过 preset apply 同步 dogfood specs，检查无 `.new` / `.bak`。

## 2. 建立 runner 与 checkpoint

- [x] 在 verifier 中保留唯一 bootstrap seed。
- [x] 新增 `source_python` 与 `installed_python` shell runner，替换全部 bootstrap 后裸 `python3`。
- [x] 新增 source-owned `verify_throwaway_python_routing.py checkpoint`，分别验证 managed launch path、physical interpreter、runtime 与 lock identity。
- [x] 在 source-bootstrap、initial、after-update、两次 change-request smoke 与 no-developer shell checkpoint 接入精确断言。

## 3. 完整 caller inventory

- [x] 新增 `throwaway-python-callers.json`，登记 verifier、内联 Python、直接 helper、wrapper 第二跳、Python subprocess 与生成 shebang。
- [x] 实现 `check-inventory` 双向静态检查，强制唯一 `bootstrap_seed` 与 source/installed 分类。
- [x] 将 verifier 实际执行的 package/platform wrapper 绑定到 canonical wrapper、`commands.json` command id 与 installed `runtime/launch.sh -> resolve-python.sh` 第二跳。
- [x] 在 verifier 业务矩阵前后运行 inventory gate。
- [x] 增加 inventory 正负单元测试，证明新增裸调用、PATH shebang、未登记第二跳都会失败。

## 4. 修复 helper 第二跳与身份输出

- [x] 将三个 source helper 改为由 installed runner 启动。
- [x] 将生成的 `/usr/bin/env python3` fixture 改为绑定 managed `sys.executable`。
- [x] 将 helper 的 Python subprocess 统一为 `sys.executable`。
- [x] 为 linked-worktree、closeout initial/after-update 返回内部 runtime checkpoint，并由 verifier 断言。

## 5. 双环境与完整矩阵

- [x] 增加 PATH Python 有依赖的 poison/sentinel fixture。
- [x] 运行 PATH Python 无 `jsonschema` 的 README 原始命令全矩阵。
- [x] 运行 PATH Python 有 `jsonschema` 的 poisoned README 原始命令全矩阵。
- [x] 两次均核对 initial/update/reapply/linked-worktree/closeout/no-developer executable、runtime identity、lock identity。

## 6. Targeted validation

```bash
bash -n trellis/presets/guru-team/scripts/bash/*.sh
SOURCE_MANAGED_RUNNER ... verify_throwaway_python_routing.py check-inventory ...
SOURCE_MANAGED_RUNNER ... test_verify_throwaway_python_routing.py -q
SOURCE_MANAGED_RUNNER ... test_apply_guru_team_trellis_preset.py -q
SOURCE_MANAGED_RUNNER ... trellis/skills/guru-team/runtime/tests/test_runtime.py -q
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

## 7. Full acceptance

```bash
./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
PATH=<jsonschema-path-python-poison-fixture>:$PATH \
  ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

两条命令都直接执行 README 原始脚本。不得仅以 outer wrapper、局部 smoke 或单个 exit 0 替代身份证据。

## 8. 收口

- [x] 运行 `guru-check-task`，完整检查需求、设计、实现、测试与 Docs SSOT。
- [ ] 在 commit 前展示精确 staged files/命令并取得用户确认。
- [ ] commit 后执行独立 `guru-review-branch`，覆盖 `origin/main...HEAD` 全 diff 与五项负向保证。
- [ ] publication/finalization 前分别展示 push/PR 与 merge 副作用并取得用户确认。
- [ ] PR body 仅使用 `Closes #236`，明确不包含 #127/#220/tag/Release/业务仓升级。

## 风险与停止条件

- 完整 verifier 运行时间长；任何失败先保留首个失败 checkpoint 和解释器身份，再修复并全量重跑。
- 若 caller inventory 不能覆盖某个动态 Python 第二跳，停止并扩充静态模型，不以白名单跳过。
- 若 installed resolver 无法为 linked-worktree/closeout 提供精确身份，停止并修复既有调用路径，不回退 source runner。
- 若 preset apply 产生 `.new` / `.bak`，逐个审阅后处理，不静默覆盖。
