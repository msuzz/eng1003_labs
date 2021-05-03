import rootfinding as rf


def func(x):
    return x**3 + 1.8*x**1.4 - 5

func_root = rf.secant(func, x0=0, x1=1, tol=1e-10, iterMax=64)
print("Root of f(x): {0}".format(func_root))