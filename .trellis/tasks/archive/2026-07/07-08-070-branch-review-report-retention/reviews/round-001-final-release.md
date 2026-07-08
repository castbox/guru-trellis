# Issue #70 Branch Review Gate 最终放行审查原始报告

## 审查身份

- 审查角色：最终放行审查代理
- agent_id：`019f3fd7-da1e-7b81-96df-ca19846d3797`
- 审查 HEAD：`fa7d0574230f6773dc319af604929f9cb17b2cfa`
- Diff 范围：`origin/main...HEAD`
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/070-branch-review-report-retention`
- 结论：不放行，发现 1 个 current-scope P3 finding。

## 审查范围

已按 `origin/main...HEAD` 完整 diff 审查 41 个变更文件，覆盖 docs、Trellis task artifacts、workflow、平台入口 overlay、companion Python 脚本、bash 脚本语法、测试、preset README、dogfood installed copies、配置 / manifest、schema / config 影响、CI/CD、Docker/Compose、K8s/Kustomize、DB migration、Makefile 与部署影响边界。

重点核对 issue #70 acceptance：

- 每轮原始 review 报告保留在 task-local `reviews/*.md`。
- 最终 `review.md` 作为汇总入口，链接每轮原始报告。
- `agent-assignment.json.review_rounds[]` 记录原始报告 path、sha256、size、modified_at、round、role、agent、HEAD、finding count。
- `review-gate.json.verification_evidence.review_reports[]` 从 assignment rounds 汇总原始报告 digest。
- pass path 校验汇总入口链接所有原始报告。
- findings path 要求 current HEAD、matching findings_count、agent assignment 和原始报告 evidence。
- archive migration 支持 `reviews/*.md` nested digest path。
- metadata-only tail 接受 `reviews/*.md`，但不放宽 source / config / script / docs / schema / preset 变更。
- #61 顶层 artifact 表边界：默认仍列顶层 human artifact `review.md`，原始报告通过汇总入口和 gate digest 追溯。
- recorder / validator 边界：脚本只校验 path / digest / HEAD / round / finding count / status-event completeness，不替代 AI review 语义判断。

## 运行命令与结果

- `python3 ./.trellis/scripts/get_context.py`：通过，读取 Trellis context。
- `python3 ./.trellis/scripts/get_context.py --mode phase`：通过，确认当前 phase context。
- `python3 ./.trellis/scripts/get_context.py --mode packages`：通过，列出 fallback specs。
- `git fetch origin main`：通过。
- `git rev-parse HEAD`：返回 `fa7d0574230f6773dc319af604929f9cb17b2cfa`。
- `git diff --name-status origin/main...HEAD`：通过，41 个变更文件。
- `git diff --stat origin/main...HEAD`：通过，1704 insertions / 194 deletions。
- `git diff --check origin/main...HEAD`：通过。
- `cmp trellis/workflows/guru-team/scripts/python/guru_team_trellis.py .trellis/guru-team/scripts/python/guru_team_trellis.py`：通过，canonical 与 dogfood Python helper 一致。
- `cmp trellis/workflows/guru-team/workflow.md .trellis/workflow.md`：通过，canonical 与 dogfood workflow 一致。
- `find . -name '*.new' -o -name '*.bak'`：通过，未发现 `.new` / `.bak`。
- `bash -n ...`：通过，已对非禁止的 canonical / dogfood / preset bash scripts 做语法检查。审查中曾误执行一次 `bash -n trellis/workflows/guru-team/scripts/bash/check-review-gate.sh`，仅做 shell 语法解析，未执行脚本逻辑、未写 artifact；该命令不作为 gate evidence。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`：通过。
- `python3 -m unittest discover -s trellis/workflows/guru-team/scripts/python -p 'test_*.py'`：通过，Ran 149 tests OK。
- `python3 -m json.tool trellis/index.json`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-08-070-branch-review-report-retention`：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过，dogfood overlay copies match canonical Guru Team overlays。

未运行被禁止的 recorder / gate 执行路径：未执行 `review-branch.sh`、未执行 `record-agent-assignment.sh`、未执行任何 `record-*`，未提交、未 push、未创建 PR、未运行 finish-work。

## Docs SSOT 对齐

已同步的 SSOT：

- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` 记录原始报告、汇总入口、gate digest、metadata tail、archive migration、recorder / validator 边界和 #61 artifact 表边界。
- `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`docs/requirements/guru-team-trellis-flow.md` 已加入 issue #70 语义。
- `.agents`、`.codex`、`.claude`、`.cursor` 平台入口与 canonical preset overlays 已同步原始报告、review round digest、finish-work metadata tail 语义。

未同步的 durable docs SSOT：

- `docs/requirements/requirement-main.md` 仍保留旧语义，见下方 P3 finding。

## 部署与安全影响

本分支未修改 CI/CD、Docker/Compose、K8s/Kustomize/Helm、DB migration、Makefile 或运行时部署资产；无数据库迁移、容器镜像、集群配置或生产部署路径影响。变更主要影响本仓库 Guru Team Trellis workflow / preset / overlay / companion scripts 的本地 gate 行为与 task metadata 结构。

安全边界方面，新增 digest / path / mtime 记录不会引入 secret 输出；审查未发现 token、secret、private key、signed URL、`.env` 或客户数据泄露。脚本仍保持 recorder / validator 角色，没有把 AI 语义审查写入确定性脚本。

## 问题

### P3 - durable docs SSOT 漏同步 issue #70 原始报告 / 汇总语义

- 文件：`docs/requirements/requirement-main.md`
- 行号：38, 95-96, 108, 112, 187, 277
- 问题：该 durable requirements 主文档仍把 Phase 3 描述为独立 review sub-agent 产出 `review.md`，并把 `review.md` 描述为 AI / human review 判断的主证据、`review-branch.sh` 固化 review report digest。它没有同步 issue #70 的新合同：每轮原始报告必须保留在 `reviews/*.md`，顶层 `review.md` 只是最终汇总，`agent-assignment.json.review_rounds[]` 与 `review-gate.json.verification_evidence.review_reports[]` 追溯原始报告 digest。
- 影响：本分支其他 workflow / README / overlay / script / test 已切到原始报告 + 汇总语义，但 durable docs 主索引仍保留旧模型，会让后续 agent 或人类以长期 SSOT 为准时误以为唯一 `review.md` 仍是完整原始审查报告，削弱 issue #70 的“多轮原始报告不被覆盖”目标。
- 必要修复：同步 `docs/requirements/requirement-main.md` 的 Phase 3、P0 evidence chain 表、review gate recorder 描述、subagent 执行边界和 issue 索引，使其明确 `reviews/*.md` 原始报告、`review.md` 汇总、raw `review_reports[]` digest 与 #61 顶层 artifact 表边界。

## 观察项

- `trellis/workflows/guru-team/README.md:284` 仍有一句简写“输出 `review.md`”，但同一段前后已明确每轮 `reviews/*.md` 原始报告、最终 `review.md` 汇总、raw `review_reports[]` digest 与 archive 迁移；该点被上面的 durable docs SSOT finding 覆盖，不单独计为 finding。
- `.trellis/guru-team/extension.json` 的 source commit 指向安装 / 同步时的 `63936960...` 且 `tree_state=dirty`；dogfood overlay drift 和 canonical / dogfood copy 比对均通过，本轮未判定为阻断问题。

## 后续候选

- 后续可增加一个文档扫描测试或 review checklist，专门检查 durable docs 中 “Branch Review 只产出 review.md / review report” 这类旧语义是否残留。
- 后续可补充更精细的 README wording cleanup，将所有简写“输出 `review.md`”统一改成“输出 `reviews/*.md` 原始报告和最终 `review.md` 汇总”。

## 最终结论

不放行。代码、测试、workflow、overlay、dogfood 同步和命令验证整体满足 issue #70 的核心行为，但 durable docs SSOT `docs/requirements/requirement-main.md` 仍保留旧的唯一 `review.md` 语义，属于 current-scope P3 finding。主会话应把该 finding 交回修复 / 闭环后，再由同一问题发现代理复审闭环，并重新派发 fresh 最终放行审查代理。
