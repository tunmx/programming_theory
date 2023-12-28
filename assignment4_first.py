from urm_simulation import *
import numpy as np


class SingletonFirst(object):
    """
    Title: Superposition of URM Computable Functions Is URM Computable
    Requirement:
        the first of them takes a program for computing a function with m arguments and m programs for computing
        functions of n arguments each and returns the program for computing their superposition;
    Conclusion:
        In the "Singleton-1" case, the simulated SUM function is dynamically constructed. It copies and builds URM instructions
        according to the required multiplicand, consuming more registers and incurring higher computational costs. Conversely,
        the "Singleton-2" case employs a primitive recursive approach to implement the SUM function, which mitigates this issue

    Student: Jingyu Yan
    """

    def __init__(self, m: int, n: int):
        # function sum()
        g_sum_instructions = self.build_func_sum(n)
        self.param_num = n
        self.G1 = g_sum_instructions.copy()
        add_highest = haddr(self.G1)
        self.L = [0]
        self.m = m
        # Storage L[m+1], The last value in the list L is L[m-1], L[-1] == L[m-1]
        for i in range(1, self.m + 1):
            self.L.append(self.L[-1] + max(self.param_num, add_highest) + 1)

    def build_p1(self) -> Instructions:
        """
        :return: C(1, L[2+1]) ... C(n, L[2+n]) and son C(1, L[m+1]) ... C(n, L[m+n])
        """
        instructions_list = Instructions()
        for idx in range(1, len(self.L)):
            for pn in range(1, self.param_num + 1):
                instructions_list.append(C(pn, self.L[idx] + pn))

        return instructions_list

    def build_p2(self) -> Instructions:
        """
        :return: G1 ⊳ reloc(G2, (L2, ..., L3-1)) ⊳ ... ⊳ reloc(Gm, (L[m], ..., L[m+1]-1))
        """
        numbers = tuple(range(0, self.m))
        superposition = Instructions(self.G1)
        for idx in range(1, len(numbers)):
            alloc = tuple(range(self.L[idx], self.L[idx + 1]))
            reloc_G = reloc(self.G1, alloc)
            superposition = superposition + reloc_G

        return superposition

    def build_p3(self) -> Instructions:
        """
        :return: C(0, L[m+1]+1) ... C(L[m], L[m+1]+m)
        """
        p3 = Instructions()
        for idx in range(self.m):
            p3.append(C(self.L[idx], self.L[-1] + (idx + 1)))

        return p3

    @staticmethod
    def build_func_sub_xy() -> Instructions:
        """
        :return: function sub(x, y) = x - y
        """
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
    def build_func_sum(n: int = 3) -> Instructions:
        """
        Build the sum(a0, a1, a2, ..., an) = add(a0, add(a1, add(a2, ..., add(an-1, an)...)))
        :param n: n is the sum of n numbers and cannot be less than 2
        :return: URM function sum()
        """
        # [Step.1] Prepare basic functions and basic parameters
        # Basic function: add(x, y) = x + y
        add_instructions = Instructions([
            C(2, 0),
            Z(2),
            J(1, 2, 0),
            S(0),
            S(2),
            J(0, 0, 3)
        ])
        # add(x, y) function at the parameter location of the urm register: input_x -> R1, input_y -> R2, output -> R0
        inputs_index = [1, 2, ]
        superposition = add_instructions.copy()
        if n < 2:
            raise ValueError("Value n must be > 2")
        elif n == 2:
            # if n = 2 then return add(x, y)
            pass
        else:

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

        # [Step.3] Build sum normalize function
        highest = haddr(superposition)
        num_of_sum_param = n
        # Relocation command to make room for input block
        alloc = tuple(range(num_of_sum_param, highest + num_of_sum_param + 1))
        reloc_sum_instructions = reloc(superposition, alloc)
        # Build the sum function inputs block
        inputs_block = Instructions()
        last_output_index = 0
        for loc, idx in enumerate(inputs_index):
            update_index = idx + num_of_sum_param
            new_input_in_register = loc + 1
            # Copy the input value to the each compute section
            inputs_block.append(C(new_input_in_register, update_index))
            # Records the output node of the last section
            last_output_index = update_index - 2

        # Build the complete sum function instruction: P1 ⊳ P2 ⊳ P3
        final = inputs_block + reloc_sum_instructions + Instructions(C(last_output_index, 0))

        return final

    def build_pipeline(self) -> Instructions:
        """
        step.0: Prepare the F and G functions
            I'm going to use the SUM function for both G and F in this case:
            F = SUM(v[0], v[1], v[2], ..., v[m])
            G = SUM(a[0], a[1], a[2], ..., a[n])
        step.1: Build input blocks for the program
            P1 = C(1, L[2+1]) ... C(n, L[2+n]) and son C(1, L[m+1]) ... C(n, L[m+n])
        step.2: Build P2 each segment numbered from 1 to m is ready for computing the function for which it is allocated.
            P2 = G1 ⊳ reloc(G2, (L2, ..., L3-1)) ⊳ ... ⊳ reloc(Gm, (L[m], ..., L[m+1]-1))
        step.3: Build p3 prepare input for F in Segment m+1
            P3 = C(0, L[m+1]+1) ... C(L[m], L[m+1]+m)
        Conclusion: Finally, we build a function
            P = SUM(SUM1(a[1], a[2], ..., a[n]), SUM2(a[1], a[2], ..., a[n]), ..., SUMm(a[1], a[2], ..., a[n])) = m * SUM(a[1], a[2], ..., a[n])

        :return: P = P1 ⊳ P2 ⊳ P3 ⊳ reloc(F, (L[m+1], ...)) ⊳ C(L[m+1], 0)
        """
        # Prepare the F function and set the m value
        F = self.build_func_sum(self.m)
        # P1: Build the input blocks for the program
        P1 = self.build_p1()
        # P2: Build the m superposition functions of G
        P2 = self.build_p2()
        # P3: Build the input blocks for F functions
        P3 = self.build_p3()

        # Relocation F function, calculated from the L[m-1] position
        alloc = tuple(range(self.L[-1], self.L[-1] + haddr(F) + 1))
        reloc_F = reloc(F, alloc)

        # Build: P1 ⊳ P2 ⊳ P3 ⊳ reloc_F ⊳ C(L[m+1], 0)  Note: Operator '+' is overloaded for concatenation(⊳)
        P = P1 + P2 + P3 + reloc_F + Instructions(C(self.L[self.m], 0))

        return P

    def run(self, *inputs):
        """
        Run example.
        :param inputs: Parameters starting at register index 1 :R1, R2,... ,Rn
        :return:
        """
        assert len(
            inputs) == self.param_num, f"The number of input parameters does not match. The value should be {self.param_num}"
        # Build the URM program
        P = self.build_pipeline()
        # Create some registers
        registers = allocate(haddr(P) + 1)
        # Prepare input parameter
        param = {i: arg for i, arg in enumerate(inputs, start=1)}
        # execute calculation
        result = forward(param, registers, P, safety_count=100000)

        for idx, reg in enumerate(result.registers_of_steps):
            command = result.ops_of_steps[idx]
            # print(reg, command)

        # Result registers
        last = result.last_registers

        # Check result
        assert self.m * np.sum(inputs) == last[0], "The result is abnormal!"
        print(f"{self.m}*({'*'.join(map(str, inputs))})={last[0]}")


if __name__ == '__main__':
    # Singleton-First
    m = 10
    n = 5
    singleton = SingletonFirst(m, n)
    singleton.run(1, 2, 3, 4, 5)
