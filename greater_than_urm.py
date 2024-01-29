import random

from urm_simulation import *

pre_instructions = Instructions([
    Z(0),
    J(0, 1, 0),
    S(2),
    J(1, 2, 8),
    S(0),
    S(2),
    J(0, 0, 4),
    Z(2),
])


def build_greater_than_or_equal():
    # x >= y
    # R1 = x, R2 = Y
    # R3 = x - 1, temp
    # r5 = pre_temp
    # [R0 R1 R2 R3 R4 R5 R6 R7]
    inst = Instructions(
        Z(0),  # 1

        J(2, 0, 24),  # 2
        J(1, 0, 25),  # 3

        Z(3),  # 4
        J(3, 1, 25),  # 5
        S(4),  # 6
        J(1, 4, 11),  # 7
        S(3),  # 8
        S(4),  # 9
        J(0, 0, 7),  # 10
        C(3, 1),  # 11
        Z(4),  # 12

        Z(3),  # 13
        J(3, 2, 25),  # 14
        S(4),  # 15
        J(2, 4, 20),  # 16
        S(3),  # 17
        S(4),  # 18
        J(0, 0, 16),  # 19
        C(3, 2),  # 20
        Z(4),  # 21

        Z(3),  # 22
        J(0, 0, 2),  # 23

        S(0),  # 24

    )

    return inst


def greater_than(x, y) -> bool:
    gto = build_greater_than_or_equal()
    registers = allocate(haddr(gto) + 1)

    result = forward({1: x, 2: y}, registers, gto, safety_count=100000)

    for idx, reg in enumerate(result.registers_of_steps):
        command = result.ops_of_steps[idx]
        print(reg, command)
    last = result.last_registers

    return bool(last[0])

def test_greater_than(n):
    """
    Test the greater_than function with n pairs of random numbers between 0 and 100.
    """
    test_results = []
    for _ in range(n):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        result = greater_than(x, y)
        expected_result = x >= y
        test_results.append((x, y, result, expected_result))

    return test_results

greater_than(6, 7)

# Generate test cases and print results
# n = 10  # Number of test cases
# test_cases = test_greater_than(n)
# for x, y, result, expected in test_cases:
#     assert result == expected, f"Test failed for x={x}, y={y}, result={result}, expected={expected}"
#     print(f"Test passed for x={x}, y={y}, result={result}, expected={expected}")