try:
    import pytest
    raises = pytest.raises
except ImportError:
    from contextlib import contextmanager
    @contextmanager
    def raises(expected_exception):
        class ExcInfo:
            value = None
        info = ExcInfo()
        try:
            yield info
            raise AssertionError(f"Expected exception {expected_exception.__name__} was not raised")
        except expected_exception as e:
            info.value = e

from dag_scheduler import TaskScheduler, CircularDependencyError



def test_linear_dependency():
    scheduler = TaskScheduler()
    scheduler.add_task("build")
    scheduler.add_task("test", dependencies=["build"])
    scheduler.add_task("deploy", dependencies=["test"])

    order = scheduler.resolve_execution_order()
    assert order == ["build", "test", "deploy"]


def test_parallel_stages():
    scheduler = TaskScheduler()
    # Stage 0: vpc, iam
    # Stage 1: eks_cluster (needs vpc, iam), rds (needs vpc)
    # Stage 2: helm_app (needs eks_cluster, rds)
    scheduler.add_task("vpc")
    scheduler.add_task("iam")
    scheduler.add_task("eks_cluster", dependencies=["vpc", "iam"])
    scheduler.add_task("rds", dependencies=["vpc"])
    scheduler.add_task("helm_app", dependencies=["eks_cluster", "rds"])

    stages = scheduler.resolve_parallel_stages()
    assert stages == [
        ["iam", "vpc"],
        ["eks_cluster", "rds"],
        ["helm_app"]
    ]


def test_circular_dependency_detection():
    scheduler = TaskScheduler()
    scheduler.add_task("A", dependencies=["C"])
    scheduler.add_task("B", dependencies=["A"])
    scheduler.add_task("C", dependencies=["B"])

    with raises(CircularDependencyError) as exc_info:
        scheduler.resolve_execution_order()
    assert "Circular dependency detected" in str(exc_info.value)


def test_isolated_independent_tasks():
    scheduler = TaskScheduler()
    scheduler.add_task("task1")
    scheduler.add_task("task2")
    scheduler.add_task("task3")

    stages = scheduler.resolve_parallel_stages()
    assert len(stages) == 1
    assert sorted(stages[0]) == ["task1", "task2", "task3"]
