# ../managers/managerRecordTest.py
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


class RecordManagerTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell() #for alternative approach see managerSimulationTest.py
        os.chdir(pwd)
        self.regionslist_str = list(self.chosenmodel.regions.keys())

    #@unittest.skip("reason for skipping")
    def test_1_prepare_recording_NEURON_without_stimulating(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        rec_t, rec_v, rec_reg, x = rm.prepare_recording_NEURON(self.chosenmodel)
        sm.engage_NEURON()
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(rec_v["soma"]),#len(rec_v[self.regionslist_str[0]]),
                          2*total_iterations )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    @unittest.skip("reason for skipping")
    def test_2_prepare_recording_NEURON_without_stimulating_multiple_sections(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        rec_t, rec_v, rec_reg, x = rm.prepare_recording_NEURON(self.chosenmodel)
        sm.engage_NEURON()
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(rec_v["soma"]) #len(rec_v[self.regionslist_str[0]])
                                     + len(rec_v["axon"]),#len(rec_v[self.regionslist_str[1]]),
                          3*total_iterations )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    @unittest.skip("reason for skipping")
    def test_3_prepare_recording_NEURON_without_stimulating_but_evoke_stimulate_model(self):
        os.chdir(rootwd) # move up to load the model
        # pick the modelstimtype = currparameters["type"]
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimulate_not = sm.stimulate_model_NEURON()
        rec_t, rec_v, rec_reg, x = rm.prepare_recording_NEURON(self.chosenmodel,
                                                               stimuli = stimulate_not)
        sm.engage_NEURON()
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(rec_v["soma"]),#len(rec_v[self.regionslist_str[0]]),
                          2*total_iterations )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    @unittest.skip("reason for skipping")
    def test_4_prepare_recording_NEURON_currentclamp(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        currparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {'amp': 0.5, 'dur': 10.0, 'delay': 5.0},
                                        {'amp': 1.0, 'dur': 20.0, 'delay': 5.0+10.0} ],
                          "tstop": parameters["tstop"] }
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimuli_list = sm.stimulate_model_NEURON(stimparameters = currparameters,
                                               modelsite = self.chosenmodel.cell.soma)
        rec_t, rec_v, rec_reg, rec_i_indivs = rm.prepare_recording_NEURON(
                                                           self.chosenmodel,
                                                           stimuli = stimuli_list,
                                                           stimtype = currparameters["type"] )
        sm.engage_NEURON()
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(rec_v["soma"]) #len(rec_v[self.regionslist_str[0]])
                                     + len(rec_i_indivs),
                          2*total_iterations + len( currparameters["stimlist"] ) )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    @unittest.skip("reason for skipping")
    def test_5_prepare_recording_NEURON_voltageclamp(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        injparameters = {"type": ["voltage", "SEClamp"],
                         "stimlist": [ {'amp1': 0., 'dur1': 10.0},
                                       {'amp2': -70.0, 'dur2': 20.0} ],
                         "tstop": parameters["tstop"] }
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        vstimuli = sm.stimulate_model_NEURON(stimparameters = injparameters,
                                             modelsite = self.chosenmodel.cell.soma)
        rec_t, rec_v, rec_reg, rec_v_stim = rm.prepare_recording_NEURON(
                                                         self.chosenmodel,
                                                         stimuli = vstimuli,
                                                         stimtype = injparameters["type"] )
        sm.engage_NEURON()
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertEqual( [ len(rec_t) + len(rec_v["soma"]),#len(rec_v[self.regionslist_str[0]]),
                            rec_v_stim.amp1, rec_v_stim.dur1, rec_v_stim.amp2, rec_v_stim.dur2 ],
                          [ 2*total_iterations, injparameters["stimlist"][0]["amp1"],
                            injparameters["stimlist"][0]["dur1"],
                            injparameters["stimlist"][1]["amp2"],
                            injparameters["stimlist"][1]["dur2"] ] )
        #self.assertEqual( len(rec_t) + len(rec_v["soma"]),#len(rec_v[self.regionslist_str[0]]),
        #                  2*total_iterations )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    @unittest.skip("reason for skipping")
    def test_6_postrun_recording_NEURON_without_stimulating(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimuli_list = sm.stimulate_model_NEURON()
        rec_t, rec_v, rec_reg, rec_i_indivs = rm.prepare_recording_NEURON(
                                                         self.chosenmodel,
                                                         stimuli = stimuli_list )
        sm.engage_NEURON()
        rec_i = rm.postrun_record_NEURON( injectedstimuli =  rec_i_indivs)
        self.assertEqual( rm.postrun_record_NEURON(),
                          "Model is not stimulated" )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    @unittest.skip("reason for skipping")
    def test_7_postrun_recording_NEURON_currentclamp(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        currparameters = {"type": ["current", "IRamp"],
           "stimlist": [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                         {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                         {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                         {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ] }
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        stimuli_list = sm.stimulate_model_NEURON(stimparameters = currparameters,
                                               modelsite = self.chosenmodel.cell.soma)
        rec_t, rec_v, rec_reg, rec_i_indivs = rm.prepare_recording_NEURON(
                                                         self.chosenmodel,
                                                         stimuli = stimuli_list,
                                                         stimtype = currparameters["type"] )
        sm.engage_NEURON()
        rec_i = rm.postrun_record_NEURON( injectedstimuli = rec_i_indivs,
                                          stimtype = currparameters["type"] )
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        self.assertEqual( len(rec_t) + len(rec_v["soma"])#len(rec_v[self.regionslist_str[0]])
                                     + len(rec_i),
                          3*total_iterations )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

    @unittest.skip("reason for skipping")
    def test_8_postrun_recording_NEURON_voltageclamp(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        injparameters = {"type": ["voltage", "SEClamp"],
                         "stimlist": [ {"amp1": 0.0, "dur1": 10},
                                       {"amp2": 10, "dur2": 20},
                                       {"amp3": 20, "dur3": 30} ],
                         "tstop": parameters["tstop"] }
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=self.chosenmodel)
        vstimuli = sm.stimulate_model_NEURON(stimparameters = injparameters,
                                             modelsite = self.chosenmodel.cell.soma)
        rec_t, rec_v, rec_reg, rec_v_stim = rm.prepare_recording_NEURON(
                                                         self.chosenmodel,
                                                         stimuli = vstimuli,
                                                         stimtype = injparameters["type"] )
        sm.engage_NEURON()
        rec_v_stim = rm.postrun_record_NEURON( injectedstimuli = rec_v_stim,
                                               stimtype = injparameters["type"] )
        print(len(rec_t), len(rec_v), len(rec_v["soma"]), len(rec_reg))
        print(len(rec_v["channels"]))
        print(len(rec_v["channels"]["soma"]))
        print(len(rec_v["channels"]["soma"]["pas"]))
        total_iterations = len( range(-1, int(parameters["tstop"]/parameters["dt"])) )
        #print(len(rec_v), len(rec_reg))
        self.assertEqual( len(rec_t) + len(rec_v["soma"])#len(rec_v[self.regionslist_str[0]])
                                     + len(rec_v_stim),
                          3*total_iterations )
        os.chdir(pwd) # reset to the location of this managerRecordTest.py

if __name__ == '__main__':
    unittest.main()
