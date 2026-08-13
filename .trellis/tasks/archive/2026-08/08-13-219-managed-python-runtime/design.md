# #219 技术设计

## 架构边界

实现分为 bootstrap 控制面与 command 执行面：

1. `apply.sh` 使用 PATH Python 只启动 preset installer。installer 读取 canonical lock，选择兼容 Python，计算 runtime identity，在 target runtime root 构建候选 venv。
2. 候选 venv 以 hash-locked 模式安装依赖，并运行版本、import 与 Draft 2020-12 能力探针。
3. 验证成功后写入受管 runtime metadata，再替换一个小型 active identity pointer；失败不触碰原 active pointer 或旧 runtime。本任务不扩展跨 OS 原子性或 crash consistency 合同。
4. 所有 Guru-owned Python wrapper 通过共享 shell resolver 读取 active pointer、验证 identity/解释器/能力，然后 `exec` 受管 Python。
5. resolver 只做客观路径、identity 和 import/capability 判定，不参与 Skill routing 或语义判断。

## Canonical 布局

实现使用以下 canonical managed asset 角色；最终文件名必须由当前 installer inventory 统一声明：

```text
trellis/skills/guru-team/runtime/
  python-runtime.json
  requirements.lock
  resolve-python.sh
  bootstrap.py
  probe.py
```

安装到：

```text
.trellis/guru-team/runtime/              # tracked/managed runtime code and lock
.trellis/.runtime/guru-team/python/
  active.json                            # ignored active identity pointer
  <runtime-id>/
    metadata.json                        # ignored managed provenance
    venv/bin/python                      # ignored managed interpreter
```

canonical 与 installed 的相对合同必须一致，不保留并行 resolver 或 lock 路径。

## Runtime Identity

identity 输入为闭合对象：

- extension/runtime API version；
- lock 文件 SHA-256；
- Python implementation；
- Python major/minor；
- venv layout version。

`runtime-id` 是该对象的稳定 digest 前缀，仅用于版本绑定和 stale 检测，不是安全认证边界。metadata 保存完整 identity、lock digest、解释器相对路径和已验证 dependency versions，不保存本机绝对路径、凭据或授权。

## Bootstrap 与切换

- installer 在任何 target managed asset 激活前执行 Python capability preflight。
- 若 active metadata 与目标 identity 完全一致且 probe 通过，直接复用。
- 否则创建全新的 `<runtime-id>` 候选；目标目录已存在但无有效 managed metadata 时 fail closed，不覆盖未知内容。
- 使用 `python -m venv` 创建隔离环境，确认 pip 可用，以 `--require-hashes --no-input --disable-pip-version-check` 安装 lock。
- 清除 `PIP_INDEX_URL`、`PIP_EXTRA_INDEX_URL`、`PIP_CONFIG_FILE` 和 active venv 影响，不注入 credentials；公开 index URL 与安装命令在 manifest/README 中明确。
- probe 验证锁定版本并执行包含 `$ref`、`oneOf`、`if/then/else`、`contains` 与 format checker 的 Draft 2020-12 fixture。
- probe 通过后才更新 `active.json`。普通失败保留旧目录；只允许清理由 metadata 明确归属的失败候选，不递归处理未知 sibling。

## Resolver 合同

resolver 输入为 repo root 与可选 runtime root，输出只通过 `exec` 或稳定 JSON 错误表达：

- 读取 installed runtime manifest 与 active pointer；
- 重新计算 lock digest及预期 identity；
- 验证 active metadata、解释器 regular-file/可执行状态和 probe；
- 成功时 `exec <managed-python> ...`；
- 失败时 stderr 输出单个 `runtime_dependency_missing` JSON，退出码 2，无 traceback。

错误对象字段保持最小稳定集合：`code`、`field_path`、`dependency`、`runtime_identity`（无法确定时为 null）与 `remediation`。remediation 使用当前 README 中真实存在的 preset apply 命令。

`launch.sh`、`run-skill-command.sh` 以及直接调用 Python 的 Guru-owned eval/discovery/validation shell 入口统一调用 resolver。纯 installer bootstrap 与只在 installer 内运行的 source ownership validator不依赖尚未创建的受管 runtime。

## Installer 集成与回滚

- lock、runtime manifest、resolver/bootstrap/probe 加入 `SKILL_RUNTIME_KERNEL_PATHS` 或等价 managed inventory，并进入 installed manifest hash 校验。
- runtime bootstrap 在 staging/activation 边界前完成；若 target asset install 随后失败，active runtime 可以保留，因为它是 gitignored、可由相同 identity 幂等复用的已验证环境。
- lock/Python identity 变化不会修改旧 environment；切换失败自然回滚到旧 active pointer。
- reapply 必须验证 resolver 没被 `trellis update` 后的 installed bytes 回退为 PATH `python3`。

## 兼容性

- 现有 Skill package、command id、public schema、typed exit 均不变。
- canonical source wrapper 与 installed/platform projections 最终都落到同一 `.trellis/guru-team/runtime` resolver；平台无需独立 Python 配置。
- Python 支持范围由 manifest 明确声明，并根据当前 Trellis/Guru 支持基线测试；不依赖未声明的 minor version。

## 测试设计

- runtime unit：identity、active pointer、resolver 成功/错误、Draft 2020-12 probe、PATH/venv 隔离。
- installer unit：fresh build、same identity reuse、lock/Python identity change、corrupt runtime、venv/pip 缺失、pip/network failure、candidate recovery、unknown directory保护。
- package tests：真实 wrapper `--help --json` 与至少一个 schema-bound command 都由 managed Python 执行；缺依赖为失败而非 skip。
- focused clean install：建立临时 repo 和一个 PATH `python3` shim，该 Python 可运行 installer/venv 但 `import jsonschema` 失败；apply 后通过真实公开 wrapper schema 路径。
- equality/drift：canonical/installed runtime 与 lock byte equality、targeted reapply、dogfood drift、递归 sidecar 扫描。

## 风险与取舍

- 完整 hash lock 对 Python minor/platform wheel 可用性敏感；测试必须证明支持的当前 macOS 环境可安装，错误合同需明确 wheel/hash remediation。
- 每次 wrapper 都运行完整 schema probe 成本较高；resolver 可用 metadata 加轻量 import/version probe，但不得仅因 metadata 存在就信任损坏 runtime。具体平衡以测试性能和损坏检测为准。
- 不在本任务做 stale runtime 垃圾回收，避免扩大删除边界；旧环境占用磁盘是接受的当前取舍。
