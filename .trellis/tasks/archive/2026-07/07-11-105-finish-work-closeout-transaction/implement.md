# Issue #105 实施计划

## 1. Phase 1 门禁

- [ ] 主会话完成 `prd.md`、`design.md`、`implement.md` 需求歧义、状态机完整性与AI/script边界审核。
- [ ] 主会话展示三份规划文档链接，用户给出独立post-planning approval。
- [ ] recorder写入并校验schema 1.2 `planning-approval.json`。
- [ ] `implement.jsonl` 与 `check.jsonl` 写入真实spec上下文。
- [ ] `task.py start` 把task切换到 `in_progress` 后才派发实现sub-agent。

## 2. Durable SSOT 先行

- [ ] 更新 `.trellis/spec/workflow/companion-scripts.md`，固化prepare、state machine、draft handshake、archive transaction与单入口恢复。
- [ ] 更新 `.trellis/spec/workflow/data-contracts.md`，固化closeout plan、digest、pending/passed evidence与final summary projection。
- [ ] 更新 `.trellis/spec/workflow/workflow-contract.md`，替换archive-first与post-PR metadata tail顺序。
- [ ] 检查 `.trellis/spec/workflow/quality-guidelines.md` 与 `.trellis/spec/preset/installer.md`，同步受影响的验证和安装合同。
- [ ] 更新 `docs/requirements/guru-team-trellis-flow.md` 的durable流程说明。

## 3. Closeout plan 与 prepare

- [ ] 新增 `closeout-plan.schema.json` 及canonical/dogfood安装清单。
- [ ] 实现plan canonicalization、digest、schema/Python validator和安全字段检查。
- [ ] 抽取 `prepare_closeout()`，让dry-run与formal调用同一完整local pipeline。
- [ ] 新增 `--expected-plan-digest` formal handshake；formal protected input漂移在push前失败。
- [ ] 首次formal写入canonical `closeout-plan.json`；重试加载committed plan/readiness并验证唯一后继状态。
- [ ] dry-run payload输出plan、digest、future archive mapping、metadata allowlist与每段动作，不写文件或远端状态。
- [ ] 实现temporary future archive projection与artifact/path cross-validation。

## 4. Marketplace evidence 与 readiness

- [ ] 把pending machine evidence生成从AI artifact编辑移到deterministic recorder。
- [ ] 把semantic reason从machine identity中分离，保留AI scope/evidence判断。
- [ ] content push后把canonical pending写入active ledger；verifier成功后只替换为passed，失败时保留active pending供同一entry恢复。
- [ ] required verifier绑定reviewed work HEAD并在archive前执行。
- [ ] 把passed verifier artifact、ledger evidence与immutable readiness纳入exact metadata commit/push。
- [ ] not-required路径只写readiness并保持同一state transition输出。
- [ ] 补reason变化、machine字段缺失/篡改、stale HEAD、artifact digest mismatch负向测试。

## 5. Draft PR 与状态恢复

- [ ] formal create固定为draft PR。
- [ ] 实现repo/head/base唯一open PR查询: 0创建、1复用、多于1失败。
- [ ] 删除无生产调用者的 `resolve_closeout_state()`；状态识别由真实 active/archive recovery调用链中的stage-specific resolver承担。
- [ ] 移除normal path对 `--skip-archive` 与 `--recovery-after-finish-work` 的依赖。
- [ ] 兼容flags若保留则fail closed并返回同一finish entry提示。
- [ ] 所有重试从committed readiness与plan digest恢复，不接受title/body/base/draft override。

### 5.1 单一实现减法修复

- [ ] 把 `cmd_publish_pr()` 收敛为兼容性 fail-closed handler；保留command/wrapper路径，不保留第二套executor。
- [ ] 基于production call graph删除只服务旧 `cmd_publish_pr()` 的helper，目标覆盖旧PR body fallback、marketplace recorder/validator、recovery command、open PR recovery、summary URL rewrite与metadata tail commit。
- [ ] 删除手工构造`from_finish_work`/`recovery_after_finish_work`并直接调用dormant handler的测试，只保留真实parser/main兼容拒绝测试。
- [ ] 运行AST/`rg`检查，证明新增production top-level functions均有真实生产调用者或显式CLI handler。
- [ ] 记录删除前后canonical production/test/installed smoke numstat；installed smoke不得为降低行数而删除。

## 6. Final projection 与 archive transaction

- [ ] 取得PR URL后在active task构建final summary，保留#97 schema与#98 PR ref合同。
- [ ] 在temporary archive projection执行summary、ledger、gate、readiness、artifact、path和allowlist完整校验。
- [ ] final summary随官方 `task.py archive` move进入archive，不在archive后rewrite。
- [ ] archive commit只stage当前task active/archive metadata path。
- [ ] push archive commit并校验local/remote/draft PR三方HEAD。
- [ ] 三方HEAD相同后执行draft-to-ready；此后禁止repo mutation。
- [ ] archive move/commit/push与ready失败均由同一finish entry恢复。

## 7. Canonical workflow、preset 与平台同步

- [ ] 更新 `trellis/workflows/guru-team/workflow.md` 与workflow README。
- [ ] 更新preset README、canonical overlays、finish skill/commands/prompts。
- [ ] 检查 `.agents/skills/trellis-finish-work/`、`.codex/skills/trellis-finish-work/`、`.codex/prompts/`、`.claude/commands/trellis/`、`.cursor/commands/`。
- [ ] 更新schema/companion managed asset清单与extension manifest public contract。
- [ ] 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms` 同步dogfood。
- [ ] 处理全部sidecar并运行 `check-dogfood-overlay-drift.sh`。

## 8. Failure injection 与历史回归

- [ ] prepare validator失败: task active、无push、无PR。
- [ ] content push/remote identity失败: task active、无PR。
- [ ] verifier/evidence commit/evidence push失败: task active、无PR或draft不存在。
- [ ] draft create客户端失败但远端已创建: 下次唯一复用，不重复创建。
- [ ] final projection失败: task active、PR draft。
- [ ] archive move/commit/push失败: 同一entry恢复exact transaction。
- [ ] remote HEAD mismatch: PR保持draft，不转ready。
- [ ] draft-to-ready失败: archive与remote HEAD不变，只重试ready transition。
- [ ] 2026-07-03、2026-07-04与#100三类历史失败回归。
- [ ] 对每个case断言task locator、PR state、local/remote/PR head、dirty paths和next action。
- [ ] canonical closeout failure matrix继续只走 `cmd_finish_work()`；不得依赖已删除的legacy publish handler。
- [ ] installed initial/update smoke继续通过真实wrapper、parser、draft/archive/ready路径。

### Round 18 scope cap checklist

- [ ] exact committed archived recovery 在保留 task context 且 working-tree plan 缺失、篡改、symlink 或 invalid 时仍只消费 commit blob；incomplete/nonexact 状态继续 fail closed。
- [ ] 所有 formal workflow 示例携带 `--expected-plan-digest`，dry-run/preview 不被误判。
- [ ] official move 前校验 tracked bytes/mode、staged/dirty/untracked allowlist；漂移时 task 保持 active。
- [ ] archive month 不一致时 official move 前失败，同一入口必须生成新 digest 并重新 prepare；不实现跨月迁移。
- [ ] 非空或不可解析 `after_archive` hook 在 prepare 阶段失败；不执行或分析 hook。
- [ ] P1-1 review ledger 由主会话结构化重锚，并在不包含旧 commit object 的 `--no-local` fresh clone 中通过 assignment validator。

## 9. 验证命令

```bash
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-11-105-finish-work-closeout-transaction
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

- [ ] 运行`publish-pr.sh --json --dry-run`并断言在repo/task解析前固定fail closed，错误指向`trellis-finish-work`。
- [ ] 运行production AST call graph，确认无仅测试可达的新增函数与legacy publish专属闭包。
- [ ] 汇总`origin/main...HEAD -- trellis/`与本轮cleanup commit的numstat，说明production、test与installed smoke构成。

- [ ] 运行targeted plan/digest、ledger、draft handshake、final projection和failure injection tests。
- [ ] 运行full canonical Python suite与preset suite。
- [ ] 验证canonical/dogfood workflow、scripts、schema和platform entries一致。
- [ ] clean throwaway repo执行remote branch workflow/preset安装与完整closeout smoke。
- [ ] throwaway repo执行workflow preview/switch、`trellis update`、preset reapply与递归sidecar空扫描。
- [ ] 记录命令、exit code、关键计数与未验证风险。

## 10. Phase 2 Check、提交与 Branch Review

- [ ] 实现sub-agent完成代码与tests后，独立check sub-agent覆盖需求、设计、代码、tests、spec、Docs SSOT、安全、部署和安装升级。
- [ ] 主会话修复全部P0/P1/P2/P3 finding，同一checker复核闭环。
- [ ] recorder写入并校验 `phase2-check.json`，更新#105 acceptance evidence。
- [ ] 只stage #105范围文件，提交信息使用 `fix(workflow): #105 ...`。
- [ ] 独立Branch Review覆盖 `origin/main...HEAD` 完整diff，保留raw reports、agent ledger、rollup和gate。
- [ ] gate必须明确覆盖#105、durable docs、schema、preset/overlay、all-platform entry、failure matrix与throwaway/update证据。

## 11. Finish 与发布

- [ ] AI审查 `finish-summary-index.json`、中文PR title/body、Docs SSOT、安全和部署说明。
- [ ] Issue Scope Ledger只把#105放入 `close_issues`；#53/#96/#97/#100只引用，#98/#99/#101保持follow-up。
- [ ] `trellis-finish-work` dry-run输出canonical plan digest和active-task Markdown review表。
- [ ] formal传入expected digest，完成draft handshake、final projection、archive transaction和draft-to-ready。
- [ ] archive后解析Markdown review表，确认final PR URL、remote HEAD、clean tree和非draft状态。

## 12. 回滚点

- closeout plan/schema回滚必须与parser、validator、workflow和preset资产同时执行。
- draft PR创建后、archive前回滚时保持PR draft并记录失败阶段，不把draft转ready。
- archive transaction已push后不得通过新增metadata commit修改summary；修复必须新建独立issue与常规代码PR。
