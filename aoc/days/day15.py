#!/usr/bin/env python3
import logging
from typing import List, Tuple

from aocd.models import Puzzle

from shared import utils
from shared.logger import logger
from shared.utils import Point

logger.setLevel(logging.INFO)
EXAMPLE_DATA = False
SUBMIT = True

# HACK: Overwrites
# SUBMIT = False
# logger.setLevel(logging.DEBUG)
# EXAMPLE_DATA = True

# --- Constants ---
ROBOT = '@'
WALL = '#'
EMPTY = '.'
BOX = 'O'
BOX_LEFT = '['
BOX_RIGHT = ']'


def solve_part_a(input_data: str) -> str:
    """Solves part A of the puzzle."""
    grid, movements = parse_input(input_data)
    return str(run_simulation(grid, movements))


def solve_part_b(input_data: str) -> str:
    """Solves part B of the puzzle."""
    grid, movements = parse_input(input_data, part_b=True)
    return str(run_simulation(grid, movements))
    
    
def parse_input(input_data: str, part_b: bool = False) -> Tuple[utils.Grid, List[Point]]:
    """Parses the input data into a grid and a list of movement points."""
    grid_str, movements_str = input_data.split('\n\n', 1)
    if part_b:
        grid = double_grid(grid_str)
    else:
        grid = utils.Grid(grid_str)
    movements = parse_movements(movements_str)
    return grid, movements


def parse_movements(movements_str: str) -> List[Point]:
    """Parses the movement string into a list of direction points."""
    return [utils.STRAIGHT_DIRECTIONS_SYMBOL[c] for c in movements_str if c in utils.STRAIGHT_DIRECTIONS_SYMBOL]


def double_grid(grid_data: str) -> utils.Grid:
    """Creates a new grid with doubled width according to part B rules."""
    mapping = {
        WALL: WALL * 2,
        BOX: BOX_LEFT + BOX_RIGHT,
        EMPTY: EMPTY * 2,
        ROBOT: ROBOT + EMPTY,
    }
    new_grid_lines = []
    for line in grid_data.splitlines():
        if line:
            new_grid_lines.append(''.join(mapping.get(char, '') for char in line))
    return utils.Grid('\n'.join(new_grid_lines))

    
def run_simulation(grid: utils.Grid, movements: List[Point]) -> int:
    """Runs the robot simulation on a given grid and returns the final GPS score."""
    robot_position = get_robot_start(grid)
    for movement in movements:
        new_robot_position, boxes_to_push = check_robot_move(grid, movement, robot_position)
        if robot_position != new_robot_position:
            robot_position = move_robot(robot_position, new_robot_position, movement, boxes_to_push, grid)
    logger.debug(grid)
    return calc_total_gps(grid)


def get_robot_start(grid: utils.Grid) -> Point:
    """Finds the starting position of the robot."""
    for p, val in grid:
        if val == ROBOT:
            return p
    raise ValueError('No robot start point found in the grid')


def get_box_at(position: Point, grid: utils.Grid) -> Tuple[Point, Point] | None:
    """If position is part of a 2-cell box, returns the two points of the box, else None."""
    if grid[position] == BOX_LEFT:
        return position, position + Point(0, 1)
    if grid[position] == BOX_RIGHT:
        return position + Point(0, -1), position
    return None


def check_robot_move(grid: utils.Grid, direction: Point, robot_position: Point) -> Tuple[Point, List]:
    """Checks if a move is possible and returns the new position and any boxes that would be pushed."""
    new_robot_position = direction + robot_position
    boxes_to_push = []
    stack = {new_robot_position}
    processed = set()  # Contains single points and tuples of points (boxes)

    while stack:
        current_pos = stack.pop()
        if current_pos in processed:
            continue

        obj_at_pos = grid[current_pos]

        if not obj_at_pos or obj_at_pos == WALL:
            return robot_position, []  # Blocked move

        if obj_at_pos == EMPTY:
            continue  # Path is clear

        processed.add(current_pos)

        if obj_at_pos == BOX:
            boxes_to_push.append(current_pos)
            stack.add(direction + current_pos)
        elif obj_at_pos in [BOX_LEFT, BOX_RIGHT]:
            box = get_box_at(current_pos, grid)
            if box and box not in processed:
                boxes_to_push.append(box)
                processed.add(box)
                stack.add(direction + box[0])
                stack.add(direction + box[1])

    return new_robot_position, boxes_to_push


def move_robot(robot_position: Point, new_robot_position: Point, direction: Point, boxes_to_push: list, grid: utils.Grid) -> Point:
    """Executes the move, updating the grid with new robot and box positions."""
    to_clear = {robot_position}
    to_set = {new_robot_position: ROBOT}

    for box in boxes_to_push:
        if isinstance(box, Point):  # Single 'O' box
            to_clear.add(box)
            to_set[direction + box] = BOX
        else:  # Tuple for '[]' box
            to_clear.update(box)
            to_set[direction + box[0]] = BOX_LEFT
            to_set[direction + box[1]] = BOX_RIGHT

    # Clear old positions, careful not to clear a spot that will be occupied
    for p in to_clear:
        if p not in to_set:
            grid[p] = EMPTY

    # Set new positions
    for p, val in to_set.items():
        grid[p] = val

    return new_robot_position


def calc_total_gps(grid: utils.Grid) -> int:
    """Calculates the total GPS signal strength from all boxes."""
    return sum(y * 100 + x for (y, x), val in grid if val in (BOX, BOX_LEFT))


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day.
    """
    year = 2024
    day = 15
    logger.info('🎄 Running puzzle day 15...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)

    return None

if __name__ == '__main__':
    main()
    