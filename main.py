from mst import prim_minimum_spanning_tree, update_mst

def main():
    nodes = list(range(20))
    edges = [
        (0, 1, 4), (0, 2, 1), (0, 3, 7), (1, 2, 2), (1, 4, 3),
        (2, 3, 6), (2, 5, 8), (3, 6, 5), (4, 5, 9), (4, 7, 4),
        (5, 8, 3), (6, 9, 7), (7, 8, 2), (7, 10, 1), (8, 11, 6),
        (9, 12, 4), (10, 13, 5), (11, 14, 8), (12, 15, 3), (13, 16, 7),
        (14, 17, 9), (15, 18, 4), (16, 19, 3), (17, 18, 2), (18, 19, 1),
        (1, 6, 5), (3, 8, 4), (5, 10, 6), (7, 14, 5), (9, 16, 7)
    ]

    print("Original Graph:")
    for edge in edges:
        print(edge)

    mst = prim_minimum_spanning_tree(nodes, edges)
    print("\nInitial Minimum Spanning Tree:")
    for edge in mst:
        print(edge)

    new_edge = (0, 4, 10)
    print("\nAdding new edge (does not affect MST):", new_edge)
    mst = update_mst(mst, new_edge, nodes)
    print("Updated MST:")
    for edge in mst:
        print(edge)

    new_edge = (0, 4, 1)
    print("\nAdding new edge (affects MST):", new_edge)
    mst = update_mst(mst, new_edge, nodes)
    print("Updated MST:")
    for edge in mst:
        print(edge)

if __name__ == "__main__":
    main()
