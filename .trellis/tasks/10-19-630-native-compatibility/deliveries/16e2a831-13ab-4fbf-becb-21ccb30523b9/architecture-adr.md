# ADR-630-CANDIDATE：受管文本的 LF 策略与精确 EOL 恢复

状态：proposed/task-owned；未晋升共享authority。原baseline .102，constitution-v1；Task 630-native-compatibility generation0，Delivery 16e2a831-13ab-4fbf-becb-21ccb30523b9。

## 决策与必要性

正常preset初装、commit后core.autocrlf=true clone会将受管文本物化为CRLF，造成raw validator漂移并使reapply冲突；两历史摘要与该链路一致。Guru-owned声明文本在canonical与目标installed inventory内采用LF。canonical attributes及目标有界Guru attributes块分别维护各自字节策略；不拥有上游入口或用户.gitattributes整体。

只替代现installer/upstream-ownership规则中“current raw不等canonical/previous时一律unknown”的窄条件：声明文本current的CRLF→LF精确等于canonical LF bytes，或其sha256精确等于有效previous-managed hash时，可恢复LF再走原流程。旧版本内容升级仍写原.bak；unknown真实内容改动继续.new/阻塞。二进制、lock、manifest/候选精确身份不采用宽松归一，raw installed validator不变。不靠重算manifest接纳漂移，不新增第二hash authority、旧源缓存或通用normalizer。

## Owner与取舍

installer原owner管理attributes、copy/generate和恢复，validator继续原raw-byte检查；用户块外字节与原sidecar、activation及ownership边界保持。选择标准Git attributes限制正常checkout字节，并用精确换行对照恢复已有目标，避免所有文件无条件归一或关闭校验。无法证明previous来源等价时原conflict，不猜测历史正文。

真实贡献须随本批完整候选接受独立Phase2，之后原Architecture owner决定正式ADR编号及共享晋升。Planning不是已实现或已通过证据。最终原生三系统、实际Agent与release证据各归原owner，不能由本ADR存在替代。
