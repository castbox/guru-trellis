# #724 Codex Guru Skill 公共目录迁移

## 当前分发合同

Codex 的项目级 Guru Skill 公共投影统一使用 .agents/skills/<id>/。新安装及 reapply 不再创建受管 .codex/skills/guru-*/；完整执行器、私有 runtime 和运行证据继续由 .trellis/guru-team/ 的原 owner 管理。package-private tests/ 只留 canonical 源。

目标平台选择包含 codex 时，共享目录同时包含 Codex 专属编排包及 agents/openai.yaml；未选择 codex 时不新增这些包。仅支持 Codex 的 platform_destinations、显式调用策略和原生工具前置保持。多个所选平台共用同一共享包时只投影一份。

## 已有安装

更新工具、workflow、Skills 或受管投影且须保留 Task/session 的 checkout，使用完整目标 source 中的 [guru-upgrade-tools](../../skills/guru-team/packages/guru-upgrade-tools/SKILL.md) 及其完整合同。完整旧安装升级继续由 [guru-upgrade-installation](../../skills/guru-team/packages/guru-upgrade-installation/SKILL.md) 承接。不要直接删除旧目录，也不要把普通 apply 的旧 Task 诊断转成无关历史迁移。

原维护 owner 从目标 installed manifest/provenance 读取 exact platform selection，不从 source 仓库的选择推断目标。它先完成并核对目标公共文件集合、内容和可执行位；目标无未解决冲突后，才按 previous managed provenance 移除未修改旧文件及其派生空目录。

旧目录和共享目标中的用户修改、来源不明文件均保留，沿原 conflict/sidecar 处置。目标冲突解决前保留仍需迁移的旧受管副本。保留旧副本造成重复发现或冲突未解决时，迁移尚未完成，不能报告成功。解决具体冲突后，沿原 frozen operation 的恢复入口继续；不重建另一操作来绕过原冲突。

迁移完成后的正常 reapply 只维护新 current 根，不重新生成旧投影。平台选择加入 codex 时安装专属包；移除 codex 时按原受管规则退出专属公共文件，同时保留其它所选平台仍需的 shared 包、其它平台副本及用户文件。

## 保留边界

本迁移只处理目标仓库内由 Guru 管理的项目级公共 Skill 文件和受管记录。不清理用户级 ~/.codex/skills、第三方 Skill 或上游 Trellis 文件；不删除整个 .codex/，不改变 config.toml、agents、hooks.json、hooks 或 prompts 的职责。Claude/Cursor 的平台 Skill 根与公共 Skill id、行为、出口保持。

旧路径仅供原迁移 owner 识别 predecessor，不是 current 平台根、必要文件或长期兼容分发。目标冲突与旧来源保护仍属于现有安装/维护 owner，无新增迁移台账或并行 writer。

## 验证与采用范围

官方 [Codex Skills 文档](https://developers.openai.com/codex/skills/) 定义从 CWD 到仓库 root 的 .agents/skills 发现机制、同名 Skill 不合并及 agents/openai.yaml 的显式调用策略。本批按该机制选择真实 CLI0.162.1 作为代表，验证公共 Skill 和专属编排 Skill 的发现及原公开调用。真实记录位于本 Task D1 的 validation，由原 Task 身份解析活动或归档位置；本说明不预填验证通过。

专属包的 dry-run 检查仍保留 native chat/async 能力前置。合法能力不足出口证明此次公开调用到达了原门禁，不证明真实业务编排已运行。文件扫描、installed validator 和聊天 Skill 清单都不能替代 native 调用证据。发现受支持宿主依赖旧根时，先记录宿主/版本及依赖并完成兼容承接，再退出其旧投影。

本 Issue 的定向范围为正常新装、升级、两端冲突、恢复/reapply、平台选择变化和一个代表性 clean 安装。完整多平台 Throwaway/Release Gate、桌面 UI 展示、其它客户端独立执行、业务采用和生产效果不从这些结果推定。local_candidate 工具维护继续报告 formal_fork_source_lock 未验证。

