import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from urm_simulation import *

"""
dist(x, y) = minus(x, y) + minus(y, x) 

input_R1: x, input_R2: y, output_R0: result
"""
minus_instruct = Instructions(
            C(1, 4),
            J(3, 2, 14),
            J(5, 4, 10),
            S(5),
            J(5, 4, 9),
            S(5),
            S(0),
            J(0, 0, 5),
            Z(5),
            S(3),
            C(0, 4),
            Z(0),
            J(0, 0, 2),
            C(4, 0),
)

def minus(x, y, safety_count=100000):
    num_of_registers = haddr(minus_instruct) + 1
    registers = allocate(num_of_registers)
    input_nodes = {1: x, 2: y}
    result = forward(input_nodes, registers, minus_instruct, safety_count=safety_count)
    return result.last_registers[0]


if __name__ == '__main__':
    z = minus(45, 20)
    print(z)
