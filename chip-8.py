__author__ = 'Clayton Powell'
import pygame
import sys


fonts = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
         0x20, 0x60, 0x20, 0x20, 0x70,  # 1
         0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
         0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
         0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
         0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
         0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
         0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
         0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
         0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
         0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
         0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
         0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
         0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
         0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
         0xF0, 0x80, 0xF0, 0x80, 0x80]  # F


class CPU(object):
    def __init__(self):
        self.memory = [0] * 4096  # 4096 bits
        self.gpio = [0] * 16  # max 16
        self.console = [0] * 64 * 32  # Display console is 64 x 32 pixels
        self.stack = []
        self.key_inputs = [0] * 16  # 16 different key inputs available
        self.opcode = 0
        self.index = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.should_draw = False
        self.pc = 0x200

        for i in range(0, 80):
            self.memory[i] = fonts[i]

        self.op_map = {0x0000: self._0ZZZ,
                       0x00e0: self._0ZZ0,
                       0x00ee: self._0ZZE,
                       0x1000: self._1ZZZ,
                       0x2000: self._2ZZZ,
                       0x3000: self._3ZZZ,
                       0x4000: self._4ZZZ,
                       0x5000: self._5ZZZ,
                       0x6000: self._6ZZZ,
                       0x7000: self._7ZZZ,
                       0x8000: self._8ZZZ,
                       0x8FF0: self._8ZZ0,
                       0x8FF1: self._8ZZ1,
                       0x8FF2: self._8ZZ2,
                       0x8FF3: self._8ZZ3,
                       0x8FF4: self._8ZZ4,
                       0x8FF5: self._8ZZ5,
                       0x8FF6: self._8ZZ6,
                       0x8FF7: self._8ZZ7,
                       0x8FFE: self._8ZZE,
                       0x9000: self._9ZZZ,
                       0xA000: self._AZZZ,
                       0xB000: self._BZZZ,
                       0xC000: self._CZZZ,
                       0xD000: self._DZZZ,
                       0xE000: self._EZZZ,
                       0xE00E: self._EZZE,
                       0xE001: self._EZZ1,
                       0xF000: self._FZZZ,
                       0xF007: self._FZ07,
                       0xF00A: self._FZ0A,
                       0xF015: self._FZ15,
                       0xF018: self._FZ18,
                       0xF01E: self._FZ1E,
                       0xF029: self._FZ29,
                       0xF033: self._FZ33,
                       0xF055: self._FZ55,
                       0xF065: self._FZ65}

    def load_rom(self, rom_path):
        rom = open(rom_path, "rb").read()
        for index in range(0, len(rom)):
            self.memory[index + 0x200] = ord(rom[index])

    def cycle(self):
        self.opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2
        self.vx = (self.opcode & 0x0f00) >> 8
        self.vy = (self.opcode & 0x00f0) >> 4
        new_opcode = self.opcode & 0xf000
        try:
            self.op_map[new_opcode]()
        except:
            print "unknown instruction: %X" % self.opcode
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            if self.sound_timer == 0:
                # Play a sound!
                pass

    def _0ZZZ(self):
        new_op = self.opcode & 0xf0ff
        try:
            self.op_map[new_op]()
        except:
            print "Unknown instruction: %X" % self.opcode

    def _0ZZ0(self):
        """
        Clears the screen
        :return:
        """

    def _0ZZE(self):
        pass

    def _1ZZZ(self):
        pass

    def _2ZZZ(self):
        pass

    def _3ZZZ(self):
        pass

    def _4ZZZ(self):
        pass

    def _5ZZZ(self):
        pass

    def _6ZZZ(self):
        pass

    def _7ZZZ(self):
        pass

    def _8ZZZ(self):
        pass

    def _8ZZ0(self):
        pass

    def _8ZZ1(self):
        pass

    def _8ZZ2(self):
        pass

    def _8ZZ3(self):
        pass

    def _8ZZ4(self):
        pass

    def _8ZZ5(self):
        pass

    def _8ZZ6(self):
        pass

    def _8ZZ7(self):
        pass

    def _8ZZE(self):
        pass

    def _9ZZZ(self):
        pass

    def _AZZZ(self):
        pass

    def _BZZZ(self):
        pass

    def _CZZZ(self):
        pass

    def _DZZZ(self):
        pass

    def _EZZZ(self):
        pass

    def _EZZE(self):
        pass

    def _EZZ1(self):
        pass

    def _FZZZ(self):
        pass

    def _FZ07(self):
        pass

    def _FZ0A(self):
        pass

    def _FZ15(self):
        pass

    def _FZ18(self):
        pass

    def _FZ1E(self):
        pass

    def _FZ29(self):
        pass

    def _FZ33(self):
        pass

    def _FZ55(self):
        pass

    def _FZ65(self):
        pass


if __name__ == '__main__':
    pygame.init()
    console = pygame.display.set_mode((640, 320))
    pixel = pygame.image.load('pixel.png')
    pixel_rect = pixel.get_rect()
    emulator = CPU()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        console.fill((0, 0, 0))
        console.blit(pixel, pixel_rect)
        pygame.display.flip()