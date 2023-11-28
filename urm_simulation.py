"""
Created by Jingyu Yan on 2023/11/25.
"""

import copy


class URM(object):
    """
    Implementation scheme for simulating an Unlimited Register Machine,
    realizing the computational logic of four types of instructions: zero, successor, copy, and jump.
    """

    @staticmethod
    def zero(registers, n):
        """
        Set the value of register number n to 0.
        """
        registers[n] = 0
        return registers

    @staticmethod
    def successor(registers, n):
        """
        Increment the value of register number n.
        """
        registers[n] += 1
        return registers

    @staticmethod
    def copy(registers, j, k):
        """
        Copy the value of register number j to register number k.
        """
        registers[k] = registers[j]
        return registers

    @staticmethod
    def jump(registers, m, n, q, current_line):
        """
        Jump to line 'q' if values in registers 'm' and 'n' are equal, else go to the next line.
        """
        if registers[m] == registers[n]:
            return q - 1  # Adjust for zero-based indexing
        else:
            return current_line + 1

    def __init__(self, instructions, initial_registers, ):
        """
        Initialize a URM (Unlimited Register Machine) model, requiring input of an instruction set and registers.
        :param instructions: Instruction set, constructed and passed in from outside.
        :param initial_registers: Registers, constructed and passed in from outside.
        """
        self.instructions = instructions
        self.initial_registers = initial_registers
        self.instructions.append(('END',))  # Include an exit instruction by default.
        for v in self.initial_registers:
            assert v >= 0, "Input must be a natural number"

    def forward(self, safety_count=1000):
        """
        Execute simulated URM (Unlimited Register Machine) operations;
        this is only a simulation and cannot achieve 'infinity'
        :param safety_count: Set a safe maximum number of computations to prevent the program from falling into an infinite loop (to protect my device).
        :return: Return all computation steps and description of instructions.
        """
        registers = self.initial_registers

        current_line = 0
        count = 0
        while current_line < len(self.instructions):
            assert count < safety_count, "The number of cycles exceeded the safe number."

            # Adjust current_line to align with the external indexing starting from 1.
            instruction = self.instructions[current_line]
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
