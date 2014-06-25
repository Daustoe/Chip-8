__author__ = 'Claymore'


class Disassembler(object):
    def __init__(self, rom_path):
        self.memory = [0] * 4096
        self.load_rom(rom_path)
        self.opcode = 0x0
        self.op_map = {0x1000: self._1NNN,
                       0x2000: self._2NNN,
                       0x3000: self._3XNN,
                       0x4000: self._4XNN,
                       0x5000: self._5XY0,
                       0x6000: self._6XNN,
                       0x7000: self._7XNN,
                       0x8000: self._8000,
                       0x9000: self._9XY0,
                       0xa000: self._ANNN,
                       0xb000: self._BNNN,
                       0xc000: self._CXNN,
                       0xd000: self._DNNN
                       }

    def load_rom(self, rom_path):
        rom = open(rom_path, "rb").read()
        for index in range(0, len(rom)):
            self.memory[index + 0x200] = ord(rom[index])

    def disassemble(self):
        for index in range(0x200, len(self.memory), 2):
            self.opcode = (self.memory[index] << 8) | self.memory[index+1]
            try:
                print '%s %s\t%s' % (hex(index), hex(self.opcode), self.op_map[self.opcode & 0xf000]())
            except:
                print '%s %s\t%s' % (hex(index), hex(self.opcode), 'n/a')

    def _1NNN(self):
        return 'JUMP\t$%s' % (str(hex(self.opcode & 0x0fff))[2:])

    def _2NNN(self):
        return 'CALL\t$%s' % (str(hex(self.opcode & 0x0fff))[2:])

    def _3XNN(self):
        vx = str(hex(self.opcode & 0xf00))[2]
        nn = str(hex(self.opcode & 0xff))[2:]
        return 'SKIP.EQ\tV%s, $%s' % (vx, nn)

    def _4XNN(self):
        vx = str(hex(self.opcode & 0xf00))[2]
        nn = str(hex(self.opcode & 0xff))[2:]
        return 'SKIP.NE\tV%s, $%s' % (vx, nn)

    def _5XY0(self):
        vx = str(hex(self.opcode & 0xf00))[2]
        vy = str(hex(self.opcode & 0xf0))[2]
        return 'SKIP.EQ\tV%s, V%s' % (vx, vy)

    def _6XNN(self):
        return 'MVI \tV%s, $%s' % (str(hex(self.opcode & 0xf00))[2], str(hex(self.opcode & 0x00ff))[2:])

    def _7XNN(self):
        return 'ADI \tV%s, $%s' % (str(hex(self.opcode & 0xf00))[2], str(hex(self.opcode & 0x00ff))[2:])

    def _8000(self):
        return 'just another 0x8 command...'

    def _9XY0(self):
        vx = str(hex(self.opcode & 0xf00))[2]
        vy = str(hex(self.opcode & 0xf0))[2]
        return 'SKIP.NE\tV%s, V%s' % (vx, vy)

    def _ANNN(self):
        return 'MVI \tI,  $%s' % (str(hex(self.opcode & 0x0fff))[2:])

    def _BNNN(self):
        return 'JUMP\t$%s(V0)' % str(hex(self.opcode & 0x0fff))[2:]

    def _CXNN(self):
        return 

    def _DNNN(self):
        vx = str(hex(self.opcode & 0xf00))[2]
        vy = str(hex(self.opcode & 0xf0))[2]
        height = str(hex(self.opcode & 0xf))[2]
        return 'DRAW\tVX:%s VY:%s H:%s' % (vx, vy, height)

if __name__ == '__main__':
    dsm = Disassembler('games/PONG')
    dsm.disassemble()
