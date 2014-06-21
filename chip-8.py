__author__ = 'Clayton Powell'
import pygame
import sys
import random


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


# noinspection PyPep8Naming
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
        self.should_draw = True
        self.pc = 0x200
        self.vx = 0
        self.vy = 0

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

    def op_filter(self, opcode):
        try:
            # noinspection PyCallingNonCallable
            self.op_map[opcode]()
        except KeyError:
            print "Unknown instruction: %X" % self.opcode

    def cycle(self):
        self.opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2
        self.vx = (self.opcode & 0x0f00) >> 8
        self.vy = (self.opcode & 0x00f0) >> 4
        self.op_filter(self.opcode & 0xf000)
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            if self.sound_timer == 0:
                # Play a sound!
                pass

    def get_key(self):
        for index in range(16):
            if self.key_inputs[index] == 1:
                return index
        return -1

    def draw(self):
        if self.should_draw:
            #console.fill((0, 0, 0))
            #for index in range(2048):
             #   if self.console[index] == 1:
              #      console.blit(pixel, ((index % 64) * 10, 310 - ((index / 64) * 10)))
            pygame.display.update()
            self.should_draw = False

    def _0ZZZ(self):
        # passes off to other opcode calls
        self.op_filter(self.opcode & 0xf0ff)

    def _0ZZ0(self):
        # Clears the screen
        self.console = [0] * 64 * 32
        self.should_draw = True

    def _0ZZE(self):
        # Returns from subroutine
        self.pc = self.stack.pop()

    def _1ZZZ(self):
        # Jumps to address NNN
        self.pc = self.opcode & 0x0fff

    def _2ZZZ(self):
        # Calls subroutine at NNN
        self.stack.append(self.pc)
        self.pc = self.opcode & 0x0fff

    def _3ZZZ(self):
        # Skips the next instruction if VX equals NN
        if self.gpio[self.vx] == (self.opcode & 0x00ff):
            self.pc += 2

    def _4ZZZ(self):
        # Skips the next instruction if VX doesn't equal NN.
        if self.gpio[self.vx] != (self.opcode & 0x00ff):
            self.pc += 2

    def _5ZZZ(self):
        # Skips the next instruction if VX equals VY
        if self.gpio[self.vx] == self.gpio[self.vy]:
            self.pc += 2

    def _6ZZZ(self):
        # Sets VX to NN
        self.gpio[self.vx] = (self.opcode & 0x00ff)

    def _7ZZZ(self):
        # Adds NN to VX
        self.gpio[self.vx] += (self.opcode & 0x00ff)

    def _8ZZZ(self):
        # Sets VX to the value of VY
        extracted_op = self.opcode & 0xf00f
        extracted_op += 0xff0
        self.op_filter(extracted_op)

    def _8ZZ0(self):
        # Sets VX to the value of VY
        self.gpio[self.vx] = self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8ZZ1(self):
        # Sets VX to (VX or VY)
        self.gpio[self.vx] |= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8ZZ2(self):
        # Sets VX to (VX and VY)
        self.gpio[self.vx] &= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8ZZ3(self):
        # Sets VX to (VX xor VY)
        self.gpio[self.vx] ^= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8ZZ4(self):
        # Adds VY to VX. VF is set to 1 when there is a carry, and to 0 when there isn't.
        if self.gpio[self.vx] + self.gpio[self.vy] > 0xff:
            self.gpio[0xf] = 1
        else:
            self.gpio[0xf] = 0
        self.gpio[self.vx] += self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8ZZ5(self):
        # VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't
        if self.gpio[self.vy] > self.gpio[self.vx]:
            self.gpio[0xf] = 0
        else:
            self.gpio[0xf] = 1
        self.gpio[self.vx] -= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8ZZ6(self):
        # Shifts VX right by one. VF is set to the value of the least significant bit of VX before the shift.
        self.gpio[0xf] = self.gpio[self.vx] & 0x0001
        self.gpio[self.vx] >>= 1

    def _8ZZ7(self):
        # Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
        if self.gpio[self.vx] > self.gpio[self.vy]:
            self.gpio[0xf] = 0
        else:
            self.gpio[0xf] = 1
        self.gpio[self.vx] = self.gpio[self.vy] - self.gpio[self.vx]
        self.gpio[self.vx] &= 0xff

    def _8ZZE(self):
        # Shifts VX left by one. VF is set to the value of the most significant bit of VX before the shift.
        self.gpio[0xf] = (self.gpio[self.vx] & 0x00f0) >> 7
        self.gpio[self.vx] <<= 1
        self.gpio[self.vx] &= 0xff

    def _9ZZZ(self):
        # Skips the next instruction if VX doesn't equal VY
        if self.gpio[self.vx] != self.gpio[self.vy]:
            self.pc += 2

    def _AZZZ(self):
        # Sets I to the address NNN
        self.index = self.opcode & 0x0fff

    def _BZZZ(self):
        # Jumps to the address NNN plus V0
        self.pc = (self.opcode & 0x0fff) + self.gpio[0]

    def _CZZZ(self):
        # Sets VX to a random number and NN
        random_number = int(random.random())
        self.gpio[self.vx] = random_number & (self.opcode & 0x00ff)
        self.gpio[self.vx] &= 0xff

    def _DZZZ(self):
        # Draw a sprite
        self.gpio[0xf] = 0
        x = self.gpio[self.vx] & 0xff
        y = self.gpio[self.vy] & 0xff
        height = self.opcode & 0x000f
        row = 0
        console.fill(0, 0, 0)
        while row < height:
            current_row = self.memory[row + self.index]
            pixel_offset = 0
            while pixel_offset < 8:
                location = x + pixel_offset + ((y + row) * 64)
                pixel_offset += 1
                if (y + row) >= 32 or (x + pixel_offset - 1) >= 64:
                    continue
                mask = 1 << 8 - pixel_offset
                current_pixel = (current_row & mask) >> (8 - pixel_offset)
                self.console[location] ^= current_pixel
                if self.console[location] == 0:
                    self.gpio[0xf] = 1
                else:
                    self.gpio[0xf] = 0
            row += 1
        console.blit(pixel, (((x + y) % 64) * 10, 310 - (((x + y) / 64) * 10)))
        self.should_draw = True

    def _EZZZ(self):
        self.op_filter(self.opcode & 0xf00f)

    def _EZZE(self):
        # Skips the next instruction if the key stored in VX is pressed
        key = self.gpio[self.vx] & 0xf
        if self.key_inputs[key] == 1:
            self.pc += 2

    def _EZZ1(self):
        # Skips the next instruction if the key stored in VX isn't pressed
        key = self.gpio[self.vx] & 0xf
        if self.key_inputs[key] == 0:
            self.pc += 2

    def _FZZZ(self):
        self.op_filter(self.opcode & 0xf0ff)

    def _FZ07(self):
        # Sets VX to the value of the delay timer
        self.gpio[self.vx] = self.delay_timer

    def _FZ0A(self):
        # A key press is awaited, and then stored in VX
        ret = self.get_key()
        if ret >= 0:
            self.gpio[self.vx] = ret
        else:
            self.pc -= 2

    def _FZ15(self):
        # Sets the delay timer to VX
        self.delay_timer = self.gpio[self.vx]

    def _FZ18(self):
        # Sets the sound timer to VX
        self.sound_timer = self.gpio[self.vx]

    def _FZ1E(self):
        # Adds VX to I. If overflow, VF = 1
        self.index += self.gpio[self.vx]
        if self.index > 0xfff:
            self.gpio[0xf] = 1
            self.index &= 0xfff
        else:
            self.gpio[0xf] = 0

    def _FZ29(self):
        # Set index to point to a character
        self.index = (5 * (self.gpio[self.vx])) & 0xfff

    def _FZ33(self):
        # Store a number as BCD
        self.memory[self.index] = self.gpio[self.vx] / 100
        self.memory[self.index + 1] = (self.gpio[self.vx] % 100) / 10
        self.memory[self.index + 2] = self.gpio[self.vx] % 10

    def _FZ55(self):
        # Stores V0 to VX in memory starting at address I
        for index in range(0, self.vx):
            self.memory[self.index + index] = self.gpio[index]
        self.index += self.vx + 1

    def _FZ65(self):
        # Fills V0 to VX with values from memory starting at address I
        for index in range(0, self.vx):
            self.gpio[index] = self.memory[self.index + index]
        self.index += self.vx + 1


if __name__ == '__main__':
    pygame.init()
    console = pygame.display.set_mode((640, 320))
    pixel = pygame.image.load('pixel.png')
    pixel_rect = pixel.get_rect()
    emulator = CPU()
    emulator.load_rom('games/PONG')
    clock = pygame.time.Clock()
    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        emulator.cycle()
        emulator.draw()