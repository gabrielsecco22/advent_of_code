# solve the equation x = cos(x) for x
import math


def f(x):
    return x - math.cos(x)

def solve(f, x0, x1, eps):
    while abs(x1 - x0) > eps:
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        x0 = x1
        x1 = x2
    return x1

print(solve(f, 0, 1, 0.000000000000000000001))
