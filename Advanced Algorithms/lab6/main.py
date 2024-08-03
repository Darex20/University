from typing import Tuple
import numpy as np


# infinite value
INF = 10 ** 6 - 1


def wfi(weight_matrix: np.ndarray, start: int, end: int) -> Tuple[np.ndarray, list]:
    """
    Implementation of the WFI algorithm with recreation of the route between two edges.
    Args:
        weight_matrix (np.ndarray): Weight matrix representation of the graph.
        start (int): Starting node in the route.
        end (int): Ending node in the route.
    Returns:
        np.ndarray: Distance matrix of the WFI algorithm.
        list: List of nodes on the route between starting and ending node including starting
            and ending node.
    """
    distance = weight_matrix
    next = np.full_like(weight_matrix, -1) #init all values to -1

    #TODO: Implement the rest of the function.

    #initialize the next matrix - assign value where the distance is not inf
    for i in range(len(weight_matrix)):
        for j in range(len(weight_matrix)):
            if i != j and weight_matrix[i][j] < INF:
                next[i][j] = j
    
    #WFI algorithm implementation with the next array update
    for k in range(len(weight_matrix)):
        for i in range(len(weight_matrix)):
            for j in range(len(weight_matrix)):
                if distance[i][k] + distance[k][j] < distance[i][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]
                    next[i][j] = next[i][k]

    #reconstruct the shortest path from start to end - create a list named path
    path = []
    if next[start][end] != -1:
        i = start
        while i != end:
            path.append(i)
            i = next[i][end]
        path.append(end)

    return distance, path

# Testiranje
W = np.array([[0, 2, INF, INF],
              [INF, 0, 3, -1],
              [-1, INF, 0, 7],
              [3, INF, INF, 0]])

distance, path = wfi(W, 0, 3)

print("Distance matrix:")
print(distance)
print("Path:", path)