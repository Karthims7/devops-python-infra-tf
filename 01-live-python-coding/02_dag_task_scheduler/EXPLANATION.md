# Live Coding Topic: DAG Task Scheduler & Topological Sort

## What the Interviewer Is Really Testing
1. **Graph Fundamentals:** Understanding Directed Acyclic Graphs (DAG), In-Degree vs Out-Degree.
2. **Kahn's Algorithm vs DFS:** Kahn's algorithm (queue of nodes with in-degree 0) is ideal for DevOps because it naturally yields **parallel execution stages** (breadth-first stage layering).
3. **Cycle Detection:** Knowing that if the output length != total tasks, a cycle exists.
4. **Clean Code & Data Structures:** Using `collections.defaultdict` and `collections.deque` instead of naive list operations ($O(1)$ popleft vs $O(N)$ list pop(0)).

## Time & Space Complexity
- **Time Complexity:** $O(V + E)$ where $V$ is number of tasks (vertices) and $E$ is number of dependency links (edges).
- **Space Complexity:** $O(V + E)$ to store the adjacency lists and in-degree mappings.

## Key Talking Points to Share During Interview
- *"In DevOps orchestration (like Terraform resource graphs or GitHub Actions job dependencies), we need to resolve dependencies before execution. I'll use Kahn's algorithm because it allows us to identify independent tasks that can be dispatched to worker pools concurrently in parallel stages."*
- *"We maintain an in-degree map. Any node with 0 in-degree is immediately ready to execute."*

