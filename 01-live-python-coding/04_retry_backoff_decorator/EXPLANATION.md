# Live Coding Topic: Exponential Backoff with Jitter

## What the Interviewer Is Really Testing
1. **Python Decorator Syntax:** Writing decorators that take arguments requires a 3-tier function structure (`def retry(...) -> def decorator(func) -> def wrapper(*args, **kwargs)`).
2. **`functools.wraps`:** Preserving function metadata (`__name__`, docstrings, `__module__`).
3. **The "Thundering Herd" Problem & Jitter:**
   - Why do we need jitter? If 500 instances fail simultaneously and all retry at exactly 1s, 2s, 4s, they will repeatedly overwhelm the downstream service at synchronized intervals.
   - Adding full jitter (`random.uniform(0, calculated_delay)`) spreads the retries smoothly over time (reference: AWS Architecture blog on exponential backoff and jitter).
4. **Selective Exception Catching:** Never doing a bare `except:`; allowing callers to specify `retryable_exceptions` so client errors like 400 Bad Request or 401 Unauthorized fail fast instead of uselessly retrying.

