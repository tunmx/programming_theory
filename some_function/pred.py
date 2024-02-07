import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from urm_simulation import *

pred_instruct = Instructions(
    J(0, 1, 0),
    S(2,),
    J(1, 2, 0),
    S(0),
    S(2),
    J(0, 0, 3)
)

def pred(x, safety_count=10000):
    num_of_registers = haddr(pred_instruct) + 1
    registers = allocate(num_of_registers)
    input_nodes = {1: x}
    result = forward(input_nodes, registers, pred_instruct, safety_count=safety_count)
    return result.last_registers[0]

if __name__ == '__main__':
    y = pred(34)
    print(y)