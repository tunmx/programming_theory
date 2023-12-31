from urm_simulation import *
from assignment4_second import SingletonSecond


class SingletonThird(object):

    def __init__(self):
        self.input_target = None
        self.input_b = None
        self.input_a = None
        self.output_x = None
        self.output_n = None

    @staticmethod
    def build_add() -> Instructions:
        return Instructions(
            C(2, 0),
            Z(2),
            J(1, 2, 0),
            S(0),
            S(2),
            J(0, 0, 3),
        )

    @staticmethod
    def build_pre() -> Instructions:
        return Instructions(
            Z(0),
            J(0, 1, 0),
            S(2),
            J(1, 2, 8),
            S(0),
            S(2),
            J(0, 0, 4),
            Z(2),
        )

    @staticmethod
    def build_greater_than_or_equal() -> Instructions:
        return Instructions(
            Z(0),  # 1

            J(2, 0, 24),  # 2
            J(1, 0, 25),  # 3

            Z(3),  # 4
            J(3, 1, 25),  # 5
            S(4),  # 6
            J(1, 4, 11),  # 7
            S(3),  # 8
            S(4),  # 9
            J(0, 0, 7),  # 10
            C(3, 1),  # 11
            Z(4),  # 12

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

    @staticmethod
    def build_linear():
        # Multiply() using Singleton2's original recursive function
        s2 = SingletonSecond()
        multiply_instructions = s2.build_pipeline()
        add_instructions = SingletonThird.build_add()

        # Ready to build
        mul_highest = haddr(multiply_instructions)
        mul_end = mul_highest + 1
        add_end = mul_end + haddr(add_instructions)
        add_new_loc = tuple(range(mul_end, add_end + 1))
        reloc_add = reloc(add_instructions, add_new_loc)
        # Build linear computable block
        linear_block = multiply_instructions + Instructions(C(s2.output_acc_index, mul_highest + 2)) + reloc_add

        # Build to add input and output modules for linear
        IO_placeholder = 4
        linear_highest = haddr(linear_block)
        linear_loc = tuple(range(IO_placeholder, linear_highest + IO_placeholder + 1))
        reloc_linear_block = reloc(linear_block, linear_loc)

        # Input nodes: Copy the placeholder parameter to the linear_block input parameter location
        I = Instructions([
            C(1, IO_placeholder + s2.input_x_index),  # Copy param 'a' to mul block's param 'x'
            C(2, IO_placeholder + s2.input_n_index),  # Copy param 'x' to mul block's param 'n'
            C(3, IO_placeholder + mul_highest + 3),  # Copy param 'b' to add block's param 'y'
        ])
        # Output nodes: Copy the linear_block output to index 0
        O = Instructions(C(IO_placeholder + mul_highest + 1, 0))

        # Build the final linear function: linear(a, x, b) = a * x + b
        linear = I + reloc_linear_block + O

        return linear

    def build_pipeline(self):
        # Build each sub-module
        linear = SingletonThird.build_linear()  # f(n) has 3 param
        greater_than_or_equal = SingletonThird.build_greater_than_or_equal()
        # Build computes the minimization function [Inputs, n, target, linear, greater_than, acc+=1, loop]
        # Prepare
        prepare_n_target = Instructions(Z(1), )
        h_linear = haddr(linear)
        reloc_range = tuple(range(haddr(prepare_n_target) + 1, h_linear + haddr(prepare_n_target) + 2))
        linear_reloc = reloc(linear, reloc_range)
        out_from_linear_reloc_loc = haddr(prepare_n_target) + 1
        a_from_linear_reloc_loc = haddr(prepare_n_target) + 2
        x_from_linear_reloc_loc = haddr(prepare_n_target) + 3
        b_from_linear_reloc_loc = haddr(prepare_n_target) + 4

        G1 = prepare_n_target + Instructions(C(1, x_from_linear_reloc_loc)) + linear_reloc
        h_G1 = haddr(G1)
        h_gtoe = haddr(greater_than_or_equal)
        gtoe_loc = h_G1 + 1
        reloc_gtoe_range = tuple(range(gtoe_loc, gtoe_loc + h_gtoe + 1))
        gtoe_reloc = reloc(greater_than_or_equal, reloc_gtoe_range)
        glue_copy_value_to_gtoe = Instructions(C(out_from_linear_reloc_loc, gtoe_loc + 1), C(0, gtoe_loc + 2))

        G2 = G1 + glue_copy_value_to_gtoe + gtoe_reloc

        size_G2 = size(G2)

        LOOP_pre_size = 6
        LOOP = Instructions(
            Z(gtoe_loc + 5),
            S(gtoe_loc + 5),
            J(gtoe_loc, gtoe_loc + 5, size_G2 + LOOP_pre_size),
            S(1),
            J(0, 0, 2)
        )
        G2.append(LOOP)

        self.output_n = 1
        self.output_x = 2
        self.input_a = a_from_linear_reloc_loc
        self.input_b = b_from_linear_reloc_loc
        self.input_target = 0

        return G2


s3 = SingletonThird()
G = s3.build_pipeline()

registers = allocate(haddr(G) + 1)

a, b, target = 3, 5, 34
result = forward({s3.input_a: a, s3.input_b: b, s3.input_target: target}, registers, G, safety_count=10000000)

for idx, reg in enumerate(result.registers_of_steps):
    command = result.ops_of_steps[idx]
    print(reg, command)
last = result.last_registers
print(last[s3.output_n])

