#!/usr/bin/env python3
from typing import Tuple

from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # comment out to use real data

CHANGE_DIRECTION = {
    'up': 'right',
    'right': 'down',
    'down': 'left',
    'left': 'up'
}


def __in_bound(y: int, x: int, grid: list) -> bool:
    rows = len(grid)
    cols = len(grid[0])
    if  0 <= y < rows and 0 <= x < cols:
        return True
    return False


def __get_next_position(y: int, x: int, direction: str, grid: list) -> Tuple[int, int, str]:
    next_y = y + utils.DIRECTIONS[direction][0]
    next_x = x + utils.DIRECTIONS[direction][1]
    if __in_bound(next_y, next_x, grid):
        if grid[next_y][next_x] == '#':
            direction = CHANGE_DIRECTION[direction]
            next_y = y
            next_x = x
    else:
        next_y, next_x, direction = None, None, None
    return next_y, next_x, direction


def __get_start_location(grid: list) -> Tuple[int, int, str]:
    rows = len(grid)
    cols = len(grid[0])
    for y in range(rows):
        for x in range(cols):
            c = grid[y][x]
            if c == '^':
                logger.debug(f'{y}, {x}, up')
                return y, x, 'up'
    else:
        raise Exception('Start location not found')


def __get_visited_locations(guard_y: int, guard_x: int, guard_dir: str, grid: list) -> set:
    visited_locations = set()
    while True:
        visited_locations.add((guard_y, guard_x))
        guard_y, guard_x, guard_dir = __get_next_position(guard_y, guard_x, guard_dir, grid)
        if guard_y is None:
            break
    return visited_locations


def solve_part_a(input_data: str) -> str:
    grid = utils.get_grid(input_data)
    guard_y, guard_x, guard_dir = __get_start_location(grid)
    visited_locations = __get_visited_locations(guard_y, guard_x, guard_dir, grid)
    return str(len(visited_locations))


def solve_part_b(input_data: str) -> str:
    """
    for each position in the grid that the guard visits:
    replace position with #
    -> check if same position (+ direction) is visited twice
    if yes, break and add this position as looping loouie
    -> when done, len(looping loouie)
    """
    grid = utils.get_grid(input_data)
    looping_loouie = set()
    start_y, start_x, start_dir = __get_start_location(grid)
    guard_path = __get_visited_locations(start_y, start_x, start_dir, grid)

    for y, x in guard_path:
        if grid[y][x] == '#' or grid[y][x] == '^':
            continue
        grid[y][x] = '#'
        guard_y, guard_x, guard_dir = start_y, start_x, start_dir
        visited_locations = set()
        is_looping_loouie = False

        while True:
            location = (guard_y, guard_x, guard_dir)
            if location in visited_locations:
                is_looping_loouie = True
                logger.debug('break is_looping_loouie')
                break
            visited_locations.add(location)
            guard_y, guard_x, guard_dir = __get_next_position(guard_y, guard_x, guard_dir, grid)
            if guard_y is None:
                break

        if is_looping_loouie:
            looping_loouie.add((y, x))
        grid[y][x] = '.'

    return str(len(looping_loouie))


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 6
    logger.info(f'🎄 Running puzzle day 06...')
    puzzle = Puzzle(year=year, day=day)
    input_data = utils.get_input_data(puzzle, example_data=EXAMPLE_DATA)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', input_data, submit_solution=(not EXAMPLE_DATA))
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', input_data, submit_solution=(not EXAMPLE_DATA))

    return None

if __name__ == '__main__':
    main()