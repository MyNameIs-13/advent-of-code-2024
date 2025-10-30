#!/usr/bin/env python3
import operator
import re

from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # comment out to use real data


def in_bounds(x: int, y: int, rows_length: int, cols_length: int) -> bool:
    return 0 <= x < rows_length and 0 <= y < cols_length


def find_word(grid: list, word: str) -> list:
    rows_length = len(grid)
    cols_length = len(grid[0])
    word_length = len(word)
    found_positions = []
    # 8 directions: (dx, dy)
    directions = [
        # forward
        (1, 0),  # down
        (0, 1),  # right
        (1, -1),  # down-left
        (1, 1),  # down-right
        # backward
        (-1, 0),  # up
        (0, -1),  # left
        (-1, -1),  # up-left
        (-1, 1)  # up-right
    ]

    # Loop through the grid and use every position as starting position
    for i in range(0, rows_length):
        for j in range(0, cols_length):
            # Check if the starting position start with the letter the words start with
            if grid[i][j] == word[0]:
                # search in all directions if the word can be found
                for dx, dy in directions:
                    k = 0
                    x, y = i, j
                    while k < word_length and in_bounds(x, y, rows_length, cols_length) and grid[x][y] == word[k]:
                        x += dx
                        y += dy
                        k += 1
                    if k == word_length:
                        found_positions.append(((i, j), (x - dx, y - dy)))  # start & end position

    return found_positions


def check_diagonal(grid: list, word: str, i: int, j: int, directions) -> bool:
    half = len(word) // 2
    rows, cols = len(grid), len(grid[0])

    # check in one direction while comparing the left part of the word, the other direction while comparing the right part of the word
    for dx, dy, op in directions:
        for k in range(1, half + 1):
            x = i + dx * k
            y = j + dy * k
            if not in_bounds(x, y, rows, cols) or grid[x][y] != word[op(half, k)]:
                return False
    return True


def find_X_word(grid: list, word: str) -> list:
    if len(word) % 2 == 0:
        raise ValueError('Word must have odd length')

    rows = len(grid)
    cols = len(grid[0])
    half = len(word) // 2
    mid_char = word[half]
    found = []

    # Predefine direction sets
    slash_dirs = {(1, -1, operator.add), (-1, 1, operator.sub)}   # ↙ ↗
    backslash_dirs = {(1, 1, operator.add), (-1, -1, operator.sub)} # ↘ ↖

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != mid_char:
                continue

            # Check if the word appear forward or backward in slash directions
            slash = check_diagonal(grid, word, i, j, slash_dirs) or check_diagonal(grid, word[::-1], i, j, slash_dirs)
            # Check if the word appear forward or backward in backslash directions
            backslash = check_diagonal(grid, word, i, j, backslash_dirs) or check_diagonal(grid, word[::-1], i, j, backslash_dirs)
            # When the word appear forward or backwards in slash or backslash directions, it's a hit
            if slash and backslash:
                found.append((i, j))

    return found


def solve_part_a(input_data: str) -> str:
    # TODO: implement solution for part A
    p1 = find_word(utils.get_grid(input_data), 'XMAS')
    result = len(p1)
    return str(result)


def solve_part_b(input_data: str) -> str:
    # TODO: implement solution for part B
    # How many times is the word MAS in a X shape in the grid
    # M - M    M - S
    # - A -    - A -
    # S - S    M - S
    p1 = find_X_word(utils.get_grid(input_data), 'MAS')
    result = len(p1)
    return str(result)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 4
    logger.info(f'🎄 Running puzzle day 04...')
    puzzle = Puzzle(year=year, day=day)
    input_data = utils.get_input_data(puzzle, example_data=EXAMPLE_DATA)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', input_data, submit_solution=(not EXAMPLE_DATA))
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', input_data, submit_solution=(not EXAMPLE_DATA))

    return None

if __name__ == '__main__':
    main()