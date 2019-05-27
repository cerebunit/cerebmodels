# ../managers/signalprocessingTest.py
import unittest
import os
import importlib

import sys
# import modules from other directories
# set to ~/cerebmodels
sys.path.append(os.path.dirname(os.getcwd()))
# this is required for

pwd = os.getcwd()
os.chdir("..") # this moves you up to ~/cerebmodels
rootwd = os.getcwd()
from models.cells.modelDummyTest import DummyCell
os.chdir(pwd)

from managers.simulation import SimulationManager as sm
from managers.record import RecordManager as rm
from managers.signalprocessing import SignalProcessingManager as sp


class SignalProcessingManagerTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell() #for alternative approach see managerSimulationTest.py
        os.chdir(pwd)
        self.rec = {"time": None, "response": None, "stimulus": None}
        self.regionslist_str = list(self.chosenmodel.regions.keys())

    #@unittest.skip("reason for skipping")
    def test_1_transform_signal_None(self):
        os.chdir("..") # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        rec_t, rec_v, x = rm.prepare_recording_NEURON(self.chosenmodel)
        sm.engage_NEURON()
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertRaises( ValueError, sp.transform_signal,
                           chosenmodel = self.chosenmodel,
                           recordings = rec_v[self.regionslist_str[0]] )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_2_transform_signal_to_spikes(self):
        os.chdir("..") # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        currparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {'amp': 0.5, 'dur': 10.0, 'delay': 5.0},
                                        {'amp': 1.0, 'dur': 20.0, 'delay': 5.0+10.0} ] }
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimuli_list = sm.stimulate_model_NEURON(stimparameters = currparameters,
                                               modelsite = self.chosenmodel.cell.soma)
        self.rec["time"], self.rec["response"], self.rec["stimulus"] = \
                 rm.prepare_recording_NEURON(self.chosenmodel)
        sm.engage_NEURON()
        spikes = sp.transform_signal( chosenmodel = self.chosenmodel,
                                      recordings = self.rec,
                                      tosignal = 'spikes')
        ans = \
          len( range(
               int(spikes[self.regionslist_str[0]].t_start.magnitude),
               int(spikes[self.regionslist_str[0]].t_stop.magnitude/parameters["dt"])
              ) ) + 1 # for the additional dt step
        self.assertEqual( ans, len(self.rec["time"]) )
        os.chdir(pwd) # reset to the location of this managerSignalProcessingTest.py

if __name__ == '__main__':
    unittest.main()
