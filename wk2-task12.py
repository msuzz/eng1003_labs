# Plots sin(x), cos(x) and tan(x) on the same graph from 0 to 4pi.
# Limited on the y-axis to [-1.5, 1.5].

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 4*np.pi, 500)

plt.plot(x, np.sin(x))
plt.plot(x, np.cos(x))
plt.plot(x, np.tan(x))
plt.ylim([-1.5, 1.5])
plt.show()
