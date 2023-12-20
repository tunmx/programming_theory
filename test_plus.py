from urm_simulation import C, Z, J, S
import urm_simulation as urm

instructions = urm.Instructions([
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

print(f"size: {urm.size(instructions)}")
print(f"size: {urm.haddr(instructions)}")

instructions_norm = urm.normalize(instructions)
print(instructions)
print(instructions_norm)

reg = urm.allocate(6)
reg[1] = 20  # set R1 = x
reg[2] = 19  # set R2 = x
simulator = urm.URMSimulator(instructions=instructions_norm, initial_registers=reg)

safety_count = 10000
steps = simulator(safety_count=safety_count)
print(steps)

print(type(steps))
for step, command in steps:
    value = step[0]
    print(step, command)

