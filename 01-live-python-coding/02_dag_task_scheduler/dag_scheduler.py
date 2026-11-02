"""
DAG Task Scheduler & Dependency Resolver
Common Interview Scenario for DevOps:
"Given a set of infrastructure components or CI/CD tasks with dependencies
(e.g., 'deploy_app' depends on 'build_image' and 'provision_database'),
determine the valid execution order, detect circular dependencies, and
group tasks into parallel execution stages."
"""

from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple


class CircularDependencyError(Exception):
    """Raised when a cycle is detected in the dependency graph."""
    pass


class TaskScheduler:
    """
    Direct Acyclic Graph (DAG) task scheduler using Kahn's Algorithm
    (in-degree approach).
    """

    def __init__(self):
        # adjacency list: task -> list of tasks that depend on it (dependents)
        self.dependents: Dict[str, List[str]] = defaultdict(list)
        # in-degree count: task -> number of prerequisites it still needs
        self.in_degree: Dict[str, int] = defaultdict(int)
        # all registered tasks
        self.all_tasks: Set[str] = set()

    def add_task(self, task_name: str, dependencies: List[str] = None) -> None:
        """
        Add a task and its prerequisites.
        `dependencies` are tasks that must finish BEFORE `task_name` can execute.
        """
        dependencies = dependencies or []
        self.all_tasks.add(task_name)
        if task_name not in self.in_degree:
            self.in_degree[task_name] = 0

        for dep in dependencies:
            self.all_tasks.add(dep)
            if dep not in self.in_degree:
                self.in_degree[dep] = 0

            self.dependents[dep].append(task_name)
            self.in_degree[task_name] += 1

    def resolve_execution_order(self) -> List[str]:
        """
        Returns a linear execution order of tasks respecting dependencies.
        Raises CircularDependencyError if a cycle is detected.
        """
        in_deg = dict(self.in_degree)
        queue = deque([task for task in self.all_tasks if in_deg[task] == 0])
        order: List[str] = []

        while queue:
            current = queue.popleft()
            order.append(current)

            for dependent in self.dependents[current]:
                in_deg[dependent] -= 1
                if in_deg[dependent] == 0:
                    queue.append(dependent)

        if len(order) != len(self.all_tasks):
            unresolved = [t for t in self.all_tasks if t not in order]
            raise CircularDependencyError(
                f"Circular dependency detected among tasks: {', '.join(unresolved)}"
            )

        return order

    def resolve_parallel_stages(self) -> List[List[str]]:
        """
        Returns tasks grouped by execution stages.
        All tasks in stage N can be run concurrently in parallel.
        Tasks in stage N+1 start only after stage N completes.
        """
        in_deg = dict(self.in_degree)
        queue = deque([task for task in self.all_tasks if in_deg[task] == 0])
        stages: List[List[str]] = []
        processed_count = 0

        while queue:
            # All tasks currently in the queue have in_degree == 0, so they can run concurrently
            stage_size = len(queue)
            current_stage: List[str] = []

            for _ in range(stage_size):
                task = queue.popleft()
                current_stage.append(task)
                processed_count += 1

                for dependent in self.dependents[task]:
                    in_deg[dependent] -= 1
                    if in_deg[dependent] == 0:
                        queue.append(dependent)

            stages.append(sorted(current_stage))

        if processed_count != len(self.all_tasks):
            unresolved = [t for t in self.all_tasks if in_deg[t] > 0]
            raise CircularDependencyError(
                f"Circular dependency detected: {', '.join(unresolved)}"
            )

        return stages

