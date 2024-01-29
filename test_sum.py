from urm_simulation import *

# sum(x, y) program instructions set
sum_instructions = Instructions([
    C(2, 0),
    Z(2),
    J(1, 2, 0),
    S(0),
    S(2),
    J(0, 0, 3)
])

P = sum_instructions
num_of_registers = haddr(P) + 1
registers = allocate(num_of_registers)
print("Init Registers: ")
print(registers.summary())

x, y = 5, 9
param = {1: x, 2: y}

# Run program
result = forward(param, registers, P, safety_count=100000)

for idx, reg in enumerate(result.registers_of_steps):
    command = result.ops_of_steps[idx]
    print(f"[step {idx}] {command}")
    print(reg.summary())
    print("")
