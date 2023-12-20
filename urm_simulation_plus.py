"""
Created by Jingyu Yan on 2023/12/19.
"""

import copy
from typing import List, Tuple, Generator


class Instructions(object):
    """
    'Instructions' represents a list of URM (Unlimited Register Machine) instructions.
    """

    def __init__(self, inst=None):
        if inst is None:
            inst = list()
        self.instructions = inst

    def __str__(self):
        return str(self.instructions)

    def summary(self):
        # Define the format for each row of the table
        row_format = "{:<5}\t{:<3}\t{:<4}\t{:<4}\t{:<7}\n"
        # Create a table header with lines
        header_line = '-' * 40
        table = row_format.format("Line", "Op", "Arg1", "Arg2", "Jump To") + header_line + '\n'

        # Iterate over the instructions and their indices
        for index, instruction in enumerate(self.instructions, 1):
            # Prepare args with empty strings for missing values
            args = [''] * 3
            # Fill the args list with actual values from the instruction
            for i, arg in enumerate(instruction[1:]):
                args[i] = str(arg)
            # Format each line as a row in the table
            line = row_format.format(index, instruction[0], *args)
            table += line

        return table

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
        normalized_instructions = Instructions()
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

    @staticmethod
    def relocation(instructions, alloc: Tuple[int]):
        if not isinstance(alloc, tuple) or len(alloc) != instructions.haddr() + 1:
            raise ValueError("invalid allocation")
        relocated_instructions = []
        for i in instructions:
            if i[0] == 'Z' or i[0] == 'S':
                relocated_instructions.append((i[0], alloc[i[1]]))
            elif i[0] == 'C':
                relocated_instructions.append((i[0], alloc[i[1]], alloc[i[2]]))
            elif i[0] == 'J':
                relocated_instructions.append((i[0], alloc[i[1]], alloc[i[2]], i[3]))
        return Instructions(relocated_instructions)


class Registers(object):
    """
    'Registers' represents a list of register values for a URM.
    """

    def __init__(self, lis: List[int]):
        for item in lis:
            if not isinstance(item, int):
                raise ValueError("All items in the list must be integers")
            if item < 0:
                raise ValueError("An integer greater than 0 must be entered")

        self.registers = lis

    def summary(self):
        headers = [f"R{i}" for i in range(len(self.registers))]
        divider = '-' * (len(headers) * 8 - 1)
        header_row = '\t'.join(headers)
        values_row = '\t'.join(map(str, self.registers))
        table = f"{header_row}\n{divider}\n{values_row}"
        return table

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
    def zero(registers: Registers, n: int) -> Registers:
        """
        Set the value of register number n to 0.
        """
        registers[n] = 0
        return registers

    @staticmethod
    def successor(registers: Registers, n: int) -> Registers:
        """
        Increment the value of register number n.
        """
        registers[n] += 1
        return registers

    @staticmethod
    def copy(registers: Registers, j: int, k: int) -> Registers:
        """
        Copy the value of register number j to register number k.
        """
        registers[k] = registers[j]
        return registers

    @staticmethod
    def jump(registers: Registers, m: int, n: int, q: int, current_line: int) -> int:
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

    @staticmethod
    def execute_instructions(instructions: Instructions, initial_registers: Registers, safety_count: int = 1000) -> Generator:
        """
        Execute a set of URM (Unlimited Register Machine) instructions.

        :param instructions: The set of URM instructions to execute.
        :param initial_registers: The initial state of the registers.
        :param safety_count: Maximum number of iterations to prevent infinite loops.
        :return: Generator yielding the state of the registers after each instruction.
        """
        registers = initial_registers
        exec_instructions = copy.deepcopy(instructions)
        exec_instructions.append(('END',))
        current_line = 0
        count = 0

        while current_line < len(exec_instructions):
            assert count < safety_count, "The number of cycles exceeded the safe number."

            instruction = exec_instructions[current_line]
            op = instruction[0]

            if op == 'Z':
                registers = URMSimulator.zero(registers, instruction[1])
                current_line += 1
            elif op == 'S':
                registers = URMSimulator.successor(registers, instruction[1])
                current_line += 1
            elif op == 'C':
                registers = URMSimulator.copy(registers, instruction[1], instruction[2])
                current_line += 1
            elif op == 'J':
                jump_result = URMSimulator.jump(registers, instruction[1], instruction[2], instruction[3], current_line)
                current_line = jump_result if jump_result != -1 else len(exec_instructions)
            elif op == 'END':
                break
            count += 1

            yield copy.deepcopy(registers), f"{current_line}: {op}" + "(" + ", ".join(map(str, instruction[1:])) + ")"

    def forward(self, safety_count: int = 1000, only_result=False):
        """
        Execute simulated URM (Unlimited Register Machine) operations;
        this is only a simulation and cannot achieve 'infinity'
        :param only_result: Return only register results.
        :param safety_count: Set a safe maximum number of computations to prevent the program from falling into an infinite loop (to protect my device).
        :return: Return all computation steps and description of instructions.
        """
        gen = URMSimulator.execute_instructions(self.instructions, self.initial_registers, safety_count)
        if not only_result:
            return gen
        reg = None
        for step, command in gen:
            reg = step
        return reg

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
    """
    URM Copy operation. Copies the value from one register to another.
    """
    pass


@urm_op
def J():
    """
    URM Jump operation. Jumps to a specified line if two registers hold the same value.
    """
    pass


@urm_op
def Z():
    """
    URM Zero operation. Sets the value of a register to zero.
    """
    pass


@urm_op
def S():
    """
    URM Successor operation. Increments the value of a register by one.
    """
    pass


_END = "END"  # Marker for the end of a URM program (used internally)


def size(instructions: Instructions) -> int:
    """
    Calculates the number of instructions in a URM program.

    :param instructions: An Instructions object representing a URM program.
    :return: The number of instructions in the program.
    """
    return len(instructions)


def haddr(instructions: Instructions) -> int:
    """
    Finds the highest register address used in a URM program.

    :param instructions: An Instructions object representing a URM program.
    :return: The highest register index used in the program.
    """
    return instructions.haddr()


def normalize(instructions: Instructions) -> Instructions:
    """
    Normalizes a URM program so that all jump operations target valid instruction lines.

    :param instructions: An Instructions object representing a URM program.
    :return: A new Instructions object with normalized jump targets.
    """
    return Instructions.normalize(instructions)


def concat(p: Instructions, q: Instructions) -> Instructions:
    """
    Concatenates two URM programs into a single program.

    :param p: An Instructions object representing the first URM program.
    :param q: An Instructions object representing the second URM program.
    :return: A new Instructions object with the concatenated program.
    """
    return Instructions.concatenation(p, q)


def reloc(instructions: Instructions, alloc: Tuple[int, ...]) -> Instructions:
    """
    Relocates the register addresses in a URM program according to a specified mapping.

    :param instructions: An Instructions object representing a URM program.
    :param alloc: A tuple defining the new register addresses for each original address.
    :return: A new Instructions object with relocated register addresses.
    """
    return Instructions.relocation(instructions, alloc)


def allocate(num: int) -> Registers:
    """
    Allocates a specified number of registers, initializing them with zero values.

    This function creates a new Registers object with a given number of registers.
    Each register is initialized with the value 0.

    :param num: The number of registers to allocate.
    :return: A Registers object with 'num' registers, each initialized to 0.
    """
    return Registers.allocate(num)
