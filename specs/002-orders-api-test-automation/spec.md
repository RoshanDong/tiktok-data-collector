# Feature Specification: Orders API Test Automation

**Feature Branch**: `002-orders-api-test-automation`

**Created**: 2026-06-12

**Status**: Draft

**Input**: User description: "现在以.kol-agent/scripts/test_order_simple.py脚本为api调用的示例，参考/Users/yuelnn/RoshanProgram/Cursor/First-CC/api官方文档/Orders中的接口api文档，然后实现一个新的python脚本，对每一个api接口进行调用和严格的验证，直到每一个api接口能都获取到正确的返回数据。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Orders API Test Script (Priority: P1)

创建一个 Python 测试脚本，调用 TikTok Shop Orders API 目录下的所有 6 个接口，逐一验证每个接口能返回正确数据。

**Why this priority**: API 调用逻辑已验证成功（Get Order List），但其他 5 个接口尚未测试。需要系统化测试所有接口确保数据抓取功能完整。

**Independent Test**: 可通过运行脚本验证每个 API 的响应，每个 API 测试独立运行、独立验证结果。

**Acceptance Scenarios**:

1. **Given** 有效的 access_token 和 shop_cipher，**When** 调用 Get Order List API，**Then** 返回订单列表且 code=0
2. **Given** 有效的 access_token 和已知订单 ID，**When** 调用 Get Order Detail API，**Then** 返回订单详情且 code=0
3. **Given** 有效的 access_token 和已知订单 ID，**When** 调用 Get Price Detail API，**Then** 返回价格明细且 code=0
4. **Given** 有效的 access_token 和已知订单 ID，**When** 调用 Get External Order References API，**Then** 返回外部订单引用且 code=0
5. **Given** 有效的 access_token 和外部订单数据，**When** 调用 Add External Order References API，**Then** 返回成功且 code=0
6. **Given** 有效的 access_token 和订单 ID，**When** 调用 Update Blind Box Results API，**Then** 返回成功且 code=0

---

### User Story 2 - Token Auto-Refresh on 401 (Priority: P2)

当 API 调用返回 401 错误时，脚本自动使用 refresh_token 刷新 access_token 并重试。

**Why this priority**: access_token 7天过期，自动化刷新确保长时间运行的测试不会因 token 失效而中断。

**Independent Test**: 可以通过模拟 401 响应或等待 token 过期来测试此功能。

**Acceptance Scenarios**:

1. **Given** access_token 已过期，**When** 调用任何 API，**Then** 自动刷新 token 并返回正确数据
2. **Given** refresh_token 也已过期，**When** 调用任何 API，**Then** 脚本报错并提示需要重新授权

---

### User Story 3 - 严格响应验证 (Priority: P3)

对每个 API 返回的响应进行严格验证：检查 code=0、message=success、必要字段存在且类型正确。

**Why this priority**: 确保获取的数据完整且格式正确，避免因字段缺失导致后续数据处理失败。

**Independent Test**: 可通过构造不同响应验证验证逻辑是否正确工作。

**Acceptance Scenarios**:

1. **Given** API 返回成功的响应，**When** 验证响应，**Then** 通过所有验证检查
2. **Given** API 返回错误响应（code≠0），**When** 验证响应，**Then** 抛出异常并包含错误码和错误信息
3. **Given** API 返回成功但缺少必需字段，**When** 验证响应，**Then** 抛出异常指出缺失的字段

---

### Edge Cases

- 当 API 返回空订单列表（合法情况）时，验证逻辑不应报错
- 当网络超时或连接断开时，脚本应支持重试机制
- 当 shop_cipher 无效时，API 应返回明确的错误码
- 当请求参数格式错误时，API 应返回 400 错误并说明原因

## Clarifications

### Session 2026-06-12

- Q: 重试与错误处理策略 → A: 指数退避：初始 1 秒，每次重试翻倍，最高 30 秒，最多 3 次尝试
- Q: 日志记录策略 → A: 详细日志：API 请求参数、响应状态码、响应时间、错误信息
- Q: API 版本处理 → A: 使用文档中标注的最新版本
- Q: 测试数据获取方式 → A: 通过 Get Order List API 动态获取订单 ID

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 脚本 MUST 支持调用 6 个 Orders API：Get Order List、Get Order Detail、Get Price Detail、Get External Order References、Add External Order References、Update Blind Box Results
- **FR-002**: 每个 API 调用 MUST 使用正确的 HTTP 方法（GET/POST）、正确的 endpoint URL、正确的签名算法
- **FR-003**: 所有 API 调用 MUST 使用 `x-tts-access-token` header 传递 access_token
- **FR-004**: 签名算法 MUST 遵循：secret + path + 按字母排序的 query 参数 + secret，进行 HMAC-SHA256 签名
- **FR-005**: Get Order List API MUST 支持分页，通过 page_token 获取下一页数据
- **FR-006**: 脚本 MUST 在 401 错误时自动使用 refresh_token 刷新 access_token
- **FR-007**: 每个 API 调用 MUST 在成功后验证响应：code=0、message=success、必要字段存在
- **FR-008**: 脚本 MUST 从配置文件读取所有凭证和配置（client_key、client_secret、access_token、shop_cipher 等）
- **FR-009**: API 调用失败时 MUST 使用指数退避重试：初始延迟 1 秒，每次翻倍，最高 30 秒，最多 3 次尝试
- **FR-010**: 脚本 MUST 记录详细日志：每个 API 的请求参数、响应状态码、响应时间、错误信息
- **FR-011**: 脚本 MUST 使用文档中标注的 API 最新版本
- **FR-012**: Get Order Detail、Get Price Detail 等需要订单 ID 的 API，订单 ID MUST 通过 Get Order List API 动态获取

### Key Entities

- **API Response**: 包含 code、message、request_id、data 字段的标准 TikTok API 响应结构
- **Order**: 订单实体，包含 id、status、create_time、payment、line_items、recipient_address 等
- **Access Token**: 包含 access_token、refresh_token、expire_in 的认证对象
- **Shop Cipher**: 用于标识店铺的加密字符串

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 所有 6 个 Orders API 都能成功调用并返回 code=0
- **SC-002**: Get Order List API 能获取并解析至少 1 条订单数据
- **SC-003**: Get Order Detail API 能获取并解析至少 1 个订单的完整信息
- **SC-004**: Get Price Detail API 能获取并解析至少 1 个订单的价格明细
- **SC-005**: 401 错误自动刷新 token 机制能正常工作
- **SC-006**: 脚本运行时间不超过 60 秒（包含所有 6 个 API 调用）

## Assumptions

- 用户已提供有效的 TikTok Partner Center App（包含 client_key 和 client_secret）
- 用户已完成店铺授权，配置文件中有有效的 access_token 和 refresh_token
- 用户已获取 shop_cipher（通过 Get Authorized Shops API 或配置文件）
- Orders API 文档路径：`/Users/yuelnn/RoshanProgram/Cursor/First-CC/api官方文档/Orders/`
- 参考脚本路径：`.kol-agent/scripts/test_order_simple.py`
- API 签名算法与 test_order_simple.py 中验证通过的算法一致