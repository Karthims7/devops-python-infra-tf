"""
High-Throughput Log Stream & Latency Percentile Analyzer
Common Interview Scenario for DevOps:
"You are given streaming log lines from an API gateway or ingress controller.
Each line has: TIMESTAMP METHOD PATH STATUS_CODE DURATION_MS
Calculate:
1. Total request count and error rate (4xx, 5xx)
2. Top N requested paths
3. P50, P90, P95, and P99 response latencies
Make sure the solution processes logs as a generator stream to handle multi-gigabyte files."
"""

import re
import math
from typing import Iterator, Dict, Any, List, Optional
from collections import Counter
from dataclasses import dataclass


LOG_REGEX = re.compile(
    r'^(?P<timestamp>\S+)\s+(?P<method>[A-Z]+)\s+(?P<path>\S+)\s+(?P<status>\d{3})\s+(?P<latency_ms>\d+(?:\.\d+)?)$'
)


@dataclass
class LogEntry:
    timestamp: str
    method: str
    path: str
    status: int
    latency_ms: float


def parse_log_line(line: str) -> Optional[LogEntry]:
    """Parse a single log string into structured LogEntry. Returns None if invalid."""
    match = LOG_REGEX.match(line.strip())
    if not match:
        return None
    data = match.groupdict()
    return LogEntry(
        timestamp=data["timestamp"],
        method=data["method"],
        path=data["path"],
        status=int(data["status"]),
        latency_ms=float(data["latency_ms"]),
    )


class LogStreamMetrics:
    def __init__(self):
        self.total_requests: int = 0
        self.status_counts: Counter = Counter()
        self.path_counts: Counter = Counter()
        self.latencies: List[float] = []

    def ingest_line(self, line: str) -> bool:
        """Process a single line. Returns True if parsed successfully."""
        entry = parse_log_line(line)
        if not entry:
            return False

        self.total_requests += 1
        self.status_counts[entry.status] += 1
        self.path_counts[entry.path] += 1
        self.latencies.append(entry.latency_ms)
        return True

    def ingest_stream(self, stream: Iterator[str]) -> None:
        """Ingest an iterable/generator stream of log lines."""
        for line in stream:
            self.ingest_line(line)

    def calculate_percentile(self, percentile: float) -> float:
        """
        Calculate latency percentile (0 to 100).
        Uses nearest-rank / linear interpolation logic.
        """
        if not self.latencies:
            return 0.0
        if not (0 <= percentile <= 100):
            raise ValueError("Percentile must be between 0 and 100")

        # Sort on demand (in an interview, mention reservoir sampling / t-digest for infinite streams)
        sorted_lat = sorted(self.latencies)
        k = (len(sorted_lat) - 1) * (percentile / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_lat[int(k)]
        d0 = sorted_lat[int(f)] * (c - k)
        d1 = sorted_lat[int(c)] * (k - f)
        return round(d0 + d1, 2)

    def get_summary(self, top_paths_limit: int = 5) -> Dict[str, Any]:
        """Generate comprehensive metrics report."""
        if self.total_requests == 0:
            return {"total_requests": 0, "error_rate": 0.0}

        error_count = sum(
            count for status, count in self.status_counts.items() if status >= 400
        )
        error_rate = round((error_count / self.total_requests) * 100, 2)

        return {
            "total_requests": self.total_requests,
            "error_rate_pct": error_rate,
            "top_paths": self.path_counts.most_common(top_paths_limit),
            "p50_latency_ms": self.calculate_percentile(50),
            "p90_latency_ms": self.calculate_percentile(90),
            "p95_latency_ms": self.calculate_percentile(95),
            "p99_latency_ms": self.calculate_percentile(99),
        }

