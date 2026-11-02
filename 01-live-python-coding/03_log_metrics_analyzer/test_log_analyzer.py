from log_analyzer import parse_log_line, LogStreamMetrics, LogEntry


def test_parse_valid_log_line():
    raw = "2026-11-03T10:00:00Z GET /api/v1/vehicles 200 45.2"
    entry = parse_log_line(raw)
    assert entry is not None
    assert entry.method == "GET"
    assert entry.path == "/api/v1/vehicles"
    assert entry.status == 200
    assert entry.latency_ms == 45.2


def test_parse_invalid_log_line():
    raw = "malformed log line without proper tokens"
    assert parse_log_line(raw) is None


def test_log_metrics_aggregation():
    logs = [
        "2026-11-03T10:00:01Z GET /api/v1/telemetry 200 10.0",
        "2026-11-03T10:00:02Z POST /api/v1/telemetry 201 20.0",
        "2026-11-03T10:00:03Z GET /api/v1/telemetry 500 100.0",
        "2026-11-03T10:00:04Z GET /healthz 200 5.0",
        "2026-11-03T10:00:05Z GET /api/v1/routes 404 15.0",
    ]

    metrics = LogStreamMetrics()
    metrics.ingest_stream(iter(logs))
    summary = metrics.get_summary()

    assert summary["total_requests"] == 5
    # 2 errors out of 5 -> 40.0%
    assert summary["error_rate_pct"] == 40.0
    # top path is /api/v1/telemetry (3 requests)
    assert summary["top_paths"][0] == ("/api/v1/telemetry", 3)
    # Latencies: [5, 10, 15, 20, 100]
    # P50 should be 15.0
    assert summary["p50_latency_ms"] == 15.0
