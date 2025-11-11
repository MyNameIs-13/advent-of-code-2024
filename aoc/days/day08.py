#!/usr/bin/env python3
from typing import Tuple

from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # comment out to use real data

def __is_antinode(y: int, x: int, row_count: int, col_count: int, antinodes: set) -> bool:
    if 0 <= y < row_count and 0 <= x < col_count:
        antinodes.add((y, x))
        return True
    return False


def __calculate_antinodes(positions: list, antinodes: set, row_count: int, col_count: int, part_b: bool = False) -> None:
    if len(positions) == 1:
        return

    start_position = positions[0]
    for _position in positions[1:]:
        __calc_distance(start_position, _position, antinodes, row_count, col_count, part_b=part_b)

    __calculate_antinodes(positions[1:], antinodes, row_count, col_count, part_b=part_b)


def __calc_distance(start_position: Tuple[int, int], _position: Tuple[int, int], antinodes: set, row_count: int, col_count: int, part_b: bool = False) -> None:
    diff_y = _position[0] - start_position[0]
    diff_x = _position[1] - start_position[1]

    possible_antinode = (start_position[0] - diff_y, start_position[1] - diff_x)
    if part_b:
        while part_b and __is_antinode(possible_antinode[0], possible_antinode[1], row_count, col_count, antinodes):
            possible_antinode = (possible_antinode[0] - diff_y, possible_antinode[1] - diff_x)
    else:
        __is_antinode(possible_antinode[0], possible_antinode[1], row_count, col_count, antinodes)

    possible_antinode = (_position[0] + diff_y, _position[1] + diff_x)
    if part_b:
        while __is_antinode(possible_antinode[0], possible_antinode[1], row_count, col_count, antinodes):
            possible_antinode = (possible_antinode[0] + diff_y, possible_antinode[1] + diff_x)
    else:
        __is_antinode(possible_antinode[0], possible_antinode[1], row_count, col_count, antinodes)

    return


def __build_antenna_type_positions_dict(grid: list) -> dict:
    col_count = len(grid[0])
    row_count = len(grid)
    # build a dict with all positions for each antenna frequency type
    antenna_type_positions_dict = {}
    for y in range(row_count):
        for x in range(col_count):
            c = grid[y][x]
            if c in utils.SMALL_LETTER or c in utils.CAPITAL_LETTER or c in utils.NUMBERS_STR:
                antenna_type_positions_dict.setdefault(c, []).append((y, x))
    logger.debug(antenna_type_positions_dict)
    return antenna_type_positions_dict


def solve_part_a(input_data: str) -> str:
    """
    loop through grid.
    For each Antenna signal, save locations in dict (a: [(1, 2), ...], b: [])
    for each antenna signal calc distance between all other of same antenna
        with that distance calc noise source positions
        save noise source positions
    """
    grid = utils.get_grid(input_data)
    antenna_type_positions_dict = __build_antenna_type_positions_dict(grid)

    antinodes = set()
    col_count = len(grid[0])
    row_count = len(grid)
    for _, positions in antenna_type_positions_dict.items():
        __calculate_antinodes(positions, antinodes, row_count, col_count)

    return str(len(antinodes))


def solve_part_b(input_data: str) -> str:
    grid = utils.get_grid(input_data)
    antenna_type_positions_dict = __build_antenna_type_positions_dict(grid)

    antinodes = set()
    col_count = len(grid[0])
    row_count = len(grid)
    for _, positions in antenna_type_positions_dict.items():
        for antenna in positions:
            antinodes.add((antenna[0], antenna[1]))
        __calculate_antinodes(positions, antinodes, row_count, col_count, part_b=True)
    logger.debug(antinodes)
    return str(len(antinodes))


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 8
    logger.info(f'🎄 Running puzzle day 08...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=True)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=True)

    return None

if __name__ == '__main__':
    main()