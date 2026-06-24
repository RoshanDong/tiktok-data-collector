"""
Logging Module for TikTok Shop Data Fetch Automation
Handles JSONL log writing and log rotation.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from models import FetchLog, FetchStatus


class FetchLogger:
    """Handles logging of fetch operations to JSONL files"""

    def __init__(self, log_dir: Path):
        """
        Initialize logger with log directory path.

        Args:
            log_dir: Directory path for log files (e.g., .kol-agent/tiktok-data/logs/)
        """
        self.log_dir = Path(log_dir)
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        """Ensure log directory exists"""
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _get_log_filename(self, date_str: Optional[str] = None) -> Path:
        """
        Get log filename for a given date.

        Args:
            date_str: Date in YYYY-MM-DD format. Defaults to today.

        Returns:
            Path to the log file
        """
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        return self.log_dir / f"{date_str}.jsonl"

    def write_log(self, log_entry: FetchLog) -> Path:
        """
        Write a single log entry to the daily log file.

        Args:
            log_entry: FetchLog object to write

        Returns:
            Path to the log file that was written
        """
        log_file = self._get_log_filename(log_entry.dateQueried[:10])

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry.to_jsonl_line() + '\n')

        return log_file

    def read_logs(self, date_str: str) -> list:
        """
        Read all log entries for a given date.

        Args:
            date_str: Date in YYYY-MM-DD format

        Returns:
            List of FetchLog objects
        """
        log_file = self._get_log_filename(date_str)

        if not log_file.exists():
            return []

        logs = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        logs.append(FetchLog.from_dict(data))
                    except json.JSONDecodeError:
                        continue

        return logs

    def get_latest_log(self, date_str: str) -> Optional[FetchLog]:
        """
        Get the most recent log entry for a given date.

        Args:
            date_str: Date in YYYY-MM-DD format

        Returns:
            Most recent FetchLog or None if no logs exist
        """
        logs = self.read_logs(date_str)
        return logs[-1] if logs else None

    def log_success(
        self,
        date_queried: str,
        order_count: int,
        total_revenue: float,
        retry_count: int = 0
    ) -> FetchLog:
        """
        Convenience method to log a successful fetch.

        Args:
            date_queried: Date that was queried (YYYY-MM-DD)
            order_count: Number of orders fetched
            total_revenue: Total revenue
            retry_count: Number of retries attempted

        Returns:
            The created FetchLog
        """
        log_entry = FetchLog(
            timestamp=datetime.now().isoformat() + 'Z',
            status=FetchStatus.SUCCESS,
            dateQueried=date_queried,
            orderCount=order_count,
            totalRevenue=total_revenue,
            retryCount=retry_count
        )
        self.write_log(log_entry)
        return log_entry

    def log_failure(
        self,
        date_queried: str,
        error_message: str,
        retry_count: int = 0,
        order_count: int = 0,
        total_revenue: float = 0.0
    ) -> FetchLog:
        """
        Convenience method to log a failed fetch.

        Args:
            date_queried: Date that was queried (YYYY-MM-DD)
            error_message: Description of the error
            retry_count: Number of retries attempted
            order_count: Number of orders processed before failure (0 if none)
            total_revenue: Revenue before failure (0.0 if none)

        Returns:
            The created FetchLog
        """
        log_entry = FetchLog(
            timestamp=datetime.now().isoformat() + 'Z',
            status=FetchStatus.FAILURE,
            dateQueried=date_queried,
            orderCount=order_count,
            totalRevenue=total_revenue,
            errorMessage=error_message,
            retryCount=retry_count
        )
        self.write_log(log_entry)
        return log_entry

    def log_partial(
        self,
        date_queried: str,
        order_count: int,
        total_revenue: float,
        error_message: str,
        retry_count: int = 0
    ) -> FetchLog:
        """
        Convenience method to log a partial success (some data with non-fatal errors).

        Args:
            date_queried: Date that was queried (YYYY-MM-DD)
            order_count: Number of orders successfully fetched
            total_revenue: Total revenue fetched
            error_message: Description of non-fatal errors
            retry_count: Number of retries attempted

        Returns:
            The created FetchLog
        """
        log_entry = FetchLog(
            timestamp=datetime.now().isoformat() + 'Z',
            status=FetchStatus.PARTIAL,
            dateQueried=date_queried,
            orderCount=order_count,
            totalRevenue=total_revenue,
            errorMessage=error_message,
            retryCount=retry_count
        )
        self.write_log(log_entry)
        return log_entry


def get_logger(config: dict) -> FetchLogger:
    """
    Factory function to create a FetchLogger from config dict.

    Args:
        config: Configuration dictionary with 'storage.log_dir' path

    Returns:
        FetchLogger instance
    """
    log_dir = config.get('storage', {}).get('log_dir', '.kol-agent/tiktok-data/logs')
    return FetchLogger(Path(log_dir))


if __name__ == "__main__":
    # Test logger
    from pathlib import Path

    test_log_dir = Path(".kol-agent/tiktok-data/logs")
    logger = FetchLogger(test_log_dir)

    # Test success log
    log = logger.log_success("2026-06-09", 156, 4523.50, 0)
    print(f"Success log written to: {logger._get_log_filename('2026-06-09')}")

    # Test failure log
    log = logger.log_failure("2026-06-08", "API rate limit exceeded", 3)
    print(f"Failure log written")

    # Read back
    logs = logger.read_logs("2026-06-09")
    print(f"Logs for 2026-06-09: {len(logs)} entries")