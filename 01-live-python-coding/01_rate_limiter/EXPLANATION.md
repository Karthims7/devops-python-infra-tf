# Live Coding Topic: Rate Limiter (Token Bucket)

## What the Interviewer Is Really Testing
1. **Concurrency and Thread Safety:** Do you use `threading.Lock` appropriately to prevent race conditions when multiple worker threads share the limiter?
2. **Time Precision:** Do you use `time.monotonic()` instead of `time.time()`? (`time.time()` can jump backwards due to NTP updates or clock drift).
3. **API Design & Pythonic Idioms:** Using decorators (`@wraps`), type hints, custom exceptions, and clean argument validation.
4. **Calculations without Periodic Background Threads:** Notice that the refill calculation happens *lazily* on-demand (`elapsed * refill_rate`) instead of running an expensive background daemon thread ticking every 1ms.

## Step-by-Step Interview Narration
- **Step 1: Clarify Requirements**
  - *"Should this limiter support burst traffic or strict evenly-spaced requests?"* (Token Bucket allows burst up to capacity; Leaky Bucket forces smooth flow).
  - *"Is this single-process multi-threaded, or distributed across multiple instances like Redis?"*
- **Step 2: Propose Algorithm**
  - State clearly: *"I will implement a Token Bucket algorithm using lazy refill. Instead of a background worker adding tokens every millisecond, we compute the tokens to add based on `time.monotonic() - last_refill`."*
- **Step 3: Handle Edge Cases**
  - Zero/negative inputs validation.
  - Floating point arithmetic precision.
  - Blocking vs non-blocking calls with configurable timeout.

