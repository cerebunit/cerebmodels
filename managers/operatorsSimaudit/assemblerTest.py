# ~/managers/operatorsSimaudit/assemblerTest.py
import unittest

import os
import sys
# import modules from other directories
# set to ~/cerebmodels
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
# from utilities import UsefulUtils as uu
# called in assembler.py 

from assembler import SimAssembler

from neuron import h
h.load_file("stdrun.hoc")

class SimAssemblerTest(unittest.TestCase):

    def setUp(self):
        self.sa = SimAssembler()

    #@unittest.skip("reason for skipping")
    def test_1_set_fixed_timesteps(self):
        self.assertEqual(SimAssembler.set_fixed_timesteps(),
                         "timestep is fixed")

    #@unittest.skip("reason for skipping")
    def test_2_set_runtime_NEURON_noparams(self):
        self.assertRaises(ValueError, self.sa.set_runtime_NEURON)

    #@unittest.skip("reason for skipping")
    def test_3_set_runtime_NEURON(self):
        param = {"dt": 1, "celsius": 2}
        self.assertEqual(self.sa.set_runtime_NEURON(parameters=param),
                         "parameters are set")

    #@unittest.skip("reason for skipping")
    def test_4_set_runtime_NEURON_parameterkey_not_in_h(self):
        param = {"dt": 1, "c": 2, "does_not_exist": 3}
        self.assertRaises(AttributeError, self.sa.set_runtime_NEURON,
                          parameters = param)

if __name__ == '__main__':
    unittest.main()
