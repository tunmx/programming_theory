import math

def distance_to_probability(d):
    k = 20.0
    theta = 0.5
    return 1 / (1 + math.exp(k * (d - theta)))


dd = 0.002 * 100
print(distance_to_probability(dd))