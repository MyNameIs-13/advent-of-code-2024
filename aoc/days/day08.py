#!/usr/bin/env python3
from aocd.models import Puzzle

from shared import utils
from shared.logger import logger

# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # comment out to use real data


def __calculate_antinodes(positions: list, antinodes: set, grid: utils.Grid, part_b: bool = False) -> None:
    if len(positions) == 1:
        return

    start_position = positions[0]
    for _position in positions[1:]:
        __calc_distance(start_position, _position, antinodes, grid, part_b=part_b)

    __calculate_antinodes(positions[1:], antinodes, grid, part_b=part_b)


def __calc_distance(start_position: utils.Point, _position: utils.Point, antinodes: set, grid: utils.Grid, part_b: bool = False) -> None:
    diff = _position - start_position
    potential_antinode_1 = start_position - diff
    if part_b:
        current_antinode = potential_antinode_1
        while grid.in_bounds(current_antinode):
            antinodes.add(current_antinode)
            current_antinode -= diff
    else:
        if grid.in_bounds(potential_antinode_1):
            antinodes.add(potential_antinode_1)

    potential_antinode_2 = _position + diff
    if part_b:
        current_antinode = potential_antinode_2
        while grid.in_bounds(current_antinode):
            antinodes.add(current_antinode)
            current_antinode += diff
    else:
        if grid.in_bounds(potential_antinode_2):
            antinodes.add(potential_antinode_2)
    return


def __build_antenna_type_positions_dict(grid: utils.Grid) -> dict:

    # build a dict with all positions for each antenna frequency type
    antenna_type_positions_dict = {}
    for p, value in grid:
        if value != '.':
            antenna_type_positions_dict.setdefault(value, []).append(p)
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
    grid = utils.Grid(input_data)
    antenna_type_positions_dict = __build_antenna_type_positions_dict(grid)

    antinodes = set()
    for _, positions in antenna_type_positions_dict.items():
        __calculate_antinodes(positions, antinodes, grid)

    return str(len(antinodes))


def solve_part_b(input_data: str) -> str:
    grid = utils.Grid(input_data)
    antenna_type_positions_dict = __build_antenna_type_positions_dict(grid)

    antinodes = set()
    for _, positions in antenna_type_positions_dict.items():
        for antenna in positions:
            antinodes.add(antenna)
        __calculate_antinodes(positions, antinodes, grid, part_b=True)
    logger.debug(antinodes)
    return str(len(antinodes))


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 8
    logger.info('🎄 Running puzzle day 08...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=True)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=True)

    return None

if __name__ == '__main__':
    main()