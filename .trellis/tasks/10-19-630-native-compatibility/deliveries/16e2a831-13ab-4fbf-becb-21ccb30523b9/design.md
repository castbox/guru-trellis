# D1 原生失败诊断与精确选择设计

## 1. 设计目标、需求承接与内容基线

承接 DR1–DR6、DA1–DA5。D1 是整体 #630 的部分交付，后继产品修复及外部验收继续保留。development baseline B 与 Planning H0 均为 `0543731bf52aa80842fde5db47332380de513cf0`，来源为显式 main；最终内容范围为 B...最终 HEAD，PR 目标为 main，不把 H0 当最终实现 head。

Architecture candidate_assessment 实际输出为 baseline_current/no_architecture_impact，baseline=current-main-0.7.0-guru.102、constitution=guru-trellis-design-constitution-v1。该结果限当前既有 CI、runtime、ownership 边界；最终 design 另经独立 final_plan。

## 2. 当前系统、边界与目标差额

ci/targeted_ci.py 创建目标 checkout 与依赖环境，调用 driver unittest_report，再独立尝试 source-lock Fork 构建和 clean 安装。现有 smoke 失败只保留最外层错误。目标 bootstrap_check.py 本身已经通过真实公开 wrapper 测试两种 schema 输入，但底层 stdout/stderr 未进入现有 artifact。

本批无前序。差额是一个明确选择语法和一个仅观察目标原实现的诊断入口。不改变产品错误协议、manifest、runtime cache 或激活规则。

## 3. 来源设计处置（唯一）

| 来源承诺 | 处置 | 具体落点及理由 |
| --- | --- | --- |
| #630：复用 #631，不能新建重复基础设施 | retain | 第4节复用现有 Steps/target/artifact；只补本 Issue 必需入口 |
| #630：文件+用例精确加载，独立 driver/target | retain | 第4–5节 file::selector 与明确目标根；不复制产品代码 |
| #630：先取得 Windows 底层返回码和输出 | retain | 第4/6节观察目标 capability fixture 的实际 subprocess 结果 |
| #630：expected matcher 不接受任意安装失败 | retain | 第5/8节保持 matcher 原语义，诊断结果独立记录 |
| #630：三系统、产品验收、真实 Agent 分开 | retain | 第7–8节只交付本批原生诊断；后继承担产品与 Agent |

两个历史工具修改为后继产品修复线索，本批不吸收其 runtime patch。公开 Skill I/O 和现有 bootstrap fixture 输入保持原合同。

## 4. 模块、职责与设计取舍

1. ci/unittest_report.py 解析 `文件.py::类.方法`。使用标准 unittest loader 从指定文件的真实模块装载目标对象；按测试选择维持目标 import 根，保留旧文件和模块入口。找不到目标使用 unittest error/非零，不能空 suite 通过。
2. 新增 ci/runtime_diagnostic.py，只负责在独立子进程/受控 import 根加载目标自己的 bootstrap_check 与依赖。将现有 hash-locked venv 放入 fixture 期望布局，执行目标原有 check_public_wrapper。临时包装 subprocess.run 仅记录该固定 capability wrapper 调用的 argv、原始结果与异常，不修改 argv、stdin、encoding、返回值或异常；finally 恢复原函数。目标产品文件不改写。
3. ci/targeted_ci.py 在目标依赖具备时调用该 driver-owned 诊断，使用目标资产/解释器。诊断报告与安装结果分开。无论诊断或测试结果如何，都继续原安装尝试；原失败保持原非零。诊断 collector 的执行错误作为基础设施错误，目标原 fixture 失败作为记录的产品观察，不改写安装阶段结果。
4. ci/test_targeted_ci.py 与新增必要 driver 回归验证真实文件加载、观察器不改参数/结果，以及失败继续。docs/ci/README.md 说明新语法和读取结果。

不在 Guru runtime 增加诊断协议或持久状态，不创建新的公共 Skill、hook 或业务 authority。选择只观察 fixture 是为了不收集任意命令或业务输出。

## 5. 接口与数据

unittest_report 的 tests argv 新增 `path.py::Class.test`，仍为一个字符串；`path.py` 与 `module.Class.test` 保持原语义。结果仍为 tests_run/failures/errors/skips/outcomes，不修改 matcher。

runtime_diagnostic 以 `--target-root`、`--python`、`--output` 的明确路径定位对象。报告记录 driver/target 身份、fixture 调用 argv、returncode、stdout/stderr 或异常和诊断状态。命令与日志仅来自固定 schema fixture；不包含环境、认证、.git 或完整工作树。CI 报告复用现有 step command/returncode/log 机制，增加指向该诊断报告的明确字段。缺环境记未执行；fixture 失败记失败事实，绝不伪造成功返回。

## 6. 状态、顺序、正常与失败流程

目标 checkout → hash-locked 环境 → 精确测试 → 目标 capability 诊断 → 原 clean 安装 → 汇总。诊断使用临时目录，退出按既有临时生命周期清理；不激活目标 pointer。诊断调用目标原 fixture，保留其成功与普通 schema 不完整输入两例的原行为。

loader import 错误、缺类/方法或零用例继续非零。诊断 collector 无法启动/加载前提失败记基础设施失败。fixture 在实际 Bash/Python 调用失败时保留输出与失败阶段，collector 仍能完成记录；原安装结果继续决定产品安装状态。基线失败不取消候选，单系统失败不取消另外系统。

## 7. 恢复、兼容、迁移与集成

无持久化模型或公共状态迁移。正常重跑使用原 workflow_dispatch，创建新的独立目标，不修改已保存旧证据。新增选择语法是显式扩展，旧语法保留其现有 caller，不新增旧 runtime fallback。未知产品安装失败保留原失败，不通过诊断 success 重分类。D1 产物供后继 Delivery 选择真实缺陷断言、收集首偏差和比较修复，不证明修复或 Task Completion。

## 8. 验证设计

| 验证 | 需求/验收 | 测试层和入口 | 预期观察/限制 |
| --- | --- | --- | --- |
| V1 | DR1/DA1 | 临时文件实际 unittest_report 子进程 | 精确选中一项；未选失败不执行 |
| V2 | DR1/DA2 | 旧文件、模块、缺方法与 import 错误 | 旧入口结果保持；错误和零用例不得通过 |
| V3 | DR2–4/DA3 | 诊断脚本加载目标资产与真实 Bash/venv | 真实 argv、返回码和输出；无目标代码替换 |
| V4 | DR5/DA4 | driver 集成测试与三系统 targeted CI | 失败继续，原安装失败仍非零，目标 identity 不混合 |
| V5 | DR6/DA5 | docs/ci 自检与 artifact 读取 | 使用说明可复制；区分诊断、产品与 Agent 证据 |

每个原生结果记录实际 OS/Git/Python/Bash、driver/target SHA、入口和返回码。平台模拟只证明对应单元层，不代替原生三系统结果。Windows Codex 会话与完整上游集成不在本批执行，继续为整体必需责任。

## 9. Canonical 引用、本轮差额与实际未决项

命中 docs/ci/README.md 的精确选择与诊断读取；原 Test And Validation Value 与 Validation Scope Ownership 保持。RDT 当前 lifecycle/Completion/knowledge authority 不因 CI 驱动细化变化。候选 no-impact 不创建空 Architecture contribution 或 ADR；若最终实际代码改变产品 authority、runtime 输入/状态或字节/hash 合同，停止并回原 Author/Architecture，不在本批顺带实现。实际 Windows 首偏差由本批原生 run 取得，不能先填根因。
