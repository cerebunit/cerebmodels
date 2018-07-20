# ~/managers/operatorsYield/recorderTest.py
import unittest

import os
import sys
# import modules from other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
#from utilities import UsefulUtils as uu
from models.cells.modelDummyTest import DummyTest
from managers.managerSimulation import SimulationManager

from recorder import Recorder

class RecorderTest(unittest.TestCase):

    def setUp(self):
        self.rc = Recorder()
        #self.uu = UsefulUtils()
        self.pwd = os.getcwd()
        self.chosenmodel = DummyTest()
        self.sm = SimulationManager()

    def test_1_time_NEURON_without_engaging(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters, self.chosenmodel)
        rec_t = self.rc.time_NEURON()
        # the length of the rec_time != 0:dt:tstop since recording was not done
        self.assertNotEqual( len( rec_t ),
                             len( range(0,
                                     int(parameters["tstop"]/parameters["dt"]) )
                              ) + 1 # for the additional dt  step
                        )
        os.chdir(self.pwd) # reset to the location of this recorderTest.py

    def test_2_time_NEURON(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters, self.chosenmodel)
        rec_t = self.rc.time_NEURON()
        self.sm.engage_NEURON()
        # check the length of the recorded time = 0:dt:tstop
        self.assertEqual( len( rec_t ),
                          len( range(0,
                                     int(parameters["tstop"]/parameters["dt"]) )
                             ) + 1 # for the additional dt  step
                        )
        os.chdir(self.pwd) # reset to the location of this recorderTest.py

    def test_3_response_voltage_NEURON(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters, self.chosenmodel)
        rec_v = self.rc.response_voltage_NEURON(self.chosenmodel.cell.soma)
        self.sm.engage_NEURON()
        # check the length of the rec_v = 0:dt:tstop
        self.assertEqual( len( rec_v ),
                          len( range(0,
                                     int(parameters["tstop"]/parameters["dt"]) )
                             ) + 1 # for the additional dt  step
                        )
        os.chdir(self.pwd) # reset to the location of this recorderTest.py

if __name__ == '__main__':
    unittest.main()
