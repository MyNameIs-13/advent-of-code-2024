#!/usr/bin/env python3
from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # overwrite
SUBMIT = True
# SUBMIT = False  # overwrite

def solve_part_a(input_data: str) -> str:
    is_file = True
    decompressed = []
    i = 0
    for c in input_data:
        if is_file:
            is_file = False
            decompressed_value = str(i)
            i += 1
        else:
            is_file = True
            decompressed_value = '.'
        for j in range(int(c)):
            decompressed.append(decompressed_value)
    logger.debug(decompressed)

    for i in range(len(decompressed)):
        if '.' not in decompressed:
            break

        if decompressed[i] == '.':
            while True:
                c = decompressed.pop(-1)
                if c == '.':
                    continue
                else:
                    decompressed[i] = c
                    break
        else:
            continue
    logger.debug(decompressed)

    result = 0
    for i in range(len(decompressed)):
        result += i * int(decompressed[i])

    return str(result)


def solve_part_b(input_data: str) -> str:
    """
    todo:
    create output as in a, but create space map
    upadte space map from time to time
    """
    is_file = True
    decompressed = []
    free_space_map = {}  # start_index, space_count
    i = 0
    free_space_index = 1
    for c in input_data:
        if is_file:
            is_file = False
            decompressed_value = str(i)
            i += 1
        else:
            is_file = True
            decompressed_value = '.'
            if int(c) > 0:
                free_space_map[free_space_index] = int(c)
                free_space_index += 2
            else:
                free_space_index += 1
        if int(c) > 0:
            _ = []
            for j in range(int(c)):
                _.append(decompressed_value)
            decompressed.append(_)
    logger.debug(decompressed)
    logger.debug(free_space_map)

    for rev_i in range(len(decompressed)-1, 0, -1):
        if decompressed[rev_i][0] == '.':
            if rev_i in free_space_map:
                free_space_map.pop(rev_i)
        else:
            for index, free_spaces in free_space_map.items():
                if index > rev_i:
                    break
                if free_spaces >= len(decompressed[rev_i]):
                    index_offset = 0
                    for dot in decompressed[index]:
                        if dot == '.':
                            break
                        else:
                            index_offset += 1
                    else:
                        index_offset = 0
                    for j, num in enumerate(decompressed[rev_i]):
                        # logger.debug(decompressed)
                        # logger.debug(free_space_map)
                        logger.debug(f'index: {index} - j: {j} - index_offset: {index_offset} - rev_i: {rev_i}')
                        decompressed[index][j+index_offset] = num
                        free_space_map[index] -= 1
                        decompressed[rev_i][j] = '.'
                        # TODO: add decompressed[rev_i] to spaces map (seems not necessary for correct solution...)

                    if free_space_map[index] == 0:
                        free_space_map.pop(index)

                    break


    logger.debug(decompressed)
    logger.debug(free_space_map)
    decompressed = [x for sublist in decompressed for x in sublist]
    logger.debug(decompressed)

    result = 0
    for i in range(len(decompressed)):
        if decompressed[i] != '.':
            result += i * int(decompressed[i])

    return str(result)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 9
    logger.info(f'🎄 Running puzzle day 09...')
    puzzle = Puzzle(year=year, day=day)

    # utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)

    return None

if __name__ == '__main__':
    main()