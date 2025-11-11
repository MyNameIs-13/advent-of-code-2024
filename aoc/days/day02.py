#!/usr/bin/env python3
from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # comment out to use real data


def is_level_save(numbers_list):
    save = True
    first_direction = None
    prev_num = None
    for num in numbers_list:
        logger.debug(f'prev_num={prev_num}')
        logger.debug(f'num={num}')
        if prev_num is None:
            prev_num = num
        else:
            if abs(prev_num - num) < 1 or abs(prev_num - num) > 3:
                logger.debug('diff to big')
                save = False
                break
            if first_direction is None:
                first_direction = 'up' if prev_num < num else 'down'
            else:
                if (prev_num < num and first_direction == 'up') or (prev_num > num and first_direction == 'down'):
                    pass
                else:
                    logger.debug('not steady')
                    save = False
                    break
            prev_num = num
    return save

def solve_part_a(input_data: str) -> str:
    # TODO: implement solution for part A
    result = 0

    for line in utils.input_data_to_list(input_data):
        logger.debug(line)
        numbers_list = [int(num_str) for num_str in line.split(' ')]
        if is_level_save(numbers_list):
            logger.debug('save')
            result += 1

    return str(result)


def solve_part_b(input_data: str) -> str:
    result = 0

    for line in utils.input_data_to_list(input_data):
        logger.debug(line)
        numbers_list = [int(num_str) for num_str in line.split(' ')]
        if is_level_save(numbers_list):
            logger.debug('save')
            result += 1
        else:
            for i in range(0, len(numbers_list)):
                _numbers_list = numbers_list.copy()
                _numbers_list.pop(i)
                if is_level_save(_numbers_list):
                    logger.debug('save')
                    result += 1
                    break


    return str(result)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 2
    logger.info(f'🎄 Running puzzle day 02...')
    puzzle = Puzzle(year=year, day=day)
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=True)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=True)

    return None

if __name__ == '__main__':
    main()