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
        self.dasm_labels = [pyglet.text.Label(font_size=10, x=5, y=40 + i * 12) for i in range(60)]
        self.dasm = disassembler.Disassembler()
        self.gpio_labels = [pyglet.text.Label(font_size=10, x=300, y=400 + i * 12) for i in range(0x10)]
        self.index_label = pyglet.text.Label(font_size=10, x=300, y=150)
        self.history = []
        self.set_vsync(False)
        self.emulator = None

    def update_disassembly(self, pc, opcode):
        """
        Adds latest opcode disassembly to history of disassembly output.
        :param pc:
        :param opcode:
        """
        self.history.append(self.dasm.disassemble(pc, opcode))

    def hook(self, emulator):
        """
        Attaches the given emulator to this debugger.
        :param emulator:
        """
        self.emulator = emulator

    def on_key_press(self, symbol, modifiers):
        """
        Key press event for the dbg. Here we enable cpu control, stop, one cycle, and such.
        :param symbol:
        :param modifiers:
        """
        if symbol == pyglet.window.key.P:
            self.emulator.cpu.is_paused = True
        elif symbol == pyglet.window.key.G:
            self.emulator.cpu.is_paused = False
        elif symbol == pyglet.window.key.T and self.emulator.cpu.is_paused:
            self.emulator.cpu.cycle()
            self.update_disassembly(self.emulator.cpu.pc, self.emulator.cpu.opcode)

    def on_draw(self):
        """
        Draw method for the debugger window.
        """
        self.clear()
        self.index_label.text = 'I: ' + hex(self.emulator.cpu.index)[2:]
        self.index_label.draw()
        for index in range(60):
            try:
                self.dasm_labels[index].text = self.history[-(index + 1)]
                self.dasm_labels[index].draw()
            except IndexError:
                continue
        for label in range(0x10):
            self.gpio_labels[label].text = hex(label) + ' ' + hex(self.emulator.cpu.gpio[label])[2:]
            self.gpio_labels[label].draw()
        self.flip()
