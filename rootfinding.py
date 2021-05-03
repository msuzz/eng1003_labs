def bisection(f, xLo, xHi, tol=1e-10, iterMax=64):
  if xLo >= xHi:
    print("ERROR: xLo must be strictly less than xHi")
    return
  print("f(xLo): ", f(xLo))
  print("f(xHi): ", f(xHi))
  if f(xLo) * f(xHi) > 0:
    print("ERROR: f(xLo) and f(xHi) must have different sign")
    print("f(xLo): ", f(xLo))
    print("f(xHi): ", f(xHi))
    return
  xMid = (xLo + xHi) / 2
  iters = 0
  while abs(f(xMid)) > tol and iters < iterMax:
    if f(xMid) * f(xLo) > 0:
      xLo = xMid
    else:
      xHi = xMid
    xMid = (xLo + xHi) / 2
    iters += 1
  return xMid, iters


def secant(f, x0=0, x1=1, tol=1e-10, iterMax=64):
  iters = 0
  while abs(f(x1)) > tol and iters < iterMax:
    x = x1 - f(x1) * ((x1 - x0) / (f(x1) - f(x0)))
    x0 = x1
    x1 = x
    iters += 1
  return x, iters


def newton(f, df, x0=1, tol=1e-10, iterMax=32):
  iters = 0
  xNew = x0 - f(x0) / df(x0)
  x0 = xNew
  while abs(f(xNew) > tol) and iters < iterMax:
    xNew = x0 - f(x0) / df(x0)
    x0 = xNew
    iters += 1
  return x0, iters