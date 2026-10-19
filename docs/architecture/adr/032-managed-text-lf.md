# ADR-032：受管文本 LF 与精确 EOL 恢复

状态：accepted。来源为#630真实正常checkout/安装差异；只承接受管字节策略，不改变FOUNDATION、public Skill/exit或原owner。

## 决策

Guru声明文本在canonical源码与实际installed inventory内使用LF。源码Git attributes限Guru source根和明确文本类别；installer维护目标root .gitattributes中的有界Guru块，只覆盖实际Guru namespace、选中guru-* Skill、明确managed spec/finish条目。用户块外原始字节保留，真实更深/info/global attributes冲突阻塞激活。lock、binary及extension/source精确身份文件保留各自raw合同。

只窄替代原installer/upstream-ownership中“raw不等canonical/previous即unknown”的条件：声明文本current.replace(CRLF,LF)精确等于canonical LF bytes，或其归一后hash精确等于有效previous-managed hash时，installer可恢复LF。恢复后原installed validator仍校验真实raw bytes；canonical-equal只恢复换行，旧受管内容升级保留原始.bak。其他内容差异仍保留目标并.new/阻塞；不靠重算manifest接纳漂移，不新增第二摘要authority或历史源码cache。

## 责任与取舍

installer原owner单写属性块、copy/generate和精确恢复；raw validator、激活前runtime检查、旧pointer保护及原sidecar lifecycle不变。标准Git属性限制正常物化，精确原文对照恢复已存在目标，避免全文件无条件归一、关闭校验或覆盖未知编辑。该恢复只服务当前正常LF/CRLF转换；不能推导安全/防伪边界或新增对抗测试。

路径身份、file URI、UTF8、Bash transport和TaskCommit继续各原runtime/package owner；固定Fork .5只沿source lock及公开原生维护接入，Guru不patch上游资产。实际三系统、Windows Codex和正式发行各自验收；知识接受不证明它们通过。
