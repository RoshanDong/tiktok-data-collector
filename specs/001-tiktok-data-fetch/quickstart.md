# Quickstart: TikTok Shop Data Fetch Automation

**Feature**: 001-tiktok-data-fetch
**Date**: 2026-06-10

---

## Prerequisites

1. **Python 3.11+** installed
2. **TikTok Shop Seller API** credentials (client ID + client secret)
3. **write access** to `.kol-agent/` directory

---

## Setup

### 1. Install Dependencies

```bash
pip install requests openpyxl python-crontab tenacity pytest pytest-mock
```

### 2. Configure API Credentials

Create `.kol-agent/tiktok-config.json`:
```json
{
  "tiktok_api": {
    "client_key": "your_client_key",
    "client_secret": "your_client_secret"
  },
  "storage": {
    "data_dir": ".kol-agent/tiktok-data",
    "log_dir": ".kol-agent/tiktok-data/logs"
  },
  "schedule": {
    "hour": 6,
    "minute": 0
  }
}
```

### 3. Create Directory Structure

```bash
mkdir -p .kol-agent/tiktok-data/logs
```

---

## Running the Script

### Manual Run

```bash
python3 .kol-agent/scripts/tiktok-fetch.py
```

Expected output on success:
```
[2026-06-10 06:00:15] Starting TikTok data fetch
[2026-06-10 06:00:18] Authenticated successfully
[2026-06-10 06:00:25] Fetched 156 orders for 2026-06-09
[2026-06-10 06:00:26] Excel file written: .kol-agent/tiktok-data/tiktok-sales-2026-06.xlsx
[2026-06-10 06:00:26] Log entry written
[2026-06-10 06:00:26] SUCCESS - Completed in 11 seconds
```

### Verify Output

Check Excel file was created:
```bash
ls -la .kol-agent/tiktok-data/tiktok-sales-*.xlsx
```

Check log entry:
```bash
cat .kol-agent/tiktok-data/logs/2026-06-10.jsonl
```

---

## Testing Validation

### Run Unit Tests

```bash
pytest .kol-agent/scripts/tests/ -v
```

### Test Scenarios

| Scenario | Expected Result |
|----------|-----------------|
| Normal run with data | Excel created, log written, exit code 0 |
| Zero orders day | Excel created with zero values, log written |
| API rate limited | Retry with backoff, then success or failure logged |
| Invalid credentials | Error logged, exit code 1, notification |
| Network unavailable | Retry 3 times, then failure logged |

---

## Scheduling (Optional)

To add to cron (runs daily at 6 AM):

```bash
crontab -e
# Add line:
0 6 * * * /usr/bin/python3 /Users/yuelnn/RoshanProgram/Cursor/First-CC/.kol-agent/scripts/tiktok-fetch.py >> /Users/yuelnn/RoshanProgram/Cursor/First-CC/.kol-agent/tiktok-data/logs/cron.log 2>&1
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Authentication failed" | Verify client_key and client_secret in config |
| "Permission denied" | Check write permissions on .kol-agent/tiktok-data/ |
| "Module not found" | Run `pip install` again for missing package |
| Excel file corrupted | Ensure no other program has file open |

---

## File Locations Reference

| File | Path |
|------|------|
| Main script | `.kol-agent/scripts/tiktok-fetch.py` |
| Config | `.kol-agent/tiktok-config.json` |
| Excel data | `.kol-agent/tiktok-data/tiktok-sales-YYYY-MM.xlsx` |
| Execution logs | `.kol-agent/tiktok-data/logs/YYYY-MM-DD.jsonl` |
| Cron log (if scheduled) | `.kol-agent/tiktok-data/logs/cron.log` |

---

**Quickstart Status**: ✅ Ready for `/speckit-tasks`