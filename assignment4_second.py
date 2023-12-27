import random

from urm_simulation import *
import numpy as np


class MulRecursive(object):
    @staticmethod
    def base_case(x):
        return 0

    @staticmethod
    def recursive_step(acc, x, n):
        if n == 0:
            return acc
        else:
            return MulRecursive.recursive_step(acc + x, x, n - 1)

    @staticmethod
    def multiply(x, y):
        return MulRecursive.recursive_step(MulRecursive.base_case(x), x, y, )


class SingletonSecond(object):

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

    def build_G_func(self):
        ori_add = self.build_func_add()

        ori_pre = self.build_func_pre()

        # Concat add functions and pre functions
        G = ori_add.copy()
        concat_add_pre_alloc = tuple(range(self.func_add_L[1], self.func_add_L[2]))

        reloc_pre = reloc(ori_pre, concat_add_pre_alloc)
        G = G + reloc_pre

        return G

    def build_p1(self) -> Instructions:
        return self.build_F_func()

    def build_p2(self):
        G = self.build_G_func()
        # Build input nodes for G
        I = Instructions([
            C(self.func_add_L[0], self.func_add_L[0] + 4),  # input x index
            C(self.func_add_L[0] + 1, self.func_add_L[0] + 1 + 4),  # input acc index
            C(self.func_add_L[0] + 2, self.func_add_L[1] + 1 + 3),  # input n index
        ])

        # P1 ↓
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

    def build_F_func(self):
        F = Instructions(Z(self.input_acc_index))
        return F

    def build_p3(self):
        CP = Instructions([
            C(self.output_x_index, self.input_x_index),
            C(self.output_acc_index, self.input_acc_index),
            C(self.output_n_index, self.input_n_index),
        ])
        return CP

    def build_p4(self):
        return Instructions([J(2, self.G_haddr, 0), J(0, 0, self.F_highest)])

    def pipeline(self):
        P1 = self.build_p1()
        P2 = self.build_p2()
        P3 = self.build_p3()
        P4 = self.build_p4()

        P = P1 + P2 + P3
        P.append(P4)

        return P

    def run(self, x, n):
        P = self.pipeline()
        print(P)
        registers = allocate(haddr(P) + 1)

        param = {self.input_x_index: x, self.input_n_index: n}
        result = forward(param, registers, P, safety_count=100000)

        for idx, reg in enumerate(result.registers_of_steps):
            command = result.ops_of_steps[idx]
            print(reg, command)
        last = result.last_registers

        print(f"{param[self.input_n_index]} * {param[self.input_x_index]} = {last[self.output_acc_index]}")


if __name__ == '__main__':
    singleton2 = SingletonSecond()
    singleton2.run(32, 6)

