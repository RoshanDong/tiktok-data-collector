# Quickstart: Video Performance Data Exporter

**Feature**: `specs/003-video-performance-exporter/spec.md`

## Prerequisites

- Python 3.9+
- TikTok API credentials configured in `.kol-agent/tiktok-config.json`
- Required packages: `requests`, `openpyxl`, `tenacity`

```bash
pip install requests openpyxl tenacity
```

## Run the Export

```bash
# Default: export last 7 days to .kol-agent/tiktok-data/exports/
python3 .kol-agent/scripts/export_video_performance.py
```

## Output

- Files: `video_performance_YYYY-MM-DD.xlsx` (one per day)
- Location: `.kol-agent/tiktok-data/exports/` (configurable)
- Sheets: Single sheet `Videos` per file
- Columns: video_id, title, username, creator info, GMV, GPM, views, CTR, products, etc.

## Validate

1. Check output directory has 7 files:
```bash
ls -la .kol-agent/tiktok-data/exports/video_performance_*.xlsx | wc -l
# Expected: 7
```

2. Open any file and verify:
   - Column headers present (row 1)
   - Video records start from row 2
   - All fields populated (no crashes on missing fields)
   - Data corresponds to correct date range

3. Verify pagination (check total_count in API matches row count):
```bash
# Each file should contain all videos for that day (no data missing)
```

## Configuration Options

```bash
# Custom output directory
python3 .kol-agent/scripts/export_video_performance.py --output-dir /path/to/dir

# Custom date range (override default 7 days)
python3 .kol-agent/scripts/export_video_performance.py --start-date 2026-06-01 --end-date 2026-06-07
```