# Trellis 官方扩展边界核对

核对日期：2026-07-20。

## 权威页面

- <https://docs.trytrellis.app/index.md>
- <https://docs.trytrellis.app/advanced/custom-workflow.md>
- <https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md>

## 与 #144 直接相关的结论

1. `.trellis/workflow.md` 是 workflow phase、skill routing 与 runtime breadcrumb 的 Markdown 控制面；本任务不通过修改 Trellis upstream、全局 npm 包、`node_modules` 或 hook parser 实现流程分叉。
2. Workflow marketplace 与项目内安装副本属于不同层级。#144 先修改本仓库 canonical contract/runtime/preset，再通过 installer 同步 dogfood 与平台副本。
3. Spec template marketplace 只承载可复用工程约定，不承载 active task、workspace journal、平台 prompt 或项目私有状态。
4. Marketplace/template id 与公开 command/schema id 属于稳定公共接口；#144 使用独立 interface 1.3，并保留 1.2 legacy 语义。
5. `trellis update` 会依据 template hash 处理已管理文件；实现与验收必须覆盖 update/reapply、`.new`/`.bak` 和 clean throwaway install，不能只验证当前 dogfood 仓库。

这些结论只约束扩展面和分发方式，不增加 #144 的产品范围。
