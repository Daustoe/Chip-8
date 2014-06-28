__author__ = 'Clayton Powell'
import pyglet
import cpu
"""
Notes:
Want to create an entire debugger for the Chip-8 emulator. This will be nice to have
when we move to upgrading to Super Chip-8.

This includes a view of the registers, a disassembler of the opcodes run, emulation flow
control, and a view of the memory.
"""


class Chip8(pyglet.window.Window):
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
        self.pixel = pyglet.image.load('pixel.png')
        self.cpu = cpu.CPU()
        self.cpu.load_rom('utils/games/Pong.ch8')
        self.clear()

    def on_key_press(self, symbol, modifiers):
        if symbol in self.key_map.keys():
            self.cpu.key_inputs[self.key_map[symbol]] = 1

    def on_key_release(self, symbol, modifiers):
        if symbol in self.key_map.keys():
            self.cpu.key_inputs[self.key_map[symbol]] = 0

    def on_draw(self):
        if self.cpu.should_draw:
            self.clear()
            for i in range(2048):
                if self.cpu.graphics[i] == 1:
                    self.pixel.blit((i % 64) * 10, 310 - ((i / 64) * 10))
            self.cpu.should_draw = False


if __name__ == '__main__':
    emulator = Chip8(640, 320)
    pyglet.clock.schedule_interval(emulator.cpu.cycle, 1/100.0)
    pyglet.app.run()