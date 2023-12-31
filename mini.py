# 重定义最小化函数，增加步骤打印
def minimization_verbose(f, *fixed_args, min_condition_func=None):
    def default_min_condition(output):
        return output == 0

    min_condition = min_condition_func or default_min_condition
    n = 0
    while True:
        result = f(*fixed_args, n)
        print(f"Testing n = {n}: f(*fixed_args, n) = {result}")
        if min_condition(result):
            print(f"Found! The smallest n for which f(*fixed_args, n) meets the condition is {n}\n")
            return n
        n += 1


# 示例函数
def example_function(a, b, x):
    return a * x + b  # 使用线性表达式


# 自定义的 min_condition 函数
def custom_min_condition(output, target_value):
    return output >= target_value


# 使用最小化函数，并传递自定义的 min_condition 函数
a, b = 4, 8  # 固定参数
target_value = 1000  # 目标值
result = minimization_verbose(example_function, a, b,
                              min_condition_func=lambda output: custom_min_condition(output, target_value))

print(result)
