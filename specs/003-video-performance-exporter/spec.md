# Feature Specification: Video Performance Data Exporter

**Feature Branch**: `003-video-performance-exporter`

**Created**: 2026-06-12

**Status**: Draft

**Input**: User description: "在.kol-agent/scripts/get_shop_video_performance_api_tester.py脚本的基础上，帮我设计一个脚本批量导出近7天每天的全量视频数据，包含所有的数据信息，以excel表格形式存储。"

## Clarifications

### Session 2026-06-12

- Q: 输出格式选择 → A: 多文件模式（每天一个 .xlsx 文件），统一放在同一目录下

## User Scenarios & Testing

### User Story 1 - Daily Video Performance Export (Priority: P1)

As a seller, I want to export full video performance data for each of the last 7 days so that I can analyze video marketing effectiveness over the past week.

**Why this priority**: Core functionality - without this the feature has no value.

**Independent Test**: Run the script and verify an Excel file is created containing video data for each of the 7 days.

**Acceptance Scenarios**:

1. **Given** the API credentials are valid, **When** the user runs the export script, **Then** it should create 7 Excel files (one per day) in the output directory
2. **Given** the API credentials are valid, **When** the user runs the export script, **Then** each Excel file should contain all video records for that day including: video ID, title, username, creator info, post time, duration, hashtags, GMV, GPM, views, CTR, SKU orders, items sold, and products
3. **Given** the API credentials are invalid, **When** the user runs the export script, **Then** it should display a clear error message and exit gracefully

---

### User Story 2 - Export Directory Structure (Priority: P2)

As a seller, I want all exported files organized in a single directory so I can easily locate and manage exports.

**Why this priority**: Keeps exports clean and discoverable.

**Independent Test**: Verify all 7 Excel files exist in the same output directory after export.

**Acceptance Scenarios**:

1. **Given** the export completes successfully, **When** the files are created, **Then** all files should be in the same directory (default: `.kol-agent/tiktok-data/exports/`)

---

### User Story 3 - Progress and Error Reporting (Priority: P3)

As a user, I want clear progress indicators during export so I know the script is working and how much remains.

**Why this priority**: Exporting 7 days of data takes time; users need feedback to know it's not stuck.

**Independent Test**: Run the script and observe console output shows day-by-day progress and record counts.

**Acceptance Scenarios**:

1. **Given** the export is in progress, **When** each day's data is being fetched, **Then** the console should show which date is being processed and record count
2. **Given** an error occurs on a specific day, **When** the script continues to next day, **Then** it should log the error but not stop the entire export

---

## Requirements

### Functional Requirements

- **FR-001**: Script MUST fetch all video performance data for each of the last 7 days from TikTok Shop Video Performance API
- **FR-002**: Script MUST support pagination to retrieve all videos (not just first page)
- **FR-003**: Script MUST write data to Excel format (.xlsx) with proper column headers
- **FR-004**: Each video record MUST include all fields: video ID, title, username, creator (open_id, user_name, nick_name, author_type), video_post_time, duration, hash_tags, gmv (amount, currency), gpm (amount, currency), avg_customers, sku_orders, items_sold, views, click_through_rate, products (id, name)
- **FR-005**: Script MUST create one Excel file per day (格式: `video_performance_YYYY-MM-DD.xlsx`)，统一存放在同一输出目录下
- **FR-006**: Script MUST handle API rate limits gracefully (retry with backoff)
- **FR-007**: Script MUST handle missing/null fields in API responses without crashing
- **FR-008**: Script MUST output files to a configurable directory (default: .kol-agent/tiktok-data/exports/)
- **FR-009**: Script MUST skip days with no data rather than creating empty files

### Key Entities

- **VideoPerformance**: Represents a single video's performance metrics for a given day
  - video_id: string
  - title: string
  - username: string
  - creator: object (open_id, user_name, nick_name, author_type)
  - video_post_time: datetime
  - duration: integer (seconds)
  - hash_tags: list of strings
  - gmv: object (amount, currency)
  - gpm: object (amount, currency)
  - avg_customers: integer
  - sku_orders: integer
  - items_sold: integer
  - views: integer
  - click_through_rate: string
  - products: list of objects (id, name)
- **DailyExport**: A collection of VideoPerformance records for a specific date with metadata
  - date: date
  - total_count: integer
  - records: list of VideoPerformance
  - export_time: datetime

## Success Criteria

### Measurable Outcomes

- **SC-001**: Script successfully exports data for all 7 days within 30 minutes
- **SC-002**: Each Excel file contains 100% of videos returned by the API for that day
- **SC-003**: All video fields specified in FR-004 are present in the output Excel
- **SC-004**: Script handles API errors on individual days without stopping entire export
- **SC-005**: Output Excel files are valid and openable in Excel/Google Sheets without data corruption

## Assumptions

- The TikTok Shop Video Performance API (version 202605) remains available and unchanged
- API credentials stored in .kol-agent/tiktok-config.json are valid and have analytics scope
- The 7-day window is relative to today (2026-06-12), so dates will be 2026-06-05 through 2026-06-11
- Data volume: up to ~3500 videos per day based on recent API responses
- Excel library (openpyxl) is available in the environment
- User has sufficient disk space for export files (~10-50MB estimated for 7 days of full data)