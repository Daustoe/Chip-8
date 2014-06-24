__author__ = 'Claymore'


class Disassembler(object):
    def __init__(self, rom_path):
        self.memory = [0] * 4096
        self.load_rom(rom_path)
        self.disassemble()

    def load_rom(self, rom_path):
        rom = open(rom_path, "rb").read()
        for index in range(0, len(rom)):
            self.memory[index] = ord(rom[index])

    def disassemble(self):
        for index in range(0, len(self.memory), 2):
            opcode = (self.memory[index] << 8) | self.memory[index+1]
            print hex(opcode)
            print hex(opcode & 0xf000)

if __name__ == '__main__':
    dsm = Disassembler('games/INVADERS')
