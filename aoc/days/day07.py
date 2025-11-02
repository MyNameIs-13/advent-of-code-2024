#!/usr/bin/env python3
import operator
from math import prod
from os import MFD_ALLOW_SEALING

from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # comment out to use real data


def __get_input_data_list(input_data: str) -> list:
    input_data_list = []
    for line in utils.input_data_to_list(input_data):
        _ = line.split(':')
        input_data_list.append(
            {
                'result': int(_[0]),
                'parts': [int(x) for x in _[1].split(' ') if x]
            }
        )
    # logger.debug(input_data_list)
    logger.debug(len(input_data_list))
    return input_data_list


def __concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def __calculate_solution_recursive(input_data_list: list, part_b = False):
    solution = 0
    for line in input_data_list:
        result, parts = line['result'], line['parts']
        if __is_calculation_match(result, parts[0], parts[1:], part_b = part_b):
            solution += result
    return solution


def __is_calculation_match(expected_result: int, previous_result: int, remaining_numbers_list: list, part_b: bool = False) -> bool:
    if len(remaining_numbers_list) == 0:
        return expected_result == previous_result

    if previous_result > expected_result:
        return False

    if __is_calculation_match(expected_result, previous_result * remaining_numbers_list[0], remaining_numbers_list[1:], part_b=part_b):
        return True

    if part_b and __is_calculation_match(expected_result, __concat(previous_result, remaining_numbers_list[0]), remaining_numbers_list[1:], part_b=part_b):
        return True

    return __is_calculation_match(expected_result, previous_result + remaining_numbers_list[0], remaining_numbers_list[1:], part_b=part_b)


def solve_part_a(input_data: str) -> str:
    input_data_list = __get_input_data_list(input_data)
    solution = __calculate_solution_recursive(input_data_list)
    return str(solution)


def solve_part_b(input_data: str) -> str:
    input_data_list = __get_input_data_list(input_data)
    solution = __calculate_solution_recursive(input_data_list, part_b = True)
    return str(solution)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 7
    logger.info(f'🎄 Running puzzle day 07...')
    puzzle = Puzzle(year=year, day=day)
    input_data = utils.get_input_data(puzzle, example_data=EXAMPLE_DATA)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', input_data, submit_solution=(not EXAMPLE_DATA))
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', input_data, submit_solution=(not EXAMPLE_DATA))

    return None

if __name__ == '__main__':
    main()