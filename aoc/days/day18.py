#!/usr/bin/env python3
import logging
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

def solve_part_a(input_data: str) -> str:
    start_point = Point(0, 0)
    row_col_length = 6 if EXAMPLE_DATA else 70
    end_point = Point(row_col_length, row_col_length)
    grid_string = '\n'.join(['.' * (row_col_length+1) for _ in range(row_col_length+1)])
    grid = utils.Grid(grid_string)
    corrupted_points_set = fill_grid_with_corruptions(input_data, grid, 12 if EXAMPLE_DATA else 1024)
    graph = {}
    add_all_edges_to_graph(graph, grid, start_point, corrupted_points_set)
    logger.debug(f'Graph has {len(graph)} points')
    all_shortest_paths, cost = get_all_shortest_paths(graph, start_point, end_point)
    logger.debug(f'Found {len(all_shortest_paths)} shortest paths with cost {cost}')

    # grid[Point(0, 0)] = f'\033[39m{grid[Point(0, 0)]}'  # Reset color for the first char
    for _shortest_path in all_shortest_paths: # Ensure there is at least one path
        _grid = grid.copy()
        for p in _shortest_path: # Exclude start and end for clear visualization
            _grid[p] = '\033[31mO\033[39m'  # color path red
        logger.debug(_grid) # Log the colored grid
    return str(cost)


def solve_part_b(input_data: str) -> str:
    # TODO: that is neither fast nor pretty
    start_point = Point(0, 0)
    row_col_length = 6 if EXAMPLE_DATA else 70
    end_point = Point(row_col_length, row_col_length)
    grid_string = '\n'.join(['.' * (row_col_length+1) for _ in range(row_col_length+1)])
    corruptions = 12 if EXAMPLE_DATA else 1024
    grid = utils.Grid(grid_string)
    corrupted_points_set = fill_grid_with_corruptions(input_data, grid, corruptions)
    for i, line in enumerate(input_data.split('\n')):
        if i < corruptions:
            continue
        x, y = line.split(',')
        p = Point(int(y), int(x))
        corrupted_points_set.add(p)
        graph = {}
        add_all_edges_to_graph(graph, grid, start_point, corrupted_points_set)
        all_shortest_paths, cost = get_all_shortest_paths(graph, start_point, end_point)
        if not all_shortest_paths:
            return str(f'{x},{y}')

    return str('Not solved')


def fill_grid_with_corruptions(input_data: str, grid: utils.Grid, corruptions: int) -> set:
    corrupted_points_set = set()
    for i, line in enumerate(input_data.split('\n')):
        if i == corruptions:
            break
        x, y = line.split(',')
        p = Point(int(y), int(x))
        corrupted_points_set.add(p)
        grid[p] = '#'
    logger.debug(grid)
    return corrupted_points_set


def add_all_edges_to_graph(graph: dict, grid: utils.Grid, start_point: Point, corrupted_points_set: set) -> None:
    visited_points_set = set()
    points_to_visit = [start_point]

    while points_to_visit:
        current_point = points_to_visit.pop()
        if current_point in visited_points_set:
            continue
        visited_points_set.add(current_point)
        
        for neighbor_point in grid.get_neighbors(current_point):
            if neighbor_point in corrupted_points_set:
                continue            
            weight = 1            
            add_edge(graph, current_point, neighbor_point, weight)
            points_to_visit.append(neighbor_point)
    return None


def add_edge(graph: dict, point1: Point, point2: Point, weight: int) -> None:
    graph.setdefault(point1, {}) # Ensure point1 has an entry in the graph
    graph[point1][point2] = weight # Add/update the edge to point2 with its weight
    return None


def do_dijkstra(graph: dict, start_point: Point) -> tuple[dict, dict]:
    """
    Executes Dijkstra's algorithm to find the shortest paths (and their costs)
    from a `start_point` to all other reachable points in a graph.
    It also records all predecessors for each point, allowing for reconstruction
    of multiple shortest paths if they exist.

    Args:
        graph: The adjacency list representation of the graph.
               {point: {Neighbor_point: weight}}.
        start_point: The starting point (Point, Direction) for Dijkstra's algorithm.

    Returns:
        A tuple containing:
            - path_costs_for_each_point: A dictionary mapping each point to its
                                        minimum accumulated cost from `start_point`.
            - predecessors: A dictionary mapping each point to a list of its
                            predecessor points on *all* shortest paths.
    """
    # Initialize costs: 0 for start_point, infinity for all others implicitly.
    path_costs_for_each_point = {start_point: 0}
    # Initialize predecessors: empty list for start_point.
    predecessors: dict[Point, list[Point]] = {start_point: []}

    # Initialize a min-priority queue with the start point and its cost.
    # The heap stores tuples of (cost, point).
    priority_queue = [(0, start_point)]
    heapify(priority_queue)

    while priority_queue:  # Continue as long as there are points to process
        current_weight, current_point = heappop(priority_queue)

        # If we've already found a shorter path to `current_point`, skip this (stale) entry.
        if current_weight > path_costs_for_each_point.get(current_point, float('inf')):
            continue

        # If the current point has no outgoing edges, it's a dead end in the graph, skip.
        if current_point not in graph:
            continue

        # Explore all neighbors of the current point.
        for neighbor_point, weight in graph.get(current_point, {}).items():
            # Calculate the total cost to reach the `neighbor_point` through `current_point`.
            tentative_cost = current_weight + weight

            # If this path offers a shorter cost to `neighbor_point` than previously known:
            if tentative_cost < path_costs_for_each_point.get(neighbor_point, float('inf')):
                path_costs_for_each_point[neighbor_point] = tentative_cost # Update the shortest cost
                predecessors[neighbor_point] = [current_point] # This is now the *only* known predecessor for this shortest path
                heappush(priority_queue, (tentative_cost, neighbor_point)) # Add neighbor to priority queue
            # # If this path offers an equally short cost:
            # elif tentative_cost == path_costs_for_each_point.get(neighbor_point, float('inf')):
            #     predecessors.setdefault(neighbor_point, []).append(current_point) # Add current_point as an alternative predecessor

    logger.debug('dijkstra done')
    return path_costs_for_each_point, predecessors


def get_all_shortest_paths(graph: dict, start_point: Point, end_point: Point) -> tuple[list[list[Point]], int | None]:
    """
    Finds all shortest paths from the `start_point` to any graph point whose
    Point component matches the `end_point` in the grid. It leverages
    Dijkstra's algorithm and a backtracking step.

    Args:
        graph: The graph (adjacency list) containing all (Point, Direction) points.
        start_point: The initial point (Point and initial direction).
        end_point: The target Point (destination grid location).

    Returns:
        A tuple containing:
            - all_paths: A list of lists, where each inner list represents one
                         shortest path as a sequence of points.
            - lowest_cost: The minimum numerical cost to reach the `end_point`,
                           or `None` if no path exists.
    """
    # First, run Dijkstra's to get the shortest path costs to all points
    # and a record of all predecessors that lead to those shortest paths.
    path_costs_for_each_point, predecessors = do_dijkstra(graph, start_point)

    # Filter for all points that are at the `end_point` location and map them to their costs.
    end_points_to_cost_dict = {point: cost for point, cost in path_costs_for_each_point.items() if point == end_point}
    # If no paths were found to the end_point, or the lowest cost is still infinity, return empty.
    if not end_points_to_cost_dict or min(end_points_to_cost_dict.values()) == float('inf'):
        return [], None  # No path found

    lowest_cost = min(end_points_to_cost_dict.values())
    # Identify all specific (Point, Direction) end points that achieve this `lowest_cost`.
    # There might be multiple such points if arriving at the end_point from different
    # directions results in the same minimum total cost.
    end_points = [point for point, cost in end_points_to_cost_dict.items() if cost == lowest_cost]

    all_paths = []

    # For each identified `end_point`, reconstruct all paths back to the `start_point`.
    for end_point in end_points:
        backtrack([end_point], all_paths, start_point, predecessors)

    return all_paths, lowest_cost
    

def backtrack(current_path: list, all_paths: list, start_point: Point, predecessors: dict):
    """
    Recursively reconstructs all shortest paths from an `end_point` back to the
    `start_point` using the `predecessors` dictionary generated by Dijkstra's algorithm.

    Args:
        current_path: The path being built during the current recursive call.
                      It starts with the `end_point` and grows backward.
        all_paths: A list that accumulates all fully reconstructed shortest paths.
        start_point: The designated starting point of the overall path.
        predecessors: The dictionary mapping points to a list of their predecessors
                      on shortest paths, as returned by `do_dijkstra`.
    """
    last_point = current_path[0] # The most recently added point to the current_path (which is the farthest from start)
    if last_point == start_point:
        all_paths.append(current_path) # Base case: If we reached the start point, a full path is found.
        return

    if last_point not in predecessors: # Safety check: If a point has no predecessors, it's an isolated part or error.
        return

    # For each predecessor of the `last_point`, recursively call backtrack to extend the path.
    for predecessor in predecessors[last_point]:
        backtrack([predecessor] + current_path, all_paths, start_point, predecessors)
    

def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 18
    logger.info('🎄 Running puzzle day 18...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)

    return None

if __name__ == '__main__':
    main()
