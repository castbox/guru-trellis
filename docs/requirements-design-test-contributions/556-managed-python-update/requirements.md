# #556 受管 Python 更新需求增量

唯一来源：[Issue #556](https://github.com/castbox/guru-trellis/issues/556) 当前正文；无评论增量。本贡献以 RDT `.94/active` 为前像，继承 Architecture `.89/active`；尚未晋升共享 current authority。

| Requirement / behavior | 可观察行为 |
| --- | --- |
| R556-01 / BEH556-SELECT | 初始化和显式 apply/reapply 默认选择当时 PATH python3；明确解释器优先，选择失败不回退 |
| R556-02 / BEH556-ADMIT | 保留 CPython/Python3 约束，取消 minor allowlist；依赖和运行能力由实际安装检查判定 |
| R556-03 / BEH556-IDENTITY | 复用现有 cache；identity 保留 lock/API/layout、implementation/major/minor、OS/machine/ABI/platform，排除 patch/path；有效同身份复用，minor 变化选择对应环境 |
| R556-04 / BEH556-ACTIVATE | 锁定依赖、能力 probe、真实 schema-bound public wrapper 检查通过后才替换环境/active；失败保留原 pointer 与原环境，同身份 repair 亦然 |
| R556-05 / BEH556-DIAGNOSE | 缺失/不可执行/非 Python3/implementation、venv-pip、依赖和公开检查失败给出安全原因及可执行修复方法 |
| R556-06 / BEH556-DISTRIBUTE | canonical、完整适用安装投影及使用/排障文档同步；日常 Skill 继续使用受管解释器，不随 Homebrew 自动重建 |
| R556-07 / BEH556-EVIDENCE | 聚焦回归及一个代表性 clean/reapply；真实执行、fixture、SKIP 和未验证边界分别陈述 |

不修改系统 Python/Homebrew、不自动清理旧 cache、不改变日常 Skill 业务语义、不升级业务仓或发布软件。完整 Python-minor、多平台/Release 矩阵及旧源码 dogfood 的整套迁移不属于本次增量。不开始 #557，不触及 backend #148、#149/PR #526 或其资源。
