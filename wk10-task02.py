import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

hopper = mpimg.imread('wk10-Hopper-3 square.jpg')
hopper64 = np.float64(hopper)
print(hopper)
print(hopper64)
hopper64 += 0.5
hopperNew = np.uint8(np.round(hopper64))

plt.xticks([])
plt.yticks([])
plt.imshow(hopperNew)
print('Hopper64 datatype: {}'.format(hopper64.dtype))
print('HopperNew datatype: {}'.format(hopperNew.dtype))
plt.savefig('.artifacts/hopper-uint8-to-float64+0.5-to-uint8-round.jpg')
plt.show()
