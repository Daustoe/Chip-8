__author__ = 'Clayton Powell'
from chipy8 import chip8
import pyglet
import cProfile
import pstats


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
        pyglet.clock.schedule(update)


def load_rom(dt):
    """
    loads the chosen rom for the chip8 emulator
    """
    emulator.blit_list = set()
    emulator.load_rom('chipy8/resources/demos/Trip8 Demo.ch8')


def update(dt):
    """
    Update method for both debugger and the cpu.
    :param dt:
    """
    if not emulator.cpu.is_paused:
        emulator.cpu.cycle()

if __name__ == '__main__':
    template = pyglet.gl.Config(double_buffer=False)
    emulator = chip8.Chip8(640, 320, config=template)
    cProfile.run('intro_sequence()', 'stats')
    p = pstats.Stats('stats')
    p.sort_stats('cumulative').print_stats()