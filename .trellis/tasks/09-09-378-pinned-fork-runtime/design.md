# #378 技术设计

## 候选固定身份

- Fork：`https://github.com/castbox/Trellis.git`
- SHA：`ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`
- CLI/core 源码版本：0.6.16。该版本不是 npm 发布证明。
- Guru base：`a2b32ea8dc730eecf0507e0adfb946ce9b8c7bc8`

## 单一来源与执行边界

在 canonical preset 的 `source/trellis-source.json` 保存 schema version、Fork URL、
完整 commit、CLI/core 版本和源 package-manager identity。构建器、安装入口和验证器
直接消费同一文件。installed 投影为 `.trellis/guru-team/trellis-source.json`，由 preset inventory 管理。
不建立第二份可独立变更的 installed source authority。

复用现有 Fork checkout，自身依赖安装和 build 完成后直接运行
`packages/cli/bin/trellis.js`。不新增 `trellis.sh`、source-build 系统或缓存管理器，
不复制 dist、不重造 launcher。当前安装与后续更新都使用同一 Node CLI 调用；
验证器接收 checkout 作为调用参数，核验来源记录与实际 HEAD、remote 和构建文件。

构建顺序：复用 checkout 并 fetch 固定 Fork commit -> 核验 HEAD -> 根据 Fork lockfile 安装构建依赖 ->
构建 core -> 构建 CLI -> 调用该构建的 bin。保留正常第三方依赖，不下载原 Trellis
框架发行包。构建不执行递归 submodule 初始化；docs-site 与 marketplace 的 Git URL
列入来源审计，只有实际安装/更新需要的依赖才进入执行路径。

受控入口不执行 stock `upgrade` 的 npm 全局安装逻辑。框架版本更新先修改 canonical
source lock，经评审后由同一入口重建，再运行 update。移除当前文档和脚本里的原发行源
自动选择路径，不提供长期原源/Fork 双运行模式。直接运行用户自行安装的全局 trellis
不属于受控入口，不声称能拦截它。

## 安装与迁移

新安装：固定源构建入口运行 init，并显式指定 Guru workflow marketplace；再运行同一
Guru checkout 的 preset，保留目标平台选择。

已有项目：固定源 CLI update dry-run -> 根据输出选择 migrate/非 migrate 的 preserve-mode
update -> 核验 workflow 字节 -> 保留当前 Guru workflow 或经预览切换 -> 同平台 preset reapply。
逐个处理本次 sidecar，不能覆盖未审查本地修改。

本 worktree 不整体 apply 旧 stash。优先由固定 CLI 重新生成 Trellis-owned 文件；stash
只用于解释前次更新差异。旧 installed manifest 不恢复；当前 preset 根据新源码生成
manifest，确保 #388/#389 保留。

## 来源证明

准备命令以 `&&` 串联，成功完成 Fork 自身构建后才将实际 HEAD 写入 CLI dist 下的
`.guru-source-commit`。来源校验比较此标记与固定 HEAD，避免同版本源码切换后误用旧
编译代码。它只表示本地成功构建的来源，不承担语义批准、防篡改或发布身份。

验证器检查固定源 commit、构建版本及关键 installed 文件对应关系，不以版本号相同
推断来自 Fork。构建日志中的机器路径只保留在本机；共享来源记录只保存固定源码身份。
不得把用户授权、语义批准或完整扫描过程写入 lock/manifest。

## 文件范围

- canonical preset source lock、现有 verifier 的 checkout 输入、安装器 inventory。
- `trellis/guru-team-extension.json` 的 target/要求字段及直接消费它的配置、验证与测试。
- README、preset/workflow README 中当前安装更新合同；历史 Release 和 archive 不批量替换。
- 定向 Fork 来源与隔离测试；受影响的脚本测试随 source contract 同步更新。
- 由更新器生成的 `.trellis/scripts` 和平台 hooks；由 preset 生成的 Guru 受管投影。

## Docs SSOT Plan

策略：delta_first。先由 RDT/Architecture owner 判定任务影响并形成 contribution，
再在实现核验后 promotion。共享 current authority 不在本规划写入时直接提升。
当前导航为 `current-main-0.6.5-guru.46`；新 identity 由 owner 根据实际改动确定，
不预先声明新版本已兼容或已发布。

## 风险与约束

verify-throwaway-install.sh 只承接参数与受管 Python dispatch；移除 dispatch 后不可达的
历史尾部，full/focused 场景由现有 Python matrix 单独拥有，不复制构建或场景编排。
保留 #267/#332 对完整发布矩阵的独立 ownership。
固定源码不可用、构建失败、版本不符、未知定制冲突均停止，不删除旧安装或全局 CLI。
