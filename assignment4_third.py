from urm_simulation import *
from assignment4_second import SingletonSecond
from typing import Callable


class Minimization(object):

    @staticmethod
    def minimization(f: Callable, *fixed_args, min_condition=lambda x: x == 0) -> int:
        """
        Find the smallest integer satisfying the given condition.
        """
        n = 0
        while True:
            result = f(*fixed_args, n)
            if min_condition(result):
                return n
            n += 1

    @staticmethod
    def example_function(a, b, x) -> int:
        """
        Example function for demonstrating minimization.
        """
        return a * x + b

    @staticmethod
    def run_example(a, b, target) -> int:
        """
        Run an example minimization and return the result.
        """
        return Minimization.minimization(Minimization.example_function, a, b,
                                         min_condition=lambda output: output >= target)


class SingletonThird(object):
    """
    Title: Minimization of URM Computable Function
    Requirement:
        The third of them takes a program for computing a function of n+1 arguments and returns its minimization.
    Conclusion:
         I'm attempting to use a linear function and assuming it is monotonically increasing only under natural numbers
         to perform a search for a minimization function. I have some doubts about my example, as I'm not sure if this
         approach meets the requirements of the assignment.
    """

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
    def build_greater_than_or_equal() -> Instructions:
        """
        Construct an instruction to compare two numbers for greater than or equal to, where R0 stores the comparison result,
         1 for True, 0 for False. The comparison process is: R1 >= R2.
        """
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
    def build_linear() -> Instructions:
        """
        When using only natural numbers, a URM instruction set can be designed for a linear function "ax + b" that is
        always either monotonically increasing or constant. This is because:

        If "a" is greater than 0, the function increases as "x" increases.
        If "a" is 0, the function remains constant, regardless of "x".
        Since natural numbers don't include negatives, "ax + b" cannot be monotonically decreasing when "a" is a natural number.
        :return:
        """
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

    def build_pipeline(self) -> Instructions:
        """
        Construct a minimization program for computing a function with "n+1" parameters. For this purpose,
        we choose a linear function "ax + b" as the target function. The goal is to set the (n+1)th parameter as
        the target value and use the program to find the smallest value of "x" that is greater than or equal to this
        target value. This value of "x" will be the output of the function's minimization.
        """
        # Prepare each sub-module
        linear = SingletonThird.build_linear()  # f(a, b, x)
        greater_than_or_equal = SingletonThird.build_greater_than_or_equal()
        # Prepare to build the minimization function
        prepare_n_target = Instructions(Z(1), )
        h_linear = haddr(linear)
        reloc_range = tuple(range(haddr(prepare_n_target) + 1, h_linear + haddr(prepare_n_target) + 2))
        linear_reloc = reloc(linear, reloc_range)
        out_from_linear_reloc_loc = haddr(prepare_n_target) + 1
        # Remarks the inputs nodes
        a_from_linear_reloc_loc = haddr(prepare_n_target) + 2
        x_from_linear_reloc_loc = haddr(prepare_n_target) + 3
        b_from_linear_reloc_loc = haddr(prepare_n_target) + 4

        # Build the glue input module for linear
        G1 = prepare_n_target + Instructions(C(1, x_from_linear_reloc_loc)) + linear_reloc
        h_G1 = haddr(G1)
        h_gtoe = haddr(greater_than_or_equal)
        gtoe_loc = h_G1 + 1
        reloc_gtoe_range = tuple(range(gtoe_loc, gtoe_loc + h_gtoe + 1))
        gtoe_reloc = reloc(greater_than_or_equal, reloc_gtoe_range)
        # Build the computational module for determining greater than or equal
        glue_copy_value_to_gtoe = Instructions(C(out_from_linear_reloc_loc, gtoe_loc + 1), C(0, gtoe_loc + 2))

        # Build computes the minimization function
        G2 = G1 + glue_copy_value_to_gtoe + gtoe_reloc

        size_G2 = size(G2)

        # Loop blocks budget size
        LOOP_pre_size = 6
        LOOP = Instructions(
            Z(gtoe_loc + 5),
            S(gtoe_loc + 5),
            J(gtoe_loc, gtoe_loc + 5, size_G2 + LOOP_pre_size),
            S(1),       # n++
            J(0, 0, 2)
        )
        G2.append(LOOP)

        # Setting up the I/O nodes
        self.output_n = 1
        self.output_x = 2
        self.input_a = a_from_linear_reloc_loc
        self.input_b = b_from_linear_reloc_loc
        self.input_target = 0

        return G2

    def find(self, a, b, target):
        """
        Find the minimization function given input parameters.
        """
        P = self.build_pipeline()
        registers = allocate(haddr(P) + 1)

        result = forward({self.input_a: a, self.input_b: b, self.input_target: target}, registers, P,
                         safety_count=10000000)

        last = result.last_registers[self.output_n]

        return last


if __name__ == '__main__':
    s3 = SingletonThird()
    a = 7
    b = 4
    target = 61
    calculated = s3.find(a, b, target)
    expected = Minimization.run_example(a, b, target)
    assert expected == calculated, "Error result."

    print(f"Found! The smallest x for which linear function {a}x+{b} >= {target} meets the condition is x = {calculated}")
