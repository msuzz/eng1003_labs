import numpy as np


def f(x):
    return 3 * np.sin(0.1*x)


def trap_function(g, a, b, N):
    deltax = (b - a) / N
    mid_sum = 0; trap = 1
    while trap != N:
        mid_sum += g(a + deltax * trap)
        trap += 1
    return deltax * (mid_sum + g(a) + g(b) / 2)


print(trap_function(f, 0, np.pi/4, 10))
