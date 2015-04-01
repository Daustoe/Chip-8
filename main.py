__author__ = 'Clayton Powell'
from chipy8 import chip8
import pyglet


def intro_sequence():
    """Performs the intro sequence for the emulator, allows game selection."""
    emulator.load_rom('chipy8/resources/programs/Chip8 emulator Logo.ch8')
    pyglet.clock.schedule(intro_update)
    pyglet.app.run()


def intro_update(dt):
    """
    Update method for both intro sequence.
    :param dt:
    """
    if emulator.cpu.opcode != 0x1210:
        emulator.cpu.cycle()
    else:
        pyglet.clock.unschedule(intro_update)
        pyglet.clock.schedule_once(load_rom, 3)


def load_rom(dt):
    """
    loads the chosen rom for the chip8 emulator
    """
    emulator.clear()
    emulator.load_rom('chipy8/resources/games/Pong.ch8')
    pyglet.clock.schedule_interval(main_loop, 1/1000)


def main_loop(dt):
    emulator.main()


if __name__ == '__main__':
    template = pyglet.gl.Config(double_buffer=False)
    emulator = chip8.Chip8(640, 320, config=template)
    intro_sequence()