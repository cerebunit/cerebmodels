# ../managers/managerRecordTest.py
import unittest
import os
import importlib

import sys
# import modules from other directories
# set to ~/cerebmodels
sys.path.append(os.path.dirname(os.getcwd()))
# this is required for
from models.cells.modelDummyTest import DummyCell

from managerSimulation import SimulationManager
from managerRecord import RecordManager

class RecordManagerTest(unittest.TestCase):

    def setUp(self):
        self.rm = RecordManager() #instance for non: static & class methods.
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell() #for alternative approach see managerSimulationTest.py
        self.regionslist_str = list(self.chosenmodel.regions.keys())
        self.sm = SimulationManager()

    #@unittest.skip("reason for skipping")
    def test_1_prepare_recording_NEURON_without_stimulating(self):
        os.chdir("..") # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters, self.chosenmodel)
        rec_t, rec_v, x = self.rm.prepare_recording_NEURON(self.chosenmodel)
        self.sm.engage_NEURON()
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(rec_v[self.regionslist_str[0]]),
                          2*total_iterations )
        os.chdir(self.pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_2_prepare_recording_NEURON_without_stimulating_multiple_sections(self):
        os.chdir("..") # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters, self.chosenmodel)
        rec_t, rec_v, x = self.rm.prepare_recording_NEURON(self.chosenmodel)
        self.sm.engage_NEURON()
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(rec_v[self.regionslist_str[0]])
                                     + len(rec_v[self.regionslist_str[1]]),
                          3*total_iterations )
        os.chdir(self.pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_3_prepare_recording_NEURON_without_stimulating_but_evoke_stimulate_model(self):
        os.chdir("..") # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters, self.chosenmodel)
        stimulate_not = self.sm.stimulate_model_NEURON()
        rec_t, rec_v, x = self.rm.prepare_recording_NEURON(self.chosenmodel,
                                                           stimuli = stimulate_not)
        self.sm.engage_NEURON()
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(rec_v[self.regionslist_str[0]]),
                          2*total_iterations )
        os.chdir(self.pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_4_prepare_recording_NEURON_stimulate(self):
        os.chdir("..") # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        currparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {'amp': 0.5, 'dur': 10.0, 'delay': 5.0},
                                        {'amp': 1.0, 'dur': 20.0, 'delay': 5.0+10.0} ] }
        self.sm.prepare_model_NEURON(parameters, self.chosenmodel)
        stimuli_list = self.sm.stimulate_model_NEURON(stimparameters = currparameters,
                                               modelsite = self.chosenmodel.cell.soma)
        rec_t, rec_v, rec_i_indivs = self.rm.prepare_recording_NEURON(
                                                         self.chosenmodel,
                                                         stimuli = stimuli_list )
        self.sm.engage_NEURON()
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(rec_v[self.regionslist_str[0]])
                                     + len(rec_i_indivs),
                          2*total_iterations + len( currparameters["stimlist"] ) )
        os.chdir(self.pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_5_postrun_recording_NEURON_stimulate(self):
        os.chdir("..") # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        currparameters = {"type": ["current", "IRamp"],
           "stimlist": [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                         {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                         {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                         {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ] }
        self.sm.prepare_model_NEURON(parameters, self.chosenmodel)
        stimuli_list = self.sm.stimulate_model_NEURON(stimparameters = currparameters,
                                               modelsite = self.chosenmodel.cell.soma)
        rec_t, rec_v, rec_i_indivs = self.rm.prepare_recording_NEURON(
                                                         self.chosenmodel,
                                                         stimuli = stimuli_list )
        self.sm.engage_NEURON()
        rec_i = self.rm.postrun_record_NEURON( injectedcurrents = rec_i_indivs )
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(rec_v[self.regionslist_str[0]]) + len(rec_i),
                          3*total_iterations )
        os.chdir(self.pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_6_postrun_recording_NEURON_without_stimulating(self):
        os.chdir("..") # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters, self.chosenmodel)
        stimuli_list = self.sm.stimulate_model_NEURON()
        rec_t, rec_v, rec_i_indivs = self.rm.prepare_recording_NEURON(
                                                         self.chosenmodel,
                                                         stimuli = stimuli_list )
        self.sm.engage_NEURON()
        rec_i = self.rm.postrun_record_NEURON( injectedcurrents =  rec_i_indivs)
        self.assertEqual( self.rm.postrun_record_NEURON(),
                          "Model is not stimulated" )
        os.chdir(self.pwd) # reset to the location of this managerRecordTest.py

if __name__ == '__main__':
    unittest.main()
