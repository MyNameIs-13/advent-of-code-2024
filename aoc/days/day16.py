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

DIRECTIONS = {
    0: utils.STRAIGHT_DIRECTIONS['right'],
    1: utils.STRAIGHT_DIRECTIONS['down'],
    2: utils.STRAIGHT_DIRECTIONS['left'],
    3: utils.STRAIGHT_DIRECTIONS['up'],
}

DIRECTION_SYMBOLS = {
    0: '>',
    1: 'v',
    2: '<',
    3: '^',
}

Node = namedtuple('Node', ('p', 'd'))

def solve_part_a(input_data: str) -> str:
    grid, wall_coordinates_set, start_point, end_point = parse_input(input_data)
    graph = {}
    add_all_labyrinth_edges_to_graph(graph, grid, wall_coordinates_set, Node(start_point, 0))
    all_shortest_paths, cost = get_all_shortest_paths(graph, Node(start_point, 0), end_point)
    logger.debug(f'Found {len(all_shortest_paths)} shortest paths with cost {cost}')

    grid[Point(0, 0)] = f'\033[39m{grid[Point(0, 0)]}'  # Make first char default color
    for shortest_path in all_shortest_paths:  # Take the first path for visualization
        _grid = grid.copy()
        for node in shortest_path[1:-1]:
            _grid[node.p] = f'\033[31m{DIRECTION_SYMBOLS[node.d]}\033[39m'  # color path red
        logger.debug(_grid)
    return str(cost)


def solve_part_b(input_data: str) -> str:
    grid, wall_coordinates_set, start_point, end_point = parse_input(input_data)
    graph = {}
    add_all_labyrinth_edges_to_graph(graph, grid, wall_coordinates_set, Node(start_point, 0))
    all_shortest_paths, cost = get_all_shortest_paths(graph, Node(start_point, 0), end_point)
    logger.debug(f'Found {len(all_shortest_paths)} shortest paths with cost {cost}')

    visited_locations = {node.p for shortest_path in all_shortest_paths for node in shortest_path}
            
    return str(len(visited_locations))


def parse_input(input_data: str) -> tuple[utils.Grid, set, Point, Point]:
    grid = utils.Grid(input_data)
    wall_coordinates_set = set()
    start_point = None
    end_point = None
    for y, x, value in grid:
        current_coordinate = Point(y, x)
        if value == '#':
            wall_coordinates_set.add(current_coordinate)
        elif value == 'S':
            start_point = current_coordinate
        elif value == 'E':
            end_point = current_coordinate

    if not (start_point and end_point):
        raise ValueError('Start and end points not found')

    return grid, wall_coordinates_set, start_point, end_point


def add_all_labyrinth_edges_to_graph(graph: dict, grid: utils.Grid, wall_coordinates_set: set, start_node: Node) -> None:
    visited_nodes_set = set()
    nodes_to_visit = [start_node]

    while nodes_to_visit:
        current_node = nodes_to_visit.pop()
        if current_node in visited_nodes_set:
            continue
        visited_nodes_set.add(current_node)

        for _key, (dy, dx) in DIRECTIONS.items():
            neighbor_point = Point(current_node.p.y + dy, current_node.p.x + dx)
            if neighbor_point in wall_coordinates_set:
                continue
            if not grid.in_bounds(neighbor_point):
                continue
            weight_multiplicator = min(abs(_key - current_node.d), 4 - abs(_key - current_node.d))
            weight = 1 + (1000 * weight_multiplicator)
            neighbor_node = Node(neighbor_point, _key)
            add_edge(graph, current_node, neighbor_node, weight)
            nodes_to_visit.append(neighbor_node)
    return None


def add_edge(graph: dict, node1: Node, node2: Node, weight: int) -> None:
    graph.setdefault(node1, {})
    graph[node1][node2] = weight
    return None


def do_dijkstra(graph: dict, start_node: Node) -> tuple[dict, dict]:
    path_costs_for_each_node = {start_node: 0}
    predecessors: dict[Node, list[Node]] = {start_node: []}

    # Initialize a priority queue
    priority_queue = [(0, start_node)]
    heapify(priority_queue)

    while priority_queue:  # While the priority queue isn't empty
        current_weight, current_node = heappop(priority_queue)

        # If we've found a shorter path already, skip
        if current_weight > path_costs_for_each_node.get(current_node, float('inf')):
            continue

        if current_node not in graph:
            continue

        for neighbor_node, weight in graph.get(current_node, {}).items():
            # Calculate the distance from current_node to the neighbor
            tentative_cost = current_weight + weight

            if tentative_cost < path_costs_for_each_node.get(neighbor_node, float('inf')):
                path_costs_for_each_node[neighbor_node] = tentative_cost
                predecessors[neighbor_node] = [current_node]
                heappush(priority_queue, (tentative_cost, neighbor_node))
            elif tentative_cost == path_costs_for_each_node.get(neighbor_node, float('inf')):
                predecessors.setdefault(neighbor_node, []).append(current_node)

    return path_costs_for_each_node, predecessors


def get_all_shortest_paths(graph: dict, start_node: Node, end_point: Point) -> tuple[list[list[Node]], int | None]:
    # Generate the predecessors dict
    path_costs_for_each_node, predecessors = do_dijkstra(graph, start_node)

    end_nodes_to_cost_dict = {node: cost for node, cost in path_costs_for_each_node.items() if node.p == end_point}
    if not end_nodes_to_cost_dict or min(end_nodes_to_cost_dict.values()) == float('inf'):
        return [], None  # No path found

    lowest_cost = min(end_nodes_to_cost_dict.values())
    end_nodes = [node for node, cost in end_nodes_to_cost_dict.items() if cost == lowest_cost]

    all_paths = []

    for end_node in end_nodes:
        backtrack([end_node], all_paths, start_node, predecessors)

    return all_paths, lowest_cost
    

def backtrack(current_path: list, all_paths: list, start_node: Node, predecessors: dict):
    last_node = current_path[0]
    if last_node == start_node:
        all_paths.append(current_path)
        return

    if last_node not in predecessors:
        return

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
