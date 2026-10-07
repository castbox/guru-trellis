# ADR-017 版本系列来源扩展候选

状态：proposed supplement；不修改 accepted ADR-017 历史。

决定：支持全部 `v0.6.x-guru.*` 和 `v0.7.0-guru.*` 正常安装向后继目标升级，以实际安装清单、资产 ownership 和 task/control 合同分组，不用代表 revision 限制支持。显式 migrate 与 Guru upgrade 是唯一一次性边界，普通 runtime/current owners 不长期双读。

理由：release 后缀不等于实际 extension，版本也不等于 task 格式。分组既覆盖正常路径，又避免每 tag 重复相同测试。旧 receipt 不完整时核验旧 source bytes，本地定制保留；每来源备份/回退真实 before，升级后的新业务工作阻止覆盖。

代价与退出：family selector 同步公共 schemas/consumers/docs；旧 fixed selector 不留 alias，已发布 tag 不变。正式 lock/CI、代表 actual 升级/恢复/回退及同源远端验收完成，独立审查和受控 promotion 后才接受本补充。完整 Release matrix 与真实业务升级仍为独立边界。
