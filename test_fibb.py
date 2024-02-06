from urm_simulation import *

# sum(x, y) program instructions set
fibb_instructions = Instructions(
        J(1, 0, 0),  # 1. if R1 == 0 then fibb(0) = 0
        S(0),  # 2. set R0 = 2
        J(1, 0, 0),  # 3. if R1 = 1 then fibb(1) = 1
        S(2),  # 4. set R2 = 1

        J(1, 2, 0),  # 5. loop_1 if R1 == R2 then jump to the end

        S(2),  # 6. set k++
        C(0, 4),  # 7. set fibb(k-1) to R4
        Z(0),  # 8. set R0 to 0
        Z(5),  # 9. set R5 to 0

        C(4, 0),  # 10. copy R4 to 0
        J(5, 3, 15),  # 11. if R5 == R3 then jump to 15
        S(0),  # 12. set R0++
        S(5),  # 13. set R5++
        J(1, 1, 11),  # 14. do while
        C(4, 3),  # 15. copy fibb(k-1) for the current k to fibb(k-2) for the next k(k++)

        J(2, 2, 5),  # 16 do while
)

P = fibb_instructions
num_of_registers = haddr(P) + 1
registers = allocate(num_of_registers)
print("Init Registers: ")
print(registers.summary())

x = 10
param = {1: x,}

# Run program
result = forward(param, registers, P, safety_count=100000)

last = result.last_registers
print(last.summary())
