# #575 S1 测试策略与实际结果

本文件是 S1 验证结果的唯一长期归属；需求、设计及双向关系分别见同目录 requirements.md、design.md、traceability.md。候选尚未晋升 shared current，以下命令通过不代表 Phase 2、committed Branch Review 或发布通过。

| Test identity | 场景与观察 | 实际结果 |
| --- | --- | --- |
| T575-S1-01 | 通过 canonical managed Python 调用生产 `validate_fork_source` 和 maintenance `inspect_source`，消费精确 Fork checkout | 通过：HEAD `2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0`、tree 与 ordered parents 匹配 source record；main CI `38851816688` completed/success；CLI/Core `0.7.0-castbox.3`、pnpm `10.32.1`；干净源码 install/build、build marker、211 templates 和 API1.0 匹配，`unverified: []` |
| T575-S1-02 | 在 `trellis/presets/guru-team/scripts/python` 经 canonical `resolve-python.sh` 运行 `-m unittest test_fork_preparation` | 4/4 通过；覆盖当前 README 来源一致性、构建准备失败即停止、同版本 stale build 拒绝和缺少 Guru branch binding；没有新增镜像测试 |
| T575-S1-03 | 直接核对三份 README、public-docs spec 与 source record；比较根 README 第一构建 Bash 块的前后字节 | 通过：首块未变；稳定 `.3` 原锁、当前新锁、未发布 `.4` 分开；源码入口要求显式同 ref marketplace/provider；manifest 与 maintenance target 保持 `.3`；知识版本与软件版本分开 |
| T575-S1-04 | 核对历史引用、贡献双向 trace、S1/M/S2 边界及 diff hygiene | 历史证据未被替换为当前证明；R01..05 均有设计与测试承接；shared authority 未晋升。`git diff --check` 通过。真实 gitleaks v8.30.1 对本次全部 17 个 tracked/untracked 文件快照扫描，零告警 |

上述验证运行于独立的精确 Fork build 和当前 S1 checkout，不修改全局 Trellis 安装。`inspect_source` 证明实际匹配源码/build/API；对当前 Task 的 inspect 只证明可读的 schema1、branch/session，不证明已转换。

正式 source_locked tools 预览仍因 Guru canonical source 未提交而拒绝，这是原 owner 的前置边界，尚未安装或通过。S1 先经过正式提交与审查；之后 M 才能使用实际 clean committed remote source。没有通过 local_candidate、伪写来源或复制单个 Skill 来绕过。

未验证/剩余：M tools/selected-task apply、native 下一 consumer 与历史交付承接、S2 `.4` 和 matching maintenance assertion、最终 installed/platform/dogfood/reapply parity、代表性 clean install/旧样本、完整多平台矩阵、远端最终 candidate 与 tag-pinned Release。前述项目不计入本 S1 已通过声明；整体准备与发布仍沿 #575 的原 owners 和后续切片完成。
