# #792 需求贡献

状态：proposed；strategy为delta_first。原RDT owner维护，当前authority为guru-trellis-rdt；固定源为05a16a5989669ca216d8ba34b9b419776410f04d。直接要求来自[Issue #792](https://github.com/castbox/guru-trellis/issues/792)，本Task D1完整承担五项行为及三项验收。

完整拟写为[生命周期Requirements](proposed/docs/requirements/current/task-delivery-lifecycle.md)的R792-01..05/BEH792，保留该单元全部原条件。新增当前出口一次查询、正常按当前步骤加载、legacy实际入口读取及matching采用，不改阶段/原AI判断/#793条件，不实施#794/#734。没有未分配后继实现。

本目录是隔离候选，不能因文件存在成为current；原candidate Check后由原RDT owner在final_integration整合完整current单元，最终candidate/Check/Review覆盖实际after。关系见[traceability](traceability.md)。
