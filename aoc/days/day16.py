#!/usr/bin/env python3
import logging
from collections import namedtuple
from heapq import heapify, heappop, heappush

from aocd.models import Puzzle

from shared import utils
from shared.logger import logger
from shared.utils import Point

logger.setLevel(logging.INFO)
EXAMPLE_DATA = False
SUBMIT = True

# HACK: Overwrites
# SUBMIT = False
# logger.setLevel(logging.DEBUG)
# EXAMPLE_DATA = True

# Maps integer directions to Point objects representing movement vectors (dy, dx).
DIRECTIONS = {
    0: utils.STRAIGHT_DIRECTIONS['right'],
    1: utils.STRAIGHT_DIRECTIONS['down'],
    2: utils.STRAIGHT_DIRECTIONS['left'],
    3: utils.STRAIGHT_DIRECTIONS['up'],
}

# Maps integer directions to character symbols for visualizing paths.
DIRECTION_SYMBOLS = {
    0: '>',
    1: 'v',
    2: '<',
    3: '^',
}

# Represents a node in the graph, consisting of a Point (p) for its grid coordinates
# and an integer direction (d) indicating the direction of arrival at this point.
Node = namedtuple('Node', ('p', 'd'))

def solve_part_a(input_data: str) -> str:
    grid, wall_coordinates_set, start_point, end_point = parse_input(input_data)
    graph = {}
    add_all_labyrinth_edges_to_graph(graph, wall_coordinates_set, Node(start_point, 0))
    all_shortest_paths, cost = get_all_shortest_paths(graph, Node(start_point, 0), end_point)
    logger.debug(f'Found {len(all_shortest_paths)} shortest paths with cost {cost}')

    # Optional: Visualize the shortest paths found for debugging or demonstration.
    grid[Point(0, 0)] = f'\033[39m{grid[Point(0, 0)]}'  # Reset color for the first char
    for _shortest_path in all_shortest_paths: # Ensure there is at least one path
        _grid = grid.copy()
        # Mark the path nodes with their direction symbols, colored red.
        for node in _shortest_path[1:-1]: # Exclude start and end for clear visualization
            _grid[node.p] = f'\033[31m{DIRECTION_SYMBOLS[node.d]}\033[39m'  # color path red
        logger.debug(_grid) # Log the colored grid
    return str(cost)


def solve_part_b(input_data: str) -> str:
    grid, wall_coordinates_set, start_point, end_point = parse_input(input_data)
    graph = {}
    add_all_labyrinth_edges_to_graph(graph, wall_coordinates_set, Node(start_point, 0))
    all_shortest_paths, cost = get_all_shortest_paths(graph, Node(start_point, 0), end_point)
    logger.debug(f'Found {len(all_shortest_paths)} shortest paths with cost {cost}')

    # Collect all unique Point objects (grid locations) from all nodes in all shortest paths.
    visited_locations = {node.p for shortest_path in all_shortest_paths for node in shortest_path}
            
    return str(len(visited_locations))


def parse_input(input_data: str) -> tuple[utils.Grid, set, Point, Point]:
    """
    Parses the raw input string into a grid, identifying wall locations ('#'),
    the start point ('S'), and the end point ('E').

    Args:
        input_data: The raw input string from the puzzle.

    Returns:
        A tuple containing:
            - grid: A utils.Grid object representing the entire puzzle area.
            - wall_coordinates_set: A set of Point objects corresponding to wall cells.
            - start_point: A Point object for the 'S' location.
            - end_point: A Point object for the 'E' location.

    Raises:
        ValueError: If either the start or end point is not found in the input.
    """
    grid = utils.Grid(input_data)
    wall_coordinates_set = set()
    start_point = None
    end_point = None
    # Iterate through each cell in the grid to identify special locations.
    for p, value in grid:
        current_coordinate = p
        if value == '#':
            wall_coordinates_set.add(current_coordinate)
        elif value == 'S':
            start_point = current_coordinate
        elif value == 'E':
            end_point = current_coordinate

    # Ensure both start and end points were found.
    if not (start_point and end_point):
        raise ValueError('Start and end points not found')

    return grid, wall_coordinates_set, start_point, end_point


def add_all_labyrinth_edges_to_graph(graph: dict, wall_coordinates_set: set, start_node: Node) -> None:
    """
    Constructs a directed graph where each node is a (Point, Direction) pair.
    Edges are added for valid movements, and their weights are calculated based on
    whether the movement changes direction. This effectively performs a BFS/DFS
    to discover all reachable (point, direction) states and their connections.

    Args:
        graph: The dictionary representing the adjacency list of the graph.
               It will be populated in the format: {Node: {Neighbor_Node: weight}}.
        wall_coordinates_set: A set of Point objects marking impassable walls.
        start_node: The initial node (Point, Direction) from which to begin
                    exploring and building the graph.
    """
    visited_nodes_set = set()
    nodes_to_visit = [start_node] # Using a list as a stack for a DFS-like exploration

    while nodes_to_visit:
        current_node = nodes_to_visit.pop()
        # If this node has already been fully processed, skip it.
        if current_node in visited_nodes_set:
            continue
        visited_nodes_set.add(current_node)

        # Explore all four possible cardinal directions from the current point.
        for _key, p in DIRECTIONS.items(): # _key is the integer representation of the neighbor's direction
            neighbor_point = current_node.p + p
            
            # Skip if the neighbor point is a wall or outside the grid boundaries.
            if neighbor_point in wall_coordinates_set:
                continue
            
            # Calculate the weight for the edge. Movement costs 1, plus a penalty
            # for changing direction. The penalty is 1000 per 90-degree turn.
            # `_key` is the direction of movement to the neighbor, `current_node.d`
            # is the direction from which `current_node` was approached.
            # `min(abs(_key - current_node.d), 4 - abs(_key - current_node.d))`
            # calculates the minimum angular difference (e.g., 0 for straight,
            # 1 for 90 degrees, 2 for 180 degrees).
            weight_multiplicator = min(abs(_key - current_node.d), 4 - abs(_key - current_node.d))
            weight = 1 + (1000 * weight_multiplicator)
            
            neighbor_node = Node(neighbor_point, _key)
            add_edge(graph, current_node, neighbor_node, weight)
            # Add the neighbor node to the list to be visited, ensuring all reachable
            # (point, direction) states are processed.
            nodes_to_visit.append(neighbor_node)
    return None


def add_edge(graph: dict, node1: Node, node2: Node, weight: int) -> None:
    """
    Adds a directed edge from `node1` to `node2` with a specified `weight`
    to the given graph. If `node1` is not yet in the graph, it is initialized.

    Args:
        graph: The graph dictionary (adjacency list).
        node1: The source Node.
        node2: The destination Node.
        weight: The cost associated with traversing this edge.
    """
    graph.setdefault(node1, {}) # Ensure node1 has an entry in the graph
    graph[node1][node2] = weight # Add/update the edge to node2 with its weight
    return None


def do_dijkstra(graph: dict, start_node: Node) -> tuple[dict, dict]:
    """
    Executes Dijkstra's algorithm to find the shortest paths (and their costs)
    from a `start_node` to all other reachable nodes in a graph.
    It also records all predecessors for each node, allowing for reconstruction
    of multiple shortest paths if they exist.

    Args:
        graph: The adjacency list representation of the graph.
               {Node: {Neighbor_Node: weight}}.
        start_node: The starting node (Point, Direction) for Dijkstra's algorithm.

    Returns:
        A tuple containing:
            - path_costs_for_each_node: A dictionary mapping each Node to its
                                        minimum accumulated cost from `start_node`.
            - predecessors: A dictionary mapping each Node to a list of its
                            predecessor Nodes on *all* shortest paths.
    """
    # Initialize costs: 0 for start_node, infinity for all others implicitly.
    path_costs_for_each_node = {start_node: 0}
    # Initialize predecessors: empty list for start_node.
    predecessors: dict[Node, list[Node]] = {start_node: []}

    # Initialize a min-priority queue with the start node and its cost.
    # The heap stores tuples of (cost, node).
    priority_queue = [(0, start_node)]
    heapify(priority_queue)

    while priority_queue:  # Continue as long as there are nodes to process
        current_weight, current_node = heappop(priority_queue)

        # If we've already found a shorter path to `current_node`, skip this (stale) entry.
        if current_weight > path_costs_for_each_node.get(current_node, float('inf')):
            continue

        # If the current node has no outgoing edges, it's a dead end in the graph, skip.
        if current_node not in graph:
            continue

        # Explore all neighbors of the current node.
        for neighbor_node, weight in graph.get(current_node, {}).items():
            # Calculate the total cost to reach the `neighbor_node` through `current_node`.
            tentative_cost = current_weight + weight

            # If this path offers a shorter cost to `neighbor_node` than previously known:
            if tentative_cost < path_costs_for_each_node.get(neighbor_node, float('inf')):
                path_costs_for_each_node[neighbor_node] = tentative_cost # Update the shortest cost
                predecessors[neighbor_node] = [current_node] # This is now the *only* known predecessor for this shortest path
                heappush(priority_queue, (tentative_cost, neighbor_node)) # Add neighbor to priority queue
            # If this path offers an equally short cost:
            elif tentative_cost == path_costs_for_each_node.get(neighbor_node, float('inf')):
                predecessors.setdefault(neighbor_node, []).append(current_node) # Add current_node as an alternative predecessor

    return path_costs_for_each_node, predecessors


def get_all_shortest_paths(graph: dict, start_node: Node, end_point: Point) -> tuple[list[list[Node]], int | None]:
    """
    Finds all shortest paths from the `start_node` to any graph node whose
    Point component matches the `end_point` in the grid. It leverages
    Dijkstra's algorithm and a backtracking step.

    Args:
        graph: The graph (adjacency list) containing all (Point, Direction) nodes.
        start_node: The initial node (Point and initial direction).
        end_point: The target Point (destination grid location).

    Returns:
        A tuple containing:
            - all_paths: A list of lists, where each inner list represents one
                         shortest path as a sequence of Nodes.
            - lowest_cost: The minimum numerical cost to reach the `end_point`,
                           or `None` if no path exists.
    """
    # First, run Dijkstra's to get the shortest path costs to all nodes
    # and a record of all predecessors that lead to those shortest paths.
    path_costs_for_each_node, predecessors = do_dijkstra(graph, start_node)

    # Filter for all nodes that are at the `end_point` location and map them to their costs.
    end_nodes_to_cost_dict = {node: cost for node, cost in path_costs_for_each_node.items() if node.p == end_point}
    # If no paths were found to the end_point, or the lowest cost is still infinity, return empty.
    if not end_nodes_to_cost_dict or min(end_nodes_to_cost_dict.values()) == float('inf'):
        return [], None  # No path found

    lowest_cost = min(end_nodes_to_cost_dict.values())
    # Identify all specific (Point, Direction) end nodes that achieve this `lowest_cost`.
    # There might be multiple such nodes if arriving at the end_point from different
    # directions results in the same minimum total cost.
    end_nodes = [node for node, cost in end_nodes_to_cost_dict.items() if cost == lowest_cost]

    all_paths = []

    # For each identified `end_node`, reconstruct all paths back to the `start_node`.
    for end_node in end_nodes:
        backtrack([end_node], all_paths, start_node, predecessors)

    return all_paths, lowest_cost
    

def backtrack(current_path: list, all_paths: list, start_node: Node, predecessors: dict):
    """
    Recursively reconstructs all shortest paths from an `end_node` back to the
    `start_node` using the `predecessors` dictionary generated by Dijkstra's algorithm.

    Args:
        current_path: The path being built during the current recursive call.
                      It starts with the `end_node` and grows backward.
        all_paths: A list that accumulates all fully reconstructed shortest paths.
        start_node: The designated starting node of the overall path.
        predecessors: The dictionary mapping nodes to a list of their predecessors
                      on shortest paths, as returned by `do_dijkstra`.
    """
    last_node = current_path[0] # The most recently added node to the current_path (which is the farthest from start)
    if last_node == start_node:
        all_paths.append(current_path) # Base case: If we reached the start node, a full path is found.
        return

    if last_node not in predecessors: # Safety check: If a node has no predecessors, it's an isolated part or error.
        return

    # For each predecessor of the `last_node`, recursively call backtrack to extend the path.
    for predecessor in predecessors[last_node]:
        backtrack([predecessor] + current_path, all_paths, start_node, predecessors)
    

def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 16
    logger.info('🎄 Running puzzle day 16...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)

    return None

if __name__ == '__main__':
    main()
