# 发布消费者与当前输入清单修复实施计划

## 1. 输入与引用

读取整体 `../../prd.md` 与本批PRD/design全文。唯一来源设计处置在design第3节，11项current登记及Sync被引用分支在design4.4；不复制另一支持清单。当前Task/gen1/DeliveryKey与planning_root从原公共current取得，保固定B `b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec` 和已有完整增量。

工程authority为 `.trellis/spec/preset/installer.md` 的AGENTS及平台选择、`.trellis/spec/workflow/data-contracts.md#public-skill-io-current-fields`、quality-guidelines的Test And Validation Value/Validation Scope Ownership。必要迁移来源是canonical MIGRATION-812/813/819；后继采用顺序来自私有release合同Complete Source Before Actual Adoption。原R724/R630的完整R/D/T及Architecture authority按design第9节承接。

本批source目标为八文件，不包括installed副本或旧schema：五个现有verifier/test、`trellis/guru-team-extension.json`、新 `trellis/presets/guru-team/MIGRATION-861.md`、同目录README。official implement/check JSONL经原task.py add-context维护必要真实file/reason，不写runtime状态、授权或新的handoff。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置/owner | 文件与动作 | 完成观察 |
| --- | --- | --- | --- |
| I1 | 当前完整计划接受后，原Activation；实施coordinator | 消费真实approved token，原公共Planning写入；每次写前fresh checkout boundary | 同key implementing，不重复旧Activation |
| I2 | 已选清单合同；Trellis implement worker | canonical manifest只退出design4.4的11项独立登记；完整核当前structured输入来源、保历史schema及Sync3.0→2.0引用 | actual current input exact；typed outputs/原selector/所有schema字节保持 |
| I3 | I2同批，原installer测试owner | 保已有Wording退役修复；原manifest测试从current声明取版本并处理conversation无JSON输出，保持exact集合；不恢复退役helper | 同一真实install_assets后的完整manifest test通过，用户修改保护保持 |
| I4 | 既有三项已审机制，原matrix/native owner | 保完整AGENTS preimage→原renderer gate与全部调用链、native每root适用集合及回归；只修当前发现的同范围遗漏 | V2/V3及实际focused覆盖充分，无分发/renderer额外修改 |
| I5 | 既有兼容边界；原source文档writer | MIGRATION-861完整说明current登记、仍被引用分支、原provider恢复及安装采用；preset README原迁移段只加入导航 | 不新增MANAGED_SOURCE_PATHS、decoder或支持期；准确可发现 |
| I6 | I2–I5完整；工程验证owner | V1–V4/V6，采用仍适用的原事实并补新manifest真实after | source独立可交付，无真实checkout采用冒充 |
| I7 | 完整真实after及工程结果；原RDT/Architecture owners | 复核知识差额，必要整合完整target并readback；没有变化不制造tracked证明 | 所有必要after进入同次TaskCommit范围，仍待独立Review |
| I8 | 原TaskCommit及独立Check/Branch Review、readiness/Publish owners | 展示精确commit/Publish计划，各原边界后执行；形成完整B..H和真实Refs-only PR | 当前gate/PR事实明确；Merge由独立原owner边界控制 |
| I9 | 当前source Delivery实际delivered；原Completion/Creation | additional_delivery_required→同Task后继采用Delivery，独立Planning/Activation | 不提前创建或选择，不用未交付commit |
| I10 | I9真实干净源/采用前置；后继tools/验证owner | source_locked采用准备checkout、V5完整existing；全部责任后再Completion/Closure/Finish | 未实施采用保业务缺口，未满足existing不Whole Completion |

原三项代码增量不能被新分配的worker覆盖。worker只拥有明确文件，发现规划外候选时在新增编辑/测试前返回coordinator。每个touched非生成代码≤3000行，逼近阈值先作职责内小拆分判断。

## 3. 验证入口、输入与预期观察

### V0 运行前置

Python执行设置 `PYTHONDONTWRITEBYTECODE=1`，使用source managed wrapper：

```bash
PYTHONPATH=trellis/presets/guru-team/scripts/python:trellis/skills/guru-team \
bash trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime -B -m unittest <实际test名称> -v
```

`GURU_UPSTREAM_DELIVERY_SCRIPTS` 取固定Fork的 `packages/cli/src/templates/trellis/scripts`。`FORK` 由验证owner在调用期解析为本机已干净且已构建的完整匹配checkout，不新增本机映射；HEAD必须等source lock的 `e3793251fad8bd261d0c370d408c7675b9f6a140`、CLI/Core `.6`；不改Fork/全局包或包管理器声明。前置失败不算功能证据。

### V1 原installer与current inventory

执行原 `test_apply_guru_team_trellis_preset.PlatformOverlayInstallerTest.test_default_platforms_install_claude_codex_cursor_and_shared_overlays`、`ExtensionManifestInstallerTest.test_install_assets_writes_installed_extension_manifest` 与 `Phase0TranscriptOwnerBindingTest`。原manifest test使用真实install_assets后的installed extension，独立对比active Interface当前JSON input/output exact集合；conversation输出按其原合同不贡献schema，不能漏掉任何structured输出。核11项旧独立登记退出current，全部原schema与Sync3.0引用及当前selector保持字节。保已通过且未受改动影响的用户修改保护与退役产物观察。

原完整受影响模块的首次真实失败保留。按其当前归因区分范围内manifest/退役问题与范围外旧固定计数、文本布局、Phase0旧shape或全Git历史断言；不能删测试/改生产掩盖后者，也不能把全模块结果报告为pass。新真实supported consumer影响本切片可交付时回原资格/范围owner，不因红测自动扩张。

### V2 AGENTS/hash与调用链

采用原受影响模块中AGENTS/hash、focused、existing cell调用链的仍适用执行事实；对本批后续触及的部分补同入口定向回归。覆盖旧受管块合法替换、append/幂等、独立prefix/suffix、原template hash bytes、source equality单独不得放行、首次preset后late capture拒绝及后续未知正常编辑失败。fixture只建立合法preimage，不替被测gate修after。当前这些verifier/test机制未被manifest修复改变，不要求惯例旧版红绿或重复rollback。

### V3 Native平台集合

完整 `test_verify_native_platform_load` 已有9例行为覆盖可在内容未变时采用：合法shared fixture、mixed Codex-only、Claude/Cursor排除、Codex包含及真实missing/extra。原三平台focused亦可用于未变verifier行为；它们不证明新manifest已安装。

### V4 新manifest实际安装after

先核workflow、registry、受管投影、source lock与固定B不变，清楚记录当前source dirty。原三平台focused的clean/two update/reapply、平台parity、完整bytes/modes/lock/workflow/零residue事实在未变对象上采用。新manifest后执行一次新的Codex focused：

```bash
NODE_OPTIONS=--dns-result-order=ipv4first \
TRELLIS_FORK_SOURCE="$FORK" \
TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec \
bash trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh <新临时目录> --mode focused --platform codex
```

对原Claude/Cursor focused目标，用当前canonical source原 `apply.sh --repo <该独立临时target> --platform <相应平台>` 正常reapply；这些临时target没有历史Task迁移阻塞，不对repair/主目录普通apply。若遇到guard/冲突，保真实结果并回原owner，不绕过。分别核完整managed_source_projections集合/bytes/modes、实际extension.public_api与canonical current清单、source dirty provenance、CLI、lock、workflow、无旧Codex受管根/私有release Skill/私有tests及零sidecar/residue。用 `capability_projection` 与 `installed_capability_projection` 观察current清单被真实consumer读取；与repair checkout的旧installed清单区分，不手改它以制造相等。

只补受manifest变化影响的安装/consumer证据，不重复已充分且未变的三平台完整focused。当前workflow immutable b85只用于未变workflow字节；source dirty不冒充新candidate或formal source_locked，不声明实际Agent行为。

### V5 后继实际采用与完整existing

当前source修复实际合main后，以包含本批的干净完整commit C为source。原Completion/Creation再建立并规划后继；该Delivery使用原guru-upgrade-tools preview/prepare/invoke执行source_locked，验证准备checkout的实际installed清单、完整受管内容、真实provenance、CLI/source lock、native entry、mode/sidecar及Task/session/peer/config保留。

完整existing用同一已交付源、真实前驱 `v0.7.0-guru.9` 和从其manifest/lock推导的实际Fork/CLI，沿原入口：

```bash
TRELLIS_FORK_SOURCE="$FORK" \
TRELLIS_PREDECESSOR_SOURCE="$BEFORE_FORK" \
TRELLIS_PREDECESSOR_COMMIT="$BEFORE_COMMIT" \
TRELLIS_WORKFLOW_SOURCE="gh:castbox/guru-trellis/trellis#$C" \
bash trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh <新临时目录> --mode existing --platform codex --before-tag v0.7.0-guru.9 --before-cli "$BEFORE_CLI"
```

变量均为原owner实际解析事实，不是新发布输入。必须取得完整matrix结果，核retired assets/hash gate/platform集合及零sidecar；tools_upgraded或局部target检查不能替代。当前source未交付时不运行失败占位，不预填后继证据。

### V6 必要质量与分发边界

执行原source `check-skill-packages.sh --root . --mode source --json`、目标自身installed版本同入口、`check-upstream-ownership.sh --repo . --json`、`check-dogfood-overlay-drift.sh --repo .`，完整managed byte/mode检查、变更Python in-memory compile、`git diff --check`及 `.pyc/.pyo/__pycache__/.new/.bak` residue。检查公开README/MIGRATION链接真实可解析。

repair checkout installed manifest在后继实际采用前保持原provenance事实；原dogfood验证结果只覆盖其实际层级，不把source package通过当已采用。source manifest current清单及临时安装验收由本批负责，不能转交后继补本source缺陷。累计全平台/全历史Release矩阵、secret scan/tag/smoke/Release/主目录收敛继续由后继Stage2按新候选负责。

## 4. 停止条件与适用回退点

身份/checkout/current selection/authority stale按原Identity/Ensure/Bind处理，保Task/gen1/key。scope、renderer、registry/platform能力、runtime selector、持久化或source lock实质变化回Clarify/Author/Architecture；worker不得自修规划外候选。

原必需验收FAIL/SKIP/缺证据不推进依赖阶段；保第一真实失败。设施重复失败时重评原方法及具体缺口，不无限重试或弱化matcher。证据充分后停止可选实验；不以任何旧pass替本轮实际after。

本批没有业务部署或数据迁移，无新rollback协议；普通本地编辑保无关改动，绝不reset/revert他人。commit/Publish/Merge等各由原owner精确展示和独立边界控制，不从规划推导远端动作权限。

## 5. Delivery Policy（唯一）

**partial：**当前选中切片完整交付D-R1–D-R5的四项source/consumer修复、公开兼容说明及D-R4对应工程/知识整合；D-R6承接source可独立交付与有序后继的责任分配。当前source切片的通过条件是全部本批source/consumer功能和V1–V4/V6充分，不依赖未来checkout已采用它。所有当前修复代码同批，不把已确认source缺陷延期到采用或发版后。

**明确剩余责任：**新的可分发manifest触发真实准备checkout source_locked采用，当前尚未实施，是同Task后继业务Delivery。只有本批实际delivered，原Completion返回additional_delivery_required，原Creation才建立/选取/规划后继；不提前分配。后继采用以本批完整干净交付源为前置，并完成V5真实前驱existing。采用未实施不是evidence_pending；采用业务完成而existing仅缺合法外部证据时，原Completion才按真实缺口判断evidence_pending或修复路由。全部采用、完整existing和整体责任满足后才whole Completion/no_mutation Closure/Finish。

本批source、后继采用与最终Stage2分别保持真实内容身份。当前source可经独立Review/readiness/Publish形成PR；其Merge有独立边界，source交付事实不能由local commit或PR Ready代替。后继正式发布仍从届时最新main重新冻结，不增加其他Issue状态依赖。

## 6. Docs SSOT Plan（唯一）

strategy：`no_docs_update_needed`。本批恢复data-contracts Public Skill I/O Current Fields的既有current清单合同与MIGRATION-812/813/819的原迁移边界，不新增产品能力、runtime支持或知识语义。原三项继续由R724-02/D724-01/03/T724-01/04及R630-04/05/D630-04/T630-05/07完整单元承接。MIGRATION-861及README导航是本source的必要公开说明，不代替RDT权威，也不在共享current重复原合同。

原 `guru-maintain-requirements-design-test-ssot` 在I7按真实after复核命中单元与必要关系；若出现真正知识差额，在TaskCommit前由原owner整合完整target/readback，提交后一次独立Review审actual after。Architecture按本轮独立candidate/final_plan执行，无影响不造空contribution/ADR。不得用本计划no-change推定免除真实维护，也不追加跨Task总索引或版本登记。
