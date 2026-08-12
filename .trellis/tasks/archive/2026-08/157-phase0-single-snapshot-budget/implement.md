# 实施计划

## Phase 0：基线测量

- [ ] 枚举六个 package 的 record/check/invoke/execute live-call graph，标出 invocation、authority 和 mutation boundary。
- [ ] 扩展 fake harness 的结构化 operation counters，先提交 current behavior 的 deterministic before baseline。
- [ ] 覆盖 open issue、duplicate 空/非空、retain/select/retarget、authority mutation、wording changed、base changed、draft rebind、workspace mutation 和 standalone/workflow 场景。
- [ ] 根据基线列出实际受影响 package；未复现重复调用的 package 不做结构性改造。

## Phase 1：Package 内 validation 收敛

- [ ] 为实际受影响 package 建立 invocation-local immutable snapshot/validation context。
- [ ] 收敛 recorder/checker/public serializer 相邻重复验证；serializer 对 exact checked result 新增 live calls 必须为 0。
- [ ] 为旧 snapshot/receipt 增加 result/prerequisite/authority identity 变化拒绝测试。
- [ ] 保持独立 CLI 调用、workflow invocation 和 standalone invocation 的 entry/freshness 语义一致。

## Phase 2：跨 Skill duplicate 与 readiness

- [ ] 设计并迁移 Discovery -> Clarification 最小 duplicate snapshot public projection。
- [ ] 更新 producer output、consumer input、interfaces、schemas、examples、evals、tests 和唯一 consumer mapping。
- [ ] 让 Clarification current path 复用 projection，使 `discover -> clarify` search 总数等于 1；所有 refresh 原因走显式 route。
- [ ] 将 readiness target/comments/prerequisite validation 收敛到同一 invocation-local snapshot。
- [ ] 增加 dependency-aware invalidation matrix，验证 representation-only change 不触发全链重审，真实 authority change 定向失效。

## Phase 3：Workspace boundary 与合同文档

- [ ] 先用 Phase 0 counter 验证 workspace recorder/checker/serializer；只有计数证明存在相邻重复验证时才收敛该路径。
- [ ] 保留首次业务写入前单一 authoritative mutation-boundary recheck，断言 unchanged=1、changed=1 且零业务写入。
- [ ] 更新各 package `references/contract.md` 及受影响的 workflow/preset/docs SSOT。
- [ ] 检查 stable Skill id、external exit id、schema id 和 consumer projection 的兼容迁移，没有 silent break。

## Phase 4：Canonical 与分发同步

- [ ] 先完成 `trellis/skills/guru-team/**` canonical 变更。
- [ ] 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 同步 dogfood。
- [ ] 核对 `.agents/skills/`、`.codex/skills/`、Claude、Cursor 和 shared destinations。
- [ ] 运行 dogfood overlay drift 与 source/installed contract parity 验证，逐个处理 `.new` / `.bak`。

## Phase 5：验证

- [ ] 运行所有受影响 package-local unit/contract/eval tests。
- [ ] 运行 public-only Phase 0 integration transcript 和 before/after call-count ceilings。
- [ ] 运行 Python compile、JSON schema/index、shell syntax、task validate 和 `git diff --check`。
- [ ] 在 clean throwaway repo 验证 marketplace install/preview/switch、preset install、完整 Phase 0 transcript 和声明平台入口。
- [ ] 在 existing repo 验证 update/reapply、managed provenance、本地修改保护与零未处理 sidecar。
- [ ] 调用 `guru-check-task`，由独立 Trellis check 子代理审查完整 task scope、semantic/freshness 不回退和测试充分性。

## 关键验证命令

```bash
python3 -m json.tool trellis/index.json
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/157-phase0-single-snapshot-budget
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

完整测试命令由 Phase 0 基线确认受影响 package 后补齐到实施证据；不得用少量 targeted tests 代替 clean install/update/reapply 门禁。

## 风险文件与回滚点

- `trellis/skills/guru-team/packages/*/schemas` 与 `interface.json`：公共 API 迁移必须 producer/consumer 同步。
- `trellis/skills/guru-team/packages/*/runtime`：不得把 semantic route 判断移入脚本。
- `trellis/skills/guru-team/adapters/eval/native_adapter.py` 与 Phase 0 transcript：counter 必须记录规范化 operation，不能依赖 wall-clock。
- preset installer/manifest/platform projection：canonical 更新后必须重装验证，不能手改安装副本收口。
- workspace executor：任何优化都不能跨过 mutation-boundary fresh recheck。
