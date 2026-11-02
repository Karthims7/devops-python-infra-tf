# Senior Python for DevOps & Platform Engineers | Deep Dive Q&A

### Q1: When should you use `threading`, `multiprocessing`, and `asyncio` in Python DevOps automation?
- **`asyncio` (Single-threaded cooperative multitasking):** Best for massive high-volume I/O-bound tasks (e.g. querying 5,000 GitHub repositories or polling hundreds of Kubernetes pod status endpoints concurrently). Low memory footprint, minimal context switching overhead.
- **`threading` (Multi-threading with GIL):** Good for standard I/O-bound tasks (network requests, disk writes) where third-party synchronous libraries (like `requests` or `boto3`) are used. Python releases the GIL during I/O operations.
- **`multiprocessing` (Bypasses GIL):** Essential for CPU-bound tasks (e.g., intensive image parsing, cryptographic hashing, parsing gigabytes of raw JSON/HCL logs across multiple CPU cores).

### Q2: Why use `time.monotonic()` instead of `time.time()` for rate limiters, timeouts, and benchmarking?
- `time.time()` returns wall-clock time (seconds since Epoch). It is subject to NTP clock sync adjustments, daylight saving time adjustments, or manual system time changes, which can jump forwards or backwards.
- `time.monotonic()` is guaranteed to never move backwards and progresses at a steady rate. Perfect for calculating elapsed time, retry backoff, and rate limiting.

### Q3: How do Python generators save memory in cloud infrastructure pipelines?
- Regular list comprehension `[line.strip() for line in file]` loads all lines into RAM at once. For a 10 GB access log, this triggers an OOM (Out Of Memory) kill.
- A generator expression `(line.strip() for line in file)` or generator function with `yield` produces one item at a time lazily on demand ($O(1)$ memory).

### Q4: What is the purpose of `functools.wraps` when writing decorators?
- Decorating a function replaces the original function object with the inner wrapper. Without `@wraps(func)`, metadata such as `func.__name__`, `func.__doc__`, and `func.__annotations__` are replaced by the wrapper's metadata, breaking introspection, logging, and documentation tools.

### Q5: How do context managers (`with` statement) work under the hood?
- A context manager implements `__enter__()` and `__exit__(exc_type, exc_val, exc_tb)`.
- In `__enter__`, resources (such as temporary files, SSH connections, database transactions, or locks) are acquired.
- In `__exit__`, cleanup occurs reliably even if an unhandled exception is raised in the block.
- Alternatively, Python's `contextlib.contextmanager` decorator converts a generator function with a `try...finally` block into a context manager.

