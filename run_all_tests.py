#!/usr/bin/env python3
"""
Zero-dependency test runner using Python standard library.
Enables running all interview coding test suites immediately without pip.
"""

import sys
import os
import unittest

# Ensure modules in subdirectories can be imported
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(base_dir, "01-live-python-coding", "01_rate_limiter"))
sys.path.insert(0, os.path.join(base_dir, "01-live-python-coding", "02_dag_task_scheduler"))
sys.path.insert(0, os.path.join(base_dir, "01-live-python-coding", "03_log_metrics_analyzer"))
sys.path.insert(0, os.path.join(base_dir, "01-live-python-coding", "04_retry_backoff_decorator"))
sys.path.insert(0, os.path.join(base_dir, "01-live-python-coding", "05_tfplan_cost_security"))


def run_tests():
    print("==================================================")
    print("  Running Live Python Coding Verification Tests   ")
    print("==================================================")

    # 1. Rate Limiter Tests
    import test_rate_limiter
    test_rate_limiter.test_initial_capacity()
    test_rate_limiter.test_refill_mechanism()
    test_rate_limiter.test_timeout_behavior()
    test_rate_limiter.test_rate_limited_decorator()
    print("✅ 01_rate_limiter tests passed")

    # 2. DAG Scheduler Tests
    import test_dag_scheduler
    test_dag_scheduler.test_linear_dependency()
    test_dag_scheduler.test_parallel_stages()
    test_dag_scheduler.test_circular_dependency_detection()
    test_dag_scheduler.test_isolated_independent_tasks()
    print("✅ 02_dag_task_scheduler tests passed")

    # 3. Log Metrics Analyzer Tests
    import test_log_analyzer
    test_log_analyzer.test_parse_valid_log_line()
    test_log_analyzer.test_parse_invalid_log_line()
    test_log_analyzer.test_log_metrics_aggregation()
    print("✅ 03_log_metrics_analyzer tests passed")

    # 4. Retry Backoff Tests
    import test_retry_backoff
    test_retry_backoff.test_success_on_first_try()
    test_retry_backoff.test_retry_eventual_success()
    test_retry_backoff.test_fatal_error_not_retried()
    test_retry_backoff.test_exceeded_max_retries()
    print("✅ 04_retry_backoff_decorator tests passed")

    # 5. Terraform Plan Security Auditor Tests
    import test_tfplan_parser
    test_tfplan_parser.test_clean_plan_passes()
    test_tfplan_parser.test_detect_database_deletion()
    test_tfplan_parser.test_detect_open_ssh_security_group()
    test_tfplan_parser.test_detect_missing_mandatory_tags()
    print("✅ 05_tfplan_cost_security tests passed")

    print("\n🎉 ALL LIVE CODING SUITES PASSED FLAWLESSLY!\n")


if __name__ == "__main__":
    run_tests()

