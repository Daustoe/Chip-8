__author__ = 'cjpowell'
from pyglet import sprite
from pyglet import image
image = image.load('chipy8/resources/pixel.png')


class Pixel(sprite.Sprite):
    """
    Pixel class which is going to represent each individual pixel on the graphics screen for the Chip 8 emulator. Idea
    behind this is that pyglet sprites draw much faster to the screen than blitting an image does. This should help
    speed up our emulator.
    """
    def __init__(self, x, y):
        super(Pixel, self).__init__(image, x=x*10, y=y*10)
        self.active = 0

    def draw(self):
        if self.active == 1:
            super(Pixel, self).draw()