from urm_simulation import *
import numpy as np


class SingletonSecond(object):

    def __init__(self):
        self.func_add_L = [0]
        add_highest = haddr(self.build_func_add())
        for i in range(1, 3):
            self.func_add_L.append(self.func_add_L[-1] + max(2, add_highest) + 1)

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
        # add_highest = haddr(ori_add)
        # add_param_num = 2
        # add_L1 = 0
        # add_L2 = add_L1 + max(add_param_num, add_highest + 1)
        # add_L3 = add_L2 + max(add_param_num, add_highest + 1)
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
            C(3 + O_param_num, 1),
            C(4 + O_param_num, 0),
            C(6 + O_param_num, 2),
        ])

        # Concat
        IG_highest = haddr(IG)
        concat_O_and_IG_alloc = tuple(range(G_param_num, IG_highest + G_param_num + 1))
        # print(concat_O_and_IG_alloc)

        # Index_x->R3, Index_acc->R4, Index_n->R5;  Output_x->R0, Output_acc->R1， Output_n->R2
        IGO = reloc(IG, concat_O_and_IG_alloc) + O
        # print(IGO)

        return IGO

    def build_F_func(self):
        F = Instructions(Z(4))
        return F

    def build_p3(self):
        CP = Instructions([
            C(0, 3),
            C(1, 4),
            C(2, 5),
        ])
        return CP

    def pipeline(self):
        P2 = self.build_p2()
        P1 = self.build_p1()

        # P2
        FG = P1 + P2
        loop = size(P1) + 1
        print(loop)

        CP = self.build_p3()

        last = haddr(FG)
        RECUR = Instructions([J(2, last, 0), J(0, 0, loop)])

        # P3
        P = FG + CP
        PP = P.copy()

        P.append(RECUR)
        print(P)

        print(PP + RECUR)

        return P


if __name__ == '__main__':
    s = SingletonSecond()
    # G = s.build_G_func()
    # s.test_G(G)
    P = s.pipeline()
    # registers = allocate(haddr(P) + 1)
    # input_x = 3
    # input_n = 5
    #
    # param = {input_x: 4, input_n: 3}
    # result = forward(param, registers, P, safety_count=150)
    #
    # for idx, reg in enumerate(result.registers_of_steps):
    #     command = result.ops_of_steps[idx]
    #     print(reg, command)
