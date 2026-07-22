# #145 Branch Review 汇总

## 审查轮次

| 轮次 | 角色 | reviewed_head | Findings | 原始报告 |
| --- | --- | --- | --- | --- |
| 1 | 问题发现审查代理 `/root/issue145_final_review` | `72326953e4df36a91201f10f581361b045e8c6f0` | P1=1 | [001-final.md](reviews/001-final.md) |
| 2 | 问题闭环审查代理 `/root/issue145_final_review` | `ded63e71e5bab787c5d795a300e3507142b18521` | 0 | [002-closure.md](reviews/002-closure.md) |
| 3 | 最终放行审查代理 `/root/issue145_final_release` | `ded63e71e5bab787c5d795a300e3507142b18521` | P1=1 | [003-final.md](reviews/003-final.md) |
| 4 | 问题闭环审查代理 `/root/issue145_final_release` | `9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8` | 0 | [004-closure.md](reviews/004-closure.md) |
| 5 | 最终放行审查代理 `/root/issue145_final_release_r2` | `9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8` | 0 | [005-final.md](reviews/005-final.md) |

Round 1 与 Round 3 的 finding owner 均只以 `reuse-for-closure` 审查对应修复及同路径 correctness，未担任最终通过轮次。Round 5 使用从未参与 Round 1-4 finding ownership、closure 或实现的 fresh technical agent，`reuse_decision=new-agent`，是当前 HEAD 的最后一轮完整独立审查。

## 问题生命周期

### BR-001：preset conflict 失败后留下 mixed 1.2/1.3 graph

- 优先级：P1。
- 发现轮次：Round 1；finding owner：`/root/issue145_final_review`。
- 正常路径：pre-#145 已安装 graph 中存在正常 unknown local edit 时，旧 installer 会先改写其它受管文件再返回 conflict，留下 mixed graph。
- 修复 commit：`ded63e71e5bab787c5d795a300e3507142b18521`。
- 闭环轮次：Round 2，`reuse_decision=reuse-for-closure`。
- 闭环证据：installer 在 staging repository 内完成完整安装与 installed validation 后才激活；unknown edit / forced validation failure 只物化 `.new` 并保留旧 graph；known managed upgrade 完整激活六包五 roots 的 1.3 graph，处理声明 backup 后 reapply 与 zero-sidecar 通过；`.trellis/.developer`、runtime/workspace、Git 与 Python cache 不进入 transaction。
- 最终状态：closed；Round 5 完整复验未发现回归。

### BR-002：semantic re-entry 将 non-main resolver fallback 改写为显式 `main`

- 优先级：P1。
- 发现轮次：Round 3；finding owner：`/root/issue145_final_release`。
- 正常路径：仓库只有 `develop`，配置 `base_branch_candidates=["develop"]` 且省略显式 base 时，formal resolver 选择 `develop`，但 semantic producer 曾输出 `main` 并使 consumer 稳定返回 `blocked`。
- 修复 commit：`9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8`。
- 闭环轮次：Round 4，`reuse_decision=reuse-for-closure`。
- 闭环证据：删除 semantic producer 的第二套 `main` fallback；clarification / readiness 的相关输出和三条 sync-directed projections 保持 `base_branch` optional，由 `guru-sync-base` formal resolver 独占 explicit -> configured scalar -> ordered candidates -> remote default；config-candidate、remote-default 与 explicit 回归均通过。
- 最终状态：closed；Round 5 完整复验未发现回归。

## 最终审查

Round 5 fresh reviewer 独立覆盖 `origin/main...9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8` 的 1258 paths、三个 commits、四轮历史报告、两个 finding 生命周期、fresh Phase 2、三个 commit plans、Docs SSOT、六包/24 exits、三包 `1.2+legacy` 边界、canonical/installed/platform parity、preset transaction、clean install、pre-#145 upgrade、Trellis workflow preview/switch、`trellis update`、preset reapply、部署与安全影响。

最终语义结论为 passed：P0=0、P1=0、P2=0、P3=0。#145 是唯一 `close_issue`；#144/#147 仅为 closed authority refs；#146 保持 follow-up。Optional base fallback、actual-exit schema selection、production eval adapter 与 installer activation 均符合批准范围和 durable contract。

## 证据

- Base：`origin/main@096d1889a511969d5ff09ef4d198ac2825110148`；最终 reviewed HEAD：`9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8`。
- Work commits：`72326953e4df36a91201f10f581361b045e8c6f0`、`ded63e71e5bab787c5d795a300e3507142b18521`、`9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8`；parent chain 与三个 commit plans 的 path/tree/blob/mode 绑定一致。
- Commit 003：92 个 committed paths；expected/actual tree 均为 `ed8c7f4325113fc83911a264d8be8fcf4d4a73ae`；`hook_mutation=false`。
- Fresh Phase 2：artifact SHA-256 `dbf5ab3535c5fd5ab2829e1bb610a8d9caa1869d60368015ad222012bfc790e3`，`facts_sha256=73334880433f8384f50537d7ec645dd1acd02d49387d3a1f8dfa6e570f6c9eec`，`typed_exit=passed`，P0-P3 全 0。
- 测试：Skill `161/161`；runtime `548/548`、13 skipped；preset `45/45`；ownership `6/6`；shared production eval `24/24`。
- Source/installed validators、dogfood drift、upstream ownership、changed JSON、Python/shell syntax、task validation、`git diff --check`、sidecar scan 与 30/30 canonical-installed-platform parity 通过。
- Full throwaway 覆盖 marketplace discovery、local unpublished workflow sample、clean install、pre-#145 upgrade、preview/switch、`trellis update`、preset reapply、Stage 0 smokes 与 zero-sidecar，整体 exit 0；未发布分支 default marketplace guard 按预期 exit 2。
- Docs SSOT strategy=`ssot_first`；15 个 durable paths 已同步并与实现一致，Round 3 修复没有产生新的 durable-doc delta。
- 五轮 raw report digest、size、modified time、reviewed HEAD、technical identity、finding count 与 reuse decision 均已记录在 `agent-assignment.json`。

## 观察项

- Exact remote feature-branch marketplace install 仍需等待分支可远程解析后由 publish gate 验证；当前 local current-source、public marketplace discovery 与 fail-closed default guard 已验证。该发布时序限制不构成当前实现 finding。
- Authenticated Claude native live probe 未执行；repository tests 已覆盖 stdin/safe-mode 协议、fake-native trace、declared unsupported 与四平台 package parity。该外部 capability 限制不阻断当前交付。

## 后续候选

- #146 继续独占 `guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit` 三包迁移，不并入 #145。
- Publish gate 在远程 branch 可解析后补 exact remote marketplace proof，并在 PR readiness 中仅使用 `Closes #145`。
- 不新增恶意 actor、锁、并发压力、TOCTOU、crash consistency、跨 OS 原子性或额外 fault injection follow-up；这些场景不在当前需求范围。

## 部署与安全影响

完整 diff 不包含 GitHub Actions、container/Docker、K8s/Kustomize、Helm、数据库 migration、Makefile、dependency lock/config、生产配置、生产数据或权限变更，不需要服务停机、数据迁移或部署动作。Secret-shaped diff scan 为 0；报告未包含 token、credential、`.env`、signed URL、客户数据或原始 provider payload。升级仍按既有 `.new/.bak` 人工处理与 reapply 合同执行。

## 结论

Branch Review 最终语义审查通过：P0=0、P1=0、P2=0、P3=0，两个历史 P1 均已完成正常路径修复、同 finding owner closure 与 fresh final verification。该结论支持主会话执行正式 workspace boundary 与 post-commit Branch Review recorder/validator；它不授权 push、创建 PR、关闭 issue 或调用 `trellis-finish-work`。
