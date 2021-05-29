import ass2_imageProcessing as ip
import matplotlib.pyplot as plt

x = ip.loadImage("wk10-Hopper-3 square.jpg")
plt.figure(1)
ip.showImage(x)
plt.title("Original")

xB = ip.brightness(x.copy(), 1.8, changeType="relative")
plt.figure(2)
ip.showImage(xB)
plt.title("Brightness Up")

ip.saveImage(xB, "Helsinki-brightened.jpg")

xC = ip.contrast(x.copy(), 2)
plt.figure(3)
ip.showImage(xC)
plt.title("Contrast Up")

xS = ip.hsl2rgb(ip.saturation(ip.rgb2hsl(x.copy()), 2))
plt.figure(4)
ip.showImage(xS)
plt.title("Saturation Up")

plt.figure(5)
ip.showImage(ip.hsl2rgb(ip.toneMap(ip.rgb2hsl(x.copy()), 285, 0.1)))
plt.title("Tone Mapped")

plt.figure(6)
ip.showImage(ip.crop(x.copy(), 70,200, 80, 200))
plt.title("Cropped")

plt.figure(7)
ip.histogram(ip.contrast(x.copy(), 2), bins=128)
ip.histogram(x.copy(), bins=128)
plt.title("L Channel Histogram Before and After Contrast Boost")

print("White saturated in original: ", ip.saturated(x.copy()))
print("White saturated in contrast boosted: ", ip.saturated(ip.contrast(x.copy(),2)))

plt.figure(8)
ip.showImage(ip.unsharpMask(x.copy(), amount=3))
plt.title("Sharpened")

plt.show()
