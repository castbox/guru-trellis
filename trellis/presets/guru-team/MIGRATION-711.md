# 并行知识导航隔离的采用与迁移

`knowledge-navigation-1` 是文档组织的采用边界标签。它不是公共 Skill API 版本，也不要求普通任务递增共享版本。完整方法唯一位于 [current-knowledge.md](../../skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md)。RDT 与 Architecture 原 owner、profiles、公共 I/O、阶段与 runtime 保持。

## 1. 先安装匹配规则

1. 固定同一完整 Guru source 的实际可取得 revision。已有 checkout 仅维护工具并保留 Task/session 时，加载该 source 的 `guru-upgrade-tools` 完整合同，由原 tools owner 执行。新安装使用 README 的完整 workflow/preset 入口；符合 current-only 前置的完整 reapply 使用原 installer。不手工覆盖受管 Skill/spec 或绕过 Task 库存门禁。
2. 若本次需要更新 workflow，使用同 provider 的 `trellis workflow --marketplace <matching-provider> --template guru-team --create-new` 预览。原 owner 核对实际差额、用户修改、sidecar 与 live identity 后，才以同 provider 的 `--force` 应用。本项不改变 workflow bytes，不为形式重写 workflow。
3. 验证 canonical、shared installed、所声明平台与 managed-spec 正文、mode、reapply 和 drift。由原 owner 逐项处置 `.new`/`.bak`，保留用户内容与 Task/session。安装器分发规则，不选择或迁移项目 docs authority。

安装完成只证明相应规则已分发。项目文档是否完成下面的切换单独判断；源码、dogfood 和业务项目采用不能互相代替。

## 2. 原维护 owners 准备项目候选

1. 固定旧完整 Git revision，记录所有旧根/current 入口及可读的完整来源。读取本阶段适用版本，列实际读取者、写入者、目标能力、稳定 identity/aliases、必要 R/D/T/Architecture 关系和未迁移范围。此清单属于本次隔离贡献，不建立日后每 PR 必写的共享登记。
2. 在 Task-owned contribution/proposed 内准备每个实际修改目标的完整 after 正文。RDT 采用现有 `docs/{requirements,design,test}/current/<stable-capability>.md`；Architecture 保留其职责目录。多文件能力可用自身目录的局部 README。修改既有能力沿原完整正文整合，不以 Issue 建第二 current。
3. 将根/current README 改为稳定体系身份、范围/状态、真实版本引用、历史/未迁移边界和限定查找方法。它们不逐项枚举全部单元。逐一对照旧导航 alias 与所属正文；缺失 alias、状态、来源或晋升依据时，只补所属完整单元，保留原语义和必要关系。
4. 调整实际读取投影，使用稳定入口→限定目录与稳定 ID/概念搜索→完整正文与必要关系。搜索命中、文件存在、日期、排序和更大版本都不能证明 current。读者核原 owner 晋升依据与适用来源；accepted target、未晋升 contribution、历史和 superseded 分开。

## 3. 切换条件与原质量链

候选必须保留全部仍有效的条件、否定、例外、顺序、兼容和稳定引用。原 owners 核完整性、traceability、旧 alias 可发现性及适用的真实样本：独立主题组合、状态区分、真实重叠、迁移和结构变化。原独立 Architecture 与候选 Check 审完整 proposed 和受影响未改消费者。

条件未满足时，原共享入口及完整 authority 保持可读；候选标 proposed/incomplete，明确未迁移范围和受影响结论。不能声称已消除共享索引写入。

实际 `candidate_checked` 后，原 RDT 与 Architecture owners 各自固定一次真实目标 branch/commit，重读目标和贡献，整合仍有效条件，再实际写入并读回全部目标。两任务共同修改同一能力或有效关系时，比较 base、双方完整 proposal 与实际 target；Git 自动合并不替代组合语义审核，不只取一侧或复制关系规避重叠。真实变化回原适用性/质量 owner。

随后 implementation 重绑全部实际 after，完成匹配最终 Architecture/Check、TaskCommit 和完整 committed Review。只有实际受审切换后的入口和单元采用新写入合同。后续独立新增或修订只维护所属完整正文/局部导航及真实关系；不再双写旧根/current 索引，也不把登记转到共享 manifest、metadata 或每 PR 提交的生成索引。入口自身合同真正变化仍由原 owner 修改。

## 4. 在途任务、结构变化与恢复

旧 Task 继续读取其计划/阶段适用的不可变版本或 Git。其旧普通读取在 Task Finish、合法 Reactivate 改选或真实依赖变化后退出。最终整合触及已迁移单元时，原 owner 重读真实目标并写入当前完整单元；旧读取兼容不授权回写旧索引。未触及的历史范围不因本项重做。

改名保留稳定 ID。替换、删除、拆分和合并维护仍有效引用、前驱/后继及精确替代范围。旧路径需要解析时只保转换 locator 或固定 Git 引用，不留另一份活动完整正文。不可变版本、历史快照及原始失败证据保持原义。

切换前失败保留旧入口与 proposed，沿原 repair/澄清修正。切换后普通问题沿原 repair 或受审 successor；partial/output-loss 只恢复原 owner 可唯一确认的 intent，读回 completed、补 pending，冲突或意图不唯一时停止。无第二 current、迁移台账、锁或新恢复状态机。

## 5. 本仓代表迁移与证据边界

本仓旧来源为 `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/` 的完整 tree；三层根与 current/README 保留原身份、历史 Git 及 `.109` 未迁移来源。目标为稳定发现入口、原能力路径及必要缺失 aliases/状态/来源补齐。Architecture 根改为职责目录发现，原具体单元继续拥有身份、状态和关系；变更合同及治理正文由原 Architecture owner 晋升。候选完整 targets 位于 #711 的隔离贡献，存在候选不表示已切换。

旧 `.109` 未列入原迁移映射的语料保持 `legacy_unmigrated`，原固定 Task 与 predecessor Git 引用保留。本项不宣称整个历史语料已迁移，也不修改业务仓库。

唯一实际结果由 `docs/requirements-design-test-contributions/711-knowledge-navigation-isolation/test.md` 定位。分别报告确定性两序合并、实际 Agent 原入口读写、分发/安装和本仓文档切换。一个代表 clean 安装可复用；完整多平台 Upgrade/Release 矩阵和业务采用不由本项证明。方法或目录存在不能替代实际行为证据。
