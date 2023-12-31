import random

from urm_simulation import *
from assignment4_second import SingletonSecond


def example_function(a, x, b):
    return a * x + b  # linear


def build_linear():
    # ax + b = y
    # Build inputs nodes for linear function
    s2 = SingletonSecond()
    multiply_instructions = s2.build_pipeline()
    add_instructions = Instructions([
        C(2, 0),
        Z(2),
        J(1, 2, 0),
        S(0),
        S(2),
        J(0, 0, 3),
    ])
    mul_highest = haddr(multiply_instructions)

    mul_end = mul_highest + 1
    add_end = mul_end + haddr(add_instructions)
    add_loc = tuple(range(mul_end, add_end + 1))
    # print(add_loc)
    reloc_add = reloc(add_instructions, add_loc)
    # print(reloc_add)

    linear_block = multiply_instructions + Instructions(C(s2.output_acc_index, mul_highest + 2)) + reloc_add

    IO_placeholder = 4
    linear_highest = haddr(linear_block)
    linear_loc = tuple(range(IO_placeholder, linear_highest + IO_placeholder + 1))
    reloc_linear = reloc(linear_block, linear_loc)

    IO = Instructions([
        C(1, IO_placeholder + s2.input_x_index),  # Copy param 'a' to mul block's param 'x'
        C(2, IO_placeholder + s2.input_n_index),  # Copy param 'x' to mul block's param 'n'
        C(3, IO_placeholder + mul_highest + 3),  # Copy param 'b' to add block's param 'y'
    ])

    linear = IO + reloc_linear + Instructions(C(IO_placeholder + mul_highest + 1, 0))

    return linear


def linear_urm(P, a, x, b):
    registers = allocate(haddr(P) + 1)

    result = forward({1: a, 2: x, 3: b}, registers, P,
                     safety_count=100000)
    for idx, reg in enumerate(result.registers_of_steps):
        command = result.ops_of_steps[idx]
        print(reg, command)
    last = result.last_registers

    return last[0]



linear_urm(build_linear(), 1, 2, 3)

# def check():
#     linear_instructions = build_linear()
#     num_range = (0, 50)
#     num_triplet = 10
#     triplet_list = [(random.randint(*num_range), random.randint(*num_range), random.randint(*num_range)) for _ in
#                     range(num_triplet)]
#     for a, x, b in triplet_list:
#         assert example_function(a, x, b) == linear_urm(linear_instructions, a, x, b), f"Result error."
#     print("Pass test")
#
#
# check()
