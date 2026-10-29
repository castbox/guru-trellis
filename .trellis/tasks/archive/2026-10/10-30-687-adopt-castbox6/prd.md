# 采用 Castbox Trellis 0.7.0-castbox.6 固定来源：整体需求

## 1. 来源与术语

| 来源 | 角色与用途 |
| --- | --- |
| [Direct Source #687](https://github.com/castbox/guru-trellis/issues/687)，完整正文 | 要求：固定来源采用、安装回归和验证边界。用户本轮明确要求完成实现与交付，承接正文中的采用目标。 |
| [Trellis #59](https://github.com/castbox/Trellis/issues/59)、[修复 PR #60](https://github.com/castbox/Trellis/pull/60) | 原始问题与修复证据；不扩大 Guru 支持的交付 profile。 |
| [版本 PR #61](https://github.com/castbox/Trellis/pull/61)、[.6 Release](https://github.com/castbox/Trellis/releases/tag/castbox-v0.7.0-castbox.6) | 已发布来源证据：tag 指向 17015f987166f4106034f115d23212446f16d536。 |
| `trellis/presets/guru-team/source/trellis-source.json`；`trellis/guru-team-extension.json` | 当前来源锁及公开版本映射，作为本轮实际修改入口。 |
| `trellis/presets/guru-team/README.md`、`README.md` 的固定来源与工具维护说明 | 既有来源、资产所有权和 tools-only 维护合同。 |

source_locked 指原工具维护入口对完整、干净、匹配来源及 build 的校验。stop 指由原阶段 owner 撤回已存在的 Delivery；它不表示交付、Task Completion 或 Closure。

## 2. 背景与问题

当前来源锁固定于 79a97ed60fe19e8f287eaddfa74722b5250ced35 / 0.7.0-castbox.5，未包含 #59 修复。上游 Core 和匹配 Python 在 stop 前错误应用当前 profile 准入条件，使 Guru 仅支持 pull_request 时，已保留的 manual/local_commit 切片无法合法撤回。上游已修复该入口，并将版本升为 .6。本 Task 采用该来源并验证 Guru 集成结果。

## 3. 目标与非目标

目标是通过现有来源锁、受管投影和 preset 机制采用 .6。整体责任包含来源身份核对、映射同步、真实隔离 tools-only 采用、旧 profile 停止回归和定向质量检查。

不新增 Guru 软件 Release，不执行完整多平台 Release/upgrade 累计矩阵，不更新实际业务项目，不收尾原 Backend Task，不承担 AWS/media/capacity 验收。不修改 Guru profile 声明，不补丁官方生成资产，不弱化来源校验。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与动作 | 处理及可观察结果 |
| --- | --- | --- |
| S1 来源采用 | Guru 维护者在本仓库更新固定来源 | canonical lock 和受管投影一致，公开目标映射指向同一 .6 精确 Core/CLI 对。 |
| S2 工具维护 | 原 tools-only owner 接受干净匹配 Guru/Fork source/build，更新隔离已有安装 | 真实公开入口完成采用；Task/session、用户内容及非目标资源保留。来源不匹配时沿原合同阻止更新。 |
| S3 旧切片撤回 | 当前 workflow 仅支持 pull_request，安装中保留 manual/local_commit Delivery | 原阶段 owner 调用公开 stop；合法撤回成功，peer/history 保留，selection 合法释放；匹配重试保持原结果。 |
| S4 重应用 | 维护者按原 installer/preset 机制重应用 | source/installed、ownership、reapply/drift 和 sidecar 结果可核对，不依赖生成文件手工 patch。 |

## 5. 行为要求

- R1：来源固定为 17015f987166f4106034f115d23212446f16d536 / 0.7.0-castbox.6。核对真实 merge parents、tree、main CI，以及 Release 四附件和精确依赖；不能以相同版本号替代身份。
- R2：同步唯一 canonical source lock、受管投影和当前公开版本映射。Core/CLI 名称与精确配对保持原合同。
- R3：至少完成一次代表性隔离 tools-only 实际采用。完整、干净、匹配 Guru/Fork source/build、API、字节及 mode 校验继续生效。维护中保留已有 Task/session 和用户内容。
- R4：通过已安装公开入口验证两种已保留旧 profile 的合法停止。原 owner、阶段和 evidence/retry 约束保持，peer/history/selection 语义保持。停止不得触发 Completion/Closure，也不得新增不支持 profile。
- R5：执行与来源采用相关的 source/installed、ownership、reapply/drift、sidecar 和回归检查。报告区分上游证据、本轮来源检查、真实安装行为及未覆盖边界。

## 6. 约束与依赖

依赖已经发布的 .6 来源和附件；缺失或身份不符时阻止采用。官方 `trellis-*` 资产仍由 Trellis 拥有，Guru 仅通过其公开扩展面工作。AI 判断适用性与充分性，脚本执行事实和验证。复用原工具维护恢复入口，不另造迁移或审批协议。

没有新的业务 API、数据库或持久化字段，因此无数据迁移。旧 Task/schema 的迁移责任仍属于原迁移 owner，不能为本轮验证批量改写历史 Task。

## 7. 可观察验收与验证方式

| 验收 | 关联要求/场景 | 入口、输入与预期结果 |
| --- | --- | --- |
| AC1 | R1、S1 | GitHub merge/tag/CI/Release 和本地 source/build 身份核对，得到同一 17015f98/.6 的精确配对。 |
| AC2 | R2、S1/S4 | 对 canonical lock、受管投影、manifest 与当前说明进行 source/installed 校验，当前映射一致。历史发行记录保留历史身份。 |
| AC3 | R3、S2 | 在隔离目标使用原公开 tools-only 入口，输入干净匹配来源；采用后版本/API/字节/mode 匹配，目标 Task/session/用户内容保留。 |
| AC4 | R4、S3 | 已安装 Core/Python 公开操作分别停止 manual/local_commit；检查结果、peer/history、selection、匹配重试以及未产生 Completion/Closure。 |
| AC5 | R5、S4 | 定向回归、ownership、重应用漂移和 sidecar 检查通过；最终说明明确未执行完整累计矩阵和业务安装。 |

## 8. 实际未决项

整体需求没有必须由用户回答的未决选择。匹配来源构建和严格工具维护入口的具体实施由 Delivery Author/Architecture 确定；执行遇到的真实失败回原 owner 处理，不降低验收。完整累计矩阵、Guru 软件发布和业务项目采用保留为本轮范围外边界。
