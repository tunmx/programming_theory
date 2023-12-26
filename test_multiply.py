from urm_simulation import *


def base_case(x):
    # 基础情况: 0 乘以任何数都是 0
    return 0


def recursive_step(n, acc, x):
    # 递归步骤: 把 x 加到累加器 acc 上 n 次
    if n == 0:
        return acc
    else:
        return recursive_step(n - 1, acc + x, x)


def multiply(x, y):
    # 乘法函数: 使用原始递归模式计算两个数的乘积
    return recursive_step(y, base_case(x), x)


if __name__ == '__main__':
    # 测试函数
    product = multiply(4, 3)  # 应该计算出 4 * 3
    print(product)  # 预期输出: 12
