#!/usr/bin/env python3
import operator

from aocd.models import Puzzle

from shared import utils
from shared.logger import logger

# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # comment out to use real data


def find_word(grid: utils.Grid, word: str) -> list:
    word_length = len(word)
    found_positions = []

    for p, value in grid:
        # Check if the starting position start with the letter the words start with
        if value == word[0]:
            # search in all directions if the word can be found
            for d in utils.DIRECTIONS.values():
                k = 0
                temp_p = utils.Point(p.y, p.x)
                while k < word_length and grid.in_bounds(temp_p) and grid[temp_p] == word[k]:
                    temp_p += d
                    k += 1
                if k == word_length:
                    found_positions.append((p, temp_p - d))  # start & end position            
    return found_positions


def check_diagonal(grid: utils.Grid, word: str, p: utils.Point, directions) -> bool:
    half = len(word) // 2

    # check in one direction while comparing the left part of the word, the other direction while comparing the right part of the word
    for d, op in directions:
        for k in range(1, half + 1):
            y = p.y + d.y * k
            x = p.x + d.x * k
            next_p = utils.Point(y, x)
            if not grid.in_bounds(next_p) or grid[next_p] != word[op(half, k)]:
                return False
    return True


def find_X_word(grid: utils.Grid, word: str) -> list:
    if len(word) % 2 == 0:
        raise ValueError('Word must have odd length')

    half = len(word) // 2
    mid_char = word[half]
    found = []

    # Predefine direction sets
    slash_dirs = {(utils.DIRECTIONS['down-left'], operator.add), (utils.DIRECTIONS['up-right'], operator.sub)}   # ↙ ↗
    backslash_dirs = {(utils.DIRECTIONS['down-right'], operator.add), (utils.DIRECTIONS['up-left'], operator.sub)} # ↘ ↖

    for p, value in grid:
        if value != mid_char:
            continue
        # Check if the word appear forward or backward in slash directions
        slash = check_diagonal(grid, word, p, slash_dirs) or check_diagonal(grid, word[::-1], p, slash_dirs)
        # Check if the word appear forward or backward in backslash directions
        backslash = check_diagonal(grid, word, p, backslash_dirs) or check_diagonal(grid, word[::-1], p, backslash_dirs)
        # When the word appear forward or backwards in slash or backslash directions, it's a hit
        if slash and backslash:
            found.append(p)            
            
    return found


def solve_part_a(input_data: str) -> str:
    found_positions = find_word(utils.Grid(input_data), 'XMAS')
    result = len(found_positions)
    return str(result)


def solve_part_b(input_data: str) -> str:
    # How many times is the word MAS in a X shape in the grid
    # M - M    M - S
    # - A -    - A -
    # S - S    M - S
    found_positions = find_X_word(utils.Grid(input_data), 'MAS')
    result = len(found_positions)
    return str(result)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 4
    logger.info('🎄 Running puzzle day 04...')
    puzzle = Puzzle(year=year, day=day)
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=True)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=True)

    return None

if __name__ == '__main__':
    main()