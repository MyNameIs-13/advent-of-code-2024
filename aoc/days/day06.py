#!/usr/bin/env python3
from typing import Tuple

from aocd.models import Puzzle

from shared import utils
from shared.logger import logger

# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # comment out to use real data

CHANGE_DIRECTION = {
    'up': 'right',
    'right': 'down',
    'down': 'left',
    'left': 'up'
}


def __get_next_position(p: utils.Point, direction: str, grid: utils.Grid) -> Tuple[utils.Point, str] | None:
    next_p = p + utils.DIRECTIONS[direction]
    if grid.in_bounds(next_p):
        if grid[next_p] == '#':
            direction = CHANGE_DIRECTION[direction]
            next_p = p
    else:
        return None
    return next_p, direction


def __get_start_location(grid: utils.Grid) -> Tuple[utils.Point, str]:
    for p, value in grid:
        if value == '^':
            logger.debug(f'{p}, up')
            return p, 'up' 
    else:
        raise Exception('Start location not found')


def __get_visited_locations(guard_p: utils.Point, guard_dir: str, grid: utils.Grid) -> set:
    visited_locations = set()
    while True:
        visited_locations.add(guard_p)
        next_pos = __get_next_position(guard_p, guard_dir, grid)
        if next_pos:
            guard_p = next_pos[0]
            guard_dir = next_pos[1]
        else:
            break
    return visited_locations


def solve_part_a(input_data: str) -> str:
    grid = utils.Grid(input_data)
    guard_p, guard_dir = __get_start_location(grid)
    visited_locations = __get_visited_locations(guard_p, guard_dir, grid)
    return str(len(visited_locations))


def solve_part_b(input_data: str) -> str:
    """
    for each position in the grid that the guard visits:
    replace position with #
    -> check if same position (+ direction) is visited twice
    if yes, break and add this position as looping loouie
    -> when done, len(looping loouie)
    """
    looping_loouie = set()
    grid = utils.Grid(input_data)
    start_p, start_dir = __get_start_location(grid)
    guard_path = __get_visited_locations(start_p, start_dir, grid)

    for p in guard_path:
        if grid[p] in ('#', '^'):
            continue
        grid[p] = '#'
        guard_p, guard_dir = start_p, start_dir
        visited_locations = set()
        is_looping_loouie = False

        while True:
            location = (guard_p, guard_dir)
            if location in visited_locations:
                is_looping_loouie = True
                logger.debug('break is_looping_loouie')
                break
            visited_locations.add(location)
            next_location = __get_next_position(guard_p, guard_dir, grid)
            if next_location:
                guard_p = next_location[0]
                guard_dir = next_location[1]
            else:
                break            

        if is_looping_loouie:
            looping_loouie.add(p)
        grid[p] = '.'

    return str(len(looping_loouie))


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 6
    logger.info('🎄 Running puzzle day 06...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=True)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=True)

    return None

if __name__ == '__main__':
    main()