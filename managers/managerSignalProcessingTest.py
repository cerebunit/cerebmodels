# ../managers/managerSignalProcessingTest.py
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
from managerSignalProcessing import SignalProcessingManager

class SignalProcessingManagerTest(unittest.TestCase):

    def setUp(self):
        self.sp = SignalProcessingManager() #instance for non: static & class methods.
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell() #for alternative approach see managerSimulationTest.py
        self.rec = {"time": None, "response": None, "stimulus": None}
        self.regionslist_str = list(self.chosenmodel.regions.keys())
        self.sm = SimulationManager()
        self.rm = RecordManager()

    #@unittest.skip("reason for skipping")
    def test_1_transform_signal_None(self):
        os.chdir("..") # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        rec_t, rec_v, x = self.rm.prepare_recording_NEURON(self.chosenmodel)
        self.sm.engage_NEURON()
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertRaises( ValueError, self.sp.transform_signal,
                           chosenmodel = self.chosenmodel,
                           recordings = rec_v[self.regionslist_str[0]] )
        os.chdir(self.pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_2_transform_signal_to_spikes(self):
        os.chdir("..") # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        currparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {'amp': 0.5, 'dur': 10.0, 'delay': 5.0},
                                        {'amp': 1.0, 'dur': 20.0, 'delay': 5.0+10.0} ] }
        self.sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimuli_list = self.sm.stimulate_model_NEURON(stimparameters = currparameters,
                                               modelsite = self.chosenmodel.cell.soma)
        self.rec["time"], self.rec["response"], self.rec["stimulus"] = \
                 self.rm.prepare_recording_NEURON(self.chosenmodel)
        self.sm.engage_NEURON()
        spikes = self.sp.transform_signal( chosenmodel = self.chosenmodel,
                                           recordings = self.rec,
                                           tosignal = 'spikes')
        ans = \
        len( range(
             int(spikes[self.regionslist_str[0]].t_start.magnitude),
             int(spikes[self.regionslist_str[0]].t_stop.magnitude/parameters["dt"])
              ) ) + 1 # for the additional dt step
        self.assertEqual( ans, len(self.rec["time"]) )
        os.chdir(self.pwd) # reset to the location of this managerSignalProcessingTest.py

if __name__ == '__main__':
    unittest.main()
