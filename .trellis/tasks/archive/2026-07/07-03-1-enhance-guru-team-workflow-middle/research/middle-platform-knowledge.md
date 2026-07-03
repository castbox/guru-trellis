# 中台知识检索记录

## 检索请求

- MCP：`guru-knowledge-center`
- `project_domain`: `middle-platform`
- `task_type`: `coding`
- `retrieve_trace_id`: `6218cc88-6450-427f-8b4f-79be47d49944`
- 查询上下文：为 Guru Team Trellis workflow 增加可配置中台知识门禁，覆盖 go-guru、proto-guru、go-guru ORM / repo proto 生成、server framework、Unity3D / Flutter Guru SDK 等方向，要求通用 workflow policy 而非项目私有规则。

## 返回的相关知识入口

- `castbox/go-guru docs/README.md`：Go-Guru 文档结构列出基础设施集成、统一 ORM、ORM Proto 定义与生成规范、MongoDB、PostgreSQL、Redis、Kafka、S3、Sentry、Logger、服务开发、客户端开发等入口。
  - Citation: <https://github.com/castbox/go-guru/blob/9e83ecc49b237b9c6266c777585b9fc0357a738f/docs/README.md#基础设施集成>
- `docs/guides/infrastructure/orm-proto-specification.md`：go-guru Entity Proto 建模、Repo Proto 生成与 `protoc-gen-go-guru` 消费合同的单一规范入口。
  - Citation: <https://github.com/castbox/go-guru/blob/9e83ecc49b237b9c6266c777585b9fc0357a738f/docs/guides/infrastructure/orm-proto-specification.md#go-guru-orm-proto-定义与生成规范>
- `docs/guides/infrastructure/orm.md`：统一 ORM 使用指南，强调统一建模 Entity / Repo、请求响应结构、查询构建、更新语义和事务抽象。
  - Citation: <https://github.com/castbox/go-guru/blob/bb773742324609ce90d5413393e9282569bf753f/docs/guides/infrastructure/orm.md#go-guru-统一-orm-使用指南>
- `docs/guides/infrastructure/mongodb.md`：迁移建议中明确新版本只需手写实体 `.proto`，Repo Service `.proto` 由 `proto-guru` 自动生成。
  - Citation: <https://github.com/castbox/go-guru/blob/9e83ecc49b237b9c6266c777585b9fc0357a738f/docs/guides/infrastructure/mongodb.md#92-不再手写-repo-的-proto仅保留实体-proto>
- `docs/guides/server/development.md`：Go-Guru HTTP/gRPC 服务开发指南，说明 API / Biz / Repo / Infra 分层、proto 与代码生成、Wire、启动与测试。
  - Citation: <https://github.com/castbox/go-guru/blob/bb773742324609ce90d5413393e9282569bf753f/docs/guides/server/development.md#go-guru-httpgrpc-服务开发指南>

## 对 workflow 的启示

- workflow 不应内置某个 SDK 的具体实现规则，而应要求 AI 在任务相关时检索当前 middle-platform 知识，并把 citation 持久化到 task artifact。
- go-guru / proto-guru / ORM repo proto generation 是高价值示例，应在 workflow 文案中作为“包括但不限于”的检索关键词。
- 检索不可用时不能全局阻塞，因为不是所有团队都接入 Guru Team middle-platform；阻塞只能由项目配置 `required` opt-in。
