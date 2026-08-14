# #231 用户级共享 Python runtime cache

## 背景

#219 已让公开 Skill wrapper 使用含锁定依赖的受管 Python venv，但 venv 与
`active.json` 都存放在 checkout-local `.trellis/.runtime/`。linked worktree
不会复制该 gitignored 目录，因此正常 worktree 首次调用 wrapper 时无法找到已安装
runtime，并把“尚未 bootstrap”误报为 `jsonschema` 缺失。该缺陷阻断 #222 的
exact-candidate throwaway gate，Finding 为 `EXT-222-001`。

## 目标

1. 每个操作系统用户维护一个共享 cache，每个完整 runtime identity 对应一个不可变 venv。
2. 同一 Git repository 的所有 linked worktree 通过 Git common-dir 下的私有 pointer 解析同一 runtime。
3. identity 绑定 runtime API、layout、dependency lock、Python implementation/minor、OS、architecture 与 ABI/platform tag。
4. preset initial apply、reapply、official update 后 reapply 与公开 wrapper 使用同一 locator 合同。
5. 缺失 pointer、未 bootstrap、损坏 runtime、真实 dependency 缺失返回准确且稳定的 JSON 错误。
6. 不修改系统 Python、global/user site-packages、Trellis upstream、全局 npm 或真实业务 checkout。

## 验收

- 主 checkout 完成 apply 后，新 linked worktree 无需复制 venv即可运行真实公开 wrapper。
- 相同用户、平台、Python ABI和lock复用同一runtime；不同identity不复用。
- cache位置符合macOS/Linux/Windows用户cache约定，并允许测试通过显式环境变量隔离。
- active pointer 位于 Git common-dir 的 Guru 私有runtime状态中，不tracked且不依赖worktree-local `.trellis/.runtime/`。
- 旧checkout-local runtime在新shared runtime验证并激活前保持不变；正常迁移不删除旧runtime。
- source/installed/platform copies、manifest inventory与dogfood一致，零未知sidecar。
- 重放 `EXT-222-001` linked-worktree路径通过；#222完整Release Gate仍由#222独立重跑。

## 不在范围

- hostile actor、故意篡改、并发锁、TOCTOU、跨OS原子事务或自动GC。
- #223、#208、#164、#220。
- tag、Release、部署或真实业务仓mutation。
