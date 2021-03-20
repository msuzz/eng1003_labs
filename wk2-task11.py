# Plots some simultaneous equations and allows us to see the intersect

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-5, 5, 50)
eq1y = (x - 1)/2   # x - 2y = 1
eq2y = (3 - 2*x)/4  # 2x + 4y = 3

plt.plot(x, eq1y)
plt.plot(x, eq2y)
plt.show()
