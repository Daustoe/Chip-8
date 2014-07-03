"""
Unitests for the Chip8 cpu.
"""
__author__ = 'cjpowell'
import unittest
import cpu


class OpcodeTests(unittest.TestCase):
    def setUp(self):
        self.cpu = cpu.CPU()

    def test_00e0(self):
        self.cpu.memory[0x200] = 0
        self.cpu.memory[0x201] = 0xe0
        self.cpu.graphics[0] = 1
        self.cpu.cycle()
        self.assertEqual(self.cpu.graphics[0], 0)
        self.assertEqual(self.cpu.pc, 0x202)
        self.cpu.pc = 0x200
        self.cpu.graphics = [1] * 64 * 32
        self.cpu.cycle()
        self.assertListEqual(self.cpu.graphics, [0] * 64 * 32)

    def test_00ee(self):
        self.cpu.stack = [0x22e]
        self.cpu.memory[0x200] = 0
        self.cpu.memory[0x201] = 0xee
        self.cpu.cycle()
        self.assertEqual(self.cpu.pc, 0x22e)

    def test_1nnn(self):
        self.cpu.memory[0x200] = 0x12
        self.cpu.memory[0x201] = 0x3e
        self.assertEqual(self.cpu.pc, 0x200)
        self.cpu.cycle()
        self.assertEqual(self.cpu.pc, 0x23e)

    def test_2nnn(self):
        self.cpu.memory[0x200] = 0x22
        self.cpu.memory[0x201] = 0x3e
        self.cpu.cycle()
        self.assertListEqual(self.cpu.stack, [0x202])
        self.assertEqual(self.cpu.pc, 0x23e)

    def test_3xnn(self):
        self.cpu.memory[0x200] = 0x30
        self.cpu.memory[0x201] = 0xff
        self.cpu.gpio[0] = 0xff
        self.cpu.cycle()
        self.assertEqual(self.cpu.pc, 0x204)
        self.cpu.pc = 0x200
        self.cpu.gpio[0] = 0
        self.cpu.cycle()
        self.assertEqual(self.cpu.pc, 0x202)

    def test_4xnn(self):
        self.cpu.memory[0x200] = 0x40
        self.cpu.memory[0x201] = 0xff
        self.cpu.gpio[0] = 0xff
        self.cpu.cycle()
        self.assertEqual(self.cpu.pc, 0x202)
        self.cpu.pc = 0x200
        self.cpu.gpio[0] = 0
        self.cpu.cycle()
        self.assertEqual(self.cpu.pc, 0x204)

    def test_5xy0(self):
        self.cpu.memory[0x200] = 0x50
        self.cpu.memory[0x201] = 0x10
        self.cpu.gpio[0] = 0xff
        self.cpu.gpio[1] = 0xff
        self.cpu.cycle()
        self.assertEqual(self.cpu.pc, 0x204)
        self.cpu.pc = 0x200
        self.cpu.gpio[1] = 0
        self.cpu.cycle()
        self.assertEqual(self.cpu.pc, 0x202)

    def test_6xnn(self):
        self.cpu.memory[0x200] = 0x60
        self.cpu.memory[0x201] = 0xff
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0xff)

    def test_7xnn(self):
        self.cpu.memory[0x200] = 0x70
        self.cpu.memory[0x201] = 0x10
        self.cpu.gpio[0] = 0x1
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0x11)

    def test_8xy0(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x10
        self.cpu.gpio[1] = 0x1
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], self.cpu.gpio[1])

    def test_8xy1(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x11
        self.cpu.gpio[1] = 0xff
        self.cpu.gpio[0] = 0xf0
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0xff)

    def test_8xy2(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x12
        self.cpu.gpio[1] = 0xff
        self.cpu.gpio[0] = 0xf0
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0xf0)

    def test_8xy3(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x13
        self.cpu.gpio[1] = 0xff
        self.cpu.gpio[0] = 0xf0
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0xf)

    def test_8xy4(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x14
        self.cpu.gpio[1] = 0xff
        self.cpu.gpio[0] = 0xf0
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0xef)
        self.assertEqual(self.cpu.gpio[0xf], 1)
        self.cpu.gpio[1] = 1
        self.cpu.pc = 0x200
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0xf0)
        self.assertEqual(self.cpu.gpio[0xf], 0)

    def test_8xy5(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x15
        self.cpu.gpio[1] = 0xff
        self.cpu.gpio[0] = 0xf0
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0xf1)
        self.assertEqual(self.cpu.gpio[0xf], 0)
        self.cpu.gpio[1] = 1
        self.cpu.pc = 0x200
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0xf0)
        self.assertEqual(self.cpu.gpio[0xf], 1)

    def test_8xy6(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x16
        self.cpu.gpio[0] = 0xff
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0x7f)
        self.assertEqual(self.cpu.gpio[0xf], 1)
        self.cpu.pc = 0x200
        self.cpu.gpio[0] = 0xf0
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0x78)
        self.assertEqual(self.cpu.gpio[0xf], 0)

    def test_8xy7(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x17
        self.cpu.gpio[1] = 0xff
        self.cpu.gpio[0] = 0xf0
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0xf)
        self.assertEqual(self.cpu.gpio[0xf], 1)
        self.cpu.gpio[1] = 1
        self.cpu.pc = 0x200
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0xf2)
        self.assertEqual(self.cpu.gpio[0xf], 0)

    def test_8xye(self):
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x1e
        self.cpu.gpio[0] = 0xff
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0xfe)
        self.assertEqual(self.cpu.gpio[0xf], 1)
        self.cpu.pc = 0x200
        self.cpu.gpio[0] = 0x0f
        self.cpu.cycle()
        self.assertEqual(self.cpu.gpio[0], 0x1e)
        self.assertEqual(self.cpu.gpio[0xf], 0)

    def test_9xy0(self):
        self.cpu.memory[0x200] = 0x90
        self.cpu.memory[0x201] = 0x10
        self.cpu.gpio[0] = 1
        self.cpu.cycle()
        self.assertEqual(self.cpu.pc, 0x204)
        self.cpu.pc = 0x200
        self.cpu.gpio[0] = 0
        self.cpu.cycle()
        self.assertEqual(self.cpu.pc, 0x202)

    def test_annn(self):
        self.cpu.memory[0x200] = 0xa2
        self.cpu.memory[0x201] = 0x3e
        self.cpu.cycle()
        self.assertEqual(self.cpu.index, 0x23e)

    def test_bnnn(self):
        self.cpu.memory[0x200] = 0xb2
        self.cpu.memory[0x201] = 0x3e
        self.cpu.gpio[0] = 1
        self.cpu.cycle()
        self.assertEqual(self.cpu.pc, 0x23f)

    def test_cxnn(self):
        self.cpu.memory[0x200] = 0xc0
        self.cpu.memory[0x201] = 0x17
        self.cpu.cycle()
        test1 = self.cpu.gpio[0]
        self.cpu.pc = 0x200
        self.cpu.cycle()
        test2 = self.cpu.gpio[0]
        self.assertNotEqual(test1, test2)

    def test_dxyn(self):
        self.cpu.memory[0x200] = 0xd0
        self.cpu.memory[0x201] = 0x01
        self.cpu.memory[0] = 0x80
        self.cpu.cycle()
        self.assertEqual(self.cpu.graphics[0], 1)
        self.assertListEqual(self.cpu.graphics[1:], [0] * 2047)

    def test_ex9e(self):
        self.assertTrue(False)

    def test_exa1(self):
        self.assertTrue(False)

    def test_fx07(self):
        self.cpu.memory[0x200] = 0xf0
        self.cpu.memory[0x201] = 0x07
        self.cpu.delay_timer = 0x12
        self.cpu.cycle()

    def test_fx0a(self):
        self.assertTrue(False)

    def test_fx15(self):
        self.assertTrue(False)

    def test_fx18(self):
        self.assertTrue(False)

    def test_fx1e(self):
        self.assertTrue(False)

    def test_fx29(self):
        self.assertTrue(False)

    def test_fx33(self):
        self.assertTrue(False)

    def test_fx55(self):
        self.assertTrue(False)

    def test_fx65(self):
        self.assertTrue(False)