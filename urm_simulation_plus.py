"""
Created by Jingyu Yan on 2023/12/19.
"""

import copy
from typing import List, Tuple


class Instructions(object):

    def __init__(self, inst: List[Tuple]):
        self.instructions = inst

    def __str__(self):
        return str(self.instructions)

    def __getitem__(self, index):
        return self.instructions[index]

    def __setitem__(self, index, value):
        if not isinstance(value, tuple):
            raise ValueError("Type error.")
        self.instructions[index] = value

    def __iter__(self):
        return iter(self.instructions)

    def __len__(self):
        return len(self.instructions)

    def append(self, item):
        self.instructions.append(item)

    def haddr(self):
        highest_register = -1
        for instruction in self.instructions:
            op = instruction[0]
            if op in ['Z', 'S']:  # These instructions involve only one register
                highest_register = max(highest_register, instruction[1])
            elif op in ['C', 'J']:  # These instructions involving two registers
                highest_register = max(highest_register, instruction[1], instruction[2])
        return highest_register if highest_register >= 0 else None

    @staticmethod
    def normalize(instructions):
        normalized_instructions = []
        for instruction in instructions:
            if instruction[0] == 'J':  # Check if it's a jump instruction
                m, n, k = instruction[1], instruction[2], instruction[3]
                if not 1 <= k <= len(instructions):  # Check if k is out of range
                    k = len(instructions) + 1  # Set k to n + 1
                normalized_instructions.append(('J', m, n, k))
            else:
                normalized_instructions.append(instruction)

        return normalized_instructions

    @staticmethod
    def concatenation(p1, p2):
        if not p1.instructions:  # P is empty
            return Instructions(p2)
        else:
            # Normalize P and obtain P' = I'1 ... I'n
            normalized_p1 = Instructions.normalize(p1)
            n = len(normalized_p1)

            # Prepare the concatenated instructions list with normalized P
            concatenated = normalized_p1[:]

            # Process Q and adjust the jump instructions
            for instruction in p2:
                if instruction[0] == 'J':  # It's a jump instruction
                    # If I_k = J(k, l, q) then change I_k with I'_k = J(k, l, q+n)
                    k, l, q = instruction[1], instruction[2], instruction[3]
                    if q != 0:  # We don't adjust if q is 0 (means jump to start)
                        q += n
                    concatenated.append(('J', k, l, q))
                else:
                    # Non-jump instructions remain the same
                    concatenated.append(instruction)

            return Instructions(concatenated)

def size(instructions: Instructions):
    return len(instructions)


def haddr(instructions: Instructions):
    return instructions.haddr()


def normalize(instructions: Instructions):
    return Instructions.normalize(instructions)


def concatenation(p: Instructions, q: Instructions):
    return Instructions.concatenation(p, q)

class Registers(object):

    def __init__(self, lis: List[int]):
        for item in lis:
            if not isinstance(item, int):
                raise ValueError("All items in the list must be integers")
            if item < 0:
                raise ValueError("An integer greater than 0 must be entered")

        self.registers = lis

    def __str__(self):
        return str(self.registers)

    def __getitem__(self, index):
        return self.registers[index]

    def __setitem__(self, index, value):
        if not isinstance(value, int):
            raise ValueError("Only integers can be assigned")
        if value < 0:
            raise ValueError("An integer greater than 0 must be entered")
        self.registers[index] = value

    def __len__(self):
        return len(self.registers)

    @staticmethod
    def allocate(num: int):
        r = [0 for _ in range(num)]
        reg = Registers(r)
        return reg


class URMSimulator(object):
    """
    Implementation scheme for simulating an Unlimited Register Machine,
    realizing the computational logic of four types of instructions: zero, successor, copy, and jump.
    """

    @staticmethod
    def zero(registers: Registers, n: int):
        """
        Set the value of register number n to 0.
        """
        registers[n] = 0
        return registers

    @staticmethod
    def successor(registers: Registers, n: int):
        """
        Increment the value of register number n.
        """
        registers[n] += 1
        return registers

    @staticmethod
    def copy(registers: Registers, j: int, k: int):
        """
        Copy the value of register number j to register number k.
        """
        registers[k] = registers[j]
        return registers

    @staticmethod
    def jump(registers: Registers, m: int, n: int, q: int, current_line: int):
        """
        Jump to line 'q' if values in registers 'm' and 'n' are equal, else go to the next line.
        """
        if registers[m] == registers[n]:
            return q - 1  # Adjust for zero-based indexing
        else:
            return current_line + 1

    def __init__(self, instructions: Instructions, initial_registers: Registers, ):
        """
        Initialize a URM (Unlimited Register Machine) model, requiring input of an instruction set and registers.
        :param instructions: Instruction set, constructed and passed in from outside.
        :param initial_registers: Registers, constructed and passed in from outside.
        """
        self.instructions = instructions
        self.initial_registers = initial_registers
        for v in self.initial_registers:
            assert v >= 0, "Input must be a natural number"

    def forward(self, safety_count: int = 1000):
        """
        Execute simulated URM (Unlimited Register Machine) operations;
        this is only a simulation and cannot achieve 'infinity'
        :param safety_count: Set a safe maximum number of computations to prevent the program from falling into an infinite loop (to protect my device).
        :return: Return all computation steps and description of instructions.
        """
        registers = self.initial_registers
        exec_instructions = copy.deepcopy(self.instructions)
        exec_instructions.append(('END',))  # Include an exit instruction by default.
        current_line = 0
        count = 0
        while current_line < len(self.instructions):
            assert count < safety_count, "The number of cycles exceeded the safe number."

            # Adjust current_line to align with the external indexing starting from 1.
            instruction = exec_instructions[current_line]
            op = instruction[0]

            # Construct a description of the current instruction.
            instruction_str = f"{current_line + 1}: {op}" + "(" + ", ".join(map(str, instruction[1:])) + ")"

            if op == 'Z':
                registers = self.zero(registers, instruction[1])
                current_line += 1
            elif op == 'S':
                registers = self.successor(registers, instruction[1])
                current_line += 1
            elif op == 'C':
                registers = self.copy(registers, instruction[1], instruction[2])
                current_line += 1
            elif op == 'J':
                jump_result = self.jump(registers, instruction[1], instruction[2], instruction[3], current_line)
                if jump_result == -1:  # If the result of the jump is -1, then terminate the program.
                    break
                else:
                    current_line = jump_result
            elif op == 'END':
                break  # Terminate the program.
            count += 1

            # Use a generator to return the state of the registers and the current instruction.
            yield copy.deepcopy(registers), instruction_str

    def __call__(self, *args, **kwargs):
        """
        Forward
        """
        return self.forward(*args, **kwargs)


def urm_op(func):
    """
    Decorator to convert the function to op.
    """

    def wrapper(*args):
        function_name = func.__name__
        return (function_name, *args)

    return wrapper


@urm_op
def C():
    pass


@urm_op
def J():
    pass


@urm_op
def Z():
    pass


@urm_op
def S():
    pass


_END = "END"  # op: end (private)
