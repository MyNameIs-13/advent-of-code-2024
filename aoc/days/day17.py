#!/usr/bin/env python3
import logging

from aocd.models import Puzzle

from shared import utils
from shared.logger import logger

logger.setLevel(logging.INFO)
EXAMPLE_DATA = False
SUBMIT = True

# HACK: Overwrites
# SUBMIT = False
# logger.setLevel(logging.DEBUG)
# EXAMPLE_DATA = True

class ThreeBitComputer:
    def __init__(self, program: list[int], register_a: int = 0, register_b: int = 0, register_c: int = 0):
        self._program = program  # list of opcode, operands to be executed
        self._register_a = register_a
        self._register_b = register_b
        self._register_c = register_c
        self._instruction_pointer: int = 0  # index which opcode is read next from the program
        self._output = []
        self._execute_instruction = {
            0: self._adv,
            1: self._bxl,
            2: self._bst,
            3: self._jnz,
            4: self._bxc,
            5: self._out,
            6: self._bdv,
            7: self._cdv,
            None: 'invalid'
        }
                           
    def get_output(self) -> str:
        return ','.join(self._output)
        
    def reboot(self, register_a: int  = 0, register_b: int = 0, register_c: int = 0) -> None:
        """reset computer values to initial values"""
        self._instruction_pointer = 0
        self._output = []
        self._register_a = register_a
        self._register_b = register_b
        self._register_c = register_c        
               
    def run_program(self) -> None:
        while self._instruction_pointer < len(self._program):
            self._opcode = self._program[self._instruction_pointer]
            self._operand = self._program[self._instruction_pointer + 1]
            self._instruction_pointer += 2
            self._execute_instruction[self._opcode]()
        logger.debug('Program terminated')
        logger.debug(f'register A: {self._register_a}')
        logger.debug(f'register B: {self._register_b}')
        logger.debug(f'register C: {self._register_c}')
        
    def _set_combo_operand_value(self):
        if  0 >= self._operand <= 3:
            pass
        elif self._operand == 4:
            self._operand = self._register_a
        elif self._operand == 5:
            self._operand = self._register_b
        elif self._operand == 6:
            self._operand = self._register_c
        elif self._operand == 7:
            raise Exception('Invalid program - Encountered operand 7')
        
    def _adv(self):
        self._set_combo_operand_value()
        self._register_a = self._register_a // pow(2,self._operand)
    
    def _bxl(self):
        # bitwise XOR
        self._register_b = self._register_b ^ self._operand
    
    def _bst(self):
        self._set_combo_operand_value()
        self._register_b = self._operand % 8
    
    def _jnz(self):
        if self._register_a != 0:
            self._instruction_pointer = self._operand
    
    def _bxc(self):
        # bitwise XOR
        self._register_b = self._register_b ^ self._register_c
       
    def _out(self):
       self._set_combo_operand_value()
       self._output.append(str(self._operand % 8))

    def _bdv(self):
        self._set_combo_operand_value()
        self._register_b = self._register_a // pow(2,self._operand)
      
    def _cdv(self):
        self._set_combo_operand_value()
        self._register_c = self._register_a // pow(2,self._operand)           
        

def parse_input(input_data: str) -> tuple[list,int, int, int]:
    registers_str, program = input_data.split('\n\n', maxsplit=1)
    register_lines = registers_str.split('\n')
    a = int(register_lines[0].split(': ')[1])
    b = int(register_lines[1].split(': ')[1])
    c = int(register_lines[2].split(': ')[1])
    
    program = program.split(': ')[1]
    program = [int(x) for x in program.split(',')]
    
    logger.debug(f'initial register A: {a}')
    logger.debug(f'initial register B: {b}')
    logger.debug(f'initial register C: {c}')
    logger.debug(f'initial program: {program}')
    if not (a is not None and b is not None and c is not None and program):
        raise ValueError('Invalid input')
    
    return program, a, b, c
        

def solve_part_a(input_data: str) -> str:
    program, a, b, c = parse_input(input_data)
    # computer = ThreeBitComputer([2,6], register_c=9)
    # computer = ThreeBitComputer([5,0,5,1,5,4], register_a=10)
    # computer = ThreeBitComputer([0,1,5,4,3,0], register_a=2024)
    # computer = ThreeBitComputer([1,7], register_b=29)
    # computer = ThreeBitComputer([4,0], register_b=2024, register_c=43690)
    computer = ThreeBitComputer(program, register_a=a, register_b=b, register_c=c)
    computer.run_program()
    return computer.get_output()


def solve_part_b(input_data: str) -> str:
    program, _, _, _ = parse_input(input_data)
    computer = ThreeBitComputer(program)
    program_str = ','.join([str(x) for x in program])
    a: int = -1
    while  computer.get_output() != program_str:
        a = a + 1
        computer.reboot(register_a=a)
        computer.run_program()
    return str(a)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = 2024
    day = 17
    logger.info('🎄 Running puzzle day 17...')
    puzzle = Puzzle(year=year, day=day)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)

    return None

if __name__ == '__main__':
    main()
