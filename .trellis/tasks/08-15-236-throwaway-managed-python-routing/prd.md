# Issue #236: throwaway verifier 受管 Python 路由

## 目标

修复维护者公开入口 `./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 的解释器路由，使 bootstrap seed 成为完整 verifier caller graph 中唯一直接使用 PATH Python 的调用。bootstrap 成功后，所有 Python subprocess 均由 source 或 installed managed runner 执行，并在 PATH Python 有、无 `jsonschema` 的环境中保持相同结果。

## 范围假设

我们永远处在一个诚实互信的 Agent 人机协作环境里；本需求只解决 Happy Path，并确保所有合法场景下的 Happy Path 通过。caller inventory 和静态防回归检查用于发现当前真实调用图中的遗漏、普通实现错误与后续正常维护漂移，不用于枚举攻击手段、对抗性语法变体、故意绕过或恶意输入，也不得以这些场景扩张实现和验收范围。

## 背景与当前证据

- 本 Issue 来自多次普通使用中反复出现的 Python 环境故障：维护者按 README 运行 verifier、执行正常 update、linked-worktree 与 closeout 流程时，Happy Path 会因 PATH Python 的环境或依赖差异而失败。既往问题均发生在这些简单合法场景，不涉及攻击、绕过或恶意调用方。
- Live Issue #236 是当前唯一 open 交付目标，无评论；open duplicate 检索只返回 #236。
- Fresh base 为 `main@f2bfbd93a0bb7db1b6850a760c278827c21c13b1`。
- 当前 verifier 在第 36 行完成 bootstrap seed，但之后仍有大量裸 `python3`，包括内联标准库断言、package tests 和三个 source helper。
- verifier 的内联 Python 与 `verify_installed_closeout.py`、`verify_installed_task_workspace.py`、`verify_installed_phase0_transcript.py` 还包含 Python `subprocess` 第二跳和 `#!/usr/bin/env python3` fixture。
- 现有 `runtime/resolve-python.sh` 已能从 Git common-dir pointer 解析并验证精确 managed interpreter；本任务复用该合同，不新增 repo-local venv 或新的 runtime identity 模型。
- #219 定义 managed dependency/runtime 合同，#231 定义用户级 immutable cache 与 linked-worktree pointer 合同；二者只作为既有约束，不作为旧 task/worktree 复用来源。

## 需求

### R1. 唯一 bootstrap seed

- verifier 启动阶段只能有一个 shell-level PATH Python 调用。
- 该调用只能执行 canonical `trellis/skills/guru-team/runtime/bootstrap.py`，不得执行 verifier 业务检查。
- bootstrap 输出继续写入 `source-managed-runtime.json`，并必须被后续 managed 检查消费。

### R2. 两类 managed runner

- bootstrap 后建立唯一 source managed runner，调用 canonical source `resolve-python.sh`。
- target preset 完成安装后，建立 installed managed runner，调用 target 自身 `.trellis/guru-team/runtime/resolve-python.sh`。
- source 检查不得用 installed interpreter，installed/target/linked-worktree/no-developer 检查不得用 source interpreter 冒充 installed evidence。
- resolver、pointer、runtime cache、interpreter、identity 或 dependency lock 不匹配时 fail closed，不得回落 PATH、active venv、global 或 user site-packages。

### R3. 完整 caller inventory

- 盘点 verifier shell、内联 Python、直接 source helper、shell wrapper 第二跳、Python `subprocess` 第二跳和生成的 Python shebang。
- 每个 Python 入口只能分类为 `bootstrap_seed`、`source_managed` 或 `installed_managed`。
- 增加 source-owned、机器可执行的静态门禁；新增裸 `python3`、`#!/usr/bin/env python3`、未登记 Python subprocess 或未通过 `source_python`、`installed_python`、`sys.executable` 的入口时立即失败。
- “仅使用标准库”不是保留裸解释器的理由。

### R4. 精确运行时证据

- source/installed runner 执行 checkpoint probe 时必须断言：
  - `sys.executable` 的规范化启动路径必须与 resolver/bootstrap 返回的 managed interpreter 启动路径一致；规范化只解析父目录 alias，必须保留最终 `venv/bin/python` symlink；
  - 两侧启动路径各自解析后的物理 interpreter identity 必须一致，不能只比较路径文本或只比较物理文件；
  - runtime id 必须与 active pointer、cache metadata 与 bootstrap/resolver 结果完全一致；
  - dependency lock SHA-256 必须与 runtime metadata identity 中的 lock digest 完全一致；
  - interpreter 是该 runtime identity 下的可执行 regular file。
- 证据覆盖 `source-bootstrap`、initial、`guru-review-change-request` initial、after-update/reapply、`guru-review-change-request` after-update、linked-worktree、closeout initial/after-update 与 no-developer fixture。
- 证据仅作为测试/gate 输出，不扩张 public Skill DTO。

### R5. 双环境判别

- PATH Python 无 `pip` / `jsonschema`：不 activate venv、不预装依赖、不手工导出 cache path，直接运行 README 原始 verifier 命令并完整 exit 0。
- PATH Python 有 `jsonschema`：probe/poison fixture 在 bootstrap 返回后拒绝任何 PATH Python 调用；完整 verifier 仍 exit 0，且 checkpoint 证明实际执行者为 managed interpreter。
- 双环境均不得通过只运行上层 `guru-verify-extension-installation` wrapper 代替 README 原始命令。

### R6. 原完整矩阵保持

- 保持 marketplace workflow install、preset initial apply、official `trellis update`、workflow preview/switch、preset reapply、source/installed/platform equality、linked worktree、closeout、no-developer、ownership、dogfood drift、inventory、executable modes 和零 sidecar/cache residue覆盖。
- `guru-review-change-request/tests/test_contract.py` initial 与 after-update smoke 必须由 installed runner 执行。

### R7. Canonical、installed 与文档同步

- 修改 canonical verifier/helper/test 与 preset durable specs。
- 通过 preset apply 同步 dogfood installed copies，并同步 README；不修改 Trellis upstream 或全局安装。
- 处理并报告所有 `.new` / `.bak`，最终 drift/sidecar 为零。

## 验收标准

- AC1: 静态 inventory 门禁证明 verifier caller graph 只有一个 `bootstrap_seed`，其余入口全部有且只有一个 managed 分类。
- AC2: source bootstrap JSON 被消费，source runner 的 executable/runtime/lock 三项完全匹配。
- AC3: initial 与 after-update target、两次 change-request smoke、linked-worktree、closeout 和 no-developer checkpoint 的启动路径、物理 interpreter、runtime 与 lock identity 完全匹配对应 installed runner。
- AC4: PATH Python 无 `jsonschema` 的环境直接运行 README 原始命令，完整矩阵 exit 0。
- AC5: PATH Python 有 `jsonschema` 的 poisoned fixture 证明 bootstrap 后 PATH Python 未再执行，原始命令完整 exit 0。
- AC6: source/installed runner 不混用；损坏或 mismatch 路径 fail closed，无 PATH fallback。
- AC7: focused tests、shell syntax、Python compile、ownership、managed inventory、dogfood drift、零 `.new`/`.bak`/cache residue通过。
- AC8: 独立 Branch Review 覆盖 `origin/main...HEAD` 全 diff 与完整 caller graph，并逐项回答 bootstrap 输出消费、bootstrap 后裸 Python、runner 混用、PATH 依赖掩盖、新 subprocess 静态约束五个负向问题。
- AC9: PR 仅包含 `Closes #236`；不关闭 #127、#220，不创建 tag/Release，不升级业务仓。

## 非目标

- 不实现、恢复、清理或修改 #220 的 worktree、branch、task 或未提交内容。
- 不处理 #127 的 fresh reconciliation。
- 不创建 `v0.6.5-guru.8` tag 或 GitHub Release。
- 不升级任何真实业务仓。
- 不重新设计 runtime identity、cache ownership、Git common-dir pointer、锁、TOCTOU、恶意篡改或跨 OS 原子性。
- 不枚举或防御调用方故意构造的静态检查绕过；只覆盖仓库真实 caller graph 和合法维护场景中的常见调用形态。

## 开放问题

无。实现路径与风险边界均可由 live Issue、现有 runtime、verifier 和 specs 直接确定。
