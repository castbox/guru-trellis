# 实施计划

## 实施顺序

1. 重新读取 canonical 与 dogfood source records，确认当前 commit/parents/tree/CI/CLI/package-manager 身份未漂移。
2. 精确更新 `README.md` 的 current source candidate、发布身份表 commit 与 CI。
3. 精确更新 `trellis/workflows/guru-team/README.md` 中所有 current source commit/CI 声明。
4. 精确更新 `trellis/presets/guru-team/README.md` 中所有 current source commit/CI 声明。
5. 在 `trellis/presets/guru-team/scripts/python/test_fork_preparation.py` 增加三份 README 映射一致性测试；期望 commit/CI 从 canonical source lock 读取，旧 CI 只作为退出断言。
6. 修正同文件 stale-build fixture：临时 Fork 新 commit 后同步 fixture lock 的 full commit、ordered parents 与 tree，使测试到达原有 stale-build marker 断言。
7. 检查完整 diff，确认未修改 source lock、manifest、schema、installer、validator、版本轴或 #410 candidate。

## 定向验证

```bash
python3 trellis/presets/guru-team/scripts/python/test_fork_preparation.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
cmp trellis/presets/guru-team/source/trellis-source.json .trellis/guru-team/trellis-source.json
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
find . -type f \( -name '*.new' -o -name '*.bak' -o -name '*.pyc' -o -name '*.pyo' \) -print
find . -type d -name '__pycache__' -print
```

若 repository-managed Python wrapper 对验证命令有专用入口，执行时使用当前 package 合同声明的 wrapper，不安装或修改全局 Python/npm。

## Phase 2 检查范围

- 需求：三个 README current identity 与 canonical source lock 一致。
- 设计：source lock 继续为唯一 authority，不新增平行配置或生成路径。
- 测试：新增断言覆盖三份文档，现有 source/installed projection 与 preparation 行为通过。
- 兼容性：版本轴、安装命令、managed assets、平台投影与 upstream ownership 不变。
- 安全与部署：无 secret、配置、CI/CD、容器、K8s、数据库 migration 或生产部署影响。

## 提交与发布边界

- 只 stage 本任务四个预期文件及 Trellis task artifacts。
- task commit 后对完整 `origin/main...HEAD` 执行独立 Branch Review。
- PR 标题和正文使用中文；PR 关闭 #426，并使用 `Refs #410` 引用正式发布 Issue。
- PR 合并后停止 #426 delivery 流程；#410 从新的 `origin/main` 创建全新 exact candidate 并从零重跑 Stage 2。
- 本任务不创建 tag、GitHub Release，不关闭 #410，不执行 cleanup。

## 停止条件

出现以下任一情况立即停止并重新进入对应 owner：

- canonical source identity 再次变化；
- 需要修改 manifest、schema、installer、source lock 或公共 API；
- preset reapply 产生未预期 managed bytes 或 sidecar；
- 任一定向验证失败且根因不属于本任务范围；
- Branch Review 出现任何未解决 P0-P3 finding。
