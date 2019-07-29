# ~/managers/operatorsYield/recorderTest.py
import unittest

import os
import sys
# import modules from other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for

pwd = os.getcwd()
os.chdir("..") # this moves you up to ~/managers
os.chdir("..") # you are now in parent /cerebmodels
rootwd = os.getcwd()
from models.cells.modelDummyTest import DummyCell
os.chdir(pwd)

#from utilities import UsefulUtils as uu
from managers.simulation import SimulationManager as sm

from recorder import Recorder as rc

import numpy as np

class RecorderTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        os.chdir(pwd)
        #
        self.parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}

    #@unittest.skip("reason for skipping")
    def test_1_time_NEURON_without_engaging(self):
        #os.chdir("..") # this moves you up to ~/managers
        #os.chdir("..") # you are now in parent /cerebmodels
        os.chdir(rootwd)
        sm.prepare_model_NEURON(parameters=self.parameters, chosenmodel=self.chosenmodel)
        rec_t = rc.time_NEURON()
        # the length of the rec_time != 0:dt:tstop since recording was not done
        self.assertNotEqual( len( rec_t ),
                             len( range(0,
                                     int(self.parameters["tstop"]/self.parameters["dt"]) )
                              ) + 1 # for the additional dt  step
                        )
        os.chdir(pwd) # reset to the location of this recorderTest.py

    #@unittest.skip("reason for skipping")
    def test_2_time_NEURON(self):
        #os.chdir("..") # this moves you up to ~/managers
        #os.chdir("..") # you are now in parent /cerebmodels
        os.chdir(rootwd)
        sm.prepare_model_NEURON(parameters=self.parameters, chosenmodel=self.chosenmodel)
        rec_t = rc.time_NEURON()
        sm.engage_NEURON()
        # check the length of the recorded time = 0:dt:tstop
        self.assertEqual( len( rec_t ),
                          len( range(0,
                                     int(self.parameters["tstop"]/self.parameters["dt"]) )
                             ) + 1 # for the additional dt  step
                        )
        os.chdir(pwd) # reset to the location of this recorderTest.py

    #@unittest.skip("reason for skipping")
    def test_3_response_body_NEURON(self):
        #os.chdir("..") # this moves you up to ~/managers
        #os.chdir("..") # you are now in parent /cerebmodels
        os.chdir(rootwd)
        sm.prepare_model_NEURON(parameters=self.parameters, chosenmodel=self.chosenmodel)
        rec_v = rc.response_body_NEURON(self.chosenmodel.cell.soma,
                                        self.chosenmodel.regions["soma"][0]) # "v"
        sm.engage_NEURON()
        # check the length of the rec_v = 0:dt:tstop
        self.assertEqual( len( rec_v ),
                          len( range(0,
                                     int(self.parameters["tstop"]/self.parameters["dt"]) )
                             ) + 1 # for the additional dt  step
                        )
        os.chdir(pwd) # reset to the location of this recorderTest.py

    #@unittest.skip("reason for skipping")
    def test_4_response_body_NEURON_tworesponses(self):
        #os.chdir("..") # this moves you up to ~/managers
        #os.chdir("..") # you are now in parent /cerebmodels
        os.chdir(rootwd)
        sm.prepare_model_NEURON(parameters=self.parameters, chosenmodel=self.chosenmodel)
        rec_v = rc.response_body_NEURON(self.chosenmodel.cell.soma, "v")
        rec_i = rc.response_body_NEURON(self.chosenmodel.cell.soma, "i_cap")
        sm.engage_NEURON()
        # check the length of the rec_v = 0:dt:tstop
        a = all( boolean == True for boolean in np.array(rec_v) != np.array(rec_i) )
        self.assertEqual( a, True)
        os.chdir(pwd) # reset to the location of this recorderTest.py

    #@unittest.skip("reason for skipping")
    def test_5_response_channel_NEURON(self):
        #os.chdir("..") # this moves you up to ~/managers
        #os.chdir("..") # you are now in parent /cerebmodels
        os.chdir(rootwd)
        sm.prepare_model_NEURON(parameters=self.parameters, chosenmodel=self.chosenmodel)
        rec_i = rc.response_channel_NEURON( self.chosenmodel.cell.soma,
                      list( self.chosenmodel.regions["channels"]["soma"].keys() )[0], # "pas"
                      self.chosenmodel.regions["channels"]["soma"]["pas"][0] ) # "i"
        sm.engage_NEURON()
        # check the length of the rec_v = 0:dt:tstop
        self.assertEqual( len( rec_i ),
                          len( range(0,
                                     int(self.parameters["tstop"]/self.parameters["dt"]) )
                             ) + 1 # for the additional dt  step
                        )
        os.chdir(pwd) # reset to the location of this recorderTest.py

    @unittest.skip("reason for skipping")
    def test_4_stimulus_individual_currents_NEURON(self):
        #os.chdir("..") # this moves you up to ~/managers
        #os.chdir("..") # you are now in parent /cerebmodels
        os.chdir(rootwd)
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        currparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {'amp': 0.5, 'dur': 10.0, 'delay': 5.0},
                                        {'amp': 1.0, 'dur': 20.0, 'delay': 5.0+10.0} ],
                          "tstop": parameters["tstop"] }
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimuli_list = sm.stimulate_model_NEURON(stimparameters = currparameters,
                                               modelsite = self.chosenmodel.cell.soma)
        rec_i_indivs = rc.stimulus_individual_currents_NEURON(stimuli_list)
        sm.engage_NEURON()
        # check the length of the rec_v = 0:dt:tstop
        self.assertEqual( len( rec_i_indivs ), len( currparameters["stimlist"] ) )
        os.chdir(pwd) # reset to the location of this recorderTest.py

    @unittest.skip("reason for skipping")
    def test_5_stimulus_overall_currents_NEURON(self):
        #os.chdir("..") # this moves you up to ~/managers
        #os.chdir("..") # you are now in parent /cerebmodels
        os.chdir(rootwd)
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        currparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {'amp': 0.5, 'dur': 10.0, 'delay': 5.0},
                                        {'amp': 1.0, 'dur': 20.0, 'delay': 5.0+10.0} ],
                          "tstop": parameters["tstop"] }
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimuli_list = sm.stimulate_model_NEURON(stimparameters = currparameters,
                                                 modelsite = self.chosenmodel.cell.soma)
        rec_i_indivs = rc.stimulus_individual_currents_NEURON(stimuli_list)
        sm.engage_NEURON()
        rec_i = rc.stimulus_overall_current_NEURON(rec_i_indivs)
        # check the length of the rec_v = 0:dt:tstop
        self.assertEqual( len( rec_i ),
                          len( range(-1,
                                     int(parameters["tstop"]/parameters["dt"]) )
                             )
                        )
        os.chdir(pwd) # reset to the location of this recorderTest.py

    @unittest.skip("reason for skipping")
    def test_6_stimulus_overall_voltage_NEURON(self):
        #os.chdir("..") # this moves you up to ~/managers
        #os.chdir("..") # you are now in parent /cerebmodels
        os.chdir(rootwd)
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        voltparameters = {"type": ["voltage", "SEClamp"],
                          "stimlist": [ {'amp1': 0.0, 'dur1': 5.0},
                                        {'amp2': -70.0, 'dur2': 10.0} ],
                          "tstop": parameters["tstop"] }
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimuli = sm.stimulate_model_NEURON(stimparameters = voltparameters,
                                            modelsite = self.chosenmodel.cell.soma)
        sm.engage_NEURON()
        rec_v = rc.stimulus_overall_voltage_NEURON(stimuli)
        # check the length of the rec_v = 0:dt:tstop
        self.assertEqual( len( rec_v ),
                          len( range(-1,
                                     int(parameters["tstop"]/parameters["dt"]) )
                             )
                        )
        os.chdir(pwd) # reset to the location of this recorderTest.py

if __name__ == '__main__':
    unittest.main()
