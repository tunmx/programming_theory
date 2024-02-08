import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from urm_simulation import *

"""
gt(x, y) = 0 if x > y and gt(x, y) = 1 for other x and y
"""
gt_instruct_norm = Instructions(
    Z(0),  # 1

    # If either side is 0 first, it will enter the end game
    J(1, 0, 25),  # 2
    J(2, 0, 24),  # 3

    # R1 pred
    Z(3),  # 4
    J(3, 1, 25),  # 5
    S(4),  # 6
    J(1, 4, 11),  # 7
    S(3),  # 8
    S(4),  # 9
    J(0, 0, 7),  # 10
    C(3, 1),  # 11
    Z(4),  # 12

    # R2 pred
    Z(3),  # 13
    J(3, 2, 25),  # 14
    S(4),  # 15
    J(2, 4, 20),  # 16
    S(3),  # 17
    S(4),  # 18
    J(0, 0, 16),  # 19
    C(3, 2),  # 20
    Z(4),  # 21

    Z(3),  # 22
    J(0, 0, 2),  # 23

    S(0),  # 24
)

"""
gt(x, y) = 1 if x > y and gt(x, y) = 0 for other x and y
"""
gt_instruct = Instructions(
    S(0),  # 1

    # If either side is 0 first, it will enter the end game
    J(1, 0, 25),  # 3
    J(2, 0, 24),  # 2

    # R1 pred
    Z(3),  # 4
    J(3, 1, 25),  # 5
    S(4),  # 6
    J(1, 4, 11),  # 7
    S(3),  # 8
    S(4),  # 9
    J(0, 0, 7),  # 10
    C(3, 1),  # 11
    Z(4),  # 12

    # R2 pred
    Z(3),  # 13
    J(3, 2, 25),  # 14
    S(4),  # 15
    J(2, 4, 20),  # 16
    S(3),  # 17
    S(4),  # 18
    J(0, 0, 16),  # 19
    C(3, 2),  # 20
    Z(4),  # 21

    Z(3),  # 22
    J(0, 0, 2),  # 23

    Z(0),  # 24
)



def gt(x, y, safety_count=10000):
    num_of_registers = haddr(gt_instruct) + 1
    registers = allocate(num_of_registers)
    input_nodes = {1: x, 2: y}
    result = forward(input_nodes, registers, gt_instruct, safety_count=safety_count)
    for idx, reg in enumerate(result.registers_of_steps):
        command = result.ops_of_steps[idx]
        print(command)
        print(result.registers_of_steps[idx].summary())
        print()
    return result.last_registers[0]


if __name__ == '__main__':
    z = gt(6, 5)
    print(z)
