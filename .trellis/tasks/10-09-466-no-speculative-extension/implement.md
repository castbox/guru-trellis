# #466 执行与验证规划

## 顺序

1. 核对 live #466、TaskId/generation/checkout、current Architecture/RDT/constitution/change contract；current 有变化时执行现有 stale/re-entry。
2. 完成 Planning wording、normal-scenario/mechanism qualification、Planning Architecture 与 plan approval；展示三份具体规划并在现有 activation 边界暂停。
3. 激活后先更新 task-isolated RDT/Architecture contribution 与 proposed amendment；在 canonical skill references 中补充对唯一 authority 的消费和现有回程，不写公共 schema、新状态或评分机制。
4. 完成 C466-01..06 的正反例/fixture；检查当前必要 abstraction 与真实 compatibility 不被关键词或功能绿测错误拒绝。
5. 同步 canonical -> dogfood/installed/声明平台投影，运行最小定向检查；实际结果仅写唯一 Test contribution。
6. 完成 fresh Phase2 Architecture/check；在独立 Git 副作用边界创建任务 commit，随后在 exact `origin/main...HEAD` 上进行独立 Architecture 与完整 Branch Review。
7. 对已 reviewed contribution 执行 expected-current-bound promotion；原 RDT owner承接 successor authority；删除已消费 proposed amendment 副本。
8. promotion 新 diff 重新 Phase2 Architecture/check、commit、不同 reviewer 完整 Branch Review。只有当前 formal typed exits 才能进入 Delivery/Completion/Closure/Finish。

## 定向验证

| 检查 | 目的与完成条件 |
| --- | --- |
| constitution/六案例语义审查 | R466-01..05 与 C466-01..06 全部有当前证据，正确区分 requirement/mechanism 回程，五 identity 不变；脚本成功不等于语义 pass。 |
| project-check | 按 `guru-trellis-architecture-convergence@1` current descriptor 检查九 concern、单 authority/writer、before/after、current freshness、review/promotion。 |
| package contract/runtime | 执行 Architecture、Check、Branch Review 的变更相关 tests；新增 fixture 只增加直接验证 accepted scope 的检查。 |
| source/installed | `check-skill-packages.sh --root . --mode source --json` 与 `--mode installed` 均通过。 |
| apply/reapply/drift | `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 后执行 `check-dogfood-overlay-drift.sh`；各真实 .new/.bak 按原 ownership处理，最终零未处理 sidecar。 |
| task/hygiene | `python3 .trellis/scripts/task.py validate .trellis/tasks/10-09-466-no-speculative-extension` 与 `git diff --check` 通过。 |
| fresh promotion gates | 每个结果绑定 promotion 后当前 candidate/完整 committed range，不复用旧 pass。 |

命令从已解析的 task checkout 执行。通过项目现有 managed runtime 跑 package tests，缺依赖记 blocked/unverified；不安装环境来伪装已验证。完整多平台 clean/existing/update/release matrix、远端 marketplace、真实业务安装/部署不在本任务验证范围。普通 installer apply/reapply 是投影检查，不声明软件发布或全链兼容。

## 外部副作用边界

本轮写三份 Planning 和 Architecture contribution；实现需计划激活。commit、push、PR、merge、Issue closure、tag/Release、资源清理均由后续原 owner 展示精确候选并取得各自所需确认。授权只存在当前对话，不写入文件或 checkpoint。业务 Delivery 为 Refs-only，不在 PR 文案中自动关闭 Issue。
