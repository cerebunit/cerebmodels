# ~/managers/operatorsYield/recorderTest.py
import unittest

import os
import sys
# import modules from other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
#from utilities import UsefulUtils as uu
from models.cells.modelDummyTest import DummyCell
from managers.managerSimulation import SimulationManager

from recorder import Recorder

class RecorderTest(unittest.TestCase):

    def setUp(self):
        self.rc = Recorder()
        #self.uu = UsefulUtils()
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell()
        self.sm = SimulationManager()

    #@unittest.skip("reason for skipping")
    def test_1_time_NEURON_without_engaging(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in parent /cerebmodels
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        rec_t = self.rc.time_NEURON()
        # the length of the rec_time != 0:dt:tstop since recording was not done
        self.assertNotEqual( len( rec_t ),
                             len( range(0,
                                     int(parameters["tstop"]/parameters["dt"]) )
                              ) + 1 # for the additional dt  step
                        )
        os.chdir(self.pwd) # reset to the location of this recorderTest.py

    #@unittest.skip("reason for skipping")
    def test_2_time_NEURON(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in parent /cerebmodels
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        rec_t = self.rc.time_NEURON()
        self.sm.engage_NEURON()
        # check the length of the recorded time = 0:dt:tstop
        self.assertEqual( len( rec_t ),
                          len( range(0,
                                     int(parameters["tstop"]/parameters["dt"]) )
                             ) + 1 # for the additional dt  step
                        )
        os.chdir(self.pwd) # reset to the location of this recorderTest.py

    #@unittest.skip("reason for skipping")
    def test_3_response_voltage_NEURON(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in parent /cerebmodels
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        rec_v = self.rc.response_voltage_NEURON(self.chosenmodel.cell.soma)
        self.sm.engage_NEURON()
        # check the length of the rec_v = 0:dt:tstop
        self.assertEqual( len( rec_v ),
                          len( range(0,
                                     int(parameters["tstop"]/parameters["dt"]) )
                             ) + 1 # for the additional dt  step
                        )
        os.chdir(self.pwd) # reset to the location of this recorderTest.py

    #@unittest.skip("reason for skipping")
    def test_4_stimulus_individual_currents_NEURON(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in parent /cerebmodels
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        currparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {'amp': 0.5, 'dur': 10.0, 'delay': 5.0},
                                        {'amp': 1.0, 'dur': 20.0, 'delay': 5.0+10.0} ] }
        self.sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimuli_list = self.sm.stimulate_model_NEURON(stimparameters = currparameters,
                                               modelsite = self.chosenmodel.cell.soma)
        rec_i_indivs = self.rc.stimulus_individual_currents_NEURON(stimuli_list)
        self.sm.engage_NEURON()
        # check the length of the rec_v = 0:dt:tstop
        self.assertEqual( len( rec_i_indivs ), len( currparameters["stimlist"] ) )
        os.chdir(self.pwd) # reset to the location of this recorderTest.py

    #@unittest.skip("reason for skipping")
    def test_5_stimulus_overall_currents_NEURON(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in parent /cerebmodels
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        currparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {'amp': 0.5, 'dur': 10.0, 'delay': 5.0},
                                        {'amp': 1.0, 'dur': 20.0, 'delay': 5.0+10.0} ] }
        self.sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimuli_list = self.sm.stimulate_model_NEURON(stimparameters = currparameters,
                                               modelsite = self.chosenmodel.cell.soma)
        rec_i_indivs = self.rc.stimulus_individual_currents_NEURON(stimuli_list)
        self.sm.engage_NEURON()
        rec_i = self.rc.stimulus_overall_current_NEURON(rec_i_indivs)
        # check the length of the rec_v = 0:dt:tstop
        self.assertEqual( len( rec_i ),
                          len( range(-1,
                                     int(parameters["tstop"]/parameters["dt"]) )
                             )
                        )
        os.chdir(self.pwd) # reset to the location of this recorderTest.py

if __name__ == '__main__':
    unittest.main()
