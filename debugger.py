__author__ = 'cjpowell'
import pyglet
import disassembler


class Debugger(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Debugger, self).__init__(*args, **kwargs)
        self.labels = [pyglet.text.Label(font_name='Consolas', font_size=11, x=5, y=400 + i*10, anchor_x='left',
                                         anchor_y='top') for i in range(10)]
        self.dsm = disassembler.Disassembler()
        self.history = []

    def update_disassembly(self, pc, opcode):
        self.history.append(self.dsm.disassemble(pc, opcode))

    def on_draw(self):
        self.clear()
        for index in range(10):
            try:
                self.labels[index].text = self.history[-(index + 1)]
                self.labels[index].draw()
            except IndexError:
                continue
