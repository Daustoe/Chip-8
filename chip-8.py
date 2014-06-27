__author__ = 'Clayton Powell'
import pygame
import sys
import pyglet
import cpu

"""
Notes:

Want to move to pyglet instead of pygame for the flexibility that it provides.
Want to create an entire debugger for the Chip-8 emulator. This will be nice to have
when we move to upgrading to Super Chip-8.

This includes a view of the registers, a disassembler of the opcodes run, emulation flow
control, and a view of the memory.


"""


class Chip8(object):
    def __init__(self):
        self.key_map = {pygame.K_1: 0x1,
                        pygame.K_2: 0x2,
                        pygame.K_3: 0x3,
                        pygame.K_4: 0xc,
                        pygame.K_q: 0x4,
                        pygame.K_w: 0x5,
                        pygame.K_e: 0x6,
                        pygame.K_r: 0xd,
                        pygame.K_a: 0x7,
                        pygame.K_s: 0x8,
                        pygame.K_d: 0x9,
                        pygame.K_f: 0xe,
                        pygame.K_z: 0xa,
                        pygame.K_x: 0,
                        pygame.K_c: 0xb,
                        pygame.K_v: 0xf}
        self.console = pygame.display.set_mode((640, 320))
        self.debug_window = pyglet.window.Window(800, 600)
        self.clock = pygame.time.Clock()
        self.white_pixel = pygame.Surface((10, 10))
        self.white_pixel.fill((255, 255, 255))
        self.black_pixel = pygame.Surface((10, 10))
        self.black_pixel.fill((0, 0, 0))
        self.cpu = cpu.CPU()
        self.cpu.load_rom('utils/games/Tron.ch8')

    def emulator_loop(self):
        while True:
            self.clock.tick(1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.key_map:
                        self.cpu.key_inputs[self.key_map[event.key]] = 1
                elif event.type == pygame.KEYUP:
                    if event.key in self.key_map:
                        self.cpu.key_inputs[self.key_map[event.key]] = 0
            self.cpu.cycle()
            self.draw()

    def draw(self):
        if self.cpu.should_draw:
            self.console.fill((0, 0, 0))
            for index in range(2048):
                if self.cpu.graphics[index] == 1:
                    self.console.blit(self.white_pixel, ((index % 64) * 10, ((index / 64) * 10)))
            pygame.display.update()
            self.cpu.should_draw = False

if __name__ == '__main__':
    pygame.init()
    emulator = Chip8()
    emulator.emulator_loop()

