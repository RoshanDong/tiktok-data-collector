# Feature Specification: TikTok Shop Data Fetch Automation

**Feature Branch**: `001-tiktok-data-fetch`

**Created**: 2026-06-10

**Status**: Draft

**Input**: User description: "我需要再创建一个新的定时任务，用于每日自动拉取tiktok店铺后台数据，然后格式化存储到excel表格中"

## Clarifications

### Session 2026-06-10

- Q: Top 10 products 排名规则是什么？ → A: 按销售数量（quantity sold）降序排列
- Q: Excel 文件应该存储在哪里？ → A: 项目本地目录 `.kol-agent/tiktok-data/`
- Q: 通知方式是什么？ → A: 不使用邮件通知，改为在 `.kol-agent/tiktok-data/logs/` 目录创建日志文件，记录任务结果摘要和错误详情

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Daily Sales Data Sync (Priority: P1)

As a business manager, I want the system to automatically fetch daily sales data from TikTok Shop each morning so I can review yesterday's performance without manual intervention.

**Why this priority**: Daily sales data is the core metric for business decision-making. This is the primary use case that justifies the automation investment.

**Independent Test**: Can be fully tested by verifying that after a scheduled run, an Excel file exists with yesterday's sales data including order count, revenue, and product breakdown.

**Acceptance Scenarios**:

1. **Given** the scheduled time has arrived, **When** the system executes the fetch task, **Then** it should retrieve TikTok Shop data for the previous day and store it in an Excel file organized by date.
2. **Given** TikTok Shop API is available, **When** the fetch completes, **Then** the Excel file should contain: date, total orders, total revenue, top products by quantity sold.
3. **Given** the fetch task has completed successfully, **When** I open the Excel file, **Then** I should see clear column headers and properly formatted numeric values.

---

### User Story 2 - Historical Data Retention (Priority: P2)

As a business manager, I want historical data to be accumulated in separate files or sheets organized by month so I can compare performance across different periods.

**Why this priority**: Enables trend analysis and period-over-period comparison, which is essential for strategic planning.

**Independent Test**: Can be tested by checking that after 2+ months of runs, files/sheets exist for each month with consistent data structure.

**Acceptance Scenarios**:

1. **Given** data has been collected for multiple months, **When** I access the storage location, **Then** I should find files named with year-month pattern (e.g., `tiktok-sales-2026-06.xlsx`).
2. **Given** a new month begins, **When** the daily fetch runs on the 1st, **Then** it should create a new file or sheet for the current month.

---

### User Story 3 - Error Notification (Priority: P3)

As a business manager, I want to be notified when the daily fetch fails so I can take manual action or escalate to technical support.

**Why this priority**: Without notification, failures go unnoticed and data gaps may not be discovered until too late to remediate.

**Independent Test**: Can be tested by simulating an API failure and verifying that a notification is sent with failure details.

**Acceptance Scenarios**:

1. **Given** the TikTok Shop API returns an error, **When** the fetch task fails, **Then** the system should send a notification with the error type and timestamp.
2. **Given** the network connection is unavailable, **When** the fetch task runs, **Then** the system should retry up to 3 times before reporting failure.

---

### Edge Cases

- What happens when TikTok Shop API rate limits the requests? → System should implement backoff and retry
- How does the system handle a day with zero orders? → Should still create file with zero values, not skip
- What if the Excel file is already open by another user? → Should retry with timestamp suffix or report error
- How does the system handle timezone differences for daily cutoff? → Uses shop's configured timezone for day boundaries

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST fetch sales data from TikTok Shop API daily at a configured time (default: 6:00 AM)
- **FR-002**: System MUST retrieve the following metrics for the previous day: total orders, total revenue, top 10 products by quantity sold (descending order)
- **FR-003**: System MUST format fetched data into an Excel file with columns: Date, Order Count, Revenue, Top Products (ranked by quantity sold descending)
- **FR-004**: System MUST store Excel files in `.kol-agent/tiktok-data/` directory with naming pattern `tiktok-sales-YYYY-MM.xlsx`
- **FR-005**: System MUST write task execution results to log files in `.kol-agent/tiktok-data/logs/` directory, including task summary and error details on failure
- **FR-006**: System MUST retry failed API calls up to 3 times with exponential backoff before reporting failure
- **FR-007**: System MUST log all fetch activities with timestamps for audit purposes

### Key Entities

- **DailySalesData**: Represents one day's sales summary from TikTok Shop
  - date: The date of the sales data (YYYY-MM-DD)
  - orderCount: Total number of orders placed
  - totalRevenue: Total revenue in local currency
  - topProducts: List of top 10 products ranked by quantity sold (descending)
- **FetchLog**: Audit trail of all fetch operations
  - timestamp: When the fetch was attempted
  - status: success/failure/partial
  - errorMessage: Details if failed
  - recordsRetrieved: Number of data records fetched

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Daily fetch task completes within 5 minutes of scheduled time
- **SC-002**: Excel files contain accurate data matching TikTok Shop backend records
- **SC-003**: System maintains 99% successful fetch rate over any 30-day period
- **SC-004**: Notification sent within 10 minutes of fetch completion (success or failure)
- **SC-005**: Data is available for review by 7:00 AM local time each day

## Assumptions

- TikTok Shop API credentials (client key/secret) are available and stored securely
- There is a designated server/environment where the scheduled task will run
- Local storage has sufficient space for monthly Excel files (~10MB estimated)
- User has basic Excel knowledge to open and review files
- Local directory `.kol-agent/tiktok-data/logs/` has write permissions for log files
- TikTok Shop API supports programmatic access and has no IP restrictions blocking the server