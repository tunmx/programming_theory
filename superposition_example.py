from urm_simulation import C, Z, J, S
import urm_simulation as urm


def build_sum_triplet():
    # Original sum function: sum(x, y) = x + y; input_x -> r1, input_y -> r2
    sum_instructions = urm.Instructions([
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
    highest_reg_sum = urm.haddr(g1)
    L1 = 0
    n = 2  # two param
    # Used to calculate the relocation register address
    L2 = L1 + max(n, highest_reg_sum) + 1
    L3 = L2 + max(n, highest_reg_sum) + 1
    alloc2 = tuple(range(L2, L3))

    # The g2 instructions was obtained from location g1
    g2 = urm.reloc(g1, alloc2)

    # To keep the program nested-running, use a glue op to copy the results of g1 as input to g2
    glue_op = urm.Instructions([C(L1, L2 + 1)])
    # To normalize the output, the output must start at index 0 or index 0
    outputs_normal = urm.Instructions([C(L2, 0)])
    # Using the URM command connect function, assemble a sum(x,y,z)=x+y+z function
    sum_triplet = g1 + glue_op + g2 + outputs_normal

    # The inputs index in the register
    input_x_index = 1
    input_y_index = 2
    input_z_index = L2 + 2
    # The outputs index in the register
    output_index = 0

    return sum_triplet, (input_x_index, input_y_index, input_z_index), (output_index, )


if __name__ == '__main__':
    sum_triplet, inputs_index, outputs_index = build_sum_triplet()
    print(sum_triplet.summary())

    registers = urm.allocate(urm.haddr(sum_triplet) + 1)
    print(registers.summary())

    x = 5
    y = 5
    z = 12

    result = urm.forward({inputs_index[0]: x, inputs_index[1]: y, inputs_index[2]: z}, registers, sum_triplet,
                         safety_count=1000)
    for idx, reg in enumerate(result.registers_of_steps):
        command = result.ops_of_steps[idx]
        print(reg, command)

    out = outputs_index[0]
    print(f"sum_triplet({x}, {y}, {z}) = {result.last_registers[out]}")