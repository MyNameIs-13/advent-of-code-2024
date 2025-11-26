#!/usr/bin/env python3
import logging
import re
from time import sleep

from aocd.models import Puzzle

from shared import utils
from shared.logger import logger

logger.setLevel(logging.INFO)
EXAMPLE_DATA = False
SUBMIT = True

# HACK: Overwrites
# logger.setLevel(logging.DEBUG)
# EXAMPLE_DATA = True
# SUBMIT = False


def solve_part_a(input_data: str) -> str:
    columns: int = 11 if EXAMPLE_DATA else 101  # wide
    rows: int = 7 if EXAMPLE_DATA else 103  # tall  
    seconds: int = 100
    quadrants: dict = {'a': 0, 'b': 0, 'c': 0, 'd': 0}

    robots: list = getRobots(input_data)
    for robot in robots:
        y, x = get_robot_position_after_seconds(robot, seconds, columns, rows)
        countQuadrant(y, x, quadrants, columns, rows)
        logger.debug(f"Robot {robot} position after {seconds} seconds: {y}", {x})
    robot_per_quadrant_multiplied = 1
    logger.debug(f"Quadrants: {quadrants}")
    for quadrant_robot_count in quadrants.values():
        robot_per_quadrant_multiplied *= quadrant_robot_count
    return str(robot_per_quadrant_multiplied)


def solve_part_b(input_data: str) -> str:
    columns: int = 11 if EXAMPLE_DATA else 101  # wide
    rows: int = 7 if EXAMPLE_DATA else 103  # tall    
    initial_grid = [['.' for _ in range(columns)] for _ in range(rows)]
    seconds: int = 0
    
    robots: list = getRobots(input_data)
    tree_found: bool = False
    while not tree_found:
        grid = [row.copy() for row in initial_grid]
        for robot in robots:
            y, x = get_robot_position_after_seconds(robot, seconds, columns, rows)
            grid[y][x] = '#'
        for row in grid:
            if "##########" in ''.join(row):
                tree_found = True
        if tree_found:
            for row in grid:
                print(' '.join(row))
            sleep(3)        
        else:
            seconds += 1       
    return str(seconds)


def getRobots(input_data: str) -> list:
    pattern = r'p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)'
    robots: list = []
    for line in utils.input_data_to_list(input_data):
        # logger.debug(line)
        matches = re.match(pattern, line)
        if matches:
            robot = {
                'p': (int(matches.group(2)), int(matches.group(1))),
                'v': (int(matches.group(4)), int(matches.group(3)))
            }
            robots.append(robot)
            logger.debug(f"Added robot: {robot}")
        else:
            raise ValueError(f"Invalid input line: {line}")    
    return robots
    
    
def get_robot_position_after_seconds(robot: dict, seconds: int, columns: int, rows: int) -> tuple[int, int]:
    new_y = ((seconds * robot['v'][0]) + robot['p'][0]) % rows
    new_x = ((seconds * robot['v'][1]) + robot['p'][1]) % columns
    return new_y, new_x


def countQuadrant(y: int, x: int, quadrants: dict, columns: int, rows: int):
    center_x = columns // 2
    center_y = rows // 2
    if x < center_x and y < center_y:
        quadrants['a'] += 1
    elif x > center_x and y < center_y:
        quadrants['b'] += 1
    elif x < center_x and y > center_y:
        quadrants['c'] += 1
    elif x > center_x and y > center_y:
        quadrants['d'] += 1
        
        
def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 14
    logger.info('🎄 Running puzzle day 14...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)

    return None

if __name__ == '__main__':
    main()