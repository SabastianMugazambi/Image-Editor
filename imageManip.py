# imageManip.py - an image manipulation program by Sherri Goings
# 

import pygame

class DisplayWindow:
    """A class that describes a display window that can be used 
    for drawing and manipulating Image objects"""

    def __init__(self, width, height):
        """Constructor for a DisplayWindow object."""
        self.display = pygame.display.set_mode((width, height))
        self.display.fill((50,50,50))

    def getSurface(self):
        """Gets the pygame Surface object associated with this DisplayWindow"""
        return self.display

    def update(self):
        """Updates the DisplayWindow's Surface display"""
        pygame.display.flip()

        
class Image:
    """This class describes an image."""

    def __init__(self, filename="", copySurf=None, width=0, height=0):
        """Constructor for an Image object. Can be passed a filename
        to read from, a copy of a surface to use, or a width and height
        to create a new empty Image"""
        if filename:
            try:
                self.surface = pygame.image.load(filename)
            except pygame.error, theError:
                print "Cannot load image:", filename
                raise SystemExit, theError
        elif copySurf:
            self.surface = copySurf
        elif width>0 and height>0:
            self.surface = pygame.Surface((width, height))
            self.surface.fill((50,50,50))
        else:
            print "Error, invalid arguments when attempting to create image"
            raise SystemExit, 1

    def draw(self, window, x=0, y=0):
        """Draws this Image in the given DisplayWindow at the given location"""
        window.getSurface().blit(self.surface, (x,y))
        window.update()

    def getPixel2D(self, x, y):
        """Gets the pixel at the given (x, y) location. 
        Returns a list of 3 ints 0-255"""
        color =  self.surface.get_at((x,y))
        return [color.r, color.g, color.b]

    def setPixel2D(self, x, y, rgb):
        """Sets the pixel at the given (x, y) location. 
        The pixel information needs to be passed as a list of 3 ints, 0-255."""
        self.surface.set_at((x,y), pygame.Color(rgb[0], rgb[1], rgb[2]))

    def getPixel1D(self, n):
        """Gets the pixel at the given index. 
        Returns a list of 3 ints 0-255."""
        color = self.surface.get_at((n%self.surface.get_width(), n/self.surface.get_width()))
        return [color.r, color.g, color.b]

    def setPixel1D(self, n, rgb):
        """Sets the pixel at the given index. 
        The pixel information needs to be passed as a list of 3 ints, 0-255"""
        self.surface.set_at((n%self.surface.get_width(), n/self.surface.get_width()),
                            pygame.Color(rgb[0], rgb[1], rgb[2]))

    def copy(self):
        """Returns a copy of this Image"""
        return Image(copySurf=self.surface.copy())

    def getWidth(self):
        """Gets the width (in pixels) of this Image"""
        return self.surface.get_width()

    def getHeight(self):
        """Gets the height (in pixels) of this Image"""
        return self.surface.get_height()

    def getNumPixels(self):
        """Gets the total number of pixels in this Image"""
        return self.surface.get_width()*self.surface.get_height()

    def save(self, filename):
        """Saves this Image to the given filename"""
        pygame.image.save(self.surface, filename)
    
    

def loadImage(afile):
    """Loads an Image from the given file"""
    return Image(filename=afile)

def createEmptyImage(w, h):
    """Creates an empty Image with width w and height h"""
    return Image(width=w, height=h)

if __name__=="__main__":
    pass
else:
    pygame.init()
