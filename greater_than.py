def compare_greater_than_or_equal_simulation_steps(x, y):
    """
    Simulates URM program logic to determine if x is greater than or equal to y.
    Uses multiple registers to simplify computation steps.
    :param x: The first value to compare (stored in register R1)
    :param y: The second value to compare (stored in register R2)
    :return: Steps of the simulation.
    """
    # Initialize registers
    R1, R2 = x, y  # R1 and R2 are used for comparison
    R3 = 0  # A flag register to store the result
    steps = []

    while True:
        steps.append((R1, R2, R3))

        # If R2 is zero, set R3 flag to 1 (True)
        if R2 == 0:
            R3 = 1
            steps.append((R1, R2, R3))
            break

        # If R1 is zero, and R2 is not zero, keep R3 as 0 (False)
        if R1 == 0:
            steps.append((R1, R2, R3))
            break

        # Decrement both R1 and R2
        R1 -= 1
        R2 -= 1

    return steps


# Test the function and print steps
x = 5
y = 3
steps = compare_greater_than_or_equal_simulation_steps(x, y)
print(f"Steps for {x} >= {y}:")
for step in steps:
    print(step)

x = 2
y = 5
steps = compare_greater_than_or_equal_simulation_steps(x, y)
print(f"\nSteps for {x} >= {y}:")
for step in steps:
    print(step)

