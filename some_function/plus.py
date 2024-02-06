import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from urm_simulation import *

plus_instruct = Instructions(
    C(2, 0),  # copy R2 to R0
    Z(2),  # set R2 to zero
    J(1, 2, 0),  # if R1 == R2 then break
    S(0),  # R0++
    S(2),  # R2++
    J(3, 3, 3),  # into loop
)


def plus(x, y, safety_count=1000):
    num_of_registers = haddr(plus_instruct) + 1
    registers = allocate(num_of_registers)
    input_nodes = {1: x, 2: y}
    result = forward(input_nodes, registers, plus_instruct, safety_count=safety_count)
    return result.last_registers[0]


if __name__ == '__main__':
    z = plus(10, 20)
    print(z)
