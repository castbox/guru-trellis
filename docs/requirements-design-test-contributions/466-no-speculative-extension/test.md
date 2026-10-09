# #466 Test 增量

状态：draft / task-isolated / non-current；继承 `current-main-0.6.17-guru.76/active`。本文件是本任务实际验证结果的唯一 owner。2026-10-09 从 #466 已绑定任务 checkout 验证。脚本结果仅证明确定性合同，不证明正式 semantic gates、promotion 或 Release。

| Test | 实际结果与覆盖 |
| --- | --- |
| T466-SEMANTIC | 实现期人工语义核对：C466-01..06 的事实/正反对照/原回程完整；当前必要能力、兼容和职责抽象可成立，多余 mechanism 与 Requirement-authority 冲突分流，future边界不产生实现义务。当前五 identity/short name 未改；公共包只消费 identity/适用结论，无 schema/runtime/exit 变更。此核对不替代主 owner 正式 Phase2、project-check 或独立 review。 |
| T466-PACKAGES | PASS：managed interpreter 下 Architecture 26、Check 29、Branch Review 36 项既有 contract/runtime tests，共 91 项。覆盖现有 closed routes、qualification边界、Architecture stage消费、独立range/promotion条件和 projection。没有将示例语义写成脚本分类器或镜像文本测试；这些机器测试不证明六案例的 AI 语义判断已由独立 reviewer 执行。 |
| T466-DISTRIBUTION | PASS：source inventory（35 packages、106 commands），installed inventory（35 packages、159 public exits、33 mandatory invokes/153 business exits；0 conflicts/sidecars），preset apply/reapply 后 activation passed、dogfood drift passed。五变更文件在 installed/shared/Codex/Claude/Cursor 的25份投影与canonical逐字节一致，workflow也保持parity。 |
| T466-HYGIENE | PASS：task validate（implement/check各7项；有两个大spec的32768-byte截断警告，相关完整章节已直接读取）；git diff --check；contribution相对链接、zero sidecars、shared current未写检查。 |
| T466-PROMOTION | 未执行：独立 committed review、expected-current promotion、promotion 后 fresh Phase2/commit/完整 Branch Review。该项仍是当前 Delivery 前提，不能用上述结果代替。 |

## 可复现命令与结果

三个 package 从本 checkout 各自执行，均退出 0：

```sh
bash trellis/skills/guru-team/runtime/resolve-python.sh "$PWD" "$PWD/trellis/skills/guru-team/runtime" -m unittest discover -s trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/tests -v
bash trellis/skills/guru-team/runtime/resolve-python.sh "$PWD" "$PWD/trellis/skills/guru-team/runtime" -m unittest discover -s trellis/skills/guru-team/packages/guru-check-task/tests -v
bash trellis/skills/guru-team/runtime/resolve-python.sh "$PWD" "$PWD/trellis/skills/guru-team/runtime" -m unittest discover -s trellis/skills/guru-team/packages/guru-review-branch/tests -v
bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
bash trellis/presets/guru-team/scripts/bash/apply.sh --repo . --json
bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 .trellis/scripts/task.py validate .trellis/tasks/10-09-466-no-speculative-extension
git diff --check
```

首次 apply 退出 2 / conflict：本次五文件在五个managed projection roots中产生25个正常 `.bak`，installed validator正确阻塞未处理sidecars。逐个读取后确认每个backup等于同路径canonical的HEAD前版字节、当前目标等于新canonical；只消费这些已确认本次生成的backup。随后再次apply退出0，activation passed，recursive sidecar scan为0；无unknown local edit或 `.new`，没有删除其它资产。

安装使用已有managed runtime，未安装新依赖；没有改installer、上游agent、平台launcher或全局workflow。未执行官方 Trellis update；已验证canonical/preset投影及reapply恢复面，不能宣称完整upgrade-update兼容。

## 未验证边界

正式 Architecture/RDT/Phase2 结论由各原 owner 在当前调用承接，本页不重复保存或重建 semantic pass；独立 committed review、promotion及其fresh gates仍未执行。完整多平台 clean/existing/update/release matrix、远端 marketplace、真实业务安装/部署与软件 Release 不在 #466 验证范围；未验证，不声明完成。
