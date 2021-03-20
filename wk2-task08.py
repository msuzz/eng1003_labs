# Subplot example

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2, 2, 100)
y1 = 2*x+5
y2 = -0.5*x+2

plt.subplot(2, 1, 1)
plt.plot(x, y1)

plt.subplot(2, 1, 2)
plt.plot(x, y2)

plt.show()
