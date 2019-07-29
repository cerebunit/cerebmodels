# ../managers/managerRecordTest.py
import unittest
import os
import importlib

from collections import Counter

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

import numpy as np

class RecordManagerTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell() #for alternative approach see managerSimulationTest.py
        os.chdir(pwd)
        #self.regionslist_str = list(self.chosenmodel.regions.keys())
        self.no_parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        self.ic_parameters = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        self.ic_stimparam = {"type": ["current", "IClamp"],
                         "stimlist": [ {'amp': 0.5, 'dur': 10.0, 'delay': 5.0},
                                       {'amp': 1.0, 'dur': 20.0, 'delay': 5.0+10.0} ],
                            "tstop": self.ic_parameters["tstop"] }
        self.sec_parameters = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        self.sec_stimparam = {"type": ["voltage", "SEClamp"],
                          "stimlist": [ {'amp1': 0., 'dur1': 10.0},
                                       {'amp2': -70.0, 'dur2': 20.0} ],
                             "tstop": self.sec_parameters["tstop"] }
        self.ir_parameters = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        self.ir_stimparam = {"type": ["current", "IRamp"],
           "stimlist": [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                         {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                         {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                         {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ],
           "tstop": self.ir_parameters["tstop"] }

    #@unittest.skip("reason for skipping")
    def test_1_recordings_of_cellular_regionbodies_NEURON(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        sm.prepare_model_NEURON(parameters=self.no_parameters, chosenmodel=self.chosenmodel)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        recs = rm.recordings_of_cellular_regionbodies_NEURON(self.chosenmodel)
        sm.engage_NEURON()
        total_iterations = len( range(-1,
                                int(self.no_parameters["tstop"]/self.no_parameters["dt"])) )
        a = ( Counter( list(recs["soma"][0]) ) != Counter( list(recs["axon"][0]) ) )
        self.assertEqual( [ len(recs["soma"][0]), a ],
                          [ total_iterations, True ] )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_2_recordings_of_cellular_componenets_NEURON(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        sm.prepare_model_NEURON(parameters=self.no_parameters, chosenmodel=self.chosenmodel)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        recs = rm.recordings_of_cellular_components_NEURON(self.chosenmodel)
        sm.engage_NEURON()
        a = ( Counter( list(recs["channels"]["soma"]["hh"][0]) ) !=
              Counter( list(recs["channels"]["soma"]["hh"][1]) ) )
        b = ( Counter( list(recs["channels"]["soma"]["pas"][0]) ) !=
              Counter( list(recs["channels"]["axon"]["pas"][0]) ) )
        self.assertEqual( [ a, b ], [ True, True ] )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_3_prepare_recording_NEURON_without_stimulating(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        sm.prepare_model_NEURON(parameters=self.no_parameters, chosenmodel=self.chosenmodel)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        rec_t, recs, x = rm.prepare_recording_NEURON(self.chosenmodel)
        sm.engage_NEURON()
        a = ( Counter( list(recs["soma"][0]) ) != Counter( list(recs["axon"][0]) ) )
        b = ( Counter( list(recs["channels"]["soma"]["pas"][0]) ) !=
              Counter( list(recs["channels"]["axon"]["pas"][0]) ) )
        total_iterations = len( range(-1,
                                int(self.no_parameters["tstop"]/self.no_parameters["dt"])) )
        self.assertEqual( [len(rec_t), a, b], [total_iterations,  True, True] )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_4_prepare_recording_NEURON_without_stimulating_but_evoke_stimulate_model(self):
        os.chdir(rootwd) # move up to load the model
        # pick the modelstimtype = currparameters["type"]
        sm.prepare_model_NEURON(parameters=self.no_parameters, chosenmodel=self.chosenmodel)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        stimulate_not = sm.stimulate_model_NEURON()
        rec_t, recs, x = rm.prepare_recording_NEURON(self.chosenmodel,
                                                     stimuli = stimulate_not)
        sm.engage_NEURON()
        a = ( Counter( list(recs["soma"][0]) ) !=
              Counter( list(recs["channels"]["soma"]["pas"][0]) ) )
        b = ( Counter( list(recs["axon"][0]) ) !=
              Counter( list(recs["channels"]["axon"]["pas"][0]) ) )
        total_iterations = len( range(-1,
                                int(self.no_parameters["tstop"]/self.no_parameters["dt"])) )
        self.assertEqual( [len(rec_t), a, b], [total_iterations,  True, True] )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_5_prepare_recording_NEURON_currentclamp(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        sm.prepare_model_NEURON(parameters=self.ic_parameters, chosenmodel=self.chosenmodel)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        stimuli_list = sm.stimulate_model_NEURON(stimparameters = self.ic_stimparam,
                                                 modelsite = self.chosenmodel.cell.soma)
        rec_t, recs, rec_i_indivs = rm.prepare_recording_NEURON(
                                                 self.chosenmodel,
                                                 stimuli = stimuli_list,
                                                 stimtype = self.ic_stimparam["type"] )
        sm.engage_NEURON()
        total_iterations = len( range(-1,
                             int(self.ic_parameters["tstop"]/self.ic_parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(recs["soma"][0]) + len(rec_i_indivs),
                          2*total_iterations + len( self.ic_stimparam["stimlist"] ) )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_6_prepare_recording_NEURON_voltageclamp(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        sm.prepare_model_NEURON(parameters=self.sec_parameters, chosenmodel=self.chosenmodel)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        vstimuli = sm.stimulate_model_NEURON(stimparameters = self.sec_stimparam,
                                             modelsite = self.chosenmodel.cell.soma)
        rec_t, recs, rec_v_stim = rm.prepare_recording_NEURON(
                                             self.chosenmodel,
                                             stimuli = vstimuli,
                                             stimtype = self.sec_stimparam["type"] )
        sm.engage_NEURON()
        total_iterations = len( range(-1,
                                int(self.sec_parameters["tstop"]/self.sec_parameters["dt"])) )
        self.assertEqual( [ len(rec_t) + len(recs["soma"][0]),
                            rec_v_stim.amp1, rec_v_stim.dur1, rec_v_stim.amp2, rec_v_stim.dur2 ],
                          [ 2*total_iterations, self.sec_stimparam["stimlist"][0]["amp1"],
                            self.sec_stimparam["stimlist"][0]["dur1"],
                            self.sec_stimparam["stimlist"][1]["amp2"],
                            self.sec_stimparam["stimlist"][1]["dur2"] ] )
        #self.assertEqual( len(rec_t) + len(rec_v["soma"]),#len(rec_v[self.regionslist_str[0]]),
        #                  2*total_iterations )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_7_postrun_recording_NEURON_without_stimulating(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        sm.prepare_model_NEURON(parameters=self.no_parameters, chosenmodel=self.chosenmodel)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        stimuli_list = sm.stimulate_model_NEURON()
        rec_t, recs, rec_i_indivs = rm.prepare_recording_NEURON(
                                                         self.chosenmodel,
                                                         stimuli = stimuli_list )
        sm.engage_NEURON()
        rec_i = rm.postrun_record_NEURON( injectedstimuli =  rec_i_indivs)
        self.assertEqual( rm.postrun_record_NEURON(), "Model is not stimulated" )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_8_postrun_recording_NEURON_currentclamp(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        sm.prepare_model_NEURON(parameters=self.ir_parameters, chosenmodel=self.chosenmodel)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        stimuli_list = sm.stimulate_model_NEURON(stimparameters = self.ir_stimparam,
                                               modelsite = self.chosenmodel.cell.soma)
        rec_t, recs, rec_i_indivs = rm.prepare_recording_NEURON(
                                               self.chosenmodel,
                                               stimuli = stimuli_list,
                                               stimtype = self.ir_stimparam["type"] )
        sm.engage_NEURON()
        rec_i = rm.postrun_record_NEURON( injectedstimuli = rec_i_indivs,
                                          stimtype = self.ir_stimparam["type"] )
        total_iterations = len( range(-1,
                                int(self.ir_parameters["tstop"]/self.ir_parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(recs["soma"][0]) + len(rec_i),
                          3*total_iterations )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    #@unittest.skip("reason for skipping")
    def test_9_postrun_recording_NEURON_voltageclamp(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        sm.prepare_model_NEURON(parameters=self.sec_parameters, chosenmodel=self.chosenmodel)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        vstimuli = sm.stimulate_model_NEURON(stimparameters = self.sec_stimparam,
                                             modelsite = self.chosenmodel.cell.soma)
        rec_t, recs, rec_v_stim = rm.prepare_recording_NEURON(
                                             self.chosenmodel,
                                             stimuli = vstimuli,
                                             stimtype = self.sec_stimparam["type"] )
        sm.engage_NEURON()
        rec_v_stim = rm.postrun_record_NEURON( injectedstimuli = rec_v_stim,
                                               stimtype = self.sec_stimparam["type"] )
        total_iterations = len( range(-1,
                                int(self.sec_parameters["tstop"]/self.sec_parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(recs["soma"][0]) + len(rec_v_stim),
                          3*total_iterations )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

if __name__ == '__main__':
    unittest.main()
