import numpy as np


def diceprob(k, n):
    sum = 0
    for _ in range(n):
        a = np.random.randint(1, 7)
        b = np.random.randint(1, 7)
        if a == k or b == k:
            sum += 1
    return sum/n


np.random.seed(1)
for k in range(1,7):
    print(k, diceprob(k, 100))