"""
Notes:
May want to look into PySide or PyQT in order to get a better gui system for our debugger.
"""
import cpu

__author__ = 'Clayton Powell'
import pyglet


class Chip8(pyglet.window.Window):
    """
    Chip 8 emulator class. Subclasses pyglet Window class and contains the cpu of the Chip 8 interpreter.
    :param args:
    :param kwargs:
    """

    def __init__(self, *args, **kwargs):
        super(Chip8, self).__init__(*args, **kwargs)
        self.key_map = {pyglet.window.key._1: 0x1,
                        pyglet.window.key._2: 0x2,
                        pyglet.window.key._3: 0x3,
                        pyglet.window.key._4: 0xc,
                        pyglet.window.key.Q: 0x4,
                        pyglet.window.key.W: 0x5,
                        pyglet.window.key.E: 0x6,
                        pyglet.window.key.R: 0xd,
                        pyglet.window.key.A: 0x7,
                        pyglet.window.key.S: 0x8,
                        pyglet.window.key.D: 0x9,
                        pyglet.window.key.F: 0xe,
                        pyglet.window.key.Z: 0xa,
                        pyglet.window.key.X: 0,
                        pyglet.window.key.C: 0xb,
                        pyglet.window.key.V: 0xf}
        self.pixel = pyglet.image.load('chipy8/resources/pixel.png')
        self.cpu = cpu.CPU()
        self.clear()
        self.set_vsync(False)

    def load_rom(self, rom_path):
        """
        Hands off to the cpu to load the given rom.
        :param rom_path
        """
        self.cpu.load_rom(rom_path)

    def on_key_press(self, symbol, modifiers):
        """
        Determines what should be done on a key press. Overrides the pyglet Window definition of this method. Looks up
        key in self.key_map and hands it to the cpu to use with opcodes.
        :param symbol:
        :param modifiers:
        """
        if symbol in self.key_map.keys():
            self.cpu.key_inputs[self.key_map[symbol]] = 1

    def on_key_release(self, symbol, modifiers):
        """
        Functions the same as the on_key_press, but for key stroke up.
        :param symbol:
        :param modifiers:
        """
        if symbol in self.key_map.keys():
            self.cpu.key_inputs[self.key_map[symbol]] = 0

    def on_draw(self):
        """
        Draw method for the Window.
        """
        if self.cpu.should_draw:
            self.clear()
            for i in range(2048):
                if self.cpu.graphics[i] == 1:
                    self.pixel.blit((i % 64) * 10, 310 - ((i / 64) * 10))
            self.cpu.should_draw = False
            self.flip()