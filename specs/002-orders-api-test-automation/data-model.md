# Data Model: Orders API Test Automation

## Overview

此数据模型基于 TikTok Shop Orders API 的响应结构。

## Core Entities

### APIResponse

标准 TikTok API 响应结构。

| Field | Type | Description |
|-------|------|-------------|
| code | int | 状态码，0 表示成功 |
| message | str | 响应消息 |
| request_id | str | 请求 ID，用于追踪 |
| data | object | 响应数据体 |

### Order

订单实体。

| Field | Type | Description |
|-------|------|-------------|
| id | str | 订单唯一标识 |
| status | str | 订单状态（UNPAID, ON_HOLD, AWAITING_SHIPMENT 等） |
| create_time | int | 创建时间（Unix timestamp） |
| update_time | int | 更新时间（Unix timestamp） |
| payment | Payment | 支付信息 |
| line_items | LineItem[] | 商品列表 |
| recipient_address | Address | 收货地址 |
| fulfillment_type | str | 履约类型（FULFILLMENT_BY_SELLER/FULFILLMENT_BY_TIKTOK） |
| shipping_type | str | 配送类型（TIKTOK/SELLER） |

### Payment

| Field | Type | Description |
|-------|------|-------------|
| currency | str | 货币代码（USD, IDR 等） |
| total_amount | str | 总金额 |
| sub_total | str | 商品小计 |
| shipping_fee | str | 运费 |
| tax | str | 税额 |

### LineItem

| Field | Type | Description |
|-------|------|-------------|
| id | str | 商品行 ID |
| product_id | str | 商品 ID |
| product_name | str | 商品名称 |
| sku_id | str | SKU ID |
| sku_name | str | SKU 名称 |
| quantity | int | 数量 |
| sale_price | str | 售价 |
| original_price | str | 原价 |

### Address

| Field | Type | Description |
|-------|------|-------------|
| full_address | str | 完整地址 |
| name | str | 收件人姓名 |
| phone_number | str | 电话号码 |
| region_code | str | 地区代码 |

### OrderListResult

| Field | Type | Description |
|-------|------|-------------|
| orders | Order[] | 订单列表 |
| total_count | int | 订单总数 |
| next_page_token | str | 下一页 token（用于分页） |

### AccessToken

| Field | Type | Description |
|-------|------|-------------|
| access_token | str | 访问令牌 |
| refresh_token | str | 刷新令牌 |
| expire_in | int | 过期时间戳 |

### PriceDetail

| Field | Type | Description |
|-------|------|-------------|
| order_id | str | 订单 ID |
| price_breakdown | PriceBreakdown | 价格明细 |

### ExternalOrderRef

| Field | Type | Description |
|-------|------|-------------|
| platform | str | 外部平台（SHOPIFY, WOOCOMMERCE 等） |
| external_order_id | str | 外部订单号 |
| tiktok_order_id | str | TikTok 订单号 |

## Enums

### OrderStatus

- UNPAID
- ON_HOLD
- AWAITING_SHIPMENT
- PARTIALLY_SHIPPING
- AWAITING_COLLECTION
- IN_TRANSIT
- DELIVERED
- COMPLETED
- CANCELLED

### ShippingType

- TIKTOK
- SELLER
- TIKTOK_DIGITAL

### Platform

- SHOPIFY
- WOOCOMMERCE
- BIGCOMMERCE
- MAGENTO
- SALESFORCE_COMMERCE_CLOUD
- CHANNEL_ADVISOR
- AMAZON
- ORDER_MANAGEMENT_SYSTEM
- WAREHOUSE_MANAGEMENT_SYSTEM
- ERP_SYSTEM

## Relationships

```
AccessToken (认证)
    └── 用于调用所有 API

OrderListResult (订单列表结果)
    ├── orders[] → Order
    └── 分页通过 next_page_token

Order
    ├── payment → Payment
    ├── line_items[] → LineItem
    └── recipient_address → Address

Get Order Detail 返回 Order
Get Price Detail 返回 PriceDetail
Get/Add External Order References 返回 ExternalOrderRef
```
