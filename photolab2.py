# Updated by Student: Sabastian Mugazambi to edit an image color.
# Starter program by : Sherri Goings
# Created 9/30/2010, last updated 05/12/2014
# Updated by Jadrian Miles to work with the new image library 2014-05-06.

from imageManip import *
import sys
import math
import pygame


def oneColor(image, color):
    """Given an image and a color choice either as a full word or starting
    letter only (e.g red or just r); converts the whole image to the
    desired color maintaining the value of the requested color"""
    #color = raw_input("What single color do you want?")
    #I could have put raw input so that the user enters what color they want but
    #according to the example main function given it seems like the user
    #is already calling main with the right arguments.

    s_color = image.copy()

    #loop that directs the program to convert the image to the right requested color.
    if color.startswith("r"):
        for x in range(s_color.getNumPixels()):
            pixel = s_color.getPixel1D(x)
            s_color.setPixel1D(x, (pixel[0],0,0))
    elif color.startswith("g"):
        for x in range(s_color.getNumPixels()):
            pixel = s_color.getPixel1D(x)
            s_color.setPixel1D(x, (0,pixel[1],0))
    elif color.startswith("b"):
        for x in range(s_color.getNumPixels()):
            pixel = s_color.getPixel1D(x)
            s_color.setPixel1D(x, (0,0, pixel[2]))

    return s_color

def greyscale(image):
    """Convertin the image to grayscale by setting every pixel
    to the average value of every color"""
    #creating a copy to be edited.
    s_greyscale = image.copy()
    for x in range(s_greyscale.getNumPixels()):
        pixel = s_greyscale.getPixel1D(x)
        average = (pixel[0]+pixel[1]+pixel[2])/3
        s_greyscale.setPixel1D(x, (average,average,average))

    return s_greyscale

def invert(image):
    """Inverting the picture by subtracting every Rgb_color value from 255."""
    s_inverted = image.copy()
    for x in range(s_inverted.getNumPixels()):
        pixel = s_inverted.getPixel1D(x)
        s_inverted.setPixel1D(x, (255-pixel[0],255-pixel[1],255-pixel[2]))

    return s_inverted

def saturate(image, k):
    """ Saturating the image by calling the saturatedRgb function with the
    arguments taken from the Rgb_color values of each pixel."""
    s_saturate = image.copy()
    for x in range(s_saturate.getNumPixels()):
        pixel = s_saturate.getPixel1D(x)
        s_saturate.setPixel1D(x, saturatedRgb((pixel[0],pixel[1],pixel[2]), k))

    return s_saturate

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
    """Rplaces the uniform background with a specified color and produces a
    picture with the changed background."""
    s_replace = image.copy()
    for p in range(s_replace.getNumPixels()):
        x = s_replace.getPixel1D(p)
        if abs((x[0]-x[1]))<30 and abs((x[0]-x[2]))<30 and abs((x[1]-x[2]))<30 and x[0]>100 and x[1]>100:
            s_replace.setPixel1D(p, color)

    return s_replace

def replaceWallWithImage(image, replacement):
    """Replaces the wall or background in an image with another chosen image"""
    org_img = image.copy()
    replacement_img = replacement.copy()

    #looping around the all the pixels and identifying background pixels to be
    #replaced and replacing them
    for p in range(org_img.getNumPixels()):
        x = org_img.getPixel1D(p)
        y = replacement_img.getPixel1D(p)
        if abs((x[0]-x[1]))<30 and abs((x[0]-x[2]))<30 and abs((x[1]-x[2]))<30 and x[0]>100 and x[1]>100:
            org_img.setPixel1D(p, y)

    return org_img

def rotateLeftImage(image):
    """Rotates the image 90 degrees anti clockwise but fails to get rid of the old image. """
    s_rotate = image.copy()
    new = createEmptyImage(image.getHeight(),image.getWidth())

    #Transposing the coodinates of every pixel by interchanging the x and y coordinates.
    for coordinate in range(image.getWidth()):
        x = coordinate
        for coordinate in range(image.getHeight()):
            y = coordinate
            c = s_rotate.getPixel2D(x,y)
            new.setPixel2D(y,x,c)

    return new

def blur(image, radius):
    """Creates a blurred replica of the original image."""
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
    """Scales the image up or down according to the choice of the user."""
    rescale = image.copy()

    #creates a new empty image to add the pixels that have been rescaled.
    new = createEmptyImage(int(rescale.getWidth()*scale),int(rescale.getHeight()*scale))
    for co in range(rescale.getWidth()):
        x = co
        for co in range(rescale.getHeight()):
            y = co
            new_pixel = rescale.getPixel2D(x,y)
            new.setPixel2D(int(x*scale),int(y*scale),new_pixel)
    return new

def main():
    """Tests all photolab functions."""
    if len(sys.argv) < 2:
        print "Usage: python photolab1.py <filename>"
        print "  where <filename> is an image file."
        return

    # Open file given as a command line argument.
    image = Image(sys.argv[1])
    replacement = Image(sys.argv[2])


    # Display the image.
    window = DisplayWindow(1024, 768)
    image.draw(window)


    #Commented out functions that test the different functions
##    rescale(image,0.25).draw(window)
    #replaceWallWithImage(image, replacement).draw(window)
    #rotateLeftImage(image).draw(window)
    #replaceWallWithColor(image, (0,255,0)).draw(window)
    #invert(image).draw(window)
    blur(image, 3).draw(window)
    #greyscale(image).draw(window)
    #saturate(image, k).draw(window)
    raw_input("Hit [Enter] to quit. ")

if __name__ == "__main__":
    main()
