# 实现与受管采用验证

## 范围与实际结果

本记录覆盖 D1 的 canonical 方法合同和 AC7 受管采用。质量规范 Test And Validation Value 单写行为断言、方法选择、证据采用、追加实验、失败归因与停止原则。根因 Skill 区分候选准入和修复完成；Author 共享合同、两个模板、Phase2、Check、Branch Review 和两份公共 README 消费同一方法。公共 I/O、阶段、runtime 语义和官方 Agent/hook 未修改。

由完整 canonical `guru-upgrade-tools` 的原 preview → prepare → invoke 更新本 checkout。目标保持 Claude、Codex、Cursor 三平台；`.trellis/config.yaml` 保留，AGENTS 自定义内容由原 renderer 承接。原 installer 生成受管副本与 manifest；未手工复制 projection、未走普通 apply、未迁移 Task/session。

实际 public 出口为 `tools_upgraded`，installed_version=`0.7.0-guru.7`，未验证边界为 `formal_fork_source_lock`。恢复定位仅由原维护 owner 在私有运行时承接。

本次 source HEAD 为 `b78edbbdc32e77392bc3775366473971050ccb4b`，采用 dirty canonical 内容的 `local_candidate`。真实 CLI/Core 从本地完整 Trellis 的 public maintenance API 加载，版本均为 `0.7.0-castbox.6`；实际 bytes identity、API1.0 和 AGENTS custom capability 已通过原 transport 核对。上述 DTO 仅证明工具维护结果，语义行为另由原评估与正式 owners 判断。

## 实际检查

以下命令在本 Task checkout 执行；结果没有由模板预填。

| 检查 | 实际结果与证明边界 |
| --- | --- |
| managed Python `-m unittest discover -s trellis/skills/guru-team/packages/guru-qualify-root-cause/tests -p test_contract.py` | 2/2 通过；既有合同结构检查，不替代语义评估。 |
| managed Python `-m unittest discover -s trellis/skills/guru-team/packages/guru-author-task-plan/tests -p test_contract.py` | 2/2 通过；既有合同结构检查。 |
| `.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source` | passed；43 packages、128 commands、147 package tests。后续私有 collector 不改变公共投影。 |
| `.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed` | 新进程检查 passed；8566 managed files，conflict/sidecar/private-test 数均为0。首轮曾 exit2 `runtime_dependency_missing`；随后目标 resolver 和相同 wrapper 均通过，首轮原因未确定，未修改 runtime。 |
| `bash .trellis/guru-team/runtime/resolve-python.sh "$PWD" "$PWD/.trellis/guru-team/runtime" -c 'import sys;print(sys.executable)'` | exit0，解析到现有 managed cache 的实际 Python。 |
| `python3 .trellis/scripts/get_context.py --mode continuation` | exit0，目标原生 continuation 提取可用；不以此声明新的会话绑定或正式阶段通过。 |
| `python3 .trellis/scripts/get_context.py --mode phase` 及分别 `--step 1.1`、`--step 2.1`、`--step 3.5` | 四次 exit0；Phase2 输出包含当前共同方法消费提示。 |
| `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` | exit0；canonical workflow、shared、Claude、Cursor、Codex 选择及 spec 投影一致，22 descriptor 的 ownership 检查通过。 |
| 递归检查 `.trellis`、`.agents`、`.claude`、`.cursor`、`.codex` 下 `.new`/`.bak` | 空列表；`.trellis/workflow.md` 与 canonical workflow 字节相等。 |
| `python3 .trellis/scripts/task.py validate .trellis/tasks/11-05-735-behavior-causal-validation --delivery 51cf3d42-d210-4938-a20a-da800f158795` | exit0；implement/check context 各7项。正文较大产生注入截断 warning，workers 仍须按原合同完整实际读取。最初省略 Delivery 参数的调用返回 selection-required，显式指定后通过。 |
| 规范 in-memory Python syntax、marketplace JSON、Bash syntax、`git diff --check` | 通过；本 worker 检查372个 Guru Python 文件，未写 bytecode。collector 后续变动由其 owner 检查 changed-file syntax。 |

## 证据边界

真实行为评估由 eval worker 提供，不能从分发一致、合同测试或上述工具 DTO 推定 AC1–AC6 通过。正式 Check/Review、RDT 晋升与交付由原 owners 承接。本次未运行完整多平台 clean/update/Release 矩阵，未证明外部业务仓采用，也未验证 formal Fork source-lock。未 commit、push 或创建 PR。
