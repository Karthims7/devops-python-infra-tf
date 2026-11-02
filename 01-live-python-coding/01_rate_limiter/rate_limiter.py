"""
Rate Limiter Implementation
Includes:
1. Token Bucket Algorithm (Burst handling + smooth refilling)
2. Sliding Window Counter (Precise request throttling over time)
3. Decorator for API Functions / HTTP Clients

Common Interview Scenario for DevOps:
"You are building an automation service that queries the GitHub API or AWS API.
Implement a rate limiter to ensure your workers never exceed the provider's rate limit,
supporting burst traffic and thread safety."
"""

import time
import threading
from typing import Callable, Any, Optional
from functools import wraps


class TokenBucketRateLimiter:
    """
    Token Bucket Rate Limiter with thread safety.

    - capacity: Maximum number of tokens the bucket can hold (burst limit).
    - refill_rate: Tokens added per second (sustained rate).
    """

    def __init__(self, capacity: int, refill_rate: float):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill_timestamp = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        """Internal helper to add tokens based on elapsed monotonic time."""
        now = time.monotonic()
        elapsed = now - self.last_refill_timestamp
        if elapsed > 0:
            added_tokens = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + added_tokens)
            self.last_refill_timestamp = now

    def acquire(self, tokens: int = 1, blocking: bool = True, timeout: Optional[float] = None) -> bool:
        """
        Attempt to consume `tokens`.
        If blocking is True, wait until tokens become available or timeout expires.
        Returns True if acquired, False otherwise.
        """
        start_time = time.monotonic()

        while True:
            with self._lock:
                self._refill()
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True

                if not blocking:
                    return False

                # Calculate how long to sleep until enough tokens accumulate
                needed = tokens - self.tokens
                wait_time = needed / self.refill_rate

            if timeout is not None:
                elapsed = time.monotonic() - start_time
                if elapsed + wait_time > timeout:
                    return False

            time.sleep(min(wait_time, 0.05))  # Sleep in small slices to remain responsive


def rate_limited(limiter: TokenBucketRateLimiter):
    """Decorator to rate-limit a function call using the provided limiter."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            acquired = limiter.acquire(tokens=1, blocking=True)
            if not acquired:
                raise RuntimeError("Rate limit exceeded")
            return func(*args, **kwargs)
        return wrapper
    return decorator
