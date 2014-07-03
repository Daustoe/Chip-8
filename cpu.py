"""
Chip 8 CPU module.

Notes:
Currently there is a problem with how Chip 8 programs expect the interpreter to draw sprites.
Because of this there is a blinking/flickering effect. The program clears a sprite, we draw, the program writes
a sprite, we draw.

It should be program clears a sprite, program writes a sprite, we Draw
"""
__author__ = 'Clayton Powell'
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


class CPU(object):
    """
    CPU class that emulates the Chip 8 cpu for the entire program.
    """
    def __init__(self):
        self.memory = [0] * 4096
        self.gpio = [0] * 16
        self.graphics = [0] * 64 * 32
        self.stack = []
        self.key_inputs = [0] * 16
        self.opcode = 0
        self.index = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.should_draw = True
        self.pc = 0x200
        self.vx = 0
        self.vy = 0
        self.is_paused = False
        self.previous_pc = None
        for i in range(0, 80):
            self.memory[i] = fonts[i]

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
                       0x8FF0: self._8xy0,
                       0x8FF1: self._8xy1,
                       0x8FF2: self._8xy2,
                       0x8FF3: self._8xy3,
                       0x8FF4: self._8xy4,
                       0x8FF5: self._8xy5,
                       0x8FF6: self._8xy6,
                       0x8FF7: self._8xy7,
                       0x8FFE: self._8xye,
                       0x9000: self._9xy0,
                       0xA000: self._annn,
                       0xB000: self._bnnn,
                       0xC000: self._cxnn,
                       0xD000: self._dxyn,
                       0xE000: self._ezzz,
                       0xE00E: self._ex9e,
                       0xE001: self._exa1,
                       0xF000: self._fzzz,
                       0xF007: self._fx07,
                       0xF00A: self._fx0a,
                       0xF015: self._fx15,
                       0xF018: self._fx18,
                       0xF01E: self._fx1e,
                       0xF029: self._fx29,
                       0xF033: self._fx33,
                       0xF055: self._fx55,
                       0xF065: self._fx65}

    def load_rom(self, rom_path):
        """
        Loads the rom at the given rom_path into local memory. Starts the loaded rom at offset 0x200. This is the
        standard for Chip 8 interpreters as anything before 0x200 was typically reserved.
        :param rom_path:
        """
        rom = open(rom_path, "rb").read()
        for index in range(0, len(rom)):
            self.memory[index + 0x200] = ord(rom[index])

    def _op_filter(self, opcode):
        try:
            function = self.op_map[opcode]
            function()
        except KeyError:
            print "Unknown instruction: %X" % self.opcode

    def cycle(self):
        """
        Performs one cpu cycle.
        """
        self.previous_pc = self.pc
        self.opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2
        self.vx = (self.opcode & 0x0f00) >> 8
        self.vy = (self.opcode & 0x00f0) >> 4
        self._op_filter(self.opcode & 0xf000)
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            if self.sound_timer == 0:
                # Play a sound!
                pass

    def _get_key(self):
        for index in range(16):
            if self.key_inputs[index] == 1:
                return index
        return -1

    def _0zzz(self):
        self._op_filter(self.opcode & 0xf0ff)

    def _00e0(self):
        # Clears the screen
        self.graphics = [0] * 64 * 32
        self.should_draw = True

    def _00ee(self):
        # Returns from a subroutine
        self.pc = self.stack.pop()

    def _1nnn(self):
        # Jumps to address NNN
        self.pc = self.opcode & 0x0fff

    def _2nnn(self):
        # Calls subroutine at NNN
        self.stack.append(self.pc)
        self.pc = self.opcode & 0x0fff

    def _3xnn(self):
        # Skips the next instruction if VX equals NN
        if self.gpio[self.vx] == (self.opcode & 0x00ff):
            self.pc += 2

    def _4xnn(self):
        # Skips the next instruction if VX doesn't equal NN.
        if self.gpio[self.vx] != (self.opcode & 0x00ff):
            self.pc += 2

    def _5xy0(self):
        # Skips the next instruction if VX equals VY
        if self.gpio[self.vx] == self.gpio[self.vy]:
            self.pc += 2

    def _6xnn(self):
        # Sets VX to NN
        self.gpio[self.vx] = (self.opcode & 0x00ff)

    def _7xnn(self):
        # Adds NN to VX
        self.gpio[self.vx] += (self.opcode & 0x00ff)

    def _8zzz(self):
        self._op_filter((self.opcode & 0xf00f) + 0xff0)

    def _8xy0(self):
        # Sets VX to the value of VY
        self.gpio[self.vx] = self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8xy1(self):
        # Sets VX to (VX | VY)
        self.gpio[self.vx] |= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8xy2(self):
        # Sets VX to (VX & VY)
        self.gpio[self.vx] &= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8xy3(self):
        # Sets VX to (VX ^ VY)
        self.gpio[self.vx] ^= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8xy4(self):
        # Adds VY to VX. VF is set to 1 when there is a carry, and to 0 when there isn't.
        if self.gpio[self.vx] + self.gpio[self.vy] > 0xff:
            self.gpio[0xf] = 1
        else:
            self.gpio[0xf] = 0
        self.gpio[self.vx] += self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8xy5(self):
        # VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't
        if self.gpio[self.vy] > self.gpio[self.vx]:
            self.gpio[0xf] = 0
        else:
            self.gpio[0xf] = 1
        self.gpio[self.vx] -= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8xy6(self):
        # Shifts VX right by one. VF is set to the value of the least significant bit of VX before the shift.
        self.gpio[0xf] = self.gpio[self.vx] & 0x0001
        self.gpio[self.vx] >>= 1

    def _8xy7(self):
        # Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
        if self.gpio[self.vx] > self.gpio[self.vy]:
            self.gpio[0xf] = 0
        else:
            self.gpio[0xf] = 1
        self.gpio[self.vx] = self.gpio[self.vy] - self.gpio[self.vx]
        self.gpio[self.vx] &= 0xff

    def _8xye(self):
        # Shifts VX left by one. VF is set to the value of the most significant bit of VX before the shift.
        self.gpio[0xf] = (self.gpio[self.vx] & 0x00f0) >> 7
        self.gpio[self.vx] <<= 1
        self.gpio[self.vx] &= 0xff

    def _9xy0(self):
        # Skips the next instruction if VX doesn't equal VY
        if self.gpio[self.vx] != self.gpio[self.vy]:
            self.pc += 2

    def _annn(self):
        # Sets I to the address NNN
        self.index = self.opcode & 0x0fff

    def _bnnn(self):
        # Jumps to the address NNN plus V0
        self.pc = (self.opcode & 0x0fff) + self.gpio[0]

    def _cxnn(self):
        # Sets VX to a random number and NN
        self.gpio[self.vx] = (random.randint(0, 0xff) & (self.opcode & 0x00ff)) & 0xff

    def _dxyn(self):
        # Sprites stored in memory at location in index register (I), maximum 8bits wide. Wraps around the screen.
        # If when drawn, clears a pixel, register VF is set to 1 otherwise it is zero. All drawing is XOR drawing
        # (e.g. it toggles the screen pixels)
        self.gpio[0xf] = 0
        x = self.gpio[self.vx] & 0xff
        y = self.gpio[self.vy] & 0xff
        height = self.opcode & 0x000f
        row = 0
        self.gpio[0xf] = 0
        while row < height:
            curr_row = self.memory[row + self.index]
            pixel_offset = 0
            while pixel_offset < 8:
                loc = x + pixel_offset + ((y + row) * 64)
                pixel_offset += 1
                if (y + row) >= 32 or (x + pixel_offset - 1) >= 64:
                    # ignore pixels outside the screen
                    continue
                mask = 1 << 8-pixel_offset
                curr_pixel = (curr_row & mask) >> (8-pixel_offset)
                if self.graphics[loc] == 1 and curr_pixel == 1:
                    self.gpio[0xf] = 1
                self.graphics[loc] ^= curr_pixel
            row += 1
        self.should_draw = True

    def _ezzz(self):
        self._op_filter(self.opcode & 0xf00f)

    def _ex9e(self):
        # Skips the next instruction if the key stored in VX is pressed
        key = self.gpio[self.vx] & 0xf
        print key
        if self.key_inputs[key] == 1:
            self.pc += 2

    def _exa1(self):
        # Skips the next instruction if the key stored in VX isn't pressed
        key = self.gpio[self.vx] & 0xf
        if self.key_inputs[key] == 0:
            self.pc += 2

    def _fzzz(self):
        self._op_filter(self.opcode & 0xf0ff)

    def _fx07(self):
        # Sets VX to the value of the delay timer
        self.gpio[self.vx] = self.delay_timer

    def _fx0a(self):
        # A key press is awaited, and then stored in VX
        ret = self._get_key()
        if ret >= 0:
            self.gpio[self.vx] = ret
        else:
            self.pc -= 2

    def _fx15(self):
        # Sets the delay timer to VX
        self.delay_timer = self.gpio[self.vx]

    def _fx18(self):
        # Sets the sound timer to VX
        self.sound_timer = self.gpio[self.vx]

    def _fx1e(self):
        # Adds VX to I. If overflow, VF = 1
        self.index += self.gpio[self.vx]
        if self.index > 0xfff:
            self.gpio[0xf] = 1
            self.index &= 0xfff
        else:
            self.gpio[0xf] = 0

    def _fx29(self):
        # Sets I to the location of the sprite for the character in VX. Characters 0-F (in hexadecimal) are represented
        # by a 4x5 font.
        self.index = (5 * (self.gpio[self.vx])) & 0xfff

    def _fx33(self):
        # Store a number as BCD
        self.memory[self.index] = self.gpio[self.vx] / 100
        self.memory[self.index + 1] = (self.gpio[self.vx] % 100) / 10
        self.memory[self.index + 2] = self.gpio[self.vx] % 10

    def _fx55(self):
        # Stores V0 to VX in memory starting at address I
        for index in range(0, self.vx):
            self.memory[self.index + index] = self.gpio[index]
        self.index += self.vx + 1

    def _fx65(self):
        # Fills V0 to VX with values from memory starting at address I
        for index in range(0, self.vx):
            self.gpio[index] = self.memory[self.index + index]
        self.index += self.vx + 1