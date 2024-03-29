import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from urm_simulation import *


sg_instruct = Instructions(
    Z(2),
    J(1, 2, 4),
    S(0),
)

def sg(x, safety_count=10000):
    num_of_registers = haddr(sg_instruct) + 1
    registers = allocate(num_of_registers)
    input_nodes = {1: x}
    result = forward(input_nodes, registers, sg_instruct, safety_count=safety_count)
    return result.last_registers[0]

if __name__ == '__main__':
    print(f'sg(0)={sg(0)}')
    print(f'sg(10086)={sg(10086)}')
