# Plots the polynomial equation y = ax^2 + bx + c

import matplotlib.pyplot as plt
import numpy as np

a = 2
b = 5
c = -2

x = np.linspace(-4, 2, 100)
y = a*x**2 + b*x + c

plt.plot(x, y)
plt.show()
