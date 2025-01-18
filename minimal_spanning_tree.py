import heapq
from typing import List, Tuple, Dict, Set

Node = int
Edge = Tuple[Node, Node, float]
Graph = Dict[Node, List[Tuple[Node, float]]]

# Function 1: Prim's algorithm to find a Minimum Spanning Tree (MST)
def prim(graph: Graph, start_node: Node) -> List[Edge]:
    """
    Finds the Minimum Spanning Tree (MST) of a given graph using Prim's algorithm.

    :param graph: The input graph represented as an adjacency list.
    :param start_node: The starting node for the MST.
    :return: A list of edges representing the MST.
    """
    visited: Set[Node] = set()  # Tracks visited nodes
    mst: List[Edge] = []  # Stores the resulting MST edges
    edges_heap: List[Tuple[float, Node, Node]] = []  # Min-heap to prioritize edges by weight

    # Initialize heap with edges from the start node
    visited.add(start_node)
    for neighbor, weight in graph[start_node]:
        heapq.heappush(edges_heap, (weight, start_node, neighbor))

    # Continue until we visit all nodes or the heap is empty
    while edges_heap and len(visited) < len(graph):
        weight, u, v = heapq.heappop(edges_heap)
        if v not in visited:  # If the node is not visited, add it to the MST
            visited.add(v)
            mst.append((u, v, weight))
            # Add all edges of the new node to the heap
            for neighbor, weight in graph[v]:
                if neighbor not in visited:
                    heapq.heappush(edges_heap, (weight, v, neighbor))

    return mst

# Function 2: Update an existing MST with a new edge
def update_mst(mst: List[Edge], new_edge: Edge) -> List[Edge]:
    """
    Updates an existing Minimum Spanning Tree (MST) with a new edge.

    :param mst: The existing MST represented as a list of edges.
    :param new_edge: The new edge to be added (u, v, weight).
    :return: The updated MST as a list of edges.
    """
    u, v, weight = new_edge

    # Check if the new edge already exists in the MST
    if any((u, v, weight) == edge or (v, u, weight) == edge for edge in mst):
        return mst  # No update needed

    # Build a set of nodes in the current MST
    nodes = set()
    for edge in mst:
        nodes.update(edge[:2])

    if u in nodes and v in nodes:  # If adding the edge creates a cycle
        # Build a graph from the current MST
        graph: Graph = {node: [] for node in nodes}
        for edge in mst:
            x, y, w = edge
            graph[x].append((y, w))
            graph[y].append((x, w))

        # Find the cycle and the edge with the highest weight in the cycle
        def dfs(curr, target, visited, path):
            if curr == target:
                return True
            visited.add(curr)
            for neighbor, w in graph[curr]:
                if neighbor not in visited:
                    if dfs(neighbor, target, visited, path):
                        path.append((curr, neighbor, w))
                        return True
            return False

        path = []
        dfs(u, v, set(), path)
        max_edge = max(path, key=lambda edge: edge[2])

        # Replace the edge if the new edge has a smaller weight
        if weight < max_edge[2]:
            mst.remove(max_edge)
            mst.append(new_edge)
    else:  # If no cycle is formed, simply add the edge
        mst.append(new_edge)

    return mst

# Function 3: Main program
def main():
    """
    Main function to demonstrate graph creation, finding MST using Prim's algorithm,
    and updating the MST with new edges.
    """
    import random
    random.seed(42)  # For reproducible results

    # Generate a graph with at least 20 nodes and 50 edges
    num_nodes = 20
    num_edges = 50
    graph: Graph = {i: [] for i in range(num_nodes)}

    edges = set()
    while len(edges) < num_edges:
        u, v = random.sample(range(num_nodes), 2)
        weight = random.uniform(1, 10)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            graph[u].append((v, weight))
            graph[v].append((u, weight))

    # Print the generated graph
    print("Generated Graph (Adjacency List):")
    for node, neighbors in graph.items():
        print(f"{node}: {neighbors}")

    # Find the MST using Prim's algorithm
    mst = prim(graph, start_node=0)
    print("\nMinimum Spanning Tree (MST):")
    print(mst)

    # Validate MST
    assert len(mst) == num_nodes - 1, "MST should have n-1 edges."
    print("MST validation passed: Correct number of edges.")

    # Add a new edge that does not affect the MST
    new_edge = (0, 19, 15)  # High-weight edge
    print("\nAdding New Edge (No Effect):", new_edge)
    updated_mst = update_mst(mst, new_edge)
    assert mst == updated_mst, "MST should not change with a high-weight edge."
    print("MST validation passed: No change for high-weight edge.")

    # Add a new edge that affects the MST
    new_edge = (0, 19, 1)  # Low-weight edge
    print("\nAdding New Edge (Affects MST):", new_edge)
    print(f"Original MST weight: {sum(edge[2] for edge in mst)}")
    updated_mst = update_mst(mst, new_edge)
    print(f"Updated MST weight: {sum(edge[2] for edge in updated_mst)}")
    print("Edge replaced in MST:", set(map(tuple, mst)) - set(map(tuple, updated_mst)))
    print("Edge added to MST:", set(map(tuple, updated_mst)) - set(map(tuple, mst)))
    assert len(updated_mst) == num_nodes - 1, "Updated MST should still have n-1 edges."
    assert sum(edge[2] for edge in updated_mst) <= sum(edge[2] for edge in mst), \
        "Updated MST should not have a higher total weight."
    print("MST validation passed: Updated MST is correct.")

if __name__ == "__main__":
    main()
