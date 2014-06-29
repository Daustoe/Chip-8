"""
Chip 8 CPU module.
"""
__author__ = 'Clayton Powell'
import disassembler
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
        self.memory = [0] * 4096  # 4096 bits
        self.gpio = [0] * 16  # max 16
        self.graphics = [0] * 64 * 32  # Display console is 64 x 32 pixels
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
        self.disassembler = disassembler.Disassembler()

        for i in range(0, 80):
            self.memory[i] = fonts[i]

        self.op_map = {0x0000: self._0ZZZ,
                       0x00e0: self._00E0,
                       0x00ee: self._00EE,
                       0x1000: self._1NNN,
                       0x2000: self._2NNN,
                       0x3000: self._3XNN,
                       0x4000: self._4XNN,
                       0x5000: self._5XY0,
                       0x6000: self._6XNN,
                       0x7000: self._7XNN,
                       0x8000: self._8ZZZ,
                       0x8FF0: self._8XY0,
                       0x8FF1: self._8XY1,
                       0x8FF2: self._8XY2,
                       0x8FF3: self._8XY3,
                       0x8FF4: self._8XY4,
                       0x8FF5: self._8XY5,
                       0x8FF6: self._8XY6,
                       0x8FF7: self._8XY7,
                       0x8FFE: self._8XYE,
                       0x9000: self._9XY0,
                       0xA000: self._ANNN,
                       0xB000: self._BNNN,
                       0xC000: self._CXNN,
                       0xD000: self._DXYN,
                       0xE000: self._EZZZ,
                       0xE00E: self._EX9E,
                       0xE001: self._EXA1,
                       0xF000: self._FZZZ,
                       0xF007: self._FX07,
                       0xF00A: self._FX0A,
                       0xF015: self._FX15,
                       0xF018: self._FX18,
                       0xF01E: self._FX1E,
                       0xF029: self._FX29,
                       0xF033: self._FX33,
                       0xF055: self._FX55,
                       0xF065: self._FX65}

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

    def cycle(self, dt):
        """
        Performs one cpu cycle. 
        :param dt:
        """
        self.opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        print self.disassembler.disassemble(self.pc, self.opcode)
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

    def get_key(self):
        for index in range(16):
            if self.key_inputs[index] == 1:
                return index
        return -1

    def _0ZZZ(self):
        # passes off to other opcode calls
        self._op_filter(self.opcode & 0xf0ff)

    def _00E0(self):
        # Clears the screen
        self.graphics = [0] * 64 * 32
        self.should_draw = True

    def _00EE(self):
        # Returns from a subroutine
        self.pc = self.stack.pop()

    def _1NNN(self):
        # Jumps to address NNN
        self.pc = self.opcode & 0x0fff

    def _2NNN(self):
        # Calls subroutine at NNN
        self.stack.append(self.pc)
        self.pc = self.opcode & 0x0fff

    def _3XNN(self):
        # Skips the next instruction if VX equals NN
        if self.gpio[self.vx] == (self.opcode & 0x00ff):
            self.pc += 2

    def _4XNN(self):
        # Skips the next instruction if VX doesn't equal NN.
        if self.gpio[self.vx] != (self.opcode & 0x00ff):
            self.pc += 2

    def _5XY0(self):
        # Skips the next instruction if VX equals VY
        if self.gpio[self.vx] == self.gpio[self.vy]:
            self.pc += 2

    def _6XNN(self):
        # Sets VX to NN
        self.gpio[self.vx] = (self.opcode & 0x00ff)

    def _7XNN(self):
        # Adds NN to VX
        self.gpio[self.vx] += (self.opcode & 0x00ff)

    def _8ZZZ(self):
        # Sets VX to the value of VY
        self._op_filter((self.opcode & 0xf00f) + 0xff0)

    def _8XY0(self):
        # Sets VX to the value of VY
        self.gpio[self.vx] = self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8XY1(self):
        # Sets VX to (VX | VY)
        self.gpio[self.vx] |= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8XY2(self):
        # Sets VX to (VX & VY)
        self.gpio[self.vx] &= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8XY3(self):
        # Sets VX to (VX ^ VY)
        self.gpio[self.vx] ^= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8XY4(self):
        # Adds VY to VX. VF is set to 1 when there is a carry, and to 0 when there isn't.
        if self.gpio[self.vx] + self.gpio[self.vy] > 0xff:
            self.gpio[0xf] = 1
        else:
            self.gpio[0xf] = 0
        self.gpio[self.vx] += self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8XY5(self):
        # VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't
        if self.gpio[self.vy] > self.gpio[self.vx]:
            self.gpio[0xf] = 0
        else:
            self.gpio[0xf] = 1
        self.gpio[self.vx] -= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff

    def _8XY6(self):
        # Shifts VX right by one. VF is set to the value of the least significant bit of VX before the shift.
        self.gpio[0xf] = self.gpio[self.vx] & 0x0001
        self.gpio[self.vx] >>= 1

    def _8XY7(self):
        # Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
        if self.gpio[self.vx] > self.gpio[self.vy]:
            self.gpio[0xf] = 0
        else:
            self.gpio[0xf] = 1
        self.gpio[self.vx] = self.gpio[self.vy] - self.gpio[self.vx]
        self.gpio[self.vx] &= 0xff

    def _8XYE(self):
        # Shifts VX left by one. VF is set to the value of the most significant bit of VX before the shift.
        self.gpio[0xf] = (self.gpio[self.vx] & 0x00f0) >> 7
        self.gpio[self.vx] <<= 1
        self.gpio[self.vx] &= 0xff

    def _9XY0(self):
        # Skips the next instruction if VX doesn't equal VY
        if self.gpio[self.vx] != self.gpio[self.vy]:
            self.pc += 2

    def _ANNN(self):
        # Sets I to the address NNN
        self.index = self.opcode & 0x0fff

    def _BNNN(self):
        # Jumps to the address NNN plus V0
        self.pc = (self.opcode & 0x0fff) + self.gpio[0]

    def _CXNN(self):
        # Sets VX to a random number and NN
        random_number = int(random.random())
        self.gpio[self.vx] = random_number & (self.opcode & 0x00ff)
        self.gpio[self.vx] &= 0xff

    def _DXYN(self):
        # Sprites stored in memory at location in index register (I), maximum 8bits wide. Wraps around the screen.
        # If when drawn, clears a pixel, register VF is set to 1 otherwise it is zero. All drawing is XOR drawing
        # (e.g. it toggles the screen pixels)
        '''self.gpio[0xf] = 0
        x = self.gpio[self.vx] & 0xff
        y = self.gpio[self.vy] & 0xff
        height = self.opcode & 0x000f
        row = 0
        while row < height:
            current_row = self.memory[row + self.index]
            pixel_offset = 0
            self.gpio[0xf] = 0
            while pixel_offset < 8:
                location = x + pixel_offset + ((y + row) * 64)
                pixel_offset += 1
                if (y + row) >= 32 or (x + pixel_offset - 1) >= 64:
                    continue
                mask = 1 << 8 - pixel_offset
                current_pixel = (current_row & mask) >> (8 - pixel_offset)
                if self.graphics[location == 1 and current_pixel == 1]:
                    self.gpio[0xf] = 1
                self.graphics[location] ^= current_pixel
            row += 1
        self.should_draw = True'''
        self.gpio[0xf] = 0
        x = self.gpio[self.vx] & 0xff
        y = self.gpio[self.vy] & 0xff
        height = self.opcode & 0x000f
        row = 0
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
                self.graphics[loc] ^= curr_pixel
                if self.graphics[loc] == 0:
                    self.gpio[0xf] = 1
                else:
                    self.gpio[0xf] = 0
            row += 1
        self.should_draw = True

    def _EZZZ(self):
        self._op_filter(self.opcode & 0xf00f)

    def _EX9E(self):
        # Skips the next instruction if the key stored in VX is pressed
        key = self.gpio[self.vx] & 0xf
        if self.key_inputs[key] == 1:
            self.pc += 2

    def _EXA1(self):
        # Skips the next instruction if the key stored in VX isn't pressed
        key = self.gpio[self.vx] & 0xf
        if self.key_inputs[key] == 0:
            self.pc += 2

    def _FZZZ(self):
        self._op_filter(self.opcode & 0xf0ff)

    def _FX07(self):
        # Sets VX to the value of the delay timer
        self.gpio[self.vx] = self.delay_timer

    def _FX0A(self):
        # A key press is awaited, and then stored in VX
        ret = self.get_key()
        if ret >= 0:
            self.gpio[self.vx] = ret
        else:
            self.pc -= 2

    def _FX15(self):
        # Sets the delay timer to VX
        self.delay_timer = self.gpio[self.vx]

    def _FX18(self):
        # Sets the sound timer to VX
        self.sound_timer = self.gpio[self.vx]

    def _FX1E(self):
        # Adds VX to I. If overflow, VF = 1
        self.index += self.gpio[self.vx]
        if self.index > 0xfff:
            self.gpio[0xf] = 1
            self.index &= 0xfff
        else:
            self.gpio[0xf] = 0

    def _FX29(self):
        # Sets I to the location of the sprite for the character in VX. Characters 0-F (in hexadecimal) are represented
        # by a 4x5 font.
        self.index = (5 * (self.gpio[self.vx])) & 0xfff

    def _FX33(self):
        # Store a number as BCD
        self.memory[self.index] = self.gpio[self.vx] / 100
        self.memory[self.index + 1] = (self.gpio[self.vx] % 100) / 10
        self.memory[self.index + 2] = self.gpio[self.vx] % 10

    def _FX55(self):
        # Stores V0 to VX in memory starting at address I
        for index in range(0, self.vx):
            self.memory[self.index + index] = self.gpio[index]
        self.index += self.vx + 1

    def _FX65(self):
        # Fills V0 to VX with values from memory starting at address I
        for index in range(0, self.vx):
            self.gpio[index] = self.memory[self.index + index]
        self.index += self.vx + 1