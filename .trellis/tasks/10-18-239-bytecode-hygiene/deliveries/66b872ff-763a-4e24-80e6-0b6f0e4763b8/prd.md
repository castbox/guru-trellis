# #239 D1 字节码过滤与语法检查需求

## 1. 整体来源与术语

整体范围由 [Task PRD](../../prd.md) 的 accepted_scope 拥有，当前版本 `sha256:557b9f11dc1f678c3d1fe68f61f71e1a182e73331a011ebaea63481857594c91`。Direct Source 为 [Issue #239](https://github.com/castbox/guru-trellis/issues/239) 的 R1–R3、验收与非目标；已完整读取。产品资产、dogfood 和字节码定义见整体 PRD 第1节。本批 scope_ref 覆盖 R1、R2、R3、AC1–AC5；planning_root 为 `deliveries/66b872ff-763a-4e24-80e6-0b6f0e4763b8`。

## 2. 整体与本批目标、非目标

本批是全量 D1：消除相邻字节码导致的产品漂移误报，将常规语法检查改为不落盘、不执行模块的内存编译，并同步受影响副本。两个缺口共同影响 Guru 产品判断与检查卫生。保留安装器、collect_files、tree_sha256 和 #430 已有正确能力。
仅修改 Guru 管理资产。排除业务仓源码/测试/缓存/入口/ignore 与发布身份、源码缓存清理、第三方/虚拟环境、统一摘要框架、新身份格式、所有入口快照化、Trellis 上游、完整历史/发布矩阵及生产操作。完整约束由整体 PRD 第3、5、6节定位，本批同样适用。

## 3. 本批起点、前序结果、依赖与剩余责任

没有前序 Delivery。开发基线 main@`ed59e851b6c1257bac6316a9571274427e383c93`。真实安装副本的隔离复制已复现：baseline verify 通过，py_compile 输出相邻 pyc 后完整 verify 误报；-B 下显式 py_compile 仍写缓存。这是调查事实，不是修复验收。
依赖当前匹配 preset 和 managed Python。未分配的 accepted scope 为零，但所有 AC 仍须执行验证。若直接复制工具正常复现遗漏 .pyo，仅修复其 Guru 产品范围。Delivery 合并后由 Completion 独立评估整体范围、证据和边界。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置与触发 | 处理和观察 |
| --- | --- | --- |
| S1 | dogfood checker，真实一致安装副本 | 完整检查通过；增加/改变 __pycache__、相邻 pyc/pyo 仍通过且不改缓存 |
| S2 | 同 checker，真实产品缺失或内容改变 | 继续失败并报告原有 drift |
| S3 | Agent，按常规文档检查 Guru Python | 合法成功，语法错误失败且指明文件/原因；不执行模块，不增删改缓存 |
| S4 | 原安装、runtime、资格摘要或复制入口 | 在各自既有产品范围忽略三类字节码，保留合法范围和摘要差异 |
| S5 | 维护者，preset 同步后重复应用 | 受管副本一致，无新 sidecar 或非预期 tracked 变化 |

执行顺序：修改 canonical → 定向行为验证 → 现有机制同步 → 重复应用与 drift 验证。缓存清理不作为任何前提。

## 5. 完整行为、条件与约束

R1：文件清单、摘要、一致性和隔离产品复制排除 __pycache__ 分量与 .pyc/.pyo 文件；缓存数量/路径/内容/大小变化不改变产品判断；真实产品变化必须检出。保留原公开/私有划分、排序、算法和身份格式。不新建缓存基线；其它路径仅在正常复现后修正。
R2：将常规落盘 py_compile/compileall 改为内存 compile，覆盖原 Guru 文件范围；不执行、不写、不清理；错误必须非零并报告文件与原因。编译工具仅可用于临时目录内的字节码专项回归。
R3：从 canonical 经现有 preset/managed spec/platform 机制同步实际受影响副本。复制改动仅限 Guru 产品资产；保留前后检查，分别报告产品变化与执行缓存。不要求新复制协议、错误码或引擎。设计承诺的唯一处置在本批 design 第3节。
没有公共 API、schema、持久化字段或发布身份变化；没有数据迁移。其余完整非目标继承整体 PRD，不能将本批工程细化扩成业务升级。

## 6. 本批验收、验证方式与未决项

AC1：真实安装隔离复制的完整 verify 覆盖一致/三类缓存新增及变化/真实产品修改及删除；缓存检查前后不变。
AC2：定向调用安装器文件选择、runtime collect_files、资格 tree_sha256 和实际影响的复制入口，验证自身范围过滤及真实变化。
AC3：执行最终文档中的真实内存语法命令；合法成功，错误失败且指明文件/原因；产品与既有缓存不变且无新缓存。
AC4：相关包/集成、所有权、canonical-installed/platform parity、重复 apply 与 #430 回归通过；无新 .new/.bak 或非预期 tracked 变化。
AC5：只有新增安装资产或布局变化才做最多一个当前版本 clean 临时安装；无布局变化不增加形式安装。完整多平台、历史升级和发布候选矩阵明确未执行。
无必要产品未决项。复制路径候选须实现调查后正常复现，证据不足不扩大工作。

## 7. Canonical 引用与本轮差额

当前 RDT：`docs/requirements/versions/current-main-0.6.17-guru.108/requirement-main.md`、`docs/design/versions/current-main-0.6.17-guru.108/design-main.md`、`docs/test/versions/current-main-0.6.17-guru.108/test-strategy.md`，继承链的相关过滤/安装合同由本轮定向修复承接。Architecture：`docs/architecture/README.md` current .99，constitution 与 change-contract 由原 owner 判断。工程直接合同：`trellis/presets/guru-team/spec/workflow/quality-guidelines.md` 的 Required Validation 与 `companion-scripts.md` 检查命令；本轮移除落盘语法检查。原机制和知识 owner 保持，Docs 差额由原 RDT owner reconciliation。
