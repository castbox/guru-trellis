# #575 S2：唯一验证结果与边界

本文件拥有本贡献的实际执行结果。需求、机制与双向 trace 分别读同目录专属文档。本文的未执行项不是通过，知识贡献不证明软件发布。

## T575-S2-01：版本和正式来源消费者

实际 canonical 目标版本消费已对齐 `.4`：包括 extension manifest、TARGET_GURU、生产 upgraded() 返回、public output schema/example 及两个 stop consumer；合法旧版本族和真实 predecessor 保留原值。目标自身 managed resolver 执行 `test_contract.py` 34/34、`test_resume_source_update.py` 7/7、`test_fork_preparation.py` 4/4 通过，生产输出示例 schema 校验通过。

`test_delivery_upgrade.py` 首次未设置 CLI 环境时全部 SKIP，不计通过；随后使用源码 bin 路径导致20项 setup ERROR，未执行迁移。改用既有 pnpm 安装布局的匹配 candidate/predecessor CLI 后，20项中10通过、10 ERROR，首错均为正常 preset resume 使用 `sys.executable` 时模块未导入 sys。仅补齐模块 import 后，原20项全部通过（69.249秒，exit0，无SKIP）。这是本地真实 CLI 加临时 Task/Plan2/recovery fixture 的模块层证据；preset 使用既有测试替身，predecessor fixture 缺正式来源 marker，不能替代 `.4` 正式 source_locked 或真实完整安装。

三处 current-source 测试的目标版本现在读取 canonical manifest；前两处 AST 定向检查 2/2 通过。原 installer `ExtensionManifestInstallerTest.test_install_assets_writes_installed_extension_manifest` 首次因缺 `GURU_UPSTREAM_DELIVERY_SCRIPTS` setup ERROR；补上精确 Fork 的 `dist/templates/trellis/scripts` 后，原完整单测运行16.131秒、1 FAIL。新的版本传播断言通过，后续旧 schema inventory 断言仍期待 merge aggregate `1.0`，实际 interface 为 `2.0`。主 owner 以 `git show HEAD` 核实旧测试已期待 `1.0`、HEAD merge interface 已为 `2.0`，installer 生成与 merge 生产代码没有本 Task 差额，故保留为不相关历史失败；没有修复、缩小样本或记为通过。该执行只增加来源版本传播层证据，不证明正式 `.4` 安装通过。

## T575-S2-02：来源、现存基础图与投影边界

实际 source validator、ownership 检查及固定 Fork source 校验通过；最终 `.4` installed/parity/native projection、三平台 apply/reapply/drift、权限和 sidecar 仍待完成。既有 `.3` 新图验证只保持原来源，不作为最终 `.4` 证明。

按计划调用原三平台 `apply.sh --repo .`，在写入前返回 `upstream_delivery_migration_required`：目标仍保留其他合法旧归档，普通 current-only 安装要求全库存符合其合同。未转换这些归档、未绕过 guard、未手工复制工具文件。调用前保存的64个 Task/session/config/common/peer pointer内容摘要全部复核不变。

tools-only owner 是对应升级入口，但新的 `.4` 操作要求真实 clean committed `.4` source，不能复用 M 的 `.3` operation。当前同-key 规划已将来源提交与完整投影分为 S2/S3；新的 `.4` tools 操作、最终投影及正式安装归 S3，原拒绝结果仍保留，不改名为通过。

## T575-S2-03：S3 代表性安装与真实 predecessor

S3 待执行：一个 Codex focused clean/local-workflow 样本，及真实 stable `.3` predecessor 的正式 split-maintenance 样本。要求 clean committed Guru source 的 `.4` 调用在真实提交后取得；未执行前不得声称 source_locked/native/下一 consumer 通过。

远端 immutable 最终 candidate、最终 predecessor gate 与 tag-pinned smoke 由 #575 Stage2 对同一 final main candidate 重跑。generic existing verifier 若与公开迁移合同不匹配，保留其真实失败及原 owner 前置。

## T575-S2-04：M 原生维护的历史分层事实

实际 source 为 S1 clean merge `404d3f4d7635b19fb2c9f0d6aa642e2f1bf925b4`，extension `0.7.0-guru.3`，匹配 Fork `2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0`。该结果属于本次 Task 的 M 边界，不是未来 `.4` 的正式来源证明。

- 原 tools owner 首次在 preset 阶段遇到目标 native 的 `spawnSync python3 ETIMEDOUT`；沿原同操作 recovery resume 后，实际返回 `tools_upgraded`、installed_version `.3`、`unverified=[]`。没有修改 timeout、重新准备备份或更换来源。
- 目标自身 installed validator 通过，新 native 对旧 Task 返回支持的 `maintenance_required` 诊断；该诊断只证明工具层，未提前转换 Task。
- 原 selected-task owner 实际返回 `task_resumed`。同 TaskId/generation/source/整体 scope 保留，五份原规划及历史副本与旧 committed bytes 一致，原始 Task 备份完整。真实 S1 PR576/head b6b8c906/merge404d3f4d 由原 Publish/Merge 核验并恢复为 delivered；历史四个 gate slots 为空，没有导入当前 pass。
- session schema3 的目标 native continuation 和实际 Completion 均运行；Completion 先返回 `evidence_pending`，维护 finalize 复跑观察后完成；后续 evidence refresh 选择实际剩余 S2，而非 completed。目标 current query 正确识别实际新 Delivery。
- 独立 worker 初次调用因 child context 的 `no_current_task` 被原 validator 拒绝；用官方 `TRELLIS_CONTEXT_ID` 传入 caller 既有 selection，新 round 核实匹配后运行。没有 bind/select、修改 session 或清除 context 绕过。
- main checkout 仍为旧工具，自己的 schema3 注入诊断不作为新目标的运行结论；没有扩张到其它 checkout 的升级。

上述恢复是实际观察；新的 `.4` source、隔离 predecessor、完整 rollback 条件仍归 T03，不从这些历史结果推断通过。

## T575-S2-05：实际内容卫生与测试价值

重规划前实际隔离扫描覆盖当时4343个 changed/new regular files，gitleaks exit0、报告为空；该结果只绑定当时 bytes，不覆盖后续三规划、当前贡献和公开文档的新差额。64个保护文件曾全部复核不变。本轮重新核对64个保护文件时，session/config/common/peer等63个保持；唯一 task.json 因原 Check rework→新 Activation 的正常公共状态写入发生变化，不能声称当前64/64不变。主 check 已复核整体 scope/source/历史 S1 身份保持。本轮另对当时4350个 changed/new regular files执行真实 gitleaks扫描，exit0、report []；159个 Python AST、3816个 JSON 和33个 bash syntax 检查通过，git diff --check exit0。此扫描绑定该轮实际文件身份，不覆盖写入本文的新差额；本文更新后由主 session 单独补扫自身。可执行权限、递归 bytecode/sidecar/residue 仍待独立 check 确认，本文不提前称通过。新增 case 只用于独立缺陷检测；计数、常量自比较或 fixture 自证不构成充分性。

## T575-S2-06：Docs 与完成语义

本轮按当前 S2 三规划完成独立贡献 reconciliation：requirements/design/trace 区分 canonical `.4` 来源与现存 installed `.3`，保留原实际测试及未验证边界。贡献保持 draft；S3 的完整安装与最终贡献收敛、首次 committed 完整 Review 后 promotion 及晋升后 fresh gates 尚未执行。当前 S2 的最终 Phase2/TaskCommit/完整 Review/Publication 和 Whole Completion/Closure/Finish 亦须各原 owner 的实际结果，本贡献不作通过断言。

本贡献未执行真实业务安装/升级、生产验证、累计多平台/native-host Release 矩阵或软件发布；不声明这些层次已通过。
