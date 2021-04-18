import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt

N = 1000                    # Number of steps
d = 1                       # Step size
rng = default_rng()         # Modern way to create numpy random numbers
x = np.zeros(N+1)           # Define x and y as arrays of zeros
y = np.zeros(N+1)
x[0] = 0;   y[0] = 0

for i in range(N):
    x[i] = x[i-1] + rng.uniform(-1, 1)  # Move east/west
    y[i] = y[i-1] + rng.uniform(-1, 1)  # Move north/south

# Plot path (mark start and stop with blue o and *, respectively)
plt.plot(x, y, 'r', x[0], y[0], 'bo', x[-1], y[-1], 'b*')
plt.xlabel('x');    plt.ylabel('y')
plt.show()
