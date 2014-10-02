# Starter program for photolab assignment.
# Author: Sherri Goings
# Created 9/30/2010, last updated 4/30/2013.
# Updated by Jadrian Miles to work with the new image library 2014-05-06.
# Completed by Aditya Subramanian 2014-05-08.

from imageManip import *
import sys

def oneColor(image, color):
    if color == "r" or color == "g" or color == "b":
        new_image = image.copy()
        NumPixels = new_image.getNumPixels()
        for i in range(NumPixels):
            if color == 'r':
                new_image.setPixel1D(i, [new_image.getPixel1D(i)[0], 0, 0])
            elif color == 'g':
                new_image.setPixel1D(i, [0, new_image.getPixel1D(i)[1], 0])
            elif color == 'b':
                new_image.setPixel1D(i, [0, 0, new_image.getPixel1D(i)[2]])
        #window = DisplayWindow(new_image.getWidth(), new_image.getHeight())
        #new_image.draw(window)
        #raw_input("Hit [Enter] to continue. ")
        return new_image
    else:
        print  "I didn't understand that, please try again!"
    return

def invert(image):
    new_image = image.copy()
    NumPixels = new_image.getNumPixels()
    for i in range(NumPixels):
        new_image.setPixel1D(i, [255-new_image.getPixel1D(i)[0], 255-new_image.getPixel1D(i)[1], 255-new_image.getPixel1D(i)[2]])
    #window = DisplayWindow(new_image.getWidth(), new_image.getHeight())
    #new_image.draw(window)
    #raw_input("Hit [Enter] to continue. ")
    return new_image

def greyscale(image):
    new_image = image.copy()
    NumPixels = new_image.getNumPixels()
    for i in range(NumPixels):
        average = sum([new_image.getPixel1D(i)[0], new_image.getPixel1D(i)[1], new_image.getPixel1D(i)[2]])/3
        new_image.setPixel1D(i, [average, average, average])
    #window = DisplayWindow(new_image.getWidth(), new_image.getHeight())
    #new_image.draw(window)
    #raw_input("Hit [Enter] to continue. ")
    return new_image

def saturate(image):
    new_image = image.copy()
    NumPixels = new_image.getNumPixels()
    k = float(raw_input('By how much do you want to enhance the image? '))
    for i in range(NumPixels):
        saturated = saturatedRgb(new_image.getPixel1D(i), k)
        new_image.setPixel1D(i, [saturated[0], saturated[1], saturated[2]])
    #window = DisplayWindow(new_image.getWidth(), new_image.getHeight())
    #new_image.draw(window)
    #raw_input("Hit [Enter] to continue. ")
    return new_image

def saturatedRgb(rgb, k):
    """Given an RGB color triplet (a list or tuple), and a number k,
    returns an RGB color triplet representing the original color
    saturated to the appropriate intensity as determined by k."""
    r = clipColor((.3+.7*k)*rgb[0] + .6*(1-k)*rgb[1] + .1*(1-k)*rgb[2])
    g = clipColor(.3*(1-k)*rgb[0] + (.6+.4*k)*rgb[1] + .1*(1-k)*rgb[2])
    b = clipColor(.3*(1-k)*rgb[0] + .6*(1-k)*rgb[1] + (.1+.9*k)*rgb[2])
    return (r, g, b)

def clipColor(intensity):
    return int(min(255, max(0, intensity)))

def replaceWallWithColor(image, color):
    new_image = image.copy()
    NumPixels = new_image.getNumPixels()
    for i in range(NumPixels):
        high_enough = False
        close_enough = False
        pixclr = new_image.getPixel1D(i)
        if pixclr[0] > 100 and pixclr[1] > 100 and pixclr[2] > 100:
            high_enough = True
        if pixclr[0] + 25 > pixclr[1] and pixclr[1] + 25 > pixclr[2] and pixclr[2] + 25 > pixclr[0]:
            close_enough = True
        if close_enough == True and high_enough == True:
            new_image.setPixel1D(i, color)
  #   window = DisplayWindow(new_image.getWidth(), new_image.getHeight())
#     new_image.draw(window)
#     raw_input("Hit [Enter] to continue. ")
    return new_image

def replaceWallWithImage(orig_img, replacement_img):
    new_image = replaceWallWithColor(orig_img, [102,255,0])
    NumPixels = new_image.getNumPixels()
    for i in range(NumPixels):
        pixclr = new_image.getPixel1D(i)
        if pixclr == [102,255,0]:
            new_image.setPixel1D(i, replacement_img.getPixel1D(i))
    #window = DisplayWindow(new_image.getWidth(), new_image.getHeight())
    #new_image.draw(window)
    #raw_input("Hit [Enter] to continue. ")
    return new_image

def rotate_left(image):
    width= image.getWidth()
    height = image.getHeight()
    new_image = createEmptyImage(height, width)
    for x in range(width):
        for y in range(height):
            new_image.setPixel2D( y, width - x, image.getPixel2D(x, y))

    #window = DisplayWindow(new_image.getWidth(), new_image.getHeight())
    #new_image.draw(window)
    #raw_input("Hit [Enter] to continue. ")
    return new_image

def blur(image, radius):
    if radius <= 0:
        print "lol no"
        return None
    width= image.getWidth()
    height = image.getHeight()
    new_image = createEmptyImage(width, height)
    for x in range(width):
        for y in range(height):
            avg_r = 0
            avg_g = 0
            avg_b = 0
            for i in range(2*radius+1):
                avg_r = image.getPixel2D((x-radius+i)%width, y)[0] + image.getPixel2D(x, (y-radius+i)%height)[0] + avg_r
                avg_b = image.getPixel2D((x-radius+i)%width, y)[2] + image.getPixel2D(x, (y-radius+i)%height)[2] + avg_b
                avg_g = image.getPixel2D((x-radius+i)%width, y)[1] + image.getPixel2D(x, (y-radius+i)%height)[1] + avg_g
            new_image.setPixel2D(x, y, [avg_r/(1+(4*radius)), avg_g/(1+(4*radius)), avg_b/(1+(4*radius))])
    window = DisplayWindow(new_image.getWidth(), new_image.getHeight())
    new_image.draw(window)
    raw_input("Hit [Enter] to continue. ")
    return new_image

def rescale(image, scale):
    width= image.getWidth()
    height = image.getHeight()
    if scale <= 0:
        print "lol no"
        return None
    new_image = createEmptyImage(width*scale, height*scale)
    width_new = new_image.getWidth()
    height_new = new_image.getHeight()
    for x in range(width_new):
        for y in range(height_new):
            new_image.setPixel2D(x, y, image.getPixel2D(int(x/scale), int(y/scale)))
    #window = DisplayWindow(new_image.getWidth(), new_image.getHeight())
    #new_image.draw(window)
    #raw_input("Hit [Enter] to continue. ")
    return new_image


def main():
    """Tests all photolab functions."""
    # Make sure user enters an image file on the command line.
    if len(sys.argv) < 2:
        print "Usage: python photolab1.py <filename>"
        print "  where <filename> is an image file."
        return

    # Open file given as a command line argument.
    orig_image = Image(sys.argv[1])

##    a = oneColor(orig_image, raw_input('Please enter either "r", "g", or "b": '))
##    b = invert(orig_image)
##    c = greyscale(orig_image)
##    d = saturate(orig_image)
##    e = replaceWallWithColor(orig_image, [102,255,0])
##    f = replaceWallWithImage(orig_image, Image(raw_input('What is the name of your background image? ')))
##    g = rotate_left(orig_image)
    h = blur(orig_image, int(raw_input('What is your blur radius? ')))
##    i = rescale(orig_image, float(raw_input('What is your scale? ')))


if __name__ == "__main__":
    main()
