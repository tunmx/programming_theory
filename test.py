from urm_simulation import C, J, Z, S, URM
import copy

def fibb_urm(x):
    instructions = [
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
    ]

    num_of_registers = 6
    R = [0 for _ in range(num_of_registers)]
    R[1] = x  # set R1 = x
    # copy the initial register
    R_init = copy.deepcopy(R)
    urm = URM(instructions=instructions, initial_registers=R)
    # Using a URM simulator to calculate fibb(x) numbers involves a large amount of computation,
    # thus a larger safety_count needs to be set to prevent premature termination.
    safety_count = 10000
    # run
    steps_command = urm(safety_count=safety_count)

    return R_init, steps_command


x = 10
R_init, results = fibb_urm(x)
print(R_init)
value = -1
for step, command in results:
    value = step[0]
    print(step, command)
print("Result of ffib({}) = {}".format(x,value))