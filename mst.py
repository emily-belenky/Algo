from collections import defaultdict
import heapq

def prim_minimum_spanning_tree(nodes, edges):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((w, v))
        graph[v].append((w, u))

    mst = []  # List to store MST edges
    visited = set()
    min_heap = [(0, nodes[0], None)]  # (weight, current_node, previous_node)

    while min_heap:
        weight, current, prev = heapq.heappop(min_heap)
        if current in visited:
            continue
        visited.add(current)
        if prev is not None:
            mst.append((prev, current, weight))
        for next_weight, neighbor in graph[current]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (next_weight, neighbor, current))

    return mst

def update_mst(mst, new_edge, nodes):
    u, v, w = new_edge
    mst_graph = defaultdict(list)
    for a, b, weight in mst:
        mst_graph[a].append((b, weight))
        mst_graph[b].append((a, weight))

    def dfs(node, target, visited):
        if node == target:
            return []
        visited.add(node)
        for neighbor, weight in mst_graph[node]:
            if neighbor not in visited:
                path = dfs(neighbor, target, visited)
                if path is not None:
                    return [(node, neighbor, weight)] + path
        return None

    if dfs(u, v, set()) is None:
        mst.append((u, v, w))
        return mst

    path = dfs(u, v, set())
    max_edge = max(path, key=lambda edge: edge[2])
    if max_edge[2] > w:
        mst.remove(max_edge)
        mst.append((u, v, w))
    return mst
