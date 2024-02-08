import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from urm_simulation import *

"""
max(x, y) is the maximum of x and y
"""
max_instruct = Instructions(
    Z(6),     # 1
    C(2, 0),  # 2
    C(1, 5),    # 3

    J(2, 6, 26),  # 4
    J(1, 6, 27),  # 5

    Z(3),  # 6
    J(3, 1, 27),  # 7
    S(4),  # 8
    J(1, 4, 13),  # 9
    S(3),  # 10
    S(4),  # 11
    J(0, 0, 9),  # 12
    C(3, 1),  # 13
    Z(4),  # 14

    Z(3),  # 15
    J(3, 2, 27),  # 16
    S(4),  # 17
    J(2, 4, 22),  # 18
    S(3),  # 19
    S(4),  # 20
    J(0, 0, 18),  # 21
    C(3, 2),  # 22
    Z(4),  # 23

    Z(3),  # 24
    J(0, 0, 4),  # 25

    C(5, 0),  # 26
)



def urm_max(x, y, safety_count=10000):
    num_of_registers = haddr(max_instruct) + 1
    registers = allocate(num_of_registers)
    input_nodes = {1: x, 2: y}
    result = forward(input_nodes, registers, max_instruct, safety_count=safety_count)
    for idx, reg in enumerate(result.registers_of_steps):
        command = result.ops_of_steps[idx]
        print(command)
        print(result.registers_of_steps[idx].summary())
        print()
    return result.last_registers[0]


if __name__ == '__main__':
    z = urm_max(1, 3)
    print(z)
