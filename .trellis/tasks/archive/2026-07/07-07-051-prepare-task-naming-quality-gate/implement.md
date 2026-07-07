# #51 实施计划

## 步骤

1. 定位并修改 canonical prepare 实现：
   - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
   - 新增命名质量 helper 与 executor 阻断。
   - 保持只读 prepare 无 GitHub / filesystem 副作用。

2. 更新 payload/schema/docs：
   - `trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
   - `trellis/workflows/guru-team/workflow.md`
   - `trellis/workflows/guru-team/README.md`
   - `trellis/presets/guru-team/README.md`
   - `README.md`

3. 补充回归测试：
   - `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
   - 覆盖英文自动命名、中文只读标记、中文 create 阻断、语义覆盖通过、低信息覆盖阻断。

4. 同步安装副本：
   - 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
   - 检查并处理 `.bak` / `.new`
   - 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`

5. 运行验证：
   - `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`
   - `python3 -m json.tool trellis/index.json`
   - `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
   - `python3 -m json.tool .trellis/guru-team/schemas/intake-handoff.schema.json`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-07-051-prepare-task-naming-quality-gate`
   - `git diff --check`

6. 最小 CLI 验证：
   - 中文 issue planner JSON 标记 `naming_quality.ok=false`。
   - 中文 issue create 路径返回 exit 2，未创建低信息 worktree/task。
   - 显式语义覆盖 planner/create dry path 生成目标名称。

## 规划审批前自检

- 已读 issue #51、用户原始需求、本仓库 workflow specs 和 official Trellis 扩展文档。
- 本任务不涉及 middle-platform 知识库。
- 本任务会改变长期可复用 workflow / preset 行为，必须同步 canonical 与 dogfood 副本。
- 本任务会新增 payload 字段，必须更新 schema 和测试。
