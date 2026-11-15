# 必需正文读取的设计职责

Identity：`RDT-DES-REQUIRED-CONTRACT-READING`；检索别名：`D848`、首读导航、provider-aware reading。原语义 owner：`guru-maintain-requirements-design-test-ssot`。承接 `docs/requirements/current/required-contract-reading.md` 的 R848；验证关系为 `docs/test/current/required-contract-reading.md` 的 T848。适用基线为 Git `0fb7dc9aac817a684c2f95bebb6570061a5ef868`，版本由本单元的实际 Git 内容定位。repository-relative locator 从仓库根解析。

知识状态：本候选已实现的设计，验证范围见 T848；共享整合及正式质量判断分别由原 owner 完成，不从文件位置推断。

## D848-01 / CON848-METHOD：唯一方法与判断职责

`trellis/presets/guru-team/spec/workflow/companion-scripts.md#reading-required-contracts-in-full` 单独拥有完整操作方法。当前 AI 根据确需正文、已有完整上下文和真实工具选择直接读取、补显或补读，亲自核验全文及文件尾。分段大小、预算请求及显示结果不成为脚本评分或自动通过条件。

执行顺序为：确需范围/完整上下文复用 → 容量允许时显式两层预算直接读 → 核对实际显示 → 依据内层缺失或仅外层截断补读/原内存补显 → 原 owner 的依赖判断。prose 已读结果只使用既有调用内存；跨调用补显需原结果真实存活，局部变量失效时按原方法补读。结果消费后释放引用，没有新增缓存服务、文件状态或生命周期。

选取直接修改原方法及薄导航。新增 reader 无法保证模型已获得正文，却增加 API 和状态；一律先固定行数分段会保留预算/首读缺口。因此采用原 AI 职责内的工具选择和实际显示核验。宿主名义参数未生效的内部原因保持未知，不以该方案宣称已经修复。

## D848-02 / CON848-ENTRY：导航与 provider 边界

原 installer 的 `AGENTS_AI_FIRST_BLOCK` 只分发短节 locator。canonical workflow 的 Phase Index、continuation/caller 及现有 descriptor-bound Guru finish payload 在首次长文要求前引用 installed 小节；JSON/TOML 等原生载体保留原格式。没有新增 launcher、upstream hook 或 `trellis-*` 修改，也不批改全部 Guru Skills。

`trellis/skills/guru-team/packages/guru-review-change/SKILL.md` 先解析完整 provider，在其 workflow-spec root 读取原短方法，再读取同源写作及审核充分性正文。source root 为 `trellis/presets/guru-team/spec/workflow`，installed root 为 `.trellis/spec/workflow`。缺失或不完整 provider 回原来源/安装 owner，暂停依赖判断；不混用 target 中另一版本。原入口的独立视角、只读范围及正式出口保持。

## D848-03 / CON848-RESULT：prose 与原 producer 结果分开

原 `Intermediate Command Stdout 1.0` 继续拥有 JSON/receipt/typed exit 的完整 stdout 消费与结果恢复。prose 补显例子不应用于按片段重构结构化结果；输出丢失由原 owner 恢复同一已执行结果，不触发第二次 mutation。不存在新公共字段、schema、状态或 recorder。

## D848-04 / CON848-DISTRIBUTE：受管采用

规范通过原 managed-spec 分发，Skill 与各 native payload 通过原 package/preset 分发。完整匹配源由原 `guru-upgrade-tools` 对既有 checkout 采用，保护用户正文、配置、Task/session、controls 和 peer；不手工覆盖 installed 副本。原冲突及 `.new/.bak` owner 继续处理。local_candidate 的 source-lock 局限不能改称正式发布资格。

长期分发测试复用 `test_clear_technical_writing.py` 的真实资产安装/reapply fixture，解析实际 native payload 和引用，验证同源短节、顺序、用户内容及再次安装。实际 Agent 行为、当前 checkout 安装和机械分发各自验证；没有因分发通过推断模型行为。

现有 R717/D717 的共同审核 owner/provider 分工保持。Planning 的原独立 Architecture candidate/final 判断为 no impact：本设计不改变 Architecture 决定、公共 I/O、状态、持久化、gate 或恢复边界，因此没有空 Architecture contribution/ADR。实现后的正式 committed before/after 仍由原独立 Review 判断，不由本文预填。
