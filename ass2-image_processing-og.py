import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy.ndimage


def loadImage(filename):
    img = mpimg.imread(filename)
    (rows, cols, colourChannels) = img.shape

    # Discard alpha channel if present
    if colourChannels == 4:
        img = img[:,:,0:3]

    img64 = np.float64(img)

    # Handle 0..1 value floating point images
    if type(img[0,0,0]) == np.float32:
        img64 *= 255

    return img64


def saveImage(imageData, filename, scale='False', format="RGB"):
    img = imageData.copy()
    if scale == 'True':  # Scale intensity between 0 and 255
        img -= np.min(img)
        img /= np.max(img)
        img *= 255
    else:
        img[img > 255] = 255  # Clip at 255
        img[img < 0] = 0

    if format == 'HSL':
        img = hsl2rgb(img)
    img = np.uint8(np.round(img))
    plt.imshow(img)
    plt.imsave(filename)


def showImage(imageData):
    img = imageData.copy()
    img[img > 255] = 255  # Clip at 255
    img[img < 0] = 0      # Clip at 0
    img = np.uint8(np.round(img))
    plt.axis('off')
    plt.imshow(img)


def rgb2hsl(imageData):
    R2 = imageData[:,:,0] / 255
    G2 = imageData[:,:,1] / 255
    B2 = imageData[:,:,2] / 255
    Cmax = np.max(R2, G2, B2)
    Cmin = np.min(R2, G2, B2)
    D = Cmax - Cmin
    L = (Cmax + Cmin) / 2

    if D == 0:
        H = 0
        S = 0
    else:
        S = D / (1 - np.abs(2*L - 1))
        if Cmax == R2:
            H = 60 * np.mod((G2 - B2) / D, 6)
        elif Cmax == G2:
            H = 60 * ((B2 - R2) / D + 2)
        elif Cmax == B2:
            H = 60 * ((R2 - G2) / D + 4)

    img = imageData.copy()
    img[:,:] = [H,S,L]

    return img


def hsl2rgb(imageData):
    H = imageData[:,:,0]
    S = imageData[:,:,1]
    L = imageData[:,:,2]
    C = (1 - np.abs(2*L - 1)) * S
    X = C * (1 - np.abs(np.mod(H / 60, 2) - 1))
    m = L - C / 2

    if 0 <= H < 60:
        R2 = C; G2 = X; B2 = 0
    elif 60 <= H < 120:
        R2 = X; G2 = C; B2 = 0
    elif 120 <= H < 180:
        R2 = 0; G2 = C; B2 = X
    elif 180 <= H < 240:
        R2 = 0; G2 = X; B2 = C
    elif 240 <= H < 300:
        R2 = X; G2 = 0; B2 = C
    elif 300 <= H < 360:
        R2 = C; G2 = 0; B2 = X

    (R,G,B) = ((R2 + m) * 255), ((G2 + m) * 255), ((B2 + m) * 255)

    img = imageData.copy()
    img[:,:] = [R,G,B]

    return img

def brightness(imageData, b, changeType="absolute", format="RGB"):
    img = imageData.copy()

    if format == "HSL":
        img = hsl2rgb(img)
    elif format != "RGB":
        print("Error: '{}' is not a valid format!".format(format))
        return

    if changeType == "absolute":
        print("blah blah")
    elif changeType == "relative":
        print("blah blah")
    else:
        print("Error: '{}' is not a valid change type!".format(changeType))
        return


