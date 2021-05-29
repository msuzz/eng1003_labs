import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import scipy.ndimage as nd

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


def saveImage(imageData, filename, scale=False, format="RGB"):
    img = imageData.copy()
    if scale == True:  # Scale intensity between 0 and 255
        img -= np.min(img)
        img = img / np.max(img)
        img *= 255
    else:
        img[img > 255] = 255  # Clip at 255
        img[img < 0] = 0

    if format == 'HSL': img = hsl2rgb(img)

    plt.imsave(filename, np.uint8(np.round(img)))
    return None


def showImage(imageData):
    img = imageData.copy()
    img[img > 255] = 255  # Clip at 255
    img[img < 0] = 0      # Clip at 0
    img = np.uint8(np.round(img))
    plt.axis('off')
    plt.imshow(img)

def rgb2hsl(imageData):
    (rows, cols, colorLength) = imageData.shape
    for row in range(0,rows):
        for col in range(0,cols):
            (R, G, B) = imageData[row,col,:]

            (R2, G2, B2) = np.array((R, G, B))/255

            Cmax = np.max(np.array((R2, G2, B2)))
            Cmin = np.min(np.array((R2, G2, B2)))
            D = Cmax - Cmin
            if D == 0:
                H = 0
            elif Cmax == R2:
                H = 60*np.mod((G2-B2)/D,6)
            elif Cmax == G2:
                H = 60*((B2-R2)/D + 2)
            else:
                H = 60*((R2-G2)/D + 4)
            L = (Cmax + Cmin)/2
            if D == 0:
                S = 0
            else:
                S = D/( 1- np.abs(2*L-1))

            imageData[row,col,:] = (H, S, L)
    return imageData

def hsl2rgb(imageData):
    (rows, cols, colorLength) = imageData.shape
    for row in range(0,rows):
        for col in range(0,cols):
            (H, S, L) = imageData[row,col,:]
            C = (1-np.abs(2*L-1))*S
            X = C*(1-np.abs(np.mod(H/60,2)-1))
            m = L-C/2
            if 0 <= H < 60:
                (R2, G2, B2) = (C,X,0)
            if 60 <= H < 120:
                (R2, G2, B2) = (X,C,0)
            if 120 <= H < 180:
                (R2, G2, B2) = (0,C,X)
            if 180 <= H < 240:
                (R2, G2, B2) = (0,X,C)
            if 240 <= H < 300:
                (R2, G2, B2) = (X,0,C)
            if 300 <= H < 360:
                (R2, G2, B2) = (C,0,X)
            (R,G,B) = ( (R2+m)*255, (G2+m)*255, (B2+m)*255 )
            imageData[row,col,:] = (R,G,B)
    return imageData


def brightness(imageData, brt, changeType="absolute", format="RGB"):
    img = imageData.copy()

    if format == "HSL":
        img = hsl2rgb(img)
    elif format != "RGB":
        print("Error: '{}' is not a valid format parameter!".format(format))
        return imageData

    if changeType == "absolute":
        img += brt
    elif changeType == "relative":
        img *= brt
    else:
        print("Error: '{}' is not a valid changeType parameter!".format(changeType))
        return imageData

    if format == "HSL": img = rgb2hsl(img)
    return img

def contrast(imageData, cont, format="RGB"):
    img = imageData.copy()

    if format == "HSL":
        img = hsl2rgb(img)
    elif format != "RGB":
        print("Error: '{}' is not a valid format parameter!".format(format))
        return imageData

    img = cont * (img - 127.5) + 127.5

    if format == "HSL": img = rgb2hsl(img)
    return img

def saturation(imageData, amt, format="HSL"):
    img = imageData.copy()

    if format == "RGB":
        img = rgb2hsl(img)
    elif format != "HSL":
        print("Error: '{}' is not a valid format parameter!".format(format))
        return imageData

    img[:,:,1] *= amt  # Multiply saturation by amount

    if format == "RGB": img = hsl2rgb(img)
    return img

def toneMap(imageData, hue, sat, format="HSL"):
    img = imageData.copy()

    if format == "RGB":
        img = rgb2hsl(img)
    elif format != "HSL":
        print("Error: '{}' is not a valid format parameter!".format(format))
        return imageData

    img[:,:,0] = hue  # Multiply hue by amount
    img[:,:,1] = sat  # Multiply saturation by amount

    if format == "RGB": img = hsl2rgb(img)
    return img

def crop(imageData, top, bot, left, right):
    (rows, cols, colours) = imageData.shape

    if top >= bot:
        print ("Error: top ({}) must be less than bottom ({})!".format(top, bot))
        return imageData
    if left >= right:
        print("Error: left ({}) must be less than right ({})!".format(left, right))
        return imageData
    if top < 0:
        print ("Error: top ({}) must be greater than 0!".format(top))
        return imageData
    if left < 0:
        print ("Error: left ({}) must be greater than 0!".format(left))
        return imageData
    if bot > rows:
        print ("Error: bottom ({}) must be less than the ".format(bot) +
               "vertical resolution ({}) of the original image!".format(rows))
        return imageData
    if right > rows:
        print ("Error: right ({}) must be less than the ".format(right) +
               "horizontal resolution ({}) of the original image!".format(rows))
        return imageData

    return imageData[top:bot, left:right, :]

def saturated(imageData, type="white", format="RGB"):
    if format == "RGB":
        img = imageData[:,:]
    elif format == "HSL":
        img = imageData[:,:,2]
    else:
        print("Error: {} is not a valid format parameter!".format(format))
        return imageData

    if type == "white":
        val = 254.5 if format == "RGB" else 0.99
        count = img[img >= val]
    elif type == "black":
        val = 0.5 if format == "RGB" else 0.01
        count = img[img <= val]
    else:
        print("Error: {} is not a valid type parameter!".format(type))
        return imageData

    if format == "RGB":
        pct = np.size(count) / np.size(imageData) * 100
    else:
        pct = np.size(count) / (np.size(imageData)/3) * 100

    return pct

def histogram(imageData, scale="linear", channel="L", bins=255, format="RGB"):
    if format == "RGB":
        if   channel == "R": img = imageData[:,:,0]
        elif channel == "G": img = imageData[:,:,1]
        elif channel == "B": img = imageData[:,:,2]
        elif channel == "L": img = rgb2hsl(imageData)[:,:,2]
        else: print("Error: {} is not a valid channel parameter!".format(channel)); return
    elif format == "HSL":
        if   channel == "L": img = imageData[:,:,2]
        elif channel == "R": img = hsl2rgb(imageData)[:,:,0]
        elif channel == "G": img = hsl2rgb(imageData)[:,:,1]
        elif channel == "B": img = hsl2rgb(imageData)[:,:,2]
        else: print("Error: {} is not a valid channel parameter!".format(channel)); return
    else:
        print("Error: {} is not a valid format parameter!".format(format))
        return

    if scale == "linear":
        return plt.hist(img.reshape(-1), bins, log=False)
    elif scale == "log":
        return plt.hist(img.reshape(-1), bins, log=True)
    else:
        print("Error: {} is not a valid scale parameter!".format(scale))
        return

def unsharpMask(imageData, radius=5, amount=2, format="RGB"):
    img = imageData.copy()

    if format == "HSL":
        img = hsl2rgb(img)
    elif format != "RGB":
        print("Error: '{}' is not a valid format parameter!".format(format))
        return imageData

    R = img[:,:,0]; G = img[:,:,1]; B = img[:,:,2]
    R_blur = nd.gaussian_filter(R, radius / 3)
    G_blur = nd.gaussian_filter(G, radius / 3)
    B_blur = nd.gaussian_filter(B, radius / 3)
    R_sharp = img[:,:,0] + (img[:,:,0] - R_blur) * amount
    G_sharp = img[:,:,1] + (img[:,:,1] - G_blur) * amount
    B_sharp = img[:,:,2] + (img[:,:,2] - B_blur) * amount
    img[:,:,0] = R_sharp
    img[:,:,1] = G_sharp
    img[:,:,2] = B_sharp

    return img