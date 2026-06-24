# API Contracts: TikTok Shop Data Fetch

**Feature**: 001-tiktok-data-fetch
**Date**: 2026-06-10

---

## External API: TikTok Shop Seller API

### Base URL
```
https://open.tiktokapis.com/v2/
```

### Authentication

**Endpoint**: `POST /oauth/token/`

**Request**:
```json
{
  "client_key": "string",
  "client_secret": "string",
  "grant_type": "client_credentials"
}
```

**Response** (200 OK):
```json
{
  "access_token": "string",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "string"
}
```

**Error Response** (401):
```json
{
  "error": "invalid_client",
  "error_description": "Client authentication failed"
}
```

---

### Order List Endpoint

**Endpoint**: `GET /order/list/`

**Headers**:
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| create_time_start | int | Yes | Unix timestamp (start of day) |
| create_time_end | int | Yes | Unix timestamp (end of day) |
| page_size | int | No | Default 100, max 1000 |
| order_status | string | No | Filter by order status |

**Response** (200 OK):
```json
{
  "data": {
    "orders": [
      {
        "order_id": "string",
        "create_time": 1717891200,
        "total_amount": 45.50,
        "status": "COMPLETED",
        "items": [
          {
            "product_id": "string",
            "product_name": "string",
            "quantity": 2,
            "unit_price": 22.75
          }
        ]
      }
    ],
    "has_more": true,
    "next_page_token": "string"
  }
}
```

**Error Responses**:
- 401: Invalid or expired access token
- 429: Rate limit exceeded
- 500: Internal server error

---

### Rate Limiting

| Tier | Limit |
|------|-------|
| Default | 100 requests/minute |
| On 429 | Retry with exponential backoff (5s, 10s, 20s) |

---

## Internal Contracts

### Script Output Contract

**stdout**: Human-readable progress messages
```
[YYYY-MM-DD HH:MM:SS] {message}
```

**stderr**: Error messages only

**Exit Codes**:
| Code | Meaning |
|------|---------|
| 0 | Success - data fetched and stored |
| 1 | Failure - error occurred (see log) |
| 2 | Partial - some data fetched, check logs |

---

### Log File Contract

**File**: `.kol-agent/tiktok-data/logs/YYYY-MM-DD.jsonl`

Each line (JSONL):
```json
{
  "timestamp": "ISO 8601",
  "status": "success|failure|partial",
  "dateQueried": "YYYY-MM-DD",
  "orderCount": 0,
  "totalRevenue": 0.00,
  "errorMessage": null,
  "retryCount": 0
}
```

---

### Excel File Contract

**File**: `.kol-agent/tiktok-data/tiktok-sales-YYYY-MM.xlsx`

**Sheet**: YYYY-MM (e.g., "2026-06")

**Columns**:
| Column | Header | Type |
|--------|--------|------|
| A | Date | string (YYYY-MM-DD) |
| B | Order Count | integer |
| C | Total Revenue | currency |
| D | Top Products | JSON string |

---

**Contracts Status**: ✅ Complete