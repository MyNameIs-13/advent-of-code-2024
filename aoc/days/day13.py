#!/usr/bin/env python3
import logging
import re

from aocd.models import Puzzle

from shared import utils
from shared.logger import logger

# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # overwrite
SUBMIT = True
# SUBMIT = False  # overwrite

def solve_part_a(input_data: str) -> str:
    claw_machines_list = get_claw_machine_list(input_data)
    result = 0
    for claw_machine in claw_machines_list:
        a, b = get_button_presses(claw_machine)
        result += get_token_costs(a, b)
    return str(result)


def solve_part_b(input_data: str) -> str:
    claw_machines_list = get_claw_machine_list(input_data, part_b=True)
    result = 0
    for claw_machine in claw_machines_list:
        a, b = get_button_presses(claw_machine)
        result += get_token_costs(a, b)
    return str(result)


def get_claw_machine_list(input_data: str, part_b: bool = False) -> list:
    claw_machines_list = []
    claw_machine = {}
    for line in utils.input_data_to_list(input_data):
        # logger.debug(line)
        if not line:
            claw_machines_list.append(claw_machine)
            claw_machine = {}
            continue
        if 'Prize' in line:
            key = 'Prize'
            pattern = r'X=(\d+), Y=(\d+)'
        else:
            key = 'A' if 'A' in line else 'B'
            pattern = r'X\+(\d+), Y\+(\d+)'
        match = re.search(pattern, line)
        if match:
            if part_b and key == 'Prize':
                claw_machine[key] = (int(match.group(1)) + 10000000000000 , int(match.group(2)) + 10000000000000)
            else:
                claw_machine[key] = (int(match.group(1)), int(match.group(2)))
        else:
            raise Exception(f'no match found for line {line}')
    claw_machines_list.append(claw_machine)
    logger.debug(claw_machines_list)
    return claw_machines_list


def get_button_presses(claw_machine: dict) -> tuple[int, int]:
    A_x, A_y = claw_machine['A']
    B_x, B_y = claw_machine['B']
    P_x, P_y = claw_machine['Prize']

    # Compute determinant
    D = A_x * B_y - A_y * B_x
    if D == 0:
        return (0, 0)  # Skip if determinant is zero (no unique solution)

    # Solve for a and b using Cramer's rule
    a_num = P_x * B_y - P_y * B_x
    b_num = P_y * A_x - P_x * A_y

    a = a_num / D
    b = b_num / D
    return (a, b)


def get_token_costs(a: int, b: int) -> int:
    if a.is_integer() and b.is_integer() and a >= 0 and b >= 0:
        return 3 * int(a) + int(b)  # Token cost
    return 0


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 13
    logger.info('🎄 Running puzzle day 13...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)

    return None

if __name__ == '__main__':
    main()
