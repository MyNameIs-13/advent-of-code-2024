#!/usr/bin/env python3
from typing import Tuple

from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
EXAMPLE_DATA = True  # comment out to use real data

def check_print_order(print_order: list, y_after_x: dict) -> bool:
    ok = True
    for i, page in enumerate(print_order):
        if page in y_after_x and y_after_x[page].intersection(set(print_order[i:])):
            ok = False
            break
    logger.debug(print_order)
    logger.debug(ok)
    return ok


def check_print_order_and_correct(print_order: list, y_after_x: dict) -> None:
    not_ordered = True
    while not_ordered:
        not_ordered = False  # assume it's fine until proven otherwise
        for i, page in enumerate(print_order):
            if page not in y_after_x:
                continue
            _intersection = y_after_x[page].intersection(set(print_order[i:]))
            if _intersection:
                # find the max index the page should go to (all pages in _intersection should come before page)
                j =  max(print_order.index(k) for k in _intersection)
                print_order.pop(i)
                print_order.insert(j, page)
                not_ordered = True  # problem detected, try again
                break
    logger.debug(print_order)
    return None


def format_input(input_data: str) -> Tuple[dict, dict, list]:
    x_before_y = {}
    y_after_x = {}
    print_input = []
    for line in utils.input_data_to_list(input_data):
        if '|' in line:
            xy = line.split('|')
            x_before_y.setdefault(int(xy[0]), set()).add(int(xy[1]))
            # {page: set()} all pages in set() must be after page
            y_after_x.setdefault(int(xy[1]), set()).add(int(xy[0]))
        else:
            pages = line.split(',')
            if pages and pages[0]:
                print_input.append([int(page) for page in pages if page])
    return x_before_y, y_after_x, print_input


def solve_part_a(input_data: str) -> str:
    result = 0
    x_before_y, y_after_x, print_input = format_input(input_data)
    for print_order in print_input:
        if check_print_order(print_order, y_after_x):
            result += print_order[len(print_order)//2]
    return str(result)


def solve_part_b(input_data: str) -> str:
    result = 0
    x_before_y, y_after_x, print_input = format_input(input_data)

    for print_order in print_input:
        if check_print_order(print_order, y_after_x):
            continue
        check_print_order_and_correct(print_order, y_after_x)
        result += print_order[len(print_order)//2]
    return str(result)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 5
    logger.info(f'🎄 Running puzzle day 05...')
    puzzle = Puzzle(year=year, day=day)
    input_data = utils.get_input_data(puzzle, example_data=EXAMPLE_DATA)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', input_data, submit_solution=(not EXAMPLE_DATA))
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', input_data, submit_solution=(not EXAMPLE_DATA))

    return None

if __name__ == '__main__':
    main()