# ~/managers/operatorsSimaudit/assemblerTest.py
import unittest

from assembler import SimAssembler

class SimAssemblerTest(unittest.TestCase):

    def setUp(self):
        self.sa = SimAssembler()

    def test_1_set_fixed_timesteps(self):
        self.assertEqual(SimAssembler.set_fixed_timesteps(),
                         "timestep is fixed")

    def test_2_set_runtime_NEURON_noparams(self):
        self.assertRaises(ValueError, self.sa.set_runtime_NEURON)

    def test_3_set_runtime_NEURON(self):
        param = {"dt": 1, "celsius": 2}
        self.assertEqual(self.sa.set_runtime_NEURON(parameters=param),
                         "parameters are set")

    def test_4_set_runtime_NEURON_parameterkey_not_in_h(self):
        param = {"dt": 1, "celsisus": 2, "tstop": 3}
        self.assertRaises(AttributeError, self.sa.set_runtime_NEURON,
                          parameters = param)

if __name__ == '__main__':
    unittest.main()
