import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from urm_simulation import *


isg_instruct = Instructions(
    S(0),
    Z(2),
    J(1, 2, 5),
    Z(0),
)

def isg(x, safety_count=10000):
    num_of_registers = haddr(isg_instruct) + 1
    registers = allocate(num_of_registers)
    input_nodes = {1: x}
    result = forward(input_nodes, registers, isg_instruct, safety_count=safety_count)
    return result.last_registers[0]

if __name__ == '__main__':
    print(f'isg(0)={isg(0)}')
    print(f'isg(10086)={isg(10086)}')