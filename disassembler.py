__author__ = 'Claymore'


class Disassembler(object):
    """
    Chip8 opcode disassembler.
    """

    def __init__(self):
        self.memory = [0] * 4096
        self.opcode = 0x0
        self.op_map = {0x0000: self._0zzz,
                       0x00e0: self._00e0,
                       0x00ee: self._00ee,
                       0x1000: self._1nnn,
                       0x2000: self._2nnn,
                       0x3000: self._3xnn,
                       0x4000: self._4xnn,
                       0x5000: self._5xy0,
                       0x6000: self._6XNN,
                       0x7000: self._7XNN,
                       0x8000: self._8ZZZ,
                       0x8ff0: self._8XY0,
                       0x8ff1: self._8XY1,
                       0x8ff2: self._8XY2,
                       0x8ff3: self._8XY3,
                       0x8ff4: self._8XY4,
                       0x8ff5: self._8XY5,
                       0x8ff6: self._8XY6,
                       0x8ff7: self._8XY7,
                       0x8ffe: self._8XYE,
                       0x9000: self._9XY0,
                       0xa000: self._ANNN,
                       0xb000: self._BNNN,
                       0xc000: self._CXNN,
                       0xd000: self._DNNN,
                       0xe000: self._EZZZ,
                       0xe00e: self._EX9E,
                       0xe001: self._EXA1,
                       0xf000: self._FZZZ,
                       0xf007: self._FX07,
                       0xf00a: self._FX0A,
                       0xf015: self._FX15,
                       0xf018: self._FX18,
                       0xf01e: self._FX1E,
                       0xf029: self._FX29,
                       0xf033: self._FX33,
                       0xf055: self._FX55,
                       0xf065: self._FX65
                       }

    def load_rom(self, rom_path):
        """
        Loads Chip8 rom from given path into local memory.
        :param rom_path:
        """
        rom = open(rom_path, "rb").read()
        for index in range(0, len(rom)):
            self.memory[index + 0x200] = ord(rom[index])

    def disassemble(self, pc, opcode):
        """
        Disassembles a single opcode, requires program counter for printing reference.
        :param pc:
        :param opcode:
        :return:
            Returns string with details about that particular opcode
        """
        self.opcode = opcode
        if opcode == 0:
            return '%s %s\t\tNOP' % (hex(pc), str(hex(opcode))[2:])
        else:
            try:
                function = self.op_map[opcode & 0xf000]
                return '%s %s\t%s' % (hex(pc), str(hex(opcode))[2:], function())
            except KeyError:
                return '%s %s\t%s' % (hex(pc), str(hex(opcode))[2:], '\tNot Handled')

    def disassemble_all(self):
        """
        Disassembles the entire rom of a given Chip8 rom.
        """
        for index in range(0x200, len(self.memory), 2):
            self.opcode = (self.memory[index] << 8) | self.memory[index+1]
            print self.disassemble(index, self.opcode)

    def _extract(self, mask):
        return str(hex(self.opcode & mask))

    def _extract_vx_vy(self):
        return self._extract(0xf00)[2], self._extract(0xf0)[2]

    def _extract_vx_nn(self):
        return self._extract(0xf00)[2], self._extract(0xff)[2:]

    def _0zzz(self):
        function = self.op_map[self.opcode & 0xf0ff]
        return function()

    @staticmethod
    def _00e0():
        return 'CLS'

    @staticmethod
    def _00ee():
        return 'RTS'

    def _1nnn(self):
        return 'JUMP\t\t$%s' % self._extract(0xfff)[2:]

    def _2nnn(self):
        return 'CALL\t\t$%s' % self._extract(0x0fff)[2:]

    def _3xnn(self):
        return 'SKIP.EQ\t\tV%s, \t$%s' % self._extract_vx_nn()

    def _4xnn(self):
        return 'SKIP.NE\t\tV%s, \t$%s' % self._extract_vx_nn()

    def _5xy0(self):
        return 'SKIP.EQ\t\tV%s, \tV%s' % self._extract_vx_vy()

    def _6XNN(self):
        return 'MVI \t\tV%s, \t$%s' % self._extract_vx_nn()

    def _7XNN(self):
        return 'ADI \t\tV%s, \t$%s' % self._extract_vx_nn()

    def _8ZZZ(self):
        function = self.op_map[(self.opcode & 0xf00f) + 0xff0]
        return function()

    def _8XY0(self):
        return 'MOV \t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8XY1(self):
        return 'OR  \t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8XY2(self):
        return 'AND \t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8XY3(self):
        return 'XOR \t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8XY4(self):
        return 'ADD.\t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8XY5(self):
        return 'SUB.\t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8XY6(self):
        return 'SHR.\t\tV%s' % self._extract(0xf00)[2]

    def _8XY7(self):
        return 'SBB.\t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8XYE(self):
        return 'SHL.\t\tV%s' % self._extract(0xf00)[2]

    def _9XY0(self):
        return 'SKIP.NE\t\tV%s, \tV%s' % self._extract_vx_vy()

    def _ANNN(self):
        return 'MVI \t\tI,\t\t$%s' % self._extract(0xfff)[2:]

    def _BNNN(self):
        return 'JUMP\t\t$%s(V0)' % self._extract(0xfff)[2:]

    def _CXNN(self):
        return 'RAND\t\tV%s, \t$%s' % self._extract_vx_nn()

    def _DNNN(self):
        vx, vy = self._extract_vx_vy()
        height = self._extract(0xf)[2]
        return 'DRAW\t\tVX:%s\tVY:%s\tH:%s' % (vx, vy, height)

    def _EZZZ(self):
        function = self.op_map[self.opcode & 0xf00f]
        return function()

    def _EX9E(self):
        return 'SKIP.KEY\tV%s' % self._extract(0xf00)[2]

    def _EXA1(self):
        return 'SKIP.NOKEY\tV%s' % self._extract(0xf00)[2]

    def _FZZZ(self):
        function = self.op_map[self.opcode & 0xf0ff]
        return function()

    def _FX07(self):
        return 'MOV \t\tV%s, \tDELAY' % self._extract(0xf00)[2]

    def _FX0A(self):
        return 'WAITKEY\t\tV%s' % self._extract(0xf00)[2]

    def _FX15(self):
        return 'MOV \t\tDELAY, \tV%s' % self._extract(0xf00)[2]

    def _FX18(self):
        return 'MOV \t\tSOUND, \tV%s' % self._extract(0xf00)[2]

    def _FX1E(self):
        return 'ADD \t\tI,\t\tV%s' % self._extract(0xf00)[2]

    def _FX29(self):
        return 'SPRITE\t\tV%s' % self._extract(0xf00)[2]

    def _FX33(self):
        return 'MOVBCD\t\tV%s' % self._extract(0xf00)[2]

    def _FX55(self):
        return 'MOVM\t\t(I), \tV0-V%s' % self._extract(0xf00)[2]

    def _FX65(self):
        return 'MOVM\t\tV0-V%s,\t(I)' % self._extract(0xf00)[2]