"""
Production-Grade Exponential Backoff & Jitter Retry Decorator
Common Interview Scenario for DevOps:
"You are writing Python tools that query cloud APIs and GitHub API.
Network blips and HTTP 429 / 503 errors occur frequently.
Implement a generic, reusable @retry decorator with exponential backoff,
jitter (to prevent the thundering herd problem), configurable retryable exceptions,
and logging hooks."
"""

import time
import random
import logging
from functools import wraps
from typing import Callable, Any, Tuple, Type, Optional

logger = logging.getLogger("retry_decorator")


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 0.5,
    backoff_factor: float = 2.0,
    max_delay: float = 30.0,
    jitter: bool = True,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry_callback: Optional[Callable[[Exception, int, float], None]] = None,
):
    """
    Decorator for retrying a function with exponential backoff and jitter.

    Delay formula: min(max_delay, initial_delay * (backoff_factor ** attempt))
    With jitter: random.uniform(0, calculated_delay)
    """
    if max_retries < 0:
        raise ValueError("max_retries must be >= 0")
    if initial_delay <= 0 or backoff_factor < 1.0:
        raise ValueError("Invalid backoff configuration")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as exc:
                    attempt += 1
                    if attempt > max_retries:
                        func_name = getattr(func, "__name__", str(func))
                        logger.error(
                            f"Function {func_name} failed after {attempt} attempts: {exc}"
                        )
                        raise

                    # Calculate raw exponential backoff
                    raw_delay = initial_delay * (backoff_factor ** (attempt - 1))
                    capped_delay = min(max_delay, raw_delay)

                    # Apply full jitter if enabled
                    delay = random.uniform(0, capped_delay) if jitter else capped_delay

                    if on_retry_callback:
                        on_retry_callback(exc, attempt, delay)

                    time.sleep(delay)

        return wrapper

    return decorator
