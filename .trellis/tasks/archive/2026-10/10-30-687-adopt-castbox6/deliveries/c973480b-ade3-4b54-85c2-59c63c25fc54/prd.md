# D1：固定 .6 来源与隔离工具维护验收

## 1. 整体来源与术语

整体 accepted_scope 是 Task 根 `prd.md` 的当前 SHA256 authority。本批 scope_ref 选择 AC1、AC2、AC3、AC4、AC5；planning_root 是本目录。完整来源为 [#687](https://github.com/castbox/guru-trellis/issues/687) 正文和用户本轮端到端交付请求（要求）、Trellis [#59](https://github.com/castbox/Trellis/issues/59)/[#60](https://github.com/castbox/Trellis/pull/60)（问题与修复证据）、[#61](https://github.com/castbox/Trellis/pull/61)/[.6 Release](https://github.com/castbox/Trellis/releases/tag/castbox-v0.7.0-castbox.6)（来源证据）。source_locked 和 stop 的含义见整体 PRD 第1节。

## 2. 整体与本批目标、非目标

本批一次交付全部 R1–R5：将当前 Guru 固定 Fork 来源从 .5 切换至 .6，保持严格来源与原维护合同，并证明隔离安装采用和旧 profile 停止。它是来源采用切片，没有其它业务功能。非目标是 Guru 新软件发布、完整累计平台矩阵、真实业务升级、Backend 收尾与 AWS/media/capacity 验收。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 尚无前序 Delivery。起点是 main@7718d129bcb2055d77c7f43d0e4edca9aee313ea 的 .5 来源锁与现有 tools-only owner。上游修复和 Release 已完成，属于外部输入，不等于 Guru 已采用。依赖实际干净匹配 Guru/Fork source/build 和已发布附件。所有整体验收都在本批承担；合并后原 Completion owner 仍须核对 AC1–AC5，不能以合并替代完成。

## 4. 本批调用方、场景与流程

- DS1：维护者核对固定 merge/tag/CI/附件，修改来源锁和当前映射；读回 canonical/installed 后能识别唯一 .6 来源。
- DS2：原 tools-only owner 对隔离已有目标输入严格匹配 source/build，执行真实采用。完成后工具版本/API/字节/mode 匹配，Task/session 与用户内容保留。普通来源不匹配沿原失败与恢复入口处理。
- DS3：目标仅支持 pull_request，合法保留 manual/local_commit。原阶段 owner 通过已安装公开 Core/Python stop 撤回；观察停止结果、peer/history/selection、重试和无 Completion/Closure。
- DS4：原 installer/preset 正常重应用并执行漂移/sidecar 检查；生成的官方资产继续由 Trellis 管理。

## 5. 完整行为、条件与约束

- DR1（R1、DS1）：固定17015f987166f4106034f115d23212446f16d536、真实 parents/tree/main CI、CLI/Core 0.7.0-castbox.6 与 pnpm@10.32.1。核对 Release 四附件和 CLI精确 Core 依赖。
- DR2（R2、DS1/4）：同步 canonical lock、受管投影、manifest 当前版本映射和当前说明。已发布 Guru .6 的历史 .5 配对不得改写成当前采用来源。
- DR3（R3、DS2）：实际完成一个隔离 source_locked tools-only 采用。保持完整/干净/匹配 source/build、API、字节和 mode 校验。Task/session/用户内容不得被当作工具资产覆盖。
- DR4（R4、DS3）：分别停止两种旧 profile；不扩展创建支持，不改 owner/阶段/evidence 约束，不将 stop 作为 delivered/Completion/Closure。匹配重试保持既有语义。
- DR5（R5、DS4）：执行 source/installed、ownership、reapply/drift、sidecar 与相关回归，明确每项实际来源和未覆盖项。来源设计承诺在 design 第3节唯一处置。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 入口、输入和预期 |
| --- | --- | --- |
| DAC1/AC1 | DR1/DS1 | GitHub/Git及实际build读取同一来源和精确依赖，附件校验与发布一致。 |
| DAC2/AC2 | DR2/DS1/4 | canonical与受管lock相同，当前映射为 .6，历史说明仍为历史 .5。 |
| DAC3/AC3 | DR3/DS2 | 原公开工具维护入口在干净匹配来源上完成采用；安装匹配且Task/session/用户内容保留。 |
| DAC4/AC4 | DR4/DS3 | 已安装Core/Python公开stop对两profile成功；检查peer/history/selection/重试及无Completion/Closure。 |
| DAC5/AC5 | DR5/DS4 | 定向回归与原ownership/reapply/drift/sidecar检查满足，结果声明范围准确。 |

需求阶段没有必须澄清的未决项。实际维护构建和验证组织由后续设计确定，严格入口失败不得以绕过校验解决。

## 7. Canonical 引用与本轮差额

- requirement/behavior：`docs/requirements/current/native-compatibility.md` R630-03/05/06，适用原解释器、canonical ownership 与分层验证责任；本轮仅采用新固定来源。
- design：`docs/design/current/native-compatibility.md` D630-03/05/06，以及 `trellis/presets/guru-team/README.md` Apply And Verify，原source/build与维护owner保持。
- test：`docs/test/current/native-compatibility.md` T630-03/06/07；本轮只做与采用相关的代表性定向验证，不重复三系统累计矩阵。
- Architecture：`docs/architecture/README.md` 当前入口与 `docs/architecture/04-integrations/distribution.md` 来源/安装边界；独立候选评估决定本轮知识差额。
