def compute_function(x):
    # 例如，这里我们计算一个函数，使得x的奇偶性相反
    return x + 1 if x % 2 == 0 else x - 1

def minimization(program_f, target_value):
    x = 0
    found_values = []  # 用于存储满足条件的x值
    while True:
        result = program_f(x)
        if result == target_value:
            found_values.append(x)
        if len(found_values) >= 5:  # 为了演示，我们找到5个满足条件的x值
            return found_values
        x += 1

target_value = 7  # 希望找到多个x，使compute_function(x)等于7
results = minimization(compute_function, target_value)
print(f"Values of x where compute_function(x) equals {target_value}: {results}")
