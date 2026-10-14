# 验证夹具 Delivery 需求

整体 requirement authority 为 ../../prd.md 的 V557-01..03；本 Delivery 承接全部范围。

实际交付内容是 validation/manual-merge-557.json，固定UTF-8 JSON字段取自已展示夹具，消费方是immutable Git/PR内容核验与原Completion。正式创建/规划/Check/独立Review/Publish均使用当前安装原owners；实际GitHub普通two-parent merge无Guru trailers/gate后，原Merge恢复实际DeliveryFact、query2只读读回、原Completion判断整个Task。

交付前验证JSON结构与字段，真实合入和恢复结果在交付后取得；missing CI按真实状态保留，本Task不增加CI要求。公共事实、原gate适用性和整体完成结论由各原owner分开判断。

来源选择与整体accepted_scope沿原Clarify/Author保留。只有一个实际夹具slice，不创建空PR或第二身份，不承担Source #557 Closure、业务恢复或软件Release。
