#!/usr/bin/env python3
import logging

from aocd.models import Puzzle

from shared import utils
from shared.logger import logger

# logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
# EXAMPLE_DATA = True  # overwrite
SUBMIT = True
# SUBMIT = False  # overwrite


def decompress(input_data: str) -> list:
    is_file = True
    decompressed = []
    i = 0
    for c in input_data:
        if is_file:
            is_file = False
            decompressed_value = i
            i += 1
        else:
            is_file = True
            decompressed_value = None
        for j in range(int(c)):
            decompressed.append(decompressed_value)
    logger.debug(decompressed)
    return decompressed
    
    
def fragment(decompressed: list) -> list:
    fragment = decompressed.copy()
    for i in range(len(fragment)):
        if i < len(fragment) and fragment[i] is None:
            while True:
                size = fragment.pop(-1)
                if size:
                    fragment[i] = size
                    break                    
    logger.debug(fragment)
    return fragment


def decompress2(input_data: str) -> tuple[list, dict]:
    is_file = True
    decompressed = []
    free_space_map = {}  # start_index, space_count
    i = 0
    free_space_index = 1
    for c in input_data:
        size = int(c)
        if is_file:
            is_file = False
            decompressed_value = i
            i += 1
        else:
            is_file = True
            decompressed_value = None
            if size > 0:
                free_space_map[free_space_index] = size
                free_space_index += 1
            free_space_index += 1
        if size > 0:
            current_segment = []
            for j in range(size):
                current_segment.append(decompressed_value)
            decompressed.append(current_segment)
    logger.debug(decompressed)
    logger.debug(free_space_map)
    return decompressed, free_space_map
    

def fragment2(decompressed: list, free_space_map: dict) -> list:
    for rev_i in range(len(decompressed)-1, 0, -1):
        logger.debug(f'rev_i: {rev_i}')
        if decompressed[rev_i][0] is None:
            if rev_i in free_space_map:
                free_space_map.pop(rev_i)
        else:
            for index, free_spaces in free_space_map.items():
                if index > rev_i:
                    break
                if free_spaces >= len(decompressed[rev_i]):
                    index_offset = 0
                    for dot in decompressed[index]:
                        if dot is None:
                            break
                        index_offset += 1
                    else:
                        index_offset = 0
                    for j, num in enumerate(decompressed[rev_i]):
                        logger.debug(f'index: {index} - j: {j} - index_offset: {index_offset} - rev_i: {rev_i}')
                        decompressed[index][j+index_offset] = num
                        free_space_map[index] -= 1
                        decompressed[rev_i][j] = None
                    if free_space_map[index] == 0:
                        free_space_map.pop(index)
                    break

    logger.debug(decompressed)
    logger.debug(free_space_map)
    decompressed = [x for sublist in decompressed for x in sublist]
    logger.debug(decompressed)
    return decompressed
    

def solve_part_a(input_data: str) -> str:
    decompressed = decompress(input_data)
    fragmented = fragment(decompressed)
    result = 0
    for i in range(len(fragmented)):
        result += i * fragmented[i]
    return str(result)
   
    
def solve_part_b(input_data: str) -> str:
    """
    todo:
    create output as in a, but create space map
    upadte space map from time to time
    """
    decompressed, free_space_map = decompress2(input_data)
    fragmented = fragment2(decompressed, free_space_map)
    result = 0
    for i in range(len(fragmented)):
        if fragmented[i] is not None:
            result += i * fragmented[i]
    return str(result)    


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 9
    logger.info('🎄 Running puzzle day 09...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)

    return None

if __name__ == '__main__':
    main()