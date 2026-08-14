# 技术设计

## 单一 locator

`bootstrap.py` 拥有路径计算的确定性实现：

- user cache root：支持测试专用显式override；否则按平台选择
  `~/Library/Caches/guru-team/python`、`${XDG_CACHE_HOME:-~/.cache}/guru-team/python`
  或 `%LOCALAPPDATA%/GuruTeam/python`。
- repository state root：直接只读解析 checkout 的 `.git` directory，或 linked
  worktree `.git` 文件指向的 gitdir 及其 `commondir`；不依赖 PATH 中存在 `git`。
  主 checkout 在 `<common-dir>/guru-team/python/active.json` 写默认 pointer；新
  linked checkout 在未 apply 时继承该默认值，apply 后在自身 worktree gitdir
  下写 override pointer，解析时优先使用 override。
- runtime root：`<user-cache>/<runtime-id>/`，包含 `venv/` 与 `metadata.json`。

pointer记录runtime identity和本机managed interpreter绝对路径；default与override均位于
Git common-dir管理的私有状态树，不得进入tracked manifest或公共DTO。shell resolver在PATH
没有Python或git时直接解析同一Git metadata，按当前checkout选择override或default并执行该
interpreter，再由bootstrap以相同的无git locator完成identity/probe复核。venv仍然只按
OS用户与完整identity创建，pointer隔离不会创建per-checkout venv。

## Identity

在#219已有字段上增加：

- `os_name`
- `machine`
- `python_abi_tag`
- `python_platform_tag`

identity经canonical JSON计算24位SHA-256前缀。新字段改变既有identity，旧venv不会被错误复用。

## 安装与迁移

bootstrap先计算新identity和目标cache路径。目标已通过metadata与Draft 2020-12 probe时直接复用；
损坏目标按既有candidate/repair-backup语义重建。成功probe后才更新common-dir pointer。

旧repo-local venv不进行路径复制，因为venv可能包含绝对interpreter路径或script shebang，
跨目录复用不具备可移植性。迁移通过构建或复用新完整identity的user-cache、完成metadata与
probe验证后再切换common-dir pointer实现；旧目录不删除，切换失败时旧目录与原pointer均不受影响。

## Resolver与错误

shell resolver先以POSIX基础工具解析pointer和interpreter，再通过bootstrap的只读validate入口
复核同一locator；validator失败时原样转发其single-JSON stderr，不得泛化为依赖缺失。错误分类至少区分：

- `runtime_not_bootstrapped`：无common-dir pointer。
- `managed_runtime_missing`：pointer存在但cache runtime缺失或不可执行。
- `runtime_dependency_missing`：runtime存在但capability probe失败。

所有错误保持single JSON stderr、无traceback，并给出preset repair命令。

验证器创建新的Git owner-repo fixture时，必须通过已安装bootstrap为该repository激活同一
user-cache runtime并写common-dir pointer；不得复制venv或依赖其它checkout的私有pointer。

Runtime unit test harness必须在独立临时repository中执行bootstrap，不能在测试专用cache
override生效时改写被测source checkout的pointer。只有明确测试source checkout wrapper的
subprocess移除该override并使用真实已激活user cache；suite验收同时比较caller pointer执行
前后bytes相等，避免临时cache清理后留下stale interpreter。

## 同步面

canonical runtime、workflow managed copy、dogfood installed copy和installer调用必须同步。
公共README与workflow/preset spec更新ownership说明。manifest revision留给#222在新candidate上分配。
