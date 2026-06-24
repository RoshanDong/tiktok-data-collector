# Research: TikTok Shop Data Fetch Automation

**Feature**: 001-tiktok-data-fetch
**Date**: 2026-06-10
**Status**: Complete

---

## Research Questions

### RQ-1: TikTok Open API for Shop Sales Data

**Question**: What TikTok API endpoint provides daily sales data?

**Decision**: Use TikTok Shop Open API `GET /order/list` endpoint with date filtering

**Rationale**:
- TikTok Shop provides seller API access through their developer portal
- The `/order/list` API returns order data with creation date, status, and product details
- Date range filtering allows fetching "yesterday's" data specifically

**Alternatives considered**:
- TikTok Shop Analytics API (requires higher access level, not available for all sellers)
- Third-party aggregator services (adds cost and complexity)

---

### RQ-2: Excel Generation Library

**Question**: Which Python library for Excel generation is most reliable and widely supported?

**Decision**: `openpyxl` - pure Python Excel writer

**Rationale**:
- Actively maintained (last release 2024)
- Supports .xlsx format (Excel 2007+)
- No system dependencies (unlike xls writer)
- Supports formatting, formulas, and multiple sheets

**Alternatives considered**:
- `xlsxwriter` - more feature-rich but slower
- `pandas` with ExcelWriter - overkill for simple data export
- `xlwt` - only supports old .xls format

---

### RQ-3: Cron Scheduling in Python

**Question**: How to manage cron jobs programmatically from Python?

**Decision**: `python-crontab` library

**Rationale**:
- Direct cron table manipulation from Python
- Allows adding/removing jobs programmatically
- Works on both Linux and macOS
- Integrates with existing `.claude/scheduled_tasks.json` for reference

**Alternatives considered**:
- System `cron` with shell scripts - adds shell layer
- `schedule` library - only in-process scheduling, doesn't survive restarts
- APScheduler - too heavy for simple cron needs

---

### RQ-4: Error Handling and Retry Strategy

**Question**: How to implement robust retry with exponential backoff?

**Decision**: Use `tenacity` library for retry logic

**Rationale**:
- Standard retry library for Python
- Supports exponential backoff
- Configurable retry conditions (connection errors, 429 rate limits)
- Decorator-based usage is clean

**Alternatives considered**:
- Custom retry implementation - reinventing wheel
- `retry` library - less flexible than tenacity

---

## Technical Stack Summary

| Component | Choice | Version |
|-----------|--------|---------|
| Language | Python | 3.11+ |
| HTTP Client | requests | 2.31+ |
| Excel Writer | openpyxl | 3.1+ |
| Cron Manager | python-crontab | 2.5+ |
| Retry Logic | tenacity | 8.2+ |
| Testing | pytest | 7.4+ |

---

## API Integration Details

### TikTok Shop API Base URL
```
https://open.tiktokapis.com/v2/
```

### Authentication
- OAuth 2.0 client credentials flow
- Access token stored in config or environment variable

### Key Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/order/list/` | GET | Fetch orders with date filter |
| `/product/list/` | GET | Fetch product catalog for top products |

### Rate Limiting
- Default: 100 requests/minute
- Strategy: Implement 1-second delay between requests
- On 429: Exponential backoff starting at 5 seconds

---

## Execution Flow

```
1. Load config (API credentials, storage paths)
2. Calculate yesterday's date range
3. Authenticate with TikTok API
4. Fetch order list for date range
5. Aggregate data (order count, revenue, top products)
6. Write to Excel file
7. Log execution result
8. Exit with appropriate code (0=success, 1=failure)
```

---

## Validation Checklist

- [x] TikTok API credentials available
- [x] Python 3.11+ environment confirmed
- [x] Required packages identified
- [x] API rate limiting strategy defined
- [x] Excel output format confirmed (.xlsx)
- [x] Log file format defined (JSONL)

**Research Status**: ✅ Complete - Ready for Phase 1