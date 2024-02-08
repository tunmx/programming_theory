import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from urm_simulation import *

minus_instruct = Instructions(
            C(1, 4),        # 1
            J(3, 2, 14),    # 2
            J(5, 4, 10),    # 3
            S(5),           # 4
            J(5, 4, 9),     # 5
            S(5),           # 6
            S(0),           # 7
            J(0, 0, 5),     # 8
            Z(5),           # 9
            S(3),           # 10
            C(0, 4),        # 11
            Z(0),           # 12
            J(0, 0, 2),     # 13
            C(4, 6),        # 14

)


test = Instructions(
            C(1, 4),        # 1
            J(3, 2, 14),    # 2
            J(5, 4, 10),    # 3
            S(5),           # 4
            J(5, 4, 9),     # 5
            S(5),           # 6
            S(0),           # 7
            J(0, 0, 5),     # 8
            Z(5),           # 9
            S(3),           # 10
            C(0, 4),        # 11
            Z(0),           # 12
            J(0, 0, 2),     # 13
            C(4, 0),        # 14
)

def minus(x, y, safety_count=100000):
    num_of_registers = haddr(test) + 1
    registers = allocate(num_of_registers)
    input_nodes = {1: x, 2: y}
    result = forward(input_nodes, registers, test, safety_count=safety_count)
    for idx, reg in enumerate(result.registers_of_steps):
        command = result.ops_of_steps[idx]
        print(command)
        print(result.registers_of_steps[idx].summary())
        print()
    return result.last_registers[0]


if __name__ == '__main__':
    z = minus(3, 5)
    print(z)
