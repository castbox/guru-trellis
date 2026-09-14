# #408 实施与验证计划

## 阶段边界

本文件是 Phase 1 计划，不是实现或验收结果。`prd.md` 定义需求，`design.md` 定义唯一设计与 Docs SSOT Plan。任务保持 `planning`；通过 wording、Architecture 和 Planning gate 后，展示三份文档并暂停，直至新的方案接受，再进入现有 task activation。

## 执行顺序

1. 重读 #408、task/Git/mapping、current RDT/Architecture 和已接受规划。基线变化先走既有 pair/reconciliation；不处理 #407 的 resolved merge。
2. 展示精确 Fork checkout/build、任务 worktree update 与 throwaway 安装路径后再执行对应安装动作。使用目标 commit 和真实 CI identity，不修改上游源码或共享全局 npm。
3. 在现有 source record/validator 中实现 D408-01，同步 preparation、upgrade 与安装 fixture。保留 predecessor 的历史语义，不用旧 provenance 或版本字符串冒充 target build。
4. 通过 target Fork 的正式 update/init 采纳 Trellis-owned templates。保留当前平台集合与未知用户文件；单独核对 generated diff。
5. 在 canonical workflow 与实际受影响的 Guru Skill/三入口实现 D408-03；逐项检查自动 stop 不禁止独立手动操作，既有 gate/exit/Finalizer 不改变。
6. 补充下表测试与 Agent 行为验证。测试只覆盖正常绑定、普通缺失/stale/执行错误及正文保留的权限/确认边界，不扩张 adversarial/TOCTOU/fault-injection 场景。
7. 执行 task worktree 的 preset reapply、逐项 sidecar 处理、source/installed/ownership/drift 与一个 focused installed 验证。既有 full matrix 不由本任务自动扩大执行；发布候选矩阵仍归现有 release owner。
8. 按 `design.md` Docs SSOT Plan 更新任务隔离贡献，完成 Phase 2 Architecture 与独立 task check。后续 commit/full-diff review/promotion/Publication/Finalizer/Merge 沿现有 lifecycle；每项 Git/GitHub 副作用单独展示确认。

## 验证矩阵

| ID | 需求 | 验证内容与通过条件 |
| --- | --- | --- |
| T408-01 | R408-01 | target Fork HEAD、CLI/core 0.6.17、pnpm identity、本地 build marker、CI run/head/success、source validator 输出一致；普通 stale build/错误来源被拒绝 |
| T408-02 | R408-02 | official update/init 生成 templates 后，canonical/dogfood/installed source record 一致；preset reapply 与 ownership/drift 通过；未覆盖用户自定义 |
| T408-03 | R408-03 | 同一显式session，primary经正常创建入口得到linked task，再回primary；current/context/SessionStart/workflow-state返回同一任务；两工作区foreign session不被借用 |
| T408-04 | R408-04 | 受影响package、finish-family和实际installed public wrapper链通过；23 Skills/97 exits/78 commands既有inventory不因本任务新增；retired依赖不重现 |
| T408-05 | R408-05 | 对缺失注入、缺失/stale session、routing/checkpoint/wrapper普通失败场景，Agent先报告原错误与已知/unknown事实，不重入no_task，不自修复、不虚报完成 |
| T408-06 | R408-06 | 在状态化fixture中分别演练commit、push、PR创建/更新、merge、Issue closure、tag/Release、cleanup；每次只执行当前明确操作，缺该操作确认不执行，无授权扩张 |
| T408-07 | R408-07 | 手动操作成功后保留task/runtime/Finalizer/archive原状态；结果报告区分操作完成和residue，不生成恢复artifact |
| T408-08 | R408-08 | focused installed使用target Fork真实build运行，source/CLI/runtime/hook同源；所有skip/外部未运行项标UNVERIFIED，不冒充Release Gate或真实远端完成 |

静态文案/fixture测试只证明合同与可控交互；T408-05..07 的 Agent 行为验证须包含实际读取 canonical 文案的运行证据。真实远端 GitHub mutation 未独立执行时明确 UNVERIFIED，不用 mock claim 实际操作成功。

## 具体命令

以下命令均在本任务 worktree 执行；当前尚未运行实施验证。

```bash
python3 -m json.tool trellis/index.json
for f in trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh; do bash -n "$f" || exit; done
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p 'test_fork_*.py'
python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p 'test_verify_trellis_upgrade_contract.py'
python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p 'test_apply_guru_team_trellis_preset.py'
python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_finish_family_integration.py'
bash trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
bash trellis/presets/guru-team/scripts/bash/apply.sh --repo .
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 .trellis/scripts/task.py validate .trellis/tasks/09-14-408-nightly-session-binding-manual-fallback
git diff --check
```

`test_fork_*.py` 的 canonical case 需显式 `TRELLIS_FORK_SOURCE`，installed case 需显式 `TRELLIS_INSTALLED_REPO`。两者只绑定实际验证后的路径。具体 source/installed package validator argv 在运行前读取现有 help，不猜测参数。

真实 installed 入口复用：

```text
bash trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh <exact-work-dir> --mode focused --fork-source <verified-target-fork>
```

临时目录必须明确给出并保留验证失败证据。local candidate与远端marketplace若不同，使用既有显式local-sample入口并标明“本地candidate installed证明”；后续远端exact-ref证据独立取得。不能把main的安装结果算作未发布candidate的结果。

## 子代理与上下文

实现阶段由主会话持有范围和副作用边界，按互不重叠的source/provenance与workflow文案职责分配Trellis implement工作；独立Trellis check读取完整当前task差异。JSONL只引用本任务文档与真实spec，不创建assignment或implementation-handoff文档。native context injection优先，缺失时由子代理读取相同路径。大规格只注入索引；子代理必须按索引分节读取 `workflow-contract.md` 与 `quality-guidelines.md` 的本任务适用正文，不能以截断的注入文本判断合同充分。

## 风险、停止与回退

- 网络/build/source校验失败：保留准确错误与日志路径，停止安装；不切换其它ref、全局包或版本。
- update产生未知修改或sidecar冲突：展示精确文件差异再处理，不覆盖用户内容。
- 场景、owner或shared-current变化：重入对应qualification/Architecture；不沿旧结果继续。
- touched非生成代码达到3000行：先做该职责的机械拆分并证明行为一致。
- 回退只针对本task已识别改动，使用已确认的Git操作；不自动reset、stash、删除worktree或重写上游。

完成本计划的Phase1审查不意味着以上测试已通过，也不意味着#408已修复或已发布。
