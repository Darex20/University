from statistics import median
from typing import Tuple, List
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

class Node:
    def __init__(self, point: Point, med: float) -> None:
        self.point = point
        self.med = med

    def __repr__(self):
        return f'Node{self.point, self.med}'

INF = float('inf')
INF_POINT = Point(-INF, -INF)
INF_NODE = Node(INF_POINT, -INF)

def from_points_help(result: List[Node], points: List[Point], start_index: int = 0) -> List[Node]:
    if not points:
        return result
    first_point = points.pop(0)
    node = Node(first_point, first_point.x)
    n_nodes = len(result)
    for _ in range(start_index - n_nodes + 1):
        result.append(INF_NODE)
    result[start_index] = node
    if points:
        med = median(map(lambda point: point.x, points))
        node.med = med
        points_left = list(filter(lambda point: point.x <= med, points))
        points_right = list(filter(lambda point: point.x > med, points))
        result = from_points_help(result, points_left, start_index=2 * start_index + 1)
        result = from_points_help(result, points_right, start_index=2 * start_index + 2)
    return result

def from_points(points: List[Point]) -> List[Node]:
    if not points:
        return []
    points = list(sorted(points, key=lambda point: -point.y))
    result = []
    return from_points_help(result, points, 0)

def get_node(tree: List[Node], index: int) -> Node:
    if index >= len(tree):
        return INF_NODE
    return tree[index]

def query_priority_subtree(tree: List[Node], index: int, limit_value: float) -> List[Point]:
    result = []
    node = get_node(tree, index)
    if node.point.y >= limit_value:  # Updated condition to check if the point is within the limit
        result.append(node.point)
        result += query_priority_subtree(tree, 2 * index + 1, limit_value)
        result += query_priority_subtree(tree, 2 * index + 2, limit_value)
    return result

def query(tree: List[Node], interval: Tuple[float, float], limit: float) -> List[Point]:
    if not tree:
        return []
    result = []
    index = 0    
    node = get_node(tree, index)
    if node.point.y >= limit and interval[0] <= node.point.x <= interval[1]:  # Include the root node if its y-value is within the Y limit and x-value is within the interval
        result.append(node.point)

    while node is not None and node is not INF_NODE and \
        (interval[0] > node.med or interval[1] < node.med) and node.med <= interval[1]:
        point = node.point
        if point.y >= limit:  # Include the point if it's within the Y limit
            result.append(point)
    
        if interval[1] < node.med:
            index = 2 * index + 1  # Move to the left subtree
        else:
            index = 2 * index + 2  # Move to the right subtree
        node = get_node(tree, index)
    
    if node is None or node is INF_NODE:
        return result
    
    point = node.point
    if point.y >= limit:  # Include the point if it's within the Y limit
        result.append(point)

    node_index = index
    index = 2 * node_index + 1
    node = get_node(tree, index)
    while node is not None and node is not INF_NODE:
        point = node.point
        if point.x <= interval[1] and point.x >= interval[0] and point.y >= limit:  # Include the point if it's within the query interval and Y limit
            result.append(point)
        if point.x > interval[0]:
            result += query_priority_subtree(tree, 2 * index + 2, limit)  # Query right subtree
        index = 2 * index + 1  # Move to the left subtree
        node = get_node(tree, index)
    
    index = 2 * node_index + 2
    node = get_node(tree, index)
    while node is not None and node is not INF_NODE:
        point = node.point
        if point.x <= interval[1] and point.x >= interval[0] and point.y >= limit:  # Include the point if it's within the query interval and Y limit
            result.append(point)
        if point.x < interval[1]:
            result += query_priority_subtree(tree, 2 * index + 1, limit)  # Query left subtree
        index = 2 * index + 2  # Move to the right subtree
        node = get_node(tree, index)
    return result


TEST_POINTS = [Point(-5.5, -5.0),
               Point(6.5, 2.0),
               Point(-3.5, 2.5),
               Point(4.5, 1.0),
               Point(2.0, -2.0),
               Point(-1.0, 4.0),
               Point(2.5, 0.5),
               Point(-0.5, -0.5),
               Point(1.0, 1.0),
               Point(-2.0, -2.5),
               Point(3.0, 4.0),
               Point(7.0, 0.0),
               Point(-4.5, -1.0),
               Point(3.5, -1.5),
               Point(5.5, -3.0),
               Point(3.5, 2.5),
               Point(6.0, 5.0),
               Point(-3.0, 0.0)]

tree = from_points(TEST_POINTS)
result = query(tree, (-1.5, 5.0), -1.75)
expected = [Point(x=-1.0, y=4.0), Point(x=1.0, y=1.0), Point(x=-0.5, y=-0.5), Point(x=3.0, y=4.0), Point(x=3.5, y=2.5), Point(x=2.5, y=0.5), Point(x=3.5, y=-1.5), Point(x=4.5, y=1.0)]
print("Actual result:", sorted(result))
print("Expected result:", sorted(expected))
assert sorted(result) == sorted(expected)

