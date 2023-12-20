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
    registers[1] = x
    registers[2] = y
    simulation = urm.URMSimulator(instructions, registers)
    result = simulation(safety_count=safety_count, only_result=True)
    print(f"run count: {simulation.run_count}")
    print(result.summary())
    print(f"add({x}, {y}) = {result[0]}")

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
    registers[1] = x
    simulation = urm.URMSimulator(instructions, registers)
    result = simulation(safety_count=safety_count, only_result=True)
    print(result.summary())

def double_sum_case(x, y):
    # double(sum(x, y)) = 2 * (x + y)
    sum_instructions = urm.Instructions([
        C(2, 0),
        Z(2),
        J(1, 2, 0),
        S(0),
        S(2),
        J(3, 3, 3),
    ])
    double_instructions = urm.Instructions([
        C(1, 2),
        J(2, 0, 0),
        S(0),
        S(0),
        S(2),
        J(2, 2, 2),
    ])
    # 重新定位 double 指令的寄存器地址
    # 假设 double 使用的寄存器从4开始，以避免与sum冲突
    relocated_double_instructions = urm.reloc(double_instructions, (4, 5, 6, ))

    # 在 sum 和 double 指令之间插入复制指令
    sum_and_prepare_double = urm.concat(sum_instructions, urm.Instructions([C(0, 4)]))

    # 合并 sum 和 double 指令
    full_instructions = urm.concat(sum_and_prepare_double, relocated_double_instructions)

    print(full_instructions.summary())
    #
    # # 分配寄存器并设置输入值
    # registers = urm.allocate(10)  # 分配足够数量的寄存器
    # registers[1] = x
    # registers[2] = y
    #
    # # 运行URM模拟器
    # safety_count = 100
    # simulation = urm.URMSimulator(full_instructions, registers)
    # result = simulation(safety_count=safety_count, only_result=True)
    # final_result = None
    # for step, command in result:
    #     print(step, command)
    #     final_result = step
    #
    # print(f"double(sum({x}, {y})) = {final_result[0]}")


if __name__ == '__main__':
    # add_case(30, 20)
    # double_case(10)
    double_sum_case(3, 5)