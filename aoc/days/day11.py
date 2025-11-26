#!/usr/bin/env python3
import math
from functools import lru_cache
from typing import Counter

from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # overwrite
SUBMIT = True
# SUBMIT = False  # overwrite


@lru_cache(maxsize=None)
def __blink_fast(stone: int, remaining_blinks: int) -> int:
    if remaining_blinks == 0:
        return 1

    if stone == 0:
        return __blink_fast(1, remaining_blinks - 1)
    elif len(str(stone)) % 2 == 0:
        logger.debug(f'stone: {stone}')
        stone_len = len(str(stone))
        left = int(str(stone)[0:stone_len // 2])
        logger.debug(f'left: {left}')
        right = int(str(stone)[stone_len // 2:])
        logger.debug(f'right: {right}')
        return __blink_fast(left, remaining_blinks - 1) + __blink_fast(right, remaining_blinks - 1)
    else:
        return __blink_fast(stone * 2024, remaining_blinks - 1)


def solve_part_a(input_data: str) -> str:
    """
    If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
    """
    blink_countdown = 25

    stone_list = []
    for line in utils.input_data_to_list(input_data):
        stone_list = [int(x) for x in line.split(' ')]

    stone_counter = 0
    for stone in stone_list:
        stone_counter += __blink_fast(stone, blink_countdown)

    return str(stone_counter)


def solve_part_b(input_data: str) -> str:
    blink_countdown = 75

    stone_list = []
    for line in utils.input_data_to_list(input_data):
        stone_list = [int(x) for x in line.split(' ')]

    stone_counter = 0
    for stone in stone_list:
        stone_counter += __blink_fast(stone, blink_countdown)

    return str(stone_counter)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 11
    logger.info(f'🎄 Running puzzle day 11...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)

    return None

if __name__ == '__main__':
    main()