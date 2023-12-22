from urm_simulation import C, Z, J, S
import urm_simulation as urm


def add_case(x, y):
    # sum(x, y) = x + y
    instructions = urm.Instructions([
        C(2, 0),
        Z(2),
        J(1, 2, 0),
        S(0),
        S(2),
        J(3, 3, 3),
    ])
    safety_count = 1000
    num_of_registers = 4
    registers = urm.allocate(num_of_registers)
    result = urm.forward({1: x, 2: y}, registers, instructions, safety_count=safety_count)
    print(f"run count: {result.num_of_steps}")
    print(result.last_registers.summary())
    print(f"add({x}, {y}) = {result.last_registers[0]}")


def double_case(x):
    # double(x) = 2x
    instructions = urm.Instructions([
        C(1, 2),
        J(2, 0, 0),
        S(0),
        S(0),
        S(2),
        J(2, 2, 2),
    ])
    safety_count = 1000
    num_of_registers = 4
    registers = urm.allocate(num_of_registers)
    result = urm.forward({1: x}, registers, instructions, safety_count=safety_count)
    print(result.last_registers.summary())
    for idx, reg in enumerate(result.registers_of_steps):
        command = result.ops_of_steps[idx]
        print(reg, command)


def double_high_case(x):
    # double(x) = 2x
    instructions_p0 = urm.Instructions([
        C(1, 2),
        J(2, 0, 0),
        S(0),
        S(0),
        S(2),
        J(2, 2, 2),
    ])

    instructions = urm.Instructions([
        C(5, 6),
        J(6, 4, 0),
        S(4),
        S(4),
        S(6),
        J(6, 6, 2),
    ])

    # instructions_p0_norm = urm.normalize(instructions_p0)
    # print(instructions_p0_norm)
    n = 1
    L1 = 0
    L2 = L1 + max(n, urm.haddr(instructions_p0)) + 1
    L3 = L2 + max(n, urm.haddr(instructions_p0)) + 1
    print(f"L2: {L2}")
    alloc2 = tuple(range(L2, L3))
    print(alloc2)
    new_p1 = urm.reloc(instructions_p0, alloc2)
    print(new_p1)
    print(f"L3: {L3}")

    # cat = urm.concat(urm.concat(instructions_p0, urm.Instructions([C(0, 4)])), new_p1)
    cat = instructions_p0 + urm.Instructions([C(0, 4)]) + new_p1
    print(cat)

    input_index = 1
    safety_count = 1000
    num_of_registers = 8
    registers = urm.allocate(num_of_registers)
    result = urm.forward({input_index: x}, registers, cat, safety_count=safety_count)
    print(result.last_registers.summary())
    for idx, reg in enumerate(result.registers_of_steps):
        command = result.ops_of_steps[idx]
        print(reg, command)
    #




def computable():
    # Define the double function: double(x) = 2x; input data = R1, output data = R0;
    instructions = urm.Instructions([
        ('C', 1, 2),
        ('J', 2, 0, 0),
        ('S', 0),
        ('S', 0),
        ('S', 2),
        ('J', 2, 2, 2),
    ])
    G1 = instructions.copy()
    highest_reg_G1 = urm.haddr(G1)
    # 分配新的寄存器地址
    alloc = tuple(range(highest_reg_G1 + 1, highest_reg_G1 * 2 + 2))
    G1_double = urm.reloc(G1, alloc)
    print(G1_double)

    # 中间结果需要复制到新的 R1 以供第二次 double 使用
    # 注意，这里我们要将 R0 的值复制到重新定位后的 G1 的 R1
    # 即，复制到 alloc[0]，它是第二次 double 的 R1
    copy_result_to_new_R1 = urm.Instructions([('C', 0, alloc[0])])

    # 将两个 G1 程序串联起来，中间插入复制指令
    P = urm.concat(urm.concat(G1, copy_result_to_new_R1), G1_double)
    print(f"P: {P}")

    # 根据 P 中使用的最高寄存器地址，分配寄存器
    num_of_registers = urm.haddr(P) + 1
    R = urm.allocate(num_of_registers)

    # 使用初始值 R1 = 2 来执行程序
    result = urm.forward({1: 2}, R, P, safety_count=100)
    print(result)


if __name__ == '__main__':
    # add_case(30, 20)
    # double_case(3)
    double_high_case(3)
    # computable()
