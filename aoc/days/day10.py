#!/usr/bin/env python3
from functools import total_ordering

from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # overwrite
SUBMIT = True
# SUBMIT = False  # overwrite

DIRECTIONS = ['up', 'down', 'left', 'right']

def __find_all_trailheads(grid: list) -> set:
    rows = len(grid)
    cols = len(grid[0])
    trailhead_set = set()
    for y in range(rows):
        for x in range(cols):
            grid[y][x] = int(grid[y][x])
            if grid[y][x] == 0:
                trailhead_set.add((y, x))
                logger.debug(f'start_location: {(y, x)}')
    return trailhead_set


def __reach_summit_and_count_summits(start_y: int, start_x: int, grid: list, different_summits: set) -> None:
    """
    reach the summit and count how many different summits have been reached (same summit with different paths does not count
    """
    if grid[start_y][start_x] == 9:
        logger.debug(f'reached summit {(start_y, start_x)}')
        different_summits.add((start_y, start_x))
    else:
        for direction in DIRECTIONS:
            new_y, new_x = start_y + utils.DIRECTIONS[direction][0], start_x + utils.DIRECTIONS[direction][1]
            if utils.in_bounds(new_y, new_x, grid) and grid[start_y][start_x] + 1 == grid[new_y][new_x]:
                __reach_summit_and_count_summits(new_y, new_x, grid, different_summits)
    return None


def __reach_summit_and_count_paths(start_y: int, start_x: int, grid: list, different_paths: list, path: set = None) -> None:
    """
    reach the summit(s) and count with how many paths the summit(s) can be reached
    """
    # Not sure if this really works of I just had luck with the input data. (there is no check that the same path has been added twice to the paths
    if path is None:
        path = set()
    path.add((start_y, start_x))

    if grid[start_y][start_x] == 9:
        logger.debug(f'reached summit {(start_y, start_x)}')
        different_paths.append(path)
    else:
        for direction in DIRECTIONS:
            new_y, new_x = start_y + utils.DIRECTIONS[direction][0], start_x + utils.DIRECTIONS[direction][1]
            if utils.in_bounds(new_y, new_x, grid) and grid[start_y][start_x] + 1 == grid[new_y][new_x]:
                __reach_summit_and_count_paths(new_y, new_x, grid, different_paths, path=path)
    return None


def solve_part_a(input_data: str) -> str:
    grid = utils.get_grid(input_data)
    trailhead_set = __find_all_trailheads(grid)
    total_summits = 0
    for trailhead in trailhead_set:
        different_summits = set()
        __reach_summit_and_count_summits(trailhead[0], trailhead[1], grid, different_summits)
        total_summits += len(different_summits)
    return str(total_summits)


def solve_part_b(input_data: str) -> str:
    grid = utils.get_grid(input_data)
    trailhead_set = __find_all_trailheads(grid)
    scores = 0
    for trailhead in trailhead_set:
        different_paths = []
        __reach_summit_and_count_paths(trailhead[0], trailhead[1], grid, different_paths)
        scores += len(different_paths)
    return str(scores)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 10
    logger.info(f'🎄 Running puzzle day 10...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)

    return None

if __name__ == '__main__':
    main()