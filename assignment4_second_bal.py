from urm_simulation import *
import numpy as np


class SingletonSecond(object):

    def __init__(self):
        pass

    def build_G_func(self):
        ori_add = Instructions([
            C(2, 0),
            Z(2),
            J(1, 2, 0),
            S(0),
            S(2),
            J(0, 0, 3),
        ])

        ori_pre = Instructions([
            Z(0),
            J(0, 1, 0),
            S(2),
            J(1, 2, 8),
            S(0),
            S(2),
            J(0, 0, 4),
            Z(2),
        ])

        # Concat add functions and pre functions
        G = ori_add.copy()
        add_highest = haddr(ori_add)
        add_param_num = 2
        add_L1 = 0
        add_L2 = add_L1 + max(add_param_num, add_highest + 1)
        add_L3 = add_L2 + max(add_param_num, add_highest + 1)
        concat_add_pre_alloc = tuple(range(add_L2, add_L3))
        # print(add_L1)
        # print(add_L2)
        # print(add_L3)

        reloc_pre = reloc(ori_pre, concat_add_pre_alloc)
        G = G + reloc_pre
        # print(G)

        # Build input nodes for G
        I = Instructions([
            C(add_L1, add_L1 + 4),  # input x index
            C(add_L1 + 1, add_L1 + 1 + 4),  # input acc index
            C(add_L1 + 2, add_L2 + 1 + 3),  # input n index
        ])
        # print("I: ", I)
        G_highest = haddr(G)
        G_param_num = 3
        concat_I_and_G_alloc = tuple(range(G_param_num, G_highest + G_param_num + 1))
        # print(concat_I_and_G_alloc)
        IG = I + reloc(G, concat_I_and_G_alloc)
        # print(IG)

        # Build Output nodes for IG
        O_param_num = 3
        O = Instructions([
            C(3 + O_param_num, 1),
            C(4 + O_param_num, 0),
            C(6 + O_param_num, 2),
        ])
        # print(O)

        # Add
        IG_highest = haddr(IG)
        concat_O_and_IG_alloc = tuple(range(G_param_num, IG_highest + G_param_num + 1))
        # print(concat_O_and_IG_alloc)

        # Index_x->R3, Index_acc->R4, Index_n->R5;  Output_x->R0, Output_acc->R1， Output_n->R2
        IGO = reloc(IG, concat_O_and_IG_alloc) + O
        # print(IGO)

        return IGO

    def test_G(self, G):

        registers = allocate(haddr(G) + 1)
        # input param
        input_x = 3
        input_acc = 4
        input_n = 5
        # output
        output_x = 0
        output_acc = 1
        output_n = 2
        param = {input_x: 3, input_acc: 0, input_n: 5}

        # STEP 1
        result = forward(param, registers, G, safety_count=100)

        for idx, reg in enumerate(result.registers_of_steps):
            command = result.ops_of_steps[idx]
            print(reg, command)
        last = result.last_registers
        # print(f"input_x->R{input_x} = {x}")
        # print(f"input_acc->R{input_acc} = {acc}")
        # print(f"input_n->R{input_n} = {n}")
        print(f"post-execution: x: {last[output_x]}, acc: {last[output_acc]}, n: {last[output_n]}")

        # STEP 2
        param = {
            input_x: last[output_x],
            input_acc: last[output_acc],
            input_n: last[output_n]
          }
        result = forward(param, last, G, safety_count=100)
        for idx, reg in enumerate(result.registers_of_steps):
            command = result.ops_of_steps[idx]
            print(reg, command)


        last = result.last_registers
        # print(f"input_x->R{input_x} = {x}")
        # print(f"input_acc->R{input_acc} = {acc}")
        # print(f"input_n->R{input_n} = {n}")
        print(f"post-execution: x: {last[output_x]}, acc: {last[output_acc]}, n: {last[output_n]}")


    def build_F_func(self):
        F = Instructions(Z(4))
        return F

    def build_CP_func(self):
        CP = Instructions([
            C(0, 3),
            C(1, 4),
            C(2, 5),
        ])
        return CP

    def build_P(self):
        G = self.build_G_func()
        F = self.build_F_func()


        last = haddr(G)

        # CHECK = Instructions(J(3, last, 0))

        FG = F + G
        loop = size(F) + 1
        print(loop)

        CP = self.build_CP_func()

        RECUR = Instructions([J(2, last, 0), J(0, 0, loop)])

        P = FG + CP
        P.append(RECUR)
        print(P)


        return P



if __name__ == '__main__':
   s = SingletonSecond()
   # G = s.build_G_func()
   # s.test_G(G)
   P = s.build_P()
   registers = allocate(haddr(P) + 1)
   input_x = 3
   input_n = 5

   param = {input_x: 4, input_n: 3}
   result = forward(param, registers, P, safety_count=150)

   for idx, reg in enumerate(result.registers_of_steps):
       command = result.ops_of_steps[idx]
       print(reg, command)
