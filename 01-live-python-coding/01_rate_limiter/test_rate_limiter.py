import time
from rate_limiter import TokenBucketRateLimiter, rate_limited


def test_initial_capacity():
    limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2.0)
    for _ in range(5):
        assert limiter.acquire(blocking=False) is True
    # 6th should fail non-blocking
    assert limiter.acquire(blocking=False) is False


def test_refill_mechanism():
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate=10.0)  # 10 tokens per sec -> 0.1s per token
    assert limiter.acquire(blocking=False) is True
    assert limiter.acquire(blocking=False) is True
    assert limiter.acquire(blocking=False) is False

    time.sleep(0.12)
    assert limiter.acquire(blocking=False) is True


def test_timeout_behavior():
    limiter = TokenBucketRateLimiter(capacity=1, refill_rate=0.5)  # 1 token every 2 seconds
    assert limiter.acquire(blocking=False) is True

    start = time.monotonic()
    # Requesting with 0.1s timeout when 2s needed should fail
    success = limiter.acquire(blocking=True, timeout=0.1)
    duration = time.monotonic() - start

    assert success is False
    assert duration < 0.3


def test_rate_limited_decorator():
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate=5.0)

    @rate_limited(limiter)
    def call_api(val: int) -> int:
        return val * 2

    assert call_api(10) == 20
    assert call_api(20) == 40
