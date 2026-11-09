# 冻结恢复中明确已退出的原 peer 对象

Identity：`ADR-TOOLS-RETIRED-PEER-OBSERVATIONS`。目标状态：accepted；隔离 proposal 不建立 current。来源 Issue #769，Task `769-tools-peer-growth-recovery / 0`，Delivery `2b62b86b-ab9c-415d-9cfc-87ec5141e8d0`，before 为 `aaf7f939e83c5a5230ecbb9d9f0827fd5c2e97ff`。原 owner 为 guru-maintain-architecture-baseline。

## 问题、决定与职责

D1 交付后，实际 #766 原恢复仍因已正常 Cleanup 的 #759 位置五项观测缺枚举而 blocked。原 Finish 与原 Cleanup 结果已找回，Cleanup 原公共入口已只读恢复同一个 cleaned；这与当前目录/注册缺失是不同层次的事实。D1 的新增 peer 修复有效，但不足以建立整体验收。

仅给原 recover_frozen_source 加性可选 retired_peer_roots。AI 负责原退出结果和适用性判断。executor 核准确原对象、非目标、完整 Git 无注册及位置不存在；原 prunable 过滤默认不变。只对这些 root 的已知 checkout-local pointer 和 installed/source runtime 观测承接对象终止。非空模式中，其它缺枚举文件仍读原路径核同值；common/gitdir 和存续真实变化仍拒绝。省略/空数组及同源 profiles 无退出例外。

列表只薄传原 engine 前后检查，必要 retry 保持输入字段存在性和值。无 cp 转换、snapshot 刷新、备份扩大、重 prepare 或第二事务。新 schema/Interface/consumer/examples 与迁移成套发布，D1 旧 schema 不获得隐式新字段。

## 取舍、成本与退出

自动忽略所有缺键或把 OS 缺失当退出依据，会把业务判断下放脚本。重建 #759 或重 prepare 改变原问题；跨 Task 台账和 C5 依赖增加无关维护。有限显式位置使 AI 判断与确定性对象核验保持分层，成本限于一个可选调用字段和原比较适配。

本决定窄修订 ADR-TOOLS-FROZEN-SOURCE-RECOVERY 的原观测保持解释，其资产源、原 operation、隔离、阶段和兼容义务继续成立。原事务终态且原恢复保留责任结束后，由 tools owner 依 MIGRATION-769 明确移除兼容能力。真实 consumer、观测对象或原阶段协议变化时重新评估，不扩为通用生命周期框架。

## 验证与晋升

真实 Git peer 的原观测及正常退出后，公开 frozen 入口验证原 bundle 保持；省略/空数组、仍存在/仍注册/选错 root 和存续变化分别验证。retry 有/无字段经实际声明 projection 到 consumer。模块隔离不代替实际 #766 的同 ref/public operation/source 恢复与目标自身验证。先完整 candidate Check，再原 Architecture final_integration/readback，重绑最终质量链。本文不预写实现、安装或 Completion 成功。
