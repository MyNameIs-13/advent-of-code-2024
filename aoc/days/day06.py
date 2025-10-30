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


def __in_bound(guard_position: Tuple[int, int] , grid: list) -> bool:
    rows = len(grid)
    cols = len(grid[0])
    if  0 <= guard_position[0] < rows and 0 <= guard_position[1] < cols:
        return True
    return False


def __get_next_position(guard_position: list) -> Tuple[int, int]:
    dy = guard_position[0] + utils.DIRECTIONS[guard_position[2]][0]
    dx = guard_position[1] + utils.DIRECTIONS[guard_position[2]][1]
    return dy, dx


def __get_start_location(grid: list) -> list:
    rows = len(grid)
    cols = len(grid[0])
    for y in range(rows):
        for x in range(cols):
            c = grid[y][x]
            if c == '^':
                start_location = [y, x, 'up']
                logger.debug(start_location)
                return start_location
    else:
        raise Exception('Start location not found')


def solve_part_a(input_data: str) -> str:
    grid = utils.get_grid(input_data)
    guard_position = __get_start_location(grid)

    visited_locations = set()
    while True:
        visited_locations.add((guard_position[0], guard_position[1]))
        next_position = __get_next_position(guard_position)
        if __in_bound((next_position[0], next_position[1]), grid):
            if grid[next_position[0]][next_position[1]] == '#':
                guard_position[2] = CHANGE_DIRECTION[guard_position[2]]
            else:
                guard_position[0] = next_position[0]
                guard_position[1] = next_position[1]
                logger.debug(guard_position)
        else:
            break

    return str(len(visited_locations))


def solve_part_b(input_data: str) -> str:
    # TODO: implement solution for part B
    """
    for each position in the grid do:
    replace position with #
    -> check if same position (+ direction) is visited twice
    if yes, break and add this position as looping loouie
    -> when done, len(looping loouie)
    """
    grid = utils.get_grid(input_data)
    start_location = __get_start_location(grid)
    looping_loouie = set()
    rows = len(grid)
    cols = len(grid[0])
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == '#' or grid[y][x] == '^':
                continue
            grid[y][x] = '#'
            guard_position = start_location[::]
            visited_locations = set()
            is_looping_loouie = False

            while True:
                location = (guard_position[0], guard_position[1], guard_position[2])
                if location in visited_locations:
                    is_looping_loouie = True
                    logger.debug('break is_looping_loouie')
                    break
                visited_locations.add(location)
                next_position = __get_next_position(guard_position)
                if __in_bound((next_position[0], next_position[1]), grid):
                    if grid[next_position[0]][next_position[1]] == '#':
                        guard_position[2] = CHANGE_DIRECTION[guard_position[2]]
                    else:
                        guard_position[0] = next_position[0]
                        guard_position[1] = next_position[1]
                        # logger.debug(guard_position)
                else:
                    logger.debug('break bounds')
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