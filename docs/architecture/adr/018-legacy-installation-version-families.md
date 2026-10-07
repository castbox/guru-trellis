# ADR-018：旧安装版本系列升级

状态：`accepted`；knowledge baseline：`current-main-0.6.17-guru.74`；predecessor：ADR-017；来源：[#495范围修正](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6040798771)与[已审查贡献](../contributions/495-upgrade-version-families.md)。

支持全部 `v0.6.x-guru.*` / `v0.7.0-guru.*` 正常安装向后继升级；安装清单、ownership、task/control的实际合同分组，代表样本不是支持白名单。仅取代 ADR-017 Decision 6 的固定来源限制，并明确 Adoption 的分阶段候选交付顺序；ADR-017 原文保留历史，其唯一owners/current-only/deferred/恢复锚点与退出删除条件继续有效。

Fork明确 migrate 处理实际旧core/task，Guru从旧source/receipts判ownership并保留定制；current控制原bytes/modes保留。备份与回退恢复每个真实来源；暂停新增工作不得被覆盖，必须接口canonical协调本身不算新业务工作。只复用一个required projection及既有preimages，不增加writer/状态机/普通runtime兼容双读。

正式Fork锁/CI、本地代表验收、完整独立committed review完成后，可晋升本地可执行slice知识；晋升diff须fresh Phase2/commit/完整独立复审，随后发布Refs-only候选以取得同一远端Guru source并补齐public/provider/deferred验收。该证据仍是整个#495完成条件，缺失时保持open。软件Release、真实业务安装和完整累计矩阵独立；未存在版本不声称已实测。
