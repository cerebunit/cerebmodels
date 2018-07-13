# ~/managers/operatorsSimaudit/assemblerTest.py
import unittest

from assembler import ModelAssembler

class ModelAssemblerTest(unittest.TestCase):

    def setUp(self):
        self.ma = ModelAssembler()

    def test_1_set_fixed_timesteps(self):
        self.assertFalse(not ModelAssembler.set_fixed_timesteps)

if __name__ == '__main__':
    unittest.main()
