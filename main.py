"""
Notes going forward.

Ignoring the flickering, it seems that is how the original Chip8 interpreter functioned.

Current program is using some function of ours that is not working correctly, things I suspect:
on a return from subroutine, we are hoping to next opcode, we may be skipping some stuff.

To check this we need to disassemble the rom itself so we can follow along with each cycle and double
check that everything is working as it should.
"""
__author__ = 'Clayton Powell'
import chip8
import pyglet
import debugger


def update(dt):
    """
    Update method for both debugger and the cpu.
    :param dt:
    """
    if not emulator.cpu.is_paused:
        emulator.cpu.cycle()
        dbg.update_disassembly(emulator.cpu.previous_pc, emulator.cpu.opcode)

if __name__ == '__main__':
    emulator = chip8.Chip8(640, 320)
    dbg = debugger.Debugger(800, 600)
    dbg.hook(emulator)
    pyglet.clock.schedule_interval(update, 1/600.0)
    pyglet.app.run()