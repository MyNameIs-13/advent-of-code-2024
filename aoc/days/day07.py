#!/usr/bin/env python3
import operator
from math import prod

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


def __calculate_solution(input_data_list: list, operators: list):
    solution = 0
    for line in input_data_list:
        result, parts = line['result'], line['parts']
        possible_results = {parts[0]}
        for _part in parts[1:]:
            new_possible_results = set()
            for _possible_result in possible_results:
                for _operator in operators:
                    _xx = _operator(_possible_result, _part)
                    if _xx <= result:
                        new_possible_results.add(_xx)
            possible_results = new_possible_results
        if result in possible_results:
            solution += result
        else:
            logger.debug(f'result: {result} parts: {parts}')
            logger.debug(f'{result} not')
            logger.debug(f'possible_results: {possible_results}')

    return solution


def __concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def solve_part_a(input_data: str) -> str:
    input_data_list = __get_input_data_list(input_data)
    operators = [operator.mul, operator.add]
    solution = __calculate_solution(input_data_list, operators)
    return str(solution)


def solve_part_b(input_data: str) -> str:
    input_data_list = __get_input_data_list(input_data)
    operators = [operator.mul, operator.add, __concat]
    solution = __calculate_solution(input_data_list, operators)
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