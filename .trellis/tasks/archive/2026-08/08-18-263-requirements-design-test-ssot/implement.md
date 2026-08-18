# 实施计划：#263

## 交付顺序

1. 以 #264 package、当前 Registry 1.4、skill-package contract 和 live workflow 为先例，冻结 #263 的四 profile、五 exit、consumer id、authority/contribution/traceability contract。
2. 建立 canonical `guru-maintain-requirements-design-test-ssot` package：SKILL/contract/interface/commands、profile input/output/consumer schemas、error、examples、semantic owner result recorder/checker/invoke runtime、tests 与 evals。
3. 注册 active package 并更新 canonical registry、extension/current inventory、source validators/eval fixtures；以 live 集合为 authority把目标收敛为 20 active、71 command、20 complete、85 package exit，不从陈旧固定计数递增；确保新增字段均有 direct consumer，不引入 private lookup 或 aggregate authoring artifact。
4. 接入 canonical workflow 的 mandatory marker、五个唯一 route、三个 workflow router 和一个 stop target，使 business workflow 收敛为 19 invoke、83 exit、31 target、20 stop target。既有 Planning/Check/Branch Review/Publication/Finish 继续重读 live authority；只有直接消费确实需要新增 DTO 字段时才发布 versioned contract，不原地改变旧 schema，并引用 #264 public baseline contract。
5. 更新 preset managed/ownership inventory、README 与 source package validation；运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 同步 dogfood/installed/Agents/Codex/Claude/Cursor 投影，逐项处理任何 `.new/.bak`。
6. 补齐 package、registry、workflow、consumer、parallel contribution、provenance、traceability、subtraction 和 Architecture inheritance 定向测试与 eval。
7. 运行 Phase 2 最小可靠验证：本次变更触及的 Python tests、schema/registry/extension validation、workflow marker/consumer graph、platform parity、preset reapply、dogfood drift、recursive `.new/.bak`、script mode。
8. 运行且只运行一个代表性 clean throwaway，验证当前 source preset 安装、package inventory、workflow entry 与公开 runtime；明确记录 #260/#267 deferred matrix。
9. 对完整 `origin/main...HEAD` 做 Branch Review，复核 Issue #263 scope、公共 API、所有既有 atomic capability、Docs SSOT subtraction 与验证边界。

## 受控文件分区

- `trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/`：唯一 canonical package source。
- `trellis/skills/guru-team/` 与 `.trellis/guru-team/`：registry、extension、current inventory、installed package projection。
- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`：mandatory invoke、typed exits 和薄 consumer routing。
- `trellis/presets/guru-team/`：managed/ownership inventory、installer/readme/validation source。
- `.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/`：由 apply 同步的平台投影。
- 现有 Planning/Check/Review/Publication/Finish packages：仅做 #263 必需的最小 versioned consumer 接入，不重构无关行为。
- `.trellis/tasks/08-18-263-requirements-design-test-ssot/`：task-local planning、ledger 与执行记录；不是公共 SSOT。

## 验证命令计划

具体命令在 `trellis-before-dev` 与 live affected-file scan 后收敛，并覆盖以下固定类别：

```bash
python3 -m unittest <new-package-contract-tests>
python3 <registry/interface/extension validators>
python3 <affected Planning/Check/Review/Publication/Finish tests>
trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill guru-maintain-requirements-design-test-ssot --adapter shared --json
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
find . -type f \( -name '*.new' -o -name '*.bak' \)
git diff --check
```

代表性 clean throwaway 使用仓库当前 source/preset 的单一平台路径；不得调用完整 `verify-throwaway-install.sh` multi-platform matrix 模式，除非该脚本提供明确的单代表性 profile 且不会隐式扩张范围。

## 风险与回滚点

- 公共 skill/profile/schema/exit/consumer id 是 API；任何不兼容变化必须新版本化，不能靠同步副本掩盖。
- apply 会批量同步 generated projections；执行前后都检查 worktree diff，仅保留 #263 scoped files，并逐项处理 `.new/.bak`。
- consumer graph 改动以 #263 前 live 19-skill/80-exit baseline 为起点，并收敛到 #263 当前 20-skill/85-exit target closure；必须同时验证 canonical、installed、workflow 和平台 projection，不以 package 单测替代集成证据。
- throwaway 只证明当前版本代表性安装，不宣称完整平台、upgrade 或 release readiness。
- 不提交、push、创建 PR、merge、release 或 cleanup，直到各自后续语义门禁与用户确认。

## Task activation 前检查

- [ ] `prd.md` 完成 convergence pass，无重复事实或未决产品问题。
- [ ] `design.md` 明确 contribution boundary、四 profile、五 exit、consumer 与 #264 inheritance。
- [ ] `implement.md` 明确 canonical/generated ownership、定向验证与单一 throwaway 边界。
- [ ] planning wording review 无 contract violation。
- [ ] `guru-approve-task-plan` 对 requirement/design/implementation/docs SSOT/provenance/unusual scenarios 全部通过。
- [ ] sub-agent workflow 的 `implement.jsonl` 与 `check.jsonl` 各有真实 task-scoped entry。
