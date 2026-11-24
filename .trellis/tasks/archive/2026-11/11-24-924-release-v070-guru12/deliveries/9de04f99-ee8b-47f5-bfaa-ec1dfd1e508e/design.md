# D1 发布源码设计

## 1. 目标与基线

承接 AC01。开发基线 B 和规划时 HEAD 均为远端 main 的 `6825949699d342eba1ad018ee04a8f9396f11619`。交付目标为 `castbox/guru-trellis:main`。候选架构审核引用 `docs/architecture/README.md` 所定位的当前权威及 ARCH-INT-009、014、015，结论为 `no_architecture_impact`。

## 2. 当前系统与目标差额

当前扩展清单和三个公开 README 指向 .11。将 canonical 版本、候选安装示例及前驱说明更新至 .12 / .11。D1 没有前序。现有源锁依赖 `0.7.0-castbox.6` 对应的 `e3793251fad8bd261d0c370d408c7675b9f6a140`。

## 3. 来源设计处置

| 来源与约定 | 处置与落点 | 理由 |
| --- | --- | --- |
| 私有发布合同 Stage 1，完整可分发来源先于实际采用 | retain，见第4、6节 | 两批使用真实的已交付源码交接 |
| 私有发布合同 Invocation Input，版本轴分开 | retain，见第5节 | 扩展更新不改变匹配框架依赖 |
| 私有发布合同 Whole Preparation，准备 PR 使用 Refs | retain，见第6节 | #924 承担后续正式发布 |

## 4. 模块和职责

`trellis/guru-team-extension.json` 提供扩展版本。根 README 提供可复制的安装入口，preset 与 workflow README 给出相同发布身份及历史前驱。沿用原有 manifest、marketplace、preset 和验证工具。源码与公开说明同步交付，消除安装示例和版本清单出现不同目标的可能。

## 5. 接口与数据

沿用 `extension.version` 对应 canonical `version` 的安装行为。清单版本取 `0.7.0-guru.12`。Trellis CLI 及 source lock 继续从既有配置读取。安装者应先核对存在非 draft 且非 prerelease 的目标 GitHub Release，条件不成立时选实际已正式发布的 tag。

## 6. 顺序与失败处理

更新源码和文档后，验证源码、平台投影和临时安装。使用与本批 workflow 及 registry 字节相同的远端准备基线作为 marketplace，使用当前完整工作树作为 preset 源。失败时回到本批修复和验证。经过独立 Review 后以 `Refs #924` 交付。合并后由 Completion 识别未实施采用，由后继 Delivery 使用实际已交付且干净的源码。

## 7. 兼容与恢复

保留正式前驱安装说明和源版本核验。D1 不写真实目标的受管安装，实际采用与恢复使用 D2 的原 tools owner。正式发布仍使用准备归档合并后的单一候选。

## 8. 验证设计

V1 使用现有 source validator 核对包和 Shared/Codex/Claude/Cursor 投影。V2 用匹配 Fork 从准备基线的确切 SHA 初始化 Codex 临时项目，执行当前 preset 安装及 update/reapply，读回扩展版本、源锁、受管入口、任务接续与 sidecar 结果。V3 核对公开命令、版本引用、前驱历史和 diff。临时安装证据覆盖 D1 可分发源码；D2 实际采用和最终候选验证各自执行。

## 9. Canonical 引用和未决项

`.trellis/spec/docs/public-docs.md` 定义安装和版本写作。ARCH-INT-009、014、015 定义分发和采用。验证入口来自私有发布合同的定向验证。现有需求、设计、测试与 Architecture 权威已经覆盖本批机制，无新的能力定义或待定事项。
