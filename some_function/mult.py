import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


from urm_simulation import *

class BuildMultiplication(object):
    """
    Title: URM Implements Primitive Recursion
    Requirement:
        the second of them takes a program for computing a function of n arguments and a program for computing
        a function of n+2 arguments and returns the program for computing their primitive recursion;
    Conclusion:
        In this case study, the computability feature of the URM was used to implement an example of a primitive
        recursive function, mul(x, y) = x * y, and relevant experimental tests were conducted.
    """

    def __init__(self):
        self.G_haddr = None
        self.func_add_L = [0]
        p1 = self.build_func_add()
        self.F_highest = haddr(p1)
        for i in range(1, 3):
            self.func_add_L.append(self.func_add_L[-1] + max(2, self.F_highest) + 1)
        self.L = [0, ]
        # Input nodes definition
        self.input_x_index = 3
        self.input_acc_index = 4
        self.input_n_index = 5
        # Output nodes definition
        self.output_x_index = 0
        self.output_acc_index = 1
        self.output_n_index = 2

    @staticmethod
    def build_func_add() -> Instructions:
        """
        A subfunction of a G function: add(x, y) = x + y
        :return: SUM(x, y) Instructions
        """
        return Instructions([
            C(2, 0),
            Z(2),
            J(1, 2, 0),
            S(0),
            S(2),
            J(0, 0, 3),
        ])

    @staticmethod
    def build_func_pre() -> Instructions:
        """
        A subfunction of a G function: pre(n) = n -1
        :return: PRE(n) Instructions
        """
        return Instructions([
            Z(0),
            J(0, 1, 0),
            S(2),
            J(1, 2, 8),
            S(0),
            S(2),
            J(0, 0, 4),
            Z(2),
        ])

    def build_G_func(self) -> Instructions:
        """
        The method constructs a URM program for the function G, corresponding to g(n+2), which primarily facilitates
        the recursive step in the primitive recursive function mul(x, y): acc = acc + x, n = n - 1.
        :return: Functions concatenation : ADD(x, acc) + PRE(n) Instructions
        """
        ori_add = self.build_func_add()

        ori_pre = self.build_func_pre()

        # concat add functions and pre functions
        G = ori_add.copy()
        concat_add_pre_alloc = tuple(range(self.func_add_L[1], self.func_add_L[2]))

        reloc_pre = reloc(ori_pre, concat_add_pre_alloc)
        G = G + reloc_pre

        return G

    def build_F_func(self) -> Instructions:
        """
        Define an f(n) function, where n is 1 in this example.
        The base case in multiply, when the multiplier is 0.
        :return: Z(L[input_acc_index], 0)
        """
        return Instructions(Z(self.input_acc_index))

    def build_p1(self) -> Instructions:
        """
        :return: f(n) -> F
        """
        return self.build_F_func()

    def build_p2(self) -> Instructions:
        """
        This approach constructs a standardized I/O module for the URM function G corresponding to the g(n+2) function
        in the example, building a complete set of input and output module instructions.
        :return: Input + recursive_step(n+2) + Output
        """
        G = self.build_G_func()
        # Build input nodes for G
        I = Instructions([
            J(self.func_add_L[0] + 2, 8, 0),  # if n = 0 than break
            C(self.func_add_L[0], self.func_add_L[0] + 4),  # input x index
            C(self.func_add_L[0] + 1, self.func_add_L[0] + 1 + 4),  # input acc index
            C(self.func_add_L[0] + 2, self.func_add_L[1] + 1 + 3),  # input n index
        ])

        G_highest = haddr(G)
        G_param_num = 3
        concat_I_and_G_alloc = tuple(range(G_param_num, G_highest + G_param_num + 1))

        IG = I + reloc(G, concat_I_and_G_alloc)

        # Build Output nodes for IG
        O_param_num = 3
        O = Instructions([
            C(3 + O_param_num, self.output_acc_index),
            C(4 + O_param_num, self.output_x_index),
            C(6 + O_param_num, self.output_n_index),
        ])

        # Concat
        IG_highest = haddr(IG)
        concat_O_and_IG_alloc = tuple(range(G_param_num, IG_highest + G_param_num + 1))
        # print(concat_O_and_IG_alloc)

        # Index_x->R3, Index_acc->R4, Index_n->R5;  Output_x->R0, Output_acc->R1， Output_n->R2
        IGO = reloc(IG, concat_O_and_IG_alloc) + O

        self.G_haddr = haddr(IGO)

        return IGO

    def build_p3(self) -> Instructions:
        """
        Recursive step: Copy the output of g(n+2) at time n into the input register position at n-1, preparing for
        the next recursive calculation.
        :return: C(output_x, input_x), C(output_acc, input_acc), C(output_n, input_n)
        """
        return Instructions([
            C(self.output_x_index, self.input_x_index),
            C(self.output_acc_index, self.input_acc_index),
            C(self.output_n_index, self.input_n_index),
        ])

    def build_loop(self) -> Instructions:
        """
        Add loop function to the tail of the function, judge the condition and jump instruction function.
        :return: J(output_n, last), J(0, 0, L_F+1)
        """
        return Instructions([J(self.output_n_index, self.G_haddr, 0), J(0, 0, self.F_highest)])

    def build_pipeline(self) -> Instructions:
        """
        The pipeline method is designed to construct URM instructions for the primitive recursive function
        mul(x, y) = x * y showcased in this example, composed of instruction sets P1, P2, P3, and LOOP.
        :return: MUL(x, y) Instructions.
        """
        # Step.1 Build the base case function: f(n)
        P1 = self.build_p1()
        # Step.2 Build the recursive step function: g(n+2)
        P2 = self.build_p2()
        # Step.3 Build calls the function recursively
        P3 = self.build_p3()
        # Step.4 Adds the loop function instruction to the function
        loop = self.build_loop()

        P = P1 + P2 + P3
        P.append(loop)

        return P


mul_instruct = Instructions(
    Z(4),
    J(5, 11, 6),
    C(3, 7),
    C(4, 8),
    C(5, 10),
    C(8, 6),
    Z(8),
    J(7, 8, 12),
    S(6),
    S(8),
    J(6, 6, 8),
    Z(9),
    J(9, 10, 20),
    S(11),
    J(10, 11, 19),
    S(9),
    S(11),
    J(9, 9, 15),
    Z(11),
    C(6, 1),
    C(7, 0),
    C(9, 2),
    C(0, 3),
    C(1, 4),
    C(2, 5),
    J(2, 11, 0),
    J(0, 0, 2)
)

def multiply(x, y, safety_count=10000):
    num_of_registers = haddr(mul_instruct) + 1
    registers = allocate(num_of_registers)
    input_nodes = {3: x, 5: y}
    result = forward(input_nodes, registers, mul_instruct, safety_count=safety_count)
    return result.last_registers[1]

if __name__ == '__main__':
    # mul = BuildMultiplication().build_pipeline()
    z = multiply(3, 6)
    print(z)

    obj = BuildMultiplication()
    obj.build_pipeline()
    print(obj.input_x_index, obj.input_n_index, obj.output_acc_index)
