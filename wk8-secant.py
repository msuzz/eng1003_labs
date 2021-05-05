def f(L):
    return  0.0268*L**3 + 1.884*L**2 + 44.15*L - 500

eps = 1e-6
x0 = 6
x1 = 10
itCnt = 0       # iteration counter
while abs(f(x1)) > eps:
    # line (=secant) through (x0,f(x)) and (x1,f(x1)) intersects
    # horizontal axis at (x,0)
    x = x1 - f(x1)*((x1 - x0)/(f(x1) - f(x0)))
    x0 = x1
    x1 = x
    itCnt += 1

print('Solution: {}'.format(x))
print('Number of iterations: {}'.format(itCnt))
print('Check: f({:.8f}) = {:.8f}'.format(x,f(x)))