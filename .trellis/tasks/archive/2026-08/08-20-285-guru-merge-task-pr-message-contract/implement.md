# #285 实施计划

## 1. Contract 与 schema 迁移

- [ ] 新增 Merge Skill active 2.0 workflow/standalone/aggregate input schemas、examples 与 2.0 private gate schema。
- [ ] 在 `interface.json` 选择新版本，保留并标注 1.0 immutable compatibility assets。
- [ ] 更新 Finalizer consumer authoring fields、production contract graph、consumer/eval fixtures；不改变 Finalizer ready output bytes。
- [ ] 更新 `SKILL.md`、package contract、workflow/data/companion/quality contracts 与 README。

## 2. Package-local runtime

- [ ] 建立唯一 reviewed merge message builder/validator，覆盖中文 summary、exact subject、fixed body、PR/Issue refs 与 close-keyword 拒绝。
- [ ] 扩展 semantic recorder/checker，绑定 message identity、live expected base head 和当前 input/facts。
- [ ] executor 写入 gitignored ephemeral body file，精确传递 `--subject`/`--body-file`，并在成功、失败与 recovery 后清理。
- [ ] post-merge verifier 回读 commit message、双 parents、remote base identity、PR 和 Issue closure。
- [ ] 保持三 typed exits、expected-head、merge method、零主动 Issue close、零 local main sync、零 task resource cleanup。

## 3. Tests 与 evals

- [ ] package contract/runtime tests：正例、默认 GitHub subject、直接 PR title、错误 PR/Issue、非中文 summary、body 段落/refs/close keyword、stale head/base/message。
- [ ] executor tests：精确 argv、body bytes、symlink/residue guard、finally cleanup、terminal recovery 零重复 mutation。
- [ ] post-merge tests：SHA、parents、subject/body、remote base 与 closure timing。
- [ ] evals 覆盖三 exits 和 message-specific blockers；真实 public wrapper 必须消费 actual gate/result。
- [ ] installed closeout fake GitHub harness 支持 `--subject`/`--body-file` 并返回可验证 commit message/parents/ref。

## 4. Canonical 与 projection 同步

- [ ] 修改 canonical package/consumer/contracts/registry/preset sources。
- [ ] 运行 preset `apply.sh --repo .` 同步 dogfood 与所有声明平台。
- [ ] 运行 dogfood overlay drift、ownership、installed manifest/public graph/parity 检查。
- [ ] 清理并记录任何 `.new`/`.bak`；最终必须递归零 sidecar。

## 5. Docs SSOT

- [ ] 调用 RDT `task_impact_sync`，生成 #285 contribution 与 traceability。
- [ ] 记录 Architecture Baseline `no_change` 结论；若实现发现 ownership 变化，停止并重新澄清。
- [ ] 校对 public README、workflow README、data contracts、quality guidelines 与 actual runtime。

## 6. 验证命令

- [ ] `python3 -m unittest trellis.skills...guru-merge-task-pr` 对应 package tests。
- [ ] package/runtime/contract/eval 集成测试与 current production contract validation。
- [ ] preset Python tests、installed closeout tests、source ownership、dogfood overlay drift。
- [ ] `bash -n`、Python compile、JSON schema/examples validation、`git diff --check`、`task.py validate`。
- [ ] preset apply/reapply，代表性 clean throwaway install/update；不是 release-wide 全矩阵替代。
- [ ] 经独立 scoped side-effect gate 后，在隔离 GitHub repository 运行一次 live expected-head merge proof。

## 7. Phase 2 与收尾门禁

- [ ] `trellis-before-dev` 加载本计划与 spec entries 后启动 task。
- [ ] Trellis implement sub-agent 仅实现 approved scope；规划外观察先回主会话 qualification。
- [ ] Trellis check sub-agent 执行完整 scope check；主会话调用 `guru-check-task`，finding=0 才进入 commit。
- [ ] `guru-create-task-commit` 后执行独立 `guru-review-branch`，覆盖 `origin/main...HEAD` 完整 committed diff。
- [ ] Publication/Finalizer 仅关闭 #285；PR full merge gate 后只询问 `合并PR`。

## 8. 回滚点

- Active 2.0 selector/runtime 改动可作为一个工作提交回退；1.0 assets 保持原字节。
- live proof 使用隔离仓库，不触碰 `castbox/guru-trellis` rules/history；失败保留证据并停止，不用历史重写修复。
