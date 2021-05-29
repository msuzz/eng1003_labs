import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

hopper = mpimg.imread('wk10-Hopper-3 square.jpg')
hopper64 = np.float64(hopper)
print('Min value in Hopper64: {}'.format(np.min(hopper64)))
print('Max value in Hopper64: {}'.format(np.max(hopper64)))
print(hopper64)

hopper64[:,:] += [50,0,0]  # Add 50 to red val

print('Min value in Hopper64 after +50 red increment: {}'.format(np.min(hopper64)))
print('Max value in Hopper64 after +50 red increment: {}'.format(np.max(hopper64)))
print(hopper64)

hopper64[hopper64>255] = 255  # Clip all values to max 255

plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.imshow(np.uint8(hopper64))
plt.savefig('.artifacts/hopper-uint8-to-float64+50-red.jpg')
plt.show()
