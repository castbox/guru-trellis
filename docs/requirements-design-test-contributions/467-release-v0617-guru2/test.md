# #467 发布准备测试增量

- `T467-01`：覆盖无关旧 checkout artifact、无关 malformed branch artifact、
  无关旧 ledger 均不阻塞创建，以及目标身份和 ledger 冲突继续阻塞。
- `T467-02`：验证 manifest 与当前文档四轴一致，canonical/installed runtime、
  Shared/Codex/Claude/Cursor 投影、preset reapply、ownership 和 drift。
- `T467-03`：pre-promotion 与 post-promotion 分别执行 Phase 2、Task Commit
  和完整 `origin/main...HEAD` Branch Review；PR 为中文 Refs-only。
- `T467-04`：合并和 Finish 后以单一 exact candidate 运行发布合同的
  predecessor full diff、版本轴、source/installed、投影、focused
  clean install/update/reapply、Fork build、真实 changed-file secret scan
  与 residue 检查。FAIL/SKIP 阻塞 tag。
- `T467-05`：tag 指向同一 candidate；tag-pinned smoke 通过后发布
  GitHub Release，复核 live Issue 后独立关闭。完整多平台矩阵未验证。
- `T467-06`：从 `v0.6.17-guru.1` 安装一个既有项目，再以 exact candidate
  升级并 reapply；核对退役 Skill、命令、package 文件和投影均已删除，
  本地修改冲突与 sidecar 按现有 installer 合同阻断。
