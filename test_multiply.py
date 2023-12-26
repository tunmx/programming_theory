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


def build_G():
    add_instructions = Instructions([
        C(1, 2),
        C(2, 0),
        Z(2),
        J(1, 2, 0),
        S(0),
        S(2),
        J(0, 0, 4)
    ])
    pre_instructions = Instructions([
        J(0, 1, 0),
        S(2),
        J(1, 2, 0),
        S(0),
        S(2),
        J(0, 0, 3),
    ])

    m = 2

    G = add_instructions.copy()

    add_highest = haddr(add_instructions)
    L = [0]
    for i in range(1, m + 1):
        L.append(L[-1] + max(m, add_highest) + 1)

    print(L)
    alloc = tuple(range(L[1], L[2]))
    print(alloc)
    reloc_pre = reloc(pre_instructions, alloc)
    print(reloc_pre)

    G = G + reloc_pre
    print(G)

    I = Instructions([C(1, L[0] + 2 + 2), C(2, L[1] + 2 + 2)])
    print(I)

    alloc2 = tuple(range(3, 3 + haddr(G) + 1))
    G = I + reloc(G, alloc2)
    CX = Instructions(S(haddr(G) + 1))

    G = G + CX


    return G

def build():

    G = build_G()
    print(G)
    #
    registers = allocate(haddr(G) + 1)
    param = {1: 4, 2: 6}
    result = forward(param, registers, G, safety_count=50)

    for idx, reg in enumerate(result.registers_of_steps):
        command = result.ops_of_steps[idx]
        print(reg, command)


if __name__ == '__main__':
    # 测试函数
    # product = multiply(4, 3)  # 应该计算出 4 * 3
    # print(product)  # 预期输出: 12

    build()
