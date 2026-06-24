# Data Model: Video Performance Data Exporter

**Feature**: `specs/003-video-performance-exporter/spec.md`

## Entities

### VideoPerformance

Represents a single video's performance metrics for a given day.

| Field | Type | Description |
|-------|------|-------------|
| `video_id` | string | Unique video identifier |
| `title` | string | Video title |
| `username` | string | Account username that posted the video |
| `creator.open_id` | string | Creator's open ID |
| `creator.user_name` | string | Creator's username |
| `creator.nick_name` | string | Creator's nickname |
| `creator.author_type` | string | OFFICIAL, AFFILIATE_ACCOUNTS, etc. |
| `video_post_time` | datetime | When the video was posted |
| `duration` | integer | Video duration in seconds |
| `hash_tags` | list[string] | Hashtags associated with the video |
| `gmv.amount` | string | Gross Merchandise Value (amount) |
| `gmv.currency` | string | Currency code (USD) |
| `gpm.amount` | string | Gross Merchandise Value per thousand views |
| `gpm.currency` | string | Currency code (USD) |
| `avg_customers` | integer | Average number of customers |
| `sku_orders` | integer | Number of SKU orders |
| `items_sold` | integer | Total items sold |
| `views` | integer | Total video views |
| `click_through_rate` | string | CTR as decimal string (e.g., "0.0620") |
| `products` | list[Product] | List of associated products |

### Product

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Product ID |
| `name` | string | Product name |

### DailyExport

Collection of VideoPerformance records for a specific date.

| Field | Type | Description |
|-------|------|-------------|
| `date` | date | The export date (YYYY-MM-DD) |
| `total_count` | integer | Total number of videos for this day |
| `records` | list[VideoPerformance] | All video performance records |
| `export_time` | datetime | When the export was performed |
| `latest_available_date` | string | API's latest available data date |
| `next_page_token` | string | Pagination token for next batch |

## Excel Output Schema

File: `video_performance_YYYY-MM-DD.xlsx`
Sheet: `Videos`

| Column | Source Field | Notes |
|--------|-------------|-------|
| A | video_id | |
| B | title | |
| C | username | |
| D | creator_user_name | Flattened from creator.user_name |
| E | creator_nick_name | Flattened from creator.nick_name |
| F | creator_author_type | Flattened from creator.author_type |
| G | video_post_time | Formatted as YYYY-MM-DD HH:MM:SS |
| H | duration | In seconds |
| I | hash_tags | Joined with comma ", " |
| J | gmv_amount | From gmv.amount |
| K | gmv_currency | From gmv.currency |
| L | gpm_amount | From gpm.amount |
| M | gpm_currency | From gpm.currency |
| N | avg_customers | |
| O | sku_orders | |
| P | items_sold | |
| Q | views | |
| R | click_through_rate | |
| S | products | Joined with "; " (id: name format) |