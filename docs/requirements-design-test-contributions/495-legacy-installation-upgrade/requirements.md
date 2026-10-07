# #495 旧安装单向升级需求贡献

状态：task-owned candidate，本轮范围修订须 fresh review，未 promotion。需求来源为 [#495](https://github.com/castbox/guru-trellis/issues/495) 与[混合库存说明](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6014030676)，本贡献承接正式规划的 MIG-495-01..09；current authority 仍为 `.71/active`。

- `R495-01`：支持精确 core `0.6.16` / Guru `0.6.16-guru.41` 来源。写前 inventory、逐文件/任务预览、AI 语义审查与对话内副作用确认；来源和目标均不可凭版本号推断。
- `R495-02`：真实更新 core、workflow、Guru preset 与 provenance，保留业务代码/spec/规划、有效配置、平台定制及无关 dirty/untracked；有效设置允许官方必要 additive 配置，历史归档、journal、identity 和 traces 原字节保留。
- `R495-03`：完整/精简旧活动 task 转换为 current schema；保留合法非 UUID TaskId，明确 generation/source/关系/未知字段处置，退役 active personnel，不推断关闭意图。
- `R495-04`：planning 保留身份/规划进入当前规划；未发布 in_progress 保留已有 commit 与未提交业务工作，经 fresh 当前规划审查进入 dev/check。必须实际执行 current identity/branch/checkout/session owners、真实脱敏项目 Architecture baseline、两类 qualifications 与语义 gates，不能以结构/schema pass 替代接续。
- `R495-05`：已有 PR、merge、旧 Finalizer/Finish 在途逐案读取 live facts，给出具体处置；旧 gate 不成为 current pass，不重复外部副作用。
- `R495-06`：私有备份与普通部分写入恢复；真实更新与转换后、尚无新版业务工作时支持回退并证明旧 runtime 可运行；部分迁移暂停期间或完成后出现新工作均禁止覆盖式回退，resume 不得吸收新增事实重置基线。
- `R495-07`：通过 Fork 正式迁移实现和固定 source lock 集成；当前普通 runtime 继续 current-only。验证 source/installed、canonical/dogfood、声明平台投影、inventory/runtime、reapply/drift 与零 sidecar。
- `R495-08`：合法 current/已迁移目标与无关 known-legacy active 共存时创建及 ref/id/branch/checkout/session 正常运行；旧记录仅保留 id/ref 占用，direct old、目标占用/同身份冲突和坏 current/JSON/id 仍拒绝。迁移允许已诊断 deferred 旧记录原地保留，核心与 installed inventory 接受 reviewed preserve；未诊断遗漏仍阻塞，不恢复旧 runtime 双读或 all-converted 声明。

本贡献仅替换 #481 的“不提供独立旧安装迁移”决策适用边界，完整继承其无人员模型、current-only reader、历史只读与 TaskId 防复用。已发布 tag、历史正文不变。完整累计多平台矩阵、真实业务安装、版本发布和自动关闭不在范围内。
