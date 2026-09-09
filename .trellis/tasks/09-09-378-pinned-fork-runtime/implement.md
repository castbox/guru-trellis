# #378 实施计划

## 当前阶段

planning。未开始实现，未恢复 stash，未更新主 checkout runtime。

## 实施顺序

1. 完成 planning wording、normal-scenario、solution-mechanism、Architecture/RDT impact 与 approval；展示最终规划后取得实施确认。
2. 固定 Fork commit；核对 build/init/update 对 docs-site/marketplace 和 npm 包的实际读取，不执行不需要的递归 submodule 初始化。
3. 先添加来源与调用路径回归，再把 canonical source lock 接入现有 installer/verifier；直接运行 Fork 自身的 Node CLI，不新增打包、缓存或 launcher。
4. 迁移 installer、manifest、当前文档和验证脚本；删除原发行源正常安装/更新路径，不修改历史记录。
5. 在代表性临时项目运行 clean init 和 existing update/reapply，再重复 update 验证来源不回退。
6. 在任务 worktree 使用固定 Fork CLI 生成 runtime，按原三平台 reapply preset；逐个审查 sidecar，不恢复 stash manifest。
7. 执行 canonical/installed 的 session、CLI、主 hooks、child、并行 worktree 回归；验证 fixture 调用前后 session 内容和路径集合不变。
8. 执行 #388 Wording 与 #389 workspace 集成回归、source/installed schema/inventory、ownership、drift 与 whitespace 检查。
9. 完成 Docs contribution reconciliation、Architecture/check；再单独申请 commit、PR 和 merge。保持 #388/#389 为关联项，不通过本任务关闭。

## 验证入口

所有测试使用现有受管 Python 或固定 Fork 的依赖环境，不使用全局包替代缺失依赖。

```bash
bash .trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task .trellis/tasks/09-09-378-pinned-fork-runtime
bash trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

新增测试落在 preset scripts/python 的现有 unittest 体系，覆盖 source identity、构建失败
无回退、两次 update、canonical/installed hooks 和 session fixture。执行命令及结果在
实际实现后记录，当前不填写 PASS。已有 #388/#389 集成测试按其现有文件运行。

## 安装态 closeout 测试边界

closeout verifier 的场景准备留在 verifier 内，通过已安装的 Planning、Phase 2、Commit、
Branch Review、Publication 入口执行；测试输入是 synthetic fixture，不是本任务的真实审批。
不从 native adapter、共享 production fixture 或 owner runtime 导入业务编排函数。
定向测试使用独立临时仓库、fake GitHub store 和实际 installed wrappers；入口缺失必须报错，
不回退到 source runtime。该测试成功不等于完整 Fork 来源迁移或发布矩阵通过。

## 回退与保留

只回退本任务工作区的具体变更步骤；不 reset 用户其他工作。构建 cache 和 installer
备份按既有 lifecycle 处理，删除前单独列出对象。`issue-378-fork-upgrade` stash 保留。
源码测试、installed 验证、真实业务接续和发布矩阵分别报告。

## Closeout 定向验证结果（2026-09-09）

- dirty worktree 直接作为安装来源时，Finalizer 按预期拒绝
  `provenance_tail_source_not_clean`；这不是 fixture API 修复失败。
- 从当前文件创建独立、干净的本地测试源码快照后，真实 installed
  record/check/public wrapper 链路完成 initial closeout：
  `ready_for_merge` -> fake-provider `merged`，终态 checkpoint 已消费。
- 同一临时目标执行三平台 preset reapply 后，`after-update` case 再次通过。
  本轮只执行 reapply，没有再次运行 Fork CLI update，不能据此声明升级验证通过。
- GitHub PR 与 merge commit 均由 fixture provider 提供；没有真实远端发布、合并或
  本任务工作区提交。临时源码快照不等于远端发布的 candidate source。
- 本结果仅关闭已观察到的 closeout fixture 私有 adapter 调用缺口；Fork 来源固定、
  source-lock 实际消费、完整矩阵和先前 template-hash 判定仍需独立审核。

## 固定来源定向验证结果（2026-09-09）

- 现有 castbox/Trellis checkout 在固定 SHA 上使用自身 pnpm lock 安装依赖并重新 build。
- 现有 verifier 直接运行该 checkout 的 Node CLI；移除原 npm 安装分支与路径猜测。
  source record 经 preset 投影到 `.trellis/guru-team/trellis-source.json`，由 managed hash 记录。
- Codex focused clean init 与两次同候选 update/reapply 通过；实际观察 source SHA 为
  `ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`，202 个模板资产与源码字节一致。
- 本次使用本地未发布 workflow 样本；不是远端发布验证，也不是 predecessor 升级矩阵。
- canonical Fork regression 503 项通过；来源/安装/routing/ownership 108 项通过；
  canonical 与 focused installed session/hook 隔离测试均通过，包括两个真实临时 worktree。
- 移除 AGENTS.md 无条件豁免。只接受准确的 preset 区块，且去除该区块和插入换行后
  必须匹配原记录 hash；区块内外其他编辑均被测试证明会拒绝。
- 当前 worktree 三平台 preset reapply、source lock 字节一致性、drift 与 whitespace 通过。
  历史完整矩阵缺少 predecessor 源码输入时明确阻塞；业务接续与发布未验证。

## 独立检查修正（2026-09-09）

- 发现并修复现有 standalone caller 未承接 Fork 参数的回归：旧 workdir 调用可继承
  显式 `TRELLIS_FORK_SOURCE`，full predecessor 使用独立 checkout/SHA 配置。
- 恢复 full runner 的实际可达路径与 `install/project` 代表安装输出；focused 不替代
  原 capability catalog。缺失 predecessor 返回具体 source-validation 失败。
- 99 项 caller/routing 回归通过；真实 shell focused 调用完成 clean 与两次同候选
  update/reapply。完整历史矩阵只完成入口/调度的轻量回归，未声明实际运行通过。
- standalone 合同已同步三平台；reapply、drift、whitespace 通过。本轮未提交或发布。
