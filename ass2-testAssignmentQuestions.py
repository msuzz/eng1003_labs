'''
ENGG1003, Semester 1, 2021

This script tests the 8 Assignment 2 functions:

    brightness()
    contrast()
    saturation()
    toneMap()
    crop()
    saturated()
    histogram()
    unsharpMask()
'''

import ass2_imageProcessing as ip
import matplotlib.pyplot as plt
import numpy as np
import os

try:
  import requests
except ImportError:
  print("Trying to Install required module: requests\n")
  os.system('python -m pip install requests')

import requests

# Make the True and False as-needed to speed up run time
# ie: don't try to test functions you haven't written
# and don't test functions you know already work
checkBrightness = True
checkContrast = True
checkSaturation = True
checkToneMap = True
checkCrop = True
checkSaturated = True
checkHistogram = True
checkUnsharpMask = True

# Download the reference images
print("Testing if reference images exist and downloading if necessary")
try:
    f = open("Hopper.tiff")
except IOError:
    print("Hopper.tiff not found - downloading all reference images")
    urls = ['https://github.com/bschulznewy/a2Testing/raw/main/Hopper.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_B.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_G.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_L.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_L_log.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_R.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_R_log.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/unsharp-defaults.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/unsharp-r2a100.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/unsharp-r50.tiff']
    for url in urls:
        x = requests.get(url)
        filename = url.rsplit('/',1)[1]
        print("Saving ", filename)
        open(filename, "wb").write(x.content)

try:
    f = open("hist_R.tiff")
except IOError:
    print("hist_R.tiff not found - downloading all reference images")
    urls = ['https://github.com/bschulznewy/a2Testing/raw/main/Hopper.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_B.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_G.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_L.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_L_log.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_R.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/hist_R_log.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/unsharp-defaults.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/unsharp-r2a100.tiff', 'https://github.com/bschulznewy/a2Testing/raw/main/unsharp-r50.tiff']
    for url in urls:
        x = requests.get(url)
        filename = url.rsplit('/',1)[1]
        print("Saving ", filename)
        open(filename, "wb").write(x.content)


if checkBrightness:
    x = np.float64(np.random.randint(0,255, size=(10,10,3)))
    xNew = ip.brightness(x.copy(), 1000)
    if xNew.max() <= 255:
        print("Brightness error - this function should NOT perform clipping saturation")
        quit()
    if np.array_equal(xNew, x+1000) == False:
        print("Brightness error - absolute change")
        print("Expected:")
        print(x+1000)
        print("Got:")
        print(xNew)
        quit()
    xNew = ip.brightness(x.copy(), 20, changeType="relative")
    if np.array_equal(xNew, x*20) == False:
        print("Brightness error - relative change")
        print("Expected:")
        print(x*20)
        print("Got:")
        print(xNew)
        quit()
    if np.array_equal(x, ip.brightness(x.copy(), 2, changeType="error")) == False:
        print("Brightness error")
        print("Passing incorrect changeType variable should return imageData argument unchanged")
        quit()
    print("Brightness test PASSED")

if checkContrast:
    x = np.float64(np.random.randint(0,255, size=(4,4,3)))
    xNew = ip.contrast(x.copy(), 100)
    diff = xNew - (100*(x - 127.5)+127.5)
    if np.linalg.norm(diff) > 1e-16:
        print("Contrast error")
        print("Got:")
        print(xNew)
        print("Expected:")
        print(100*(x - 127.5)+127.5)
        quit()
    print("Contrast test PASSED")

if checkSaturation:
    x = np.float64(np.random.randint(1,256, size=(2,2,3)))
    xNew = ip.saturation(x.copy(), 64)
    tmp = xNew/x
    tmp = np.uint8(tmp)
    print(tmp)
    if ((tmp[:,:,1] != 64).any() or (tmp[:,:,0] != 1).any() or (tmp[:,:,2] != 1).any) == False:
        print("Saturation error")
        print("Expected:")
        x[:,:,1]*=64
        print( x )
        print("Got:")
        print(xNew)
        quit()
    print("Saturation PASSED")

if checkToneMap:
    x = np.float64(np.random.randint(0,255, size=(2,2,3)))
    xNew = ip.toneMap(x, 10, 0.2)
    if (xNew[:,:,0] != 10).any() or (xNew[:,:,1] != 0.2).any():
        print("toneMap() error")
        print("H and S channels should be ", 10, " and ", 0.2, " respectivly.")
        print("These are the first and 2nd columns of numbers below:")
        print("Got:")
        print(xNew)
        quit()
    print("checkToneMap PASSED")

if checkCrop:
    x = np.float64(np.random.randint(0,255, size=(10,10,3)))
    if np.array_equal(ip.crop(x.copy(), 9, 1, 0, 1), x) == False:
        print("Crop error. Crop should return unmodified data when top > bottom")
        quit()
    if np.array_equal(ip.crop(x.copy(), 1, 9, 9, 1), x) == False:
        print("Crop error. Crop should return unmodified data when left > right")
        quit()
    if np.array_equal(ip.crop(x.copy(), 20, 30, 40, 50), x) == False:
        print("Crop error. Crop should return unmodified data when any argument exceeds the input size")
        quit()
    if np.array_equal(ip.crop(x.copy(), 2, 6, 1, 3), x[2:6, 1:3]) == False:
        print("Crop error")
        print("Expected:")
        print(x[2:6, 1:3])
        print("Got:")
        print(ip.crop(x.copy(), 2, 6, 1, 3))
        quit()
    print("Crop PASSED")

if checkSaturated:
    x = ip.saturated(np.float64(np.array([[[0,0,0], [1,1,1], [255, 255, 3], [255, 2, 255]]])))
    if np.abs(x - 4/12*100) > 1e-6:
        print("saturated() error when testing default type. Expected ", 4/12*100, " but got ", x)
        quit()
    x = ip.saturated(np.float64(np.array([[[0,0,0], [1,1,1], [255, 255, 3], [255, 2, 255]]])), type="white")
    if np.abs(x - 4/12*100) > 1e-6:
        print("saturated() error when testing explicit type=\"white\". Expected ", 4/12*100, " but got ", x)
        quit()
    x = ip.saturated(np.float64(np.array([[[0,0,0], [1,1,1], [255, 255, 3], [255, 2, 255]]])), type="black")
    if np.abs(x - 3/12*100) > 1e-6:
        print("saturated() error when testing for black pixels. Expected ", 3/12*100, " but got ", x)
        quit()
    x = ip.saturated(np.float64(np.array([[[12, 0.2, 0.999], [0,0,0], [143,532,0], [1,2,0.991]]])), format="HSL")
    if np.abs(x - 50) > 1e-6:
        print("saturated() error with HSL data. Got ", x, ". Expected ", 50)
        quit()
    x = ip.saturated(np.float64(np.array([[[12, 0.2, 0.999], [0,0,0], [143,532,0.3], [1,2,0.991]]])), type="black", format="HSL")
    if np.abs(x - 25) > 1e-6:
        print("saturated() error with HSL data type=\"black\". Got ", x, ". Expected ", 25)
        quit()
    x = ip.saturated(ip.loadImage("Hopper.tiff"))
    print("Debug: ip.saturated() white difference with Hopper.tiff: ", np.abs(x-0.5924456478031258))
    if np.abs(x-0.5924456478031258) > 1e-2:
        print("saturated() error with Hopper.jpg. Failed with default arguments. Got ", x, " but expected 0.5924456478031258.")
        quit()
    x = ip.saturated(ip.loadImage("Hopper.tiff"), type="black")
    print("Debug: ip.saturated() black difference with Hopper.tiff: ", np.abs(x-0.384623731271454))
    if np.abs(x-0.384623731271454) > 1e-2:
        print("saturated() error with Hopper.jpg and type=\"black\". Got ", x, " but expected 0.384623731271454.")
        quit()

    print("Saturated PASSED")

if checkHistogram:
    x = ip.loadImage("Hopper.tiff")
    print("Starting histogram() tests. If these all fail because of graphical differences perform manual comparisons with the reference images as-needed.")
    print("Testing histogram() with RGB input")
    plt.figure(1)
    ip.histogram(x.copy(), channel="R", bins=32)
    plt.savefig("testhist_R.tiff")
    print("Histogram diff debug R: ", np.linalg.norm(ip.loadImage("testhist_R.tiff") - ip.loadImage("hist_R.tiff")))
    if np.linalg.norm(ip.loadImage("testhist_R.tiff") - ip.loadImage("hist_R.tiff")) > 10000:
        print("histogram() error for R channel, RGB input")
        plt.close('all')
        plt.figure(1)
        ip.showImage(ip.loadImage("testhist_R.tiff"))
        plt.title("Got")
        plt.figure(2)
        ip.showImage(ip.loadImage("hist_R.tiff"))
        plt.title("Expected")
        plt.show()
        quit()
    plt.figure(2)
    ip.histogram(x.copy(), channel="G", bins=32)
    plt.savefig("testhist_G.tiff")
    print("Histogram diff debug G: ", np.linalg.norm(ip.loadImage("testhist_G.tiff") - ip.loadImage("hist_G.tiff")))
    if np.linalg.norm(ip.loadImage("testhist_G.tiff") - ip.loadImage("hist_G.tiff")) > 10000:
        print("histogram() error for G channel, RGB input")
        plt.close('all')
        plt.figure(1)
        ip.showImage(ip.loadImage("testhist_G.tiff"))
        plt.title("Got")
        plt.figure(2)
        ip.showImage(ip.loadImage("hist_G.tiff"))
        plt.title("Expected")
        plt.show()
        quit()
    plt.figure(3)
    ip.histogram(x.copy(), channel="B", bins=32)
    plt.savefig("testhist_B.tiff")
    print("Histogram diff debug B: ", np.linalg.norm(ip.loadImage("testhist_B.tiff") - ip.loadImage("hist_B.tiff")))
    if np.linalg.norm(ip.loadImage("testhist_B.tiff") - ip.loadImage("hist_B.tiff")) > 10000:
        print("histogram() error for B channel, RGB input")
        plt.close('all')
        plt.figure(1)
        ip.showImage(ip.loadImage("testhist_B.tiff"))
        plt.title("Got")
        plt.figure(2)
        ip.showImage(ip.loadImage("hist_B.tiff"))
        plt.title("Expected")
        plt.show()
        quit()
    plt.figure(4)
    ip.histogram(x.copy(), channel="L", bins=32)
    plt.savefig("testhist_L.tiff")
    print("Histogram diff debug L: ", np.linalg.norm(ip.loadImage("testhist_L.tiff") - ip.loadImage("hist_L.tiff")))
    if np.linalg.norm(ip.loadImage("testhist_L.tiff") - ip.loadImage("hist_L.tiff")) > 10000:
        print("histogram() error for L channel, RGB input")
        plt.close('all')
        plt.figure(1)
        ip.showImage(ip.loadImage("testhist_L.tiff"))
        plt.title("Got")
        plt.figure(2)
        ip.showImage(ip.loadImage("hist_L.tiff"))
        plt.title("Expected")
        plt.show()
        quit()
    plt.figure(5)
    print("Testing histogram() with HSL input")
    y = ip.rgb2hsl(x.copy())
    ip.histogram(y.copy(), channel="R", format="HSL", bins=32)
    plt.savefig("testhist_R.tiff")
    print("Histogram diff debug R: ", np.linalg.norm(ip.loadImage("testhist_R.tiff") - ip.loadImage("hist_R.tiff")))
    if np.linalg.norm(ip.loadImage("testhist_R.tiff") - ip.loadImage("hist_R.tiff")) > 10000:
        print("histogram() error for R channel, HSL input")
        plt.close('all')
        plt.figure(1)
        ip.showImage(ip.loadImage("testhist_R.tiff"))
        plt.title("Got")
        plt.figure(2)
        ip.showImage(ip.loadImage("hist_R.tiff"))
        plt.title("Expected")
        plt.show()
        quit()
    plt.figure(6)
    ip.histogram(y.copy(), channel="G", format="HSL", bins=32)
    plt.savefig("testhist_G.tiff")
    print("Histogram diff debug G: ", np.linalg.norm(ip.loadImage("testhist_G.tiff") - ip.loadImage("hist_G.tiff")))
    if np.linalg.norm(ip.loadImage("testhist_G.tiff") - ip.loadImage("hist_G.tiff")) > 10000:
        print("histogram() error for G channel, HSL input")
        plt.close('all')
        plt.figure(1)
        ip.showImage(ip.loadImage("testhist_G.tiff"))
        plt.title("Got")
        plt.figure(2)
        ip.showImage(ip.loadImage("hist_G.tiff"))
        plt.title("Expected")
        plt.show()
        quit()
    plt.figure(7)
    ip.histogram(y.copy(), channel="B", format="HSL", bins=32)
    plt.savefig("testhist_B.tiff")
    print("Histogram diff debug B: ", np.linalg.norm(ip.loadImage("testhist_B.tiff") - ip.loadImage("hist_B.tiff")))
    if np.linalg.norm(ip.loadImage("testhist_B.tiff") - ip.loadImage("hist_B.tiff")) > 10000:
        print("histogram() error for B channel, HSL input")
        plt.close('all')
        plt.figure(1)
        ip.showImage(ip.loadImage("testhist_B.tiff"))
        plt.title("Got")
        plt.figure(2)
        ip.showImage(ip.loadImage("hist_B.tiff"))
        plt.title("Expected")
        plt.show()
        quit()
    plt.figure(8)
    ip.histogram(y.copy(), channel="L", format="HSL", bins=32)
    plt.savefig("testhist_L.tiff")
    print("Histogram diff debug L: ", np.linalg.norm(ip.loadImage("testhist_L.tiff") - ip.loadImage("hist_L.tiff")))
    if np.linalg.norm(ip.loadImage("testhist_L.tiff") - ip.loadImage("hist_L.tiff")) > 10000:
        print("histogram() error for L channel, HSL input")
        plt.close('all')
        plt.figure(1)
        ip.showImage(ip.loadImage("testhist_L.tiff"))
        plt.title("Got")
        plt.figure(2)
        ip.showImage(ip.loadImage("hist_L.tiff"))
        plt.title("Expected")
        plt.show()
        quit()
    plt.figure(9)
    print("Testing histogram() log output")
    ip.histogram(x.copy(), channel="R", scale="log", bins=32)
    plt.savefig("testhist_R_log.tiff")
    print("Histogram diff debug R: ", np.linalg.norm(ip.loadImage("testhist_R_log.tiff") - ip.loadImage("hist_R_log.tiff")))
    if np.linalg.norm(ip.loadImage("testhist_R_log.tiff") - ip.loadImage("hist_R_log.tiff")) > 10000:
        print("histogram() error for R channel, RGB input, log output")
        plt.close('all')
        plt.figure(1)
        ip.showImage(ip.loadImage("testhist_R_log.tiff"))
        plt.title("Got")
        plt.figure(2)
        ip.showImage(ip.loadImage("hist_R_log.tiff"))
        plt.title("Expected")
        plt.show()
        quit()
    plt.figure(10)
    ip.histogram(y.copy(), channel="L", format="HSL", scale="log", bins=32)
    plt.savefig("testhist_L_log.tiff")
    print("Histogram diff debug L: ", np.linalg.norm(ip.loadImage("testhist_L_log.tiff") - ip.loadImage("hist_L_log.tiff")))
    if np.linalg.norm(ip.loadImage("testhist_L_log.tiff") - ip.loadImage("hist_L_log.tiff")) > 10000:
        print("histogram() error for L channel, HSL input, log output")
        plt.close('all')
        plt.figure(1)
        ip.showImage(ip.loadImage("testhist_L_log.tiff"))
        plt.title("Got")
        plt.figure(2)
        ip.showImage(ip.loadImage("hist_L_log.tiff"))
        plt.title("Expected")
        plt.show()
        quit()
    print("histogram() tests PASSED")

if checkUnsharpMask:
    plt.close('all')
    print("Double checking saveImage()")
    xTrue = np.array( [[ [-1, 256, -1], [0,0,0], [256, 256, 256] ]])
    ip.saveImage(xTrue, "smallTestSave.png", scale=False)
    xTrue[xTrue > 255] = 255
    xTrue[xTrue < 0] = 0
    x = np.uint8(np.round(ip.loadImage("smallTestSave.png")))
    if x[0,0,0] != 0:
        print("saveImage() error: clipping did not saturate negative numbers to zero")
        print("Input:")
        print(np.array( [[ [-1, 256, -1], [0,0,0], [256, 256, 256] ]]))
        print("Expected:")
        print(xTrue)
        print("Got:")
        print(x)
        quit()
    if x[0,0,1] != 255:
        print("saveImage() error: clipping did not saturate numbers over 255 to 255")
        print("Input:")
        print(np.array( [[ [-1, 256, -1], [0,0,0], [256, 256, 256] ]]))
        print("Expected:")
        print(xTrue)
        print("Got:")
        print(x)
        quit()
    print("Image saving PASSED")

    print("Testing unsharpmask()")
    x = ip.loadImage("Hopper.tiff")
    ip.saveImage(ip.unsharpMask(x.copy()), "testunsharp-defaults.tiff")
    ip.saveImage(ip.unsharpMask(x.copy(), radius=50), "testunsharp-r50.tiff")
    y = ip.rgb2hsl(x.copy())
    ip.saveImage(ip.unsharpMask(y.copy(), radius=2, amount=100, format="HSL"), "testunsharp-r2a100.tiff")

    print("unsharpMask diff debug 1: ", np.linalg.norm(ip.loadImage("testunsharp-defaults.tiff") - ip.loadImage("unsharp-defaults.tiff")))
    print("unsharpMask diff debug 2: ", np.linalg.norm(ip.loadImage("testunsharp-r50.tiff") - ip.loadImage("unsharp-r50.tiff")))
    print("unsharpMask diff debug 3: ", np.linalg.norm(ip.loadImage("testunsharp-r2a100.tiff") - ip.loadImage("unsharp-r2a100.tiff")))

    t1 = np.linalg.norm(ip.loadImage("testunsharp-defaults.tiff") - ip.loadImage("unsharp-defaults.tiff")) > 10000
    t2 = np.linalg.norm(ip.loadImage("testunsharp-r50.tiff") - ip.loadImage("unsharp-r50.tiff")) > 10000
    t3 = np.linalg.norm(ip.loadImage("testunsharp-r2a100.tiff") - ip.loadImage("unsharp-r2a100.tiff")) > 10000

    if t1 or t2 or t3:
        print("unsharp() error")
        if t1:
            plt.figure(1)
            plt.title("Expected")
            ip.showImage(ip.loadImage("unsharp-defaults.tiff"))
            plt.figure(2)
            plt.title("Got")
            ip.showImage(ip.loadImage("testunsharp-defaults.tiff"))
        if t2:
            plt.figure(3)
            plt.title("Expected")
            ip.showImage(ip.loadImage("unsharp-r50.tiff"))
            plt.figure(4)
            plt.title("Got")
            ip.showImage(ip.loadImage("testunsharp-r50.tiff"))
        if t3:
            print("unsharp() error with HSL input")
            plt.figure(5)
            plt.title("Expected")
            ip.showImage(ip.loadImage("unsharp-r2a100.tiff"))
            plt.figure(6)
            plt.title("Got")
            ip.showImage(ip.loadImage("testunsharp-r2a100.tiff"))
        plt.show()
        quit()

    print("unsharpMask() PASSED")
    quit()


