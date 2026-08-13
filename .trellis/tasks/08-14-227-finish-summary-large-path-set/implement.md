# 实施计划

## 1. 合同与测试

- 在 Publication Review 合同测试新增大型 finish-summary fixture/helper。
- 验证 canonical schema 和 Publication owner 接受 2001 个完整路径。
- 保留并显式验证路径重复、乱序、不安全和集合不一致的拒绝行为。
- 在 Finalizer 合同测试复用等价 fixture，验证其 owner 行为一致。

## 2. 实现

- 删除 canonical finish-summary schema 两处 `maxItems: 2000`。
- 删除 Publication Review 与 Finalizer owner 的 `len(changed_paths) > 2000` 分支及对应旧错误文案。
- 不修改其它字段上限、typed exits 或公共接口。

## 3. 投影同步

- 使用仓库官方 Guru Team preset apply 同步 dogfood installed tree 与公开平台投影。
- 检查 source/installed identity、managed inventory、可执行位和零 `.new`/`.bak`/conflict sidecar。

## 4. 验证

- 运行两个 owner package 的定向合同测试。
- 运行 preset installer、Guru Team workflow/package 合同及 dogfood drift 验证。
- 运行 Python compile、JSON schema、task validate 与 `git diff --check`。
- 将新提交作为 immutable source 安装到业务 #182 工作树，重跑 Publication/Finalizer 合同与真实 2130 路径 preflight；未执行的外部验证记为 `SKIP`。

## 5. 收口

- 通过 Phase 2 semantic check 后正常提交，不绕过 hooks。
- 完成独立 Branch Review；本轮不 push、不创建 PR、不 merge。
