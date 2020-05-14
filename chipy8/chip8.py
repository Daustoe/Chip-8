import chipy8.cpu as cpu
from tkinter import *


class Chip8(Canvas):
    """
    Chip 8 emulator class. Subclasses pyglet Window class and contains the cpu
    of the Chip 8 interpreter.
    :param args:
    :param kwargs:
    """

    def __init__(self, master=None, width=200, height=200):
        """
        Chip8 init function.
        :param master
            Tkinter object
        :param width
            width of display window. Default = 200
        :param height
            height of display window. Default = 200
        """
        Canvas.__init__(self, master=None)
        self.master = master
        self.master.title('Chip 8')
        self.cpu = cpu.CPU(self)
        self.key_map = {'1': 0x1,
                        '2': 0x2,
                        '3': 0x3,
                        '4': 0xc,
                        'q': 0x4,
                        'w': 0x5,
                        'e': 0x6,
                        'r': 0xd,
                        'a': 0x7,
                        's': 0x8,
                        'd': 0x9,
                        'f': 0xe,
                        'z': 0xa,
                        'x': 0,
                        'c': 0xb,
                        'v': 0xf}

    def load_rom(self, rom_path):
        """
        Hands off to the cpu to load the given rom.
        :param rom_path
            system path to ROM to be loaded by emulator
        """
        self.cpu.load_rom(rom_path)

    def main(self, dt):
        """
        Main loop of the emulator. Handles keyboard events and cpu cycle
        :param dt:
            time delta between cpu 'cycles'
        """
        if not self.has_exit:
            self.dispatch_events()
            self.cpu.cycle()

    def on_key_press(self, event):
        """
        Determines what should be done on a key press. Grabs events, and if a
        valid key is pressed for the Chip-8 interpreter, we pass it alongself.
        :param event:
            event object that contains key info
        """
        if event.char in self.key_map.keys():
            self.cpu.key_inputs[self.key_map[event.char]] = 1

    def on_key_release(self, event):
        """
        Same as on_key_press but with key release.
        :param event:
            event object that contains key info
        """
        if event.char in self.key_map.keys():
            self.cpu.key_inputs[self.key_map[event.char]] = 0

    def draw_pixel(self, x, y):
        """
        Draws an individual pixel to the screen. We flip() in specific cpu calls
        where it makes sense.
        :param x:
            x coordinate on the screen
        :param y:
            y coordinate on the screen
        """
        if self.cpu.graphics[x][y] == 1:
            self.white_pixel.blit(x * 10, 310 - y * 10)
        else:
            self.black_pixel.blit(x * 10, 310 - y * 10)
