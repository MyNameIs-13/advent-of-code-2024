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
    all_shortest_paths, cost = utils.Graph.get_shortest_paths(graph, start_point, end_point)
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
        all_shortest_paths, cost = utils.Graph.get_shortest_paths(graph, start_point, end_point)
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
            utils.Graph.add_edge(graph, current_point, neighbor_point, weight)
            points_to_visit.append(neighbor_point)
    return None


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
