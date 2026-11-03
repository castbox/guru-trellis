# Requirements / Design / Test SSOT 使用规则

这是本项目的读取投影，不保存可变版本号或历史增量正文。

## Authority 与适用性

从 `docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md` 读取同一 RDT locator/version/status；再读取 `docs/architecture/README.md` 的关联 authority。版本不一致、来源缺失或关系冲突时，返回原 `guru-maintain-requirements-design-test-ssot` repair，不以本页旧摘要作答案。

原维护方先判断当前 Task、阶段、问题及候选适用性。旧 Task 可以通过不可变版本/Git 读取原 authority；无关共享 CURRENT 前进不强制换版或重写贡献。shared promotion 仍核对实际目标的 expected-current。

## 当前知识入口

先读三层稳定根及 current 入口的适用范围、目录查找方法和历史/未迁移边界，再用 `rg --files docs/{requirements,design,test}/current` 与稳定 ID/aliases、capability、behavior、接口或职责限定搜索。命中后读取完整单元，核原 owner 晋升依据、来源/状态及必要 R/D/T/Architecture 关系；总入口无需枚举单元，文件存在或搜索命中不建立 authority。当前、已接受目标、未确认、历史和被替代状态分开。未迁移范围只使用导航明确保留的原完整来源，不据目录存在宣称已切换。

维护方法唯一读 `.trellis/guru-team/skills/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md`；公共 profile、I/O 和出口读该 package 的 `SKILL.md` / `interface.json` / `references/contract.md`。本页不复制正文或公共 API。

## 原 owner 接续

普通 Task 从 `task_impact_sync` 进入；隔离贡献由原 owner 晋升为完整一致定义，必要 R/D/T/Architecture 追踪同步。`sync_required` 返回原 promotion，`revision_required` 返回原规划/实施，缺 baseline 返回 bootstrap/repair，`blocked` 保留真实缺口。Planning、实施、最终 Check、独立 committed Review 均实际消费该方法。知识晋升不证明 Delivery、Task Completion、软件发布或业务采用。


采用 `knowledge-navigation-1` 后，独立主题不登记根/current README 或共享 index/manifest，也不递增无关版本或追加合并历史；只维护所属完整正文、能力局部导航与真实受影响关系。真实同能力/关系重叠归原 owner 整合；Git 自动合并不证明语义一致。入口自身合同变化才维护入口。安装新规则与项目文档切换分别判断；旧 Task 读取兼容不授权回写已退休索引。切换与恢复读 `trellis/presets/guru-team/MIGRATION-711.md` 或匹配 provider 的同一合同。
