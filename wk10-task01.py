import matplotlib.pyplot as plt
import matplotlib.image as mpimg

hopper = mpimg.imread('wk10-Hopper-3 square.jpg')
plt.xticks([])
plt.yticks([])
plt.imshow(hopper)
print('Image array datatype: {}'.format(hopper.dtype))
plt.show()
