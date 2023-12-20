from urm_simulation_plus import *

instructions_p = Instructions([
    Z(0), S(1), C(2, 3), J(4, 5, 0)
])

instructions_q = Instructions([
    J(4, 5, 0), C(2, 3), S(1), Z(0)
])

pipe = concat(instructions_p, instructions_q)

print(pipe)

reloc_inst = reloc(pipe, (6, 7, 8, 9, 10, 11))
print(reloc_inst)