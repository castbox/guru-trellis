# D1 实施计划

## 1. 输入和引用

读取整体 PRD、本批 PRD、design 第3节、发布合同 Stage 1、公开文档规则及匹配的源锁。准备基线为 `6825949699d342eba1ad018ee04a8f9396f11619`，本批没有前序。

## 2. 步骤和文件责任

1. 更新 `trellis/guru-team-extension.json` 的版本，并更新根、workflow 和 preset README 的安装目标和前驱身份。
2. 检查候选源码和受管平台投影。确认本批没有改变 marketplace registry 或 workflow 字节，然后运行匹配 Fork 的定向临时安装。
3. 执行 TaskCommit、固定 B..H、独立 Review、Publication 与 Merge。PR 使用 `Refs #924`。源码合并后由 Completion 转交 AC02。

## 3. 验证

- V1：运行 `trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`，并分别指定 `.agents/skills`、`.claude/skills`、`.cursor/skills` 的 `--platform-root`，核对实际声明投影。
- V2：将 `TRELLIS_FORK_SOURCE` 指向实际匹配源锁的干净构建，`TRELLIS_WORKFLOW_SOURCE` 指向 `gh:castbox/guru-trellis/trellis#6825949699d342eba1ad018ee04a8f9396f11619`。运行 `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh --mode focused --platform codex` 验证安装、update/reapply、受管入口和 sidecar。该证据用于 AC01。
- V3：核对三处公开说明、manifest 和版本轴，运行 `git diff --check`，确认所列安装命令及链接适用于当前来源。

## 4. 停止条件与恢复

源码检查或定向安装失败时调查原入口并修复后重新验证。若公开 workflow 或 registry 与远端准备基线不同，则该 SHA 不能用于本批 marketplace 验证，返回 Author 重新评估验证路径。D2 真实采用和发布候选阶段分别保留各自的恢复责任。

## 5. Delivery Policy

`staged`。当前为第一阶段，仅交付和验证 AC01。实际发布源码独立可安装并合并后结束当前批次。第二阶段交付 AC02 的真实受管安装采用。两批完成后由 Completion 和 Finish 履行 AC03。

## 6. Docs SSOT Plan

`no_docs_update_needed`。现有 RDT 和 ARCH-INT-009、014、015 保留发布与分发定义。本批仅更新版本清单和公开 README 的安装引用。公开说明由本批实施更新，由独立 Review 检查文档和真实候选的一致性。
