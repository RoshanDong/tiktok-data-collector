"""
Retry Handler with Exponential Backoff
Uses tenacity library for robust retry logic.
"""

from functools import wraps
from typing import Callable, Any, TypeVar, Type
import time
import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    after_log
)
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Type variable for generic function return
T = TypeVar('T')


class RetryConfig:
    """Configuration for retry behavior"""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 5.0,
        max_delay: float = 60.0,
        multiplier: float = 2.0
    ):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.multiplier = multiplier

    def to_dict(self) -> dict:
        return {
            "max_attempts": self.max_attempts,
            "initial_delay_seconds": self.initial_delay,
            "max_delay_seconds": self.max_delay
        }


class RateLimitError(Exception):
    """Exception raised when rate limit is exceeded"""
    pass


class NetworkError(Exception):
    """Exception raised for network-related errors"""
    pass


class APIError(Exception):
    """Exception raised for general API errors"""
    pass


def create_retry_decorator(config: RetryConfig):
    """
    Create a retry decorator with custom configuration.

    Args:
        config: RetryConfig object with retry parameters

    Returns:
        Configured retry decorator
    """
    return retry(
        stop=stop_after_attempt(config.max_attempts),
        wait=wait_exponential(
            multiplier=config.multiplier,
            min=config.initial_delay,
            max=config.max_delay
        ),
        retry=retry_if_exception_type((requests.RequestException, RateLimitError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        after=after_log(logger, logging.INFO)
    )


def retry_on_rate_limit(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator specifically for handling rate limit (429) responses.
    Uses exponential backoff starting at 5 seconds.

    Args:
        func: Function to retry

    Returns:
        Wrapped function with retry logic
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        max_attempts = 3
        base_delay = 5

        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except RateLimitError:
                if attempt < max_attempts - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        f"Rate limit hit, retrying in {delay}s (attempt {attempt + 1}/{max_attempts})"
                    )
                    time.sleep(delay)
                else:
                    raise

    return wrapper


def retry_on_network_error(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator for handling network errors with retry.

    Args:
        func: Function to retry

    Returns:
        Wrapped function with retry logic
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        max_attempts = 3
        base_delay = 2

        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except (requests.ConnectionError, requests.Timeout, NetworkError):
                if attempt < max_attempts - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        f"Network error, retrying in {delay}s (attempt {attempt + 1}/{max_attempts})"
                    )
                    time.sleep(delay)
                else:
                    raise

    return wrapper


class RetryHandler:
    """
    Handler class for managing retry logic with configurable parameters.
    """

    def __init__(self, config: RetryConfig):
        self.config = config
        self.decorator = create_retry_decorator(config)

    def execute(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Execute a function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result of func
        """
        decorated_func = self.decorator(func)
        return decorated_func(*args, **kwargs)

    @staticmethod
    def from_config(config_dict: dict) -> 'RetryHandler':
        """
        Create RetryHandler from configuration dictionary.

        Args:
            config_dict: Dictionary with retry configuration

        Returns:
            RetryHandler instance
        """
        retry_config = config_dict.get('retry', {})
        config = RetryConfig(
            max_attempts=retry_config.get('max_attempts', 3),
            initial_delay=float(retry_config.get('initial_delay_seconds', 5)),
            max_delay=float(retry_config.get('max_delay_seconds', 60))
        )
        return RetryHandler(config)


if __name__ == "__main__":
    # Test retry handler
    import json
    from pathlib import Path

    config_dict = {
        "retry": {
            "max_attempts": 3,
            "initial_delay_seconds": 5,
            "max_delay_seconds": 60
        }
    }

    handler = RetryHandler.from_config(config_dict)
    print(f"RetryHandler created with config: {handler.config.to_dict()}")