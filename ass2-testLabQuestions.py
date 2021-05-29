'''
ENGG1003, Semester 1, 2021

This script tests the five functions from the "lab" questions on small datasets.

Note that this script requires loadImage() to be working before saveImage() or showImage() can be tested.

REQUIREMENTS:

    * small.png must be in the same folder to check loadImage()
    * Hopper.jpg must be in the same folder to check showImage()
    * showImageCorrect.png must be in the same folder to check showImage()

small.png, smallImage.npy, Hopper.jpg, and showImageCorrect.png can all be found under the "Assignment 2" item on Blackboard...which is where you found this file, so I guess you know where they are.
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
checkLoadImage = True
checkSaveImage = True   # Assumes that loadImage() is working correctly!
checkColourspace = True # Checks both rgb2hsl() and hsl2rgb() at the same time
checkShowImage = True   # Requires loadImage() to be working correctly

try:
    f = open("Hopper.tiff")
except IOError:
    print("smallImage.npy not found - downloading")
    url = "https://github.com/bschulznewy/a2Testing/raw/main/Hopper.tiff"
    x = requests.get(url)
    filename = url.rsplit('/',1)[1]
    print("Saving ", filename)
    open(filename, "wb").write(x.content)

try:
    f = open("small.png")
except IOError:
    print("small.png not found - downloading")
    url = "https://github.com/bschulznewy/a2Testing/raw/main/small.png"
    x = requests.get(url)
    filename = url.rsplit('/',1)[1]
    print("Saving ", filename)
    open(filename, "wb").write(x.content)

try:
    f = open("showImageCorrect.png")
except IOError:
    print("showImageCorrect.png not found - downloading")
    url = "https://github.com/bschulznewy/a2Testing/raw/main/showImageCorrect.png"
    x = requests.get(url)
    filename = url.rsplit('/',1)[1]
    print("Saving ", filename)
    open(filename, "wb").write(x.content)

print("All prerequesite files downloaded")

if checkLoadImage == True:
    print("Checking image loading")
    x = ip.loadImage("Hopper.tiff")
    if x.size != 783363:
        print("Loading Hopper.tiff did not return an image of the correct resolution")
        print("Expected (511, 511, 3)")
        print("Got ", x.size)
    x = ip.loadImage("small.png")
    xTrue = np.float64(np.array( [[[255,0,0],[0,255,0],[0,0,255]],[[255,255,255,],[120,120,120],[0,0,0]],[[161,140,167],[104,143,145],[189,181,107]]] ))
    if x.dtype != np.float64:
        print(f"LoadImage() error: data type {x.dtype} not np.float64")
        quit()
    if x.max() != 255 or x.min() != 0:
        print(f"LoadImage() error: Incorrect scaling max is {x.max()} instead of 255 or min is {x.min} instead of 0")
        quit()
    if (np.array_equal(x, xTrue) == False) and (np.array_equal(np.round(x),np.round(xTrue) == False)):
        print("Loaded array differs from expected data")
        print("Loaded:")
        print(x)
        print("Expected:")
        print(xTrue)
        quit()
    print("Image loading PASSED")

if checkSaveImage == True:
    print("Checking image saving")
    xTrue = np.float64(np.array( [[[255,0,0],[0,255,0],[0,0,255]],[[255,255,255,],[120,120,120],[0,0,0]],[[161,140,167],[104,143,145],[189,181,107]]] ))
    ip.saveImage(xTrue, "smallTestSave.tiff", scale=False)
    x = ip.loadImage("smallTestSave.tiff")
    if np.array_equal(x, xTrue) == False:
        print("saveImage() error: saved image differs from given data")
        print("Saved data:")
        print(x)
        print("Expected:")
        print(xTrue)
        quit()
    xTrue = np.array( [[ [-100, -100, -100], [0,0,0], [100, 100, 100] ]])
    ip.saveImage(xTrue, "smallTestSave.png", scale=True)
    x = np.round(ip.loadImage("smallTestSave.png"))
    xTrue1 = np.array( [[ [0,0,0], [127, 127, 127], [255,255,255] ]])
    xTrue2 = np.array( [[ [0,0,0], [128, 128, 128], [255,255,255] ]])
    if (np.array_equal(x, xTrue1) == False) and (np.array_equal(x, xTrue2) == False):
        print("saveImage scaling produced an error")
        print("Got:")
        print(x)
        print("Expected:")
        print(xTrue1)
        print("Or:")
        print(xTrue2)
        print("When writing:")
        print(np.array([[ [-100, -100, -100], [0,0,0], [100, 100, 100] ]]))
        quit()
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

if checkColourspace == True:
    print("Checking colourspace conversion")
    print("Checking against small.png")
    x = ip.loadImage("small.png")
    got = ip.rgb2hsl(x.copy())
    expected = np.array([[[0.00000000e+00, 1.00000000e+00, 5.00000000e-01], [1.20000000e+02, 1.00000000e+00, 5.00000000e-01],  [2.40000000e+02, 1.00000000e+00, 5.00000000e-01]], [[0.00000000e+00, 0.00000000e+00, 1.00000000e+00],  [0.00000000e+00, 0.00000000e+00, 4.70588237e-01],  [0.00000000e+00, 0.00000000e+00, 0.00000000e+00]], [[2.86666667e+02, 1.33004926e-01, 6.01960808e-01],  [1.82926829e+02, 1.64658650e-01, 4.88235310e-01],  [5.41463420e+01, 3.83177592e-01, 5.80392167e-01]]])
    if np.linalg.norm(got-expected) > 1e-5:
        print("rgb2hsl() error with small.png")
        print("Got:")
        print(got)
        print("Expected:")
        print(expected)
        quit()
    print("small.png check PASSED")
    tmp = np.zeros((1,1,3))
    for r in range(0,256,5):
        print(f"{r/255*100:.2f} % Complete")
        for g in range(0,256,5):
            for b in range(0,256,5):
                tmp[0,0,:] = (r,g,b)
                tmpOut = ip.hsl2rgb(ip.rgb2hsl(tmp.copy()))
                err = np.linalg.norm(tmp - tmpOut)
                if err > 1e-6:
                    print("Colourspace conversion error for RGB triplet: ", r, g, b)
                    print("rgb2hsl() output: ", ip.rgb2hsl(tmp.copy()))
                    print("Output from hsl2rgb( rgb2hsl( ) ): ", ip.hsl2rgb(ip.rgb2hsl(tmp)))
                    print("Expected: ", np.array((r,g,b)))
                    quit()
    print("rgb2hsl() and hsl2rgb() PASSED")

if checkShowImage == True:
    print("Checking showImage()")
    x = ip.loadImage("Hopper.tiff")
    x[:,:,0] += 100
    x[:,:,1] -= 10
    ip.showImage(x)
    plt.savefig("showImageResult.png")
    expected = ip.loadImage("showImageCorrect.png")
    got = ip.loadImage("showImageResult.png")

    print("ShowImage debug diff: ", np.linalg.norm(expected - got))

    if np.linalg.norm(expected - got) > 2000:
        print("showImage error: Did not get expected plot image. This could be due to a lack of clipping, lack of datatype conversion, or lack of plt.axis('off')")
        print("figure 1 is expected image, figure 2 is what was produced")

        plt.figure(1)
        plt.imshow(np.uint8(ip.loadImage("showImageCorrect.png")))
        plt.title('Expected Result')
        plt.axis('off')
        plt.figure(2)
        plt.imshow(np.uint8(ip.loadImage("showImageResult.png")))
        plt.axis('off')
        plt.title('Produced Result')
        plt.show()
        quit()
    print("showImage() PASSED")
