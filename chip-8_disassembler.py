__author__ = 'Claymore'


class Disassembler(object):
    def __init__(self, rom_path):
        self.memory = [0] * 4096
        self.load_rom(rom_path)
        self.op_map = {0x0000: 'not handled',
                       0x1000: 'JUMP',
                       0x2000: 'CALL',
                       0x3000: 'SKIP.EQ',
                       0x4000: 'SKIP.NE',
                       0x5000: 'SKIP.EQ',
                       0x6000: 'MVI',
                       0x7000: 'ADI',
                       0x8000: 'not handled',
                       0x9000: 'SKIP.NE',
                       0xA000: 'MVI',
                       0xB000: 'JUMP',
                       0xC000: 'RNDMASK',
                       0xD000: 'DRAW',
                       0xE000: 'SKIP.KEY',
                       0xF000: 'not handled',
                       }

    def load_rom(self, rom_path):
        rom = open(rom_path, "rb").read()
        for index in range(0, len(rom)):
            self.memory[index + 0x200] = ord(rom[index])

    def disassemble(self):
        for index in range(0x200, len(self.memory), 2):
            opcode = (self.memory[index] << 8) | self.memory[index+1]
            print '{} {} {}'.format(hex(index), hex(opcode), self.disect_op(opcode))

    def disect_op(self, opcode):
        return self.op_map[opcode & 0xf000]

if __name__ == '__main__':
    dsm = Disassembler('games/PONG')
    dsm.disassemble()
