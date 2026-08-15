# Issue #236 技术设计

## 设计原则

1. 我们永远处在一个诚实互信的 Agent 人机协作环境里；设计只解决 Happy Path，并确保所有合法场景下的 Happy Path 通过。
2. 不改变 managed runtime identity/cache 合同，只修 verifier 的 caller routing。
3. shell 只选择 source/installed runner；Python 负责结构化 JSON、identity 和 caller inventory 校验。
4. source 与 installed 证据分开解析，禁止通过同一个 source interpreter 模拟 target 成功。
5. 静态 caller graph 与动态 checkpoint 同时成立，避免正常执行的 exit 0 掩盖路由错误；静态检查只建模仓库真实 caller 及常见合法维护写法，不枚举对抗性绕过语法。

## 运行链路

设计目标是让维护者不需要理解或修补本机 Python 状态：原始 README 命令在正常环境中只用 PATH Python 完成一次 bootstrap，此后每个正常 checkpoint 都沿 managed runner 获取一致解释器和依赖。静态 inventory 只防止未来维护时无意重新引入裸 PATH Python。

```text
PATH python3
  -> canonical bootstrap.py                 [bootstrap_seed, exactly once]
  -> source-managed-runtime.json
  -> canonical source resolve-python.sh
       -> source managed interpreter        [source_managed]
       -> validate bootstrap JSON/identity/lock
       -> source assertions and inventory

preset apply(target)
  -> target .trellis/guru-team/runtime/resolve-python.sh
       -> installed managed interpreter     [installed_managed]
       -> target/package/fixture assertions
       -> linked-worktree/closeout/no-developer checkpoints
```

## Runner 合同

### Source runner

`source_python()` 固定调用 canonical `trellis/skills/guru-team/runtime/resolve-python.sh`，参数绑定 source repository 与 canonical runtime assets。bootstrap seed 返回后立即使用该 runner 读取 `source-managed-runtime.json`，并验证 resolver 的实际 `sys.executable` 与 bootstrap interpreter 的规范化启动路径、物理解析 identity、runtime identity 和 lock identity 完全一致。启动路径规范化只解析父目录 alias，保留最终 `venv/bin/python` symlink。

### Installed runner

`installed_python <repo> ...` 固定调用 `<repo>/.trellis/guru-team/runtime/resolve-python.sh`，参数绑定该 repo 与其 installed runtime assets。initial、after-update、linked-worktree、closeout 与 no-developer fixture 均使用各自 repo 的 resolver；调用方不能传 source interpreter。

## Source-owned 路由检查器

新增 `trellis/presets/guru-team/scripts/python/verify_throwaway_python_routing.py`，由 source 或 installed runner 执行，提供两个确定性子命令：

- `checkpoint`：读取 bootstrap/resolver/pointer/cache metadata/lock，分别断言实际 `sys.executable` 的 managed 启动路径与物理解析 identity，再断言 runtime identity、dependency-lock identity，并输出最小 JSON evidence。
- `check-inventory`：读取显式 inventory，扫描 verifier、直接 helper 和第二跳 Python 入口，拒绝未分类裸解释器、PATH shebang、非 `sys.executable` Python subprocess 与 inventory drift。

该 helper 是 verifier source asset，不加入 public Skill DTO，不承担 semantic pass。

检查器不是 hostile-input 或 anti-bypass 边界。它只需精确识别当前 canonical caller graph、正常新增 caller 的常见写法和合法命令参数，并避免把普通数据文本误判为 Python launcher。

## Caller inventory

新增 `trellis/presets/guru-team/tests/throwaway-python-callers.json`，每项包含稳定 id、owner path、入口 kind、分类与 expected launcher。门禁要求发现集与登记集完全一致：

- 发现但未登记：失败；
- 登记但已不存在：失败；
- 同一入口重复分类：失败；
- `bootstrap_seed` 数量不是 1：失败；
- bootstrap 后 shell 裸 `python3` 或 PATH shebang：失败；
- helper 第二跳启动 Python 时未使用 `sys.executable` 或 installed resolver：失败。
- verifier 实际执行的 package/platform wrapper 未登记、固定 command id 与 `commands.json` 不一致，或未沿 canonical wrapper 进入 installed `runtime/launch.sh -> resolve-python.sh`：失败。

行号不作为长期 identity；使用 owner path、AST/语法上下文与稳定 call id，避免普通编辑造成无意义 churn。

## Helper 第二跳

- verifier 直接调用的三个 Python helper 均由 installed runner 启动。
- helper 内生成的 Python fixture shebang 使用当前 managed `sys.executable` 的绝对路径，不再使用 `/usr/bin/env python3`。
- helper 内需要再次启动 Python 时显式使用 `sys.executable`；非 Python subprocess（git、gh、shell wrapper）保持原合同。
- helper 结果增加内部 `runtime_checkpoint` 字段，供 verifier 精确断言 linked-worktree/closeout 身份；不改变 public Skill schema。

## 双环境 fixture

- 无依赖环境使用当前不含 `jsonschema` 的 PATH Python，直接运行 README 命令。
- 有依赖环境创建临时 `python3` shim，转发到可导入 `jsonschema` 的解释器。seed 完成后 verifier 通过测试专用 sentinel 激活 poison；若任何 bootstrap 后路径再次调用 PATH `python3`，shim 立即失败并记录调用。
- checkpoint 同时证明 managed `sys.executable` 的启动路径不是 PATH shim/underlying PATH interpreter，并证明其物理解析 identity 与 managed interpreter 一致。

测试专用 sentinel 只控制 fixture 观测，不参与生产路由或 runtime authority。

## Docs SSOT Plan

Strategy: `ssot_first`。

先更新以下 durable source specs，再实现代码：

- `.trellis/spec/preset/installer.md`（本仓库 preset installer durable spec；当前不作为 preset 安装资产分发）
- `trellis/presets/guru-team/spec/workflow/companion-scripts.md`
- `trellis/presets/guru-team/spec/workflow/quality-guidelines.md`
- `trellis/presets/guru-team/README.md`

随后通过 canonical preset apply 同步 dogfood `.trellis/spec/**` 与 installed managed copies，并验证 drift/sidecar。无需修改 global workflow、Skill public I/O、schema 或 platform overlay。

## 兼容与失败行为

- README 原始命令保持不变。
- runtime/cache/pointer 格式保持不变。
- source 或 installed resolver 失败时保留现有稳定 remediation，不 fallback。
- inventory/checkpoint 失败在对应业务检查前终止并给出 caller/checkpoint identity。
- 不删除或清理现有 runtime cache；throwaway 工作目录仍由原脚本生命周期管理。

## Branch Review 必答项

独立 reviewer 除完整 diff 外必须检查：

1. bootstrap JSON 是否由 source managed runner 实际消费；
2. bootstrap 后是否仍有裸 Python 或 PATH shebang；
3. source/installed runner 是否在任一 checkpoint 混用；
4. PATH Python 已有依赖时是否仍可能掩盖错误；
5. 新增 Python subprocess 是否会被静态 inventory 门禁拒绝。
