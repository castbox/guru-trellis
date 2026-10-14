# #556 设计

## 对象、职责与 Architecture

唯一 Direct Source 为 [Issue #556](https://github.com/castbox/guru-trellis/issues/556)。bootstrap 继续拥有解释器探测、runtime identity、用户级 cache 与 active pointer；preset installer 继续拥有完整 source、staged assets 与最终激活顺序。日常 resolver/launcher 保持 managed-only，不新增更新器、全局 Python fallback、Skill 业务分叉或长期状态。

独立 candidate_assessment 实际返回 baseline_current/no_architecture_impact，绑定 Architecture current-main-0.6.17-guru.89、constitution v1。候选不改变 owner、identity 维度、GAP、shared Architecture decision 或 compatibility exit，不创建 Architecture contribution/ADR。final_plan、Phase2 和 committed Branch Review 仍由各原 owner 独立完成。

本工程 Task 由当前完整旧 dogfood 的 Planning3.0 生命周期承载，沿用仓库 #553 已明示的 pinned-old 边界；installed 校验已确认其内部完整。canonical 产品模型是 Task2/Delivery，两套 DTO/gate 不混用。产品安装验证使用独立的完整 matching source/installed 样本，源仓旧 dogfood 的 migration-required/drift 结果单列，不能计为当前 source parity 通过。

## D556-01 解释器选择

初始化、显式 apply/reapply 和 bootstrap 的默认输入为当时 PATH 的 python3，不再把 installer 当前 sys.executable 当成默认目标。显式 --python 指定一个命令名或路径并优先于默认；命令名按 PATH 解析，路径按调用语义解析并检查可执行性。选择失败即报告，不搜索其它 minor、不回退 active/global Python。

Bash apply 入口在启动 Python3-only installer 前处理 --python 的启动选择及无法执行/非 Python3 诊断；Python 入口与 bootstrap 对直接调用执行相同目标选择合同。保留直接使用明确解释器运行 installer/bootstrap 的可执行文档。受控 verifier、eval/source staging 等既有 managed runner 调用若要求保留自身解释器，以显式 --python 传入它，避免默认 PATH 更新行为破坏其原路由合同；不改变其业务语义。

## D556-02 版本判定与 identity

canonical python-runtime.json 删除 supported_minor_versions 列表，改为 Python major 3 及既有 CPython implementation 要求。bootstrap 不因 minor 未枚举而拒绝。解释器真实执行 stdlib 探测，identity 继续由既有 runtime API、layout、lock digest、implementation/major/minor、OS、machine、ABI/platform tag 计算；不加入 patch、解释器绝对路径、manifest 完整 digest 或授权。

同 identity 通过 metadata/依赖能力与本次公开 wrapper 检查后复用，不能仅因 patch/path 变化重建。minor、ABI、platform 或 lock 等既有 identity 输入变化产生对应环境。Python3 identity admission 与依赖 wheel/capability compatibility 分开观察；3.15 可计算 identity 不代表其依赖必然安装成功。

## D556-03 检查完成前不动旧环境

保留原 candidate → 验证 → target → active 顺序，在原 bootstrap 的 target 替换前补足真实 public wrapper 检查：

1. 解析选择、计算 identity；有效 cache 进入复用检查，缺失或损坏 cache 在本次拥有的独立 candidate 构建。
2. 以锁定 hash 和公开 package index 安装依赖，保留 venv/pip 前置和 Draft202012 capability probe；清除既有 pip/venv 注入影响。
3. 在一次性 validation view 中使用本次 candidate 或可复用 cache 的解释器，加载真实公开 schema-bound package wrapper 的 matching 源资产。该 view 只有自有 pointer/cache locator；普通路径或 cache alias 仅用于定位受测解释器，不承担业务授权、fencing 或进程身份。
4. 执行真实 public wrapper 的合法输入及一个受支持的普通输入错误检查，确认 Draft202012 schema 路径实际运行；现有 probe 覆盖 draft 关键行为。检查不产生真实业务路由/批准/发布效果，测试输入不能被宣称为真实用户的 semantic gate。
5. 上述检查通过后才完成 cache candidate 的正式替换/复用。preset source/installed staged validation 成功后才写目标 checkout active pointer；失败保持此前 pointer bytes 和此前环境。损坏同 identity 的 repair 也不得在 wrapper 失败前覆盖旧 target。未知来源目录保持原拒绝语义。
6. 只清理本次明确拥有的失败 candidate 与 disposable validation view；不清旧 identity 环境，不扩大 crash/concurrency/跨 OS 原子性协议。

bootstrap 的 public-wrapper 检查与 installer 的 staged graph 验证分别证明 runtime capability 和完整安装图；不能互相替代。真实 wrapper 所需 matching package 资产是前置条件，缺失即明确失败，不悄悄退成 probe-only 成功。

## D556-04 诊断与文档

缺失/不可执行解释器、非 Python3、implementation 不匹配、venv/pip bootstrap、锁定依赖安装和 managed public-wrapper 检查分别保留实际失败阶段与原因，输出稳定 JSON/退出码及具体修复命令，无 traceback。既有 resolver 的 missing pointer、missing/stale cache 与 dependency failure 分类保持。

错误只包含可安全公开的原因、退出事实和 remediation，不转发可能携带凭据的原始 pip/provider 日志。文档给出默认 apply/reapply、--python 显式选择及优先级、只读 identity 检查、失败重试/修复命令，并说明 patch/path 不强制 rebuild。文档不要求修改业务 manifest 或系统 Python。

## D556-05 文件与同步边界

生产修改以 trellis/skills/guru-team/runtime/{bootstrap.py,python-runtime.json}、必要 bootstrap capability helper 和原 preset apply 入口为中心。installer 主文件当前2980行；将其 managed Python plumbing 小范围提取到同目录单职责模块，保持其它 installer 行为。任何触及的非生成代码文件达到3000行时完成机械拆分审查，未知其它大文件不顺带重构。

沿原 managed inventory 交付新增 runtime 文件，调整必要受控调用方、相关 unit/真实安装 harness、preset/workflow README 及 canonical preset spec。canonical 与完整 current installed 样本同步；不把新 package 拼入完整旧 dogfood。原 source reapply/drift 的真实拒绝保持可见，source 安装迁移不由本 Issue 实施。软件版本轴不改变。

## 来源设计承诺的唯一处分矩阵

| 来源 locator / 原承诺 | 处分 | 当前落点、理由与影响 |
| --- | --- | --- |
| #556 目标1 / 初始化和显式更新用 PATH python3，保留明确解释器 | retain | D556-01，显式优先、失败不回退；受控 managed caller 显式选取 |
| #556 目标2 / 取消 Python3 minor 白名单，无 minor 矩阵 | retain | D556-02，major/implementation 与实际依赖能力分层 |
| #556 目标3 / 复用 apply/bootstrap/cache，成功切换、失败保留 | retain | D556-02/03，候选和真实公开 wrapper 通过前不替换旧 target/active |
| #556 验收 / 相同 identity 复用，patch/path 不保证重建 | retain | D556-02，identity 字段保持；不加入 patch/path |
| #556 目标4 / 实际失败原因与修复方法 | retain | D556-04，不再把未枚举 minor 作为原因 |
| #556 目标5 / canonical、安装投影、使用排障同步 | retain | D556-05 与 implement 的 focused installed/reapply；旧 dogfood 拒绝单列 |
| #556 验收 / 日常 Skill 隔离、锁定、不随 Homebrew 自动重建 | retain | 原 resolver/launcher 继续 managed-only，不加 fallback/自动更新 |
| #556 边界 / 系统、旧环境清理、业务升级、Release 不属于本任务 | retain | implement 的排除与后续 gate 边界，不引入第二更新流程 |

该 Issue 提供以上规范性接口/顺序/兼容约束，没有另一个必须照搬的外部实现设计。这里全部 retain，无 scope 或 source 承诺的静默修改。
