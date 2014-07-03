"""
This module contains the Disassembler class for the Chip-8 interpreter.
"""
__author__ = 'Clayton Powell'


class Disassembler(object):
    """
    Chip8 opcode disassembler.
    """

    def __init__(self):
        self.opcode = 0x0
        self.recursion_count = 0
        self.op_map = {0x0000: self._0zzz,
                       0x00e0: self._00e0,
                       0x00ee: self._00ee,
                       0x1000: self._1nnn,
                       0x2000: self._2nnn,
                       0x3000: self._3xnn,
                       0x4000: self._4xnn,
                       0x5000: self._5xy0,
                       0x6000: self._6xnn,
                       0x7000: self._7xnn,
                       0x8000: self._8zzz,
                       0x8ff0: self._8xy0,
                       0x8ff1: self._8xy1,
                       0x8ff2: self._8xy2,
                       0x8ff3: self._8xy3,
                       0x8ff4: self._8xy4,
                       0x8ff5: self._8xy5,
                       0x8ff6: self._8xy6,
                       0x8ff7: self._8xy7,
                       0x8ffe: self._8xye,
                       0x9000: self._9xy0,
                       0xa000: self._annn,
                       0xb000: self._bnnn,
                       0xc000: self._cxnn,
                       0xd000: self._dnnn,
                       0xe000: self._ezzz,
                       0xe09e: self._ex9e,
                       0xe0a1: self._exa1,
                       0xf000: self._fzzz,
                       0xf007: self._fx07,
                       0xf00a: self._fx0a,
                       0xf015: self._fx15,
                       0xf018: self._fx18,
                       0xf01e: self._fx1e,
                       0xf029: self._fx29,
                       0xf033: self._fx33,
                       0xf055: self._fx55,
                       0xf065: self._fx65
                       }

    def disassemble(self, pc, opcode):
        """
        Disassembles a single opcode, requires program counter for printing reference.
        :param pc:
        :param opcode:
        :return:
            Returns string with details about that particular opcode
        """
        self.opcode = opcode
        self.recursion_count = 0
        if opcode == 0:
            return '%s %s\t\tNOP' % (hex(pc), str(hex(opcode))[2:])
        else:
            try:
                function = self.op_map[opcode & 0xf000]
                return '%s %s\t%s' % (hex(pc), str(hex(opcode))[2:], function())
            except KeyError:
                return '%s %s\t%s' % (hex(pc), str(hex(opcode))[2:], '\tNot Handled')

    def _extract(self, mask):
        return str(hex(self.opcode & mask))

    def _extract_vx_vy(self):
        return self._extract(0xf00)[2], self._extract(0xf0)[2]

    def _extract_vx_nn(self):
        return self._extract(0xf00)[2], self._extract(0xff)[2:]

    def _0zzz(self):
        self.recursion_count += 1
        if self.recursion_count <= 1:
            function = self.op_map[self.opcode & 0xfff]
            return function()
        else:
            return 0

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

    def _6xnn(self):
        return 'MVI \t\tV%s, \t$%s' % self._extract_vx_nn()

    def _7xnn(self):
        return 'ADI \t\tV%s, \t$%s' % self._extract_vx_nn()

    def _8zzz(self):
        self.recursion_count += 1
        if self.recursion_count <= 1:
            function = self.op_map[(self.opcode & 0xf00f) + 0xff0]
            return function()
        else:
            return 0

    def _8xy0(self):
        return 'MOV \t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8xy1(self):
        return 'OR  \t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8xy2(self):
        return 'AND \t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8xy3(self):
        return 'XOR \t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8xy4(self):
        return 'ADD.\t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8xy5(self):
        return 'SUB.\t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8xy6(self):
        return 'SHR.\t\tV%s' % self._extract(0xf00)[2]

    def _8xy7(self):
        return 'SBB.\t\tV%s, \tV%s' % self._extract_vx_vy()

    def _8xye(self):
        return 'SHL.\t\tV%s' % self._extract(0xf00)[2]

    def _9xy0(self):
        return 'SKIP.NE\t\tV%s, \tV%s' % self._extract_vx_vy()

    def _annn(self):
        return 'MVI \t\tI,\t\t$%s' % self._extract(0xfff)[2:]

    def _bnnn(self):
        return 'JUMP\t\t$%s(V0)' % self._extract(0xfff)[2:]

    def _cxnn(self):
        return 'RAND\t\tV%s, \t$%s' % self._extract_vx_nn()

    def _dnnn(self):
        vx, vy = self._extract_vx_vy()
        height = self._extract(0xf)[2]
        return 'DRAW\t\tVX:%s\tVY:%s\tH:%s' % (vx, vy, height)

    def _ezzz(self):
        self.recursion_count += 1
        if self.recursion_count <= 1:
            function = self.op_map[self.opcode & 0xf0ff]
            return function()
        else:
            return 0

    def _ex9e(self):
        return 'SKIP.KEY\tV%s' % self._extract(0xf00)[2]

    def _exa1(self):
        return 'SKIP.NOKEY\tV%s' % self._extract(0xf00)[2]

    def _fzzz(self):
        self.recursion_count += 1
        if self.recursion_count <= 1:
            function = self.op_map[self.opcode & 0xf0ff]
            return function()
        else:
            return 0

    def _fx07(self):
        return 'MOV \t\tV%s, \tDELAY' % self._extract(0xf00)[2]

    def _fx0a(self):
        return 'WAITKEY\t\tV%s' % self._extract(0xf00)[2]

    def _fx15(self):
        return 'MOV \t\tDELAY, \tV%s' % self._extract(0xf00)[2]

    def _fx18(self):
        return 'MOV \t\tSOUND, \tV%s' % self._extract(0xf00)[2]

    def _fx1e(self):
        return 'ADD \t\tI,\t\tV%s' % self._extract(0xf00)[2]

    def _fx29(self):
        return 'SPRITE\t\tV%s' % self._extract(0xf00)[2]

    def _fx33(self):
        return 'MOVBCD\t\tV%s' % self._extract(0xf00)[2]

    def _fx55(self):
        return 'MOVM\t\t(I), \tV0-V%s' % self._extract(0xf00)[2]

    def _fx65(self):
        return 'MOVM\t\tV0-V%s,\t(I)' % self._extract(0xf00)[2]