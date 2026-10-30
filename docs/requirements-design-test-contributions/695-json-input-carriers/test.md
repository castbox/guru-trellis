# #695 实际观察与验证边界

观察截止：本 Task 首次完整实施候选，已完成 source 和同 checkout tools-only 安装验证；正式 candidate Check 尚未执行。测试策略由 [完整 T695](proposed/docs/test/current/json-input-carriers.md) 定义；本文件是本项实际观察的唯一 Test 来源。

## 实施前观察

原 Bind wrapper 中 stdin {} 加双 - 返回 invalid_json/owner_result；zsh process substitution 返回 invalid_json/input。这些是缺陷诊断，不是完整合法 Bind 或业务成功。

## 源码与正常调用

- T695-01：经现有 managed Python 执行 shared `runtime/tests/test_io.py`，12 项通过。检查真实 reader/decoder 的普通文件优先、symlink、inline/stdin、长 inline 和错误分类；失败输出不含敏感示例值。
- T695-02：Bind 原 tests 17 项通过。首次运行缺 upstream fixture 路径而出现 setup errors；随后 live 核对 clean Fork `17015f987166f4106034f115d23212446f16d536`，显式指定其 `packages/cli/src/templates/trellis/scripts`，原套件通过，未改 fixture 或安装替代 runtime。
- T695-02：原 source invoke.sh 实际 zsh process substitution 返回 invalid_json/input/2 并说明 carrier unsupported；双 - 返回 conflicting_arguments/arguments.--owner-result/2。两者不进入 schema/身份写入。
- T695-02：在真实本 Task `695-json-input-carriers` generation 0/current session/implementing Delivery 下，原 Bind owner 完成 resume 判断后，通过 source wrapper 执行完整双普通文件及 stdin+inline。两次均 exit 0/session_resumed；前后公共 Delivery current key 一致，原 selection 保留。
- T695-03：Publish/Merge/Finish 原 legacy-maintenance 套件各 5 项通过，包含已读正文不重新探测文件；Finish 另验证 pre-read OSError/UnicodeError 转换为安全 invalid_json/input/2。原 qualifier stdin pipeline 与 Wording envelope 错误回归各 1 项通过；这些是定向准入证据，不声明全部 CLI 或远端生命周期通过。
- T695-04：canonical source package validator 返回 passed（40 active packages、125 commands）；Bind source --help 显示支持形式、双 - 限制及 conflicting_arguments。数量仅为输出定位，不作为充分性标准。
- T695-05：363 个 Guru Python 文件 in-memory syntax、trellis/index.json 解析、声明 Bash syntax、Task context validate 与 git diff --check 通过。Task validate 提醒部分 spec 超过注入字节上限；实施者已直接读取所需完整正文，不将截断注入视为充分加载。

新增 nonregular 测试的 FIFO fixture 仅在 `os.mkfifo` 可用时创建；所有平台仍执行目录载体断言。修正后同一 managed Python 的 shared reader 12 项及变更文件内存语法、diff hygiene 再次通过。官方 CPython 文档明确 mkfifo 仅 Unix 提供；这项源码适用性修正不宣称原生 Windows 已实际运行。

## 同 checkout 安装与采用

- plain `apply.sh --repo .` 实际 exit 1，code=upstream_delivery_migration_required；历史归档 preflight 阻止普通 apply，未声称其安装成功，未 bypass 或迁移无关历史。
- 原 tools-only owner 使用完整 dirty #695 canonical source 和匹配已有 CLI/Core .6 local_candidate build，返回 tools_upgraded，installed_version=0.7.0-guru.7，unverified=[formal_fork_source_lock]。准备阶段发现主 Fork checkout 的 dist 仍含旧 stop 模板，已排除该构建；实际使用 release checkout 07f31d83543581647ef7852d177c3dd16587049a 的已有构建，原 public tools 计划没有内容变更。未修改上游或安装额外构建。
- source/installed package validator 均 passed；选定 Shared/Claude/Codex/Cursor 投影、managed bytes/mode、dogfood drift 和 ownership 检查通过；递归 .new/.bak 为零。原 owner 通过实际 target resolver/native continuation/public operation probe 验证目标可用。
- 在同一次原 tools-only operation 的原 installer 与 public maintenance proof 下执行真实 reapply，package/overlay=ok、installed validation=0，native=passed。Task record、config、AGENTS、workflow 字节保持，peer/common Python pointers 保持；没有手改 manifest/hash。
- 安装后的原 Bind wrapper 对真实同 Task/session 执行完整双文件及 stdin+inline，均 exit 0/session_resumed；当前 Delivery selection 保留。双 - 返回 conflicting_arguments/arguments.--owner-result/2；实际 zsh process substitution 返回 invalid_json/input/2 并准确指出不支持载体。安装 help 同步两参数支持形式及双 - 限制。

## 尚未验证

完整 candidate Check、RDT final_integration、实际内容重绑、Architecture/final Check、commit 与独立 Branch Review 均未执行。formal_fork_source_lock 保持未验证；本轮采用证据是同 checkout local_candidate，不冒充正式发布来源采用。

业务 #961 现场、后续串行 Issues、真实全部平台 Agent、额外 clean installation、完整多平台升级/Release 矩阵不由本项验证。源码、单元、实际 source wrapper、installed 及正式 lifecycle 结论分开，未执行结果不预填通过。

## 本机替代分隔符的源码修正

官方 CPython [os.altsep](https://docs.python.org/3/library/os.html#os.altsep) 定义 Windows 同时支持反斜杠与 `/`。只检查 os.sep 的原实现会把正常 `./`、`../` 缺失路径报为 mixed 歧义；生产 reader 的只读平台常量单元复现观察到该差异，未执行原生 Windows。

当前 canonical reader 按 os.sep 及非空 os.altsep 生成 `.`、`..` 明确前缀，继续保留绝对路径和其他 mixed 歧义，不按任意斜杠猜路径。新增回归执行生产 reader，检查 Windows 分隔符常量组合下的 `./`、`../` 和裸相对名边界。修正后 shared suite 13 项、两个变更 Python 文件内存语法及 diff hygiene 通过。

本段观察截止于源码修正；已有 installed reader 尚未同步该修正。前述 source/installed 验证保留其原观察对象，不能自动升级为本次 installed 结果。后续同步、当前 Check 和独立 Review 仍由原 owner 承接，原生 Windows 实测与完整矩阵边界保持。

## 替代分隔符修正的安装采用

后续原 tools-only owner 从 `b8e1380f6817e9dd6f91bad6c69f32aa0c54e044` 加本次 ALTSEP 源码修正执行新的冻结操作，实际返回 tools_upgraded / 0.7.0-guru.7。installed reader 与 canonical 字节一致；使用目标 resolver 加载 installed reader，执行同一 shared suite 的 13 项测试通过。该测试模拟 Windows 分隔符常量，不代表原生 Windows 执行。

本次 installed package validator、ownership、Shared/Claude/Codex/Cursor 投影、dogfood drift、变更 Python 内存语法和 diff hygiene 通过，受管范围 `.new/.bak` 为零。目标原生 get_context.py --json 返回 exit 0，原 Task/Delivery 仍为 implementing。配置、AGENTS、workflow 与 Trellis config 字节保持；原执行器的 peer/common pointer 保持检查通过。先前真实 Bind 和 reapply 结果仅在相关实现、入口合同及 installer 未变的范围内采用；本次新增 installed-reader 行为已实际执行，不以旧安装结果代替。formal_fork_source_lock、业务现场和完整矩阵仍未验证。当前修订 Check 与独立 Branch Review 尚待原 owner 执行。
