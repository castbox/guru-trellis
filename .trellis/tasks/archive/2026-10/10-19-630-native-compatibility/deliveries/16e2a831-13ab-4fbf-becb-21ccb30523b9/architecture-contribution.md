# #630 三系统兼容 Architecture contribution

状态：proposed/task-owned；identity=architecture-contribution-630-native-compatibility-v1；change_path=target_native。Task=630-native-compatibility/generation0；Delivery=16e2a831-13ab-4fbf-becb-21ccb30523b9。

baseline=docs/architecture/README.md/current-main-0.7.0-guru.102/active；constitution=docs/architecture/00-foundation/design-constitution.md/guru-trellis-design-constitution-v1/current；change-contract=guru-trellis-architecture-change-contract-v1；concern-set=guru-trellis-architecture-change-concerns-v1。requirement=#630；behavior=installer.md/upstream-ownership.md；本批设计见design.md，窄新决策由architecture-adr.md单写。

| Concern | 适用及当前处置 |
| --- | --- |
| authority-binding | applicable：固定.102、实际candidate及本Task/key；Planning3.0双purpose和Phase2/committed各自freshness保持 |
| constitution-binding | applicable：标准Path/URI/UTF8/Git attributes，原owner内确定性修复；不加未来扩展/第二authority |
| boundary-and-decision | applicable：限定受管文本LF及精确EOL恢复是新决策；仅窄替代旧unknown条件，raw校验保持 |
| owner-and-single-writer | applicable：runtime/schema/TaskCommit/installer原owner不变，Author隔离贡献，Architecture原owner单写共享promotion |
| compatibility-and-exit | applicable：公开inline、单executable及原Skill/exit保持；未知编辑.new、旧升级.bak，失败旧pointer保持；采用完整preset，不热替旧工具 |
| gap-and-deviation | applicable：不扩张/重开GAP006/008，无新legacy authority；WindowsAgent和发行缺口如实保留 |
| parallel-scope | applicable：同Task隔离贡献及原canonical修复，不写其他Task或竞争shared CURRENT |
| evidence-and-freshness | applicable：正常checkout和native WSL首失败是必要性证据；修复native/非UTF8/安装证据仍待执行，不能报已修复 |
| review-and-promotion | applicable：final-plan读真实贡献/ADR；独立Phase2完整before/after后原owner晋升及写后核对，再最终Check/commit/完整committed Review |

Before：bare bash在Windows进入WSL；默认编码和URI/路径字符串存在跨系统差异；正常CRLF checkout导致raw漂移与reapply conflict。After目标：原owner按明确平台/UTF8协议执行；Guru声明文本LF稳定，已有纯EOL差异可精确恢复，真实内容编辑/二进制/lock/manifest raw身份保持。

共享拟晋升范围：docs/architecture/03-domains/ownership.md与04-integrations/distribution.md的installer字节责任、01-current/system.md中实际修复能力及evidence/current-evidence.md真实验证边界；必要正式ADR由原owner分配，并更新对应导航/版本。不得把未来native/Agent验收写成已完成。原.102完整authority可由固定B的Git对象重读。无其他owner、public API或legacy删除变化。

project-check使用现有guru-trellis-architecture-convergence:repository:1 / check@1 / result2.0，原九concern与ADR-005/009合同；不创建新descriptor。真实阶段检查和晋升状态由原Architecture输出及实际targets决定，本proposed贡献不是gate pass。
