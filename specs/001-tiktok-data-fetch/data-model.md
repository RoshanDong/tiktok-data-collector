# Data Model: TikTok Shop Data Fetch Automation

**Feature**: 001-tiktok-data-fetch
**Date**: 2026-06-10

---

## Entity Definitions

### DailySalesData

Represents one day's sales summary from TikTok Shop.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| date | string (YYYY-MM-DD) | Date of sales data | Required, ISO format |
| orderCount | integer | Total number of orders | >= 0 |
| totalRevenue | decimal | Total revenue in local currency | >= 0, 2 decimal places |
| topProducts | array[ProductSummary] | Top 10 products by quantity | Max 10 items |

### ProductSummary

| Field | Type | Description |
|-------|------|-------------|
| productId | string | TikTok product identifier |
| productName | string | Product display name |
| quantitySold | integer | Total units sold |
| revenue | decimal | Revenue from this product |

### FetchLog

Audit trail of all fetch operations.

| Field | Type | Description |
|-------|------|-------------|
| timestamp | string (ISO 8601) | When fetch was attempted |
| status | enum | success \| failure \| partial |
| dateQueried | string (YYYY-MM-DD) | The date range of data fetched |
| orderCount | integer | Number of orders processed |
| totalRevenue | decimal | Total revenue computed |
| errorMessage | string \| null | Error details if failed |
| retryCount | integer | Number of retries attempted |

---

## Data Flow

```
TikTok API → Order List Response
    ↓
Transform to DailySalesData
    ↓
Aggregate by date
    ↓
Excel File (.kol-agent/tiktok-data/tiktok-sales-YYYY-MM.xlsx)
    ↓
Log Entry (.kol-agent/tiktok-data/logs/YYYY-MM-DD.jsonl)
```

---

## Excel Output Schema

**File**: `tiktok-sales-YYYY-MM.xlsx`

**Sheet**: Monthly summary (named "YYYY-MM")

| Column | Header | Type | Example |
|--------|--------|------|---------|
| A | Date | string (YYYY-MM-DD) | 2026-06-09 |
| B | Order Count | integer | 156 |
| C | Total Revenue | currency | $4,523.50 |
| D | Top Products | string (JSON) | See note |

**Note**: Top Products column contains JSON array of product objects for that day.

---

## Log File Schema

**File**: `.kol-agent/tiktok-data/logs/YYYY-MM-DD.jsonl`

Each line is a JSON object:
```json
{
  "timestamp": "2026-06-10T06:00:15Z",
  "status": "success",
  "dateQueried": "2026-06-09",
  "orderCount": 156,
  "totalRevenue": 4523.50,
  "errorMessage": null,
  "retryCount": 0
}
```

---

## Validation Rules

| Entity | Rule |
|--------|------|
| DailySalesData.date | Must be valid ISO date, cannot be future |
| DailySalesData.orderCount | Must be >= 0 |
| DailySalesData.totalRevenue | Must be >= 0, max 2 decimal places |
| DailySalesData.topProducts | Max 10 items, sorted by quantitySold descending |
| FetchLog.timestamp | Must be valid ISO 8601 |
| FetchLog.status | Must be one of: success, failure, partial |

---

## State Transitions

### Fetch Execution States

```
IDLE → RUNNING → SUCCESS
              ↘ FAILURE
              ↘ PARTIAL (partial success with errors)
```

**Transitions**:
- IDLE → RUNNING: When cron triggers or manual run invoked
- RUNNING → SUCCESS: All data fetched and written successfully
- RUNNING → FAILURE: Unrecoverable error (auth failure, network timeout)
- RUNNING → PARTIAL: Some data fetched but with non-fatal errors

---

**Data Model Status**: ✅ Complete