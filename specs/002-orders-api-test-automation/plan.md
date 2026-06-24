# Implementation Plan: Orders API Test Automation

**Branch**: `002-orders-api-test-automation` | **Date**: 2026-06-12 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-orders-api-test-automation/spec.md`

## Summary

创建一个 Python 测试脚本，调用 TikTok Shop Orders API 目录下的所有 6 个接口（Get Order List、Get Order Detail、Get Price Detail、Get External Order References、Add External Order References、Update Blind Box Results），逐一验证每个接口能返回正确数据。

技术方案：基于已验证成功的 `test_order_simple.py`，创建统一的 API 客户端模块，支持签名生成、token 自动刷新、指数退避重试、详细日志记录。

## Technical Context

**Language/Version**: Python 3.9+

**Primary Dependencies**:
- `requests` - HTTP 客户端
- `tenacity` - 重试机制（指数退避）
- 标准库：`json`, `hmac`, `hashlib`, `time`

**Storage**: 配置文件读取（tiktok-config.json），无持久化存储需求

**Testing**: 直接运行脚本验证每个 API

**Target Platform**: macOS/Linux (Python 3.9+)

**Project Type**: CLI 工具脚本

**Performance Goals**: 脚本运行时间不超过 60 秒（包含所有 6 个 API 调用）

**Constraints**:
- 使用 `x-tts-access-token` header（不是 Bearer token）
- 签名算法：HMAC-SHA256
- API 版本使用文档标注的最新版本

**Scale/Scope**: 6 个 API 接口测试

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| 想清楚再写 | ✅ PASS | 规范已澄清 4 个关键问题 |
| 简单优先 | ✅ PASS | 单个脚本 + 共享工具模块，无过度设计 |
| 外科手术式改动 | ✅ PASS | 复用现有 test_order_simple.py 的成功逻辑 |
| 目标驱动执行 | ✅ PASS | 每个 API 独立验证，有明确的成功标准 |

**GATE RESULT**: ✅ ALL PASS - 无需额外验证或澄清

## Project Structure

### Documentation (this feature)

```text
specs/002-orders-api-test-automation/
├── plan.md              # This file
├── research.md          # Phase 0 output (N/A - 无需研究)
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A - 无外部接口)
└── tasks.md             # Phase 2 output (/speckit-tasks command)
```

### Source Code (repository root)

```text
.kol-agent/scripts/
├── test_order_simple.py       # 已验证成功的参考实现
├── orders_api_tester.py       # 新建：统一测试脚本
└── tiktok_api_client.py       # 已有：API 客户端（需更新以匹配正确调用逻辑）
```

**Structure Decision**: 单文件脚本 + 复用现有 tiktok_api_client.py 模块

## Complexity Tracking

> 无复杂度违规。此项目为一次性测试脚本，无持久化存储需求，无多组件架构。

## Phase 0: 无需研究

所有技术细节已在规范中明确：
- API 调用逻辑：已通过 test_order_simple.py 验证
- 签名算法：已明确
- 重试策略：已澄清（指数退避）
- 日志策略：已澄清（详细日志）

## Phase 1: Design

### Data Model

基于 TikTok Orders API 响应结构：

| Entity | Fields |
|--------|--------|
| APIResponse | code (int), message (str), request_id (str), data (object) |
| Order | id, status, create_time, payment, line_items, recipient_address |
| OrderListResult | orders[], total_count, next_page_token |
| AccessToken | access_token, refresh_token, expire_in |
| PriceDetail | order_id, price_breakdown |
| ExternalOrderRef | platform, external_order_id, tiktok_order_id |

### Quickstart

运行验证指南：

```bash
# 前置条件
pip install requests tenacity

# 运行测试
python3 .kol-agent/scripts/orders_api_tester.py

# 预期结果
# - Get Order List: 返回订单列表
# - Get Order Detail: 返回订单详情
# - Get Price Detail: 返回价格明细
# - Get External Order References: 返回外部订单引用
# - Add External Order References: 返回成功
# - Update Blind Box Results: 返回成功（如果不是盲盒订单则返回特定错误码）
```

### API 版本对应

| API | 版本 |
|-----|------|
| Get Order List | 202309 |
| Get Order Detail | 202507 |
| Get Price Detail | 202407 |
| Get External Order References | 202406 |
| Add External Order References | 202406 |
| Update Blind Box Results | 202605 |
