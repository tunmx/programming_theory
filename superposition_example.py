from urm_simulation import *


def build_sum_triplet():
    # Original sum function: sum(x, y) = x + y; input_x -> r1, input_y -> r2
    sum_instructions = Instructions([
        C(2, 0),
        Z(2),
        J(1, 2, 0),
        S(0),
        S(2),
        J(3, 3, 3),
    ])
    # Copy the instructions to g1
    g1 = sum_instructions.copy()
    # Get highest from g1
    highest_reg_sum = haddr(g1)
    L1 = 0
    n = 2  # two param
    # Used to calculate the relocation register address
    L2 = L1 + max(n, highest_reg_sum) + 1
    L3 = L2 + max(n, highest_reg_sum) + 1
    print('L2', L2)
    print('L3', L3)
    alloc2 = tuple(range(L2, L3))
    print(alloc2)

    # The g2 instructions was obtained from location g1
    g2 = reloc(g1, alloc2)

    # To keep the program nested-running, use a glue op to copy the results of g1 as input to g2
    glue_op = Instructions([C(L1, L2 + 1)])
    # To normalize the output, the output must start at index 0 or index 0
    outputs_normal = Instructions([C(L2, 0)])
    # Using the URM command connect function, assemble a sum(x,y,z)=x+y+z function
    sum_triplet = g1 + glue_op + g2 + outputs_normal

    # The inputs index in the register
    input_x_index = 1
    input_y_index = 2
    input_z_index = L2 + 2
    # The outputs index in the register
    output_index = 0

    return sum_triplet, (input_x_index, input_y_index, input_z_index), (output_index,)


def build_sum(n: int = 3):
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

    # [Step.3] Build sum normalize function
    highest = haddr(superposition)
    num_of_sum_param = n
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

    # Build the complete sum function instruction: P1 -> P2 -> P3
    final = inputs_block + reloc_sum_instructions + Instructions(C(last_output_index, 0))

    return final


def case_sum_n_test(m: int) -> Instructions:
    sum_instructions, inputs_index, outputs_index = build_sum(m)
    highest = haddr(sum_instructions)
    param_num = m
    alloc = tuple(range(param_num, highest + param_num + 1))
    reloc_sum_instructions = reloc(sum_instructions, alloc)

    pre = Instructions()
    last_output_index = 0
    for loc, idx in enumerate(inputs_index):
        update_index = idx + param_num
        new_input_in_register = loc + 1
        pre.append(C(new_input_in_register, update_index))
        last_output_index = update_index - 2

    final = pre + reloc_sum_instructions + Instructions(C(last_output_index, 0))

    return final


def case_sum_triplet():
    sum_triplet, inputs_index, outputs_index = build_sum_triplet()
    print(sum_triplet)
    print(inputs_index, outputs_index)
    #
    # registers = allocate(haddr(sum_triplet) + 1)
    # print(registers.summary())
    #
    # x = 5
    # y = 5
    # z = 12
    #
    # result = forward({inputs_index[0]: x, inputs_index[1]: y, inputs_index[2]: z}, registers, sum_triplet,
    #                      safety_count=1000)
    # for idx, reg in enumerate(result.registers_of_steps):
    #     command = result.ops_of_steps[idx]
    #     print(reg, command)
    #
    # out = outputs_index[0]
    # print(f"sum_triplet({x}, {y}, {z}) = {result.last_registers[out]}")


def case_sum_n():
    m = 4
    sum_instructions, inputs_index, outputs_index = build_sum(m)
    print(sum_instructions)
    print(f"inputs_index: {inputs_index}")
    print(f"outputs_index: {outputs_index}")
    registers = allocate(haddr(sum_instructions) + 1)
    print(registers.summary())
    print(inputs_index)

    # pre = Instructions([C(0, 1)])

    # inputs_data = [1, 2, 3, 4]
    # assert len(inputs_data) == len(inputs_index)
    # param = dict(zip(inputs_index, inputs_data))
    # print(param)
    # result = forward(param, registers, sum_instructions, safety_count=1000)
    # for idx, reg in enumerate(result.registers_of_steps):
    #     command = result.ops_of_steps[idx]
    #     print(reg, command)
    #
    # out = outputs_index[0]
    # print(result.last_registers[out])
    #

def case_sub():
    sum_instructions = Instructions([
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
    registers = allocate(haddr(sum_instructions) + 1)
    x = 20
    y = 14
    result = forward({1: x, 2: y}, registers, sum_instructions,
                     safety_count=1000)
    for idx, reg in enumerate(result.registers_of_steps):
        command = result.ops_of_steps[idx]
        print(reg, command)


def build_gm(m: int):
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
    instructions_list = list()
    param_num = 2
    add_highest = haddr(sub_instructions)
    L = [0]
    for i in range(1, m):
        L.append(L[-1] + max(param_num, add_highest) + 1)
    print(L)
    for idx in range(1, len(L)):
        for pn in range(1, param_num+1):
            instructions_list.append(C(pn, L[idx] + pn))

    print(instructions_list)


if __name__ == '__main__':
    # case_sub()
    # case_sum_triplet()
    #
    # build_sum_n(4)

    # case_sum_n()
    # build_gm(m=5)

    num_of_sum = 5
    sum = build_sum(n=num_of_sum)
    registers = allocate(haddr(sum) + 1)
    print(sum)
    array = range(1, num_of_sum + 1)
    assert len(array) == num_of_sum
    dictionary = {index + 1: value for index, value in enumerate(array)}
    result = forward(dictionary, registers, sum, safety_count=1000)
    for idx, reg in enumerate(result.registers_of_steps):
        command = result.ops_of_steps[idx]
        print(reg, command)