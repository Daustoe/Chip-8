"""
Notes:

We have a working disassembly output
Now we want to start to include cpu control buttons, memory viewer
"""
__author__ = 'cjpowell'
import pyglet
import disassembler


class Debugger(pyglet.window.Window):
    """
    Debugger Window class. Holds onto an instance of a Chip-8 disassembler for disassembly window.
    :param args:
    :param kwargs:
    """

    def __init__(self, *args, **kwargs):
        super(Debugger, self).__init__(*args, **kwargs)
        self.labels = [pyglet.text.Label(font_name='Consolas', font_size=11, x=5, y=400 + i*10, anchor_x='left',
                                         anchor_y='top') for i in range(20)]
        self.dasm = disassembler.Disassembler()
        self.history = []
        self.set_vsync(False)

    def update_disassembly(self, pc, opcode):
        """
        Adds latest opcode disassembly to history of disassembly output.
        :param pc:
        :param opcode:
        """
        self.history.append(self.dasm.disassemble(pc, opcode))

    def on_key_press(self, symbol, modifiers):
        """
        Key press event for the dbg. Here we enable cpu control, stop, one cycle, and such.
        :param symbol:
        :param modifiers:
        """
        if symbol == pyglet.window.key.S:
            print 'should stop!'

    def on_draw(self):
        """
        Draw method for the debugger window.
        """
        self.clear()
        for index in range(20):
            try:
                self.labels[index].text = self.history[-(index + 1)]
                self.labels[index].draw()
            except IndexError:
                continue
        self.flip()
