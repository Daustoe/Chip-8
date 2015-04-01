__author__ = 'Clayton Powell'
from chipy8 import chip8
import pyglet
import sys
import argparse


def intro_update(dt):
    """
    Update method for both intro sequence.
    :param dt:
    """
    if emulator.cpu.opcode != 0x1210:
        emulator.cpu.cycle()
    else:
        pyglet.clock.unschedule(intro_update)
        pyglet.clock.schedule_once(start, 3)


def start(dt):
    """
    loads the chosen rom for the chip8 emulator
    """
    emulator.clear()
    emulator.load_rom(args.rom)
    pyglet.clock.schedule_interval(emulator.main, 1/1000)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", type=str, help="File path to the Chip8 Rom you wish to run.")
    args = parser.parse_args()
    template = pyglet.gl.Config(double_buffer=False)
    emulator = chip8.Chip8(640, 320, config=template)
    emulator.load_rom('chipy8/resources/programs/Chip8 emulator Logo.ch8')
    pyglet.clock.schedule(intro_update)
    pyglet.app.run()