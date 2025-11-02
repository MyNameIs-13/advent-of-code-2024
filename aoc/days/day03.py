#!/usr/bin/env python3
import math
import re

from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # comment out to use real data

def solve_part_a(input_data: str) -> str:
    # TODO: implement solution for part A
    result = 0
    pattern = r'mul\(\d{1,3},\d{1,3}\)'
    matches = re.findall(pattern, input_data)
    logger.debug(matches)
    for match in matches:
        pattern = r'\d{1,3}'
        numbers = re.findall(pattern, match)
        numbers = [int(num) for num in numbers]
        logger.debug(numbers)
        result += math.prod(numbers)
    return str(result)


def solve_part_b(input_data: str) -> str:
    # TODO: implement solution for part B
    result = 0
    patten_not = r"don't\(\)"
    pattern_do = r"do\(\)"
    matches_not = [match for match in re.finditer(patten_not, input_data)]
    matches_do = [match for match in re.finditer(pattern_do, input_data)]

    logger.debug(f'input_data: {input_data}')

    do_list = []
    index = 0
    do = True

    logger.debug(f'len input_data: {len(input_data)}')
    while index <= len(input_data):
        logger.debug(f'do: {do}')
        if do:
            # find next stop
            # add the removed input data to do_list
            # set do to False
            # increase index (to start of stop)
            while matches_not and matches_not[0].start() < index:
                _ = matches_not.pop(0)
                logger.debug(f'remove not {_.start()}')
            if matches_not:
                stop_match = matches_not.pop(0)
                logger.debug(f'stop_match found. stop at {stop_match.start()}')
                logger.debug(input_data[index:stop_match.start()])
                do_list.append(input_data[index:stop_match.start()])
                index = stop_match.start()
                logger.debug(f'new index: {index}')
                do = False
            else:
                do_list.append(input_data[index:])
                break
        else:
            # find next start
            # set do to True
            # increase index (to start of stop)
            while matches_do and matches_do[0].start() < index:
                _ = matches_do.pop(0)
                logger.debug(f'remove do {_.start()}')
            if matches_do:
                start_match = matches_do.pop(0)
                logger.debug(f'start_match found. stop at {start_match.start()}')
                logger.debug(input_data[index:start_match.start()])
                index = start_match.start()
                logger.debug(f'new index: {index}')
                do = True
            else:
                break
    logger.debug(f'do_list: {do_list}')
    pattern = r'mul\(\d{1,3},\d{1,3}\)'
    pattern_num = r'\d{1,3}'
    for do_str in do_list:
        matches = re.findall(pattern, do_str)
        logger.debug(matches)
        for match in matches:
            numbers = re.findall(pattern_num, match)
            numbers = [int(num) for num in numbers]
            logger.debug(numbers)
            result += math.prod(numbers)

    return str(result)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 3
    logger.info(f'🎄 Running puzzle day 03...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=True)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=True)

    return None

if __name__ == '__main__':
    main()