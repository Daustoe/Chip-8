"""
Note: We have commented out the flip() method in the pyglet default event loop.
until we figure out how to create a custom event loop, we have done this temporary
workaround. Because of this we need to call self.flip() in our on_draw method for each
Window that we are trying to display and update.
"""
__author__ = 'cjpowell'
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
    pyglet.clock.schedule_interval(update, 1/50.0)
    pyglet.app.run()