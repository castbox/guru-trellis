# D1 tools-only peer 增长与冻结源恢复实施计划

## 1. 输入与引用

输入为整体[PRD](../../prd.md)、本批[PRD](prd.md)和[design](design.md)；来源设计处置只由design第3节拥有。B/H0为a5f3ceeabbaccddae65935d97763f5a798f71ca9，首次Delivery，无前序实现。实施前加载tools package完整合同/Interface、tools_owner.py与受影响tests，quality-guidelines的Test And Validation Value/Validation Scope Ownership及clear-technical-writing。独立candidate_assessment只批准候选方向，不替代当前最终规划门禁。

## 2. 有依赖顺序的步骤与文件责任

1. P1，Author：完成当前三正文、正式implement/check context及真实隔离Architecture/RDT贡献。经Wording、同一独立Architecture final_plan、Approval及Activation后才能实现。
2. P2，实施owner：只改trellis/skills/guru-team/packages/guru-upgrade-tools/、必要公共exit consumer及MIGRATION-769。先实现原观测键保持与新peer物理隔离，再薄复用原engine增加recover_frozen_source及独立retry消费。不得改旧事务或#766代码。核查实际复用参数在每阶段已存在且可用。
3. P3，实施owner：补V1–V3长期回归，运行受影响package与source validator。原helper/preset必须来自原资产源；覆盖preset pending、complete不再安装、retry保持action、rollback顺序和原freshness拒绝，不复制引擎。
4. P4，原tools owner：从完整修复源按guru-upgrade-tools合同同步#769安装投影，保Task/session；核mode/sidecar、installed/native与drift，不手改manifest/hash。若同步产生真实缺口，由原owner恢复。
5. P5，原Architecture/RDT owners与Check：对全部实现和完整proposed差额独立phase2、candidate Check，再final_integration/readback；重建完整candidate、begin_check、最终Architecture/Check、精确commit和独立完整B..H Review，原Delivery Review/Publication/Merge交付。
6. P6，原tools owner：从交付后的完整修复源对#766原ref执行V4，保原source bytes、public plan与备份，记录最小真实恢复结果。随后#769整体Completion/Closure/Finish。#766回自己的原Task owner继续质量和交付链。

主协调者拥有规划、贡献和正式交付；实施owner不单独写shared current，不覆盖并行工作。所有新finding先证正常受支持路径，机制变化回原规划/Architecture。

## 3. 验证入口、输入与预期观察

- V1/V2：在package定向unittest中使用真实git init/worktree add与原peer观测入口；预期仅新增且隔离通过，原键值变化拒绝，peer内容不被写入。运行该包tests/test_contract.py、tests/test_recovery.py及新定向回归。
- V3：用正常旧owner begin生成checkpoint，执行新公共invoke.sh的recover_frozen_source/action；预期旧source绑定仍验证、阶段动作/旧public恢复复用、成功出口或新retry出口可由同owner消费。unit外部边界证据只按自身层级报告。
- V5：`python -m runtime.validate --root . --mode source --json`通过source resolver执行；实际安装后用其own resolver运行installed validator和get_context.py continuation。执行canonical `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`、git diff --check，并检查本操作sidecar/mode。所用python均由匹配managed resolver提供。
- V4：交付后用完整修复源guru-upgrade-tools公共invoke，对#766目标、action=resume、recovery_ref=05d804ba-1a5d-4975-93bd-9909ff00e719执行。同public operation=8838ed00-b7c3-4ab3-97cd-0fd392e0740b及原source/preimages保持；成功后独立读取目标resolver/installed/native。local_candidate仍保formal_fork_source_lock未验证边界。

按design第8节核需求到独立观察。必要回归通过且现场验收充分后停止额外实验。全多平台clean-install/upgrade/Release矩阵未纳入本批，不能据本批声称通过。

## 4. 停止条件与适用回退点

原source/plan/ref/preimages不一致、owned后续编辑、原peer值变化或不隔离时停止该操作，回原tools owner；不刷新snapshot或绕过校验。真实范围/机制变化回原Clarify/Author/Architecture，普通实施缺陷由原实施/Check修复。设施失败先准确区分未触达行为和实际缺陷，反复失败时重评复现方式，不伪造成功。

代码本地回退只限本次明确文件；工具回退只用原action=rollback和原preimages，先核public tools/data兼容，保并行修改。没有业务数据迁移或生产发布；不新增独立rollback协议。原#766现场不可用或恢复未成功时，#769 Completion不得通过。

## 5. Delivery Policy（唯一）

full：本批覆盖R1–R6及AC1–AC4，含兼容入口和真实#766恢复。Delivery质量、发布和合并先完成；合并事实不等于Task完成。后续从已交付源执行原#766恢复是整体Completion的必要验收，不产生另一功能切片，也不以旧工具成功证明#766业务交付。兼容入口只服务修复前schema1.0事务，终态及原保留责任结束后由明确迁移处理删除，不建自动清理流程。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原RDT writer维护docs/requirements/current/runtime-location.md、docs/design/current/runtime-location.md、docs/test/current/runtime-location.md的完整隔离proposed单元，补充原peer观测与新增peer区分、修复executor/原资产源、明示恢复及证据边界；直接consumer为本批实施、Check及后继维护调用方。原Architecture writer维护隔离完整runtime-location和ADR-TOOLS-FROZEN-SOURCE-RECOVERY候选，九concerns明确适用性。

candidate Check前shared current保持；原owners在final_integration核live目标、整合真实差额并readback，之后重建candidate与最终质量门禁。Test只记录实际执行与未验证边界；现场V4在交付后发生，其最小结果由Completion消费，不提前写成已成功。package合同、Interface、schema/examples、MIGRATION由实施owner更新，直接consumer是工具调用方和retry路由。无需修改共享根/ADR索引来登记主题。历史ADR和旧证据保原观察。
