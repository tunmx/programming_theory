from urm_simulation import *


class SingletonFirst(object):

    def __init__(self, m: int):
        # sub(x, y) = x - y function
        sub_instructions = self.build_func_sub_xy()
        self.param_num = 2
        self.G1 = sub_instructions.copy()
        add_highest = haddr(self.G1)
        self.L = [0]
        self.m = m
        for i in range(1, self.m + 1):
            self.L.append(self.L[-1] + max(self.param_num, add_highest) + 1)

        print("L location: ", self.L)

    def build_p1(self):
        instructions_list = Instructions()
        for idx in range(1, len(self.L)):
            for pn in range(1, self.param_num + 1):
                instructions_list.append(C(pn, self.L[idx] + pn))

        # print(instructions_list)

        return instructions_list

    def build_p2(self):
        numbers = tuple(range(0, self.m))
        # print("L: ", self.L)
        # print("n: ", numbers)
        superposition = Instructions(self.G1)
        # print(superposition)
        for idx in range(1, len(numbers)):
            # print(idx, self.L[idx])
            alloc = tuple(range(self.L[idx], self.L[idx + 1]))
            # print(alloc)
            reloc_G = reloc(self.G1, alloc)
            # print(reloc_G)
            superposition = superposition + reloc_G

        return superposition

    def build_p3(self):
        # Build P3
        superposition, inputs_index, outputs_index = self.build_func_sum(self.m)
        highest = haddr(superposition)
        num_of_sum_param = self.m
        # Relocation command to make room for input block
        alloc = tuple(range(num_of_sum_param, highest + num_of_sum_param + 1))
        reloc_sum_instructions = reloc(superposition, alloc)
        # Build sum function inputs block
        inputs_block = Instructions()
        last_output_index = 0
        for loc, idx in enumerate(inputs_index):
            update_index = idx + num_of_sum_param
            new_input_in_register = loc + 1
            # Copy the input value to the each compute section
            inputs_block.append(C(new_input_in_register, update_index))
            # Records the output node of the last section
            last_output_index = update_index - 2

        # Build the complete sum function instruction
        final = inputs_block + reloc_sum_instructions + Instructions(C(last_output_index, 0))

        return final

    @staticmethod
    def build_func_sub_xy():
        sub_instructions = Instructions([
            C(1, 4),
            J(3, 2, 14),
            J(5, 4, 10),
            S(5),
            J(5, 4, 9),
            S(5),
            S(0),
            J(0, 0, 5),
            Z(5),
            S(3),
            C(0, 4),
            Z(0),
            J(0, 0, 2),
            C(4, 0),
        ])
        return sub_instructions

    @staticmethod
    def build_func_sum(n: int = 3):
        # [Step.1] Prepare basic functions and basic parameters
        # Basic function: add(x, y) = x + y
        add_instructions = Instructions([
            C(2, 0),
            Z(2),
            J(1, 2, 0),
            S(0),
            S(2),
            J(3, 3, 3),
        ])
        # add(x, y) function at the parameter location of the urm register: input_x -> R1, input_y -> R2, output -> R0
        inputs_index = [1, 2, ]
        outputs_index = [0, ]

        if n < 2:
            raise ValueError("Value n must be > 2")
        elif n == 2:
            # if n = 2 then return add(x, y)
            return add_instructions, inputs_index, outputs_index

        # The highest register index of Basic func add(x, y)
        add_highest = haddr(add_instructions)
        # Iter number
        numbers = tuple(range(3, n + 1))

        # add(x, y) has two parameter
        param_num = 2
        # Build the index position L for each section
        L = [0]
        for i in range(1, n):
            L.append(L[-1] + max(param_num, add_highest) + 1)

        # [Step.2] Build the main compute function instruction for sum()
        # Build the superposition function: sum(a0, a1, a2, ..., an) = add(a0, add(a1, add(a2, ..., add(an-1, an)...)))
        superposition = add_instructions.copy()

        for idx, nb in enumerate(numbers):
            L_pre = L[idx + 0]
            L_cur = L[idx + 1]
            L_suc = L[idx + 2]
            # Computes relocation instructions
            alloc = tuple(range(L_cur, L_suc))
            g = reloc(add_instructions, alloc)
            # The glue operator is used to pass the results of the calculation for each section
            glue_op = Instructions([C(L_pre, L_cur + 1)])
            # Normalized, the output must be in the R0 position
            outputs_normal = Instructions([C(L_cur, 0)])
            # Use connection functions for instruction superposition
            superposition = superposition + glue_op + g + outputs_normal
            # Add inputs index to list
            inputs_index.append(L_cur + 2)

        return superposition, inputs_index, outputs_index

    def build_pipeline(self):
        P1 = singleton.build_p1()
        P2 = singleton.build_p2()
        P3 = singleton.build_p3()
        P = P1 + P2
        highest = haddr(P3)
        alloc = tuple(range(self.m, highest + self.m + 1))
        print(alloc)
        PP3 = reloc(P3, alloc)
        print(P)
        print(PP3)

        P = P + PP3

        registers = allocate(haddr(P) + 1)
        result = forward({1: 3, 2: 1, }, registers, P, safety_count=10000)
        for idx, reg in enumerate(result.registers_of_steps):
            command = result.ops_of_steps[idx]
            print(reg, command)


if __name__ == '__main__':
    singleton = SingletonFirst(m=4)
    singleton.build_pipeline()
