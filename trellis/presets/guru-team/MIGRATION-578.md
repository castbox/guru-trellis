# #578 工程执行事实采用迁移
本次仅修改现有Architecture、Check、BranchReview及直接派发的检查适用性合同；原Skill/phase/exit/公共DTO、独立语义审查、当前freshness和private checkpoint退休不变。没有验证账本、缓存协议或兼容reader。

完整当前审查先确定范围、消费者、风险和所需检查，随后核查合法可访问的原始工程命令结果。定义/版本、真实依赖、工具链、参数、环境和测试期望仍适用时，由当前owner在已有summary中注明采用、原执行来源和适用理由，并生成当前候选结果绑定。条件变化、未知、结果缺失或新义务执行受影响检查。旧semantic pass/旧token不是原始执行事实。

## 采用
新安装采用完整匹配Trellis/Core/Guru来源和preset。现有安装由原 `guru-upgrade-installation` 或当前工具维护合同执行完整升级；不得只替换三个Skill或某份workflow，不热补丁活跃Task。升级后原任务由同一TaskId/generation和原owner读取真实当前候选/authority/可访问原始结果；无法验证适用性只补跑对应检查，不要求保留退休checkpoint。
当前开发Task的安装合同保持；产品验证在独立matching source dogfood执行完整apply/reapply/drift和声明平台投影。具体实际证据见 [唯一Test](../../../docs/requirements-design-test-contributions/578-cross-owner-validation-facts/test.md)。

项目级检查范围由 [ABTest #421](https://github.com/castbox/abtest-guru/issues/421) 和 [Backend #607](https://github.com/castbox/ai-chat-roleplay-backend/issues/607) 各自拥有。本文不宣称这些项目已经安装或消费，也不替代其业务/部署证据。完整多平台Release/Upgrade矩阵仍归专门owner。

