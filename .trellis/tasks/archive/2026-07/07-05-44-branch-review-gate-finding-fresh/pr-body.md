## 变更摘要

- 收紧 Guru Team Branch Review Gate：任意 `finding` 都阻断通过，包括 P3；`observation` 和 `followup_candidate` 只能作为非阻断记录，不能替代当前 scope defect。
- 强制通过态 gate 绑定 task-local `agent-assignment.json` 与 `review.md` digest，校验 review round 唯一递增、finding owner later same-agent closure、fresh final reviewer、当前 HEAD 和 0 findings。
- 修正用户指出的 reviewer 职责边界：finding owner closure 只证明自己的 finding 已关闭，不要求每个后续 HEAD 重跑；fresh final reviewer 负责当前 HEAD 完整 diff；独立 review subagent 不调用 Guru Team recorder/validator 扩展脚本。
- 补齐归档后 publish recovery：归档 task 成为新的 task-local 边界，validator 可只读接受 pre-archive active task path 的 digest entry，finish/publish recovery 只迁移路径与 digest 元数据并提交 Trellis metadata。
- 同步 canonical workflow、dogfood workflow、preset overlay、平台 continue 入口、README、requirements 与 `.trellis/spec/workflow/*`，避免不同入口继续传播旧 gate 语义。

## 影响范围

- 影响 Guru Team workflow / preset / dogfood 安装副本：`trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`、`trellis/presets/guru-team/overlays/**`、`.agents`、`.codex`、`.cursor`、`.claude` continue 入口。
- 影响 companion script：`guru_team_trellis.py` 的 Branch Review Gate recorder/validator、agent-assignment 校验、review report digest 校验、follow-up/observation 记录和归档后 gate publish recovery。
- 影响测试：`test_guru_team_trellis.py` 覆盖任意 finding 阻断、bool findings_count fail-closed、closure-before-final、fresh final reviewer、review report digest stale、round 唯一递增、archived gate active-path digest 兼容和 finish-work 归档后迁移等路径。
- 影响文档与规范：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`docs/requirements/requirement-main.md`、`.trellis/spec/workflow/*` 和 `.trellis/spec/preset/overlay-guidelines.md`。
- 不涉及应用运行时部署资产：未修改 GitHub Actions、Docker/Compose、K8s/Helm/Kustomize、数据库 migration/schema/seed/backfill 或 Makefile。

## 验证结果

- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：126 tests OK。
- `PYTHONPYCACHEPREFIX=/tmp/guru-trellis-pycache python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py .trellis/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m json.tool trellis/index.json`、schema 与 `.trellis/guru-team/extension.json`：通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`：通过。
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms` 与 `check-dogfood-overlay-drift.sh`：通过，无 `.bak` / `.new` 遗留。
- `git diff --check origin/main...HEAD && git diff --check`、`task.py validate`：通过。

## Review Gate

- 当前最新审查 HEAD：`2b742d8714e7b7ff1502b16bca6c82fcce25c969`。
- Fresh final reviewer 将在 publish 前记录到 task-local `review.md`、`agent-assignment.json` 和 `review-gate.json`；review evidence 必须明确 reviewer 未调用 `review-branch.sh`、`check-review-gate.sh`、`record-agent-assignment.sh` 或 `record-*` 扩展脚本，主会话只在 review 完成后运行 recorder/validator。
- `check-review-gate.sh --json --allow-metadata-after-gate` 必须在最终 gate 记录后校验当前 HEAD 与 review gate 一致。

## Issue 关闭范围

- Closes #44。
- 无 related issues。
- 无 follow-up issues。

## 安全说明

- 本次变更不读取、不输出、不持久化 token、secret、private key、`.env`、数据库 URL、签名 URL 或客户数据。
- 新增和更新的 artifact 只记录 reviewer identity、diff range、hash/digest、验证命令与 gate 结论。
- 不修改 CI/CD、容器、K8s、数据库 migration 或 Makefile；无需部署侧同步。
