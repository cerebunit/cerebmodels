# ~/managers/operatorsSimaudit/assemblerTest.py
import unittest

from assembler import SimAssembler

class SimAssemblerTest(unittest.TestCase):

    def setUp(self):
        self.sa = SimAssembler()

    def test_1_set_fixed_timesteps(self):
        self.assertFalse(not SimAssembler.set_fixed_timesteps)

if __name__ == '__main__':
    unittest.main()
