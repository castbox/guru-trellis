# D1 发布源码需求

## 1. 整体来源与术语

整体 `accepted_scope` 指向 Task 根 `prd.md`。本批 `scope_ref` 选择 AC01，规划位于 `deliveries/9de04f99-ee8b-47f5-bfaa-ec1dfd1e508e`。[#924](https://github.com/castbox/guru-trellis/issues/924) 定义发布目标。私有发布合同的 Stage 1 定义已交付源码与实际采用的顺序。canonical 源码是分发入口与对外版本说明的权威。

## 2. 整体与本批目标、非目标

本批交付可分发的 `0.7.0-guru.12` 源码及公开安装说明，覆盖整体 R1 和 AC01。实际 dogfood 受管安装采用属于后继 AC02。正式发布候选、tag、Release 和 #924 关闭属于独立发布阶段。

## 3. 本批起点、前序结果、依赖与剩余责任

没有前序 Delivery。基线为 `6825949699d342eba1ad018ee04a8f9396f11619`。前驱为 `v0.7.0-guru.11`。现有发行物依赖 Trellis CLI `0.7.0-castbox.6`，以实际 source lock 核对。D1 合并后，由整体 Completion 依据尚未交付的 AC02 分配后继责任。两批均交付后再完成准备归档。

## 4. 本批调用方、场景与流程

维护者核实正式前驱、可用目标 tag 和来源锁定，更新 canonical 版本与公开说明。维护者用匹配的 Trellis CLI 对本批源码执行分发检查和定向安装，通过后将源码交付到 `main`。

## 5. 完整行为、条件与约束

版本清单和安装文档使用同一 Guru 版本。公开安装说明继续要求核对正式 Release 是否存在。CLI 版本和 source lock 保持对应，如无依赖变化则保留已核实的现有值。D1 的定向安装必须实际验证版本及必要受管入口。若验证失败，修复并验证 D1 后再交付。来源设计逐项处置见本批 design 第3节。

## 6. 本批验收、验证方式与未决项

AC01 从本批源码执行 source 检查和平台投影核对，并使用匹配 CLI 运行定向安装。在安装目标读回版本、入口与来源。公开说明应与源码一致。对应源码交付至 `main` 后，可供后继切片执行真实采用。当前需求无待决项。

## 7. Canonical 引用与本轮差额

`.trellis/spec/docs/public-docs.md` 定义公开安装说明及版本轴分工。`docs/architecture/04-integrations/distribution.md` 的 ARCH-INT-009 定义正式发布和 source_locked 采用边界。现有发布合同定义验证入口。本批更新版本与当前安装说明，复用既有发布架构和验证入口。
