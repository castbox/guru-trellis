## 变更摘要

- 删除 canonical `trellis/workflows/guru-team/workflow.md` 与 dogfood `.trellis/workflow.md` 中不承载语义的重复空行，使两份 workflow 均由 427 行收敛到 411 行，满足既有 420 行预算。
- 保持两份 workflow 字节一致，并保持 13 个 mandatory Skill invocation、51 个 typed exit、唯一 consumer、fail-closed stop graph、Phase routing 与 #161 public contract 不变。
- 第二个提交仅补齐本任务的七个 task-local metadata 文件；没有新增 Skill、schema、runtime、preset、upstream patch 或业务产品行为。

## 影响范围

- workflow：仅影响 canonical workflow 和 dogfood workflow 的 Markdown 排版空行；line-budget assertion、marker payload、Phase/step headings 与 route contract 未改写。
- task-artifact：`.trellis/tasks/08-04-174-thin-workflow-420/` 下的 `task.json`、规划文档、JSONL 记录与 `issue-scope-ledger.json` 用于绑定本次 Issue、范围和验证过程，不参与运行时分发。
- 不涉及 Skill package、interface/schema、companion script、preset installer、平台 overlay、Trellis upstream、CI/CD、容器、Kubernetes、数据库 migration、依赖或 Makefile。

## 验证结果

- 当前 `origin/main...e68b3b2fbafc12f0b0e28e5df7f1f20a285fd336` diff 仅包含两份 workflow 与七个 task-local metadata 文件；`git diff --check`、Phase context parser、task validate 均通过。
- canonical/dogfood workflow 均为 411 行且字节一致；两份均保持 13 invokes、51 exits、15 workflow targets、13 stop targets。现有 graph/ownership、source/installed package、dogfood drift 与 managed installation/update/reapply 检查在 current-HEAD 复核中通过。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：488 项，1 个既有 README 基线失败（`FinishWorkEntrypointContractTest.test_closeout_docs_match_canonical_contract`），失败只涉及未被本 Issue 修改的根 `README.md`。
- `python3 -m unittest trellis/skills/guru-team/tests/test_skill_packages.py`：186 项，4 个既有 README 基线失败，分别为当前 finalization package state、README extension version、standalone runtime semantics 与 semantic edge migration 文案检查；本 Issue 未修改 README。
- 独立 Branch Review 已覆盖完整 `origin/main...HEAD` 两提交范围，确认没有未关闭 P0-P3 finding。上述 README 基线失败与本 Issue 的 workflow 行预算和 graph 变更分开记录。
- #132 的历史 combined acceptance 没有被本 PR 重新宣称为本 Issue 的新验证；本次新增证据只针对 #174 current-HEAD scope。

## Review Gate

- Branch Review reviewed content head：`e68b3b2fbafc12f0b0e28e5df7f1f20a285fd336`。
- Review 范围为完整 `origin/main...HEAD`，覆盖 workflow 压缩和 task metadata tail；无未关闭 P0、P1、P2 或 P3 finding。
- 发布前仍需由 Finalizer 处理 push、PR、archive 和 Issue close 等外部副作用；本 task 当前未执行这些动作。

## Issue 关闭范围

Closes #174

- 本 PR 只关闭 #174。
- 不关闭或重新打开 #132，也不关闭 #81、#98、#127、#53。

## 安全说明

- 未引入或暴露 token、credential、private key、signed URL、`.env`、数据库 URL、客户数据或敏感原始记录。
- 变更不包含部署单元、运行时配置迁移、数据库 migration、权限模型或回滚脚本；外部 push/PR/closeout 尚未执行。
- 验证中的 README 基线失败已按事实保留，没有用删除断言、放宽 420 行 assertion 或修改公共 graph 的方式掩盖。

## Docs SSOT

- strategy：`no_docs_update_needed`；本 Issue 只删除 workflow 中可重新推导的重复排版，不新增或改变公共合同。
- durable docs：不修改 durable docs；现有 `.trellis/spec/`、workflow README、preset README 与根 README 继续作为既有合同和安装说明的 SSOT。
- task delta：task-local planning、check、Issue Scope Ledger、`pr-body.md` 与 finish-summary index 只记录本 Issue 的范围、验证和发布语义，不扩展公共 workflow/spec。
- task history：current HEAD、测试计数、baseline failure、diff/marker 事实和 #132 历史 acceptance 保留为本 task/review history，不复制为新的 durable contract。
- follow-up/limitation：README 基线失败仍是独立文档同步缺口；#132 combined acceptance、远端 feature-ref marketplace 验证及 push/PR/Issue closeout 均不由本次 workflow 压缩直接完成，后续按各自门禁处理。
