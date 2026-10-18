# Guru Trellis 技术基线选择

Identity：`ARCH-FND-STACK-001`；状态：`accepted`。该投影拥有本项目的选择、适用范围、约束和差异；通用定义仅由以下准确源拥有。

## 固定来源与读取关系

| 选择 | 精确值 |
| --- | --- |
| 公共源 | [`trellis-extension-stack` baseline](../../../trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md) |
| 版本 | `1.0`；接受后的版本正文固定，不跟随目录最新项 |
| 取得方式 | 从 `castbox/guru-trellis` 匹配源码 checkout 的上述 repository-relative locator 读取；跨仓库引用固定采用 commit/tag 和同一路径 |
| 源维护方 | 公共技术基线维护方，经原 `guru-maintain-architecture-baseline` |
| 项目维护方 | Guru Trellis Architecture owner，经同一 Skill，在本项目 authority 范围维护 |
| 关联 authority | [FOUNDATION](./baseline.md)、[constitution](./design-constitution.md)、[governance](../06-governance/rules.md)、[change contract](../06-governance/change-contract.md) |

查询先读取本投影和源 `1.0` 的完整相关条款，再读取问题所需 CURRENT 或项目差异。导航与本页不替代通用源。若源缺失、版本不符、引用断链或对象尚未迁移，应说明受影响的技术结论并进入原 Architecture repair/澄清；保留可读的原 authority，不报告完整采用。

## 项目选择、约束与差异

本项目选择源 `1.0` 的 `TES-EXT-001`、`TES-AI-001`、`TES-EXEC-001`、`TES-DATA-001`、`TES-GIT-001`、`TES-DIST-001`、`TES-TEST-001` 和 `TES-KNOW-001`。适用对象为 Guru Team 可复用 workflow/preset/Skill/spec/overlay 及 companion tools，不将业务应用栈扩张到此扩展仓库。

| Project ID / Source relation | 本项目拥有的具体选择或约束 |
| --- | --- |
| `ARCH-STACK-TOOLS-001` / `TES-EXT-001` | 匹配框架来源及 CLI/package-manager 版本唯一读 [source lock](../../../trellis/presets/guru-team/source/trellis-source.json)。该锁是本项目的具体实现依赖，不写入通用源。Guru 扩展版本、CLI/core、Fork commit 与正式 Release 是不同轴；当前 source candidate、installed runtime 和已发布版本也不能互相代替。 |
| `ARCH-STACK-SOURCE-001` / `TES-DIST-001` | canonical 根为 `trellis/workflows/guru-team/`、`trellis/presets/guru-team/` 与 `trellis/skills/guru-team/`。`.trellis/` 和所选平台目录是 dogfood 投影。preset installer 只管理声明拥有的文件；平台集合由当前 ownership 与目标安装 manifest 决定。 |
| `ARCH-STACK-GIT-001` / `TES-GIT-001` | 本项目 GitHub repo 为 `castbox/guru-trellis`。阶段适用的内容基线、当前候选与 PR integration target 分开；只有真实依赖、冲突或服务端要求等原合同条件触发整合。完整规则由 [ADR-028](../adr/028-fixed-content-baseline.md) 和治理正文拥有。 |
| `ARCH-STACK-KNOW-001` / `TES-KNOW-001` | RDT 由三层 `docs/**/README.md` 选择一个一致 authority，Architecture 由 `docs/architecture/README.md` 选择。完整当前单元与未迁移范围按各自导航定位，隔离贡献继续由原 owner 晋升。项目宪法唯一位于本目录 `design-constitution.md`，本页不复制其原则正文。 |
| `ARCH-STACK-VERIFY-001` / `TES-TEST-001` | 本项目 accepted scope 决定所需 source/package/runtime、dogfood/installed、受影响平台、drift/reapply 与代表性安装更新验证。完整累计 Release 矩阵仍归专门任务；项目 Test/EVIDENCE 单写实际执行、首次失败、修复和未验证项。 |

以上是项目选择，没有改变通用源定义的例外。未来仅在本项目需要新增差异时，由本项目 Architecture owner 修改相应项目条目并检查必要 RDT/验证关联；通用源和其他消费项目保持各自维护边界。需要改变源定义时，向源 owner 提交隔离贡献并选择新版本，不能把项目差异回填为源 `1.0`。

## 知识生效与实现证据

本投影的受审接受属于 FOUNDATION 选择，不等于 CURRENT 已实现。CURRENT 的具体状态及证据必须读取 [system](../01-current/system.md) 与 [EVIDENCE](../evidence/current-evidence.md)。TARGET、GAP、PLAN、ADR 分别保留接受方向、差距、执行依赖和历史决策职责；`inferred`、`unverified` 及仅有计划的能力不得标为实现。

旧 Task 继续读取其阶段适用的 immutable Architecture/Git authority。公共源或共享导航无关推进不要求改写旧 Task；真实适用规则、依赖、scope 或方案变化回原 owner。旧引用 consumer 结束或合法重选后，退出其普通读取；历史定位保留，不另设长期双写。
