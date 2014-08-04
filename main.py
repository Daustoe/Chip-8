"""
Notes going forward.

Ignoring the flickering, it seems that is how the original Chip8 interpreter functioned.

Current program is using some function of ours that is not working correctly, things I suspect:
on a return from subroutine, we are hoping to next opcode, we may be skipping some stuff.

To check this we need to disassemble the rom itself so we can follow along with each cycle and double
check that everything is working as it should.
"""
__author__ = 'Clayton Powell'
# from chipy8 import debugger
from chipy8 import chip8
import pyglet
from time import sleep


def intro_sequence():
    """Performs the intro sequence for the emulator, allows game selection."""
    emulator.load_rom('chipy8/resources/programs/Chip8 emulator Logo.ch8')
    pyglet.clock.schedule_interval(intro_update, 1/1000.0)
    pyglet.app.run()


def intro_update(dt):
    """
    Update method for both intro sequence.
    :param dt:
    """
    if emulator.cpu.opcode != 0x1210:
        emulator.cpu.cycle()
    else:
        sleep(5)
        # Start select game sequence
        # load selected game
        emulator.load_rom('chipy8/resources/games/Missile.ch8')
        pyglet.clock.schedule_interval(update, 1/1000.0)


def update(dt):
    """
    Update method for both debugger and the cpu.
    :param dt:
    """
    if not emulator.cpu.is_paused:
        emulator.cpu.cycle()
        # dbg.update_disassembly(emulator.cpu.previous_pc, emulator.cpu.opcode)

if __name__ == '__main__':
    emulator = chip8.Chip8(640, 320)
    intro_sequence()
    # dbg = debugger.Debugger(800, 600)
    # dbg.hook(emulator)