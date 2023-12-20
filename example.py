from urm_simulation import C, Z, J, S
import urm_simulation as urm


def add_case(x, y):
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


if __name__ == '__main__':
    add_case(30, 20)
