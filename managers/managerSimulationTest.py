# ../managers/managerSimulationTest.py
import unittest
import os
import importlib

import sys
# import modules from other directories
# set to ~/cerebmodels
sys.path.append(os.path.dirname(os.getcwd()))
# this is required for
# from managers.operatorsSimaudit.inspector import SimInspector
# from managers.operatorsSimaudit.hardware import HardwareConfigurator
# from managers.operatorsSimaudit.assembler import SimAssembler
# called in managerSimulation.py
# and also for the utilities
from utilities import UsefulUtils

from managerSimulation import SimulationManager


class SimulationManagerTest(unittest.TestCase):

    def setUp(self):
        self.sm = SimulationManager() #instance for non: static & class methods.
        self.uu = UsefulUtils()
        self.pwd = os.getcwd()

    def test_1_prepare_model_NEURON(self):
        os.chdir("..") # move up to load the model
        #from utilities import UsefulUtils as uu
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelPC2015Masoli")
        pickedmodel = getattr(modelmodule,
                              self.uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        self.assertEqual(self.sm.prepare_model_NEURON(parameters, chosenmodel),
                         "NEURON model is ready")
        os.chdir(self.pwd) # return to the location of this test file

if __name__ == '__main__':
    unittest.main()
