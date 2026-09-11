# #397 技术设计

## 单一 Owner

修改 `trellis/skills/guru-team/packages/guru-reconcile-task-base/runtime/common.py`
中的 `index_tree_digest`，不新增 helper owner、dispatcher、command、schema 或工作流边。
`execute.candidate`、`execute.reconcile` 和当前 receipt 校验继续调用同一函数。
候选表示的合同仍属于 Reconcile。Branch Review 自己的 committed-tree reader 必须消费同一
表示；在其既有 `tree_identity` 中补齐 gitlink，不跨包导入另一 owner 的 private runtime。

## Entry 计算

保持现有 `git ls-files --stage -z`、NUL-safe 路径解析、stage-0 检查及顺序。
仅在 mode 为 `160000` 时使用以下行表示：

```text
path_bytes + NUL + "160000" + NUL + index_oid_ascii + NUL
```

该分支不执行 `cat-file`，不解析子模块工作树，不要求父仓或子模块对象库具有该 commit。
索引 OID 是父仓已记录的版本事实，不承担人类确认或语义门禁职责。

其它 mode 保持现有 blob 读取、失败行为及行表示：

```text
path_bytes + NUL + sha256(blob_bytes).hexdigest() + NUL
```

总摘要继续为顺序拼接各行后的 SHA-256。普通文件 `100644`、可执行文件 `100755`、
符号链接 `120000` 不变；符号链接读取 Git blob 中的链接目标，不追踪文件系统目标。
gitlink 行显式携带类型和完整 OID，不忽略指针，也不伪装为 blob 内容。

## 已提交树 Consumer

`guru-review-branch/runtime/common.py` 的 `tree_identity` 使用 `git ls-tree -r -z`
读取已提交树。在 mode `160000`、type `commit` 时，以该 entry 的 path 和 OID 生成上述
gitlink 行；其余 blob 行、Git 顺序、读取失败行为和最终 SHA-256 保持不变。
不再跳过合法 gitlink，也不移除 recorder/checker 的原有摘要比较。
这是既有 consumer 对同一表示的承接，不新增共享 helper、schema、route 或第二算法版本。

## 兼容与短期证据

选择原位直接修复，不选择全量摘要重写、算法版本字段、旧算法 fallback 或双读。
无 gitlink 树的输入行完全不变，既有摘要和 consumer 无需迁移。
含 gitlink 的旧路径在生成 candidate result 前失败，因此没有这类合法成功摘要需要承接。
失败尝试在更新后的完整 preset/runtime 上重新执行 candidate；不从历史错误记录补造 token。
更新发生在 candidate 与持久整合之间时，受管副本一致性与原有 live tree 比较继续校验。

未改变 blob-backed entry 的 mode-only 摘要区分能力；不借此次修复扩展该既有语义。
新增行分支不使任何既有入口弃用，不产生需要保留的 legacy consumer。

## 验证设计

- 使用真实父仓与独立子仓提交生成 gitlink，父仓不导入子仓对象，子模块保持未初始化。
- 从旧提交执行同一候选样本得到原始失败，再对修复后的同一样本执行验证命令并读取 marker。
- 正常更新 gitlink OID，比较重复计算稳定性与指针改变后的差异。
- 既有普通、可执行、符号链接 fixture 与旧行算法作字节一致性比较，并验证内容变更敏感性。
- 在既有 feature/new-base fixture 中同时包含 gitlink 和不冲突改动，验证 candidate 与真实
  reconciliation commit 身份一致、父提交顺序正确。
- 将实际 Reconcile `review_continuity_required` 输出投影给 Branch Review，执行真实
  recorder、checker 和 public invoke，断言 `continuity_passed` 及当前提交身份。
  修复前同一 fixture 必须复现 `candidate_tree_sha256` 不一致；修复后不得改写 producer token。
- candidate 成功、验证命令非零退出、旧缺陷失败均比较 HEAD、原始 index 字节、refs、worktree
  注册和临时目录清理。验证非零退出只是结果记录，不改写为成功。
- canonical、dogfood 与一次代表性干净 preset 安装通过各自真实候选入口；不调用完整 Release verifier。

## Architecture 与分发

遵从 `docs/architecture/README.md` 的 current authority、
`docs/architecture/00-foundation/design-constitution.md` 与
`docs/architecture/06-governance/change-contract.md`。
预期为 `no_architecture_impact`：不改变语义 owner、domain、公共接口、持久化或跨层调用关系。
正式 Planning stage 结果由 Architecture owner 在本轮产生，不以本段代替。

canonical package 与测试是源码；`.trellis/guru-team/skills/packages/` 是安装投影。
通过 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 更新受管副本，按 installer
输出逐一核对 `.new/.bak`，保留无关用户变更。通用平台入口不需要改写。

## 风险

主要风险是旧 blob 分支被无意改写、pointer 未进入摘要、测试只证明 helper 而未到达真实
validation loop，以及手工更新安装副本造成漂移。上述风险由 R1-R7 对应测试覆盖。
生产业务效果、业务仓升级与完整多平台兼容性仍为未验证边界。
