# ../managers/operatorsSignaling/converterTest.py
import unittest
import os
import shutil

import sys
# import modules from other directories
# set to ~/cerebmodels
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from models.cells.modelDummyTest import DummyCell

from managers.managerSimulation import SimulationManager
from managers.managerRecord import RecordManager
from converter import Converter

class ConverterTest(unittest.TestCase):

    def setUp(self):
        self.co = Converter()
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell()
        self.rec = {"time": None, "response": None, "stimulus": None}
        self.regionslist_str = list(self.chosenmodel.regions.keys())
        self.sm = SimulationManager()
        self.rm = RecordManager()

    #@unittest.skip("reason for skipping")
    def test_1_determine_signalsign_from_threshold_above(self):
        thresh = +0.0 # 10
        self.assertEqual( self.co.determine_signalsign_from_threshold(thresh),
                          'above' )

    #@unittest.skip("reason for skipping")
    def test_2_determine_signalsign_from_threshold_below(self):
        thresh = -30.0
        self.assertEqual( self.co.determine_signalsign_from_threshold(thresh),
                          'below' )

    #@unittest.skip("reason for skipping")
    def test_3_voltage_to_spiketrain_without_stimulation(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in parent /cerebmodels
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        self.rec["time"], self.rec["response"], self.rec["stimulus"] = \
                 self.rm.prepare_recording_NEURON(self.chosenmodel)
        self.sm.engage_NEURON()
        spikes = self.co.voltage_to_spiketrain(self.chosenmodel, self.rec)
        ans = \
        len( range(
             int(spikes[self.regionslist_str[0]].t_start.magnitude),
             int(spikes[self.regionslist_str[0]].t_stop.magnitude/parameters["dt"])
              ) ) + 1 # for the additional dt step
        self.assertEqual( ans, len(self.rec["time"]) )
        os.chdir(self.pwd) # reset to the location of this converterTest.py

    #@unittest.skip("reason for skipping")
    def test_4_voltage_to_spiketrain_with_stimulation(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in parent /cerebmodels
        parameters = {"dt": 0.1, "celsius": 20, "tstop": 10, "v_init": 65}
        currparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {'amp': 0.5, 'dur': 10.0, 'delay': 5.0},
                                        {'amp': 1.0, 'dur': 20.0, 'delay': 5.0+10.0} ] }
        self.sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimuli_list = self.sm.stimulate_model_NEURON(stimparameters = currparameters,
                                               modelsite = self.chosenmodel.cell.soma)
        self.rec["time"], self.rec["response"], self.rec["stimulus"] = \
                 self.rm.prepare_recording_NEURON(self.chosenmodel)
        self.sm.engage_NEURON()
        spikes = self.co.voltage_to_spiketrain(self.chosenmodel, self.rec)
        ans = \
        len( range(
             int(spikes[self.regionslist_str[0]].t_start.magnitude),
             int(spikes[self.regionslist_str[0]].t_stop.magnitude/parameters["dt"])
              ) ) + 1 # for the additional dt step
        self.assertEqual( ans, len(self.rec["time"]) )
        os.chdir(self.pwd) # reset to the location of this converterTest.py

if __name__ == '__main__':
    unittest.main()

