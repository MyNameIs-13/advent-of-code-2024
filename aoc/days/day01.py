#!/usr/bin/env python3
from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True

def input_data_to_list(input_data: str, splitter: str = '\n') -> list:
    """
    format the input_data into a list.
    without overwriting splitter, it will split the input_data into lines
    """
    return input_data.split(splitter)


def solve_part_a(input_data: str) -> str:
    left_list = []
    right_list = []
    for line in input_data_to_list(input_data):
        l, r = input_data_to_list(line, splitter='   ')
        left_list.append(int(l))
        right_list.append(int(r))
    left_list = sorted(left_list)
    right_list = sorted(right_list)

    distance_sum = 0
    for i in range(0, len(left_list)):
        distance_sum += abs(left_list[i] - right_list[i])

    return str(distance_sum)


def solve_part_b(input_data: str) -> str:
    left_list = []
    right_list_occurrences = {}
    for line in input_data_to_list(input_data):
        l, r = input_data_to_list(line, splitter='   ')
        left_list.append(int(l))
        right_list_occurrences[int(r)] = right_list_occurrences.get(int(r), 0) + 1

    distance_sum = 0
    for i in range(0, len(left_list)):
        distance_sum += left_list[i] * right_list_occurrences.get(left_list[i], 0)

    return str(distance_sum)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 1
    logger.info(f'🎄 Running puzzle day 01...')
    puzzle = Puzzle(year=year, day=day)
    input_data = utils.get_input_data(puzzle, example_data=EXAMPLE_DATA)

    for part, solve_func in [('a', solve_part_a), ('b', solve_part_b)]:
        utils.solve_puzzle_part(puzzle, solve_func, part, input_data, submit_solution=(not EXAMPLE_DATA))

    return None

if __name__ == '__main__':
    main()