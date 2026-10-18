# Requirements / Design / Test SSOT 使用规则

这是本项目的读取投影，不保存可变版本号或历史增量正文。

## Authority 与适用性

从 `docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md` 读取同一 RDT locator/version/status；再读取 `docs/architecture/README.md` 的关联 authority。版本不一致、来源缺失或关系冲突时，返回原 `guru-maintain-requirements-design-test-ssot` repair，不以本页旧摘要作答案。

原维护方先判断当前 Task、阶段、问题及候选适用性。旧 Task 可以通过不可变版本/Git 读取原 authority；无关共享 CURRENT 前进不强制换版或重写贡献。shared promotion 仍核对实际目标的 expected-current。

## 当前知识入口

通过三层 `current/README.md` 按 capability、behavior、接口、职责或稳定 ID 定位完整单元，实际读取其定义及必要关联。当前、已接受目标、未确认、历史和被替代状态分开。未迁移范围只使用导航明确保留的原完整来源，不据目录存在宣称已切换。

维护方法唯一读 `.trellis/guru-team/skills/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md`；公共 profile、I/O 和出口读该 package 的 `SKILL.md` / `interface.json` / `references/contract.md`。本页不复制正文或公共 API。

## 原 owner 接续

普通 Task 从 `task_impact_sync` 进入；隔离贡献由原 owner 晋升为完整一致定义，必要 R/D/T/Architecture 追踪同步。`sync_required` 返回原 promotion，`revision_required` 返回原规划/实施，缺 baseline 返回 bootstrap/repair，`blocked` 保留真实缺口。Planning、实施、最终 Check、独立 committed Review 均实际消费该方法。知识晋升不证明 Delivery、Task Completion、软件发布或业务采用。
