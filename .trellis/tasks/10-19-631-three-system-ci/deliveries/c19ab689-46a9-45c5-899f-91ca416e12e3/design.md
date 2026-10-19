# 三系统 CI D1 设计

## 1. 设计目标、需求承接与内容基线

本批实现 PRD 的 R1–R8、AC1–AC6。development baseline B 为明确选择的 `71f432f22acc78df7194a818c27b8e467ceb3048`；没有前序 Delivery，Planning H0 与 B 相同，PR 目标为 main。内容审查范围从固定 B 到实际候选，main 的后续变化另由原 owner 判断，不混成内容基线。

适用 Architecture 为 `current-main-0.7.0-guru.102`，constitution 为 `guru-trellis-design-constitution-v1`，change contract 为 `guru-trellis-architecture-change-contract-v1`。独立 candidate_assessment 返回 no_architecture_impact：新增仓库私有 CI，不改变 Guru 判断、公共 API、状态 owner、共享写入或兼容退出。本设计细化该候选，最终仍经 Wording 与独立 final_plan。

## 2. 当前系统、边界与目标差额

现有 `trellis/presets/guru-team/scripts/python/test_guru_platform_inventory.py` 通过真实模块和 CLI parser 检查平台选择、inventory 和安装投影。现有 installer 与 README 定义 source-locked Fork 构建、CLI init 和 preset apply。没有 Actions 配置。本次只新增 `.github/workflows/targeted-ci.yml`、仓库私有 `ci/` 驱动、`docs/ci/README.md` 与 README 导航；不修改 installer/runtime 的产品行为，不把 CI 驱动分发到业务仓库。

## 3. 来源设计处置（唯一）

| 来源承诺（#631 实施范围） | 处置 | 落点与理由 |
| --- | --- | --- |
| 1：PR/main/手动与路径覆盖 | retain | 第4节 YAML 编排；路径包含纳入的全部源与驱动 |
| 2：明确原生 OS、真实 Python/Git Bash、版本记录 | retain | 第4/5节环境探测与版本报告 |
| 3：既有真实测试、clean smoke、非零失败 | retain | 第4/6节执行原 unittest 与原 installer，不复制业务断言 |
| 4：独立目标与 driver、真实 commit、候选继续 | retain | 第5/6节目标 checkout 与结果分离 |
| 5：Windows 可见性与编码案例不被掩盖 | retain | 本次记录真实环境；缺陷专属案例由 #630/#53 接入，不强制 UTF-8 来制造兼容通过 |
| 6：fail-fast=false、原始结果与真实汇总 | retain | 第6节；不能用预期基线失败抵消候选或基础设施失败 |
| 7：失败仍上传脱敏诊断与维护说明 | retain | 第5/8节；artifact 只收集明确诊断目录 |

没有来源设计变更或上游处置请求。

## 4. 模块、职责与设计取舍

- `.github/workflows/targeted-ci.yml` 只处理触发、原生 `ubuntu-24.04` / `macos-15` / `windows-2025` matrix、Python 3.12、Node 22、驱动调用与 always artifact 上传，matrix fail-fast=false。使用 checkout/setup-python/setup-node/upload-artifact 官方 action 的明确 major；记录实际版本。权限 contents:read；checkout 不保留凭据。
- `ci/` 中 Python 驱动负责确定性编排、源身份、命令/退出码和结果报告。按完整 SHA 分别 clone/checkout baseline 与 candidate；driver 不修改目标产品文件。目标依赖使用各自 `runtime/requirements.lock` 的 require-hashes 安装。测试以原生 Python 在目标工作目录加载目标既有 unittest；驱动只收集 unittest outcome，不实现产品断言。
- 初始默认选择 `test_guru_platform_inventory.py`，因为它在当前三个系统适用，执行真实 inventory、installer 模块和 CLI parser。手动可选明确目标测试文件或 unittest 标识，新增缺陷测试随 #630 接入；不要列不存在用例或隐式跳过失败。所有 skip/error 数量与原因都保留，未实际执行不能算通过。
- 每目标根据自己的 source lock 准备独立干净 Fork checkout，读取其 pnpm 版本并执行冻结 lock 的安装和正常 build；使用原 CLI bin，不复制 dist 或全局安装 CLI。clean smoke 创建新的 Git repo，经 `node <fork>/packages/cli/bin/trellis.js init -y --codex --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#<target_sha>`，再用目标 preset `apply.sh --repo <smoke> --platform codex --python <native_python>`。验证生成 workflow、Guru manifest 和现有 installed validator 可观察结果。若正常产品入口失败，保留入口和完整诊断，后续 AI 按 #630 具体项归因；脚本不自行判定所有安装失败都是产品问题。
- Windows 选择 Git for Windows Bash 的真实路径并验证 `uname`/版本，避免误用 WSL；Python 使用 setup-python 原生解释器。不伪造 python3/py launcher，不把系统默认编码改成兼容性证据。Fork/目标测试和安装使用各自独立目录，外部构建失败明确为基础设施/依赖失败。

使用单一驱动服务自动与手动入口，避免 YAML 复制业务断言。无需抽象 provider/plugin、持久 checkpoint、锁或重试协议。

## 5. 接口与数据

workflow_dispatch 输入为 candidate_ref、可空 baseline_ref、定向 tests，以及可空 expected_test / expected_message。candidate_ref 空时使用当前运行的 Git SHA；PR 自动使用实际 PR head，不用合并模拟提交冒充目标。driver_sha 是加载驱动的精确 checkout SHA，独立记录 event/source ref。

expected_test 与 expected_message 共同指定一项缺陷断言；缺任一项时不宣称“基线命中指定缺陷”。只有基线该 unittest failure 的 ID 与消息匹配、准备正常、候选全部通过，才报告对照成立。没有匹配或两目标同结果均照实保留。ImportError、依赖失败、无关 error 不算复现。

报告以 JSON 保存 driver SHA、runner ImageOS/ImageVersion、OS/Python/Git/Bash/Node/pnpm/依赖实际版本、每目标请求 ref/解析 SHA、工作目录、每阶段命令和原始 returncode、测试数量/失败/错误/跳过、安装步骤和对照结论。每目标还保存可读日志与测试报告；汇总写 Actions step summary。报告供维护者诊断，不是 Guru lifecycle authority。无需新公共 API 或业务数据迁移。

## 6. 状态、顺序、正常与失败流程

每系统先准备诊断目录和环境记录，再逐目标解析/checkout → 依赖 → 既有测试 → Fork 准备与 clean smoke。测试非零仍继续 smoke；基线失败仍继续候选。每阶段结束立即写已得到的命令、退出码和日志；普通异常也输出具体阶段，不伪造未运行步骤。

最后生成各系统 summary；任何候选失败或基础设施失败保持 job 非零。基线只有精确命中显式断言才可标预期；基线其他失败仍为失败。always 上传已有诊断，未生成证据时明确上传/执行失败。取消记未完成，不承诺强杀后的完整报告。没有 Guru Task 状态变化或数据库事务。

## 7. 恢复、兼容、迁移与集成

重跑使用 Actions 正常 rerun 或 workflow_dispatch；每 run 使用全新目标/安装目录，不复用失败目标作为成功证明。只保留诊断 artifact，默认14天；可以用 gh run download 下载。无需产品状态恢复、数据迁移、发布回滚或旧 consumer adapter。既有 installer/lock/冲突语义保持；CI 发现产品问题只交 #630，不替其修改产品或 source lock。

## 8. 验证设计

- V1（AC1）：检查 YAML 语法、触发路径与实际 PR/main/dispatch run；静态检查只能证明声明，实际链接证明触发。
- V2（AC2）：原生三系统真实执行既有11项测试与 clean smoke；记录准备/执行/上传身份和结果。产品失败须有具体入口/断言。
- V3（AC3）：dispatch 指定两个实际 commit，下载报告核对 driver/目标 SHA 与独立目录、两个结果及对照结论；相同结果也合法。
- V4（AC4）：实际自然失败 run 的 artifact 可下载、定位断言，候选与另外系统均继续。驱动本地集成测试用真实临时 Git/test 文件验证独立目标和失败后继续，不用 mock 声称原生系统成功。
- V5（AC5/AC6）：核对维护文档命令可执行，明确 #630/#53、解释器/编码专属案例、真实 Agent 和完整矩阵未验证边界。

## 9. Canonical 引用、本轮差额与实际未决项

`docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md` 的 Task/Delivery 公共能力不变。新运维行为唯一写在 `docs/ci/README.md`；不改共享知识版本或制造空 contribution。Architecture 无影响结论不产生 contribution/ADR；后续若实际实现扩大边界，回原 Architecture owner。`.trellis/spec/workflow/quality-guidelines.md` 的验证价值与范围分工约束当前检查。没有阻塞方案选择；原生运行结果尚未取得。
