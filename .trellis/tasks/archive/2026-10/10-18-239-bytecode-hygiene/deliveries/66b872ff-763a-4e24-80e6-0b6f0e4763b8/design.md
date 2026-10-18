# #239 D1 设计

## 1. 设计目标、需求承接与内容基线

承接本批 PRD 的 R1–R3、S1–S5、AC1–AC5，D1 全量修复两个缺口。development baseline B 为 main@`ed59e851b6c1257bac6316a9571274427e383c93`，来自初始 Sync；Planning H0 同该提交，最终实现 HEAD 另由 Task Commit 决定。内容范围为 B 到本批实际候选；PR 目标为 castbox/guru-trellis:main。
独立 candidate_assessment 已返回 baseline_current：Architecture `current-main-0.6.17-guru.99`、constitution `guru-trellis-design-constitution-v1`，impact_kind=no_architecture_impact。原 owner 核对现有过滤、复制、调用方和规范；本轮不新增架构能力。实际工程约束见 docs/architecture/06-governance/change-contract.md。

## 2. 当前系统、边界与目标差额

没有前序 Delivery。安装器 skill_package_source_files、runtime collect_files 与资格 tree_sha256 已排除三类字节码，保留其范围、排序与摘要编码。dogfood checker 的 _tree_files 只排除 __pycache__，漏掉相邻后缀。canonical quality-guidelines、companion-scripts 以及项目本地 workflow/index、preset/installer 中仍有落盘语法检查命令。
改动留在原检查职责：补后缀过滤；用内存 compile 检查原范围；只在正常复现后修正 Guru 产品临时复制遗漏。业务源码、第三方、虚拟环境和私有运行缓存保持原职责，本轮不扫描或修改。

## 3. 来源设计处置（唯一）

已完整读取 Issue #239 的 R1–R3 和约束。其必要技术承诺按下表落实；示例 compile 是实现选择的依据，不创建新 API。

| 来源与承诺 | 处置及落点 | 理由、影响、上游处置 |
| --- | --- | --- |
| R1：__pycache__ 分量、.pyc/.pyo 排除 | retain，第4节原 checker/复制条件 | 非产品缓存不进入判断，保留真实内容检测；无需改来源 |
| R1：各工具保留范围/公开私有/排序/哈希编码 | retain，第4–5节只补缺口 | 不造统一引擎；已有实现仅回归 |
| R1：不建缓存基线，不依赖清理 | retain，第6、8节只读观察 | 不新增持久台账；临时测试快照仅服务检查前后不变断言 |
| R2：覆盖原范围、内存 compile、不执行/写入/清理、错误失败 | retain，第4、6节实际文档命令 | 直接替换落盘操作，专项临时编译例外保留 |
| R3：canonical 后走原同步，复制只限 Guru 资产 | retain，第6–7节 | 不改安装布局或业务仓规则，保留前后检查与 #430 provenance |
| 验收5：布局不变不做形式 clean 安装 | retain，第8节边界 | 本设计无新安装资产，完整矩阵仍由专门 Issue 承担 |

## 4. 模块、职责与设计取舍

D1：`trellis/presets/guru-team/scripts/python/verify_dogfood_platform_selection.py` 的 _tree_files 在现有 is_file、非 symlink、__pycache__ 条件中增加 path.suffix 排除 .pyc/.pyo；_assert_equal_trees 继续比较产品文件集合和实际字节。
D2：canonical `spec/workflow/quality-guidelines.md` 定义一个完整的内存语法命令；companion-scripts 和项目本地 index/installer 定位该命令或使用同义片段。命令仅显式遍历 `trellis/skills/guru-team/runtime`、`trellis/skills/guru-team/packages` 的 Python 文件及原 installer 文件，读取 bytes 后 compile；必要时扩展到本轮已触及的 Guru Python 文件。错误沿 Python SyntaxError 的文件/原因和非零退出传播。使用 -B/禁写环境保护命令自身的普通导入；内存 compile 本身不落盘。
D3：检查 `trellis/skills/guru-team/runtime/bootstrap_check.py` 等直接产品复制入口。对普通编译产生的 .pyo 先证明原入口带入副本，再在原 ignore_patterns 增加 *.pyo；不修改上游 .trellis/scripts、hooks 或业务文件复制范围。没有复现的工具不改。
D4：新增有行为价值的定向回归，位于现有测试位置，不安装测试文件。测试调用原函数或完整 verify/实际文档命令；不通过复制过滤实现来计算期望。不改巨大 installer 源或其超过 3000 行的历史测试文件；已有 #430 测试定向重跑。
不新增共享投影模块、统一缓存策略、缓存清理或公共脚本。短过滤条件保留在各工具真实职责，避免耦合合法范围。

## 5. 接口与数据

输入仍是原 repo/资产路径，输出仍是原 verify 结果或原错误。无 profile、typed exit、JSON/schema、manifest 身份格式、数据库或用户配置变化。语法检查输出为标准 SyntaxError 信息与进程状态，不执行模块。产品文件过滤只影响非产品字节码；业务路径不成为输入。无新持久字段，因此无数据迁移。

## 6. 状态、顺序、正常与失败流程

先更新 canonical 与项目工程规范，实施 D1/D3，再在隔离复制运行回归。产品一致 → verify 通过；编译生成/改变缓存 → verify 仍通过且缓存不变；真实产品删除/改变 → 原错误。合法源码 → 内存编译成功；语法错误 → 非零并指出文件/原因。原产品文件与已有缓存前后不变，无新增缓存。
随后执行现有 preset apply，同步 canonical runtime/managed specs 与所选平台。检查每个 .new/.bak；仅本次已知 managed 更新产生的备份沿原机制逐个处理，不删除未知 sidecar。再次 apply 必须不新增 sidecar 或非预期 tracked 改动。报告区分产品变化与执行缓存。

## 7. 恢复、兼容、迁移与集成

保留 #430 no-op provenance；首次同步的受管内容变化刷新 manifest，正常等价重复应用应保留其字节。源码现有忽略缓存不清理。用户改动冲突时原机制保留并给出 sidecar，由当前 owner 精确对比处理。无新 API/字段/布局，不需要兼容层、数据迁移或发布回滚协议。实现错误在同一 D1 修复后重跑受影响检查；不新建 Delivery 掩盖失败。

## 8. 验证设计

| ID | 要求/AC | 入口、输入和预期 | 层与边界 |
| --- | --- | --- | --- |
| V1 | R1/AC1 | 真实四平台 Guru 安装副本的隔离复制，完整 verify 三种结果，实际编译生成三类缓存；检查不改缓存 | 行为集成，不代替全平台 installer 矩阵 |
| V2 | R1/AC2 | 实际 installer selector、collect_files、tree_sha256 与本轮改动的复制入口；缓存不影响各自结果，产品变化仍观察 | 模块/定向集成，保留工具范围差异 |
| V3 | R2/AC3 | 执行文档实际片段；合法/语法错误/带顶层副作用源码，观察状态、错误位置、不执行和无缓存 | 语法检查行为；前后比较仅临时内存 |
| V4 | R3/AC4 | 相关新回归、runtime package、preset transaction、#430 等价 reapply/provenance/raw apply 回归 | 定向包与集成 |
| V5 | R3/AC4 | source/installed package checker、upstream ownership、dogfood drift、apply 两轮、diff --check、sidecars | 当前所选安装副本；无跨 OS 行为声明 |
| V6 | AC5 | 核对安装资产与布局未变 | 不执行完整多平台、历史升级、发布候选矩阵；无软件发布 |

## 9. Canonical 引用、本轮差额与实际未决项

RDT .108 的 Requirements/Design/Test 三入口沿本批 PRD 第7节定位；原 RDT task_impact_sync 已返回 ssot_current。长期改动由既有 canonical quality-guidelines/companion-scripts 和 project-local 工程规范拥有；不新增知识版本或证明报告。Architecture .99 与独立无影响结论适用，无真实 contribution/ADR 需求，不造空文档。最终 Phase2、committed Review 和 Completion 各自 fresh 判断。无必要未决产品问题。
